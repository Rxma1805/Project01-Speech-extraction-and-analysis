from pyltp import  Segmentor
import os
import chardet
import pandas as pd

file_name = os.path.abspath("""../data/news_chinese_sqlResult_1558435.csv""")
model_path = os.path.abspath('./coach/ltp_data_v3.4.0/cws.model')
pos_path = os.path.abspath('./coach/ltp_data_v3.4.0/pos.model')


with open(file_name, 'rb') as f:
    encoding = chardet.detect(f.readline())
print(encoding)

df = pd.read_csv(file_name, encoding=encoding['encoding'], error_bad_lines=False, header=None, dtype='str')
content = df.iloc[0,3]
with open('../data/cont.txt','r',encoding='utf8') as f:
    content = f.read()
# print(content)
seg = Segmentor()
seg.load(model_path)
words = seg.segment(content)
seg.release()

from pyltp import Postagger
pos = Postagger()
pos.load(pos_path)
postag = pos.postag(words)
pos.release()
union = list(zip(list(words),list(postag)))
union_list = [x+' :'+y for x,y in union]
# print('\n'.join(union_list))

from pyltp import NamedEntityRecognizer
ner_path = os.path.abspath('./coach/ltp_data_v3.4.0/ner.model')
recognizer = NamedEntityRecognizer()
recognizer.load(ner_path)
# print(list(words))
# print(list(postag))
ner_list = recognizer.recognize(list(words),list(postag))
# print(list(ner_list))
print('\t'.join(list(words)))
print('\t'.join(list(ner_list)))
print('\n'.join([x+':'+y for x,y in list(zip(list(words),list(ner_list)))]))
recognizer.release()

from pyltp import Parser
parser_model_path = './coach/ltp_data_v3.4.0/parser.model'
parser = Parser()
parser.load(parser_model_path)
arcs =  parser.parse(list(words),list(postag))
print(list(words))
print ("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
print ("|\t|".join("%s:%s" % (list(words)[arc.head], arc.relation) for arc in arcs))
parser.release()

# print('-----------------')
# from pyltp import SentenceSplitter
# sents = SentenceSplitter.split(content)
# print('\n'.join(sents))