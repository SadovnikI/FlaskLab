from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

from api.argsparsers import user_args, user_args_optional, wallet_args, wallet_temp_user_id, transaction_temp
from api.serializers import user_serializer, wallet_serializer, transaction_serializer
from models.model import User, Wallet, Transactions

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3306/labapp'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()

class UserApi(Resource):
    @marshal_with(user_serializer)
    def get(self):
        user = User.query.all()
        if user == None:
            abort(404, massage="Users not found ")
        return user


    @marshal_with(user_serializer)
    def post(self):
        args = user_args.parse_args()
        user = User(id=args['id'], login=args['login'], password=bcrypt.generate_password_hash(args['password']), name=args['name'])
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return abort(404, massage="Invalid user credentials")
        return user, 200


class UserIdApi(Resource):
    @marshal_with(user_serializer)
    def put(self, user_id):
        args = user_args_optional.parse_args()
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            abort(404, massage="Invalid id ")
        if "login" in args:
            user.login = args["login"]
        if "password" in args:
            user.password = args["password"]
        if "name" in args:
            user.name = args["name"]
        else:
            user.name = user.name
        db.session.add(user)
        db.session.commit()
        return user

    @marshal_with(user_serializer)
    def get(self, user_id):
        user = User.query.get(ident=user_id)
        if user == None:
            abort(404, massage="Users not found ")
        return user

    @auth.login_required
    def delete(self, user_id):
        user = db.session.query(User).filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return 200


class WalletApi(Resource):
    @auth.login_required
    @marshal_with(wallet_serializer)
    def post(self):
        args = wallet_args.parse_args()
        wallet = Wallet(id=args['id'], currency=args['currency'], money=args['money'], owner_id=args['owner_id'])
        try:
            db.session.add(wallet)
            db.session.commit()
        except:
            return abort(404, massage="Invalid wallet credentials")
        return wallet

    @auth.login_required
    @marshal_with(wallet_serializer)
    def get(self):
        args = wallet_temp_user_id.parse_args()
        wallets = db.session.query(Wallet).filter_by(owner_id=args['owner_id']).all()
        if wallets == None:
            abort(404, massage="Wallets not found ")
        return wallets


class WalletIdApi(Resource):
    @auth.login_required
    @marshal_with(wallet_serializer)
    def get(self, wallet_id):
        wallet = Wallet.query.get(ident=wallet_id)
        if wallet == None:
            abort(404, massage="Wallet not found ")
        return wallet

    @auth.login_required
    def delete(self, wallet_id):
        wallet = db.session.query(Wallet).filter_by(id=wallet_id).first()
        if wallet == None:
            abort(404, massage="Wallet not found ")
        db.session.delete(wallet)
        db.session.commit()
        return 200


class TransactionApi(Resource):
    @auth.login_required
    @marshal_with(transaction_serializer)
    def get(self, wallet_id):
        transactions = db.session.query(Transactions).filter_by(sender_id=wallet_id).all()
        if transactions == None:
            abort(404, massage="Transactions not found ")
        return transactions

    @auth.login_required
    @marshal_with(transaction_serializer)
    def post(self, wallet_id):
        receiver_id = wallet_id
        args = transaction_temp.parse_args()
        transaction = Transactions(id=args['id'], sender_id=args['sender_id'], receiver_id=receiver_id,
                                   sendedmoney=args['sendedmoney'])

        sender = db.session.query(Wallet).filter_by(id=args['sender_id']).first()
        receiver = db.session.query(Wallet).filter_by(id=receiver_id).first()

        if (sender.money - args['sendedmoney'] < 0):
            abort(404, massage="Not enough money")
        else:
            sender.money -= args['sendedmoney']
            receiver.money += args['sendedmoney']
        try:
            db.session.add(sender)
            db.session.add(receiver)
            db.session.add(transaction)
            db.session.commit()
        except:
            return abort(404, massage="Invalid transaction credentials")
        return transaction
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(login=username)
    if username not None and bcrypt.check_password_hash(user.password, password):
         return username

api.add_resource(UserApi, "/user")
api.add_resource(UserIdApi, "/user/<string:user_id>")
api.add_resource(WalletApi, "/wallet")
api.add_resource(WalletIdApi, "/wallet/<string:wallet_id>")
api.add_resource(TransactionApi, "/transactions/<string:wallet_id>")

if __name__ == "__main__":
    app.run(debug=True)
