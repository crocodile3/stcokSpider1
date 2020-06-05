
import tushare as ts

from myStockData.config import TOKEN,CURRENT_DATE


class MyTuShare:
    def __init__(self):
        ts.set_token(TOKEN)
        self.pro = ts.pro_api()
        self.trade_days = self.load_trade_days()
        self.stock_list = self.load_stocks_list()

    def load_trade_days(self,start_date='20050101',end_date=CURRENT_DATE):
        df = self.pro.query('trade_cal', start_date=start_date, end_date=end_date)
        dates = df[['cal_date']].values.tolist()
        return dates

    def load_stocks_list(self):
        data = self.pro.stock_basic(exchange='',
                                    list_status='L',
                                    fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,list_status,delist_date,is_hs'
                                    )
        stock_codes = data['ts_code'].values.tolist()
        return stock_codes

    def stock(self):
        """
        股票数据接口
        :return:
        """
        pass

    def funds(self):
        """
        基金数据接口
        :return:
        """
        pass

    def news(self):
        pass

    def foreign_exchange(self):
        pass

    def load_hs_index(self,period='day'):
        pass


if __name__ == '__main__':
    tushare = MyTuShare()
    ls = tushare.stock_list
    print(ls)
