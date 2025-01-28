import datetime
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql.expression import update
from flask_marshmallow import Marshmallow
from MarketConfig import DEBUG,uname,	pword,	server,	dbname
app=Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# Python 3.x
import urllib
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER="+server+";DATABASE="+dbname+";UID="+uname+";PWD="+pword+";Trusted_Connection=yes;")
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
db=SQLAlchemy(app)
ma=Marshmallow(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    userName=db.Column(db.String(32))
    userEmail=db.Column(db.String(32),unique=True)
    userAge=db.Column(db.Integer)
    userAddress=db.Column(db.String(128))
    userPassword=db.Column(db.String(256))
    userLastPassword=db.Column(db.String(256))
    userIsActive=db.Column(db.String(1),default='Y') 
    UpdDate=db.Column(db.DateTime,default=datetime.datetime.now())
    def __init__(self,userName,userEmail,userAge,userAddress,userPassword):
        self.userName=userName
        self.userEmail=userEmail
        self.userAge=userAge
        self.userAddress=userAddress
        self.userPassword=userPassword
    
class UserSchema(ma.Schema):
    class Meta:
        fields=('id','userName','userEmail','userAge','userAddress','userPassword','userLastPassword','userIsActive','UpdDate')

class Funds(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Email=db.Column(db.String(32),unique=True)
    totalFund=db.Column(db.Double)
    allocatedFund=db.Column(db.Double)
    unusedFund=db.Column(db.Double)
    UpdDate=db.Column(db.DateTime,default=datetime.datetime.now())
    def __init__(self,Email,totalFund,allocatedFund,unusedFund):
        self.Email=Email
        self.totalFund=totalFund
        self.allocatedFund=allocatedFund
        self.unusedFund=unusedFund
    
class FundSchema(ma.Schema):
    class Meta:
        fields=('id','Email','totalFund','allocatedFund','unusedFund','UpdDate')

class FILoaded(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ISIN=db.Column(db.String(12),unique=True)
    SchemeCode=db.Column(db.String(6))
    FundName=db.Column(db.String(128))
    FundType=db.Column(db.String(2)) #MF Mutual Fund
    UpdDate=db.Column(db.Date)
    def __init__(self,ISIN,SchemeCode,FundName,FundType):
        self.ISIN=ISIN
        self.SchemeCode=SchemeCode
        self.FundName=FundName
        self.FundType=FundType

class FILoadedchema(ma.Schema):
    class Meta:
        fields=('id','ISIN','SchemeCode','FundName','FundType','UpdDate')

class FIUpdatedDate(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    UpdDate=db.Column(db.Date)

class FIUpdatedDatSchema(ma.Schema):
    class Meta:
        fields=('id','UpdDate')

class FIAnalyticsData(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ISIN=db.Column(db.String(12))
    FundPrice=db.Column(db.Double)
    FundPriceAsOnDate=db.Column(db.Date)
    BuySellRecommend=db.Column(db.String(2))
    Price_Lst_Mean=db.Column(db.Double)
    Price_Lst_StdDev2=db.Column(db.Double)
    Price_Lst_Mean_Plus_StdDev2=db.Column(db.Double)
    Price_Lst_Mean_Minus_StdDev2=db.Column(db.Double)
    Price_Lst_GAIN=db.Column(db.Double)
    Price_Lst_LOSS=db.Column(db.Double)
    EMA_9=db.Column(db.Double)
    EMA_12=db.Column(db.Double)
    EMA_21=db.Column(db.Double)
    EMA_26=db.Column(db.Double)
    EMA_50=db.Column(db.Double)
    EMA_100=db.Column(db.Double)
    RSI=db.Column(db.Double)
    MACD=db.Column(db.Double)
    UpdDate=db.Column(db.DateTime,default=datetime.datetime.now())
    def __init__(self,ISIN,FundPrice,FundPriceAsOnDate,BuySellRecommend,Price_Lst_Mean,Price_Lst_StdDev2,Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,Price_Lst_GAIN,Price_Lst_LOSS,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,RSI,MACD):
        self.ISIN=ISIN
        self.FundPrice=FundPrice
        self.FundPriceAsOnDate=FundPriceAsOnDate
        self.BuySellRecommend=BuySellRecommend
        self.Price_Lst_Mean=Price_Lst_Mean
        self.Price_Lst_StdDev2=Price_Lst_StdDev2
        self.Price_Lst_Mean_Plus_StdDev2=Price_Lst_Mean_Plus_StdDev2
        self.Price_Lst_Mean_Minus_StdDev2=Price_Lst_Mean_Minus_StdDev2
        self.Price_Lst_GAIN=Price_Lst_GAIN
        self.Price_Lst_LOSS=Price_Lst_LOSS
        self.EMA_9=EMA_9
        self.EMA_12=EMA_12
        self.EMA_21=EMA_21
        self.EMA_26=EMA_26
        self.EMA_50=EMA_50
        self.EMA_100=EMA_100
        self.RSI=RSI
        self.MACD=MACD
            
class FIAnalyticsDataSchema(ma.Schema):
    class Meta:
        fields=('id','ISIN','FundPrice','FundPriceAsOnDate','BuySellRecommend','Price_Lst_Mean','Price_Lst_StdDev2','Price_Lst_Mean_Plus_StdDev2','Price_Lst_Mean_Minus_StdDev2','Price_Lst_GAIN','Price_Lst_LOSS','EMA_9','EMA_12','EMA_21','EMA_26','EMA_50','EMA_100','RSI','MACD','UpdDate')

class TradingClosedDate(db.Model):
    __tablename__ = 'TradingClosedDate'
    id=db.Column(db.Integer,primary_key=True)
    CountyCode=db.Column(db.String(2))
    Segment=db.Column(db.String(2))  
        #CM Capital Market (Equities) Trade
        #FO Futures & Options  
        #CD Currency Derivatives
        #CM Commodity Derivatives
        #SL Securities Lending & Borrowing Scheme
        #MF Mutual Fund
        #DS Debt Segment
    Year=db.Column(db.Integer)
    ClosedDate=db.Column(db.Date)
    __table_args__ = (
        UniqueConstraint('CountyCode', 'Segment', 'Year', 'ClosedDate', name='uq_allColl'),)
    def __init__(self,CountyCode,Year,Segment,ClosedDate):
        self.CountyCode=CountyCode
        self.Year=Year
        self.Segment=Segment
        self.ClosedDate=ClosedDate

class TradingClosedDateSchema(ma.Schema):
    class Meta:
        fields=('id','CountyCode','Year','Segment','ClosedDate')

class FIShortLong(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ISIN=db.Column(db.String(12))
    UpdDate=db.Column(db.Date)
    BuySellRecommend=db.Column(db.String(2))
    def __init__(self,ISIN,UpdDate,BuySellRecommend):
        self.ISIN=ISIN
        self.UpdDate=UpdDate
        self.BuySellRecommend=BuySellRecommend

class FIShortLongSchema(ma.Schema):
    class Meta:
        fields=('id','ISIN','UpdDate','BuySellRecommend')

class ProposedFundBuySellAction(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Email=db.Column(db.String(32))
    ISIN=db.Column(db.String(12))
    FundPrice=db.Column(db.Double)
    Units=db.Column(db.Double)
    BUY_SELL=db.Column(db.String(2))  #B Buy S Sell
    __table_args__ = (
        UniqueConstraint('Email', 'ISIN', name='uq_MailISIN'),)
    def __init__(self,Email,ISIN,FundPrice,Units,BUY_SELL):
        self.Email=Email
        self.ISIN=ISIN
        self.FundPrice=FundPrice
        self.Units=Units
        self.BUY_SELL=BUY_SELL
    
class ProposedFundBuySellActionSchema(ma.Schema):
    class Meta:
        fields=('id','Email','ISIN','FundPrice','Units','BUY_SELL')

class Holdings(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Email=db.Column(db.String(32))
    ISIN=db.Column(db.String(12))
    FundPrice=db.Column(db.Double)
    Units=db.Column(db.Double)
    __table_args__ = (
        UniqueConstraint('Email', 'ISIN', name='uq_MailISIN'),)
    def __init__(self,Email,ISIN,FundPrice,Units):
        self.Email=Email
        self.ISIN=ISIN
        self.FundPrice=FundPrice
        self.Units=Units

class HoldingsSchema(ma.Schema):
    class Meta:
        fields=('id','Email','ISIN','FundPrice','Units')

class TransationHistory(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Email=db.Column(db.String(32))
    ISIN=db.Column(db.String(12))
    StartingUnits=db.Column(db.Double)
    BUY_SELL=db.Column(db.String(2))  #B Buy S Sell
    BUY_SELL_Units=db.Column(db.Double)
    FinalUnits=db.Column(db.Double)
    TransDate=db.Column(db.Date)
    def __init__(self,Email,ISIN,StartingUnits,BUY_SELL,FinalUnits,TransDate):
        self.Email=Email
        self.ISIN=ISIN
        self.StartingUnits=StartingUnits
        self.BUY_SELL=BUY_SELL
        self.FinalUnits=FinalUnits
        self.TransDate=TransDate

class TransationHistorySchema(ma.Schema):
    class Meta:
        fields=('id','Email','ISIN','StartingUnits','BUY_SELL','FinalUnits','TransDate')