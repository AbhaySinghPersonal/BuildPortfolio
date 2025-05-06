import datetime
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql.expression import update
from flask_marshmallow import Marshmallow
from MarketConfig import DEBUG,uname,	pword,	server,	dbname
from MarketConfig import  db, ma

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    userName=db.Column(db.String(10))
    userEmail=db.Column(db.String(32),unique=True)
    userPassword=db.Column(db.String(256))
    userLastPassword=db.Column(db.String(256))
    userIsActive=db.Column(db.String(1),default='Y') 
    UpdDate=db.Column(db.DateTime,default=datetime.datetime.now())
    def __init__(self,userName,userEmail,userPassword):
        self.userName=userName
        self.userEmail=userEmail
        self.userPassword=userPassword
    
class UserSchema(ma.Schema):
    class Meta:
        fields=('id','userName','userEmail','userPassword','userLastPassword','userIsActive','UpdDate')

class Funds(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Email=db.Column(db.String(32),unique=True)
    totalFund=db.Column(db.Double)
    allocatedFund=db.Column(db.Double)
    unusedFund=db.Column(db.Double)
    UpdDate=db.Column(db.DateTime,default=datetime.datetime.now())
    MFPer=db.Column(db.Numeric(3,1))
    EQPer=db.Column(db.Numeric(3,1))
    CMPer=db.Column(db.Numeric(3,1))
    OPPer=db.Column(db.Numeric(3,1))
    def __init__(self,Email,totalFund,allocatedFund,unusedFund,MFPer,EQPer,CMPer,OPPer):
        self.Email=Email
        self.totalFund=totalFund
        self.allocatedFund=allocatedFund
        self.unusedFund=unusedFund
        self.MFPer=MFPer
        self.EQPer=EQPer
        self.CMPer=CMPer
        self.OPPer=OPPer
    
class FundSchema(ma.Schema):
    class Meta:
        fields=('id','Email','totalFund','allocatedFund','unusedFund','MFPer','EQPer','CMPer','OPPer','UpdDate')

class FILoaded(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ISIN=db.Column(db.String(12),unique=True)
    Ticker=db.Column(db.String(16))
    FundName=db.Column(db.String(128))
    FundType=db.Column(db.String(2)) #MF Mutual Fund #EQ EQUITY #CM COMMODITY #OP OPTION & FUTURE
    AssetRank=db.Column(db.Integer)
    UpdDate=db.Column(db.Date)
    
    def __init__(self,ISIN,Ticker,FundName,FundType,AssetRank):
        self.ISIN=ISIN
        self.Ticker=Ticker
        self.FundName=FundName
        self.FundType=FundType
        self.AssetRank=AssetRank

class FILoadedchema(ma.Schema):
    class Meta:
        fields=('id','ISIN','Ticker','FundName','FundType','AssetRank','UpdDate')

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
    Price_Lst_StdDev3=db.Column(db.Double)
    Price_Lst_Mean_Plus_StdDev3=db.Column(db.Double)
    Price_Lst_Mean_Minus_StdDev3=db.Column(db.Double)
    Sum_Of_Square_Of_Prc_Minus_Mean=db.Column(db.Double)
    Price_Lst_GAIN=db.Column(db.Double)
    Price_Lst_LOSS=db.Column(db.Double)
    EMA_9=db.Column(db.Double)
    EMA_12=db.Column(db.Double)
    EMA_21=db.Column(db.Double)
    EMA_26=db.Column(db.Double)
    EMA_50=db.Column(db.Double)
    EMA_100=db.Column(db.Double)
    Smoothed_Gain=db.Column(db.Double)
    Smoothed_Loss=db.Column(db.Double)
    RSI=db.Column(db.Double)
    CCI=db.Column(db.Double)
    MACD=db.Column(db.Double)
    Signal_Line=db.Column(db.Double)
    UpdDate=db.Column(db.DateTime,default=datetime.datetime.now())
    def __init__(self,ISIN,FundPrice,FundPriceAsOnDate,BuySellRecommend,Price_Lst_Mean,Price_Lst_StdDev2,Price_Lst_Mean_Plus_StdDev2,Price_Lst_StdDev3, Price_Lst_Mean_Plus_StdDev3, Price_Lst_Mean_Minus_StdDev3,Price_Lst_Mean_Minus_StdDev2,Price_Lst_GAIN,Price_Lst_LOSS,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,Smoothed_Gain,Smoothed_Loss,RSI,CCI,MACD,Sum_Of_Square_Of_Prc_Minus_Mean,Signal_Line):
        self.ISIN=ISIN
        self.FundPrice=FundPrice
        self.FundPriceAsOnDate=FundPriceAsOnDate
        self.BuySellRecommend=BuySellRecommend
        self.Price_Lst_Mean=Price_Lst_Mean
        self.Price_Lst_StdDev2=Price_Lst_StdDev2
        self.Price_Lst_Mean_Plus_StdDev2=Price_Lst_Mean_Plus_StdDev2
        self.Price_Lst_Mean_Minus_StdDev2=Price_Lst_Mean_Minus_StdDev2
        self.Price_Lst_StdDev3=Price_Lst_StdDev3
        self.Price_Lst_Mean_Plus_StdDev3=Price_Lst_Mean_Plus_StdDev3
        self.Price_Lst_Mean_Minus_StdDev3=Price_Lst_Mean_Minus_StdDev3
        self.Price_Lst_GAIN=Price_Lst_GAIN
        self.Price_Lst_LOSS=Price_Lst_LOSS
        self.EMA_9=EMA_9
        self.EMA_12=EMA_12
        self.EMA_21=EMA_21
        self.EMA_26=EMA_26
        self.EMA_50=EMA_50
        self.EMA_100=EMA_100
        self.Smoothed_Gain=Smoothed_Gain
        self.Smoothed_Loss=Smoothed_Loss
        self.RSI=RSI
        self.CCI=CCI
        self.MACD=MACD
        self.Sum_Of_Square_Of_Prc_Minus_Mean=Sum_Of_Square_Of_Prc_Minus_Mean
        self.Signal_Line=Signal_Line

            
class FIAnalyticsDataSchema(ma.Schema):
    class Meta:
        fields=('id','ISIN','FundPrice','FundPriceAsOnDate','BuySellRecommend','Price_Lst_Mean','Price_Lst_StdDev2','Price_Lst_Mean_Plus_StdDev2','Price_Lst_Mean_Minus_StdDev2','Price_Lst_StdDev3', 'Price_Lst_Mean_Plus_StdDev3', 'Price_Lst_Mean_Minus_StdDev3','Sum_Of_Square_Of_Prc_Minus_Mean','Price_Lst_GAIN','Price_Lst_LOSS','EMA_9','EMA_12','EMA_21','EMA_26','EMA_50','EMA_100','Smoothed_Gain','Smoothed_Loss','RSI','CCI','MACD','Signal_Line','UpdDate')

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
        UniqueConstraint('Email', 'ISIN', name='uq_MailISIN2'),)
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


class HolidayList(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    FundType=db.Column(db.String(2)) #MF Mutual Fund #EQ EQUITY #CM COMMODITY #OP OPTION & FUTURE
    Year=db.Column(db.Integer)
    HolidayDate=db.Column(db.Date)
    HolidayDetail=db.Column(db.String(64))
    __table_args__ = (
            UniqueConstraint('HolidayDate','FundType', name='uq_HLHDFT'),)
    def __init__(self,Year,HolidayDate,HolidayDetail, FundType):
        self.Year=Year
        self.HolidayDate=HolidayDate
        self.HolidayDetail=HolidayDetail
        self.FundType=FundType
     
class HolidayListSchema(ma.Schema):
    class Meta:
        fields=('id','Year','HolidayDate','HolidayDetail')
