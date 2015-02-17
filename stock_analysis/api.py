import os.path
import sys
import requests
import json
import mistune
import models
import decorators

from flask import render_template

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

@app.route("/")
def main_page():
	return render_template("stock_selection.html")

@app.route("/my_stocks")
def view_my_stocks():

	#stocks = session.query(Stock).filter_by((Stock.stock_name).distinct())
	stocks = session.query(Stock.stock_name).group_by(Stock.stock_name).all()
	#query = session.query(Stock.stock_name.distinct().label("stock_name"))
	#stocks = [Stock.stock_name for stock in query.all()]
	return render_template("my_stocks.html", 
		stocks=stocks)