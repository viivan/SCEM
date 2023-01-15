# SCEM
Core code of the SCEM.

## Introduction

BTM-RB main method in /Algorithms/BTM-RB/model/btm_wvf_Adapter.py, the training can be carried out by modifying the parameters, and the training results are generated into a txt file.</br>

Topic coherence calculation in /Algorithms/BTM-RB/test/topic_word_test.py.</br>

The prototype system based on a browser/server structure is in /Web App. 
The system is implemented in Java, relies on Apache Tomcat 8.5 as a web application server, and uses a MySql 5.7 database. The front-end UI is implemented by HTML5, CSS3, and JavaScript, and communicates with the server through AJAX technology. 

## other main comparison algorithm or model implementation

TF-IDF+Word2vec: /Algorithms/cluster/cluster/tf_idf_w2v_kmeans.py</br>
LDA: /Algorithms/cluster/cluster/lda_gibbs.py</br>
LDA+Word2vec: /Algorithms/cluster/cluster/lda_expand_kmeans.py</br>
BTM: /Algorithms/cluster/model/btmAdapter.py</br>
DMM：/Algorithms/DMM implementation using [https://github.com/datquocnguyen/jLDADMM](https://github.com/datquocnguyen/jLDADMM)



<br><br><hr>
Thanks to ZhengJiahong, LuChengbing, DaiJiawei, WuHan, LiDuanni for his research contribution of this project.