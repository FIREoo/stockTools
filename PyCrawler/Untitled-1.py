import requests
import numpy as np
import pandas as pd
import json
import datetime
import time


def toTimeZone(dt, fromName, toName):
    if type() is list:
        
    #沒管 夏令 冬令
    if (fromName == 'EST'):
        dt_UTC = dt + datetime.timedelta(hours=+4)
    elif (fromName == 'TST'):
        dt_UTC = dt + datetime.timedelta(hours=-8)
    elif (fromName == 'UTC'):
        dt_UTC = dt
    elif (fromName == 'epoch'):
        #dt_UTC = time.gmtime(dt)#time_struct
        dt_UTC = datetime.datetime.fromtimestamp(int(dt))

    if (toName == 'EST'):
        outDt = dt_UTC + datetime.timedelta(hours=-4)
        return outDt
    elif (toName == 'TST'):
        outDt = dt_UTC + datetime.timedelta(hours=+8)
        return outDt
    elif (toName == 'UTC'):
        return dt_UTC
    elif (toName == 'epoch'):
        eSec = time.mktime(dt_UTC.timetuple())
        return int(eSec)
    return


def dayDiff(str1, str2):
    dt1 = datetime.datetime.strptime(str1, '%Y-%m-%d')
    dt2 = datetime.datetime.strptime(str2, '%Y-%m-%d')
    delta = dt2 - dt1
    return delta.days + 1


# nowTime = time.localtime()
# nowDt = datetime.datetime.fromtimestamp(time.mktime(nowTime))
# print('--localtime--')
# print(nowDt.strftime("%Y-%m-%d %H:%M"))  # 將時間轉換為 string
# print(time.mktime(nowDt.timetuple()))

# print('--to UTC--')
# tmp = time.gmtime()
# print(toTimeZone(nowDt,'TST','UTC').strftime("%Y-%m-%d %H:%M"))  # 將時間轉換為 string
# print(time.mktime(nowDt.timetuple()))

# print(toTimeZone(1609857000, 'epoch', 'TST'))

# Name = input("代號US:")
# fromDate = input("起始日期:")
# toDate = input("結束日期:")

Name = 'U'
fromDate = '2021-1-5'
toDate = '2021-1-7'

print(dayDiff(fromDate, toDate))
Ts = toTimeZone(datetime.datetime.strptime(fromDate + ' 01:00', '%Y-%m-%d %H:%M'), 'TST', 'epoch')
Te = toTimeZone(datetime.datetime.strptime(toDate + ' 23:00', '%Y-%m-%d %H:%M'), 'TST', 'epoch')

#每天TST早上6:30有、不知道為什麼TST 13:00有時會有
site = "https://query1.finance.yahoo.com/v8/finance/chart/" + Name + "?period1=" + str(Ts) + "&period2=" + str(Te) + "&interval=1d&events=history&=hP2rOschxO0"

# 利用 requests 來跟遠端 server 索取資料
response = requests.get(site)
print(response.text)

data = json.loads(response.text)
# df = pd.DataFrame(data['chart']['result'][0]['indicators']['quote'][0], index=pd.to_datetime(np.array(data['chart']['result'][0]['timestamp'])*1000*1000*1000))
getData_close = data['chart']['result'][0]['indicators']['quote'][0]['close']
getData_open = data['chart']['result'][0]['indicators']['quote'][0]['open']
getData_low = data['chart']['result'][0]['indicators']['quote'][0]['low']
getData_high = data['chart']['result'][0]['indicators']['quote'][0]['high']
getData_volume = data['chart']['result'][0]['indicators']['quote'][0]['volume']
getData_timestamp = data['chart']['result'][0]['timestamp']

#df = pd.DataFrame(data['chart']['result'][0]['indicators']['quote'][0], index=toTimeZone(data['chart']['result'][0]['timestamp'][0],'epoch','EST'))

#
aaa = type(getData_timestamp)


columns = [toTimeZone(getData_timestamp, 'epoch', 'TST').strftime("%Y-%m-%d")]
df = pd.DataFrame(np.array([getData_open, getData_high, getData_low, getData_close, getData_volume]), index=['Open', 'High', 'Low', 'Close', 'Volume'])
#單一值
#df = pd.DataFrame(np.array([[getData_open, getData_high, getData_low, getData_close, getData_volume]]), columns=['Open', 'High', 'Low', 'Close', 'Volume'], index=[toTimeZone(int(getData_timestamp), 'epoch', 'TST').strftime("%Y-%m-%d")])

print(df)
df.to_csv(r'file.csv')