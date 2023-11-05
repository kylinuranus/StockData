import requests
import json
import re
from Request.zskrequest import request, requestMethod
from Model.bkModel import BKModel
from Model.kModel import kModel
from datetime import datetime
import copy
import numpy as np



# 获取板块列表
def get_bks():
    url = "http://51.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408935281726377999_1682518656546&pn=1&pz=200&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:90+t:2+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222&_=1682518656547"
    data = request(requestMethod.GET, url)
    list = []
    bk_list = data["data"]["diff"]

    for data in bk_list:
        m = {
            "name": data["f14"],
            "id": data["f12"],
            "increase": data["f3"],  # 涨幅
        }
        list.append(m)

    return list


# 获取板块的K线图
def get_bks_data(id):
    params = {
        "cb": "jQuery35102576927838113152_1682946187245",
        "secid": "90." + id,
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": "101",
        "fqt": 1,
        "beg": "0",
        "end": "20500101",
        "smplmt": "755",
        "lmt": "1000000",
        "_": "1682946187249",
    }
    url = "http://59.push2his.eastmoney.com/api/qt/stock/kline/get"
    data = request(requestMethod.GET, url, params=params)
    list_data = data["data"]["klines"]
    arr = get_klines_arr(list_data, 3, 1, 2, 4, 0)
    return {
        "id": data["data"]["code"],
        "name": data["data"]["name"],
        "data": arr,
    }

#根本板块id获取股票
def get_stocks_data(id):
    url = "https://44.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124028442731216575745_1699196853559&pn=1&pz=200&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=^|0^|0^|0^|web&fid=f3&fs=b:"+id+"+f:^!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f45&_=1699196853566"
    data = request(requestMethod.GET, url)
    list_data = []
    for map in data["data"]["diff"]:
        map_data = {
            "id":map["f12"],
            "name":map["f14"]
        }
        list_data.append(map_data)
    return list_data

#格局id获取股票k
def get_stocks_list(id):
    params = {
        "cb": "jQuery35108565598443590172_1699199779925",
        "secid": "0." + id,
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": "101",   
        "fqt": 1,
        "beg": "0",
        "end": "20500101",
        "smplmt": "460",
        "lmt": "1000000",
        "_": "1699199779947",
    }
    url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
    data = request(requestMethod.GET, url, params=params)


def get_klines_arr(klines: list, high: int, open: int, close: int, low: int, date: int):
    arr = []
    for s in klines:
        l = s.split(",")
        date_string = l[date]
        date_format = "%Y-%m-%d"
        date_time_obj = datetime.strptime(date_string, date_format)
        # 获取月份
        month = date_time_obj.month
        week_day = date_time_obj.weekday()
        m = {
            "date": l[date],
            "month": month,
            "week_day": week_day,
            "high": l[high],
            "open": l[open],
            "low": l[low],
            "close": l[close],
        }
        arr.append(m)

    return arr


def get_month_arr(klines: list):
    arr = []
    small_arr = []
    temp_month = 0
    for index, map in enumerate(klines):
        m = map["month"]
        print(m)
        if temp_month == m:
            small_arr.append(map)
        elif temp_month != m or index == (len(klines) - 1):
            copied_list = copy.deepcopy(small_arr)
            arr.append(copied_list)
            small_arr.clear()
            temp_month = m
            small_arr.append(map)

    return arr


def get_week_arr(klines: list):
    arr = []
    small_arr = []
    for index, m in enumerate(klines):
        w = m["week_day"]

        if w == 0:
            small_arr.clear()
            small_arr.append(m)
        elif w == 4 or index == (len(klines) - 1):
            small_arr.append(m)
            copied_list = copy.deepcopy(small_arr)
            arr.append(copied_list)
        else:
            small_arr.append(m)

    return arr


def main():
    # bk = BKModel()
    # print("-----")
    bk_list = get_bks()
    id = bk_list[0]["id"]
    all_stock_list = []
    for map in bk_list:
        id = map["id"]
        k_bk_stocks_list = get_stocks_data(id)
        all_stock_list.append(k_bk_stocks_list)
        
    # all_stock_list_new = list(np.array(all_stock_list,dtype = object).flatten())
    # print(len(all_stock_list_new))    
    #k_bk_lines_map = get_bks_data(id)
    #k_bk_stocks_list = get_stocks_data(id)
    # model = list[0]
    # bkdata = getBksData(id=model.bkId)
    # klines = bkdata['data']["klines"];
    # arr = getKlinsArr(klines)
    # # print(arr)
    # weekArr = getWeekArr(arr)
    # month_arr = getMonthArr(arr)
    # print(month_arr)

    # getBksData()


if __name__ == "__main__":
    main()
