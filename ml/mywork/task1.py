""" Features

The objective of this task is to explore the corpus, deals.txt. 

The deals.txt file is a collection of deal descriptions, separated by a new line, from which 
we want to glean the following insights:

1. What is the most popular term across all the deals?
A: The most popular term is NUMBER (a catergory of numeric numbers). 
The followed by: URL, $, %, free.

2. What is the least popular term across all the deals?
A: There are many terms that only appear once across all the deals. 

3. How many types of guitars are mentioned across all the deals?
A: There are 24 terms co-occur with guitar that seems like types: 
'flatpicking', 'ibanez', 'art', 'classical', 'exclusive', 'series', 'gypsy', 
'taylor', 'gear', 'epiphone', 'mallet', 'bassman', 'boutique',
'jazz', 'christian', 'electric', 'big', 'rock', 'slant', 
'hd', 'fingerstyle', 'country', 'martin', 'acoustic'
"""

import nltk
import sys
import re
import datetime

from nltk.corpus import stopwords
from gensim import corpora

def isDate(datestring):
    """Match date and date range"""
    # date format
    datetimeFormat = ['%y-%m-%d','%Y-%m-%d','%m/%d/%y','%m/%d/%Y',\
                      '%m-%d-%y','%m-%d-%Y','%d/%m/%y','%d/%m/%Y',\
                      '%d.%m.%y','%d.%m.%Y','%d-%m-%y','%d-%m-%Y',\
                      '%m/%d','%m-%d'] 
    for pattern in datetimeFormat:
        try:
            datetime.datetime.strptime(datestring, pattern)
            return True
        except:
            pass
        # assume that date range seperated by '-'
        if '-' in datestring: 
            try:                         
                (start,end) = datestring.split('-')
                datetime.datetime.strptime(start, pattern)
                datetime.datetime.strptime(end, pattern)
                return True
            except:
                pass
    return False
                
def isCode(codeString):
    """Match coupon code"""
    # assume coupon code must have numbers and letters
    pattern = '\w*\d+\w+'
    try:
        if codeString == re.match(pattern,codeString).group():
            return True
    except:    
        pass
    return False
        
def isNum(numString):
    """Match numeric string"""
    # assumer numbers are digits or doubles
    if '.' in numString:
        idx = numString.index('.')
        return numString[:idx].isdigit() and numString[idx+1:].isdigit()
    else:
        return numString.isdigit()
            
def isURL(urlString):
    """Match URL string"""
    # assume URL must have pattern 'alphanumeric.letters'
    pattern = '\w+\.[a-zA-Z]+'
    try:
        if re.search(pattern,urlString) is not None:
            return True
    except:
        pass    
    return False

def preprocess(line):
    """Pre-process line into tokens"""
    tk = nltk.word_tokenize(line)
    porter = nltk.PorterStemmer()
    lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
    # English stopwords should be removed, exclude 'off' 
    removelist = stopwords.words('english')
    removelist.remove('off')
    # '$' and '%' kept on purpose
    symbols = ['*',',','?','-','+','(',')',':','.','&','#','"','!'] 
    removelist.extend(symbols)
    
    newtk = []
    for token in tk:
    	if token in removelist:
    	    continue
    	else:
    	    # to lower case
            token = token.lower()
            # stemming
#           token = porter.stem(token)
            # lemmatization
            token = lmtzr.lemmatize(token)
            # remove symbols at the end	
            while len(token)>1 and token[-1] in symbols:
                token = token[:-1]
            if token:
            	# replace special case with pre-defined Catergory
                if isNum(token):
                    token = 'NUM'
                elif isDate(token):
                    token = 'DATE'
                elif isCode(token):
                    token = 'CODE'
                elif isURL(token):
                    token = 'URL'
                newtk.append(token)
    return newtk

def reverseIndex(tk, docID):
    """create reverse index"""
    global ReverseIndex
    global TF
    global guitar
    looper = 0
    for token in tk:
    	if token == 'guitar':
    	    if looper!=0:
    	        guitar.append(tk[looper-1])
        if TF.has_key(token):
            TF[token] += 1
        else:
            TF[token] = 1
        if ReverseIndex.has_key(token):
            ReverseIndex[token].append(docID)
        else:
            ReverseIndex[token] = [docID]
        looper += 1
            
def writeDict(filename, dct):
    """Write dictionary into file"""
    fp = open(filename,'w')
    for k in dct:
        fp.write(str(k))
        fp.write(' : ')
        fp.write(str(dct[k]))
        fp.write('\n')
    fp.close()

def readDict(filename,dct):
    """Read dictionary from file"""
    dct = {}
    fp = open(filename,'r')
    for line in fp:
        line = line.strip()
        (key,value) = line.split(':')
        key = eval(key)
        value = eval(value)
        dct[key] = value
    fp.close()
    return dct

if __name__=='__main__':

    filename = sys.argv[1]
    try:
        idx = filename.rfind('.')
        name = filename[:idx]
        idx = name.rfind('/')
        name = name[idx+1:]
    except:
        pass
    
    DocsTable = {}		# key: docID value: tokens
    TF = {}			# key: term  value: term frequency
    ReverseIndex = {}		# key: term  value: list of docID
    guitar = []			# list guitar types    
    docs = []

    fp = open(filename,'r')
    docID = 1
    lastline = ''
    for line in fp:
        # skip consecutive duplicated lines 
        if line == lastline:
            continue
        tokens = preprocess(line)
        if tokens:
            docs.append(tokens)
            DocsTable[docID] = tokens
            reverseIndex(tokens,docID)
            docID += 1
     	lastline = line
    fp.close()
    writeDict(name + '_Docs.csv', DocsTable)
    writeDict(name + '_ReverseIndex.csv', ReverseIndex)
    writeDict(name + '_TF.csv', TF)
    
    # store dictionary and matrix for task 2
    dictionary = corpora.Dictionary(docs)
    dictionary.save('deals.dict')
    corpus = [dictionary.doc2bow(text) for text in docs]
    corpora.MmCorpus.serialize('deals.mm', corpus)
#    corpora.BleiCorpus.serialize('deals.lda-c', corpus) # for lda-c
    
    # list guitar types, needs human review
    print set(guitar)
    # output
    # set(['shop', 'flatpicking', 'ibanez', 'art', 'classical', 'exclusive', 
    # 'series', 'month', 'four', 'gypsy', 'taylor', 'gear', 'epiphone', 'CODE', 
    # 'mallet', 'bassman', 'boutique', 'rebate', 'NUM', 'music', 'card', 
    # 'online', 'week', 'product', 'jazz', 'christian', 'electric', 'big', 
    # 'rock', 'slant', 'link', 'buy', 'hd', 'fingerstyle', 'sa-212', 'money', 
    # 'country', 'martin', 'arrival', 'sale', 'item', 'learn', 'acoustic', 
    # 'page', 'flatpick'])

   
