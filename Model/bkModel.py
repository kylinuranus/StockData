

class BKModel :
      
     ##板块名字
     bkName = ""
     #板块id
     bkId = ""
     #涨幅
     increase = ""
     ##换手率
     turnoverRate = ""
     ##龙头
     bestStockName = ""
     ##龙头id
     bestStockId = ""
     ##上涨家数
     increaseStocksCount = ""
     ##下跌家数
     declineStocksCount = ""

     
     def __init__(self) -> None:
          pass

     def fromJson(self,json):
          self.bkName = json["f14"]
          self.bkId = json["f12"]
          self.increase = json["f3"]
          self.turnoverRate = json["f8"]
          self.bestStockName = json["f128"]
          self.bestStockId = json["f140"]
          self.increaseStocksCount = json["f104"]
          self.declineStocksCount = json["f105"]
          




