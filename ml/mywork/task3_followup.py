
import task1
import logging
import argparse
import sys
import numpy
from sklearn.externals import joblib
from collections import Counter
from sklearn.preprocessing import scale
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV



def countTerm(filename):
    """Get top N frequent terms in file"""
    fp = open(filename,'r')
    terms = []
    for line in fp:
        terms.extend(task1.preprocess(line))
    # count TF, when file is big, can use MapReduce to scale out
    wordcount = Counter(terms)
    return wordcount
        
def extractFeature(good,bad,N):
    """Extract feature from good and bad data"""
    good_wc = countTerm(good)
    bad_wc = countTerm(bad)
    good_wc.subtract(bad_wc)
    feature = good_wc.most_common(N)
    # save feature as dictionary for later use
    logger.info('saving feature...')
    joblib.dump(dict(feature), 'feature.pkl')
    logger.info('feature saved as %s' % 'feature.pkl') 
    return dict(feature).keys()
    
def updateFeature(good,bad=None):
    """Load feature from file and update"""
    global N
    feature_dict = joblib.load('feature.pkl')
    good_wc = countTerm(good)
    newfeature = good_wc + Counter(feature_dict)
    if bad!=None:
        bad_wc = countTerm(bad)
        newfeature = badwc.subtract(Counter(feature_dict))
    newfeature = newfeature.most_common(N)
    # save feature as dictionary for later use
    logger.info('saving feature...')
    joblib.dump(dict(newfeature), 'newfeature.pkl')
    logger.info('feature saved as %s' % 'newfeature.pkl') 
    return dict(newfeature).keys()         

def vectorize(filename,features):
    """From file generate vector"""
    corpus = []
    fp = open(filename,'r')
    for line in fp:
        tokens = task1.preprocess(line) 
        vector = [0]*len(features)
        for term in tokens:
            if term in features:
                idx = features.index(term)
                vector[idx] += 1 # use TF instead of binary
        corpus.append(vector)
    fp.close()
    return corpus

def train(good,bad,modelname,feature=None):
    """Train classifier from good and bad data"""
    # extract feature from file if no feature is given
    if feature == None:
        global N
        feature = extractFeature(good,bad,N)
    # log feature    
    logger.debug('feature used...')
    logger.debug(feature) 
    # generate matrix
    good_vectors = vectorize(good,feature)
    bad_vectors = vectorize(bad,feature)
    train_vector = good_vectors + bad_vectors
    train_label = [1]*len(good_vectors) + [0]*len(bad_vectors)
    train_vector = scale(train_vector) # scaling may be useful with real data
    if len(train_vector) < len(feature):
        logger.warn('# of observations smaller than # of features.')
    # grid search
    C = [2**i for i in range(11)]
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],'C': C},
                        {'kernel': ['linear'], 'C': C}]
    clf = GridSearchCV(svm.SVC(C=1), tuned_parameters, cv=5)
    clf.fit(train_vector, train_label)
    # logging grid search result
    logger.info("Best parameters set found on training set:")
    logger.info(clf.best_estimator_)
    logger.debug("Grid scores on training set:")
    for params, mean_score, scores in clf.grid_scores_:
        logger.debug("%0.3f (+/-%0.03f) for %r"
                     % (mean_score, mean_score, params))
    classifier = svm.SVC(clf.best_estimator_)    
    y_true, y_pred = train_label, clf.best_estimator_.predict(train_vector)
    logger.info("Performance on training data:")
    logger.info(classification_report(y_true, y_pred))
    # save model and feature to file
    logger.info('saving model...')
    joblib.dump(clf.best_estimator_, modelname+'.model.pkl')
    logger.info('model saved as %s' % modelname+'.model.pkl')   
         
def predict(testfile,modelname,split=False):
    """Given model, predict test file"""
    # load feature and model
    feature_dict = joblib.load('feature.pkl')
    feature = feature_dict.keys()
    clf = joblib.load(modelname+'.model.pkl')
    # vectorize test file
    test_vector = vectorize(testfile,feature)
    # predict 
    y_pred = clf.predict(test_vector)
    # write label to file, seperated by newline
    try:
        idx = testfile.rfind('.')
        name = testfile[:idx]
        idx = name.rfind('/')
        name = name[idx+1:]
    except:
        pass
    y_pred.tofile(name+'.predict',sep='\n')
    #split testfile to good & bad data according to predction
    if split:
        fp = open(testfile,'r') 
        fg = open('good_'+name,'w')  
        fb = open('bad_'+name,'w')
        looper = 0
        for line in fp:
            if y_pred[looper] == 1.0:
                fg.write(line)
            else:
                fb.write(line)
            looper += 1
        fp.close()
        fg.close()
        fb.close()
    
def retrain(modelname,good,bad,useBad=False):
    """Add features and re-train the model"""
    if useBad:
        newfeature = updateFeature(good,bad)
    else:
        newfeature = updateFeature(good)
    train(good,bad,'new.'+modelname,newfeature)        
    
if __name__=='__main__':
    # create logger
    logger = logging.getLogger('task3')
    hdlr = logging.FileHandler('task3.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.DEBUG)
    
    good = sys.argv[1]
    bad = sys.argv[2]
    test = sys.argv[3]
    model = sys.argv[4]
    # top N terms are chosen as feature
    N = 15 
    # train with good, bad data
    train(good,bad,model) 
    # predict test data
    # By setting split=True, test file will be splited based on prediction 
    predict(test,model,split=True) 
    # retrain the model based on newly predicted good data and bad data
    retrain(model,'good_test_deals',bad)
    # As can be been from log, re-trained model is improved significantly

