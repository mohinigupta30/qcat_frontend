from flask import Flask, request
from flask import render_template
import random
import json
from helpers import CurrentUser
from pprint import pprint

# initializes flask app:
app = Flask(__name__)

#########################
# some global variables #
#########################
current_category = ""
##############
# Exercise 1 #
##############
@app.route('/')
def home():
    return render_template(
        'q-cat-home-page.html',
        category = current_category
    )

@app.route('/question', methods=['POST'])
def categorize():
    question = request.form['entered_question']
    return render_template(
        'q-cat-home-page.html',
        category = question,
        explanation = "Sorry, we don't have this implemented yet."
    )