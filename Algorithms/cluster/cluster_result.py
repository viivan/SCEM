# 训练聚类的测试
import visible.coordinatepainting as cp
import judge.clustereffect as ce
import data.data_util as du

import cluster.lda_kmeans as ldakmn
import cluster.tf_idf_lda_kmeans as lda_ti
import cluster.tf_idf_lda_expand_kmeans as lda_ex_ti
import cluster.tf_idf_w2v_kmeans as w2v_ti
import cluster.btm_kmeans as btm_kmn
import cluster.gpu_dmm_kmeans as gd_kmn
import cluster.lda_gibbs_kmeans as ldagkmn
import model.word2vecAdapter as w2v
import cluster.simple_lda_kmeans as s_lda_kmn
import cluster.lda_gibbs as s_lda

 
def printResult(k, result, former):
    pur = ce.purityClusterResult(k, result, former)
    ri = ce.R1ClusterResult(k, result, former)
    # f1 = ce.f1measureClusterResult(k, result, former)
    en = ce.entropyClusterResult(k, result, former)
    pre = ce.precision_cluster(k, result, former)
    recall = ce.recall_cluster(k, result, former)
    f1 = ce.f1measure_cbq(pre, recall)

    print("纯度:{}, RI:{}, 熵：{}, 准确率：{}，召回率：{}, F1_measure:{}".format(pur, ri, en, pre, recall, f1))
    result_list = [pur, ri, en, pre, recall, f1]
    return result_list


def ldaCluster(k1, k2, filename, fre_num=5):
    """
    包含三个参数
    k1为lda模型主题数，k2为聚类数，filename为resource中csv文件
    返回为两个值，第一个为聚类结果，第二个为聚类效果结果
    """
    print("lda模型训练，kMeans聚类")

    # 获取数据
    print("开始获取数据")
    doc = du.getDocAsWordArray(filename, fre_num)
    # 获取标签信息
    former = du.getFormerCategory(filename)

    # k1主题分类数 k2聚类数量
    ldakmn.k1 = k1
    ldakmn.k2 = k2
    print("lda主题数:{}, 聚类个数:{}".format(ldakmn.k1, ldakmn.k2))
    result = ldakmn.lda_kmn_result(doc)

    result_list = printResult(ldakmn.k2, result, former)
    return result, result_list


def lda_gibbs_cluster(k1, k2, filename, fre_num=5, iterator=500):
    """
    和上面的lda方法类似
    该方法调用使用了gibbs的lda库进行模型训练
    返回聚类结果和准确度
    """
    print("lda_gibbs模型训练，kMeans聚类")

    # 获取数据
    print("开始获取数据")
    doc = du.getDocAsWordArray(filename, fre_num)
    # 获取标签信息
    former = du.getFormerCategory(filename)

    # k1主题分类数 k2聚类数量
    ldagkmn.k1 = k1
    ldagkmn.k2 = k2
    print("lda主题数:{}, 聚类个数:{}".format(ldagkmn.k1, ldagkmn.k2))
    result = ldagkmn.lda_kmn_result(doc, iterator=iterator)
    result_list = printResult(ldagkmn.k2, result, former)
    return result, result_list


def tf_idf_ldaCluster(k1, k2, filename, num, fre_num=5):
    """
    包含四个参数
    k1为lda模型主题数，k2为聚类数，filename为resource中csv文件, num为关键词数量
    返回为两个值，第一个为聚类结果，第二个为聚类效果结果
    """
    print("tf_idf预处理, lda模型训练，kMeans聚类")

    # 获取数据
    print("开始获取数据")
    doc = du.getDocAsWordArray(filename, fre_num)
    # 获取标签信息
    former = du.getFormerCategory(filename)

    # k1主题分类数 k2聚类数量
    lda_ti.k1 = k1
    lda_ti.k2 = k2

    print("lda主题数:{}, 聚类个数:{}".format(lda_ti.k1, lda_ti.k2))
    result = lda_ti.clusterResult(doc, num)

    result_list = printResult(lda_ti.k2, result, former)
    return result, result_list


def tf_idf_lda_gibbs_Cluster(k1, k2, filename, num, fre_num=5, iterator=500):
    """
    和上面差不多
    lda用的gibbs采样
    """
    print("tf_idf预处理, lda_gibbs模型训练，kMeans聚类")

    # 获取数据
    print("开始获取数据")
    doc = du.getDocAsWordArray(filename, fre_num)
    # 获取标签信息
    former = du.getFormerCategory(filename)

    # k1主题分类数 k2聚类数量
    lda_ti.k1 = k1
    lda_ti.k2 = k2

    print("lda主题数:{}, 聚类个数:{}".format(lda_ti.k1, lda_ti.k2))
    result = lda_ti.clusterResult_gibbs(doc, num, iterator=iterator)

    result_list = printResult(lda_ti.k2, result, former)
    return result, result_list


def tf_idf_expand_lda(k1, k2, filename, num, sim_num, fre_num=5):
    """
    包含五个参数
    k1为lda模型主题数，k2为聚类数，filename为resource中csv文件，num为keyword数，sim_num为扩容数
    返回为两个值，第一个为聚类结果，第二个为聚类效果结果
    """
    # 利用tf_idf进行扩容后lda训练
    print("tf_idf扩容预处理, lda模型训练，kMeans聚类")

    # 获取数据
    print("开始获取数据")
    doc = du.getDocAsWordArray(filename, fre_num)
    # 获取标签信息
    former = du.getFormerCategory(filename)

    # k1主题分类数 k2聚类数量
    lda_ex_ti.k1 = k1
    lda_ex_ti.k2 = k2
    print("lda主题数:{}, 聚类个数:{}".format(lda_ex_ti.k1, lda_ex_ti.k2))
    result = lda_ex_ti.clusterResult(doc, num, sim_num)

    result_list = printResult(lda_ex_ti.k2, result, former)
    return result, result_list


def tf_idf_expand_lda_gibbs(k1, k2, filename, num, sim_num, model, fre_num=5, iterator=500):
    """
    和上面差不多
    lda用的gibbs采样
    """
    # 利用tf_idf进行扩容后lda训练
    print("tf_idf扩容预处理, lda_gibbs模型训练，kMeans聚类")

    # 获取数据
    print("开始获取数据")
    doc = du.getDocAsWordArray(filename, fre_num)
    # 获取标签信息
    former = du.getFormerCategory(filename)

    # k1主题分类数 k2聚类数量
    lda_ex_ti.k1 = k1
    lda_ex_ti.k2 = k2
    print("lda主题数:{}, 聚类个数:{}".format(lda_ex_ti.k1, lda_ex_ti.k2))
    # gibbs方法
    result = lda_ex_ti.clusterResult_gibbs(model, doc, num, sim_num, iterator=iterator)

    result_list = printResult(lda_ex_ti.k2, result, former)
    return result, result_list


def tf_idf_w2vCluster(k, filename, use_file=False, save_path=r"E:\学校\快乐推荐\word2vec\saveVec", fre_num=5):
    """
    包含四个参数
    k为聚类数，filename为resource中csv文件，use_file为是否使用存储文件
    save_path为W2V的训练文件
    返回为两个值，第一个为聚类结果，第二个为聚类效果结果
    """
    print("tf_idf预处理, w2v训练，kMeans聚类")

    # 获取数据
    doc = du.getDocAsWordArray(filename, fre_num)
    # 获取标签信息
    former = du.getFormerCategory(filename)

    # 计算，聚类
    if use_file is False:
        result = w2v_ti.clusterResult(doc, k, save_path, False)
    else:
        result = w2v_ti.clusterResultByFile(save_path)

    result_list = printResult(k, result, former)
    return result, result_list


def btmCluster(k, filename, save_file, fre_num=5):
    """
    包含三个参数
    k为聚类数，filename为resource中csv文件
    btm比较特殊，model构建较慢，提前进行model创建并使用文件进行读取
    """
    print("BTM模型，KMeans聚类")

    # 获取数据
    doc = du.getDocAsWordArray(filename, fre_num)
    # 获取标签信息
    former = du.getFormerCategory(filename)

    # 直接计算太慢，直接将处理好的model文件拿来用
    result = btm_kmn.clusterResult(k, save_file)
    result_list = printResult(k, result, former)
    return result, result_list


def gpu_dmmCluster(k, filename, save_file, fre_num=5):
    """
    包含三个参数
    k为聚类数，filename为resource中csv文件
    save_file为存储文档_主题分布的文件
    """
    print("gpu_dmm模型，KMeans聚类")

    # 获取数据
    doc = du.getDocAsWordArray(filename, fre_num)
    # 获取标签信息
    former = du.getFormerCategory(filename)

    # 直接计算太慢，直接将处理好的model文件拿来用
    result = gd_kmn.clusterResult(k, save_file)
    result_list = printResult(k, result, former)
    return result, result_list


def simple_lda_kmn_result(k, filename, iterator=20):
    # 获取数据
    doc = du.getDocAsWordArray(filename, 5)
    # 获取标签信息
    former = du.getFormerCategory(filename)

    # 计算结果
    d_t_m, kmn_result, t_result = s_lda_kmn.s_lda_KMeans(k, file_name, iterator)

    result_list = printResult(k, t_result, former)
    return kmn_result, result_list


def simple_lda_result(k, filename, iterator=30):
    # 获取数据
    doc = du.getDocAsWordArray(filename, 5)
    # 获取标签信息
    former = du.getFormerCategory(filename)

    c_result = s_lda.lda_result(k, doc, iterator)
    result_list = printResult(k, c_result, former)
    print(result_list)
    return c_result, result_list


if __name__ == "__main__":
    topic = 10
    kkt = 10
    file_name = "C10.csv"

    iterate = 10
    key_num = 5
    sim_num = 3

    save = r""
    model = w2v.load_model_binary(save)
    cluster_result, result = tf_idf_expand_lda_gibbs(topic, kkt, file_name, key_num, sim_num, model, iterator=500)
    print(result)