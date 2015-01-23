import sys
import json
import requests
from authorization import AUTH_TOKEN


def get_stock():
	url = "https://www.quandl.com/api/v1/datasets/WIKI/TSLA.json?auth_token={auth_token}".format(auth_token=AUTH_TOKEN)
	response = requests.get(url)
	return response.json()


def get_stock_fundamentals():
	url = "https://www.quandl.com/api/v1/datasets/SEC/AAPL_SALESREVENUENET_Q.json?auth_token={auth_token}".format(auth_token=AUTH_TOKEN)
	response = requests.get(url)
	return response.json()

def main():
	"""
	stock_data = get_stock()
	for entry in stock_data["data"]:
		print [stock_data["code"], entry[0], entry[1], entry[4]]
	"""
	stock_data = get_stock_fundamentals()
	print stock_data

if __name__ == "__main__":
	main()