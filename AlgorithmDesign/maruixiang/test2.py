from pyltp import Segmentor
from pyltp import NamedEntityRecognizer
from pyltp import Postagger
import chardet
import pandas as pd
import os

model_path = os.path.abspath('./coach/ltp_data_v3.4.0/cws.model')
pos_path = os.path.abspath('./coach/ltp_data_v3.4.0/pos.model')


with open('../data/cont.txt', 'rb') as f:
    encoding = chardet.detect(f.readline())
print(encoding)

with open('../data/cont.txt','r',encoding='utf8') as f:
    content = f.read()
print(content)

for line in content.split('\n'):
    print(line)
    print('----')


seg = Segmentor()
seg.load(model_path)
words = seg.segment(content)
seg.release()


pos = Postagger()
pos.load(pos_path)
postag = pos.postag(words)
pos.release()
union = list(zip(list(words),list(postag)))
union_list = [x+' :'+y for x,y in union]


ner_path = os.path.abspath('./coach/ltp_data_v3.4.0/ner.model')
recognizer = NamedEntityRecognizer()
recognizer.load(ner_path)
# print(list(words))
# print(list(postag))
ner_list = recognizer.recognize(list(words),list(postag))
ner_list = pd.Series(ner_list,dtype='str')
# ner_list = ner_list.loc[ner_list.apply(lambda x : str(x) != '0')]
ner_list_index=ner_list.loc[ner_list.apply(lambda x : x != 'O')]

# pd.Series.index2word
# print(ner_list_index)
words_list = pd.Series(words).iloc[ner_list_index.index]
print(pd.Series(words).iloc[ner_list_index.index])
# print('\t'.join(list(words)))
# print('\t'.join(list(ner_list)))
# print('\n'.join([x+':'+y for x,y in list(zip(list(words),list(ner_list)))]))
recognizer.release()

from pyltp import Parser
parser_model_path = './coach/ltp_data_v3.4.0/parser.model'
parser = Parser()
parser.load(parser_model_path)
arcs =  parser.parse(list(words),list(postag))
# print(list(words))
# print ("\n".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
# printint ("|\t|".join("%s:%s" % (list(words)[arc.head], arc.relation) for arc in arcs))

arc_dic = {}
for arc in arcs:
    arc_dic[arc.head] = arc.relation

view =[(words_list[x],arc_dic[x]) for x in words_list.index.tolist() if x in arc_dic]
print(view)

parser.release()