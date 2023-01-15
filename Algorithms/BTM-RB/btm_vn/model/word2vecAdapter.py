from gensim.models import word2vec
from gensim.models import KeyedVectors

"""
使用word2vec获取词语的特征信息
"""
 

def build_model(text_path=r"", save_path=r"", size=5):
    print("载入语料数据")
    sentences = word2vec.Text8Corpus(text_path)
    print("进行模型的训练")
    model = word2vec.Word2Vec(sentences, size=size)  # size为词向量维度，窗口默认为5
    print("训练完成")
    model.wv.save_word2vec_format(save_path, binary=True)  # 二进制存储
    print("训练模型保存完成，地址:{}".format(save_path))
    return model


def load_model_binary(save_path=r""):
    print("加载模型文件{}".format(save_path))
    model = KeyedVectors.load_word2vec_format(save_path, binary=True)
    print("加载完毕")
    return model


def word_sim_matrix(model, word_list):
    # 预计将word_list中词相互间相似度放入n*n矩阵中输出
    sim_matrix = []
    for w1 in word_list:
        print(w1)
        word_sim = []
        for w2 in word_list:
            if w1 == w2:
                word_sim.append(1)
            elif w1 not in model.index2word or w2 not in model.index2word:
                word_sim.append(0)
            else:
                word_sim.append(model.similarity(w1, w2))
        sim_matrix.append(word_sim)

    return sim_matrix




