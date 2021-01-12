import sys
import requests
import numpy as np
import pandas as pd
import json
import datetime
import time
import copy

argvs_list = str(sys.argv)


def toTimeZone(dt, fromName, toName, strftime=''):
    #沒管 夏令 冬令
    #---Input---
    if type(dt) is list:
        dt_UTC = copy.deepcopy(dt)  #ini dt_UTC #值不重要 ini大小而已
        for i in range(0, len(dt)):
            if (fromName == 'EST'):
                dt_UTC[i] = dt[i] + datetime.timedelta(hours=+4)
            elif (fromName == 'TST'):
                dt_UTC[i] = dt[i] + datetime.timedelta(hours=-8)
            elif (fromName == 'UTC'):
                dt_UTC[i] = dt[i]
            elif (fromName == 'epoch'):
                #dt_UTC = time.gmtime(dt)#time_struct
                dt_UTC[i] = datetime.datetime.fromtimestamp(int(dt[i]))
    else:
        if (fromName == 'EST'):
            dt_UTC = dt + datetime.timedelta(hours=+4)
        elif (fromName == 'TST'):
            dt_UTC = dt + datetime.timedelta(hours=-8)
        elif (fromName == 'UTC'):
            dt_UTC = dt
        elif (fromName == 'epoch'):
            #dt_UTC = time.gmtime(dt)#time_struct
            dt_UTC = datetime.datetime.fromtimestamp(int(dt))

    #---Output---
    if type(dt_UTC) is list:
        outDt = copy.deepcopy(dt_UTC)  #ini outDt #值不重要 ini大小而已
        for i in range(0, len(dt_UTC)):
            if (toName == 'EST'):
                outDt[i] = dt_UTC[i] + datetime.timedelta(hours=-4)
            elif (toName == 'TST'):
                outDt[i] = dt_UTC[i] + datetime.timedelta(hours=+8)
                if strftime != '':
                    outDt[i] = outDt[i].strftime(strftime)
            elif (toName == 'UTC'):
                outDt = dt_UTC
            elif (toName == 'epoch'):
                eSec[i] = int(time.mktime(dt_UTC[i].timetuple()))
                outDt = eSec
        return outDt
    else:
        if (toName == 'EST'):
            outDt = dt_UTC + datetime.timedelta(hours=-4)
            return outDt
        elif (toName == 'TST'):
            outDt = dt_UTC + datetime.timedelta(hours=+8)
            if strftime != '':
                outDt = outDt.strftime(strftime)
            return outDt
        elif (toName == 'UTC'):
            return dt_UTC
        elif (toName == 'epoch'):
            eSec = time.mktime(dt_UTC.timetuple())
            return int(eSec)

    return


def dayDiff(str1, str2):
    try:
        dt1 = datetime.datetime.strptime(str1, '%Y-%m-%d')
        dt2 = datetime.datetime.strptime(str2, '%Y-%m-%d')
        delta = dt2 - dt1
        return delta.days + 1
    except:
        print('date error')
        sys.exit()


# Name = input("代號US:")
# fromDate = input("起始日期:")
# toDate = input("結束日期:")

Name = 'U'
fromDate = '2021-1-5'
toDate = '2021-1-8'

print(dayDiff(fromDate, toDate))  #有幾天
Ts = toTimeZone(datetime.datetime.strptime(fromDate + ' 01:00', '%Y-%m-%d %H:%M'), 'TST', 'epoch')
Te = toTimeZone(datetime.datetime.strptime(toDate + ' 23:00', '%Y-%m-%d %H:%M'), 'TST', 'epoch')

#每天TST早上6:30有、不知道為什麼TST 13:00有時會有
site = "https://query1.finance.yahoo.com/v8/finance/chart/" + Name + "?period1=" + str(Ts) + "&period2=" + str(Te) + "&interval=1d&events=history&=hP2rOschxO0"

# 利用 requests 來跟遠端 server 索取資料
response = requests.get(site)
print(response.text)

data = json.loads(response.text)
try:
    flag_get = data['chart']['result']
    len(flag_get)
except:
    print('stoke name error')
    sys.exit()

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

timeStamp = toTimeZone(getData_timestamp, 'epoch', 'TST', "%Y-%m-%d")
#columns = [toTimeZone(getData_timestamp, 'epoch', 'TST').strftime("%Y-%m-%d")]
df = pd.DataFrame(np.array([getData_open, getData_high, getData_low, getData_close, getData_volume]), index=['Open', 'High', 'Low', 'Close', 'Volume'], columns=timeStamp)
#單一值
#df = pd.DataFrame(np.array([[getData_open, getData_high, getData_low, getData_close, getData_volume]]), columns=['Open', 'High', 'Low', 'Close', 'Volume'], index=[toTimeZone(int(getData_timestamp), 'epoch', 'TST').strftime("%Y-%m-%d")])

print(df)
df.to_csv(r'file.csv')

print(sys.argv[1])