import os.path
import sys
import psycopg2
import models
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import render_template
from models import Stock
from database import session
from stock_analysis import app

def closing_price_graph_png(stock_symbol):
	query = session.query(Stock.date, Stock.close_price).filter(Stock.date > '01/01/1990').filter(Stock.stock_name == stock_symbol).order_by(Stock.date)

	date, close_price = zip(*query.all())

	plt.plot(date, close_price, label=stock_symbol)


	plt.legend(loc='upper left')
	plt.xlabel("Time")
	plt.ylabel("Closing Price")
	return plt

"""
def closing_price_graph_png(stock_symbol, from_year="", to_year="", etc..):
	query = session.query(Stock.date, Stock.close_price).filter(Stock.date > '01/01/1990').filter(Stock.stock_name == stock_symbol).order_by(Stock.date)

	date, close_price = zip(*query.all())

	plt.plot(date, close_price, label=stock_symbol)


	plt.legend(loc='upper left')
	plt.xlabel("Time")
	plt.ylabel("Closing Price")
	return plt"""