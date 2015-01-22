import sys
import json
import requests
from authorization import AUTH_TOKEN


def get_stock():
	url = "https://www.quandl.com/api/v1/datasets/WIKI/TSLA.json?auth_token={auth_token}".format(auth_token=AUTH_TOKEN)
	response = requests.get(url)
	return response.json()


def get_metadata():
	url = "https://www.quandl.com/api/v1/datasets/WIKI/TSLA.json?exclude_data=true"
	response = requests.get(url)
	return response.json()

def get_data_column():
	url = "https://www.quandl.com/api/v1/datasets/WIKI/TSLA.json?auth_token={auth_token}".format(auth_token=AUTH_TOKEN)
	response = requests.get(url)
	data = response.json()
	return data['Open']

def main():
	stock_data = get_stock()
	for entry in stock_data["data"]:
		print [stock_data["code"], entry[0], entry[1], entry[4]]
	#meta_data = get_metadata()
	#print meta_data
	#open_data = get_data_column()
	#print open_data

if __name__ == "__main__":
	main()