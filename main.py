
import requests
import json
import re
from Request.zskrequest import request,requestMethod
from Model.bkModel import BKModel
from Model.kModel import kModel


##获取板块列表
def getbks():
    
    url = "http://51.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408935281726377999_1682518656546&pn=1&pz=200&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:90+t:2+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222&_=1682518656547"
    data = request(requestMethod.GET,url)
    list = [];
    bklist = data["data"]["diff"];
    for json in bklist:
        model = BKModel()
        model.fromJson(json=json)
        print(model)
        list.append(model)
    return list

##获取板块的K线图
def getBksData(id):
  
    params = {"cb":"jQuery35102576927838113152_1682946187245",
              "secid":"90." + id,
              "ut":"fa5fd1943c7b386f172d6893dbfba10b",
              "fields1":"f1,f2,f3,f4,f5,f6",
              "fields2":"f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
              "klt":"101",
              "fqt":1,
              "beg":"0",
              "end":"20500101",
              "smplmt":"755",
              "lmt":"1000000",
              "_":"1682946187249"}
    url = "http://59.push2his.eastmoney.com/api/qt/stock/kline/get"
    data = request(requestMethod.GET,url,params=params)
    print(data)
    return data

def getKlinsArr(klines:list):

    arr = [];
    for s in klines:
       l = s.split(",")
       m = {"date":l[0],"high":l[1]}
       arr.append(m)
    
    return arr
 
def main():
    # bk = BKModel()  
    # print("-----")
    list = getbks()
    model = list[0]
    bkdata = getBksData(id=model.bkId)
    klines = bkdata['data']["klines"];
    arr = getKlinsArr(klines)
    print(arr)
    
    
    # getBksData()

if __name__=="__main__":
    main()



    