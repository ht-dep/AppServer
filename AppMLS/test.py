from flask import Flask
import requests
from pyquery import PyQuery as pq
import json
app = Flask(__name__)



def test():
    try:
        url="http://api.juheapi.com/japi/toh?key={}&v=1.0&month=11&day=1".format("de956536b8eb67357f77919c3de2f8db")
        res=requests.get(url)
        print(res.json())
    except Exception as e:
        print(e)



def testGetNews():
    try:
        news = []
        baseurl = "http://www.yidianzixun.com"
        url = "http://www.yidianzixun.com/home?page=channel&id=hot"
        res = requests.get(url=url)
        html = res.text
        doc = pq(html)
        listP = doc(".main")(".section-articles")("h3")("a")
        # print(listP)
        for i in listP:
            new = {}
            obj = pq(i)
            # print(obj)
            new["title"] = obj.text()
            new["url"] = baseurl + obj.attr("href")
            # print(new)
            news.append(new)
        # print(news)

        return news
    except Exception as e:
        return '请求失败'

@app.route('/')
def hello_world():
    return 'Hello flask!'
@app.route('/test/')
def hello_test():
    return 'Hello test!'

@app.route('/new/')
def get_new():
    try:
    # return testGetNews()
        data= testGetNews()

        return json.dumps(data)
    except Exception as e:
        return "error :+{}".format(e)


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8001, debug=True)
    test()