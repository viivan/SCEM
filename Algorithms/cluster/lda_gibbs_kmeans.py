import model.lda_gibbs as ldaa
import numpy as np
from cluster import kmeans as kmn

k1 = 3  # 模型主题数
k2 = 3  # 聚类数量
 

def lda_kmn_result(doc, iterator=1000):

    # 返回对应的聚类结果
    # 获取lda模型和词袋
    print("创建主题模型")
    word_list, r_model = ldaa.lda_model(doc, k1, iterator)

    # 获取文档——主题分布
    doc_topic = r_model.doc_topic_

    # 转为普通list进行聚类
    doc_topic_list = np.array(doc_topic).tolist()
    estimator = kmn.kMeansByFeature(k2, doc_topic_list)
    labels = estimator.labels_

    return list(labels)