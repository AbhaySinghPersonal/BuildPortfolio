import csv
import pandas as pd
import statistics
import yfinance as yf
import datetime
print(isinstance(datetime.datetime.now(), datetime.datetime))
print(isinstance(10, str))
print(datetime.datetime.__format__("2013-1-25", "%d-%b-%Y"))

"""
def get_latest_nav_by_isin(scheme_code,data):
    for line in data.splitlines():
        if line.startswith(scheme_code):
            fields = line.split(';')
            Lst=[]
            Lst.append(fields[0])
            Lst.append(fields[3])
            Lst.append(fields[1])
            Lst.append(fields[4])
            Lst.append(fields[5])
            return Lst
    return None

import requests
CURR_LINK="https://www.amfiindia.com/spages/NAVAll.txt"
url = CURR_LINK
response = requests.get(url)
if response.status_code == 200:
    data = response.text

nav_data=get_latest_nav_by_isin('147807',data)
if (nav_data):
    print(nav_data)



x="360 ONE Mutual Fund (Formerly Known as IIFL Mutual Fund)"
if ";" in x:
    print("Yes")
else:
    print("No")

# Specify the ticker symbol (use ".NS" for NSE stocks)
ticker = "ACC.NS"  # Replace with the desired stock ticker

# Fetch the data
stock_data = yf.Ticker(ticker)

# Get historical data (e.g., last 5 years)
historical_data = stock_data.history(period="1d")
Prc=historical_data['Close']
Date=Prc.index.to_list()
Cls=Prc.to_list()
for D in Date:
    print(D.date().strftime("%Y-%m-%d"))
print(Cls)

def GetListOfFund(FlNm):
   list_of_csv=[]
   with open(FlNm, 'r') as read_obj: 
      csv_reader = csv.reader(read_obj) 
      list_of_csv = list(csv_reader) 
   return list_of_csv

LIST_OF_Equity='EQ_LIST.csv'
List_Of_FundTmp=GetListOfFund(LIST_OF_Equity)
List_Of_FundTmp.remove(List_Of_FundTmp[0])
List_Of_Fund=[]
for L in List_Of_FundTmp:
   List_Of_Fund.append([L[0],L[1],L[6]])
print(List_Of_Fund)

from datetime import datetime, date

obj1 = datetime.now()
obj2 = date.today()
obj3 = "2023-01-01"

print(isinstance(obj1, datetime))  # True
print(isinstance(obj1, date))      # True (datetime is a subclass of date)
print(isinstance(obj2, datetime))  # False
print(isinstance(obj2, date))      # True
print(isinstance(obj3, datetime))  # False
print(isinstance(obj3, date))      # False


Smoothing_91=3/10
Smoothing_92=5/6
Smoothing_21=5/22
Smoothing_50=5/51
Smoothing_100=5/102
Smoothing_12=5/13
Smoothing_26=5/27
RSI_PERIOD=14
STRONG_SHORT_VALUE=80
STRONG_LONG_VALUE=20
STRONG_SHORT="STRONG SHORT"
SHORT="SHORT"
STRONG_LONG="STRONG_LONG"
LONG="LONG"
NONE="NONE"
print(len('Edelweiss Banking and PSU Debt Fund - Direct Plan - Growth Option'))
import datetime
from dateutil.relativedelta import relativedelta
Cur_Dt = datetime.datetime.strptime('23-Aug-2024', "%d-%b-%Y")

def GetFutOrPastDate(Cur_Dt,Time_Diff,Past=True):
   D_M_Y=Time_Diff[-1]
   No_D_M_Y=int(Time_Diff[:-1])
   if(D_M_Y=='Y'):
      if(Past):
         Fr_Dt_Unfrmtd = Cur_Dt - relativedelta(years=No_D_M_Y)
      else:
         Fr_Dt_Unfrmtd = Cur_Dt + relativedelta(years=No_D_M_Y)
   elif(D_M_Y=='M'):
      if(Past):
         Fr_Dt_Unfrmtd = Cur_Dt - relativedelta(months=No_D_M_Y)
      else:
         Fr_Dt_Unfrmtd = Cur_Dt + relativedelta(months=No_D_M_Y)
   else:
      if(Past):
         Fr_Dt_Unfrmtd = Cur_Dt - relativedelta(days=No_D_M_Y)
      else:
         Fr_Dt_Unfrmtd = Cur_Dt + relativedelta(days=No_D_M_Y)
   Fr_Dt=Fr_Dt_Unfrmtd.strftime("%Y-%m-%d")
   return Fr_Dt

print(GetFutOrPastDate(Cur_Dt,'1Y',Past=False))
import yfinance as yf

def get_latest_price(isin):
    # ISINs need to be mapped to ticker symbols
    isin_to_ticker = {
        "INE090A01021": "TCS.NS",  # Example: TCS (Tata Consultan=cy Services)
        "INE062A01020": "SBIN.NS"  # Example: State Bank of India
    }

    ticker = isin_to_ticker.get(isin)
    if not ticker:
        print(f"No ticker mapping found for ISIN: {isin}")
        return None

    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if not data.empty:
        return data["Close"].iloc[-1]
    return None

# Example: Get latest price for ISIN
isin = "INE090A01021"  # Replace with the desired ISIN
latest_price = get_latest_price(isin)

if latest_price:
    print(f"Latest Price for ISIN {isin}: {latest_price}")
else:
    print("Price data not available.")

t = [[1,2,3], [4,5,6]]
keys = ['a', 'b', 'c']
d=[dict(zip(keys, l)) for l in t ]
print(d)

def ExtractData():
    df = pd.read_csv('MF.csv', skiprows=[6],header=None,usecols=[0,1,2,4,7], sep=';')  # Replace ';' with your separator
    df.dropna(inplace=True)
    MF_Com_Lst=df.values.tolist()
    return MF_Com_Lst

def CreateMasterMFList(MF_Com_Lst):
    MF_Grp_Lst={}
    Fields=MF_Com_Lst[0]
    for MF_Row in MF_Com_Lst:
        MF_Sch=MF_Row[1]
        if MF_Sch not in MF_Grp_Lst:
            MF_Grp_Lst[MF_Sch]=[]
        MF_Grp_Lst[MF_Sch].append(MF_Row)
    return MF_Grp_Lst,Fields

def GetAnalyticalData(Price_Lst,Last_EMA_9,Last_EMA_12,Last_EMA_21,Last_EMA_26,Last_EMA_50,Last_EMA_100,Gain_Lst,Loss_Lst):
    Price_Lst_Len=len(Price_Lst)
    Lst=SecLast=0
 
    Price_Lst_Mean=statistics.mean(Price_Lst)
    Price_Lst_StdDev2=0
    Lst=Price_Lst[-1]
    if(Price_Lst_Len>=2):
        SecLast=Price_Lst[-2]
        Price_Lst_StdDev2=2*statistics.stdev(Price_Lst)
    Price_Lst_Mean_Plus_StdDev2=Price_Lst_Mean+Price_Lst_StdDev2
    Price_Lst_Mean_Minus_StdDev2=Price_Lst_Mean-Price_Lst_StdDev2

    if(Lst>SecLast):
        Price_Lst_GAIN=Lst-SecLast
        Price_Lst_LOSS=0
    else:
        Price_Lst_GAIN=0
        Price_Lst_LOSS=SecLast-Lst
    Gain_Lst.append(Price_Lst_GAIN)
    Loss_Lst.append(Price_Lst_LOSS)
    
    Smoothing_9=(Smoothing_92 if Price_Lst_Len > 2 else Smoothing_91)
    EMA_9=0
    EMA_12=0
    EMA_21=0
    EMA_26=0
    EMA_50=0
    EMA_100=0
    MACD=0
    if(Price_Lst_Len>1):
        EMA_9=Lst* Smoothing_9+Last_EMA_9*(1-Smoothing_9)
        EMA_12=Lst* Smoothing_12+Last_EMA_12*(1-Smoothing_12)
        EMA_21=Lst* Smoothing_21+Last_EMA_21*(1-Smoothing_21)
        EMA_26=Lst* Smoothing_26+Last_EMA_26*(1-Smoothing_26)
        EMA_50=Lst* Smoothing_50+Last_EMA_50*(1-Smoothing_50)
        EMA_100=Lst* Smoothing_100+Last_EMA_100*(1-Smoothing_100)
        MACD=EMA_12-EMA_26
    RSI=0
    Gain_Loss_LEN=len(Gain_Lst)
    if(Gain_Loss_LEN>=RSI_PERIOD):
        Gain_RSI_Lst=Gain_Lst[Gain_Loss_LEN-RSI_PERIOD:]
        Loss_RSI_Lst=Loss_Lst[Gain_Loss_LEN-RSI_PERIOD:]
        RSI=100
        LostMean=statistics.mean(Loss_RSI_Lst)
        if(LostMean>0):
            RSI=100-100/(1+statistics.mean(Gain_RSI_Lst)/LostMean)
    return Price_Lst_Mean,Price_Lst_StdDev2,Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,Price_Lst_GAIN,Price_Lst_LOSS,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,RSI,MACD

def CalBuySellRecommend(Prc,MeanPlusSTDev2,MeanMinusSTDev2,RSI):
    if(Prc>MeanPlusSTDev2):
       if(RSI>STRONG_SHORT_VALUE):
           return STRONG_SHORT
       else:
           return SHORT
    elif(RSI<MeanMinusSTDev2):
       if(RSI<STRONG_LONG_VALUE):
           return STRONG_LONG
       else:
           return LONG     
    else:
        return NONE

def AddAnalyticalDataInMasterMFList(MF_Grp_Lst,Fields):
    LST=['Buy/Sell Recommendation','Price_Lst_Mean','Price_Lst_StdDev2','Price_Lst_Mean_Plus_StdDev2','Price_Lst_Mean_Minus_StdDev2','Price_Lst_GAIN','Price_Lst_LOSS','EMA_9','EMA_12','EMA_21','EMA_26','EMA_50','EMA_100','RSI','MACD']
    Fields.extend(LST)
    for MF_Sch in MF_Grp_Lst:
        Price_Lst=[]
        EMA_9=EMA_12=EMA_21=EMA_26=EMA_50=EMA_100=0
        Gain_Lst=Loss_Lst=[]
        for MF_Row in MF_Grp_Lst[MF_Sch][1:]:
            Price_Lst.append(float(MF_Row[3]))
            Price_Lst_Mean,Price_Lst_StdDev2,Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,Price_Lst_GAIN,Price_Lst_LOSS,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,RSI,MACD=GetAnalyticalData(Price_Lst,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,Gain_Lst,Loss_Lst)
            Gain_Lst.append(Price_Lst_GAIN)
            Loss_Lst.append(Price_Lst_LOSS)
            BuySellRecommend=CalBuySellRecommend(float(MF_Row[3]),Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,RSI)
            LST=[BuySellRecommend,Price_Lst_Mean,Price_Lst_StdDev2,Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,Price_Lst_GAIN,Price_Lst_LOSS,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,RSI,MACD]
            MF_Row.extend(LST)
    return MF_Grp_Lst,Fields

def LoadOneMF(MF_Sub):
    MF_Com_Lst=ExtractData()
    MF_Grp_Lst,Fields=CreateMasterMFList(MF_Com_Lst)
    MF_Com_Lst,Fields=AddAnalyticalDataInMasterMFList(MF_Grp_Lst,Fields)
    print(Fields)
    for MF_Sub_str in MF_Sub:
        for x in MF_Com_Lst[MF_Sub_str]:
            print(x)
        print("\n\n--------------------------------\n\n")
LoadOneMF(['BAJAJ FINSERV LARGE CAP FUND - DIRECT PLAN - GROWTH','Bajaj Finserv Flexi Cap Fund -Regular Plan-Growth'])
"""
