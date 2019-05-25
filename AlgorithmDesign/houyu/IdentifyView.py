#-*- coding:utf-8 -*-
import pandas as pd
import re
import jieba
import numpy as np
from pyltp import SentenceSplitter
from common_func import get_words_list, get_postag_list, get_ner_list, get_parser_list
from common_func import load_model,token,cut


# from LoadModel import load_model
import jieba

def load(file_path, column_name = "content"):

    df = pd.read_csv(file_path, encoding='gb18030')
    df = df.fillna('')
    news_content = df[column_name].tolist()
    return news_content

def token(string):
    return re.findall(r'[\d|\w]+', string)

def get_say_list(file_path):

    say_list = []
    with open(file_path) as f:
        line = f.readline()
        while line:
            line = line.strip()
            say_list.append(line)
            line = f.readline()
    return say_list

say_list = get_say_list("say.txt")
# print(say_list)

def get_sentences(content_sentences):

    sentences_list = list(SentenceSplitter.split(content_sentences))
    
    # delete empty member in list
    sentences_list = [item.strip() for item in sentences_list if item]

    return sentences_list

def handle_token_str(token_string):
    string = ''
    if type(token_string) == list:
        for str_item in token_string:
            string += str_item
    else:
        string = token_string
    return string

def sbv_list(say_list, words_list, parse_list):

    # return say word index and subject index 
    ix_list = []
    parser_ix = 0
    for item in parse_list:
        ix, relation = item

        if relation == "SBV":
            word = words_list[ix - 1]
            print(word)
            if word in say_list:
                say_ix = ix - 1
                ix_list.append((parser_ix, say_ix))
        parser_ix += 1
    return ix_list

def get_view(no_say_words, is_quotation):
    view = ""
    print(no_say_words)
    if no_say_words.count("“") != 0 and \
        no_say_words.count("”") != 0:
        left_ix = no_say_words.index("“")
        right_ix = no_say_words.index("”")
        view_words = no_say_words[left_ix + 1: right_ix]
        view = "".join(view_words)
        is_quotation = True
    else:
        view = "".join(no_say_words)
        is_quotation = False
    print(view)
    # return ''.join(token(view))
    return view

def get_sentence_view(string, say_list):
    
    # string = token(string)
    string = handle_token_str(string)
    # print(string)
    words = get_words_list(string)
    postags = get_postag_list(words)
    ner_list = get_ner_list(words, postags)
    parse_list = get_parser_list(words, postags)

    print("words_list is {}".format(words))
    print("postags is {}".format(postags))
    print("ner_list is {}".format(ner_list))
    print("parse_list is {}".format(parse_list))

    say_ix = sbv_list(say_list, words, parse_list)

    result = []
    # print("say_ix is {}".format(say_ix))
    for ix in say_ix:
        subject_ix, say_ix = ix
        before_say_wors = words[:subject_ix]

        before_view = ""
        after_view = ""
        view = ""
        # print(say_ix)
        # print(len(words))

        #obtain view from before_say_words
        if len(words) - say_ix < 3:
            is_quotation = False
            view = get_view(before_say_wors, is_quotation)
            print("say in last: view is {}".format(view))
        else:        
            after_say_words = words[say_ix + 1: ]
            # obtain view from after_say_words
            befoer_quotation = False
            after_quotation = False
            before_view = get_view(before_say_wors, befoer_quotation)
            after_view = get_view(after_say_words, after_quotation)

            # all view from quotation
            if befoer_quotation and after_quotation:
                view = before_view + ' ' + after_view
                print("before and last: view is {}".format(view))
            elif not befoer_quotation and not after_quotation:     
                view = after_view
                print("last1: view is {}".format(view))
            elif not befoer_quotation and after_quotation:
                view = after_view
                print("last2: view is {}".format(view))
            else:
                view = before_view
                print("before: view is {}".format(view))

        person = words[subject_ix]
        say = words[say_ix]
        # obtain person

        print("person: {}, says: {}, view: {}".format(person, say, view))
        result.append((person, say, view))

        # views.append(view)
        # says.append(words[say_ix])
    return result
# news_string = "韩国网友说很喜欢杜甫"
# get_sentence_view(news_string, say_list)
# news_string = "非常喜欢杜甫, 李白说"
# get_sentence_view(news_string, say_list)
# line = "A股早在2013年6月就已纳入新兴市场指数的候选列表中，但此后几年，都因为配额分配、资本流动限制、资本利得税等所谓原因而遭否决，尤其是在2016年第三次闯关失败后，中国投资者和相关监管部门似乎对“A股入摩”已心灰意冷，甚至连证监会分管国际合作的副主席方星海都在今年一月份的时候表示，“中国与MSCI在股指期货上的观点存在分歧，中国并不急于加入MSCI全球指数”。"
# line = 'A股早在2013年6月就已纳入新兴市场指数的候选列表中，但此后几年，都因为配额分配、资本流动限制、资本利得税等所谓原因而遭否决，“中国与MSCI在股指期货上的观点存在分歧，中国并不急于加入MSCI全球指数”,证监会分管国际合作的副主席方星海都在今年一月份的时候表示。'
# line = '中国投资者和相关监管部门似乎对“A股入摩”已心灰意冷，甚至连证监会分管国际合作的副主席方星海都在今年一月份的时候表示，“中国与MSCI在股指期货上的观点存在分歧，中国并不急于加入MSCI全球指数”。'
# line = '唐纳德·唐对Obike的到来说道：“竞争是好事。”他的首批160辆单车6月19日将从中国运达，他的计划是在6个月的时间内向大悉尼地区街道投放6000辆单车。'
# line = "杜甫表示他很细欢李白, 李白说他也很喜欢杜甫"
# line = "在节目中，他对于自己为什么会隐忍不告发也有所解释：“我不能够做这些事情，我不能去害别人。”"
# line = "之后在6月10日凌晨，王杰发布微博说道“我发现自己越来越不能面对钢琴独奏去唱一些老歌了!"
# get_sentence_view(line, say_list)


def sentences_views(news_content, say_list = say_list):

    sentences_list = get_sentences(news_content)

    result_list = []

    for sentence in sentences_list:
        print("sentence:{}".format(sentence))
        result = get_sentence_view(sentence, say_list)
        if result:result_list.append(result)

    return result_list

def vector(string, model):

    res = ''.join(token(string))
    res = (list(jieba.cut(res)))
    return sum([model[item] for item in res]) / len(res)

def consine_dis(x, y):
    print(np.dot(x, y))
    cos_dis = np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))
    print("cos_dis is {}".format(cos_dis))
    return cos_dis * 0.5  + 0.5


sentences = """日前，歌手王杰在某节目中宣布：“这是最后一张唱片，唱完了我就会离开了。”之后在6月10日凌晨，王杰发布微博说道“我发现自己越来越不能面对钢琴独奏去唱一些老歌了!因为内心深处会自然而然扬起很多伤感往事!强忍着哽咽!唱的心很痛!”这样的言论被不少网友猜测是他在参与《围炉音乐会》后的感慨。在明晚播出的《围炉音乐会》中，王杰将连唱7首个人经典曲目，如果此次王杰真的退出歌坛，那这很可能将是一代“歌坛传奇”王杰的告别演唱会。
　　王杰《围炉》敞开心扉为13岁时初恋女友献歌现场飙泪
　　明晚，四川卫视《围炉音乐会》将迎来一位重磅嘉宾，他被称为昨日的浪子，今日的巨星，明日的传奇，他就是曾经华语乐坛最具影响力的唱作歌手之一的“歌坛传奇”王杰。节目中，王杰以一身标志性的皮衣、牛仔裤亮相，不仅演唱了《一场游戏一场梦》《忘了你忘了我》《英雄泪》等多首经典曲目，更是大谈自己的音乐历程和人生感悟，其中他还谈到了自己已逝的初恋女友。
　　谈到自己的初恋，王杰动情地说“记得在13岁时，她因为出车祸不在了。之后我每天都幻想着，暑假完了她怎么没回来。下一个暑假过了，她又没回来，其实知道她不在了。我当时真的很崩溃，就突然好想写首歌给她。”于是，就有了节目中他演唱的这首《安妮》。在演唱的过程中，王杰强忍着哽咽数次流泪，尽显浪子柔情的一面。此外，他还透露一个女孩曾约定和自己结婚，但自己在民政局苦苦等5个小时也不见对方踪影，当时内心被伤的很重，令人唏嘘不已。
　　出道30年是终点？《围炉》或将是王杰谢幕之唱
　　从1987年出道，到如今的歌坛传奇，整整30年间王杰可谓是见证了整个华语流行音乐的发展史。谈及这30年的音乐历程，王杰说道：“一转眼30年过去了，这一路上跌跌撞撞，仿佛还是在昨天一样。”他继续说道：“我经历过所有人没有办法经历过的事情，我以前以为自己很成熟，但后来发现自己很幼稚。直到过了这30年，我突然从内到外有一种感觉，我真的成熟了。”
　　众所周知，王杰曾在采访中透露嗓子受到伤害是被人下毒所致。谈到如今沙哑的嗓音，王杰说道：“我其实很清楚，我现在的声音不能再像当初那样。但我现在很喜欢这个声音。”对此，他还讲述了一个故事：“在有一年秋天，我在家里弹钢琴时唱了一首歌，那天声音很沙哑，但当录下来听完后才发现，自己真的很感动，很喜欢这种沙哑的声音。”对于参与这档《围炉音乐会》，王杰说道：“很感谢‘围炉’个音乐舞台，它有一种温暖人心的力量，对我触动很深。”
　　如果正如王杰所说，出完这张唱片后他将正式告别歌坛，那此次《围炉音乐会》将极可能是王杰最后一场个人演唱会，最后一次在节目中开机车、最后一次做“红烧浪子鸡”……想重温王杰的更多经典歌曲，聆听更多王杰背后的音乐故事，体验王杰可能的最后一场演唱会吗？敬请关注，这档由北京银河映画制作，明晚四川卫视20：30分播出的《围炉音乐会》。"""


result_list = sentences_views(sentences)
print(result_list)

g_model = load_model("word2vec.model")
def get_final(result_list):
    if not result_list:
        return (None, None, None)

    init_person, init_say, init_view = result_list[0][0]
    init_vec = vector(init_view, g_model)

    for item in result_list[1:]:
        person, say, view = item[0]
        view_vec = vector(view, g_model)

        cos_dis = consine_dis(init_vec, view_vec)
        print(cos_dis)
        if cos_dis < 0.5:
            init_view += ' ' + view

    return (init_person, init_say, init_view)

print(get_final(result_list))