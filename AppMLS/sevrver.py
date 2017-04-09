from flask import Flask, render_template
from flask import request

app = Flask(__name__)
from Handler import *
import json



@app.route('/',methods=["POST", "GET"])
def index():
    # return render_template("base.html")
    return "hello app"


@app.route('/getIndex')
def getIndex():
    return render_template("index.html", var="Jinna")



@app.route('/girl/', methods=["POST", "GET"])
def getGirls():
    data = DBGirl().check()
    print("111")
    print(data)
    return json.dumps(data[1:17], ensure_ascii=False)


@app.route('/history/', methods=["POST", "GET"])
def getHistorys():
    data = DBHistory().check()
    print(data)
    return json.dumps(data, ensure_ascii=False)


@app.route('/new/', methods=["POST", "GET"])
def getNews():
    data = Spider().getNew()
    print(data)
    return json.dumps(data, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
