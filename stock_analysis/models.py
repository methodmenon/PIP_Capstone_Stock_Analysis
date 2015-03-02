import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, Text, Date, DateTime, Float, ForeignKey, Index
from sqlalchemy.orm import relationship

from stock_analysis import app
from database import Base, engine, session

from flask.ext.login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

#stock model --> create new class for Stock data
class Stock(Base):
	__tablename__ = "stocks"

	#id = Column(Integer, Sequence('s'))
	stock_name = Column(String, nullable=False, primary_key=True)
	date = Column(Date, nullable=False, primary_key=True)
	open_price = Column(Float, nullable=False)
	close_price = Column(Float, nullable=False)
	#user_id = Column(Integer, ForeignKey('users.id'))

	#allows program to find data easier (especially for large databases)
	__table_args__ = (Index('stock_date', "stock_name", "date"), )

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, Sequence("user_id_sequence"), primary_key=True)
	username = Column(String(128))
	password = Column(String(128))
	#user_stock = relationship("Stock", backref="stock")

	def __repr__(self):
		return '<User %r>' %self.username

Base.metadata.create_all(engine)