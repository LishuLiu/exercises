""" Classification

The objective of this task is to build a classifier that can tell us whether a new, unseen deal 
requires a coupon code or not. 

We would like to see a couple of steps:

1. You should use bad_deals.txt and good_deals.txt as training data
2. You should use test_deals.txt to test your code
3. Each time you tune your code, please commit that change so we can see your tuning over time

Also, provide comments on:
    - How general is your classifier?
    - How did you test your classifier?

"""

import task1
import os
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV

'''
###############################################################################
# step 1: run task1 on good_deals, bad_deals and test_deals
os.system('python task1.py ../data/good_deals.txt')
os.system('python task1.py ../data/bad_deals.txt')
os.system('python task1.py ../data/test_deals.txt')
'''
###############################################################################
# step 2: feature selection
# Select top features from good_deals, exclude top features from bad_deals
# By 'top' I used TF>2 as criteria
good_features = ['NUM','CODE','URL','$','%','free','pillow','sale',\
                 'save','get','shipping','off','shop','all','code',\
                 'buy','link','price']
bad_deals = ['NUM','URL','deal','link']
intersect = set(good_features) & set(bad_deals) # set(['URL', 'NUM', 'link'])
features = list(set(good_features) - set(bad_deals))
# NUM and URL are kept on purpose, some features are manually removed 
features = [ 'NUM','CODE','DATE','URL','$','%','free','sale','save',\
             'get','shipping','off','shop','all','code','buy','price']

###############################################################################
# step 3: construct feature vector
# Here I used binary as feature value, instead of TF, for simplicity
def vectorize(filename,label,features,vectors,labels):
    fp = open(filename,'r')
    for line in fp:
        tokens = task1.preprocess(line)
        ones = set(features) & set(tokens)
        vector = [0]*len(features)
        for one in ones:
            idx = features.index(one)
            vector[idx] = 1
        vectors.append(vector)
        labels.append(label)
    fp.close()

train_vector = []
train_label = []
test_vector = []
test_label = []
vectorize('../data/good_deals.txt',1,features,train_vector,train_label)
vectorize('../data/bad_deals.txt',0,features,train_vector,train_label)
vectorize('../data/test_deals.txt',0,features,test_vector,test_label)

###############################################################################
# step 4: train classifier & step 5: performance tuning
# grid search on SVC parameters
C = [2**i for i in range(11)]
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': C},
                    {'kernel': ['linear'], 'C': C}]

clf = GridSearchCV(svm.SVC(C=1), tuned_parameters, cv=5)
clf.fit(train_vector, train_label)

print "\nBest parameters set found on training set:"
print clf.best_estimator_
print "\nGrid scores on training set:"
for params, mean_score, scores in clf.grid_scores_:
    print params,mean_score, scores

# performance measure
# Note that here I use precision score and recall score, other measurement 
# like ROC can be applied here for more spercific performance tuning. 
classifier = svm.SVC(clf.best_estimator_)    
y_true, y_pred = train_label, clf.best_estimator_.predict(train_vector)
print "\nPerformance on test data:"
print classification_report(y_true, y_pred)

###############################################################################
# step 6: test
# I manually labeled test_deals.txt
y_test = [0, 1, 0, 0, 0, 1, 0, 0, 0, 1,\
          0, 0, 1, 0, 1, 0, 0, 0, 1, 0,\
          1, 0, 0, 0, 0, 1, 0, 0, 0, 0,\
          0, 0, 1, 0, 0, 1, 0, 0, 0, 1,\
          1, 1, 0, 1, 0, 0, 0, 0, 0, 1,\
          0, 0, 1, 0, 0, 1, 0, 0]
y_true, y_pred = y_test, clf.best_estimator_.predict(test_vector)
print "\nPerformance on test data:"
print classification_report(y_true, y_pred)


