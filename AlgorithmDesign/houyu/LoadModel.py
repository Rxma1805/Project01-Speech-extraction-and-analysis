from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec
from gensim import utils
import itertools
from common_func import load_model
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = load_model("word2vec.model")

def get_words(word, model, deep = 10, topn = 10):
    pathes = [[word]]
    result = [word]
    seen = set()

    while pathes:
        path = pathes.pop(0)
        if len(path) == deep:
            
            return sorted(set(result),key=lambda x:model.wv.distance(word,x))
            # print(pathes)
            # return set(result)           
        frontier = path[-1]

        if frontier in seen:continue
        # print(frontier)
        # print(type(frontier))
        successor_list = model.most_similar(frontier, topn = topn)

        tmp_result = []
        for successor in successor_list:
            simi_word, simi_point = successor

            if simi_word in path: continue

            pathes.append(path + [simi_word])
            tmp_result.append(simi_word)

        result += tmp_result
        # pathes = sorted(pathes, key=lambda x: model.distance(word, x))
        seen.add(frontier)
        # print(pathes)

result = get_words("说", model, 5, 5)
print(result)


print("\n".join(result))
with open("say.txt", "w") as f:
     f.writelines('\n'.join(result))
