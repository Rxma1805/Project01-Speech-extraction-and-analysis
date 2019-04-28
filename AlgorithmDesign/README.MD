# 项目合作要求，更改后相互通知
##开发环境python3.6

###每个人的任务放在自己得文件夹下
###任务分解成类，写注释，写文档
###供其他人调用
from gensim.test.utils import common_texts, get_tmpfile  
from gensim.models import Word2Vec  

class Demo:  
    def __init__(self):   
        &nbsp;&nbsp;&nbsp;&nbsp;path = get_tmpfile("word2vec.model")  
        &nbsp;&nbsp;&nbsp;&nbsp;model = Word2Vec(common_texts, size=100, window=5, min_count=1, workers=4)  
        &nbsp;&nbsp;&nbsp;&nbsp;model.save("word2vec.model")  


if __name__ == "__main__":  
    pass
    