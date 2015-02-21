import os.path
import sys
import requests
import json
import mistune
import models
import decorators
import Image
from StringIO import StringIO

from flask import render_template
from flask import send_file

from flask import request, Response, url_for, redirect
from flask import flash 
#from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError
from sqlalchemy import and_, or_, distinct


import models
import decorators
from models import Stock
from authorization import AUTH_TOKEN
from stock_analysis import app
from database import session

from plots import closing_price_graph

@app.route("/")
def main_page():
	return render_template("stock_selection.html")

@app.route("/my_stocks")
def view_my_stocks():
	stocks = session.query(Stock.stock_name).group_by(Stock.stock_name).all()
	return render_template("my_stocks.html", 
		stocks=stocks)

@app.route("/closing_price_graph.html")
#for MSFT at the moment
def stock_closing_price_graph_first():
	graph = closing_price_graph('MSFT')

#@app.route("/closing_price_graph.svg")
@app.route("/closing_price_graph.png")
def msft_stock_closing_price_graph():
	graph = closing_price_graph('MSFT')
	img = StringIO()
	graph.savefig(img)
	img.seek(0)
	#return send_file(img, mimetype='image/svg+xml')
	return send_file(img, mimetype='image/png')

@app.route("/<symbol>/closing_price_graph.png")
def stock_closing_price_graph_png(symbol):
	graph = closing_price_graph(symbol)
	img = StringIO()
	graph.savefig(img)
	img.seek(0)
	return send_file(img, mimetype='image/png')

@app.route("/<symbol>/closing_price_graph.svg")
def stock_closing_price_graph_svg(symbol):
	graph = closing_price_graph(symbol)
	img = StringIO()
	graph.savefig(img)
	img.seek(0)
	return send_file(img, mimetype='image/svg+xml')