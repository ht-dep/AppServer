#coding=utf-8
from flask import Flask
import requests,json
#from Handler import *
#from pyquery import PyQuery as pq
# import fire
from Handler import *
app = Flask(__name__)

def test():
    try:
        url="http://api.juheapi.com/japi/toh?key={}&v=1.0&month=11&day=1".format("de956536b8eb67357f77919c3de2f8db")
        res=requests.get(url)

        return (json.dumps(res.json()))
    except Exception as e:
        return "error"

@app.route('/',methods=["POST", "GET"])
def index():
    # return render_template("base.html")
    return "hello app"

@app.route('/test/',methods=["POST", "GET"])
def hello_test():
    return test()
#
@app.route('/girl/',methods=["POST", "GET"])
def girls():
    return json.dumps(Spider().getPicGirl(),ensure_ascii=False)

@app.route('/history/',methods=["POST", "GET"])
def historys():
    sp = Spider()
    part1 = sp.getHistoryListPart1()
    part2 = sp.getHistoryListPart2()
    all=part2+part1
    return json.dumps(all,ensure_ascii=False)

@app.route('/new/',methods=["POST", "GET"])
def news():
    sp = Spider()
    news = sp.getNew()

    return json.dumps(news,ensure_ascii=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
