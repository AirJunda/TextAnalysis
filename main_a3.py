"""main_3a.py

An instance of the Text class should be initialized with a file path (a file or
directory). The example here uses object as the super class, but you may use
nltk.text.Text as the super class.

An instance of the Vocabulary class should be initialized with an instance of
Text (not nltk.text.Text).

"""
import os
import re
import nltk


from nltk.corpus import wordnet as wn
from nltk.corpus import PlaintextCorpusReader
from nltk.probability import FreqDist

"""Uncomment below if errors raised"""
#nltk.download('punkt')
#nltk.download('wordnet')


    
class FSA():
    def __init__(self, name ,states, final_states, transitions):
        self.states = states
        self.final_states = final_states
        self.transitions = transitions
        self.table = self.buildTable()
        self.name = name
 
        
    def buildTable(self):
        transtable = {}
        for state in self.states:
            transtable[state] = {}
            for link in self.transitions:
                if link[0] == state:
                    transtable[state].update({link[1]:link[2]})             
        return transtable
       
    def pp(self):
        # prety print
        for state in self.table:
            if state in self.final_states:
                print("<State " + state + " f>")
            else:
                print("<State " + state + ">")
            for key in self.table[state]:
                print("  "+ key + " --> "+  self.table[state][key])
 
    
    def accept(self,string):
        idx = 0
        curstate = self.states[0]
        table = self.table
        while idx <= len(string)-1:
            tape = string[idx]     
            if tape in table[curstate].keys(): 
                nextstate = table[curstate][tape]
                curstate = nextstate
                idx += 1
            else:
                return False
        if not curstate in self.final_states:
            return False
        else:
            return True
    
    
    def fsaMatch(self,start,tokens):
        # search a fsa pattern in a list of tokens from start index
        # if no match, return False
        idx = start
        curstate = self.states[0]
        table = self.table
        while idx <= len(tokens)-1:
            if curstate in self.final_states:
                return start, idx
            tape = tokens[idx]     
            if tape in table[curstate].keys(): 
                nextstate = table[curstate][tape]
                curstate = nextstate
                idx += 1
            else:
                return False
        if not curstate in self.final_states:
            return False
        else:
            return start, idx  # idx is the last matching position + 1
        
        
        
        
      
    

class Text(object):
    def __init__(self, path):
        if os.path.isfile(path):
            f = open(path,'rU')
            raw = f.read()
            tokens = nltk.word_tokenize(raw)            
        elif os.path.isdir(path):
            filelist = os.listdir(path) 
            tokens = []
            for file in filelist:
                filepath = path +'/'+ file
                f = open(filepath,'rU')
                raw = f.read()
                ftok = nltk.word_tokenize(raw)
                tokens = tokens + ftok

        self.text_to_str = raw
        self.text = nltk.Text(tokens)
            

        
    def apply_fsa(self,fsa):
        all_tokens = self.text.tokens
        result = []
        i = 0
        while i < len(all_tokens):            
            if fsa.fsaMatch(i,all_tokens) != False:
                start,end = fsa.fsaMatch(i,all_tokens)
                target = all_tokens[start:end]
                result.append((start, " ".join(target)))
            i += 1
        
        return result
    

    def __len__(self):
        return len(self.text_to_str)
        #Alternative, we can return len(self.text) which make senses too.
         
    def token_count(self):
        return len(self.text)
    
    def type_count(self):
        return len(set([w.lower() for w in self.text]))
    
    def sentence_count(self):
        punct = ['!','.','?']
        count = 0
        for token in self.text.tokens:
            if token in punct:
                count = count + 1
        return count
    
    def most_frequent_content_words(self):  # This function has been edited from ass2 version
        text = self.text           
        result = []
        feqlist = FreqDist(text)
        stopwords = nltk.corpus.stopwords.words('english')
        tokens = sorted(feqlist, key=feqlist.__getitem__, reverse=True) # sort the dict based on value in reverse order
        
        count = 0
        i = 0
        
        while count < 25 and i < len(tokens):
            token = tokens[i]
            if token.lower() not in stopwords and token[0].isalpha():   # here we use our teacher's definition of content word
                result.append( (token,feqlist[token]) )
                count = count + 1
            i = i + 1
        return result
            
    
    def most_frequent_bigrams(self):
        text = self.text
        allBG = list(nltk.bigrams(text))
        feqlist = FreqDist(allBG)
        result = []
        biG = sorted(feqlist, key=feqlist.__getitem__, reverse=True) #bigram
        
        count = 0
        i = 0
        while count < 25 and i < len(biG):  
            bg = biG[i]
            if self.isContentW(bg[0]) and self.isContentW(bg[1]):
                result.append( (bg,feqlist[bg]) )
                count = count + 1
            i = i + 1
        return result
        
        
    def isContentW(self,str):  
        # check if a token is a content word
        #If not stopword OR no non-alanum -> content word
        stopwords = nltk.corpus.stopwords.words('english')
        if not (str.lower() in stopwords):
            if not self.isallsymbol(str):   
                return True
        return False
    
    def isallsymbol(self,str): 
        # check if a token's chars are symbol only
        for char in str:
            if char.isalnum():
                return False
        return True
    
    
    def find_sirs(self):
        #  returns a sorted list of all sirs
        result = []
        rawtext = self.text_to_str
        pattern = re.compile(r"\bSir \S+\b") # Alternative: "Sir \S+[\w]"
        result = pattern.findall(rawtext)
        result = set(result)
        result = list(result)
        result.sort()
        return result
    
    def find_brackets(self): 
        #returns a sorted list of all bracketed expressions.
        rawtext = self.text_to_str
        pattern = re.compile(r"[(\[{].*?[)\]}]") 
        result = pattern.findall(rawtext)
        result = set(result)
        result = list(result)
        result.sort()
        return result
    
    def find_roles(self): 
        #returns a sorted list of all the roles.
        rawtext = self.text_to_str
        pattern = re.compile(r"^(?!SCENE).+?:",re.M) 
        result = pattern.findall(rawtext)
        result = set(result)
        result = list(result)       
        result = [ w[0:-1] for w in result]        
        result.sort()
        return result
    
    def find_repeated_words(self): 
        #returns a sorted list of words repeated three times
        rawtext = self.text_to_str
        pattern = re.compile(r"(\b(\w+)\b \2\b \2\b)") 
        result = pattern.findall(rawtext)
        fullmatc = [ groups[0] for groups in result]        
        fullmatc = set(fullmatc)
        fullmatc = list(fullmatc)
        fullmatc.sort()
        return fullmatc
    
    

        
class Vocabulary(object): 
    def __init__(self, TextObj):
        text = TextObj.text
        text_vocab_raw = set(w.lower() for w in text if w.isalpha())
        english_vocab = set(w.lower() for w in nltk.corpus.words.words())
        
        self.vocab = text_vocab_raw & english_vocab
        self.tokens = text.tokens
        self.text = text
        self.text_to_str = TextObj.text_to_str

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
    
    def quick(self, word):
        self.text.concordance(word)        
        
        

        

