import os.path
import sys
import requests
import json
import mistune
import models
import decorators
import Image
import cStringIO #more efficient version of StringIO module
import StringIO
import mistune

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure 
from flask import Flask
from flask import render_template
from flask import send_file

from flask import request, Response, url_for, redirect, make_response
from flask import flash 
from jsonschema import validate, ValidationError
from sqlalchemy import and_, or_, distinct


import models
import decorators
from models import Stock
from authorization import AUTH_TOKEN
from stock_analysis import app
from database import session


from plots import closing_price_graph

@app.route("/stock/add", methods=["GET"])
def stock_add_get():
	return render_template("stock_selection.html")

@app.route("/stock/add", methods=["POST"])
def stock_add_post():
	print("Hello")
	symbol = request.form["add_stock"]
	print symbol

	url ="https://www.quandl.com/api/v1/datasets/WIKI/{}".format(symbol)
	response = requests.get(url)

	stock_data = response.json()
	for entry in stock_data["data"]:
		stock_day = Stock(stock_name=stock_data["code"], date=entry[0],
			open_price=entry[1], close_price=entry[4])
		session.add(stock_day)
	session.commit()
	stocks = session.query(Stock.stock_name).group_by(Stock.stock_name).all()
	return redirect(url_for('my_stocks'))


@app.route("/my_stocks")
def my_stocks():
	stocks = session.query(Stock.stock_name).group_by(Stock.stock_name).all()
	return render_template("my_stocks.html", 
		stocks=stocks)

@app.route("/<symbol>/closing_price_graph.svg")
def stock_closing_price_graph_svg(symbol):
	canvas_svg = closing_price_graph(symbol)
	svg_img = cStringIO.StringIO()
	canvas_svg.print_svg(svg_img)
	response = make_response(svg_img.getvalue())
	response.headers['Content-Type'] = 'image/svg+xml'
	return response

@app.route("/<symbol>/closing_price_graph.png")
def stock_closing_price_graph_png(symbol):
	canvas_png = closing_price_graph(symbol)
	png_img = cStringIO.StringIO()
	canvas_png.print_png(png_img)
	response = make_response(png_img.getvalue())
	response.headers['Content-Type'] = 'image/png'
	return response