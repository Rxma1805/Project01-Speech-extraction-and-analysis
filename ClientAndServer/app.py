from flask import Flask, render_template, request, jsonify
import random
# import newsdbs as ndb
#
# news = ndb.getnews()

app = Flask(__name__)



@app.route('/')
def index():
    """
    :return: 调用指定html模板渲染网页
    """
    choice = "choice"
    # choice = random.choice(news)
    return render_template('index.html', myvalue=choice)


@app.route('/database', methods=['POST'])
def database():
    """
    选择随机新闻
    :return: 载入随即新闻数据的模板重定向
    """
    newName = random.randint(0,100)
    return render_template('index.html', myvalue=newName)




@app.route('/process', methods=['POST'])
def process():
    """
    用于提交数据的post请求
    url = /process用于对应的请求包
    request.form用于调用请求包中的数据json文件里对应key的数据
    :return:json格式文件传到请求包的data里
    """
    name = request.form['name']
    print(name)
    if name:
        #调用模型层
        # response = NLP_module(name)
        # return jsonify({"response": response})
        newName = name[::-1]

        return jsonify({"name": newName})

    return jsonify({"error": "Missing data!"})


if __name__ == '__main__':
    app.run(debug=True)


