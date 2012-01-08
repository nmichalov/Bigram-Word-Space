#!/usr/bin/env python
"""Processes the properly formated input files, first by getting a dictionary
of bigram frequencies, then by selecting the most frequently occuring bigrams
and their constituent elements to serves as the row elements of the semantic
matrix.  After the elements have been selected, a file is created for each row
element, and all words occuring within a 10 word window (5 before, 5 after) are
extracted from the corpus files.  These co-occurence words are then used to
generate the vector representations of each word.
"""

import cPickle
import os
import subprocess

__author__ = 'Nathan Michalov'

class GetFreqs:         #Loops through each of the prep files and creates a dictionary of bigram frequencies
    
    def __init__(self, stop_word_file='StopWords.pkl', prep_dir=os.getcwd()+'/CorpusPrepFiles'):  #stop words can be specified, and a default file is provided
        self.prep_dir = prep_dir                                                                  #note that stop words are not ignored in the later stages
        self.stop_words = self.get_stop_words(stop_word_file)                                     #but are considered here so as to prevent the selection of 
                                                                                                  #frequent but non-meaningful bigrams.
    def get_stop_words(self, stop_word_file):
        pickle_stops = open(stop_word_file)
        stop_words = cPickle.load(pickle_stops)
        pickle_stops.close()
        return stop_words

    def bigram_counts(self):                                  #loops through the prep files and gets bigrams by
        bigram_freq = {}                                      #creating a list which holds only two adjacent words at a time 
        for entry in os.listdir(self.prep_dir):
            bigram = []
            text = open(self.prep_dir+'/'+entry, 'r')
            for line in text:
                line = line.rstrip('\n')
                bigram.append(line)
                if len(bigram) == 2:
                    if bigram[0] not in self.stop_words and bigram[1] not in self.stop_words:
                        if bigram[0]+'-'+bigram[1] not in bigram_freq:
                            bigram_freq[bigram[0]+'-'+bigram[1]] = 1
                        else:
                            bigram_freq[bigram[0]+'-'+bigram[1]] = bigram_freq[bigram[0]+'-'+bigram[1]] + 1
                    del(bigram[0])
            text.close()
        return bigram_freq

    


class GetRows:                                                  #After obtaining the bigram frequencies
                                                                #the dictionary is used to generate a list, sorted from
    def __init__(self, bigram_freq, bigram_entries):            #most frequent to least frequent
        self.bigram_counts = self.sort_bigrams(bigram_freq)     #user input 'bigram_entries' specifies the number of 
        self.bigram_entries = bigram_entries                    #bigrams the user wishes to have become rows in the semantic space.
                                                                #so if n = 'bigram_entries', then the n most frequent
    def sort_bigrams(self, bigram_freqs):                       #bigrams will be selected, as well as their constituent unigrams
        bigrams = []                                            #to become the row elements of the semantic space.
        while bigram_freqs:
            key, value = bigram_freqs.popitem()
            bigrams.append((value, key))
        bigrams = sorted(bigrams, reverse=True) 
        return bigrams

    def row_elements(self):
        row_bigrams = []
        row_unigrams = []
        x = self.bigram_entries
        while x > 0:
            bigram = (self.bigram_counts[x])[1]
            row_bigrams.append(bigram)
            for unigram in bigram.split('-'):
                if unigram not in row_unigrams:
                    row_unigrams.append(unigram)
            x = x - 1
        return row_bigrams, row_unigrams
  




class GetCoocs:
                                                                     #Given the ngrams selected to serve as the row elements of the semantic space
    def __init__(self, row_bigrams, row_unigrams):                   #each ngram is treated abstractly as a document, with the words occuring within the 
        self.row_bigrams = row_bigrams                               #10 word window around it as the content of the document
        self.row_unigrams = row_unigrams
        self.directory = os.getcwd()
        if not os.path.exists(self.directory+'/CoocFiles'):
            os.makedirs(self.directory+'/CoocFiles')
        self.get_coocs()
        
    def get_coocs(self):
        for unigram in self.row_unigrams:                            #Again, simple unix/linux shell tools are used.  A recursive grep search finds all instances of each ngram, and sed strips
            output = self.directory+'/CoocFiles/'+unigram+'.txt'     #the ngram itself and the formatting characters seperating the files, and the output is appended to a unique file for each ngram. 
            subprocess.call('grep -rwh -C5 '+unigram+' CorpusPrepFiles | sed \'s/'+unigram+'\|\-//g\' > '+output, shell=True)
        for bigram in self.row_bigrams:
            output = self.directory+'/CoocFiles/'+bigram+'.txt'
            word1, word2 = bigram.split('-')
            subprocess.call('grep -rwh -C6 '+word1+' CorpusPrepFiles | tr -s \'\012\' \'#\' | sed \'s/'+word1+'#'+word2+'/'+word1+' '+word2+'/g\' | tr -s \'#\' \'\012\' | grep -C5 \''+word1+' '+word2+'\' | sed \'s/'+word1+' '+word2+'\|\-//g\' > '+output, shell=True)
