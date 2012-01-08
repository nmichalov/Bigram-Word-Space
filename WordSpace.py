#!/usr/bin/env python
"""A function for calling the three processes in order to convert a collection
of unprocessed text into a semantic wordspace which can be used for evaluating
the performance of different proposed methods of vector space compostion (pointwise multiplication,
tensor product, PLSR, etc).

Dependencies: os, subprocess, gensim modules
"""


import os
import Processes

__author__ = 'Nathan Michalov'


class WordSpace:

    def __init__(self, corpus_directory, bigram_row_number, reduced_dimensions):    #location of the corpus, number of bigrams desired, and number of dimensions of
        self.corpus_directory = corpus_directory                                    #semantic space must be specified
        self.bigram_row_number = bigram_row_number
        self.reduced_dimensions = reduced_dimensions

    def get_wordspace(self):                                                        #the method that actually generates the word space
        Processes.PrepCorpusFiles.FormatFiles(self.corpus_directory)
        freqs = Processes.ProcPrepFiles.GetFreqs()
        bigrams = freqs.bigram_counts()
        rows = Processes.ProcPrepFiles.GetRows(bigrams, self.bigram_row_number)
        bigram_rows, unigram_rows = rows.row_elements()
        Processes.ProcPrepFiles.GetCoocs(bigram_rows, unigram_rows)
        cooc_directory = os.getcwd()+'/CoocFiles'
        raw_matrix = Processes.GenerateMatrix.GenerateMatrix(cooc_directory, self.reduced_dimensions)
        wordspace = raw_matrix.reduce_matrix()
        return wordspace



