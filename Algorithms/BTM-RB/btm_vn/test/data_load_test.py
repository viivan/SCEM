import model.btm_wvf_Adapter as bwf
import cluster.kmeans as kmn
import judge.clustereffect as ce
import judge.whole_cluster_result as wce
import data.data_util as du
import os

if __name__ == "__main__":
    cluster_k = 8
    filename = "C8_iterate500_threshold0.15_miu0.4_result.txt"

    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("btm_wvf\\") + len("btm_wvf\\")]
    path = os.path.abspath(rootPath + "resource\\" + filename)

    matrix = bwf.load_Doc_Topic_Matrix(path)
    cluster_result = kmn.dpc_kMeans(cluster_k, matrix, 20)
    top_result = kmn.top_cluster(matrix)
    print(top_result)

    former_type = du.getFormerCategory("C8.csv")
    result = wce.printResult(cluster_k, cluster_result, former_type)



