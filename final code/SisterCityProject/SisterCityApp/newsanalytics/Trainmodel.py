# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:18:49 2018

@author: sachi
"""

import sys, os, csv, glob, json, uuid, pickle, math
import nltk 
import gensim, logging
import numpy as np, scipy, pandas as pd
from operator import itemgetter
from IPython.display import HTML, display
import tabulate
import io
from bs4 import UnicodeDammit



CONTENT_INDEX = 9
csv.field_size_limit(sys.maxsize)
CONTENT_PATH = './inputs/contents/'
TOKENS_PATH = './inputs/tokens/'
CENTROIDS_PATH = './inputs/centroids/'

if not os.path.exists(CONTENT_PATH):
    os.makedirs(CONTENT_PATH)
    
if not os.path.exists(TOKENS_PATH):
    os.makedirs(TOKENS_PATH)
    
if not os.path.exists(CENTROIDS_PATH):
    os.makedirs(CENTROIDS_PATH)



count = 0

for fname in glob.iglob('./inputs/*.csv', recursive=False):
   # f = io.open(fname,encoding="ascii")
    with open(fname, 'rt',encoding="utf-8") as f:
        reader = csv.reader(f)
        for line in reader:
            count = count + 1
            content = line[CONTENT_INDEX]
            cname = CONTENT_PATH + str(count) + '.txt'
            tname = TOKENS_PATH + str(count) + '.tokens'
            cf = open(cname, 'w')
            cf.write(content)
            cf.close()
            tf = open(tname, 'w')
            for sentence in nltk.sent_tokenize(content):
                tf.write("%s\n" % sentence.lower())
            tf.close()

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for fname in glob.iglob(self.dirname +'*.tokens', recursive=True):
            for line in open(fname):
                yield nltk.word_tokenize(line)
                
                
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = MySentences('./inputs/tokens/') 
model1 = gensim.models.Word2Vec(sentences, min_count=1)  

model1.save('./model/w2v-lc.model')
model1.wv.save_word2vec_format('./model/w2v-lc.model.bin', binary=True)
vocab = dict([(k, v.index) for k, v in model1.wv.vocab.items()])
with open('./model/w2v-lc-vocab.json', 'w') as f:
    f.write(json.dumps(vocab))              