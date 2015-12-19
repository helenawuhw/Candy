import nltk
import nltk.tokenize
import time
from threading import Thread, Lock, Condition
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from LUT import LUTindex
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
from firebase import Firebase

import os
import sys
stemmer = PorterStemmer()

#Variable to debug output
debug = 0

#Default store places
readfromfile = "input.txt"
writetofile = "output.txt"
fw = Firebase('https://fiery-heat-7465.firebaseio.com/message_list')
fr = Firebase('https://fiery-heat-7465.firebaseio.com/read_message')
testfile = "test_input.txt"

def stopword_filter(words):
    return [w for w in words if w.lower() not in stopwords.words("english")]


def stem_filter(words):
    return [stemmer.stem(w) for w in words if stemmer.stem(w) != ' ']

#To change the output, you need to modify this function
#This creates the vectors that will be use to compare terms
def tokenize_text(text, model=0.0):
    #Tokenizes words
    line = [word for sent in sent_tokenize(text) for word in word_tokenize(sent)]
    #Removes punctuation
    if model == 0.0:
        line = stem_filter(line)
        line = [w.lower() for w in line if w.isalpha()]
        tags = nltk.pos_tag(line)
        #print tags
        index = 0
        for (curword, tag) in tags:
            #This makes negative adjectives negated
            str_negate = ['not','no', 'never', 'neither', 'nor', 'not','no', 'never', 'neither', 'nor']
            if tag == 'JJ' or tag == 'NN' or tag == 'VB':
                for neg_index in xrange(len(str_negate)):
                    if str_negate[neg_index] in line[:index]:
                        if line[index].startswith('negate '):
                            line[index] = line[index].replace('negate ','')
                        else:
                            line[index] = 'negate' + ' ' + line[index]
                        del line[line.index(str_negate[neg_index])]
                        index -= 1
                                
            index+=1
        line_priority = [1]*len(line)
        new_addition = stopword_filter(line)
        new_addition_priority = [1]*len(new_addition)
        return zip(line, line_priority) + zip(new_addition, new_addition_priority)
    elif model == 1.0:
        line_priority = [1]*len(line) 
        return zip(line, line_priority)
    elif model == 1.1:
        line = stem_filter(line)
        line = [w.lower() for w in line if w.isalpha()]
        line_priority = [1]*len(line) 
        return zip(line, line_priority)
    elif model == 1.2:
        line = [w.lower() for w in line if w.isalpha()]
        line = stopword_filter(line)
        line_priority = [1]*len(line) 
        return zip(line, line_priority)
    elif model == 1.3:
        line = stem_filter(line)
        line = [w.lower() for w in line if w.isalpha()]
        line = stopword_filter(line)
        line_priority = [1]*len(line) 
        return zip(line, line_priority)
    elif model == 2.0:
        line = stem_filter(line)
        line = [w.lower() for w in line if w.isalpha()]
        line_priority = [0.05]*len(line)
        new_addition = stopword_filter(line)
        new_addition_priority = [1]*len(new_addition)
        return zip(line, line_priority) + zip(new_addition, new_addition_priority)
    elif model == 2.1:
        line = stem_filter(line)
        line = [w.lower() for w in line if w.isalpha()]
        line_priority = [0.15]*len(line)
        new_addition = stopword_filter(line)
        new_addition_priority = [1]*len(new_addition)
        return zip(line, line_priority) + zip(new_addition, new_addition_priority)
    elif model == 2.2:
        line = stem_filter(line)
        line = [w.lower() for w in line if w.isalpha()]
        line_priority = [0.25]*len(line)
        new_addition = stopword_filter(line)
        new_addition_priority = [1]*len(new_addition)
        return zip(line, line_priority) + zip(new_addition, new_addition_priority)
    elif model == 2.3:
        line = stem_filter(line)
        line = [w.lower() for w in line if w.isalpha()]
        line_priority = [0.5]*len(line)
        new_addition = stopword_filter(line)
        new_addition_priority = [1]*len(new_addition)
        return zip(line, line_priority) + zip(new_addition, new_addition_priority)
    elif model == 2.4:
        line = stem_filter(line)
        line = [w.lower() for w in line if w.isalpha()]
        line_priority = [1]*len(line)
        new_addition = stopword_filter(line)
        new_addition_priority = [1]*len(new_addition)
        return zip(line, line_priority) + zip(new_addition, new_addition_priority)
    elif model == 2.5:
        line = stem_filter(line)
        line = [w.lower() for w in line if w.isalpha()]
        line_priority = [3]*len(line)
        new_addition = stopword_filter(line)
        new_addition_priority = [1]*len(new_addition)
        return zip(line, line_priority) + zip(new_addition, new_addition_priority)        
    elif model == 2.6:
        line = stem_filter(line)
        line = [w.lower() for w in line if w.isalpha()]
        line_priority = [9]*len(line)
        new_addition = stopword_filter(line)
        new_addition_priority = [1]*len(new_addition)
        return zip(line, line_priority) + zip(new_addition, new_addition_priority)
    elif model == 3.0:
        line = stem_filter(line)
        line = [w.lower() for w in line if w.isalpha()]
        line_priority = [1]*len(line)
        new_addition = stopword_filter(line)
        new_addition_priority = [1]*len(new_addition)
        return zip(line, line_priority) + zip(new_addition, new_addition_priority)
    elif model == 3.2:    
        line = stem_filter(line)
        line = [w.lower() for w in line if w.isalpha()]
        tags = nltk.pos_tag(line)
        #print tags
        index = 0
        for (curword, tag) in tags:
            #This makes negative adjectives negated
            str_negate = ['not','no', 'never', 'neither', 'nor']
            if tag == 'JJ' or tag == 'NN':
                for neg_index in xrange(len(str_negate)):
                    if str_negate[neg_index] in line[:index]:
                        line[index] = 'negate' + ' ' + line[index]
                        del line[line.index(str_negate[neg_index])]
                        index -= 1
            elif tag == 'VB':
                for neg_index in xrange(len(str_negate)):
                    if str_negate[neg_index] in line[:index]:
                        line[index] = 'negate' + ' ' + line[index]
                        del line[line.index(str_negate[neg_index])]
                        index -= 1
                                
            index+=1
        line_priority = [1]*len(line)
        new_addition = stopword_filter(line)
        new_addition_priority = [1]*len(new_addition)
        return zip(line, line_priority) + zip(new_addition, new_addition_priority)
    elif model == 3.1:    
        line = stem_filter(line)
        line = [w.lower() for w in line if w.isalpha()]
        tags = nltk.pos_tag(line)
        #print tags
        index = 0
        for (curword, tag) in tags:
            #This makes negative adjectives negated
            str_negate = ['not','no', 'never', 'neither', 'nor']
            if tag == 'JJ' or tag == 'NN' or tag == 'VB':
                for neg_index in xrange(len(str_negate)):
                    if str_negate[neg_index] in line[:index]:
                        line[index] = 'negate' + ' ' + line[index]
                        del line[line.index(str_negate[neg_index])]
                        index -= 1
                                
            index+=1
        line_priority = [1]*len(line)
        new_addition = stopword_filter(line)
        new_addition_priority = [1]*len(new_addition)
        return zip(line, line_priority) + zip(new_addition, new_addition_priority)  
def cosine_similarity(vector1,vector2_words):
    total = 0.0
    if vector1 is None:
        return 0.0
    for i in xrange(len(vector1)):
        total+=(float(vector2_words.count(vector1[i][0]))*vector1[i][1]+0.00001)
    if len(vector1) == 0:
        return 0.0
    return total/(float(len(vector1)))

#A thread to generate response. Will go to sleep after 5 seconds.
class GenResp(Thread):
    def __init__(self, findresp):
        Thread.__init__(self)
        self.findresp = findresp
        self.current_text = '';
        self.time_out = 0

    def run(self):
        #always runs in the background
        while self.time_out < 300:
            new_text = self.findresp.process_text(self.current_text)
            if self.current_text == new_text:
                self.time_out += 1
            else:
                self.time_out = 0
            self.current_text = new_text
            time.sleep(1.0)

class TestResp(Thread):
    def __init__(self, findresp):
        Thread.__init__(self)
        self.findresp = findresp
        self.float_vec = [[1.0,1.1,1.2,1.3],[2.0,2.1,2.2,2.3,2.4,2.5,2.6],[3.0,3.2,3.1,0.0]]
        with open(testfile,"r") as r:
            self.testfile = r.read().split("\n") 

    def run(self):
        #---------------------------
        #Test for stemming versus stopping
        numcases = float(len(self.testfile))
        tests = self.float_vec[0]
        print "----------------------------"
        print "stemming vs stopping"
        for test_element in tests:
            count = 0.0
            for line in self.testfile:
                test_line = line.split(":")
                #print test_line
                predictedresp = findresp.process_text(' ',0,test_element,test_line[0])
                actualresp = test_line[1]
                if actualresp.lower() == predictedresp.lower():
                    count += (1.0/numcases)
            print '*********'
            print 'test number: ' + str(test_element)
            print 'accuracy: ' + str(count)

        #---------------------------
        #Test for weight of words
        tests = self.float_vec[1]
        print "----------------------------"
        print "testing different weights"
        for test_element in tests:
            count = 0.0
            for line in self.testfile:
                test_line = line.split(":")
                predictedresp = findresp.process_text(' ',0,test_element,test_line[0])
                actualresp = test_line[1]
                if actualres.lower() == predictedresp.lower():
                    count += (1.0/numcases)
                #else:
                #    print test_line[0]
            print '*********'
            print 'test number: ' + str(test_element)
            print 'accuracy: ' + str(count)

        #---------------------------
        #Test for negation
        tests = self.float_vec[2]
        print "----------------------------"
        print "testing negation"
        for test_element in tests:
            count = 0.0
            for line in self.testfile:
                test_line = line.split(":")
                predictedresp = findresp.process_text(' ',0,test_element,test_line[0])
                actualresp = test_line[1]
                if actualresp.lower() == predictedresp.lower():
                    count += (1.0/numcases)
            print '*********'
            print 'test number: ' + str(test_element)
            print 'accuracy: ' + str(count)

        return


class FindResp(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.monitor_write = Lock()

    def process_text(self, oldtext, write=1, testno=0.0, textline=' '):
        
        #Get the line of text
        if write:
            if debug:
                with open(readfromfile,"r") as r:
                    text = r.read()
                if oldtext == text:
                    return oldtext
            else:
                mydict = fr.get()
                res = sorted(fr.get().iterkeys())
                text = str(mydict[res[len(res)-1]]['text'])
                if oldtext == str(res[len(res)-1]):
                    return oldtext
        else:
            text = textline


        line = tokenize_text(text,testno)        
        keys = self.dictionary.get_key_elements()
        if write:
            print line

        #Sets up default okay response. Will return "OK" if none seem to match
        max_sim = 0.05
        max_key = keys[0]
        keys.sort()

        for cur_key in keys[1:]:
            temptext = tokenize_text(cur_key,testno)
            if temptext is not None and len(temptext) > 1:
                tokenwords = zip(*temptext)[0]
            else:
                tokenwords = []
            cur_sim = cosine_similarity(line, tokenwords)
            if cur_sim > max_sim:
                max_sim = cur_sim
                max_key = cur_key

        response = self.dictionary.get_response(max_key)
        if write:
            print response
        if write:
            self.write_to_output(response,writetofile)
        if write == 1 and debug == 1:
            return text
        elif write == 1 and debug == 0:
            return str(res[len(res)-1])
        else:
            return response

    def write_to_output(self, text, outfile):
        with self.monitor_write:
            update = 0
            filewrite = open(outfile,"w")
            #TODO: maybe clear the db?
            while update == 0:
                try:
                    filewrite.write(text)
                    r = fw.delete()
                    r = fw.push({'name': 'message', 'text': text})
                    print "done"
                    update = 1
                except:
                    print 'waiting on file'
                    time.sleep(5.0)
            filewrite.close()

if __name__ == '__main__':
    dictionary = LUTindex()
    findresp  = FindResp(dictionary)
    GenResp(findresp).start()
    #TestResp(findresp).start()
