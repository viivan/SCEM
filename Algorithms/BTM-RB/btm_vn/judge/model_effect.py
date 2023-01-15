# 利用主题词计算主题一致性
# 需要文档词id矩阵，主题词id的矩阵
# n为top-n词汇
import math
import data.data_file_load as dfl
import model.btm_wvf_Adapter as bwf
import os


def sort_method(element):
    # 排序用函数
    return element[0]


def cal_pmi(k, n, doc_id_matrix, topic_word_matrix):
    whole_pmi = []
    doc_num = len(doc_id_matrix)
    word_num = 0
    for doc_vec in doc_id_matrix:
        word_num += len(doc_vec)

    for i in range(k):
        topic_pmi = 0
        simple_p = []
        for j in range(n):
            # 计算p(wj)
            w_p = 0
            for doc_vec in doc_id_matrix:
                if topic_word_matrix[i][j] in doc_vec:
                    w_p += doc_vec.count(topic_word_matrix[i][j])
            p_w = w_p / word_num
            simple_p.append(p_w)
        for j in range(n-1):
            for p in range(j+1, n):
                # p(wj, wp)
                w_p = 0
                for doc_vec in doc_id_matrix:
                    if topic_word_matrix[i][j] in doc_vec:
                        if topic_word_matrix[i][p] in doc_vec:
                            j_num = doc_vec.count(topic_word_matrix[i][j])
                            p_num = doc_vec.count(topic_word_matrix[i][p])
                            if j_num > p_num:
                                w_p += j_num
                            else:
                                w_p += p_num
                p_w = w_p / word_num
                right = p_w / (simple_p[j] * simple_p[p])
                if right != 0:
                    right_pmi = math.log2(right)
                    topic_pmi += right_pmi
        topic_pmi = 2 * topic_pmi / (n * (n-1))
        print("topic{}:{}".format(i, topic_pmi))
        whole_pmi.append(topic_pmi)
    pmi = sum(whole_pmi) / k
    print(pmi)


def get_topic_word_id(k, topic_word_num):
    # 将词汇被分配次数转化成主题词id矩阵
    t_words_id = []
    for i in range(k):
        # 将对应主题的每个词和其id作为元组进行排序
        b = zip(topic_word_num[i], range(len(topic_word_num[i])))
        b = list(b)
        b.sort(key=sort_method, reverse=True)
        s_words_id = []
        for j in range(len(b)):
            s_words_id.append(b[j][1])
        t_words_id.append(s_words_id)
    return t_words_id


if __name__ == "__main__":
    t_k = 4
    t_n = 20

    doc_word_filename = "doc_wordindex_C4.txt"
    t_doc_word_id = dfl.loadWordIndexMatrix(doc_word_filename)

    filename = "C4_iterate500_threshold0.05_miu0.4_tp.txt"
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("btm_wvf\\") + len("btm_wvf\\")]
    path = os.path.abspath(rootPath + "resource\\" + filename)

    t_topic_word_num = bwf.load_Topic_word(path)
    t_topic_word_id = get_topic_word_id(t_k, t_topic_word_num)
    cal_pmi(t_k, t_n, t_doc_word_id, t_topic_word_id)
