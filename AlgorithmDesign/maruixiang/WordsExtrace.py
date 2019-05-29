import jieba
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from gensim.models.word2vec import LineSentence
# from gensim.test import utils
from gensim.test.utils import get_tmpfile
import pandas as pd
import chardet
import os
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)

class Word2MyVector:
    '''
    处理中文词到词向量的映射
    '''

    def __init__(self,base_path):
        '''
        缓存两个文件
        一个模型训练文件
        一个词向量文件
        :param base_path: 缓存路径
        '''
        self.model_path = base_path+"/word2vec.model"
        self.kv_path = base_path+'/model.kv'


    def generate_wordvector(self,file_path,is_train=True):
        '''
        加载或者重新训练词向量
        :contexts
        :param is_train: 是否重新训练
        :return: 返回Word2Vec
        '''
        if not is_train:
            return Word2Vec.load(self.model_path)
        else:
            path = get_tmpfile(self.model_path)
            print(file_path)
            sentences = LineSentence(file_path)
            for r in sentences:
                print(r)
                break
            model = Word2Vec(sentences, size=100, window=5, min_count=1, workers=4)
            model.save(path)
            model.wv.save(get_tmpfile(self.kv_path))
            return  model

    def continue_train_wordvector(self,filepath,is_saver = True,is_train=True):
        '''
        继续训练词向量，增量训练
        :param context: filepath
        :param is_saver: 是否保存结果
        :is_train  是否重新训练
        :return:
        '''
        if not is_train:
            return Word2Vec.load(self.model_path)
        with open(filepath, 'r',encoding='utf8') as f:
            model = Word2Vec.load(self.model_path)
            model.train(LineSentence(filepath), total_examples=model.corpus_count, epochs=model.iter)
            if is_saver:
                path = get_tmpfile(self.model_path)
                model.save(path)
                model.wv.save(get_tmpfile(self.kv_path))
            return model

    #读取训练好的词向量
    def Read_coach_KeyedVectors(self):
        '''
        读取训练好的词向量
        :return: KeyedVectors
        '''
        return KeyedVectors.load(self.kv_path, mmap='r')

def rows_news_handle(x,f):
    for line in str(x).split('\n'):
        l = line.strip()
        if l:
            f.writelines(' '.join(jieba.cut(l))+'\n')

def create_news_crops(file_name,output_data_path,is_force=False):
    if not os.path.exists(output_data_path) or is_force:
        #获取编码格式
        with open(file_name,'rb') as f:
            encoding = chardet.detect(f.readline())
        print(encoding)

        df = pd.read_csv(file_name,encoding=encoding['encoding'],error_bad_lines=False,header=None,dtype='str')
        #contents = df.iloc[:,3].values.tolist()
        # 创建要训练的语料库的
        with open(output_data_path,'w',encoding='utf8') as f:
            df.iloc[:, 3].apply(lambda x:rows_news_handle(x,f))

def create_wikis_crops(file_name,output_data_path,is_force=False):
    if not os.path.exists(output_data_path) or is_force:
        with open(file_name, 'rb') as f:
            encoding = chardet.detect(f.read())
        print(encoding)
        with open(file_name, 'r',encoding=encoding['encoding'],errors='ignore') as f:
            with(open(output_data_path,'w',encoding='utf8')) as fo:
                line = f.readline()
                while line:
                    line=line.strip()
                    if line:
                        fo.writelines(' '.join(jieba.cut(line))+'\n')
                    line = f.readline()

def bfs_get_word(model,word,topn,deepth):
    pathes = [[word]]
    result = [word]
    seen=set()
    while pathes:
        path = pathes.pop(0)
        if len(path) > deepth:
            return sorted(set(result),key=lambda x:model.distance(word,x))
        fronter = path[-1]
        if fronter in seen:
            continue
        tmp_list = []
        for s in  model.most_similar(fronter,topn=topn):
            if s[0] in path:
                continue
            new_path = path + [s[0]]
            tmp_list += [s[0]]
            pathes.append(new_path)
        result += tmp_list
        # result = sorted(result, key=lambda x: model.distance(word, x))
        seen.add(fronter[0])

def get_word_by_distence(file_name,word,is_force=False):
    wv = word2vector.Read_coach_KeyedVectors()
    if not os.path.exists(file_name) or is_force:
        with open(file_name, 'w', encoding='utf8') as f:
            context = bfs_get_word(wv, word, 10, 7)
            print(context)
            f.writelines('\n'.join(context))
        return  file_name
    else:
        return file_name


if __name__ == "__main__":
    base_path=os.path.abspath('./coach')
    file_name = os.path.abspath("""../data/news_chinese_sqlResult_1558435.csv""")
    news_data = os.path.abspath('../data/news_data.txt')
    wiki_news = os.path.abspath('../data/wiki_chs')
    wiki_news_data = os.path.abspath('../data/wiki_chs.txt')
    get_word_find_path = os.path.abspath('../data/get_word.txt')

    print('prepare news crops')
    create_news_crops(file_name,news_data,is_force=False)
    word2vector = Word2MyVector(base_path)
    print('train news crops  vector')
    word2vector.generate_wordvector(news_data,is_train=True)
    print('prepare wiki_news crops')
    create_wikis_crops(wiki_news,wiki_news_data,is_force=False)
    print('train wiki_news crops vector')
    word2vector.continue_train_wordvector(wiki_news_data,is_saver=True,is_train=True)

    print('get {} by distence'.format('说'))

    get_word_by_distence(get_word_find_path,'说',False)


