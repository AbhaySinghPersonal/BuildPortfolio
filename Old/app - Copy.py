from flask import Flask,jsonify,request,json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import update
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import datetime

uname='APP'
pword='Celsior2024'
server='localhost\SQLEXPRESS'
dbname='Market'
port="1433"
DEBUG=True
LINK='http://localhost:8081'


app=Flask(__name__)
CORS(app)


#app.config['SQLALCHEMY_DATABASE_URI']="mssql+pyodbc://"+uname+":"+pword+"@"+server+":"+port+"/"+dbname+"?driver=ODBC+Driver+17+for+SQL+Server"
#app.config['SQLALCHEMY_DATABASE_URI']="mssql+pyodbc://"+uname+":"+pword+"@"+server+":"+port+"/"+dbname+"?driver=ODBC Driver 17 for SQL Server?trusted_connection=yes"
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
def PrintOnConsole(str):
    if DEBUG:
        print(str)

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


if __name__ == "__main__":
    app.run(host='192.168.56.1',port='8081',debug=True)
    #app.run(debug=True)
