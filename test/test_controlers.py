import time
import unittest

import psycopg2
from flask_testing import TestCase
from sqlalchemy import create_engine
from sqlalchemy.util import b64encode

from api.controlers import app

from models.model import User, Transactions, Wallet,db


def DeleteTable(table_name):

    with psycopg2.connect("host='localhost' dbname='labapptest' user='postgres'   password='1234'") as conn:
        cur=conn.cursor()
        sql="""DROP TABLE """+table_name+""";"""
        cur.execute(sql)
        conn.commit()



engine = create_engine('postgresql://postgres:1234@localhost:5432/labapptest')
class MyTest(TestCase):

    TESTING = True
    QLALCHEMY_DATABASE_URI = "postgresql://postgres:1234@localhost:5432/labapptest"
    WTF_CSRF_ENEBLED=True
    def create_app(self):

        return app

    def setUp(self):

        db.create_all()
        db.session.commit()

        user1 = User(id=1, login="usr", password="$2b$12$O9QaaEl/2bCI8tZ.ovQqL.THW1iJstCE6bfu0yLeXiAEnbmluzMhC", name="Illia")
        user2 = User(id=33, login="login", password="12345", name="NeIllia")
        wallet2 = Wallet(id=32, currency="UAN", money=1000, owner=user2)
        wallet1 = Wallet(id=3, currency="DOLLARS", money=1000000, owner=user1)
        trans = Transactions(id=3, sender=wallet1, receiver=wallet2, sendedmoney=9)
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(wallet1)
        db.session.add(wallet1)
        db.session.add(trans)
        db.session.commit()
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()





class Controlertest(MyTest):

    def test_usergetall(self):
        test = self.client.get("/user")
        self.assertEqual(b'[{"id": 1, "login": "usr", "password": "$2b$12$O9QaaEl/2bCI8tZ.ovQqL.THW1iJstCE6bfu0yLeXiAEnbmluzMhC", "name": "Illia"}, {"id": 33, "login": "login", "password": "12345", "name": "NeIllia"}]\n',test.data)

    def test_userpost(self):
        test = self.client.post("/user",data={"id": 4, "login": "usr", "password": "qwerty", "name": "Illia"})
        print(test.data)
        self.assertEqual(200,test.status_code)

    def test_userput(self):
        test = self.client.put("/user/1",data={ "login": "usre", "password": "qwerty", "name": "Illia"})
        print(test.data)
        self.assertEqual(b'{"id": 1, "login": "usre", "password": "qwerty", "name": "Illia"}\n',test.data)

    def test_usergetid(self):
        test = self.client.get("/user/1")
        self.assertEqual(b'{"id": 1, "login": "usr", "password": "$2b$12$O9QaaEl/2bCI8tZ.ovQqL.THW1iJstCE6bfu0yLeXiAEnbmluzMhC", "name": "Illia"}\n',test.data)


    def test_wrongusergetid(self):
        test = self.client.get("/user/8")
        self.assertEqual(404,test.status_code)

    def test_userdelete(self):
        credentials = b64encode(b"usr:qwerty")
        test = self.client.delete("/user",headers={"Authorization": f"Basic {credentials}"})
        self.assertEqual(200,test.status_code)

    def test_wronguserdelete(self):
        credentials = b64encode(b"usre:qwerty")
        test = self.client.delete("/user",headers={"Authorization": f"Basic {credentials}"})
        self.assertEqual(401,test.status_code)

    def test_walletget(self):
        credentials = b64encode(b"usr:qwerty")
        test = self.client.get("/wallet", headers={"Authorization": f"Basic {credentials}"})
        print(test.data)
        self.assertEqual(b'[{"id": 3, "currency": "DOLLARS", "money": 1000000, "owner_id": 1}]\n', test.data)

    def test_wrongwalletget(self):
        credentials = b64encode(b"usre:qwerty")
        test = self.client.get("/wallet", headers={"Authorization": f"Basic {credentials}"})
        print(test.data)
        self.assertEqual(401,test.status_code)

    def test_walletpost(self):
        credentials = b64encode(b"usr:qwerty")
        test = self.client.post("/wallet", headers={"Authorization": f"Basic {credentials}"},data={"id": 55, "currency": "DOLLARS", "money": 1000000})
        print(test.data)
        self.assertEqual(b'{"id": 55, "currency": "DOLLARS", "money": 1000000, "owner_id": 1}\n', test.data)

    def test_wrongwalletpost(self):
        credentials = b64encode(b"usr:qwerty")
        test = self.client.post("/wallet", headers={"Authorization": f"Basic {credentials}"},
                                data={"id": 3, "currency": "DOLLARS", "money": 1000000})
        print(test.data)
        self.assertEqual(404,test.status_code)

    def test_walletgetid(self):
        credentials = b64encode(b"usr:qwerty")
        test = self.client.get("/wallet/3", headers={"Authorization": f"Basic {credentials}"})
        print(test.data)
        self.assertEqual(b'{"id": 3, "currency": "DOLLARS", "money": 1000000, "owner_id": 1}\n', test.data)

    def test_wrongwalletgetid(self):
        credentials = b64encode(b"usr:qwerty")
        test = self.client.get("/wallet/1", headers={"Authorization": f"Basic {credentials}"})
        print(test.data)
        self.assertEqual(b'{"massage": "Wallet not found "}\n', test.data)

    def test_walletdelete(self):
        credentials = b64encode(b"usr:qwerty")
        test = self.client.delete("/wallet/3",headers={"Authorization": f"Basic {credentials}"})
        print(test.status_code)
        self.assertEqual(200,test.status_code)

    def test_wrongwalletdelete(self):
        credentials = b64encode(b"usr:qwerty")
        test = self.client.delete("/wallet/1",headers={"Authorization": f"Basic {credentials}"})
        print(test.status_code)
        self.assertEqual(404,test.status_code)

    def test_transactionget(self):
        credentials = b64encode(b"usr:qwerty")
        test = self.client.get("/transactions/3", headers={"Authorization": f"Basic {credentials}"})
        print(test.data)
        self.assertEqual(b'[{"id": 3, "sender_id": 3, "receiver_id": 32, "sendedmoney": 9}]\n', test.data)

    def test_wrongtransactionget(self):
        credentials = b64encode(b"usr:qwerty")
        test = self.client.get("/transactions/2", headers={"Authorization": f"Basic {credentials}"})
        print(test.data)
        self.assertEqual(b'{"massage": "Wallet not found "}\n', test.data)

    def test_transactionpost(self):
        credentials = b64encode(b"usr:qwerty")
        test = self.client.post("/transactions/32", headers={"Authorization": f"Basic {credentials}"},data={"id": 311,"sender_id": 3, "sendedmoney": 9})
        print(test.data)
        self.assertEqual(b'{"id": 311, "sender_id": 3, "receiver_id": 32, "sendedmoney": 9}\n', test.data)

    def test_wrongtransactionpost(self):
        credentials = b64encode(b"usr:qwerty")
        test = self.client.post("/transactions/311111", headers={"Authorization": f"Basic {credentials}"},data={"id": 311,"sender_id": 3, "sendedmoney": 9})
        print(test.data)
        self.assertEqual(b'{"massage": "Wallets not found "}\n', test.data)
