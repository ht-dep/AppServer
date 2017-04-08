#coding=utf-8
from pymongo import MongoClient
import requests, datetime

#import fire
from bs4 import BeautifulSoup

def getDate():
    now = datetime.datetime.now().strftime("%Y%m%d")
    return now


def getTime():
    now = datetime.datetime.now().strftime("%Y-%m-%d ")
    return now


class DBGirl:
    '''
    存储数据模型,此模型只适合用来存储数据，不适合记录下载图片情形
    {"date":"2017-03-06",
   "list":
       [
            {
             "id":"",
             "title":"",
             "pic":"",
             "time":""},
        ]}
    '''

    def __init__(self):
        self.date = "table" + getDate()
        self.MONGODB_URI = "mongodb://root:QMjuaQhEon5fY5I8J0jw7hoZnQ0dcxHS38PcmhXy@jscyupgexvbn.mongodb.sae.sina.com.cn:10109,colcqebeddww.mongodb.sae.sina.com.cn:10109"
        self.client = MongoClient(self.MONGODB_URI)
        self.db = self.client["girl"]
        self.collection = self.db["tablegirl"]

    def insert(self, record):
        # 数据在外部查询结束后，再插入数据库
        self.collection.insert(record)

    def insert_many(self, recordList):
        self.collection.insert_many(recordList)

    def count(self):
        count = self.collection.count()
        return count

    def tcheck(self):
        # 针对一条记录存储所有数据list
        # 判断数据是否存在，判断key的存在，再判断value的长度
        # self.collection.
        pass

    def query(self):
        try:
            results = self.collection.find_one({"date": getDate()})

            for i in results['list']:
                print(i)
            return results
        except Exception as e:
            print("DBGirl query error:{}".format(e))

    def check(self):
        try:

            record = self.collection.find_one({"date": getDate()})

            if record:
                if 'date' in record.keys():
                    if len(record["list"]) != 0:
                        return record["list"]

            return savePicGirl()  # 插入数据

        except Exception as e:
            print("error:{}".format(e))


class DBHistory:
    '''
    存储数据模型

    一天一个表 table20170306
    {
    "id":"",
    "title":"",
    "pic":""，
    "datetime":""
    }

    '''

    def __init__(self):
        self.date = "table" + getDate()
        self.MONGODB_URI = "mongodb://root:QMjuaQhEon5fY5I8J0jw7hoZnQ0dcxHS38PcmhXy@jscyupgexvbn.mongodb.sae.sina.com.cn:10109,colcqebeddww.mongodb.sae.sina.com.cn:10109 "
        self.client = MongoClient(self.MONGODB_URI)
        self.db = self.client["history"]
        self.collection = self.db[self.date]

    def insert(self, recordList):
        # 数据在外部查询结束后，再插入数据库
        for record in recordList:
            self.collection.insert(record)

    def insert_many(self, recordList):
        self.collection.insert_many(recordList)

    def count(self):
        count = self.collection.count()
        return count

    def tcheck(self):
        # 针对一条记录存储所有数据list
        # 判断数据是否存在，判断key的存在，再判断value的长度
        # self.collection.
        pass

    def query(self):
        results = []
        try:
            records = self.collection.find()
            # 可以再优化
            for r in records:
                res = {}
                res["title"] = r["title"]
                res["pic"] = r["pic"]
                res["url"] = r["url"]
                results.append(res)
            return results
        except Exception as e:
            print("DBHistory query error:{}".format(e))

    def check(self):

        print("start")
        try:
            num = self.collection.find().count()
            print(num)
            if num == 0:
                return saveHistory()
            else:
                return self.query()
        except Exception as e:
            print(e)


class Spider:
    '''
    爬虫操作，
    爬取历史上的今天的数据。part1+part2保存为列表
    遍历列表保存或者通过insertmany
    采用BeautifulSoap


    '''

    def __init__(self):
        self.urlHistory = "http://www.lssdjt.com/"
        self.urlGirl = "http://www.mzitu.com/all"
        self.urlNewHot = "http://www.yidianzixun.com/home?page=channel&id=hot"
        self.urlNew = "http://www.yidianzixun.com"

    def getHistoryListPart1(self):
        res = requests.get(url=self.urlHistory)
        html = res.content.decode("UTF_8")
        # doc = pq(html)
        doc = BeautifulSoup(html)
        listP = doc.select("#slideshow p a[href]")
        # print(listP)
        key = getDate()
        docList = []
        for i in listP:
            cell = {}

            cell["url"] = self.urlHistory + i.attrs["href"]
            cell["pic"] = i.find('img').attrs["src"]
            cell["title"] = i.find('img').attrs["alt"]
            cell["date"] = getDate()
            docList.append(cell)

        return docList

    def getHistoryListPart2(self):
        res = requests.get(url=self.urlHistory)
        html = res.content.decode("UTF_8")
        doc = BeautifulSoup(html)

        # listP = doc(".w730")(".mt5")(".gong")("li")("[href]")

        listP = doc.select(".w730 .gong a[rel]")
        # listP = doc.select(".w730 .mt5 .gong li [href]")
        # print(listP)

        docList = []
        for i in listP:
            # per = pq(i)
            # print(i)
            cell = {}
            cell["url"] =  i.attrs["href"]
            cell["pic"] = i.attrs['rel'][0]
            cell["title"] = i.attrs["title"]
            cell["date"] = getDate()
            docList.append(cell)
        # print(docList)
        return docList
    def getPicGirl(self):
        picList = []
        res = requests.get(url=self.urlGirl)
        html = res.text
        doc = BeautifulSoup(html)

        listP = doc.select(".main .postlist #pins a")

        todayUrl = listP[0].attrs["href"]
        # print(todayUrl)
        res = requests.get(todayUrl)
        htm = res.text
        # print(htm)
        do = BeautifulSoup(htm)
        span = do.select('.pagenavi span')[-2]
        # print(span)
        max_page = int(span.string)
        # print(max_page)
        for i in range(1, max_page):
            url = todayUrl + "/" + str(i)
            h = requests.get(url).text
            d = BeautifulSoup(h)
            obj = d.select(".main-image img")[0]
            # print(obj)
            pic = obj.attrs["src"]
            # print(pic)
            alt = obj.attrs["alt"]
            # print(alt)
            picList.append(pic)

        return picList
    def getGirl(self):
        '''
        {
            'time':'',
            'pic':'',
            'title':'',
            pics=[]
        }
        :return:
        '''
        picList = []
        res = requests.get(url=self.urlGirl)
        html = res.text
        doc = BeautifulSoup(html)

        listLI = doc.select(".main .postlist #pins li")
        # print(listP)
        for i in listLI[0:10]:     #控制数量
            per={}
            s = i.select("span[class='time']")[0]
            # print(s)
            date_img = s.string
            per["time"]=date_img
            # print(date_img)
            a=i.select("a")[0]
            # print(a)
            todayUrl = a.attrs["href"]
            name=a.find('img').attrs["alt"]
            # print(name)
            per["title"]=name
            # print(todayUrl)
            per['pic']=todayUrl
            res = requests.get(todayUrl)
            htm = res.text
            # print(htm)
            do = BeautifulSoup(htm)
            span = do.select('.pagenavi span')[-2]
            # print(span)
            max_page = int(span.string)
            # print(max_page)
            pics=[]
            for j in range(1, max_page):            #控制数量
                url = todayUrl + "/" + str(j)
                h = requests.get(url).text
                d = BeautifulSoup(h)
                obj = d.select(".main-image img")[0]
                # print(obj)
                pic = obj.attrs["src"]
                # print(pic)
                # alt = obj.attrs["alt"]
                # print(alt)
                pics.append(pic)
            per["pics"]=pics
            # print(per)
        # return picList
            picList.append(per)
        # print(picList)
        return picList
    def getNew(self):
        news = []
        res = requests.get(url=self.urlNewHot)
        html = res.text
        soup = BeautifulSoup(html)

        # listP = soup(".main")(".section-articles")("h3")("a")
        # listP = soup.find("div",attrs={"class":"main"}).find("div",attrs={"class":"section-articles"}).find_all("h3")
        listP = soup.select(".main .section-articles h3 a")

        for i in listP:
            new = {}
            new["title"] = i.string
            new["url"] = self.urlNew + i.attrs["href"]
            news.append(new)
        return news



def saveHistory():
    try:
        sp = Spider()
        # 存储历史的今天数据表
        handlerHistory = DBHistory()
        part1 = sp.getHistoryListPart1()
        part2 = sp.getHistoryListPart2()
        allList = part1 + part2
        # print(allList)
        handlerHistory.insert_many(recordList=allList)
        return handlerHistory.query()
    except Exception as e:
        print("保存历史出错：{}".format(e))


def savePicGirl():
    try:
        # 存储美女图数据表
        sp = Spider()
        handlerGirl = DBGirl()
        allList = sp.getPicGirl()
        # print(allList)
        date = getDate()
        data = {"date": date, "list": allList}
        handlerGirl.insert(data)
        return handlerGirl.query()
    except Exception as e:
        print("保存girl图片出错:{}".format(e))


if __name__ == "__main__":
    # pass
    # Spider().getHistoryListPart1()
    Spider().getHistoryListPart2()
    # Spider().getGirl()
    #fire.Fire(Spider)
    # saveHistory()
    # savePicGirl()
    # fire.Fire(DBHistory)
    # fire.Fire(DBGirl)
    # # DBGirl().check()
    # DBGirl().check()
    # DBHistory().check()
