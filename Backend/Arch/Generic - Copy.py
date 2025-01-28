
from selenium import webdriver
import os
import os.path
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge import service
from fake_useragent import UserAgent
from MarketConfig import CHROME_DRIVER_PATH,LIST_OF_Fund,EDGE,BROWSER,CHROME,FIREFOX
from MarketConfig import Smoothing_91,Smoothing_92,Smoothing_12,Smoothing_21,Smoothing_26
from MarketConfig import Smoothing_50,Smoothing_100,RSI_PERIOD,STRONG_SHORT_VALUE,STRONG_LONG_VALUE
from MarketConfig import STRONG_SHORT,SHORT,STRONG_LONG,LONG,NONE,Fund_FILE_NM,TRADE_CLOSE_LOAD_FILE_NM,TRADE_CLOSE_LOAD_ON
from MarketConfig import MRKT_STRT_TM,MRKT_END_TM,HIST_LOAD_PER
import csv 
import pandas as pd
import statistics
import datetime
from dateutil.relativedelta import relativedelta
import GenericDB as GDB
def getChromeDiver():
   options = webdriver.ChromeOptions()
   options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation']) 
   options.add_argument("start-maximized");
   options.add_argument("disable-infobars")
   options.add_argument("--disable-extensions")
   options.add_argument("--disable-gpu")
   #options.set_capability("browserVersion", "114.0.5735.134")
   prefs = {"credentials_enable_service": False,
      "profile.password_manager_enabled": False}
   options.add_experimental_option("prefs", prefs) 
   from selenium.webdriver.chrome.service import Service
   #driver = webdriver.Chrome(executable_path=r".\chromedriver.exe")
   driver = webdriver.Chrome(CHROME_DRIVER_PATH,options=options)
   return driver

def User():
   ua = UserAgent()
   return ua.random

def getEdgeDriver():
   driver = webdriver.Edge(r"msedgedriver.exe") #Origional
   return driver

def getStartEndDate(Time_Diff): #5Y - 5 year 5M - 5 MONTH   90D- 90 Days
   Cur_Dt = datetime.date.today()
   To_Dt=Cur_Dt.strftime("%I-%b-%Y")
   D_M_Y=Time_Diff[-1]
   No_D_M_Y=int(Time_Diff[:-1])
   if(D_M_Y=='Y'):
      Fr_Dt_Unfrmtd = Cur_Dt - relativedelta(years=No_D_M_Y)
   elif(D_M_Y=='M'):
      Fr_Dt_Unfrmtd = Cur_Dt - relativedelta(months=No_D_M_Y)
   else:
      Fr_Dt_Unfrmtd = Cur_Dt - relativedelta(days=No_D_M_Y)
   Fr_Dt=Fr_Dt_Unfrmtd.strftime("%I-%b-%Y")
   return Fr_Dt,To_Dt

def getDriver():
   if(BROWSER==CHROME):
      driver=getChromeDiver()
   if(BROWSER==EDGE):
      driver=getEdgeDriver()
   return driver


def GetListOfFund():
   list_of_csv=[]
   with open(LIST_OF_Fund, 'r') as read_obj: 
      csv_reader = csv.reader(read_obj) 
      list_of_csv = list(csv_reader) 
   return list_of_csv

def ExtractData(FN,SKIPROW,COLS,SEP):
    Com_Lst=[]
    Com_Lst_Dict=[]
    if(os.path.exists(FN)):
      #df = pd.read_csv(FN, skiprows=[6],header=0,usecols=[0,1,2,4,7], sep=';')  # Replace ';' with your separator
      df = pd.read_csv(FN, skiprows=SKIPROW,header=0,usecols=COLS, sep=SEP)  # Replace ';' with your separator
      df.dropna(inplace=True)
      Com_Lst=df.values.tolist()
      Com_Lst_Dict=df.to_dict(orient='records')
    return Com_Lst,Com_Lst_Dict


def CreateMasterFundList(Fund_Com_Lst):
    Fund_Grp_Lst={}
    Fields=Fund_Com_Lst[0]
    for Fund_Row in Fund_Com_Lst:
        Fund_Sch=Fund_Row[1]
        if Fund_Sch not in Fund_Grp_Lst:
            Fund_Grp_Lst[Fund_Sch]=[]
        Fund_Grp_Lst[Fund_Sch].append(Fund_Row)
    return Fund_Grp_Lst,Fields

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

def AddAnalyticalDataInMasterFundList(Fund_Grp_Lst,Fields):
    LST=['Buy/Sell Recommendation','Price_Lst_Mean','Price_Lst_StdDev2','Price_Lst_Mean_Plus_StdDev2','Price_Lst_Mean_Minus_StdDev2','Price_Lst_GAIN','Price_Lst_LOSS','EMA_9','EMA_12','EMA_21','EMA_26','EMA_50','EMA_100','RSI','MACD']
    Fields.extend(LST)
    for Fund_Sch in Fund_Grp_Lst:
        Price_Lst=[]
        EMA_9=EMA_12=EMA_21=EMA_26=EMA_50=EMA_100=0
        Gain_Lst=Loss_Lst=[]
        for Fund_Row in Fund_Grp_Lst[Fund_Sch][1:]:
            Price_Lst.append(float(Fund_Row[3]))
            Price_Lst_Mean,Price_Lst_StdDev2,Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,Price_Lst_GAIN,Price_Lst_LOSS,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,RSI,MACD=GetAnalyticalData(Price_Lst,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,Gain_Lst,Loss_Lst)
            Gain_Lst.append(Price_Lst_GAIN)
            Loss_Lst.append(Price_Lst_LOSS)
            BuySellRecommend=CalBuySellRecommend(float(Fund_Row[3]),Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,RSI)
            LST=[BuySellRecommend,Price_Lst_Mean,Price_Lst_StdDev2,Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,Price_Lst_GAIN,Price_Lst_LOSS,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,RSI,MACD]
            Fund_Row.extend(LST)
    return Fund_Grp_Lst,Fields

def RetOneList(Fund_Ind_Row):
   FundDescSub={}
   FundRow={}
   FundDescSub['ISIN']=Fund_Ind_Row[2]
   FundDescSub['SchemeCode']=Fund_Ind_Row[0]
   FundDescSub['FundName']=Fund_Ind_Row[1]
   FundDescSub['UpdDate']=GetCurDate("%Y-%m-%d")
   FundRow['ISIN']=Fund_Ind_Row[2]
   FundRow['FundPrice']=Fund_Ind_Row[3]
   FundRow['FundPriceAsOnDate']=Fund_Ind_Row[4]
   FundRow['BuySellRecommend']=Fund_Ind_Row[5]
   FundRow['Price_Lst_Mean']=Fund_Ind_Row[6]
   FundRow['Price_Lst_StdDev2']=Fund_Ind_Row[7]
   FundRow['Price_Lst_Mean_Plus_StdDev2']=Fund_Ind_Row[8]
   FundRow['Price_Lst_Mean_Minus_StdDev2']=Fund_Ind_Row[9]
   FundRow['Price_Lst_GAIN']=Fund_Ind_Row[10]
   FundRow['Price_Lst_LOSS']=Fund_Ind_Row[11]
   FundRow['RSI']=Fund_Ind_Row[18]
   FundRow['MACD']=Fund_Ind_Row[19]
   FundRow['UpdDate']=datetime.datetime.now
   return FundDescSub,FundRow

def LoadOneFund(Fund_Sub):
    Fund_Com_Lst,Fund_Com_LstDict=ExtractData(Fund_FILE_NM,[5],[0,1,2,4,7],';')
    Fund_Grp_Lst,Fields=CreateMasterFundList(Fund_Com_Lst)
    Fund_Com_Lst,Fields=AddAnalyticalDataInMasterFundList(Fund_Grp_Lst,Fields)
    FundCompList=[]
    FundDesc=[]
    Fund_Sub = list(filter(None, Fund_Sub))
    for Fund_Sub_str in Fund_Sub:
        for Fund_Ind_Row in Fund_Com_Lst[Fund_Sub_str]:
            print(Fund_Ind_Row)
            FundDescSub,FundRow=RetOneList(Fund_Ind_Row)
            FundDesc.append(FundDescSub)
            FundCompList.append(FundRow)
    return FundDesc,FundCompList

def RemoveFile(FileNm):
   if(os.path.exists(FileNm)):
      os.remove(FileNm)


def LoadTradeClosedDate():
   Cur_Dt = datetime.date.today()
   Year=Cur_Dt.strftime("%Y")
   To_Dt=Cur_Dt.strftime("%d-%m")
   if(To_Dt==TRADE_CLOSE_LOAD_ON):
      HolList,HolListDict=ExtractData(TRADE_CLOSE_LOAD_FILE_NM,None,[0,1,2,3],",")
      GDB.BulkInsertTradeClosedDate(HolListDict,Year)
      RemoveFile(TRADE_CLOSE_LOAD_FILE_NM)

def GetCurDate(frmt):
   Cur_Dt = datetime.date.today()
   Cur_Dt_Formatted=Cur_Dt.strftime(frmt)
   return Cur_Dt_Formatted,Cur_Dt

def IsLoadHistorCur():
   Cur_Dt_Formatted,Cur_Dt=GetCurDate("%Y-%m-%d")
   Day=Cur_Dt.strftime("%a")
   WEEKEND=['Sat,Sun']
   IsMarketClosedToday=GDB.IsTodayTradeClosed(Cur_Dt_Formatted)
   IsWeekEnd=False
   if(Day in WEEKEND):
       IsWeekEnd=True
   MrktStrtLst=MRKT_STRT_TM.split(":")
   MrktEndLst=MRKT_END_TM.split(":")
   HistLoadStrtInMin=int(MrktEndLst[0])*60+int(MrktEndLst[1])
   MarStrInMin=int(MrktEndLst[0])*60+int(MrktEndLst[1])
   HistLoadEndInMin=(int(MrktStrtLst[0])-HIST_LOAD_PER)*60+int(MrktStrtLst[1])
   Cur_Dt = datetime.datetime.now()
   Hr=int(Cur_Dt.strftime("%H"))
   Mn=int(Cur_Dt.strftime("%M"))
   Tot_Min=Hr*60+Mn
   IsWithinHistLoadWin=False
   if((Tot_Min>HistLoadStrtInMin) or (Tot_Min<HistLoadEndInMin)):
       IsWithinHistLoadWin=True
   IsLoadHis=IsMarketClosedToday or IsWeekEnd or IsWithinHistLoadWin
   IsUpdToday=GDB.IsFundUpdatedToday(Cur_Dt_Formatted)
   IsLoadCur= (not IsMarketClosedToday) and (not IsWeekEnd) and (not IsUpdToday) and (Tot_Min>MarStrInMin) 
   return IsLoadHis,IsLoadCur

       




