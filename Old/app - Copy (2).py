from flask import jsonify,request
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

    def __init__(self,id,userName,userEmail,userAge,userAddress,userPassword,userLastPassword,userIsActive,UpdDate):
        self.id=id
        self.userName=userName
        self.userEmail=userEmail
        self.userAge=userAge
        self.userAddress=userAddress
        self.userPassword=userPassword
        self.userLastPassword=userLastPassword
        self.userIsActive=userIsActive
        self.UpdDate=UpdDate
    

class UserSchema(ma.Schema):
    class Meta:
        fields=('id','userName','userEmail','userAge','userAddress','userPassword','userLastPassword','userIsActive','UpdDate')

user_schema=UserSchema()
users_schema=UserSchema(many=True)


def PrintOnConsole(str):
    if DEBUG:
        print(str)

@app.route('/register',methods=['POST'])
def register_user():
    PrintOnConsole('------------ADD---------------')
    print(request.get_json())
    userName=request.json['name']
    userEmail=request.json['email']
    userAge=int(request.json['age'])
    userAddress=request.json['address']
    userPassword=request.json['password']

    userDB=User(1,userName,userEmail,userAge,userAddress,userPassword,"","A","1-1-2024")
    db.session.add(userDB)
    db.session.commit()
    data=user_schema.jsonify(userDB)
    data.headers.add('Access-Control-Allow-Origin', '*')
    PrintOnConsole(data.get_data(as_text=True))
    return data

"""

@app.route('/get',methods=['GET'])
def get_article():
    PrintOnConsole('-----------get_article hit-------Upd-------')
    all_articles=Articles.query.all()
    results=articles_schema.dump(all_articles)
    data=jsonify(results)
    data.headers.add('Access-Control-Allow-Origin', '*')
    PrintOnConsole(data.get_data(as_text=True))
    return data
    #return data.get_data(as_text=True)

@app.route('/get/<id>',methods=['GET'])
def post_details(id):
    PrintOnConsole('-----------Post hit--------------'+id)
    article=db.session.query(Articles).get(int(id))
    data=article_schema.jsonify(article)
    data.headers.add('Access-Control-Allow-Origin', '*')
    PrintOnConsole(data.get_data(as_text=True))
    return data


@app.route('/add',methods=['POST'])
def add_articles():
    PrintOnConsole('------------ADD---------------')
    print(request.get_json())
    Title=request.json['Title']
    Body=request.json['Body']
    article=Articles(Title,Body)
    db.session.add(article)
    db.session.commit()
    data=article_schema.jsonify(article)
    data.headers.add('Access-Control-Allow-Origin', '*')
    PrintOnConsole(data.get_data(as_text=True))
    return data

@app.route('/update/<id>',methods=['PUT'])
def update_aticle(id):
    PrintOnConsole('------------UPDATED---------------')
    article=Articles.query.get(id)
    Title=request.json['Title']
    Body=request.json['Body']
    article.Title=Title
    article.Body=Body
    db.session.commit()
    data=article_schema.jsonify(article)
    data.headers.add('Access-Control-Allow-Origin', '*')
    PrintOnConsole(data.get_data(as_text=True))
    return data


@app.route('/delete/<id>', methods=['POST'])
def delete_article(id):
    print('------------DELETE---------------')
    # Query the article by ID
    article = Articles.query.get(id)
    
    # Handle case where the article is not found
    if not article:
        print('--------not article------')
        return jsonify({'error': 'Article not found'})
    
    try:
        # Delete the article
        db.session.delete(article)
        db.session.commit()

        # Return a success response
        return jsonify({'message': 'Article deleted successfully'})
    except Exception as e:
        # Handle any database errors
        print(f"Error deleting article: {e}")
        return jsonify({'error': 'Failed to delete article'})

"""
if __name__ == "__main__":
    app.run(host='192.168.56.1',port='8081',debug=True)
    #app.run(debug=True)
