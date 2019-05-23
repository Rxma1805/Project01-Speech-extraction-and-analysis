from flask import Flask, render_template, request, jsonify
import random
import newsdbs as ndb

# news = ndb.getnews()

app = Flask(__name__)


@app.route('/')
def index():
    """
    :return: 调用指定html模板渲染网页
    """
    return render_template('index.html')

# @app.route('/database', methods=['POST'])
# def database():
#     """
#     用random.choice随机抽取一条新闻内容
#     :return: json格式的随机新闻
#     """
#     choice = random.choice(news)
#
#     if choice:
#         return jsonify({"news": choice})
#
#     return jsonify({"error": "database connection failed"})

@app.route('/process', methods=['POST'])
def process():
    """
    用于提交数据的post请求
    url = /process用于对应的请求包
    request.form用于调用请求包中的数据json文件里对应key的数据
    :return:json格式文件传到请求包的data里
    """
    name = request.form['name']

    if name:
        #调用模型层
        # response = NLP_module(name)
        # return jsonify({"response": response})
        newName = name[::-1]

        return jsonify({"name": newName})

    return jsonify({"error": "Missing data!"})


if __name__ == '__main__':
    app.run(debug=True)


