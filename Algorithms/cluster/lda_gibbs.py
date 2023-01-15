import model.lda_gibbs as ldaa
import numpy as np
'''
直接输出概率最高的topic
'''
 

def get_cluster_type_by_doc_topic_matrix(doc_topic_matrix):
    # 公共方法，直接按照文档主题矩阵概率中概率分布最高的分量作为文档的主题归属
    # 形式和KMeans那边类似，[0,0,1,1,1,2,2...]
    topic_result = []
    for distribution in doc_topic_matrix:
        max_value = max(distribution)
        index = list(distribution).index(max_value)
        topic_result.append(index)
    return topic_result


def lda_result(k, doc, iterator=1):
    # 返回对应的聚类结果
    # 获取lda模型和词袋
    print("创建主题模型")
    word_list, r_model = ldaa.lda_model(doc, k, iterator)

    # 获取文档——主题分布
    doc_topic = r_model.doc_topic_

    # 转为普通list进行聚类
    doc_topic_list = np.array(doc_topic).tolist()
    # print(type(doc_topic_list))
    c_result = get_cluster_type_by_doc_topic_matrix(doc_topic_list)
    return c_result


if __name__ == "__main__":
    t_k = 10
    t_doc = {}

    lda_result(t_k, t_doc)