""" Features

The objective of this task is to explore the corpus, deals.txt. 

The deals.txt file is a collection of deal descriptions, separated by a new line, from which 
we want to glean the following insights:

1. What is the most popular term across all the deals?
A: The most popular term is NUMBER (a catergory of numeric numbers). The following terms are: !, %, free, off.

2. What is the least popular term across all the deals?
A: There are many terms that only appear once across all the deals. 

3. How many types of guitars are mentioned across all the deals?
A: The term that occur term guitar are ['flatpicking', 'ibanez', 'art', 'classical', 'exclusive', 'series', 'gypsy', 'taylor', 'gear', 'epiphone', 'mallet', 'bassman', 'boutique', 'rebate', 'music', 'card', 'jazz', 'christian', 'electric', 'big', 'rock', 'slant', 'hd', 'fingerstyle', 'sa-212', 'country', 'martin', 'acoustic', 'flatpick'] 
"""

import nltk
import sys
import re
import datetime
from nltk.corpus import stopwords


def preprocess(line):
    """Pre-process line into tokens"""
    tk = nltk.word_tokenize(line)
    porter = nltk.PorterStemmer()
    lmtzr = nltk.stem.wordnet.WordNetLemmatizer()	# needs to download wordnet
    removelist = stopwords.words('english')		# stopwords should be removed
    removelist.remove('off')
    removelist.remove('to')
    symbols = ['*',',','?','-','+','(',')',':','.','&','#','"']		# meaningless symbols shoule be removed
    removelist.extend(symbols)
    
    newtk = []
    for token in tk:
    	if token in removelist:
    	    continue
    	else:
            token = token.lower()		# to lower case
#           token = porter.stem(token)		# stemming
            token = lmtzr.lemmatize(token)	# lemmatize
            while len(token)>1 and token[-1] in symbols:     # remove symbols at the end
                token = token[:-1]
            if token:
                newtk.append(token)
    return newtk

def reverseIndex(tk, docID):
    """create reverse index"""
    global ReverseIndex
    global TF
    global guitar
    def isDate(datestring):
        """Match datetime"""
        datetimeFormat = ['%y-%m-%d','%m/%d/%y','%m/%d','%d-%m-%y','%m-%d',\
                          '%d/%m/%y','%d.%m.%y'] # more format can be add here
        Flag = False
        for pattern in datetimeFormat:
            try:
                if '-' in datestring:                           # date range
                    idx = datestring.index('-')                 # assume that date range will not use mm-dd format  
                    startdate = datestring[:idx]
                    enddate = datestring[idx+1:]
                    datetime.datetime.strptime(startdate, pattern)
                    datetime.datetime.strptime(enddate, pattern)
                else:
                    datetime.datetime.strptime(datestring, pattern)
                return True
            except ValueError:
                continue
        return Flag
                
    def isCode(codestring):
        """Match coupon code"""
        codeFormat = ['\w*\d+\w+']			# more format can be add here
        Flag = False
        for pattern in codeFormat:
            try:
                if codestring == re.match(pattern,codestring).group():
                    return True
            except:    
                continue
        return Flag
        
    def isNum(numString):
        """Match numeric string"""
        if '.' in numString:
            idx = numString.index('.')
            return numString[:idx].isdigit() and numString[idx+1:].isdigit()
        else:
            return numString.isdigit()
            
    def isURL(urlString):
        """Match URL string"""
        urlFormat = ['\w+\.\w+']			# more format can be add here
        Flag = False
        for pattern in urlFormat:
            try:
                if re.match(pattern,urlString).group():
                    return True
            except:    
                continue
        return Flag
                
            
    looper = 0
    for token in tk:
        if isNum(token):
    	    token = 'NUM'
        elif isDate(token):
    	    token = 'DATE'
    	elif isCode(token):
    	    token = 'CODE'
    	elif isURL(token):
    	    token = 'URL'
    	elif token == 'guitar':
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

    
# construct database: doc, terms

if __name__=='__main__':
    filename = sys.argv[1]
    
    DocsTable = {}		# key: docID value: tokens
    TF = {}			# key: term  value: term frequency
    TF['NUM'] = 0		# special term - catergory NUMBER
    TF['DATE'] = 0		# special term - catergory DATE
    TF['CODE'] = 0		# special term - catergory CODE
    ReverseIndex = {}		# key: term  value: list of docID
    guitar = []			# list guitar types
    
    fp = open(filename,'r')
    docID = 1
    lastline = ''
    for line in fp:
        if line == lastline:
            continue
        tokens = preprocess(line)
        if tokens:
    	    DocsTable[docID] = tokens
    	    reverseIndex(tokens,docID)
    	    docID += 1
    	lastline = line
    fp.close()
    writeDict('Docs.txt', DocsTable)
    writeDict('ReverseIndex.txt', ReverseIndex)
    writeDict('TF.txt', TF)
    print guitar
    
