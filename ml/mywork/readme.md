Overview
========

task1.py
--------

Preprocess deals and generate tf, reverse index, and doc matrix
Usage: python task1.py deals_file
Output:
deals_Docs.csv - index for deals.txt 
deals_ReverseIndex.csv - reverse index for deals.txt
deals_TF.csv - term frequence for deals.txt 
deals.dict - [Dictionary] for deals.txt. Used by task2
deals.mm - [Matrix Market] for deals.txt. Used by task2
deal.mm.index 

Note:
test1.py - unit test for task1
test.txt - test files for task1


task2.py
--------

Read doc matrix and dictionary generated at task1, performe k-means clustering 
and Latent Semantic Analysis 
Usage: python task2.py
Output:
cluster_assignments.txt - Kmeans clustering output
topics.txt - LSA topics output

task3.py
--------

Feature selection, classifier training based on good_deals and bad_deals. 
Tested on test_deals.
Usage: python task3.py
Output:
task3.out - stdout by task3


[Dictionary]:http://radimrehurek.com/gensim/corpora/dictionary.html#gensim.corpora.dictionary.Dictionary
[Matrix Market]:http://math.nist.gov/MatrixMarket/formats.html
