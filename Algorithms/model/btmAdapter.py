import numpy as np
import os
import data.data_util as du
from model import Biterm
import random
import time

'''
实现btm主题模型
关键是gibbs采样流程 
传入参数为对应的文档dictionary
'''


def sort_method(element):
    return element[0]


def writeResult(distribution, filename):
    # 写入结果
    # distribution就是文档主题分布矩阵

    # 获取路径信息
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("ServiceCluster\\") + len("ServiceCluster\\")]
    path = os.path.abspath(rootPath + "resource\\" + filename)

    pf = open(path, "w+")
    for dis in distribution:
        str_single = ""
        for d in dis:
            str_single += str(d)+" "
        pf.writelines(str_single[0:len(str_single)-1]+"\n")
    pf.close()


def loadModel(save_path):
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


class BtmModel:
    doc = {}
    name = []  # 存对应的文档名，便于之后确认
    id_word_dic = {}  # 词典，id-word对
    word_dic = {}  # 词典，word-id对
    word_fre = {}  # word frequently
    doc_word_id = []  # doc中的词映射为id
    wordlist = []  # doc 词集合
    biterms = []  # biterms词组合
    topic_sum = []  # 对应主题biterm数
    topic_word = []  # 主题-词矩阵

    def __init__(self, num, doc={}):
        self.k = num
        self.alpha = 50 / self.k
        self.beta = 0.1
        self.iterate = 500  # 迭代次数
        self.doc = doc
        self.name = []
        self.id_word_dic = {}  # 词典，id-word对
        self.word_dic = {}  # 词典，word-id对
        self.word_fre = {}  # word frequently
        self.doc_word_id = []  # doc中的词映射为id
        self.wordlist = []  # doc 词集合
        self.biterms = []  # biterms词组合
        self.topic_sum = []  # 对应主题biterm数
        self.topic_word = []  # 主题-词矩阵

    def init_dic_freq(self):
        # 初始化词典和词频率，频率归一化
        self.wordlist = []
        for k in self.doc:
            # document为list，包含预处理后的词
            doc_value = self.doc[k]
            self.name.append(k)
            words = str(doc_value).split(" ")
            self.wordlist.append(words)

        index = 0
        for words in self.wordlist:
            for word in words:
                # 未出现过的词赋index并存入字典
                if not (word in self.word_dic):
                    self.word_dic[word] = index
                    self.id_word_dic[index] = word
                    index += 1

                # 增加该词出现的次数
                word_index = self.word_dic[word]
                if word_index in self.word_fre:
                    self.word_fre[word_index] += 1
                else:
                    # 新词
                    self.word_fre[word_index] = 1

        # 归一化
        whole_val = sum(self.word_fre.values())  # 词语总数
        smooth_val = 0.001  # 平滑参数
        for key in self.word_fre:
            self.word_fre[key] = (self.word_fre[key] + smooth_val) / (whole_val + smooth_val * (self.k + 1))

    def init_docWordTo_id(self):
        # 将doc中的词映射到dictionary中的id
        for words in self.wordlist:
            doc_simple = []
            for word in words:
                doc_simple.append(self.word_dic[word])
            self.doc_word_id.append(doc_simple)

    def init_biterm(self):
        # biterm为每个词和其它词的组合，数量为(n-1)!
        print(self.doc_word_id)
        for doc_simple in self.doc_word_id:
            biterm_single = []
            for i in range(len(doc_simple) - 1):
                # 和剩下的词语进行组合
                for j in range(i + 1, len(doc_simple)):
                    biterm_single.append(Biterm.Biterm(doc_simple[i], doc_simple[j]))
            self.biterms.append(biterm_single)
        # print(self.biterms)
        count = 0
        for i in self.biterms:
            count += len(i)
        print("count:{}".format(count))

    def init_matrix(self):
        # 初始化主题——词矩阵和文档——主题矩阵的内存
        self.topic_sum = [0] * self.k
        self.topic_word = np.zeros((self.k, len(self.word_dic)))  # 默认为float
        # 对biterm随机赋值topic
        for bit_arr in self.biterms:
            for bit in bit_arr:
                topic = random.randint(0, self.k - 1)  # randint会输出边界值，所以-1
                bit.topic = topic
                self.topic_sum[topic] += 1
                self.topic_word[topic][bit.word1] += 1
                self.topic_word[topic][bit.word2] += 1

    def updateBiterm(self, bit):
        # 处理每个biterm（矩阵减去该biterm，采样，概率得新topic，赋值，矩阵加上）
        topic = bit.topic
        self.topic_sum[topic] -= 1
        self.topic_word[topic][bit.word1] -= 1
        self.topic_word[topic][bit.word2] -= 1
        # 采样
        topic = self.sampling(bit)
        # 更新
        bit.topic = topic
        self.topic_sum[topic] += 1
        self.topic_word[topic][bit.word1] += 1
        self.topic_word[topic][bit.word2] += 1

    def sampling(self, bit):
        # 获取概率分布
        distribution = [0.0] * self.k
        for i in range(self.k):
            # 采样公式（一会补上）(重点)
            left = self.topic_sum[i] + self.alpha
            up = (self.topic_word[i][bit.word1] + self.beta) * (self.topic_word[i][bit.word2] + self.beta)
            under = (2 * self.topic_sum[i] + len(self.word_dic) * self.beta) * \
                    (2 * self.topic_sum[i] + len(self.word_dic) * self.beta)
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
        print("初始化文档字典------")
        self.init_dic_freq()  # 初始化文档词典
        print("进行id映射------")
        self.init_docWordTo_id()  # id映射
        print("初始化biterms------")
        self.init_biterm()  # 初始化biterm
        print("初始化统计信息------")
        self.init_matrix()  # 初始化矩阵,biterms_topic数据
        # 开始迭代
        print("开始迭代------")
        for i in range(self.iterate):
            print("迭代次数：{}".format(i))
            for bit_arr in self.biterms:
                for bit in bit_arr:
                    self.updateBiterm(bit)
        # 此时topic_word_sum矩阵完成，计算主题词分布矩阵和文档主题分布矩阵

    def printTopic_word(self, num=5):
        # 输出每个主题中出现次数最多的词
        t_words = []
        for i in range(self.k):
            # 计划输出概率
            b = zip(self.topic_word[i], range(len(self.topic_word[i])))  # 将对应主题的每个词和其id作为元组进行排序
            b = list(b)
            b.sort(key=sort_method, reverse=True)
            print("topic {}".format(i))
            s_words = []
            for j in range(len(b)):
                if j < num:
                    s_words.append(self.id_word_dic[b[j][1]])
                    print(self.id_word_dic[b[j][1]], "概率:{}".format(b[j][0] / sum(self.topic_word[i])))
                else:
                    break
            t_words.append(s_words)
        return t_words

    def getDoc_Topic(self):
        # 输出文档主题分布
        distribution = []
        for biterm_doc in self.biterms:
            doc_topic_dis = [0.0] * self.k
            bit_count = len(biterm_doc)
            for bit_in in biterm_doc:
                topic_distribution = [0.0] * self.k
                for i in range(self.k):
                    # 采样公式（一会补上）(重点)
                    left = (self.topic_word[i][bit_in.word1] + self.beta) \
                           / (2 * self.topic_sum[i] + len(self.word_dic) * self.beta)
                    right = (self.topic_word[i][bit_in.word2] + self.beta) \
                           / (2 * self.topic_sum[i] + len(self.word_dic) * self.beta + 1)
                    middle = (self.topic_sum[i] + self.alpha) / (len(self.biterms) + self.k * self.alpha)
                    topic_distribution[i] = left * middle * right
                dis_sum = sum(topic_distribution)
                for i in range(self.k):
                    topic_distribution[i] /= dis_sum
                for i in range(self.k):
                    doc_topic_dis[i] += topic_distribution[i] / bit_count
            distribution.append(doc_topic_dis)
        return distribution


# test---------------------------test
# 返回文档doc

if __name__ == "__main__":

    file_name = "C10.csv"
    document = du.getDocAsWordArray(file_name, 5)
    doc_for_test = {}

    for name_simple in document:
        doc_for_test[name_simple] = document[name_simple]

    topic_num = 10

    start = time.perf_counter()
    model = BtmModel(topic_num, doc_for_test)
    model.buildModel()
    end = time.perf_counter()

    print("time used:{}".format(end - start))

    print("输出主题——词")
    model.printTopic_word(5)
    print()

    print("输出文档——主题")
    doc_dis = model.getDoc_Topic()
    for i in range(len(doc_dis)):
        print("文档{} ：{}".format(i, model.name[i]))
        for j in range(len(doc_dis[i])):
            print("\ttopic{}:{}".format(j, doc_dis[i][j]))

    save = "btm_result.txt"
    # 分布结果写入文件
    writeResult(doc_dis, save)
    t4 = time.perf_counter()
    print("time used:{}".format(t4 - end))