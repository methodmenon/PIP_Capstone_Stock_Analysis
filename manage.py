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

from getpass import getpass
from werkzeug.security import generate_password_hash
from blog.models import User

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
	#stock 7 - Pfizer (PFE)
	url_7 = "https://www.quandl.com/api/v1/datasets/WIKI/PFE"
	#stock 8 - Wells Fargo and Company (WFC)
	url_8 = "https://www.quandl.com/api/v1/datasets/WIKI/WFC"

	#list of stock urls
	#url_list = [url_1, url_2, url_3, url_4, url_5, url_6, url_7, url_8]
	#6 urls seems to work max
	url_list = [url_1, url_2, url_3, url_4, url_5, url_6, url_7, url_8]
	for url in url_list:
		response = requests.get(url)
		stock_data = response.json()
		#print stock_data["data"]
		for entry in stock_data["data"]:
			stock_day = Stock(stock_name=stock_data["code"], date=entry[0],
				open_price=entry[1], close_price=entry[4])
			session.add(stock_day)
		session.commit()

@manager.command
def adduser():
    username = raw_input("username: ")
    password = raw_input("password: ")
    if session.query(User).filter_by(username=username).first():
        print "User with that username already exists"
        return
    password = raw_input("Password: ")
    password_2 = raw_input("Re-enter password: ")
    while not (password and password_2) or password != password_2:
         password = getpass("Password: ")
         password_2 = getpass("Re-enter password: ")
    user = User(username=username, email=password,
        password=generate_password_hash(password))
    """
        generate_password_hash function: 
        1) Function is used to hash our password
        2) Hashing - process that converts our plain text password
                     into a string of characters
        3) Passwords use only One-Way-Hashes: process works in one direction
    """
    session.add(user)
    session.commit()
    
if __name__ == "__main__":
	manager.run()