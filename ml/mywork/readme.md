Overview
========

task1.py
--------

Preprocess deals and generate tf, reverse index, and doc matrix <br />
**Usage:** <br />
python task1.py deals_file <br />
**Output:** <br />
*deals_Docs.csv* - index for deals.txt <br />
*deals_ReverseIndex.csv* - reverse index for deals.txt<br />
*deals_TF.csv* - term frequence for deals.txt <br />
*deals.dict* - [Dictionary] for deals.txt. Used by task2<br />
*deals.mm* - [Matrix Market] for deals.txt. Used by task2<br />
*deal.mm.index* <br />

**Note:**<br />
*test1.py* - unit test for task1<br />
*test.txt* - test files for task1<br />


task2.py
--------

Read doc matrix and dictionary generated at task1, performe k-means clustering 
and Latent Semantic Analysis <br />
**Usage:** <br />
python task2.py<br />
**Output:**<br />
*cluster_assignments.txt* - Kmeans clustering output<br />
*topics.txt* - LSA topics output<br />

task3.py
--------

Feature selection, classifier training based on good_deals and bad_deals. 
Tested on test_deals.<br />
**Usage:** <br />
python task3.py<br />
**Output:**<br />
*task3.out* - stdout by task3


[Dictionary]:http://radimrehurek.com/gensim/corpora/dictionary.html#gensim.corpora.dictionary.Dictionary
[Matrix Market]:http://math.nist.gov/MatrixMarket/formats.html
