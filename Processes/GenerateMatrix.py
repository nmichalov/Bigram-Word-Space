#!/usr/bin/env python
"""Generates a wordspace from the coocs files created in the previous step.
When initialized, a simple matrix of the frequency scores is created and saved,
but calling the reduce_matrix method returns a matrix with the raw frequency counts
replaced by tf-idf values, and use singular value decomposition to create a matrix of
reduced dimensionality.
"""

import gensim
import os

__author__ = 'Nathan Michalov'

class GenerateMatrix:                                           #This is essentially just an implementation of the tools found
                                                                #in the gensim module
    def __init__(self, cooc_directory, num_topics):
        self.cooc_directory = cooc_directory
        self.num_topics = num_topics
        self.word_id = self.merge_elements()
        self.dictionary = self.create_dictionary()
        self.corpus = self.create_corpus()
        
    def merge_elements(self):                                 #All of the co-occurence files are merged into a single document, with 
        word_id = {}                                          #each ngram occupying a single line in the file.
        position = 0                                          #This is done to simplify the matrix creation process 
        cooc_files = os.listdir(self.cooc_directory)          #as gensim is structured to operate in this way.
        output_corpus = open('WordVectors.txt', 'a')          #To ensure that ngrams can be matched to lines, a dictionary is created
        for document in cooc_files:                           #which links each ngram with its position in the merged file.
            word_id[position] = document[0:-4]
            text = open(self.cooc_directory+'/'+document, 'r')
            for line in text:
                line = line.rstrip('\n')
                output_corpus.write(line+' ')
            text.close()
            output_corpus.write('\n')
            position = position + 1
        output_corpus.close()
        return word_id
            
    def create_dictionary(self):
        dictionary = gensim.corpora.Dictionary(line.split() for line in open('WordVectors.txt'))       #A dictionary of all the ngrams is created, which is used for converting 
        return dictionary                                                                              #the word counts to vectors
    
    def create_corpus(self):
        corpus = [self.dictionary.doc2bow(word) for word in open('WordVectors.txt')]                   #A matrix of raw counts is created and saved
        gensim.corpora.MmCorpus.serialize('CoocCorpus.mm', corpus)
        return gensim.corpora.MmCorpus('CoocCorpus.mm')

    def reduce_matrix(self):                                   #calling the reduce_matrix method actually processes the raw counts matrix into the semantic matrix we're interested in
        tfidf = gensim.models.TfidfModel(self.corpus)          #this object is what is used for subsquent work on evaluating composition operations.
        tfidf_corpus = tfidf[self.corpus]
        lsi = gensim.models.LsiModel(tfidf_corpus, self.num_topics, id2word=self.dictionary)
        lsi_matrix = lsi[tfidf_corpus]
        return lsi_matrix
       
