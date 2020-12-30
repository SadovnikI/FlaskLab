from flask_restful import reqparse

user_args = reqparse.RequestParser()
user_args.add_argument("id", type=str, help="Id is invalid", required=True)
user_args.add_argument("login", type=str, help="Login is invalid", required=True)
user_args.add_argument("password", type=str, help="Password is invalid", required=True)
user_args.add_argument("name", type=str, help="Name is invalid", required=True)

user_args_optional = reqparse.RequestParser()
user_args_optional.add_argument("login", type=str, help="Login is invalid")
user_args_optional.add_argument("password", type=str, help="Password is invalid")
user_args_optional.add_argument("name", type=str, help="Name is invalid")

wallet_args = reqparse.RequestParser()
wallet_args.add_argument("id", type=str, help="Id is invalid", required=True)
wallet_args.add_argument("currency", type=str, help="Currency is invalid", required=True)
wallet_args.add_argument("money", type=int, help="Money is invalid", required=True)


transaction_temp = reqparse.RequestParser()
transaction_temp.add_argument("id", type=str, help="Id is invalid", required=True)
transaction_temp.add_argument("sender_id", type=str, help="Sender id is invalid", required=True)
transaction_temp.add_argument("sendedmoney", type=int, help="Money is invalid", required=True)
