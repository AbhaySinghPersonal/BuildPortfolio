uname='APP'
pword='Celsior2024'
server='localhost\SQLEXPRESS'
dbname='Market'
port="1433"
DEBUG=True
LINK='http://localhost:8081'
SECURITY_PASSWORD_SALT = '/2aX16zPnnIgfMwkOjGX4S'
HIST_LINK='https://www.amfiindia.com/nav-history-download'
CURR_LINK="https://www.amfiindia.com/spages/NAVAll.txt"
CHROME_DRIVER_PATH='chromedriver.exe'
LIST_OF_Fund='MF_LIST.csv'
EDGE='E'
CHROME='C'
FIREFOX='F'
BROWSER=EDGE
TYP_OPT="All"
YR_MON_DAY_FR_CUR="5Y"  #5Y - 5 year    5M - 5 MONTH    90D- 90 Days
Fund_FILE_NM="MF.csv"
TRADE_CLOSE_LOAD_FILE_NM="IN.csv"  #For Ind IN.csv for US US.csv
TRADE_CLOSE_LOAD_ON="02-01"
MRKT_STRT_TM="9:15"
MRKT_END_TM= "15:30"
HIST_LOAD_PER=3  #Load hitory 3 Hours before start of Market
LOAD_HIST_ANYTIME =True  #If it is True than Load on any day otherwise on Holidays
LOAD_CHCK_INTVL=3600

#ALL XPATHS
XPATH_HIST_Fund_DROP_DOWN='//*[@id="divNavDownMFName"]/span/input'
XPATH_HIST_TYP_DROP_DOWN='//*[@id="divNavDownType"]/span/input'
XPATH_HIST_FRM_DT='//*[@id="dpfrom"]'
XPATH_HIST_TO_DT='//*[@id="dpto"]'
XPATH_HIST_DOWNLOAD='//*[@id="hrDownload"]'

#Calculation
Smoothing_91=5/10
Smoothing_92=5/6
Smoothing_12=2/13
Smoothing_21=5/22
Smoothing_26=2/27
Smoothing_50=5/51
Smoothing_100=5/101
RSI_PERIOD=14
CAL_FREE_PERIOD="1Y"  #5Y - 5 year    5M - 5 MONTH    90D- 90 Days
STRONG_SHORT_VALUE=80
STRONG_LONG_VALUE=20
STRONG_SHORT="SS"   #"STRONG SHORT"
SHORT="S"           #"SHORT"
STRONG_LONG="SL"    #"STRONG_LONG"
LONG="L"            #"LONG"
NONE="NN"           #"NONE"
STRONG_TO_LONG_RATIO=3
MAX_FUND_TO_PROPOSE=5
SELL='S'
BUY='B'
MUTUAL_FUND="MF"
SHRT_LNG_MAPNG={STRONG_SHORT:"STRONG SHORT",SHORT:"SHORT",STRONG_LONG:"STRONG LONG",LONG:"LONG",NONE:"None"}




