"""main.py

Code scaffolding

"""

import os
import nltk
import math
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import PlaintextCorpusReader
from nltk.probability import FreqDist
from nltk.text import Text


nltk.download('stopwords')
nltk.download('words')
nltk.download('wordnet')
nltk.download('brown')


def read_text(path):
    #emma = read_text('data/emma.txt')
    #wsj = read_text('data/wsj')
    if os.path.isfile(path):
        f = open(path,'rU')
        raw = f.read()
        tokens = nltk.word_tokenize(raw)
        return nltk.Text(tokens)
    if os.path.isdir(path):
        filelist = os.listdir(path) 
        tokens = []
        for file in filelist:
            filepath = path +'/'+ file
            f = open(filepath,'rU')
            raw = f.read()
            ftok = nltk.word_tokenize(raw)
            tokens = tokens + ftok
        return nltk.Text(tokens)
             
        
def token_count(text):
    result = []
    fedqist = [][[as]]
    
    
def type_count(text):
    return len(set(text))


def sentence_count(text):
    punct = ['!','.','?']
    count = 0
    for token in text.tokens:
        if token in punct:
            count = count + 1
    return count         


def most_frequent_content_words(text):
    result = []
    feqlist = FreqDist(text)
    stopwords = nltk.corpus.stopwords.words('english')
    tokens = sorted(feqlist, key=feqlist.__getitem__, reverse=True) # sort the dict based on value in reverse order
    
    count = 0
    i = 0
    
    while count < 25 and i < len(tokens):
        token = tokens[i]
        if token.lower() not in stopwords and token.isalnum():
            result.append( (token,feqlist[token]) )
            count = count + 1
        i = i + 1
    return result
            

def most_frequent_bigrams(text):  
    allBG = list(nltk.bigrams(text))
    feqlist = FreqDist(allBG)
    result = []
    biG = sorted(feqlist, key=feqlist.__getitem__, reverse=True) #bigram
    
    count = 0
    i = 0
    while count < 25 and i < len(biG):  
        bg = biG[i]
        if isContentW(bg[0]) and isContentW(bg[1]):
            result.append( (bg,feqlist[bg]) )
            count = count + 1
        i = i + 1
    return result
    
    
def isContentW(str):  
    # check if a token is a content word
    #If not stopword OR no non-alanum -> content word
    stopwords = nltk.corpus.stopwords.words('english')
    if not (str.lower() in stopwords):
        if not isallsymbol(str):   
            return True
    return False

def isallsymbol(str): 
    # check if a token's chars are symbol only
    for char in str:
        if char.isalnum():
            return False
    return True


class Vocabulary(): 

    def __init__(self, text):
        text_vocab_raw = set(w.lower() for w in text if w.isalpha())
        english_vocab = set(w.lower() for w in nltk.corpus.words.words())
        
        self.vocab = text_vocab_raw & english_vocab
        self.tokens = text.tokens
        self.text = text

    def frequency(self, word):
        sources = self.tokens
        count = sources.count(word)
        return count
 

    def pos(self, word):
        if len(wn.synsets(word)) == 0:
            result = None
        else:
            result  = wn.synsets(word)[0].pos()
        return result
     

    def gloss(self, word):
        if len(wn.synsets(word)) == 0:
            return None
        
        syns = wn.synsets(word)
        return syns[0].definition()
    
    def quick(self, word): # same
        self.text.concordance(word)
        


categories = ('adventure', 'fiction', 'government', 'humor', 'news')


def compare_to_brown(text):
    """The union of the common words from five categories were taken.
    While construt the vector, non-alnum tokens were skiped.
    
    In the future, I may explore to see if one more removal of stop words can have make the
    comparison more meaningful.
    
    I am satisfied with my result. For example, wsj has the highest similarity with news, which is 
    consistent with the natural of wsj. In comparison, grail and emma has lower similarity to news.
    """
    
    
    ne = brown.words(categories='news')
    hu = brown.words(categories='humor')
    go = brown.words(categories='government')
    fi = brown.words(categories='fiction')
    ad = brown.words(categories='adventure')
    
    
    news = set(w.lower() for w in ne)    
    humo = set(w.lower() for w in hu)    
    gov = set(w.lower() for w in go)    
    fic = set(w.lower() for w in fi)   
    adve = set(w.lower() for w in ad)    
    com = news & humo & gov & fic & adve
    comlw = set(w for w in com if w.isalpha())  
    comw = list(comlw)
    comw.sort()
    # vector form of each category and given text
    vect_news = vectl(comw,ne)
    vect_humo = vectl(comw,hu)
    vect_gov = vectl(comw,go)
    vect_fic = vectl(comw,fi)
    vect_ad = vectl(comw,ad)
    vect_txt = vectl(comw,text)

# similarity to each category
    s_news = cossiml(vect_txt,vect_news)
    s_humo = cossiml(vect_txt,vect_humo)
    s_gov = cossiml(vect_txt,vect_gov)
    s_fic = cossiml(vect_txt,vect_fic)
    s_adve = cossiml(vect_txt,vect_ad)
    
    result = {'adventure': s_adve, 'fiction': s_fic, 'government': s_gov, 'humor': s_humo, 'news': s_news} 
    for i in result:
        print(i + ": "+ "{:.2f}".format(result[i]))
    
       
 # vectorlization    
def vectl(comlw,words): 
    vect = [0] * len(comlw)
    fdist = nltk.FreqDist(w.lower() for w in words)
    for i in range(0,len(comlw)):
        key = comlw[i]
        freq = fdist[key]  
        vect[i] = freq 
    return vect

def cossiml(v1,v2):
    if len(v1) != len(v1):
        return 'The deminsion of the input vectors must be equal!'
    
    dotp = 0
    for i in range(0,len(v1)):
        dotp = dotp + v1[i]*v2[i]
    
    v1sq = [elm**2 for elm in v1]
    v2sq = [elm**2 for elm in v2]
    
    return dotp/( math.sqrt(sum(v1sq)) * math.sqrt(sum(v2sq)) )
    
    
    
    
    





if __name__ == '__main__':

    
    vocab = Vocabulary(read_text('data/grail.txt'))
    vocab.frequency('swallow')
    vocab.pos('swallow')
    vocab.gloss('swallow')
    vocab.quick('swallow')

    
    
    grail = read_text('data/grail.txt')
    emma = read_text('data/emma.txt')
    wsj = read_text('data/wsj')
    print('Similarity with grail  \n')
    cmptograil = compare_to_brown(grail)
    print('Similarity with emma  \n')
    compare_to_brown(emma)
    print('Similarity with wsj  \n')
    compare_to_brown(wsj)
