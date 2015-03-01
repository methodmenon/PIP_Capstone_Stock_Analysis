import os.path
import sys
import psycopg2
import models
import matplotlib
import matplotlib.pyplot as plt



from flask import render_template
import cStringIO
from models import Stock
from database import session
from stock_analysis import app
from matplotlib.figure import Figure 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def closing_price_graph(stock_symbol, start_date="", end_date=""):
	query = session.query(Stock.date, Stock.close_price).filter(Stock.date > start_date, Stock.date < end_date).filter(Stock.stock_name == stock_symbol).order_by(Stock.date)

	date, close_price = zip(*query.all())

	fig = Figure()
	ax =fig.add_subplot(111)
	x = []
	y = []
	for i in range(len(date)):
		x.append(date[i])
	for i in range(len(close_price)):
		y.append(close_price[i])

	ax.plot(x, y)
	ax.set_ylabel("Closing Price")
	ax.set_xlabel("Date")
	ax.set_title("Closing Price Graph for {}".format(stock_symbol))
	
	canvas = FigureCanvas(fig)
	return canvas
"""
def closing_price_graph(stock_symbol):
	query = session.query(Stock.date, Stock.close_price).filter(Stock.date > '01/01/2000').filter(Stock.stock_name == stock_symbol).order_by(Stock.date)

	date, close_price = zip(*query.all())

	fig = Figure()
	ax =fig.add_subplot(111)
	x = []
	y = []
	for i in range(len(date)):
		x.append(date[i])
	for i in range(len(close_price)):
		y.append(close_price[i])

	ax.plot(x, y)
	ax.set_ylabel("Closing Price")
	ax.set_xlabel("Date")
	ax.set_title("Closing Price Graph for {}".format(stock_symbol))
	
	canvas = FigureCanvas(fig)
	return canvas
	"""

"""
def closing_price_graph_png(stock_symbol, from_year="", to_year="", etc..):
	query = session.query(Stock.date, Stock.close_price).filter(Stock.date > '01/01/1990').filter(Stock.stock_name == stock_symbol).order_by(Stock.date)

	date, close_price = zip(*query.all())

	plt.plot(date, close_price, label=stock_symbol)


	plt.legend(loc='upper left')
	plt.xlabel("Time")
	plt.ylabel("Closing Price")
	return plt
"""

