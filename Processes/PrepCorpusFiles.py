#!/usr/bin/env python
"""Converts the text files within a directory to the proper format for
creating a wordspace, namely, one word per line, all lowercase, and no
non-letter characters.
"""

import os
import subprocess

__author__ = 'Nathan Michalov'


class FormatFiles:

    def __init__(self, corpus_dir):                               #Creating an instance of the class automatically processes the target directory 
        self.corpus_dir = corpus_dir                              #Output is sent to a pre-defined folder for ease of processing
        self.prep_dir = os.getcwd()+'/CorpusPrepFiles'
        if not os.path.exists(self.prep_dir):
            os.mkdir(self.prep_dir)
        self.proc_files()
     
    def proc_files(self):                                         #Loops through the directory recursivley and finds all the '.txt' files
        count = 1                                                 #The files are then passed as arguments to proc_text 
        for root, dirs, files in os.walk(self.corpus_dir):
            for entry in files:
                if entry[-4::] == '.txt' and entry[0:2] != '._':
                    self.proc_text(root+'/'+entry, count)
                count = count + 1
        
    def proc_text(self, infile, count):                           #Uses the linux/unix shell to format the input files, then writes the output
        count = str(count)                                        #of each unique input file to a unique output file
        subprocess.call('tr [A-Z] [a-z] < '+infile+' | tr -sc [a-z] \'\012\' > '+self.prep_dir+'/Prep'+count+'.txt', shell=True)
