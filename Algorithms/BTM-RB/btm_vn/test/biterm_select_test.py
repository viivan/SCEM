import numpy as np
import os
import data.data_file_load as dfl
import random
import time
import model.biterm as biterm
import cluster.kmeans as kmn
import judge.whole_cluster_result as wce
import data.data_util as du
import model.btm_wvf_Adapter as btm_wvf

if __name__ == "__main__":
    t_k = 10
    t_iterate = 500
    t_threshold = 0.2
    t_miu = 0.4

    doc_word_filename = "doc_wordindex_C10.txt"
    voc_filename = "vocabulary_C10.txt"
    word_sim_filename = "word_sim_C10.txt"
    t_doc_word_id = dfl.loadWordIndexMatrix(doc_word_filename)
    t_voc_list = dfl.loadVocabularyList(voc_filename)
    t_word_sim_matrix = dfl.loadWordSimMatrix(word_sim_filename)

    print("开始btm模型训练")
    b_model = btm_wvf.BtmWvfModel(t_k, t_doc_word_id, t_voc_list, t_word_sim_matrix, threshold=t_threshold, miu=t_miu)
    accept, biterms = b_model.select_biterm()
    biterms_label_list = []
    for i in range(len(biterms)):
        word1 = t_voc_list[biterms[i].word1]
        word2 = t_voc_list[biterms[i].word2]
        label = accept[i]
        b_l = (word1, word2, label)
        biterms_label_list.append(b_l)
    # 找出包含关键词的词对并输出
    key_words = ["music", "phone", "photo", "video", "travel", "price", "weather", "map"]
    fw = open("select biterms{}.txt".format(t_threshold), "w+")
    for b_l in biterms_label_list:
        fw.write(b_l[0] + " " + b_l[1] + " " + str(b_l[2]) + "\n")
    fw.close()
    for word in key_words:
        print("{}_select biterms{}".format(word, t_threshold))
        fw = open("{}_select biterms{}.txt".format(word, t_threshold), "w+")
        for b_l in biterms_label_list:
            if b_l[0] == word or b_l[1] == word:
                fw.write(b_l[0] + " " + b_l[1] + " " + str(b_l[2]) + "\n")
        fw.close()

