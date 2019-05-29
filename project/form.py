from flask import Flask, render_template, request, jsonify
import random
from wu.newsdbs import db
from ma.WordExtract import WordExtract
import jieba
import random
from houyu.IdentifyView import sentences_analysis
# news = ndb.getnews()

app = Flask(__name__)


@app.route('/')
def index():
    """
    :return: 调用指定html模板渲染网页
    """
    choice = "新华社华盛顿3月30日新媒体专电（记者支林飞）美国白宫发言人肖恩·斯派塞30日表示，美国总统特朗普期待与中国国家主席习近平举行会晤，以规划一条中美关系向前发展的路线。中美两国30日同时宣布，中美元首将于4月6日至7日在美国佛罗里达州海湖庄园举行会晤。斯派塞当天在白宫例行记者会上说，两位领导人“将就各自的优先工作重点交换意见，并为两国关系规划一条前进路线”。双方还将讨论相互关切的其他重大问题。谈到美方对这次会晤的目标时，斯派塞表示，这次会晤将为特朗普与习近平建立私人关系提供一个机会。"
    # choice = random.choice(news)
    return render_template('index.html', myvalue=choice)


@app.route('/database', methods=['POST'])
def database():
    """
    选择随机新闻
    :return: 载入随即新闻数据的模板重定向
    """

    id = random.randint(0, int(count))
    data = db.get_content(id)[0][0]
    data = data.replace('\\n','')
    return render_template('index.html', myvalue=data)




@app.route('/process', methods=['POST'])
def process():
    """
    用于提交数据的post请求
    url = /process用于对应的请求包
    request.form用于调用请求包中的数据json文件里对应key的数据
    :return:json格式文件传到请求包的data里
    """
    content = request.form['name']

    if content:
        # content = ' '.join(jieba.cut(content))
        # extract_instance.analysis_article(content)
        # print(content)

        result = sentences_analysis(content)
        if result == (None,None,None):
            result="Empty"
        else:
            result = str(result['人物'])+' '+str(result['动作'])+' '+str(result['观点'])
        return jsonify({"name": result})

    return jsonify({"error": "Missing data!"})

@app.route('/process2', methods=['POST'])
def process2():
    """
    用于提交数据的post请求
    url = /process用于对应的请求包
    request.form用于调用请求包中的数据json文件里对应key的数据
    :return:json格式文件传到请求包的data里
    """
    content = request.form['name']

    if content:
        content = ' '.join(jieba.cut(content))
        result = extract_instance.analysis_article(content)
        print(content)
        print(result)
        print(combine_word_token(result))
        if result :
            result = combine_word_token(result)
        else:
            result="Empty"

        return jsonify({"name": result})

    return jsonify({"error": "Missing data!"})

def combine_word_token(content):
    s=''
    for person,verb,information in content:
        if person:
            if s != '':
                s+='<br/>'
            s+=person+' '+verb+' '+information
        else:
            s+=information
    return s


if __name__ == '__main__':
    extract_instance = WordExtract()
    db = db()
    db.connect()
    count = db.get_counts()
    app.run(debug=True,host='0.0.0.0',port=9090,passthrough_errors=True)


