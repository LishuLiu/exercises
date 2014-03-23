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
import sys
from sklearn import svm
#from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix

# step 1: run task1 on good_deals, bad_deals and test_deals
#os.system('python task1.py ../data/good_deals.txt')
#os.system('python task1.py ../data/bad_deals.txt')
#os.system('python task1.py ../data/test_deals.txt')

# step 2: feature selection
# select top features from good_deals, extract top features from bad_deals
features = [ 'NUM','CODE','DATE','URL','$','%','free','sale','save',\
             'get','shipping','off','shop','all','code','buy','price']

# step 3: construct feature vector
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

#print train_vector
#print train_label
# step 4: train classifier
#X_train, X_test, y_train, y_test = train_test_split(train_vector, train_label, random_state=0)
#classifier = svm.SVC(kernel='linear')
#y_pred = classifier.fit(X_train, y_train).predict(X_test)
#cm = confusion_matrix(y_test, y_pred)

#print(cm)

#pl.matshow(cm)
#pl.title('Confusion matrix')
#pl.colorbar()
#pl.ylabel('True label')
#pl.xlabel('Predicted label')
#pl.show()

classifier = svm.SVC(kernel='linear')    
classifier.fit(train_vector, train_label)
pred = classifier.predict(train_vector)
cm = confusion_matrix(train_label, pred)
print(cm)

# step 5: performance tuning
param_grid = [
  {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
  {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
 ]



