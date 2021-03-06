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
import matplotlib
import datetime
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure 
from flask import Flask
from flask import render_template
from flask import send_file
from datetime import datetime

from flask import request, Response, url_for, redirect, make_response, flash
from jsonschema import validate, ValidationError
from sqlalchemy import and_, or_, distinct

from flask.ext.wtf import Form 
from wtforms.fields import DateField, RadioField, SelectField, StringField, SubmitField, PasswordField
from wtforms.validators import Required


import models
import decorators
from models import Stock
from authorization import AUTH_TOKEN
from stock_analysis import app
from database import session

from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from models import User


from plots import closing_price_graph

@app.route("/login", methods=["GET"])
def login_get():
	return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
	username = request.form["username"]
	password = request.form["password"]

	user = session.query(User).filter_by(username=username).first()
	#keep u lower case because it is for current user
	if not user or not check_password_hash(user.password, password):
		#flash function used to store a message which can be used when we render the next page
		flash("Incorrect username or password", "danger")
		#redirect user back to the login
		return redirect(url_for("login_get"))

	login_user(user)

	return redirect(request.args.get('next') or url_for("my_stocks"))


@app.route("/stock_add", methods=["GET"])
def stock_add_get():
	return render_template("stock_selection.html")

@app.route("/stock_add", methods=["POST"])
def stock_add_post():
	symbol = request.form["add_stock"]

	url ="https://www.quandl.com/api/v1/datasets/WIKI/{}".format(symbol)
	response = requests.get(url)

	stock_data = response.json()
	for entry in stock_data["data"]:
		stock_day = Stock(stock_name=stock_data["code"], date=entry[0],
			open_price=entry[1], close_price=entry[4])
		current_user.user_stock.append(stock_day)
		session.add(User.user_stock)
	session.commit()
	stocks = session.query(Stock.stock_name).group_by(Stock.stock_name).all()
	return redirect(url_for('my_stocks'))


@app.route("/")
def my_stocks():
	stocks = session.query(Stock.stock_name).group_by(Stock.stock_name).all()
	return render_template("my_stocks.html", 
		stocks=stocks)

@app.route("/", methods=["GET"])
def stock_closing_price_graph_get():
	return render_template("my_stocks.html", stocks=stocks)

@app.route("/", methods=["POST"])
def stock_closing_price_graph_post():
	symbol = request.form["stock"]
	print (symbol)
	start_date = request.form["start_date"]
	##convert str into datetime object and use datetime.strptime to convert the string into a datetime object
	start_date = datetime.strptime(start_date, "%Y-%m-%d")
	#use datetime.strftime to convert the datetime object into a string in the specified format
	start_date = start_date.strftime("%m/%d/%Y").decode('utf8')
	print (start_date)
	end_date = request.form["end_date"]
	end_date = datetime.strptime(end_date, "%Y-%m-%d")
	end_date = end_date.strftime("%m/%d/%Y").decode('utf8')
	print (end_date)
	#return redirect(url_for("stock_closing_price_graph_svg", symbol=symbol, start_date=start_date, end_date=end_date))
	canvas_svg = closing_price_graph(symbol, start_date, end_date)
	svg_img = cStringIO.StringIO()
	canvas_svg.print_svg(svg_img)
	response = make_response(svg_img.getvalue())
	response.headers['Content-Type'] = 'image/svg+xml'
	return response
"""
@app.route("/<symbol>/closing_price_graph.svg", methods=["GET", "POST"])
def stock_closing_price_graph_svg(symbol, start_date, end_date):
	print symbol
	print start_date
	print end_date
	canvas_svg = closing_price_graph(symbol)
	svg_img = cStringIO.StringIO()
	canvas_svg.print_svg(svg_img)
	response = make_response(svg_img.getvalue())
	response.headers['Content-Type'] = 'image/svg+xml'
	return response
"""

@app.route("/<symbol>/closing_price_graph.png")
def stock_closing_price_graph_png(symbol):
	canvas_png = closing_price_graph(symbol)
	png_img = cStringIO.StringIO()
	canvas_png.print_png(png_img)
	response = make_response(png_img.getvalue())
	response.headers['Content-Type'] = 'image/png'
	return response