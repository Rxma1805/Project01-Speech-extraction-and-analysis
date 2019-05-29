#-*- coding:utf-8 -*-
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
from pyltp import NamedEntityRecognizer
from pyltp import SentenceSplitter
from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec
from gensim import utils
import os
import re
import pandas as pd
import re
import jieba

# ltp model path
cws_model_path = os.path.abspath('./ltp_data/cws.model')
pos_model_path = os.path.abspath('ltp_data/pos.model')
par_model_path = os.path.abspath('ltp_data/parser.model')
ner_model_path = os.path.abspath('ltp_data/ner.model')


def get_words_list(string):

    segmentor = Segmentor()
    segmentor.load(cws_model_path)
    words_list = list(segmentor.segment(string))
    segmentor.release() 
    return words_list

def get_postag_list(words_list):

    postag = Postagger()
    postag.load(pos_model_path)
    postag_list = list(postag.postag(words_list))
    postag.release()
    return postag_list

def get_ner_list(words_list, postag_list):

    ner = NamedEntityRecognizer()
    ner.load(ner_model_path)
    ner_list = list(ner.recognize(words_list, postag_list))    
    ner.release()
    return ner_list

def get_parser_list(words_list, postag_list):

    parser = Parser()
    parser.load(par_model_path)
    arcs = parser.parse(words_list, postag_list)

    arcs_list = [(arc.head, arc.relation) for arc in arcs]
    parser.release()
    return arcs_list


def cut(string):
    return ' '.join(jieba.cut(string))

def load(file_path, column_name = "content"):

    df = pd.read_csv(file_path, encoding='gb18030')
    df = df.fillna('')
    news_content = df[column_name].tolist()
    return news_content

def token(string):
    return re.findall(r'[\d|\w]+', string)

def get_cutfile(file_name, news_content):
    with open(file_name, 'w') as f:
        for content in news_content:
            f.write(content + '\n')

def save_moedl(file_path, size = 100, window = 3, cnt = 1, worker = 4):
    path = get_tmpfile("word2vec.model")
    model = Word2Vec(LineSentence(file_path), size = size, window = window, min_count = cnt, workers = worker)
    model.save("word2vec.model")

def load_model(model_path):
    model = Word2Vec.load(model_path)
    return model