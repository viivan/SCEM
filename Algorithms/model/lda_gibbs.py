import numpy as np
import lda
import lda.datasets

"""
使用利用gibbs采样实现的lda模型训练
多次迭代并有迭代效果计算
主要是进行对应的数据处理 
"""


def lda_model(doc, topic, iterator=500):
    # 返回词汇表和训练好的lda模型
    word_set = set()
    print("转化doc_word")
    # 首先创建词汇表
    for d in doc:
        document = doc[d]
        document_word_list = document.split(" ")
        for w in document_word_list:
            word_set.add(w)

    # 创建document矩阵
    N = len(doc)
    V = len(word_set)
    data = []
    word_list = list(word_set)
    for d in doc:
        """
        将存在的词的编号和数量作为tuple存储
        N为文档数，V为词汇数
        之后将其转换为np N*V大小的矩阵
        """
        document = doc[d]
        document_word_list = document.split(" ")
        simple_list = []

        # 每个单词在该文档中包含数
        for i in range(len(word_list)):
            c = document_word_list.count(word_list[i])
            if c > 0:
                simple_list.append((i, document_word_list.count(word_list[i])))
        data.append(tuple(simple_list))

    # 创建矩阵
    dtm = np.zeros((N, V), dtype=np.intc)
    for i, doc in enumerate(data):
        for v, cnt in doc:
            np.testing.assert_equal(dtm[i, v], 0)  # 确认下以免出错
            dtm[i, v] = cnt

    print("训练lda模型")
    model = lda.LDA(n_topics=topic, n_iter=iterator, random_state=1)
    model.fit(dtm)
    return word_list, model