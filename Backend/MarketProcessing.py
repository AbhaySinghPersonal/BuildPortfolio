from MarketConfig import HIST_LINK,XPATH_HIST_Fund_DROP_DOWN,XPATH_HIST_TYP_DROP_DOWN,TYP_OPT,YR_MON_DAY_FR_CUR
from MarketConfig import XPATH_HIST_FRM_DT,XPATH_HIST_TO_DT,XPATH_HIST_DOWNLOAD,Fund_FILE_NM,CURR_LINK,LIST_OF_Fund,LIST_OF_Equity
from MarketConfig import MUTUAL_FUND,EQUITY,NSE_EXT,ALL
import requests
import Generic as G
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import GenericDB as GDB
import yfinance as yf

def DownLoadOneFund(Fund_NM,driver):
    print('Downloading:'+Fund_NM)
    Fund_dropdown_element=driver.find_element(By.XPATH,XPATH_HIST_Fund_DROP_DOWN)
    Fund_dropdown_element.send_keys(Fund_NM)
    TYP_dropdown_element=driver.find_element(By.XPATH,XPATH_HIST_TYP_DROP_DOWN)
    TYP_dropdown_element.send_keys(TYP_OPT)
    Fr_Dt,To_Dt=G.getStartEndDate(YR_MON_DAY_FR_CUR)
    Frm_DT_element=driver.find_element(By.XPATH,XPATH_HIST_FRM_DT)
    Frm_DT_element.send_keys(Fr_Dt)
    To_DT_element=driver.find_element(By.XPATH,XPATH_HIST_TO_DT)
    To_DT_element.send_keys(To_Dt)
    DownloadButton=driver.find_element(By.XPATH,XPATH_HIST_DOWNLOAD)
    driver.implicitly_wait(10)
    time.sleep(10)
    ActionChains(driver).move_to_element(DownloadButton).click(DownloadButton).perform()
    driver.get(DownloadButton.get_attribute('href'))
    while(True):
        try:
            WebDriverWait(driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
            break
        except TimeoutException as err:
            continue
    time.sleep(20)
    PgText=driver.find_element(By.XPATH,'/html/body/pre').get_attribute('innerText')
    return PgText
    #with open(Fund_FILE_NM, 'w+') as f:
    #    #f.write(driver.page_source)
    #    f.write(Pg.text)

def ExtractDataForEQ(one_Fund,Per,Exchng):
    ticker = one_Fund[0]+ Exchng # Replace with the desired stock ticker
    # Fetch the data
    stock_data = yf.Ticker(ticker)
    # Get historical data (e.g., last 5 years)
    historical_data = stock_data.history(period=Per)
    EQ_Cls_Dt_ClsPrc=historical_data['Close']
    Dt=EQ_Cls_Dt_ClsPrc.index.to_list()
    Cls=EQ_Cls_Dt_ClsPrc.to_list()
    LEN_Of_Dur=len(Dt)
    Fund_Grp_Lst={}
    Fund_Sub_Ret=[]
    for idx in range(0,LEN_Of_Dur):
        KEY=one_Fund[0]
        if((KEY not in Fund_Grp_Lst) and (len(KEY)>0)):
            Fund_Grp_Lst[KEY]=[]
            Fund_Sub_Ret.append(KEY)
            print('Extracting:'+KEY)
        if((len(KEY)>0) and (len(one_Fund[2])>0)):
            Fund_Grp_Lst[KEY].append([one_Fund[0],one_Fund[1],one_Fund[2],Cls[idx],Dt[idx].date()])
    return Fund_Grp_Lst,Fund_Sub_Ret
        

def LoadHistoryStck(Cur_Dt_Formatted):
    print('Load History Stocks')
    List_Of_FundTmp=G.GetListOfFund(LIST_OF_Equity)
    List_Of_FundTmp.remove(List_Of_FundTmp[0])
    List_Of_Fund=[]
    for L in List_Of_FundTmp:
        List_Of_Fund.append([L[0],L[1],L[6]])
    LEN=len(List_Of_Fund)
    idx=0
    for one_Fund in List_Of_Fund:
        idx=idx+1
        FundNm=one_Fund[1]
        Sch_Lst=[one_Fund[0]]
        SchCdLstLoaded=GDB.IsFundLoaded(Sch_Lst)
        Sch_Lst_Prcs=[]
        for sc in Sch_Lst:
            if ((sc not in SchCdLstLoaded) and (len(sc)>0)):
                Sch_Lst_Prcs.append(sc)
        if len(Sch_Lst_Prcs)>0:
            print('########Loading Fund:'+FundNm+" "+str(idx)+" of "+str(LEN)+"#######")
            Fund_Com_Lst,Fund_Sub=ExtractDataForEQ(one_Fund,"5y",NSE_EXT)
            G.CreateAndLoadAnalyticalData(Fund_Com_Lst,Cur_Dt_Formatted,Fund_Sub,EQUITY)
            time.sleep(5)

def LoadHistory(Cur_Dt_Formatted):
    print('Load History')
    List_Of_Fund=G.GetListOfFund(LIST_OF_Fund)
    List_Of_Fund.remove(List_Of_Fund[0])
    LEN=len(List_Of_Fund)
    idx=0
    driver=G.getDriver()
    url=HIST_LINK
    driver.get(url)
    for one_Fund in List_Of_Fund:
        idx=idx+1
        FundNm=one_Fund[0]
        Sch_Lst=one_Fund[1:]
        if((len(Sch_Lst)==0) or (Sch_Lst[0].strip()=='')):
            Sch_Lst=[ALL]
        SchCdLstLoaded=GDB.IsFundLoaded(Sch_Lst)
        Sch_Lst_Prcs=[]
        for sc in Sch_Lst:
            if ((sc not in SchCdLstLoaded) and (len(sc)>0)):
                Sch_Lst_Prcs.append(sc)
        if len(Sch_Lst_Prcs)>0:
            print('########Loading Fund:'+FundNm+" "+str(idx)+" of "+str(LEN)+"#######")
            Pg=DownLoadOneFund(FundNm,driver)
            G.LoadOneFund(tuple(Sch_Lst_Prcs),Cur_Dt_Formatted,Pg,MUTUAL_FUND)
            time.sleep(5)
    if driver:
        print('Going to close Driver')
        try:
            driver.close()
            print('after close')
            driver.quit()
        except:
            print('Exception in closining driver')


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
            """
            return {
                "scheme_code": fields[0],
                "ISIN": fields[1],
                "scheme_name": fields[3],
                "nav": fields[4],
                "date": fields[5]
            }
            """
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
                Fund_Com_Lst,Fund_Sub=ExtractDataForEQ([Sch[0],Sch[2],Sch[1]],"1d",NSE_EXT)
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