from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, String, Integer, ForeignKey, orm, create_engine
# from sqlalchemy.ext.declarative import declarative_base

# engine= create_engine(BD_URI)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3306/labapp'
db = SQLAlchemy(app)



# server_default=text("CURRENT_TIMESTAMP"))

class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String)
    password = db.Column(db.String(200))
    name = db.Column(db.String)


class Wallet(db.Model):
    __tablename__ = 'Wallet'

    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String)
    money = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id))
    owner = db.relationship(User, backref="Wallet", lazy="joined")


class Transactions(db.Model):
    __tablename__ = 'Transactions'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey(Wallet.id))
    receiver_id = db.Column(db.Integer, db.ForeignKey(Wallet.id))
    sendedmoney = db.Column(db.Integer)
    sender = db.relationship(Wallet, foreign_keys=[sender_id], backref="sender", lazy="joined")
    receiver = db.relationship(Wallet, foreign_keys=[receiver_id], backref="resever", lazy="joined")
