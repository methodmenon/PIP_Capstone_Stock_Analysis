import os
import json
import requests
import sys
from stock_analysis.authorization import AUTH_TOKEN
from flask.ext.script import Manager

from stock_analysis import app
#from stock_analysis import models
from stock_analysis.models import Stock
from stock_analysis.database import session

manager = Manager(app)

@manager.command
def run():
	port = int(os.environ.get('PORT', 8080))
	app.run(host='0.0.0.0', port=port)

@manager.command
def seed():
	"""
	command for adding stock data from a single stock using Quandl data
	"""
	#url = "https://www.quandl.com/api/v1/datasets/WIKI/TSLA.json?auth_token={auth_token}".format(auth_token=AUTH_TOKEN)
	#stock 1 - TESLA (TSLA)
	url_1 = "https://www.quandl.com/api/v1/datasets/WIKI/TSLA.json"
	#stock 2 - Microsoft (MSFT)
	url_2 = "https://www.quandl.com/api/v1/datasets/WIKI/MSFT"
	#stock 3 - Boeing (BA)
	url_3 = "https://www.quandl.com/api/v1/datasets/WIKI/BA"
	#stock 4 - Netflix (NFLX)
	url_4 = "https://www.quandl.com/api/v1/datasets/WIKI/NFLX"
	#stock 5 - Exxon (XOM)
	url_5 = "https://www.quandl.com/api/v1/datasets/WIKI/XOM"
	#stock 6 - Kraft (KRFT)
	url_6 = "https://www.quandl.com/api/v1/datasets/WIKI/KRFT"
	#stock 7 - GlaxoSmithKline (GSK)
	url_7 = "https://www.quandl.com/api/v1/datasets/WIKI/GSK"
	#stock 8 - Wells Fargo and Company (WFC)
	url_8 = "https://www.quandl.com/api/v1/datasets/WIKI/WFC"

	#list of stock urls
	#url_list = [url_1, url_2, url_3, url_4, url_5, url_6, url_7, url_8]
	#6 urls seems to work max
	url_list = [url_1, url_2, url_3, url_4, url_5, url_6]
	for url in url_list:
		response = requests.get(url)
		stock_data = response.json()
		#print stock_data["data"]
		for entry in stock_data["data"]:
			stock_day = Stock(stock_name=stock_data["code"], date=entry[0],
				open_price=entry[1], close_price=entry[4])
			session.add(stock_day)
		session.commit()

if __name__ == "__main__":
	manager.run()