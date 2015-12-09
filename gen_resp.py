import nltk
import nltk.tokenize
import time
from threading import Thread, Lock, Condition
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from LUT import LUTindex
from nltk.tokenize import RegexpTokenizer

import os
import sys

readfromfile = "input.txt"
writetofile = "output.txt"

def stopword_filter(words):
    return [w for w in words if w.lower() not in stopwords.words("english")]

#To change the output, you need to modify this function
#This creates the vectors that will be use to compare terms
def tokenize_text(text):
    #Tokenizes words
    line = [word for sent in sent_tokenize(text) for word in word_tokenize(sent)]
    
    #Removes punctuation
    line = [w.lower() for w in line if w.isalpha()]
    tags = nltk.pos_tag(line)
    index = 0
    for (curword, tag) in tags:
        #This makes negative adjectives negated
        if tag == 'JJ':
            str_negate = ['not','no']
            for neg_index in xrange(len(str_negate)):
                if str_negate[neg_index] in line[:index]:
                    line[index] = str_negate[neg_index] + ' ' + line[index]
                    del line[line.index(str_negate[neg_index])]
                    index -= 1
        
        index+=1
    line_priority = [0.5]*len(line)
    new_addition = stopword_filter(line)
    new_addition_priority = [1]*len(new_addition)
    return zip(line, line_priority) + zip(new_addition, new_addition_priority) 

def cosine_similarity(vector1,vector2_words):
    total = 0.0
    for i in xrange(len(vector1)):
        total+=(float(vector2_words.count(vector1[i][0]))*vector1[i][1]+0.00001)
    return total/(float(len(vector1)))

#A thread to generate response. Will go to sleep after 5 seconds.
class GenResp(Thread):
    def __init__(self, findresp):
        Thread.__init__(self)
        self.findresp = findresp
        self.current_text = '';

    def run(self):
        #always runs in the background
        while True:
            self.current_text = self.findresp.process_text(self.current_text)
            time.sleep(5.0)

class FindResp(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.monitor_write = Lock()


    def process_text(self, oldtext):
        
        #Get the line of text
        with open(readfromfile,"r") as r:
            text = r.read()
        
        if oldtext == text:
            return oldtext

        print text
        line = tokenize_text(text)        
        keys = self.dictionary.get_key_elements()
        
        #Sets up default okay response. Will return "OK" if none seem to match
        max_sim = 0.05
        max_key = keys[0]
        for cur_key in keys[1:]:
            tokenwords = zip(*tokenize_text(cur_key))[0]
            cur_sim = cosine_similarity(line, tokenwords)
            if cur_sim > max_sim:
                max_sim = cur_sim
                max_key = cur_key

        response = self.dictionary.get_response(max_key)
        print response
        self.write_to_output(response,writetofile)
        return text

    def write_to_output(self, text, outfile):
        with self.monitor_write:
            update = 0
            filewrite = open(outfile,"w")
            while update == 0:
                try:
                    mturk = filewrite.write(text)
                    #Notify a change
                    #print "A CHANGE TO OUTPUT HAS BEEN MADE!"
                    update = 1
                except MyError as e:
                    print 'waiting on file'
                    time.sleep(5.0)
            filewrite.close()

if __name__ == '__main__':
    dictionary = LUTindex()
    findresp  = FindResp(dictionary)
    GenResp(findresp).start()
