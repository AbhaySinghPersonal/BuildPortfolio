uname= 'APP' #'celsioradminnew' #'APP'
pword= 'IplDC@2025' #'Celsior2025' 'Pyramid@123' #'Celsior2024'
server='localhost\SQLEXPRESS' #'celsiormetricsnew.database.windows.net' #'localhost\SQLEXPRESS'
dbname='Market' #'market' #'Market'
port="1433"
DEBUG=True
LINK='http://localhost:8081'
SECURITY_PASSWORD_SALT = '/2aX16zPnnIgfMwkOjGX4S'
HIST_LINK='https://www.amfiindia.com/nav-history-download'
CURR_LINK="https://www.amfiindia.com/spages/NAVAll.txt"
CHROME_DRIVER_PATH='chromedriver.exe'
LIST_OF_Fund='MF_LIST.csv'
LIST_OF_Equity='EQ_LIST.csv'
LIST_OF_ALL='LIST.csv'  
    #https://www.nseindia.com/products-services/indices-nifty500-index
    #https://www.nseindia.com/products-services/indices-nifty50-index
    #https://www.nseindia.com/products-services/indices-nifty100-index
EDGE='E'
CHROME='C'
FIREFOX='F'
BROWSER=CHROME
TYP_OPT="All"
YR_MON_DAY_FR_CUR="5Y"  #5Y - 5 year    5M - 5 MONTH    90D- 90 Days
Fund_FILE_NM="MF.csv"
TRADE_CLOSE_LOAD_FILE_NM="HOLIDAY_LIST.csv"  #For Ind IN.csv for US US.csv
TRADE_CLOSE_LOAD_ON="02-01"
MRKT_STRT_TM="9:15"
MRKT_END_TM= "15:30"
HIST_LOAD_PER=3  #Load hitory 3 Hours before start of Market
LOAD_HIST_ANYTIME =True  #If it is True than Load on any day otherwise on Holidays
LOAD_HLDY_ANYTIME =True  #If it is True than Load on any day otherwise on 2nd Jan
LOAD_CHCK_INTVL=3600
RSI_CAL_METHOD="SMA"  #SMA - Simple Moving Average  EMA - Exponential Moving Average #CCI - Commodity Channel Index
METHOD_CCI="CCI"
METHOD_SMA="SMA"

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
EQUITY="EQ"
COMMODITY="CM"
OPTIONS_RIGHTS="OP"
NSE_EXT=".NS"
SHRT_LNG_MAPNG={STRONG_SHORT:"STRONG SHORT",SHORT:"SHORT",STRONG_LONG:"STRONG LONG",LONG:"LONG",NONE:"None"}
ALL="ALL"

WEEKLY='W'
DAILY='D'   
MONTHLY='M'
MIXED='X'   #Mixed
CANDLE=DAILY #D-Daily W-Weekly M-Monthly
TwoSD=1.9
ThreeSD=3
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import urllib


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={dbname};UID={uname};PWD={pword};Trusted_Connection=no;"
)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)


