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
<<<<<<< HEAD
        category = question
    )

@app.route('/explanation', methods=['POST'])
def explain():
    return render_template(
        'question_explaination_page.html')

@app.route('/back_question', methods=['POST'])
def back_question():
    return render_template(
        'q-cat-home-page.html',
        category = current_category
    )

=======
        rquestion = question,
        category = "CATEGORY",
        explanation = "Sorry, we don't have this implemented yet."
    )
>>>>>>> d78776ce93cfdc982200b66cf3dac93c667f59c8
