"""
btm_vn实现
利用word2vec的阈值进行词对选取
采样过程中利用代表词对进行权重的控制
"""
import numpy as np
import os
import data.data_file_load as dfl
import random
import time
import model.biterm as biterm
import cluster.kmeans as kmn
import judge.whole_cluster_result as wce
import data.data_util as du
 
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("btm_vn\\") + len("btm_vn\\")]


def sort_method(element):
    # 排序用函数
    return element[0]


def write_Doc_Topic_Matrix(distribution, filename):
    # 文档主题分布矩阵,写入文件
    # 获取路径信息
    path = os.path.abspath(rootPath + "resource\\" + filename)

    pf = open(path, "w+")
    for dis in distribution:
        str_single = ""
        for d in dis:
            str_single += str(d)+" "
        pf.writelines(str_single[0:len(str_single)-1]+"\n")
    pf.close()


def load_Doc_Topic_Matrix(save_path):
    # 读取文档分布矩阵
    try:
        pf = open(save_path, "r+")
        result = []  # 存放文档分布
        lines = pf.readlines()
        for line in lines:
            line = line.strip()
            nums = line.split(" ")
            result.append([float(i) for i in nums])
        pf.close()
        return result
    except IOError:
        print("文件无法正常打开")
        return None


def write_Topic_word(distribution, filename):
    # 被每个词分配到每个主题的次数记录下来
    # 获取路径信息
    path = os.path.abspath(rootPath + "resource\\" + filename)

    pf = open(path, "w+")
    for dis in distribution:
        str_single = ""
        for d in dis:
            str_single += str(d)+" "
        pf.writelines(str_single[0:len(str_single)-1]+"\n")
    pf.close()


def load_Topic_word(save_path):
    # 读取每个词分配到每个主题的次数
    try:
        pf = open(save_path, "r+")
        topic_word = []  # 存放topic_word
        lines = pf.readlines()
        for line in lines:
            line = line.strip()
            nums = line.split(" ")
            topic_word.append([float(i) for i in nums])
        pf.close()
        return topic_word
    except IOError:
        print("文件无法正常打开")
        return None


class BtmVnModel:
    k = 10  # 主题数

    doc_word_id = []  # doc中的词映射为id
    doc_biterms = []  # biterms词组合
    topic_sum = []  # 对应主题biterm数
    topic_word = []  # 主题-词数量矩阵
    voc_list = []  # 词汇表list
    word_sim_matrix = []  # 词对相似度矩阵
    S = []  # 相关词对升阶计算
    count = 0  # 存放biterm的数量

    iterate = 500  # 迭代次数
    threshold = 0.3  # 相似度阈值

    def __init__(self, k, doc_word_id, voc_list, word_sim_matrix, iterate=100, threshold=0.3, miu=0.2, ber=0.3):
        self.k = k
        self.alpha = 50 / self.k
        self.beta = 0.1

        self.doc_word_id = doc_word_id
        self.voc_list = voc_list
        self.word_sim_matrix = word_sim_matrix
        self.iterate = iterate
        self.threshold = threshold
        self.miu = miu
        self.ber = ber

        # 可能多次使用，归零
        self.doc_biterms = []
        self.topic_sum = []
        self.topic_word = []
        self.S = []

    def select_biterm(self):
        # 创建词对，并返回接收与剔除标记
        accept_label = []
        biterms = []
        a = 0  # 保存数量
        d = 0  # 删去数量
        t = 0  # 序号
        for doc_simple in self.doc_word_id:
            for i in range(len(doc_simple) - 1):
                for j in range(i + 1, len(doc_simple)):
                    sim = self.word_sim_matrix[doc_simple[i]][doc_simple[j]]
                    if sim >= self.threshold:
                        biterms.append(biterm.Biterm(t, doc_simple[i], doc_simple[j]))
                        a += 1
                        t += 1
                        accept_label.append(1)
                    else:
                        biterms.append(biterm.Biterm(t, doc_simple[i], doc_simple[j]))
                        d += 1
                        t += 1
                        accept_label.append(0)
        return accept_label, biterms

    def init_biterm(self):
        # 初始化词对
        # 通过词对相似度与阈值进行词对选取
        t = 0
        for doc_simple in self.doc_word_id:
            biterm_single = []
            for i in range(len(doc_simple) - 1):
                for j in range(i + 1, len(doc_simple)):
                    sim = self.word_sim_matrix[doc_simple[i]][doc_simple[j]]
                    if sim >= self.threshold:
                        biterm_single.append(biterm.Biterm(t, doc_simple[i], doc_simple[j]))
                        t += 1
                    else:
                        pass
            self.doc_biterms.append(biterm_single)
        # 总数
        count = 0
        for i in self.doc_biterms:
            count += len(i)
        print("count:{}".format(count))
        self.count = count

    def init_matrix(self):
        # 初始化主题——词矩阵和文档——主题矩阵
        self.topic_sum = [0] * self.k
        self.topic_word = np.zeros((self.k, len(self.voc_list)))
        # 对biterm随机赋值topic
        for bit_arr in self.doc_biterms:
            for bit in bit_arr:
                topic = random.randint(0, self.k - 1)  # randint会输出边界值，所以-1
                bit.topic = topic
                self.topic_sum[topic] += 2
                self.topic_word[topic][bit.word1] += 1
                self.topic_word[topic][bit.word2] += 1

    def cal_word_probability(self, word_index0, word_index1):
        # 根据公式计算每个biterm在所有topic中的rt可能性
        simple_p = []
        # 对每个主题进行计算,因为要获取比值，所以直接计算上半部分即可
        for i in range(self.k):
            left = (self.topic_sum[i] + self.alpha) / (self.count + self.k * self.alpha)
            right0 = (self.topic_word[i][word_index0] / self.topic_sum[i])
            right1 = (self.topic_word[i][word_index1] / self.topic_sum[i])
            simple_p.append(left * right0 * right1)
        b_lambda = []
        for i in range(self.k):
            lam = simple_p[i] / max(simple_p)
            b_lambda.append(lam)
        return b_lambda

    def cal_s(self):
        self.S = []
        # 计算rt的升阶矩阵
        biterm_lambda_matrix = []
        for bit_arr in self.doc_biterms:
            for b in bit_arr:
                simple_lambda = self.cal_word_probability(b.word1, b.word2)
                biterm_lambda_matrix.append(simple_lambda)
        # 计算S,0-1分布
        la_count = 0
        for s_l in biterm_lambda_matrix:
            simple_s = []
            for la in s_l:
                if la > self.ber:
                    simple_s.append(1)
                else:
                    simple_s.append(0)
                la_count += la
            self.S.append(simple_s)
        print("likelihood:{}".format(la_count))

    def updateBiterm(self, bit, loop_index):
        # 处理每个biterm,根据S进行处理
        topic = bit.topic
        self.topic_sum[topic] -= 2
        self.topic_word[topic][bit.word1] -= 1
        self.topic_word[topic][bit.word2] -= 1
        # 采样
        topic = self.sampling(bit, loop_index)
        # 更新
        bit.topic = topic
        self.topic_sum[topic] += 2
        self.topic_word[topic][bit.word1] += 1
        self.topic_word[topic][bit.word2] += 1

    def sampling(self, bit, loop_index):
        # 采样
        # 获取概率分布,根据S进行数量的变化
        distribution = [0.0] * self.k
        bit_index = bit.index
        if loop_index == 0:
            for i in range(self.k):
                # 采样公式（一会补上）(重点)
                left = self.topic_sum[i] + self.alpha
                up = (self.topic_word[i][bit.word1] + self.beta) * (self.topic_word[i][bit.word2] + self.beta)
                under = (self.topic_sum[i] + len(self.voc_list) * self.beta) * \
                        (self.topic_sum[i] + len(self.voc_list) * self.beta)
                distribution[i] = left * up / under
        else:
            for i in range(self.k):
                if self.S[bit_index][i] == 0:
                    # 采样公式
                    left = self.topic_sum[i] + self.alpha
                    up = (self.topic_word[i][bit.word1] + self.beta) * (self.topic_word[i][bit.word2] + self.beta)
                    under = (self.topic_sum[i] + len(self.voc_list) * self.beta) * \
                            (self.topic_sum[i] + len(self.voc_list) * self.beta)
                    distribution[i] = left * up / under
                else:
                    # 采样公式, 增加数量
                    left = self.topic_sum[i] + self.alpha
                    up = (self.topic_word[i][bit.word1] * (1 + self.miu) + self.beta) * \
                         (self.topic_word[i][bit.word2] * (1 + self.miu) + self.beta)
                    under = (self.topic_sum[i] * (1 + self.miu * 2) + len(self.voc_list) * self.beta) * \
                            (self.topic_sum[i] * (1 + self.miu * 2) + len(self.voc_list) * self.beta)
                    distribution[i] = left * up / under

        # print(distribution)
        # 按分布随机获取主题
        for i in range(len(distribution)):
            if i == 0:
                continue
            distribution[i] = distribution[i - 1] + distribution[i]
        ran = random.random()
        # print(distribution, ran)
        for i in range(len(distribution)):
            if ran * distribution[self.k - 1] <= distribution[i]:
                return i

    def buildModel(self):
        print("初始化biterms------")
        self.init_biterm()  # 初始化biterm
        print("初始化统计信息------")
        self.init_matrix()  # 初始化矩阵,biterms_topic数据
        # 开始迭代
        print("开始迭代------")
        for i in range(self.iterate):
            start_time = time.time()
            print("iterate {}".format(i))
            for di in range(len(self.doc_biterms)):
                for bi in range(len(self.doc_biterms[di])):
                    self.updateBiterm(self.doc_biterms[di][bi], i)
            # 计算S
            self.cal_s()
            end_time = time.time()
            total_time = (end_time - start_time) * 1000
            print("iterate time:{} ms".format(total_time))

    def cal_likelihood(self):
        # 计算似然度，观察收敛
        ll = 1
        for i in range(len(self.voc_list)):
            for j in range(len(self.voc_list)):
                w_ij = 0
                for z in range(self.k):
                    left = (self.topic_sum[z] + self.alpha) / (self.count + self.k * self.alpha)
                    right0 = (self.topic_word[z][i] + self.beta) / (self.topic_sum[z] + len(self.voc_list) * self.beta)
                    right1 = (self.topic_word[z][j] + self.beta) / (self.topic_sum[z] + len(self.voc_list) * self.beta)
                    s_ll = left * right0 * right1
                    w_ij += s_ll
                if w_ij != 0:
                    ll += w_ij
        return ll

    def getDoc_Topic(self):
        # 输出文档主题分布
        distribution = []
        for biterm_doc in self.doc_biterms:
            doc_topic_dis = [0.0] * self.k
            bit_count = len(biterm_doc)
            for bit_in in biterm_doc:
                topic_distribution = [0.0] * self.k
                for i in range(self.k):
                    if self.S[bit_in.index][i] == -1:
                        # 采样公式
                        left = (self.topic_word[i][bit_in.word1] * (1 + self.miu) + self.beta) \
                               / (self.topic_sum[i] + len(self.voc_list) * self.beta)
                        right = (self.topic_word[i][bit_in.word2] * (1 + self.miu) + self.beta) \
                               / (self.topic_sum[i] + len(self.voc_list) * self.beta + 1)
                        middle = (self.topic_sum[i] + self.alpha) * (1 + 2 * self.miu) / (len(self.doc_biterms) + self.k * self.alpha)
                        topic_distribution[i] = left * middle * right
                    else:
                        # 采样公式
                        left = (self.topic_word[i][bit_in.word1] + self.beta) \
                               / (self.topic_sum[i] + len(self.voc_list) * self.beta)
                        right = (self.topic_word[i][bit_in.word2] + self.beta) \
                               / (self.topic_sum[i] + len(self.voc_list) * self.beta + 1)
                        middle = (self.topic_sum[i] + self.alpha) / (len(self.doc_biterms) + self.k * self.alpha)
                        topic_distribution[i] = left * middle * right

                dis_sum = sum(topic_distribution)
                for i in range(self.k):
                    topic_distribution[i] /= dis_sum
                for i in range(self.k):
                    doc_topic_dis[i] += topic_distribution[i] / bit_count
            distribution.append(doc_topic_dis)
        return distribution

    def getTopic_word(self, num=5):
        # 获取出现次数最多的主题词
        # 输出每个主题中出现次数最多的词
        t_words = []
        for i in range(self.k):
            # 将对应主题的每个词和其id作为元组进行排序
            b = zip(self.topic_word[i], range(len(self.topic_word[i])))
            b = list(b)
            b.sort(key=sort_method, reverse=True)
            print("topic {}".format(i))
            s_words = []
            for j in range(len(b)):
                if j < num:
                    s_words.append(self.voc_list[b[j][1]])
                    print(self.voc_list[b[j][1]], "概率:{}".format(b[j][0] / sum(self.topic_word[i])))
                else:
                    break
            t_words.append(s_words)
        return t_words


if __name__ == "__main__":
    t_k = 10
    t_iterate = 500
    t_threshold = 0.2
    t_miu = 0.2

    doc_word_filename = "doc_wordindex_C10.txt"
    voc_filename = "vocabulary_C10.txt"
    word_sim_filename = "word_sim_C10.txt"
    t_doc_word_id = dfl.loadWordIndexMatrix(doc_word_filename)
    t_voc_list = dfl.loadVocabularyList(voc_filename)
    t_word_sim_matrix = dfl.loadWordSimMatrix(word_sim_filename)

    print("开始模型训练")
    b_model = BtmVnModel(t_k, t_doc_word_id, t_voc_list, t_word_sim_matrix,
                          iterate=t_iterate, threshold=t_threshold, miu=t_miu)
    b_model.buildModel()
    print("训练完成")

    dis = b_model.getDoc_Topic()
    print("完成文档主题文档获取")

    cluster_result = kmn.kMeansByFeature(t_k, dis).labels_
    former_type = du.getFormerCategory("C10.csv")
    result = wce.printResult(t_k, cluster_result, former_type)
    print(result)

    # t_word = b_model.getTopic_word(10)

    suffix = voc_filename[str(voc_filename).rindex("_") + 1:str(voc_filename).rindex(".")]
    dis_save = "{}_iterate{}_threshold{}_miu{}_result.txt".format(suffix, t_iterate, t_threshold, t_miu)
    tp_save = "{}_iterate{}_threshold{}_miu{}_tp.txt".format(suffix, t_iterate, t_threshold, t_miu)
    # write_Doc_Topic_Matrix(dis, dis_save)
    # write_Topic_word(b_model.topic_word, tp_save)
