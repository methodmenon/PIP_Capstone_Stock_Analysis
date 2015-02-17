import os.path
import sys
import psycopg2
import models
import matplotlib
matplotlib.use('SVG')
import matplotlib.pyplot as plt

from flask import render_template
#from sqlalchemy import and_, or_, distinct, group_by, text
from models import Stock
from database import session
from stock_analysis import app

def closing_price_graph(stock_symbol):
	"""
	query = session.query(Stock).from_statement(
		text("SELECT date, close_price 
			FROM stocks WHERE stock_name = stock_symbol
			AND date > '01/01/2000'
			ORDER BY date "))
	"""
	query = session.query(Stock.date, Stock.close_price).filter(Stock.date > '01/01/200').filter(Stock.stock_name == stock_symbol).order_by(Stock.date)

	date, close_price = zip(*query.all())

	plt.plot(date, close_price, label=stock_symbol)


	plt.legend(loc='upper left')
	plt.xlabel("Time")
	plt.ylabel("Closing Price")
	return plt

