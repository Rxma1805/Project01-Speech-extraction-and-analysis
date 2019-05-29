from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from tkinter import _flatten
from scipy.spatial.distance import cosine
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
from pyltp import NamedEntityRecognizer
from pyltp import SentenceSplitter
import os
import jieba

class WordExtract():

    def __init__(self):
        self.cwm_path = os.path.abspath('./ltp_data_v3.4.0/cws.model')
        self.pos_model_path = os.path.abspath('./ltp_data_v3.4.0/pos.model')
        self.par_model_path = os.path.abspath('./ltp_data_v3.4.0/parser.model')
        self.ner_model_path = os.path.abspath('./ltp_data_v3.4.0/ner.model')
        get_word_find_path = os.path.abspath('./data/get_word.txt')
        self.sign_list = [':', '：', ',', '，']
        self.start_sign_list = ['"', '“', '”']
        self.end_sign_list = ['!', '.', '?', '。', '"', '”']
        self.speak_word_list = []
        # '''读取说的词'''
        with open(get_word_find_path) as f:
            line = f.readline()
            while line:
                line = line.strip()
                self.speak_word_list.append(line)
                line = f.readline()
        self.vectorizer()


    def get_speak_sentence(self,sentences):
        '''
        获取说的动词后面，从第一个符号开始，到第一个符号（！？。.”）结束
        '''
        if sentences[0] in self.sign_list:
            return self.get_speak_sentence(sentences[1:])
        else:
            if sentences[0] in self.start_sign_list:
                for i in range(1,len(sentences)):
                    if sentences[i] in self.start_sign_list:
                        if i < len(sentences) - 1 and sentences[i + 1] in self.start_sign_list:
                            return sentences[1:i+1]
                        else:
                            return sentences[1:i]+'。'
                    elif i == len(sentences)-1:
                        return sentences[1:]

            else:
                for i in range(0,len(sentences)):
                    if sentences[i] in self.end_sign_list :
                        return sentences[0:i+1]
                    # elif sentences[i] in self.end_sign_list:
                    #     return sentences[0:i + 1]
                    elif i == len(sentences)-1:
                        return sentences[0:]

        return ""

    def extract_from_sentence(self,line):
        '''
        使用哈工大ltp分解语句
        '''
        line = line.strip()
        #     line = 'A股早在2013年6月就已纳入新兴市场指数的候选列表中，但此后几年，都因为配额分配、资本流动限制、资本利得税等所谓原因而遭否决，尤其是在2016年第三次闯关失败后，中国投资者和相关监管部门似乎对“A股入摩”已心灰意冷，甚至连证监会分管国际合作的副主席方星海都在今年一月份的时候表示，“中国与MSCI在股指期货上的观点存在分歧，中国并不急于加入MSCI全球指数”。'
        #     line = 'A股早在2013年6月就已纳入新兴市场指数的候选列表中，但此后几年，都因为配额分配、资本流动限制、资本利得税等所谓原因而遭否决，“中国与MSCI在股指期货上的观点存在分歧，中国并不急于加入MSCI全球指数”,证监会分管国际合作的副主席方星海都在今年一月份的时候表示。'
        #     line = '中国投资者和相关监管部门似乎对“A股入摩”已心灰意冷，甚至连证监会分管国际合作的副主席方星海都在今年一月份的时候表示，“中国与MSCI在股指期货上的观点存在分歧，中国并不急于加入MSCI全球指数”。'
        #     line = '唐纳德·唐对Obike的到来说道：“竞争是好事。”他的首批160辆单车6月19日将从中国运达，他的计划是在6个月的时间内向大悉尼地区街道投放6000辆单车。'
        segmentor = Segmentor()  # 初始化实例
        segmentor.load(self.cwm_path)  # 加载模型，第二个参数是您的外部词典文件路径
        words = segmentor.segment(line)
        #     print(list(words))
        postagger = Postagger()  # 初始化实例
        postagger.load(self.pos_model_path)  # 加载模型

        postags = postagger.postag(words)  # 词性标注

        recognizer = NamedEntityRecognizer()  # 初始化实例
        recognizer.load(self.ner_model_path)  # 加载模型
        netags_list = [words[i] for i, k in enumerate(list(recognizer.recognize(words, postags))) if k != 'O']
        #     print(netags_list)

        # sents = SentenceSplitter.split(line)  # 分句

        parser = Parser()  # 初始化实例
        parser.load(self.par_model_path)  # 加载模型

        arcs = parser.parse(words, postags)  # 句法分析
        arc_list = [(arc.head, arc.relation) for arc in arcs]

        parser.release()  # 释放模型
        segmentor.release()
        postagger.release()  # 释放模型
        recognizer.release()

        for k, v, pos in zip(words, arc_list, postags):
            if v[0] > 0:
                if words[v[0] - 1] in self.speak_word_list and v[1] == 'SBV' and k in netags_list:
                    # 遇到第一个结束标志即返回
                    return (True, k, words[v[0] - 1], ' '.join(jieba.cut(self.get_speak_sentence(''.join(words[v[0]:])))))
        return (False, None, None, None)


    def get_two_sentence_distent(self,sent1,sent2,mode = 1,trheshold=0.4):
        '''
        判断句子的相似性
        '''
        print(sent1)
        print(sent2)
        if mode == 1:
            vec1 = self.vectorizer().transform([sent1]).toarray()[0]
            vec2 = self.vectorizer().transform([sent2]).toarray()[0]
            print(cosine(vec1,vec2))
            return cosine(vec1,vec2) < trheshold
        else:
            cv = TfidfVectorizer(tokenizer=lambda s: s.split())
            corpus = [sent1, sent2]
            vectors = cv.fit_transform(corpus).toarray()
            dis = cosine(vectors[0], vectors[1])
            return dis < trheshold

    def extract_from_long_sentence(self,line,core_sentence,is_similar) :
        '''
        获取说话内容比较长的，跨过多个句号
        '''
        if not is_similar:
            return self.extract_from_sentence(line)
        else:
            dist =  self.get_two_sentence_distent(line,core_sentence)
            if not dist:
                return self.extract_from_sentence(line)
            else:
                return (True,None,None,line)


    def analysis_article(self,document):
        """
        没有提取到观点，pass
        提取到观点，判断下语句是不是观点
        """
        sents = SentenceSplitter.split(document)
        sents_list = list(sents)
        is_similar = False
        core_sentence = ""
        extract_list = []
        for i in range(0, len(sents_list)):
            line = sents_list[i]

            is_similar, word_S, word_V, word_sents = self.extract_from_long_sentence(line, core_sentence, is_similar)
            if is_similar:
                if word_S:
                    core_sentence = word_sents
                    extract_list.append([word_S, word_V, word_sents])
                else:
                    extract_list.append(["", "", word_sents])
        return extract_list


    # def vector_similarity(self,s1, s2):
    #     def sentence_vector(s):
    #         words = jieba.lcut(s)
    #         v = np.zeros(64)
    #         for word in words:
    #             v += model[word]
    #         v /= len(words)
    #         return v
    #
    #     v1, v2 = sentence_vector(s1), sentence_vector(s2)
    #     return np.dot(v1, v2) / (norm(v1) * norm(v2))

    def vectorizer(self):
        if hasattr(self,'_vectorizer') and self._vectorizer is not None:
            return self._vectorizer
        stop_words_file = os.path.abspath('./coach/stop_words.txt')
        stop_words_file_list = []
        with open(stop_words_file, 'r') as f:
            line = f.readline()
            while (line):
                line = line.strip()
                if line:
                    stop_words_file_list.append(line)
                line = f.readline()
        self._vectorizer = TfidfVectorizer(stop_words=stop_words_file_list, smooth_idf=True)
        content = []
        # 读取所有的新闻
        with open('./data/news_data.txt', 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                if line.strip():
                    content += [line.strip()]
                line = f.readline()
        crops_vect = self._vectorizer.fit_transform(content)
        return self._vectorizer




