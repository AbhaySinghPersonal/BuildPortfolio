
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
from MarketConfig import MRKT_STRT_TM,MRKT_END_TM,HIST_LOAD_PER,LOAD_HIST_ANYTIME,CAL_FREE_PERIOD
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
   Fr_Dt=Fr_Dt_Unfrmtd.strftime("%I-%b-%Y")
   return Fr_Dt

def getStartEndDate(Time_Diff): #5Y - 5 year 5M - 5 MONTH   90D- 90 Days
   Cur_Dt = datetime.date.today()
   To_Dt=Cur_Dt.strftime("%I-%b-%Y")
   Fr_Dt=GetFutOrPastDate(Cur_Dt,Time_Diff)
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
    print('Extracting Data from '+FN)
    if(os.path.exists(FN)):
      #df = pd.read_csv(FN, skiprows=[6],header=0,usecols=[0,1,2,4,7], sep=';')  # Replace ';' with your separator
      df = pd.read_csv(FN, skiprows=SKIPROW,header=0,usecols=COLS, sep=SEP)  # Replace ';' with your separator
      df.dropna(inplace=True)
      Com_Lst=df.values.tolist()
      Com_Lst_Dict=df.to_dict(orient='records')
    return Com_Lst,Com_Lst_Dict


def CreateMasterFundList(Fund_Com_Lst):
    print('Creating Master Fund List')
    Fund_Grp_Lst={}
    for Fund_Row in Fund_Com_Lst:
        Fund_Sch=Fund_Row[1]
        if Fund_Sch not in Fund_Grp_Lst:
            Fund_Grp_Lst[Fund_Sch]=[]
        Fund_Grp_Lst[Fund_Sch].append(Fund_Row)
    return Fund_Grp_Lst

def UpdGainLossList(Lst,SecLast,Gain_Lst,Loss_Lst):
   if(Lst>SecLast):
      Price_Lst_GAIN=Lst-SecLast
      Price_Lst_LOSS=0
   else:
      Price_Lst_GAIN=0
      Price_Lst_LOSS=SecLast-Lst
   Gain_Lst.append(Price_Lst_GAIN)
   Loss_Lst.append(Price_Lst_LOSS)
   return Gain_Lst,Loss_Lst,Price_Lst_GAIN,Price_Lst_LOSS

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

    Gain_Lst,Loss_Lst,Price_Lst_GAIN,Price_Lst_LOSS=UpdGainLossList(Lst,SecLast,Gain_Lst,Loss_Lst)
    
    Smoothing_9=(Smoothing_92 if Price_Lst_Len > 2 else Smoothing_91)
    EMA_9=0
    EMA_12=0
    EMA_21=0
    EMA_26=0
    EMA_50=0
    EMA_100=0
    MACD=0
    if(Price_Lst_Len>1):
        if(Last_EMA_9==None):
         Last_EMA_9=0
        if(Last_EMA_12==None):
         Last_EMA_12=0
        if(Last_EMA_21==None):
         Last_EMA_21=0
        if(Last_EMA_26==None):
         Last_EMA_26=0
        if(Last_EMA_50==None):
         Last_EMA_50=0
        if(Last_EMA_100==None):
         Last_EMA_100=0
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
    if(RSI==0):
       return NONE
    elif(Prc>MeanPlusSTDev2):
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

def AddAnalyticalDataInMasterFundList(Fund_Grp_Lst):
    idx=0
    LEN1=len(Fund_Grp_Lst)
    Cal_Period={}
    for Fund_Sch in Fund_Grp_Lst:
        idx=idx+1
        Price_Lst=[]
        EMA_9=EMA_12=EMA_21=EMA_26=EMA_50=EMA_100=0
        Gain_Lst=Loss_Lst=[]
        LEN=len(Fund_Grp_Lst[Fund_Sch][0:])
        if(idx%10==0):
         print(str(idx)+' of '+ str(LEN1)+' Creating Analysis Data for '+Fund_Sch+" Analysing "+str(LEN)+" Rows")
        FundLaunchDt=Fund_Grp_Lst[Fund_Sch][0][4]
        DateTillNoCal=GetFutOrPastDate(datetime.datetime.strptime(FundLaunchDt, "%d-%b-%Y"),CAL_FREE_PERIOD,False)
        DateTillNoCalFrmtd=ChangeDtFomat(DateTillNoCal,"%d-%b-%Y","%Y-%m-%d")
        Last_No_Day_Cal=1
        for Fund_Row in Fund_Grp_Lst[Fund_Sch][0:]:
            PrcAsOnDtFrmtd=ChangeDtFomat(Fund_Row[4],"%d-%b-%Y","%Y-%m-%d")
            LST=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
            Price_Lst.append(float(Fund_Row[3]))
            if(PrcAsOnDtFrmtd>=DateTillNoCalFrmtd):
               Price_Lst_Mean,Price_Lst_StdDev2,Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,Price_Lst_GAIN,Price_Lst_LOSS,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,RSI,MACD=GetAnalyticalData(Price_Lst,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,Gain_Lst,Loss_Lst)
               Gain_Lst.append(Price_Lst_GAIN)
               Loss_Lst.append(Price_Lst_LOSS)
               BuySellRecommend=CalBuySellRecommend(float(Fund_Row[3]),Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,RSI)
               LST=[BuySellRecommend,Price_Lst_Mean,Price_Lst_StdDev2,Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,Price_Lst_GAIN,Price_Lst_LOSS,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,RSI,MACD]
               del Price_Lst[0]
            else:
               Last_No_Day_Cal=Last_No_Day_Cal+1
            Fund_Row.extend(LST)
    return Fund_Grp_Lst

def RetOneListDesc(Fund_Ind_Row):
   FundDescSub={}
   ISIN=FundDescSub['ISIN']=Fund_Ind_Row[2]
   FundDescSub['SchemeCode']=Fund_Ind_Row[0]
   FundDescSub['FundName']=Fund_Ind_Row[1]
   FundDescSub['UpdDate']=Fund_Ind_Row[4]
   return FundDescSub,ISIN


def RetOneList(Fund_Ind_Row):
   FundRow={}
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
   FundRow['EMA_9']=Fund_Ind_Row[12]
   FundRow['EMA_12']=Fund_Ind_Row[13]
   FundRow['EMA_21']=Fund_Ind_Row[14]
   FundRow['EMA_26']=Fund_Ind_Row[15]
   FundRow['EMA_50']=Fund_Ind_Row[16]
   FundRow['EMA_100']=Fund_Ind_Row[17]
   FundRow['RSI']=Fund_Ind_Row[18]
   FundRow['MACD']=Fund_Ind_Row[19]
   FundRow['UpdDate']=datetime.datetime.now()
   return FundRow

def LoadOneFund(Fund_Sub,Cur_Dt_Formatted):
    Fund_Com_Lst,Fund_Com_LstDict=ExtractData(Fund_FILE_NM,[5],[0,1,2,4,7],';')
    Fund_Grp_Lst=CreateMasterFundList(Fund_Com_Lst)
    Fund_Com_Lst=AddAnalyticalDataInMasterFundList(Fund_Grp_Lst)
 
    Fund_Sub = list(filter(None, Fund_Sub))
    for Fund_Sub_str in Fund_Sub:
         FundCompList=[]
         FundDesc=[]
         FundDescSub,ISIN=RetOneListDesc(Fund_Com_Lst[Fund_Sub_str][0])
         FundDesc.append(FundDescSub)
         for Fund_Ind_Row in Fund_Com_Lst[Fund_Sub_str]:
            FundRow=RetOneList(Fund_Ind_Row)
            FundCompList.append(FundRow)
         GDB.InsertOneFundData(FundDesc,FundCompList,ISIN,Cur_Dt_Formatted)

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

def ChangeDtFomat(date_str,SrcFrmt,TrgtFrmt):
   date_obj = datetime.datetime.strptime(date_str, SrcFrmt)
   formatted_date = date_obj.strftime(TrgtFrmt)
   return formatted_date

def IsLoadHistorCur(Cur_Dt_Formatted,Cur_Dt):
   Day=Cur_Dt.strftime("%a")
   WEEKEND=['Sat,Sun']
   IsMarketClosedToday=GDB.IsTodayTradeClosed(Cur_Dt_Formatted)
   IsWeekEnd=False
   if(Day in WEEKEND):
       IsWeekEnd=True
   MrktStrtLst=MRKT_STRT_TM.split(":")
   MrktEndLst=MRKT_END_TM.split(":")
   HistLoadStrtInMin=int(MrktEndLst[0])*60+int(MrktEndLst[1])
   MarStrInMin=int(MrktStrtLst[0])*60+int(MrktStrtLst[1])
   HistLoadEndInMin=(int(MrktStrtLst[0])-HIST_LOAD_PER)*60+int(MrktStrtLst[1])
   Cur_Dt = datetime.datetime.now()
   Hr=int(Cur_Dt.strftime("%H"))
   Mn=int(Cur_Dt.strftime("%M"))
   Tot_Min=Hr*60+Mn
   IsWithinHistLoadWin=False
   if((Tot_Min>HistLoadStrtInMin) or (Tot_Min<HistLoadEndInMin)):
       IsWithinHistLoadWin=True
   IsLoadHis=LOAD_HIST_ANYTIME or IsMarketClosedToday or IsWeekEnd or IsWithinHistLoadWin
   IsUpdToday=GDB.IsFundUpdatedToday(Cur_Dt_Formatted)
   IsLoadCur= (not IsMarketClosedToday) and (not IsWeekEnd) and (not IsUpdToday) and (Tot_Min>MarStrInMin) 
   return IsLoadHis,IsLoadCur

def UpdAnalyticDataForOneSch(OneNAVRec):
   No_Of_Rows= int(OneNAVRec[5])
   ISIN=OneNAVRec[2]
   Price_Lst,Last_EMA_9,Last_EMA_12,Last_EMA_21,Last_EMA_26,Last_EMA_50,Last_EMA_100,Gain_Lst,Loss_Lst,SecLast=GDB.GetPrevAnalyticalData(No_Of_Rows,ISIN)
   Lst=OneNAVRec[3]=float(OneNAVRec[3])
   Gain_Lst,Loss_Lst,Price_Lst_GAIN,Price_Lst_LOSS=UpdGainLossList(Lst,SecLast,Gain_Lst,Loss_Lst)
   Price_Lst.append(Lst)
   Price_Lst_Mean,Price_Lst_StdDev2,Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,Price_Lst_GAIN,Price_Lst_LOSS,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,RSI,MACD=GetAnalyticalData(Price_Lst,Last_EMA_9,Last_EMA_12,Last_EMA_21,Last_EMA_26,Last_EMA_50,Last_EMA_100,Gain_Lst,Loss_Lst)
   BuySellRecommend=CalBuySellRecommend(Lst,Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,RSI)
   GDB.LoadLastNAVData(Price_Lst_Mean,Price_Lst_StdDev2,Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,Price_Lst_GAIN,Price_Lst_LOSS,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,RSI,MACD,BuySellRecommend,OneNAVRec)
   

def UpdLatestNAVForAll(LstOfFundNeedsToUpd):
   for OneNAVRec in LstOfFundNeedsToUpd:
      UpdAnalyticDataForOneSch(OneNAVRec)
      GDB.UpdFILoaded(OneNAVRec[0],OneNAVRec[4])


       




