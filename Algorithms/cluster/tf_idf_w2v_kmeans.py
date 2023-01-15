import model.TF_IDFAdapter as tfidf
import model.word2vecAdapter as w2v
import cluster.kmeans as kmn
import numpy as np
"""
利用tf_idf来对经过word2vec训练后产生的词向量加工
获取文档的对应向量
利用该向量进行聚类处理
""" 


def clusterResult(doc={}, num=3, save_path=r"", result_save=False):
    # 处理文档，返回聚类标签
    word_list, weight = tfidf.cal_tf_idf(doc)
    model = w2v.load_model_binary(save_path)
    print("开始生成vec_list")
    vec_list = w2v.wordlist_to_vec(model, word_list)  # 二维矩阵

    print("完成生成vec_list,计算doc_vec")
    # 每个文档进行处理,生成向量
    doc_vec = []
    t = 0
    for doc_weight in weight:
        if t % 10 == 0:
            print("turn", t)
        t += 1
        doc_vec_list = []
        for i in range(len(doc_weight)):
            mul = doc_weight[i]
            doc_vec_list.append([x * mul for x in vec_list[i]])

        simple_vec = np.array([0.0] * len(doc_vec_list[0]))
        for vec in doc_vec_list:
            # 使用np进行矩阵相加
            simple_vec += np.array(vec)
        simple_vec = list(simple_vec)
        doc_vec.append(simple_vec)

    if result_save:
        save_dv(doc_vec)

    # 进行聚类
    estimator = kmn.kMeansByFeature(num, doc_vec)
    labels = list(estimator.labels_)

    return labels


def clusterResultByFile(num=3):
    # 直接从文件中读取分布信息计算
    doc_vec = load_dv()

    estimator = kmn.kMeansByFeature(num, doc_vec)
    labels = list(estimator.labels_)

    return labels


def save_dv(distribution):
    # 保存结果
    pf = open(r"E:\pyProject\resource\tf_idf_w2v.txt", "r+")
    for dis in distribution:
        str_single = ""
        for d in dis:
            str_single += str(d)+" "
        pf.writelines(str_single[0:len(str_single)-1]+"\n")
    pf.close()


def load_dv(save_path=r"E:\pyProject\resource\tf_idf_w2v.txt"):
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
