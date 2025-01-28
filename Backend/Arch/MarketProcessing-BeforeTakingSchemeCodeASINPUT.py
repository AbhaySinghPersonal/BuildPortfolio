from MarketConfig import HIST_LINK,XPATH_HIST_Fund_DROP_DOWN,XPATH_HIST_TYP_DROP_DOWN,TYP_OPT,YR_MON_DAY_FR_CUR
from MarketConfig import XPATH_HIST_FRM_DT,XPATH_HIST_TO_DT,XPATH_HIST_DOWNLOAD,Fund_FILE_NM,CURR_LINK
import requests
import Generic as G
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time
import GenericDB as GDB

def DownLoadOneFund(driver,Fund_NM):
    url=HIST_LINK
    driver.get(url)
    #time.sleep(10)
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
    time.sleep(4)
    ActionChains(driver).move_to_element(DownloadButton).click(DownloadButton).perform()
    driver.get(DownloadButton.get_attribute('href'))
    Pg=driver.find_element(By.XPATH,'/html/body/pre')
    with open(Fund_FILE_NM, 'w+') as f:
        #f.write(driver.page_source)
        f.write(Pg.text)

def LoadHistory(driver,Cur_Dt_Formatted):
    print('LoadHistory')
    List_Of_Fund=G.GetListOfFund()
    LEN=len(List_Of_Fund)
    idx=0
    for one_Fund in List_Of_Fund:
        idx=idx+1
        print('########Loading Fund:'+one_Fund[0]+" "+str(idx)+" of "+str(LEN)+"#######")
        Is_Fund_Loaded=GDB.IsFundLoaded(one_Fund[1:])
        if not Is_Fund_Loaded:
            DownLoadOneFund(driver,one_Fund[0])
            G.LoadOneFund(one_Fund[1:],Cur_Dt_Formatted)
            G.RemoveFile(Fund_FILE_NM)
            time.sleep(5)

def get_latest_nav_by_isin(scheme_code):
    url = CURR_LINK
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
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
    return "NAV not found or data unavailable."

def UpdateCurrent(driver,Cur_Dt):
    print('UpdateCurrent')
    SchmCodes=GDB.GetAllSchCode()
    LstOfFundNeedsToUpd=[]
    for Sch in SchmCodes:
        nav_data=get_latest_nav_by_isin(Sch[0])
        nav_data[4]=G.ChangeDtFomat(nav_data[4],"%d-%b-%Y","%Y-%m-%d")
        DoesSysLoadedLatNAV=GDB.IsSchUpdatedOnGivenDt(nav_data[4],Sch[0])
        if not DoesSysLoadedLatNAV:
            LstOfFundNeedsToUpd.append(nav_data)
    if(len(LstOfFundNeedsToUpd)>0):
        G.UpdLatestNAVForAll(LstOfFundNeedsToUpd,Cur_Dt)