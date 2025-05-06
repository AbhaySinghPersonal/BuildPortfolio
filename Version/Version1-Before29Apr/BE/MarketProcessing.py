from MarketConfig import HIST_LINK,XPATH_HIST_Fund_DROP_DOWN,XPATH_HIST_TYP_DROP_DOWN,TYP_OPT,YR_MON_DAY_FR_CUR
from MarketConfig import XPATH_HIST_FRM_DT,XPATH_HIST_TO_DT,XPATH_HIST_DOWNLOAD,Fund_FILE_NM,CURR_LINK,LIST_OF_Fund,LIST_OF_Equity
from MarketConfig import MUTUAL_FUND,EQUITY,NSE_EXT,ALL,LIST_OF_ALL,CANDLE, WEEKLY, DAILY, MONTHLY,MIXED
import requests
import Generic as G
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime, timedelta
import GenericDB as GDB
import yfinance as yf
import ta
import pandas as pd
from pandas.tseries.offsets import BMonthEnd  
import numpy as np

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
    if(PrevDt==None):
        PrevDt=Dt
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

def ExtractData(one_Fund,Per,Exchng):
    ticker = one_Fund[0]
    # Fetch the data
    stock_data = yf.Ticker(ticker)
    # Get historical data (e.g., last 5 years)
    historical_data = stock_data.history(period=Per)
    Fund_Grp_Lst={}
    Fund_Sub_Ret=[]
    OpenPrc=0
    ClosePrc=0
    HighPrc=0
    LowPrc=0

    Dt=None
    FrstMonPassed=False
    FrstDtPassed=False
    LoadFlag=False
    for idx in historical_data.index:
        KEY=one_Fund[0]
        if((KEY not in Fund_Grp_Lst) and (len(KEY)>0)):
            Fund_Grp_Lst[KEY]=[]
            Fund_Sub_Ret.append(KEY)
            print('Extracting:'+KEY)
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
        #if((len(KEY)>0) and (len(one_Fund[2])>0)):
            #Fund_Grp_Lst[KEY].append([one_Fund[0],one_Fund[1],one_Fund[2],Cls[idx],Dt[idx].date(),RSI[idx]])
            Fund_Grp_Lst[KEY].append([one_Fund[0],one_Fund[1],one_Fund[2],(OpenPrc+ClosePrc+HighPrc+LowPrc)/4,Dt.date(),one_Fund[3]])
    return Fund_Grp_Lst,Fund_Sub_Ret
        

def LoadHistory(Cur_Dt_Formatted):
    print('Load History')
    List_Of_FundTmp=G.GetListOfFund(LIST_OF_ALL)
    List_Of_FundTmp.remove(List_Of_FundTmp[0])
    List_Of_Fund=[]
    for L in List_Of_FundTmp:
        Ticker=L[0].strip()
        if(len(Ticker)==0):
            L[0] = get_ticker_from_isin(L[3])
        List_Of_Fund.append([L[0],L[1],L[2],L[3],L[4]])
    LEN=len(List_Of_Fund)
    idx=0
    for one_Fund in List_Of_Fund:
        try:
            idx=idx+1
            FundNm=one_Fund[1]
            Sch_Lst=[one_Fund[0]]
            SchCdLstLoaded=GDB.IsFundLoaded(Sch_Lst)
            FndTyp=one_Fund[2]
            del one_Fund[2]
            Sch_Lst_Prcs=[]
            for sc in Sch_Lst:
                if ((sc not in SchCdLstLoaded) and (len(sc)>0)):
                    Sch_Lst_Prcs.append(sc)
            if len(Sch_Lst_Prcs)>0:
                print('########Loading Fund:'+FundNm+" "+str(idx)+" of "+str(LEN)+"#######")
                Fund_Com_Lst,Fund_Sub=ExtractData(one_Fund,"5y",NSE_EXT)
                G.CreateAndLoadAnalyticalData(Fund_Com_Lst,Cur_Dt_Formatted,Fund_Sub,FndTyp)
                time.sleep(5)
        except SyntaxError:
            print('Exception SyntaxError'+'########Skipping Fund:'+FundNm)
        except TypeError:
            print('Exception TypeError'+'########Skipping Fund:'+FundNm)
        except NameError:
            print('Exception NameError'+'########Skipping Fund:'+FundNm)
        except IndexError:
            print('Exception IndexError'+'########Skipping Fund:'+FundNm)
        except KeyError:
            print('Exception KeyError'+'########Skipping Fund:'+FundNm)
        except ValueError:
            print('Exception ValueError'+'########Skipping Fund:'+FundNm)
        except AttributeError:
            print('Exception AttributeError'+'########Skipping Fund:'+FundNm)
        except IOError:
            print('Exception IOError'+'########Skipping Fund:'+FundNm)
        except ZeroDivisionError:
            print('Exception ZeroDivisionError'+'########Skipping Fund:'+FundNm)
        except ImportError:
            print('Exception ImportError'+'########Skipping Fund:'+FundNm)
        except TimeoutException as ex:
            print("Exception has been thrown. " + str(ex))
        except:
            print('UNCAUGHT EXCEPTION'+'########Skipping Fund:'+FundNm)

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

def UpdateCurrent(Cur_Dt):
    print('UpdateCurrent')
    SchmCodes=GDB.GetAllSchCode()
    LstOfFundNeedsToUpd=[]
    print('Total Funds:'+str(len(SchmCodes)))
    url = CURR_LINK
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
    for Sch in SchmCodes:
        try:
            print('Processing:'+Sch[2])
            FndTyp=Sch[3]
            if(FndTyp==MUTUAL_FUND):
                nav_data=get_latest_nav_by_isin(Sch[0],data)
                if(nav_data):
                    nav_data[4]=G.ChangeDtFomat(nav_data[4],"%d-%b-%Y","%Y-%m-%d")
                else:
                    continue
            elif(FndTyp==EQUITY):
                Fund_Com_Lst,Fund_Sub=ExtractData([Sch[0],Sch[2],Sch[1],Sch[4]],"1d",NSE_EXT)
                KEY_NAV=Fund_Sub[0]
                nav_data=Fund_Com_Lst[KEY_NAV][0]
                nav_data[4]=nav_data[4].strftime("%Y-%m-%d")
            else:
                print('Unknown Fund Type')
                continue
            
            nav_data.append(FndTyp)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            continue
        DoesSysLoadedLatNAV=GDB.IsSchUpdatedOnGivenDt(nav_data[4],Sch[0])
        if ((not DoesSysLoadedLatNAV) or (FndTyp==EQUITY)):
            if(isinstance(nav_data[3], float) or isinstance(nav_data[3], int)):
                LstOfFundNeedsToUpd.append(nav_data)
            else:
                nav_data[3]=float(nav_data[3])
                LstOfFundNeedsToUpd.append(nav_data)
    print('Total Funds to Update:'+str(len(LstOfFundNeedsToUpd)))
    if(len(LstOfFundNeedsToUpd)>0):
        Short_Long_Lst=G.UpdLatestNAVForAll(LstOfFundNeedsToUpd,Cur_Dt)
    print('After UpdLatestNAVForAll')
    G.ProposeFundsToAll(Short_Long_Lst)