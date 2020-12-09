from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.model import User, Wallet, Transactions

engine = create_engine('mysql+mysqldb://root:1234@localhost:3306/labapp')
Session = sessionmaker(bind=engine)
session = Session()

user1 = User(id=1, login="usr", password="qwerty", name="Illia")
user2 = User(id=33, login="login", password="12345", name="NeIllia")
wallet1 = Wallet(id=32, currency="UAN", money=10, owner=user2)
wallet2 = Wallet(id=3, currency="DOLLARS", money=1000000, owner=user1)
wallet2 = Wallet(id=43, currency="DOLLARS", money=100, owner=user2)
trans=Transactions(id=3,sender=wallet1,receiver=wallet2,sendedmoney=9)

session.add(user1)
session.add(user2)
session.add(wallet1)
session.add(wallet1)
session.add(trans)
session.commit()
