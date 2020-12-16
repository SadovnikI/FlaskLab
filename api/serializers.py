from flask_restful import fields

user_serializer = {
    'id': fields.Integer,
    'login': fields.String,
    'password': fields.String(200),
    'name': fields.String
}

wallet_serializer = {
    'id': fields.Integer,
    'currency': fields.String,
    'money': fields.Integer,
    'owner_id': fields.Integer
}
transaction_serializer = {
    'id': fields.Integer,
    'sender_id': fields.Integer,
    'receiver_id': fields.Integer,
    'sendedmoney': fields.Integer
}
