from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import update
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import datetime
from MarketConfig import uname,	pword,	server,	dbname,	port,	DEBUG,	LINK


app=Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# Python 3.x
import urllib
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER="+server+";DATABASE="+dbname+";UID="+uname+";PWD="+pword+";Trusted_Connection=yes;")
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
db=SQLAlchemy(app)
ma=Marshmallow(app)
class Articles(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(100))
    Body=db.Column(db.Text())
    Date=db.Column(db.DateTime,default=datetime.datetime.now)

    def __init__(self,Title,Body):
        self.Title=Title
        self.Body=Body

class ArticleSchema(ma.Schema):
    class Meta:
        fields=('id','Title','Body','Date')

article_schema=ArticleSchema()
articles_schema=ArticleSchema(many=True)


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    userName=db.Column(db.String(32))
    userEmail=db.Column(db.String(32),primary_key=True)
    userAge=db.Column(db.Integer)
    userAddress=db.Column(db.String(128))
    userPassword=db.Column(db.String(256))
    userLastPassword=db.Column(db.String(256))
    userIsActive=db.Column(db.String(1)) 
    UpdDate=db.Column(db.DateTime,default=datetime.datetime.now)

    def __init__(self,userName,userEmail,userAge,userAddress,userPassword):
        self.userName=userName
        self.userEmail=userEmail
        self.userAge=userAge
        self.userAddress=userAddress
        self.userPassword=userPassword
    

class UserSchema(ma.Schema):
    class Meta:
        fields=('id','userName','userEmail','userAge','userAddress','userPassword','userLastPassword','userIsActive','UpdDate')

user_schema=UserSchema()
users_schema=UserSchema(many=True)

