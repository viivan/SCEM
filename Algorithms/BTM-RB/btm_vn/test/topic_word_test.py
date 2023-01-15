import model.btm_wvf_Adapter as bwf
import cluster.kmeans as kmn
import judge.clustereffect as ce
import judge.whole_cluster_result as wce
import data.data_util as du
import data.data_file_load as dfl
import os


def sort_method(element):
    # 排序使用函数
    return element[0]


if __name__ == "__main__":
    cluster_k = 10
    filename = "C10_iterate500_threshold0.1_miu0_tp.txt"
    voc_filename = "vocabulary_C10.txt"

    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("btm_wvf\\") + len("btm_wvf\\")]
    path = os.path.abspath(rootPath + "resource\\" + filename)

    t_voc_list = dfl.loadVocabularyList(voc_filename)
    topic_word_num = bwf.load_Topic_word(path)
    word_num = 10
    t_words = []
    for i in range(cluster_k):
        # 将对应主题的每个词和其id作为元组进行排序
        b = zip(topic_word_num[i], range(len(topic_word_num[i])))
        b = list(b)
        b.sort(key=sort_method, reverse=True)
        print("topic {}".format(i))
        s_words = []
        for j in range(len(b)):
            if j < word_num:
                s_words.append(t_voc_list[b[j][1]])
                print(t_voc_list[b[j][1]], "概率:{}".format(b[j][0] / sum(topic_word_num[i])))
            else:
                break
        t_words.append(s_words)
    for w_l in t_words:
        print(w_l)
