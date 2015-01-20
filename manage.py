import os
import json
import requests
import sys
from stock_analysis.authorization import AUTH_TOKEN
from flask.ext.script import Manager

from stock_analysis import app
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
	url = "https://www.quandl.com/api/v1/datasets/WIKI/TSLA.json?auth_token={auth_token}".format(auth_token=AUTH_TOKEN)
	response = requests.get(url)
	stock_data = json.dumps(response.json(), indent=4)
	print stock_data.data
	"""
	for entry in stock_data["data"]:
		stock_day = models.Stock(stock_name=stock_data["code"], date=entry[0],
			open_price=entry[1], close_price=entry[4])
		session.add(stock_day)
	session.commit()
	"""

if __name__ == "__main__":
	manager.run()