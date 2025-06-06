from flask_sqlalchemy import SQLAlchemy
from Model import db,app
from Model import TradingClosedDate,FIUpdatedDate,FIAnalyticsData,FILoaded
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
def BulkInsertTradeClosedDate(HolListDict,Year):
    with app.app_context():
        count = db.session.query(TradingClosedDate).filter_by(Year=Year).count()
        if(count==0):
            db.session.bulk_insert_mappings(TradingClosedDate, HolListDict)
            db.session.commit()

def IsTodayTradeClosed(Cur_Dt_Formatted):
    count=0
    with app.app_context():
        count = db.session.query(TradingClosedDate).filter_by(ClosedDate=Cur_Dt_Formatted).count()
    if(count==0):
        return False
    else:
        return True
    
def IsFundUpdatedToday(Cur_Dt_Formatted):
    count=0
    with app.app_context():
        count = db.session.query(FIUpdatedDate).filter_by(UpdDate=Cur_Dt_Formatted).count()
    if(count==0):
        return False
    else:
        return True


def BulkInsertFIAnalyticsData(FundCompList,ISIN):
    try:
        with app.app_context():
            count = db.session.query(FIAnalyticsData).filter_by(ISIN=ISIN).count()
            if(count==0):
                db.session.bulk_insert_mappings(FIAnalyticsData, FundCompList)
                db.session.commit()
    except IntegrityError as e:
        print(f"IntegrityError occurred: {e}")
        db.session.rollback()
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
        db.session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.session.rollback()

def BulkInsertFILoaded(FundDesc,ISIN,Cur_Dt_Formatted):
    try:
        with app.app_context():
            count = db.session.query(FILoaded).filter_by(ISIN=ISIN).count()
            if(count==0):
                db.session.bulk_insert_mappings(FILoaded, FundDesc)
                db.session.commit()
            else:
                UpdFILoaded(FundDesc['SchemeCode'],Cur_Dt_Formatted)
    except IntegrityError as e:
        print(f"IntegrityError occurred: {e}")
        db.session.rollback()
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
        db.session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.session.rollback()

def InsertOneFundData(FundDesc,FundCompList,ISIN,Cur_Dt_Formatted):
    BulkInsertFILoaded(FundDesc,ISIN,Cur_Dt_Formatted)
    BulkInsertFIAnalyticsData(FundCompList,ISIN)


def IsFundLoaded(FundList):
    try:
        with app.app_context():
            count = db.session.query(FILoaded).filter(FILoaded.FundName.in_(FundList)).count()
            if(count==0):
                return False
            else:
                return True
    except IntegrityError as e:
        print(f"IntegrityError occurred: {e}")
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def GetAllSchCode():
    try:
        SchCd=None
        SchCdLst=[]
        CalLst=[]
        with app.app_context():
            SchCd = db.session.query(FILoaded).with_entities(FILoaded.SchemeCode).all()
        for Sch in SchCd:
            OneRec=[]
            OneRec.append(Sch.SchemeCode)
            SchCdLst.append(OneRec)
        return SchCdLst
    except IntegrityError as e:
        print(f"IntegrityError occurred: {e}")
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def IsSchUpdatedOnGivenDt(Cur_Dt_Formatted,Sch):
    count=0
    with app.app_context():
        count = db.session.query(FILoaded).filter_by(SchemeCode=Sch,UpdDate=Cur_Dt_Formatted).count()
    if(count==0):
        return False
    else:
        return True

def UpdFILoaded(Sch,Cur_Dt_Formatted):
    try:
        with app.app_context():
            FILoadedObj=db.session.query(FILoaded).filter_by(SchemeCode=Sch).first()
            FILoadedObj.UpdDate=Cur_Dt_Formatted
            db.session.commit()
    except IntegrityError as e:
        print(f"IntegrityError occurred: {e}")
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def GetPrevAnalyticalData(No_Of_Rows,ISIN):
    try:
        AnalyticalDataRaw=None
        with app.app_context():
            AnalyticalDataRaw=db.session.query(FIAnalyticsData).filter_by(ISIN=ISIN).order_by(FIAnalyticsData.id.desc()).all()[-No_Of_Rows:]
        Price_Lst=[]
        Gain_Lst=[]
        Loss_Lst=[]
        for  AnalyticalDatarow in  AnalyticalDataRaw:
            Last=AnalyticalDatarow
            Price_Lst.append(AnalyticalDatarow.FundPrice)
            Gain_Lst.append(AnalyticalDatarow.Price_Lst_GAIN)
            Loss_Lst.append(AnalyticalDatarow.Price_Lst_LOSS)
        Last_EMA_9=Last.EMA_9
        Last_EMA_12=Last.EMA_12
        Last_EMA_21=Last.EMA_21
        Last_EMA_26=Last.EMA_26
        Last_EMA_50=Last.EMA_50
        Last_EMA_100=Last.EMA_100
        SecLast=Last.FundPrice
        return Price_Lst,Last_EMA_9,Last_EMA_12,Last_EMA_21,Last_EMA_26,Last_EMA_50,Last_EMA_100,Gain_Lst,Loss_Lst,SecLast
    except IntegrityError as e:
        print(f"IntegrityError occurred: {e}")
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
   

def LoadLastNAVData(Price_Lst_Mean,Price_Lst_StdDev2,Price_Lst_Mean_Plus_StdDev2,Price_Lst_Mean_Minus_StdDev2,Price_Lst_GAIN,Price_Lst_LOSS,EMA_9,EMA_12,EMA_21,EMA_26,EMA_50,EMA_100,RSI,MACD,BuySellRecommend,OneNAVRec):
    try:
        with app.app_context():
            FIAnalyticsDataRow=FIAnalyticsData(ISIN=OneNAVRec[1],FundPrice=OneNAVRec[3],
                FundPriceAsOnDate=OneNAVRec[4],BuySellRecommend=BuySellRecommend,Price_Lst_Mean=Price_Lst_Mean,
                Price_Lst_StdDev2=Price_Lst_StdDev2,Price_Lst_Mean_Plus_StdDev2=Price_Lst_Mean_Plus_StdDev2,
                Price_Lst_Mean_Minus_StdDev2=Price_Lst_Mean_Minus_StdDev2,Price_Lst_GAIN=Price_Lst_GAIN,Price_Lst_LOSS=Price_Lst_LOSS,
                EMA_9=EMA_9,EMA_12=EMA_12,EMA_21=EMA_21,EMA_26=EMA_26,EMA_50=EMA_50,EMA_100=EMA_100,RSI=RSI,MACD=MACD)
            db.session.add(FIAnalyticsDataRow)
            db.session.commit()
    except IntegrityError as e:
        print(f"IntegrityError occurred: {e}")
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
