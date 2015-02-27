import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, Text, Date, DateTime, Float, ForeignKey, Index
from sqlalchemy.orm import relationship

from stock_analysis import app
from database import Base, engine, session

#stock model --> create new class for Stock data
class Stock(Base):
	__tablename__ = "stocks"

	#id = Column(Integer, Sequence('s'))
	stock_name = Column(String, nullable=False, primary_key=True)
	date = Column(Date, nullable=False, primary_key=True)
	open_price = Column(Float, nullable=False)
	close_price = Column(Float, nullable=False)
	__table_args__ = (Index('stock_date', "stock_name", "date"), )

Base.metadata.create_all(engine)