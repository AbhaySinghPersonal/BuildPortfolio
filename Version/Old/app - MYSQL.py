from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:'root'@localhost/TestDB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
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

@app.route('/get',methods=['GET'])
def get_article():
    print('-----------get_article hit--------------')
    all_articles=Articles.query.all()
    results=articles_schema.dump(all_articles)
    print('-----------get_article exit --------------'+str(jsonify(results)))
    return jsonify(results)

@app.route('/get/<id>',methods=['GET'])
def post_details(id):
    article=Articles.query.get(id)
    return articles_schema.jsonify(article)

@app.route('/add',methods=['POST'])
def add_articles():
    Title=request.json['Title']
    Body=request.json['Body']
    articles=Articles(Title,Body)
    db.session.add(articles)
    db.session.commit()
    return articles_schema.jsonify(articles)

@app.route('/update/<id>',methods=['PUT'])
def update_aticle(id):
    article=Articles.query.get(id)
    Title=request.json['Title']
    Body=request.json['Body']
    article.Title=Title
    article.Body=Body
    db.session.commit()
    return articles_schema.jsonify(article)

@app.route('/delete/<id>',methods=['DELETE'])
def delete_aticle(id):
    article=Articles.query.get(id)
    db.session.delete(article)
    return articles_schema.jsonify(article)

if __name__ == "__main__":
    app.run(host='192.168.56.1',port='8081',debug=True)