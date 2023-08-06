import pandas as pd
import datetime
import time
import pytz
import requests
import json

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
}


def string_to_timestamp(st):
    return int(time.mktime(time.strptime(st, "%Y-%m-%d")))


def string_to_timestamp_with_time_zone(date, format="%Y-%m-%d", zone='Asia/Shanghai'):
    """
    按照时区字符串形式日期转换为时间戳 ，默认格式"%Y-%m-%d"
    转换出错默认返回 0
    """
    try:
        time_array = time.strptime(date, format)
        y, m, d, H, M, S = time_array[0:6]
        dt = datetime.datetime(y, m, d, H, M, S)
        tz = pytz.timezone(zone)
        t = tz.localize(dt)
        t = t.astimezone(pytz.utc)
        return int(time.mktime(t.utctimetuple())) - time.timezone
    except:
        return 0

def timestamp_to_date_with_time_zone(ts,zone='Asia/Shanghai'):
    tz = pytz.timezone(zone)
    dt = pytz.datetime.datetime.fromtimestamp(ts, tz)
    return dt.date()


def get_history(asset_class,inst_type,code,start,end,maturity="")-> pd.DataFrame:
    """
    获取历史行情数据
    params：
       asset_class:资产类别 ,choice of  {"FX", "IR", "CM", "EQ"}
       inst_type:交易类别，根据asset_class可选择
                 CM, choice of  {"SPOT", "FUTURE", "OPTION"}
                 EQ, choice of  {"SPOT", "FUTURE", "OPTION"}
                 FX, choice of  {"SPOT", "SWAP", "OPTION"}
                 IR, choice of  {"IBOR", "SWAP", "CCS"}
       code:代码，CM/EQ两种类别的代码与交易所编码一致;FX/IR两种类别的代码根据业界使用惯例自行编制
       start/end: 起止日期，str, 格式为"%Y-%m-%d",eg:"2021-06-01"
       maturity: 交易到期期限，仅针对于FX/IR, choice of {"nD", "nM", "nY"},n为自然数   
    """
    url = "http://123.60.35.67:8080/market/quote/hist"
    payload = {
            "username": "admin",
            "token":"test",
            "asset_class":asset_class,
            "inst_type":inst_type,
            "code":code,
            "maturity":maturity,
            "timestamp_start":str(string_to_timestamp_with_time_zone(start))+"000",
            "timestamp_end":str(string_to_timestamp_with_time_zone(end))+"000"
    }                        
    try:
      r = requests.post(url, params=payload, headers=headers)
      jdata = r.json()['quotes']    
      df = pd.DataFrame(jdata)
      dates = [timestamp_to_date_with_time_zone(int(ts[:-3])) for ts in df['timestamp'].tolist()]
      df['date'] = dates
      df = df.drop_duplicates('date')
      df = df.set_index('date')
      df = df.sort_index()
      if asset_class in {'CM','EQ'}:
         return df[['code','open','high','low','close','volume']]
      else:
         return df[['code','bid','ask','mid','change_abs','change_rel']]
    except:
       try:
         r = requests.post(url, params=payload, headers=headers)
         jdata = r.json()['quotes']    
         df = pd.DataFrame(jdata)
         dates = [timestamp_to_date_with_time_zone(int(ts[:-3])) for ts in df['timestamp'].tolist()]
         df['date'] = dates
         df = df.drop_duplicates('date')
         df = df.set_index('date')
         df = df.sort_index()
         if asset_class in {'CM','EQ'}:
            return df[['code','open','high','low','close','volume']]
         else:
            return df[['code','bid','ask','mid']]
       except Exception as error:
          print(error)



def get_bond_history(code,price_type,start,end)-> pd.DataFrame:
    """
    获取债券历史行情数据
    params：
       code:债券代码
       price_type:报价类型，choice of  {"clean_price", "dirty_price", "yield"}
       start/end: 起止日期，str, 格式为"%Y-%m-%d",eg:"2021-06-01"
    """
    price_type = price_type.lower()
    url = "http://123.60.35.67:8080/market/quote/bondhist"
    payload = {
            "username": "admin",
            "token":"test",
            "code":code,
            "pricetype":price_type,
            "timestamp_start":str(string_to_timestamp_with_time_zone(start))+"000",
            "timestamp_end":str(string_to_timestamp_with_time_zone(end))+"000"
    }                        
    
    try:
      r = requests.post(url, params=payload, headers=headers)
      jdata = r.json()['quotes']    
      df = pd.DataFrame(jdata)
      dates = [timestamp_to_date_with_time_zone(int(ts[:-3])) for ts in df['timestamp'].tolist()]
      df['date'] = dates
      df = df.drop_duplicates('date')
      df = df.set_index('date')
      df = df.sort_index()
      if price_type=="dirty_price":
         return df[['code','open','high','low','close','volume','market']]
      else:
         return df[['code','broker','bid','ask','mid','last','market']]
    except:
       try:
         r = requests.post(url, params=payload, headers=headers)
         jdata = r.json()['quotes']    
         df = pd.DataFrame(jdata)
         dates = [timestamp_to_date_with_time_zone(int(ts[:-3])) for ts in df['timestamp'].tolist()]
         df['date'] = dates
         df = df.drop_duplicates('date')
         df = df.set_index('date')
         df = df.sort_index()
         if price_type=="dirty_price":
            return df[['code','open','high','low','close','volume','market']]
         else:
            return df[['code','broker','bid','ask','mid','last','market']] 
       except Exception as error:
          print(error)



if __name__ == '__main__':
    #df = get_history("CM","OPTION","au2108C360","2021-05-10","2021-05-31")
    #df = get_history("FX","SPOT","USDCNY","2021-05-10","2021-05-31","0D")
        
    df = get_bond_history("sh010107","dirty_price","2021-05-10","2021-06-08")
    print(df)    


