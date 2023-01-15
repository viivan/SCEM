"""
数据的文件存储，方便多次调用
"""

import data.data_util as du
import os
import model.word2vecAdapter as w2v

# 获取路径信息
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("btm_vn\\") + len("btm_vn\\")]


def saveDicAsVocIndex(filename, fre_num=5):
    # 获取文档集合的词汇表，存储
    # 获取文档集合，转换为词汇表中词汇index存储
    docs = du.getDocAsWordArray(filename, fre_num=fre_num)
    # 生成词汇表
    vocabulary = set()
    for k in docs:
        simple_word_list = docs[k].split(" ")
        for w in simple_word_list:
            vocabulary.add(w)
    voc_list = list(vocabulary)

    # 转换分词文档形式
    word_index_list = []
    for k in docs:
        simple_word_list = docs[k].split(" ")
        for i in range(len(simple_word_list)):
            w = simple_word_list[i]
            w_index = voc_list.index(w)
            simple_word_list[i] = str(w_index)
        word_index_str = ",".join(simple_word_list)
        word_index_list.append(word_index_str)

    # 存入文件
    suffix = filename[0:str(filename).index(".")]
    voc_filename = "vocabulary_{}.txt".format(suffix)
    word_index_filename = "doc_wordIndex_{}.txt".format(suffix)

    voc_path = os.path.abspath(rootPath + "resource\\" + voc_filename)
    word_index_path = os.path.abspath(rootPath + "resource\\" + word_index_filename)

    try:
        pf = open(voc_path, "w+")
        for v in voc_list:
            pf.writelines(v + "\n")
        pf.close()

        wf = open(word_index_path, "w+")
        for w_str in word_index_list:
            wf.writelines(w_str + "\n")
        wf.close()
    except IOError:
        print("文件无法写入")
        return None

    print("{},{} 文件写入成功".format(voc_filename, word_index_filename))


def calWordSimilarity(voc_filename, model_path):
    # 利用w2v和词汇表文件计算相似度矩阵，估计非常慢
    voc_path = os.path.abspath(rootPath + "resource\\" + voc_filename)
    voc_list = []
    # 读取文档分布矩阵
    try:
        pf = open(voc_path, "r+")
        lines = pf.readlines()
        for line in lines:
            voc_list.append(line.strip())
    except IOError:
        print("词汇表读取失败")
    print("词汇表读取完成")

    # 根据描述需要生成一个词相似度的矩阵
    # 计划直接使用word2vec
    print("加载word2vec模型")
    model = w2v.load_model_binary(save_path=model_path)
    print("计算词汇相似度")
    sim_matrix = w2v.word_sim_matrix(model, voc_list)
    print("词汇相似度矩阵计算完成")

    # 输出文件
    sim_save_filename = "word_sim_{}.txt"\
        .format(voc_filename[str(voc_filename).rindex("_") + 1:str(voc_filename).rindex(".")])
    save_path = os.path.abspath(rootPath + "resource\\" + sim_save_filename)
    print(save_path)

    try:
        file = open(save_path, "w+", encoding="utf-8")
        for sim in sim_matrix:
            line = " ".join([str(x) for x in sim])
            file.writelines(line + "\n")
            print(line)
        file.close()
    except IOError:
        print("文件存放失败")

    print("词汇相似度矩阵文件生成")
    return sim_matrix


if __name__ == "__main__":
    t_filename = "C10.csv"
    t_voc_filename = "vocabulary_C8.txt"
    model_path = r"E:\研究生\word2vec\GoogleNews_vec.bin"
    # saveDicAsVocIndex(t_filename)
    calWordSimilarity(t_voc_filename, model_path)

