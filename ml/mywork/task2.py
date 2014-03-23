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


dictionary = corpora.Dictionary.load('deals.dict')
corpus = corpora.MmCorpus('deals.mm')
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
# convert to scipy sparse matrix
sm_corpus_tfidf = gensim.matutils.corpus2csc(corpus_tfidf) 

###############################################################################
# clustering

# k-means clustering
# the rule of thumb of choosing k is square-root of n
labeler = KMeans(k=100)
# note: Kmeans currently only works with CSR type sparse matrix
labeler.fit(sm_corpus_tfidf.tocsr()) 

# write cluster assignments for each row
fp = open('cluster_assignments.txt','w')
fp.write('row : label\n')
for (row, label) in enumerate(labeler.labels_):
    fp.write(" %d : %d\n" % (row, label))
fp.close()


###############################################################################
# topic modeling
# Latent Semantic Analysis
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
corpus_lsi = lsi[corpus_tfidf]
topics = lsi.show_topics()
fp = open('topics.txt','w')
for topic in topics:
    fp.write(topic)
    fp.write('\n')
fp.close()


# Latent Dirichlet Allocation
lda = gensim.models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, \
num_topics=50, update_every=1, chunksize=10000, passes=1)
lda.print_topics(20)
