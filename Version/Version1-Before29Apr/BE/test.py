import csv
import pandas as pd
import statistics
import yfinance as yf
from datetime import datetime, timedelta
import GenericDB as GDB
from googletrans import Translator
import googletrans
from langdetect import detect   
# Python program to translate
# speech to text and text to speech

import cv2
import pytesseract
from PIL import Image

import requests
import time

def get_ticker_from_isin(isin):
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    params = {'q': isin, 'quotesCount': 1, 'newsCount': 0}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 429:
            print("Rate limit hit. Waiting before retrying...")
            time.sleep(10)  # wait and retry
            return get_ticker_from_isin(isin)
        response.raise_for_status()
        data = response.json()
        if data.get('count', 0) > 0:
            return data['quotes'][0].get('symbol')
        else:
            return None
    except Exception as e:
        print(f"Failed for ISIN {isin}: {e}")
        return None

isin_list = ["INF192K01CE3", "INF090I01JS8", "INF174K01KW6"]  # Replace with your list
for isin in isin_list:
    ticker = get_ticker_from_isin(isin)
    print(f"{isin}: {ticker}")
    time.sleep(2)  # delay to avoid getting blocked

a=0
print(a:=a+1)
print(a:=a+1)

"""
# Set Tesseract path (Windows only, comment if on Linux/Mac)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    # Read image using OpenCV
    img = cv2.imread(image_path)
    
    # Convert to grayscale (improves OCR accuracy)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding (optional, for better contrast)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Use Tesseract to extract text
    text = pytesseract.image_to_string(thresh)
    
    return text.strip()

# Example usage
image_path = "Words.jpg"  # Replace with your image path
extracted_text = extract_text_from_image(image_path)
print("Extracted Text:")
print(extracted_text)




def detect_language(text):
    # Detect the language of the input text
    language = detect(text)
    return language


import speech_recognition as sr
import pyttsx3 

# Initialize the recognizer 
r = sr.Recognizer() 

# Function to convert text to
# speech
def SpeakText(command):
    
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()
    
    
# Loop infinitely for user to
# speak

while(1):    
    
    # Exception handling to handle
    # exceptions at the runtime
    try:
        
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level 
            print("Listening...")
            r.adjust_for_ambient_noise(source2, duration=0.2)
            
            #listens for the user's input 
            audio2 = r.listen(source2)
            # Using google to recognize audio
            Lang=googletrans.LANGUAGES.keys()
            print(Lang)
            lang=['hi','fr','af','bg','zh-tw','de','it','ja','ko','ru','es']
            for L in Lang:
                try:
                    result = r.recognize_google(audio2, language=L.upper(), show_all=True)
                    language = detect(result['alternative'][0]['transcript'])  
                    if(language == 'unknown'):
                        continue
                    else:
                        MyText =result['alternative'][0]['transcript']
                        MyText = MyText.lower()  
                        print(f"Detected language: {language}")
                        break
                except:
                    continue
            if(language == 'unknown'):
                print("Language not detected")
            else:
                translator = Translator()
                translated = translator.translate(MyText, src= language, dest='en')
                #print("Did you say ",translation)
                SpeakText(translated.text)
            
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        
    except sr.UnknownValueError:
        print("unknown error occurred")




import numpy as np
import pandas as pd
WEEKLY='W'
DAILY='D'   
MONTHLY='M'
MIXED='X'   #Mixed
CANDLE=WEEKLY #D-Daily W-Weekly M-Monthly
from pandas.tseries.offsets import BMonthEnd    


def rma(dataframe: pd.DataFrame, length: int = 14):
    alpha = 1.0 / length
    series = dataframe['Close']
    for i in range(1, series.size):
        #if not pd.isna(series[i - 1]):
        series[i] = (series[i] * alpha) + (1 - alpha) * (series[i - 1])  
        #else: 
        #    series.iloc[i]=(series[i]/length)
    return series

#tradingview ta.sma function

def sma(dataframe: pd.DataFrame, length: int = 14):
    series = dataframe['Close']
    sum=0
    for i in range(1, series.size):
        sum = sum+(series.iloc[i]/length) 
    return sum  


#tradingview ta.rsi function
def rsi_tradingview(ohlc: pd.DataFrame, period: int = 14, round_rsi: bool = False):
    delta =ohlc['Close'].diff()
    delta=delta.fillna(0)
    
    up = delta.copy()
    up[up < 0] = 0
    up1=pd.DataFrame(up)
    up2=pd.Series(rma(up1,14))
    down = delta.copy()
    down[down > 0] = 0
    down *= -1
    down1=pd.DataFrame(down)
    down2=pd.Series(rma(down1,14))

    rsi = np.where(up2 == 0, 0, np.where(down2 == 0, 100, 100 - (100 / (1 + (up2 / down2)))))
    return np.round(rsi, 2) if round_rsi else rsi

def get_last_working_day(dt):
    Dt=BMonthEnd().rollforward(dt)
    while(GDB.IsHoliday('EQ',Dt.strftime("%Y-%m-%d"))>0):
        Dt = Dt - timedelta(days=1)
    return Dt

def getDataToLoad(Prv_OpenPrc,Prv_HighPrc,Prv_LowPrc,PrevDt,PrevLoadFlg,OpenPrc,ClosePrc,HighPrc,LowPrc,Dt):
    LoadFlag=False
    Ret_OpenPrc=OpenPrc
    Ret_ClosePrc=ClosePrc
    Ret_HighPrc=HighPrc
    Ret_LowPrc=LowPrc 
    Ret_Dt=Dt
    FirstDt=False
    if(PrevLoadFlg or ((Dt.weekday()==0) and (CANDLE==WEEKLY)) or ((Dt.date().day==1) and (CANDLE==MONTHLY))):
        Ret_OpenPrc=OpenPrc
        Ret_Dt=Dt
        FirstDt=True
    else:
        Ret_Dt=PrevDt
        Ret_OpenPrc=Prv_OpenPrc
    if(CANDLE==DAILY):
        LoadFlag=True
    else:
        if(FirstDt):
            Ret_HighPrc=HighPrc
            Ret_LowPrc=LowPrc
        else:
            if(Prv_HighPrc>HighPrc):
                Ret_HighPrc=Prv_HighPrc
            if((Prv_LowPrc<LowPrc) and (Prv_LowPrc!=0)):
                Ret_LowPrc=Prv_LowPrc 
        if((CANDLE==WEEKLY) and (Dt.weekday()==4)):
            LoadFlag=True
        MonthEndDt=get_last_working_day(Dt)
        if((CANDLE==MONTHLY) and ( MonthEndDt== Dt)):
            LoadFlag=True
    return Ret_OpenPrc,Ret_ClosePrc,Ret_HighPrc,Ret_LowPrc,Ret_Dt,LoadFlag



# Example Usage
date_time = datetime(2023, 12, 18)
Dt1=get_last_working_day(date_time)
print(Dt1.strftime("%Y-%m-%d"))

stock_data = yf.Ticker('TATASTEEL.NS')
# Get historical data (e.g., last 5 years)
historical_data = stock_data.history(period='5Y')
DtLst=historical_data.index.to_list()

OpenPrc=0
ClosePrc=0
HighPrc=0
LowPrc=0
Dt=None
FrstMonPassed=False
FrstDtPassed=False
LoadFlag=False
for idx in historical_data.index:
    if(CANDLE==WEEKLY):
        if(not FrstMonPassed):
            if(idx.weekday()==0):
                FrstMonPassed=True
            else:
                continue
    if(CANDLE==MONTHLY):
        if(not FrstDtPassed):
            if(idx.date().day==1):
                FrstDtPassed=True
            else:
                continue
    
    OpenPrc,ClosePrc,HighPrc,LowPrc,Dt,LoadFlag=getDataToLoad(OpenPrc,HighPrc,LowPrc,Dt,LoadFlag,historical_data.loc[idx,'Open'],historical_data.loc[idx,'Close'],historical_data.loc[idx,'High'],historical_data.loc[idx,'Low'],idx)
    if(LoadFlag):
        print(Dt.date(),ClosePrc,OpenPrc,HighPrc,LowPrc)
    #print(idx.date().strftime("%Y-%m-%d"),historical_data.loc[idx,'RSI'],historical_data.loc[idx,'Close'],historical_data.loc[idx,'Open'],historical_data.loc[idx,'High'],historical_data.loc[idx,'Low'])



def calculate_rsi_derivative(prices, period=14):
    # Calculate price changes
    delta = prices.diff()
    
    # Calculate gains and losses
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    
    # Calculate rolling averages
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    
    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    # Calculate RSI Derivative
    rsi_derivative = rsi.diff()
    
    return rsi, rsi_derivative

# Example usage
data = pd.Series([45, 46, 47, 46, 48, 49, 48, 50, 51, 50, 52, 53, 54, 53, 55])
rsi, rsi_derivative = calculate_rsi_derivative(data)

print("RSI:\n", rsi)
print("\nRSI Derivative:\n", rsi_derivative)


print(isinstance(datetime.datetime.now(), datetime.datetime))
print(isinstance(10, str))
print(datetime.datetime.__format__("2013-1-25", "%d-%b-%Y"))


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
