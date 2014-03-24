""" Groups and Topics

The objective of this task is to explore the structure of the deals.txt file. 

Building on task 1, we now want to start to understand the relationships to help us understand:

1. What groups exist within the deals?
2. What topics exist within the deals?

"""
import gensim
import numpy as np
from gensim import corpora, models, similarities
from scipy.sparse import * 
from sklearn.cluster import KMeans  

# read dictionary and document matrix, transformed by tf-idf
dictionary = corpora.Dictionary.load('deals.dict')
corpus = corpora.MmCorpus('deals.mm')
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
# convert to scipy sparse matrix
sm_corpus_tfidf = gensim.matutils.corpus2csc(corpus_tfidf) 
# <29940x56631 sparse matrix of type '<type 'numpy.float64'>

###############################################################################
# clustering

# k-means clustering
# the rule of thumb of choosing k is square-root of n (56631), which is k = 238
# grid search on init and k to decide best k
# inertia is used here to evaluate k-means performance
best_k = 0
best_init = ''
inertia = 10000000
for init in ['k-means++', 'random']: 
    for k in range(38,338,50):
        try: 
            labeler = KMeans(k = k,init = init)
            labeler.fit(sm_corpus_tfidf.tocsr())
            if labeler.inertia_ < inertia:
                best_k = k
                best_init = init
            print k,init,labeler.inertia_
        except (RuntimeError, TypeError, NameError,ValueError):
            print 'Error: ', k,init 
# output
# 38 k-means++ 51980.811733
# 88 k-means++ 48577.2056794
# 138 k-means++ 46192.2196129
# 188 k-means++ 44003.4396531
# 238 k-means++ 42313.0053122
# 288 k-means++ 40861.4916342
# 38 random 53830.6887249
# 88 random 52157.3562656
# Error:  138 random
# Error:  188 random
# Error:  238 random
# Error:  288 random

# write cluster assignments for each row
labeler = KMeans(k = best_k,init = best_init)
labeler.fit(sm_corpus_tfidf.tocsr())
fp = open('cluster_assignments.txt','w')
fp.write('row : label\n')
for (row, label) in enumerate(labeler.labels_):
    fp.write(" %d : %d\n" % (row, label))
fp.close()


###############################################################################
# topic modeling

# Latent Semantic Analysis
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=238)
corpus_lsi = lsi[corpus_tfidf]
topics = lsi.show_topics()
fp = open('topics.txt','w')
for topic in topics:
    fp.write(topic)
    fp.write('\n')
fp.close()

