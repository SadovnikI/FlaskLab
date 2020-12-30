import copy

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

from api.argsparsers import user_args, user_args_optional, wallet_args,  transaction_temp
from api.serializers import user_serializer, wallet_serializer, transaction_serializer
from models.model import User, Wallet, Transactions

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost:5432/labapptest"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()


def create_app(config_filename):
    app = Flask(__name__)
    db.init_app(app)
    return app

class UserApi(Resource):
    @marshal_with(user_serializer)
    def get(self):
        user = User.query.all()
        if user == None:
            db.session.close()
            abort(404, massage="Users not found ")
        return user

    @marshal_with(user_serializer)
    def post(self):
        args = user_args.parse_args()
        user = User(id=args['id'], login=args['login'], password=bcrypt.generate_password_hash(args['password']).decode('utf8'),
                    name=args['name'])
        cop = copy.deepcopy(user)
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return cop, 200

    @auth.login_required
    def delete(self):
        users = User.query.filter_by(login=auth.username()).first()
        user = db.session.query(User).filter_by(id=users.id).first()
        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return 200


class UserIdApi(Resource):
    @marshal_with(user_serializer)
    def put(self, user_id):
        args = user_args_optional.parse_args()
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            db.session.close()
            abort(404, massage="Invalid id ")
        if "login" in args:
            user.login = args["login"]
        if "password" in args:
            user.password = args["password"]
        if "name" in args:
            user.name = args["name"]
        else:
            user.name = user.name
        cop = copy.deepcopy(user)
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return cop

    @marshal_with(user_serializer)
    def get(self, user_id):
        user = User.query.get(ident=user_id)
        if user == None:
            abort(404, massage="Users not found ")
        return user

class WalletApi(Resource):
    @auth.login_required
    @marshal_with(wallet_serializer)
    def post(self):
        args = wallet_args.parse_args()
        users = User.query.filter_by(login=auth.username()).first()
        wallet = Wallet(id=args['id'], currency=args['currency'], money=args['money'], owner_id=users.id)
        cop =copy.deepcopy(wallet)
        try:
            db.session.add(wallet)
            db.session.commit()
        except:
            db.session.close()
            return abort(404, massage="Invalid wallet credentials")
        db.session.close()
        return cop

    @auth.login_required
    @marshal_with(wallet_serializer)
    def get(self):
        users = User.query.filter_by(login=auth.username()).first()
        wallets = db.session.query(Wallet).filter_by(owner_id=users.id).all()
        if wallets == None:
            db.session.close()
            abort(404, massage="Wallets not found ")
        db.session.close()
        return wallets

class WalletIdApi(Resource):
    @auth.login_required
    @marshal_with(wallet_serializer)
    def get(self, wallet_id):
        users = User.query.filter_by(login=auth.username()).first()
        wallets = db.session.query(Wallet).filter_by(owner_id=users.id).all()
        wallet=None
        if wallets == None:
            db.session.close()
            abort(404, massage="Wallets not found ")

        for w in wallets:
            if str(w.id) == str(wallet_id):
                wallet=w
        if wallet == None:
            db.session.close()
            abort(404, massage="Wallet not found ")
        db.session.close()
        return wallet

    @auth.login_required
    def delete(self, wallet_id):
        users = User.query.filter_by(login=auth.username()).first()
        wallets = db.session.query(Wallet).filter_by(owner_id=users.id).all()
        wallet = None
        if wallets == None:
            db.session.close()
            abort(404, massage="Wallets not found ")

        for w in wallets:
            if str(w.id) == str(wallet_id):
                wallet = w
        if wallet == None:
            db.session.close()
            abort(404, massage="Wallet not found ")
        db.session.delete(wallet)
        db.session.commit()
        db.session.close()
        return 200


class TransactionApi(Resource):
    @auth.login_required
    @marshal_with(transaction_serializer)
    def get(self, wallet_id):
        users = User.query.filter_by(login=auth.username()).first()
        wallets = db.session.query(Wallet).filter_by(owner_id=users.id).all()
        wallet = None
        if wallets == None:
            db.session.close()
            abort(404, massage="Wallets not found ")

        for w in wallets:
            if str(w.id) == str(wallet_id):
                wallet = w
        if wallet == None:
            db.session.close()
            abort(404, massage="Wallet not found ")
        transactions = db.session.query(Transactions).filter_by(sender_id=wallet.id).all()
        if transactions == None:
            db.session.close()
            abort(404, massage="Transactions not found ")
        db.session.close()
        return transactions

    @auth.login_required
    @marshal_with(transaction_serializer)
    def post(self, wallet_id):
        receiver_id = wallet_id
        if receiver_id == None:
            db.session.close()
            abort(404, massage="Wallets not found ")
        args = transaction_temp.parse_args()
        users = User.query.filter_by(login=auth.username()).first()
        wallets = db.session.query(Wallet).filter_by(owner_id=users.id).all()
        wallet = None
        if wallets == None:
            db.session.close()
            abort(404, massage="Wallets not found ")

        for w in wallets:
            if str(w.id) == str(args['sender_id']):
                wallet = w
        if wallet == None:
            db.session.close()
            abort(404, massage="Wallet not found ")
        transaction = Transactions(id=args['id'], sender_id=wallet.id, receiver_id=receiver_id,
                                   sendedmoney=args['sendedmoney'])
        cop = copy.deepcopy(transaction)
        sender = db.session.query(Wallet).filter_by(id=wallet.id).first()
        receiver = db.session.query(Wallet).filter_by(id=receiver_id).first()
        if receiver == None:
            db.session.close()
            abort(404, massage="Wallets not found ")
        if sender == None:
            db.session.close()
            abort(404, massage="Wallets not found ")

        if (sender.money - args['sendedmoney'] < 0):
            db.session.close()
            abort(404, massage="Not enough money")
        else:
            sender.money -= args['sendedmoney']
            receiver.money += args['sendedmoney']

        db.session.add(sender)
        db.session.add(receiver)
        db.session.add(transaction)
        db.session.commit()

        db.session.close()
        return cop
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(login=username).first()
    if username != None :
        if user !=None:
            if bcrypt.check_password_hash(user.password,password):
                return username
api.add_resource(UserApi, "/user")
api.add_resource(UserIdApi, "/user/<string:user_id>")
api.add_resource(WalletApi, "/wallet")
api.add_resource(WalletIdApi, "/wallet/<string:wallet_id>")
api.add_resource(TransactionApi, "/transactions/<string:wallet_id>")

if __name__ == "__main__":
    app.run(debug=True)
