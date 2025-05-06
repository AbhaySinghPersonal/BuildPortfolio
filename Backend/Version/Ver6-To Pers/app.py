
from MarketConfig import DEBUG,NONE,SHRT_LNG_MAPNG
from Model import User,UserSchema,app,db,FundSchema,Funds,Holdings,HoldingsSchema,ProposedFundBuySellAction,ProposedFundBuySellActionSchema
from Model import FIShortLong,FIShortLongSchema
from flask import jsonify,request
import json
import Generic as G
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
user_schema=UserSchema()
users_schema=UserSchema(many=True)
fund_schema=FundSchema()
holding_schema=HoldingsSchema(many=True)
proposed_schema=ProposedFundBuySellActionSchema(many=True)
shortlong_schema=FIShortLongSchema()

def PrintOnConsole(str):
    if DEBUG:
        print(str)

@app.route('/Recommend', methods=['POST'])
def Recommend_fund():
    PrintOnConsole('-----------Recommend---------------')
    ISIN_F = request.json['ISIN']
    dateOn = request.json['Date']
    print('ISIN_F:', ISIN_F)
    print('dateOn:', dateOn)

    # Query for the record prior to dateOn
    previous_record = db.session.query(FIShortLong).filter(
        FIShortLong.ISIN == ISIN_F,
        FIShortLong.UpdDate < dateOn
    ).order_by(FIShortLong.UpdDate.desc()).first()

    # Query for the record on dateOn
    current_record = db.session.query(FIShortLong).filter(
        FIShortLong.ISIN == ISIN_F,
        FIShortLong.UpdDate == dateOn
    ).first()

    # Query for the record after dateOn
    next_record = db.session.query(FIShortLong).filter(
        FIShortLong.ISIN == ISIN_F,
        FIShortLong.UpdDate > dateOn
    ).order_by(FIShortLong.UpdDate.asc()).first()

    RET = {'RETURN_CODE': 0}
    previous_recommendation = NONE
    current_recommendation = NONE
    next_recommendation = NONE
    previous_date = None
    current_date = None
    next_date = None

    if previous_record:
        previous_recommendation = previous_record.BuySellRecommend
        previous_date = previous_record.UpdDate

    if current_record:
        current_recommendation = current_record.BuySellRecommend
        current_date = current_record.UpdDate

    if next_record:
        next_recommendation = next_record.BuySellRecommend
        next_date = next_record.UpdDate

    message = {
        'Previous': {
            'BuySellRecommend': SHRT_LNG_MAPNG[previous_recommendation],
            'Date': previous_date
        },
        'Current': {
            'BuySellRecommend': SHRT_LNG_MAPNG[current_recommendation],
            'Date': current_date
        },
        'Next': {
            'BuySellRecommend': SHRT_LNG_MAPNG[next_recommendation],
            'Date': next_date
        }
    }

    print(message)
    return jsonify(message)
    

@app.route('/getProposedFund/<id>',methods=['GET'])
def get_proposed_fund(id):
    PrintOnConsole('-----------get_proposed_fund---------------')
    UsrObj=db.session.query(User).get(int(id))
    PrintOnConsole('UsrObj.userEmail:'+UsrObj.userEmail)
    ProposedFundObj=db.session.query(ProposedFundBuySellAction).filter_by(Email=UsrObj.userEmail).all()
    print(ProposedFundObj)
    data=proposed_schema.jsonify(None)
    if(ProposedFundObj):
        data=proposed_schema.jsonify(ProposedFundObj)
        data.headers.add('Access-Control-Allow-Origin', '*')
        PrintOnConsole(data.get_data(as_text=True))
    return data

@app.route('/getPortfolio/<id>',methods=['GET'])
def get_portfolio(id):
    PrintOnConsole('-----------get_porfolio---------------')
    UsrObj=db.session.query(User).get(int(id))
    PrintOnConsole('UsrObj.userEmail:'+UsrObj.userEmail)
    HoldingObj=db.session.query(Holdings).filter_by(Email=UsrObj.userEmail).all()
    print(HoldingObj)
    data=holding_schema.jsonify(None)
    if(HoldingObj):
        data=holding_schema.jsonify(HoldingObj)
        data.headers.add('Access-Control-Allow-Origin', '*')
        PrintOnConsole(data.get_data(as_text=True))
    return data
    
@app.route('/getFund/<id>',methods=['GET'])
def get_fund(id):
    PrintOnConsole('-----------get_fund---------------')
    UsrObj=db.session.query(User).get(int(id))
    FundsObj=db.session.query(Funds).filter_by(Email=UsrObj.userEmail).all()
    data=fund_schema.jsonify(None)
    if(FundsObj):
        data=fund_schema.jsonify(FundsObj[0])
        data.headers.add('Access-Control-Allow-Origin', '*')
        PrintOnConsole(data.get_data(as_text=True))
    return data

@app.route('/addFund',methods=['POST'])
def add_fund():
    PrintOnConsole('------------ADD FUND---------------')
    print(request.get_json())
    Email=request.json['Email']
    totalFund=request.json['totalFund']
    allocatedFund=request.json['allocatedFund']
    unusedFund=request.json['unusedFund']
    MFPer=float(request.json['MFPer'])
    EQPer=float(request.json['EQPer'])
    CMPer=float(request.json['CMPer'])
    OPPer=float(request.json['OPPer'])
    fund=Funds(Email,totalFund,allocatedFund,unusedFund,MFPer,EQPer,CMPer,OPPer)
    db.session.add(fund)
    db.session.commit()
    data=fund_schema.jsonify(fund)
    data.headers.add('Access-Control-Allow-Origin', '*')
    PrintOnConsole(data.get_data(as_text=True))
    return data

@app.route('/updFund',methods=['PUT'])
def upd_fund():
    PrintOnConsole('------------UPD FUND---------------')
    print(request.get_json())
    Email=request.json['Email']
    FundsObj=db.session.query(Funds).filter_by(Email=Email).all()
    fund=FundsObj[0]
    fund.totalFund=request.json['totalFund']
    fund.allocatedFund=request.json['allocatedFund']
    fund.unusedFund=request.json['unusedFund']
    db.session.commit()
    data=fund_schema.jsonify(fund)
    data.headers.add('Access-Control-Allow-Origin', '*')
    PrintOnConsole(data.get_data(as_text=True))
    return data

@app.route('/register',methods=['POST'])
def register_user():
    PrintOnConsole('------------Register---------------')
    print(request.get_json())
    userName=request.json['name']
    userEmail=request.json['email']
    userPassword=request.json['password']
    userDB=User(userName,userEmail,bcrypt.generate_password_hash (userPassword).decode('utf-8'))
    db.session.add(userDB)
    db.session.commit()
    data=user_schema.jsonify(userDB)
    data.headers.add('Access-Control-Allow-Origin', '*')
    PrintOnConsole(data.get_data(as_text=True))
    return data

@app.route('/login',methods=['POST'])
def login_user():
    PrintOnConsole('------------LOGIN---------------')
    userEmail_F=request.json['email']
    userPassword=request.json['password']
    usrDet=db.session.query(User).filter_by(userEmail=userEmail_F).all()
    RET={'RETURN_CODE':0}
    if(usrDet):
        if(bcrypt.check_password_hash (usrDet[0].userPassword, userPassword) ):
            RET['RETURN_CODE']=usrDet[0].id
    message = {
        'status': 200,
        'message': 'OK',
        'FRM_API': RET
    }
    print(message)
    return jsonify(message) 

@app.route('/inspector/network', methods=['GET'])
def inspector_network():
    print('Network inspector active')
    return {"status": "Network inspector active"}, 200
    
if __name__ == "__main__":
    #app.run(host='10.0.0.4',port='8081',debug=True)
    app.run(host='192.168.56.1',port='8081',debug=True)
    #app.run(debug=True)
