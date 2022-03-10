from flask import Flask, request
from flask import render_template
import random
import json
from helpers import CurrentUser
from pprint import pprint
import torch
from transformers import DistilBertTokenizerFast 
from transformers import DistilBertForSequenceClassification, Trainer, TrainingArguments
from transformers import TextClassificationPipeline, BertConfig, AutoConfig, PretrainedConfig

# initializes flask app:
app = Flask(__name__)




class Qcat:
  # maybe keep a static dict of parent-labels?

  def __init__(self):
    # load the model and save it in this object
    model_name = "distilbert-base-uncased"
    tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)
    path = "ekohrt/qcat"
    config = AutoConfig.from_pretrained(pretrained_model_name_or_path=path)
    model = DistilBertForSequenceClassification.from_pretrained(path, config=config)
    self.pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)

  def classify(self, input_question_text):
    softmaxed_logits = self.pipe(input_question_text)
    return ResultsContainer(softmaxed_logits)

class ResultsContainer:
  def __init__(self, softmaxed_logits):
    # store results as ordered list of {'label': labelName, 'confidence': confidence_flt} objects.
    self.softmaxed_logits = sorted(softmaxed_logits[0], key=lambda x: x['score'], reverse=True)
    # print(self.softmaxed_logits)
    self.top_label = self.softmaxed_logits[0]
    self.formatted_string = f"{self.top_label['label']} ({round(self.top_label['score'], 2)})"






#########################
# some global variables #
#########################
current_category = ""
qcat = Qcat()
confidence=""
formatting_category = {"qualitative_property_retrieval": "Qualitative Property Retrieval", 
            "numeric_retrieval": "Numeric Retrieval", 
            "boolean_retrieval": "Boolean Retrieval",
            "datetime_retrieval": "Datetime Retrieval",
            "set_retrieval": "Set Retrieval",
            "qualitative_property_multihop_retrieval": "Qualitative Property Multihop Retrieval", 
            "numeric_comparison": "Numeric Comparison",
            "datetime_comparison": "Datetime Comparison", 
            "qualitative_comparison": "Qualitative Comparison", 
            "superlative": "Superlative", 
            "set_intersection": "Set Intersection",
            "set_union": "Set Union", 
            "set_difference": "Set Difference", 
            "mathematical_comparison": "Mathematical Comparison", 
            "set_property_satisfaction": "Set Property Satisfaction", 
            "arithmetic": "Arithmetic",
            "standard_deviation": "Standard Deviation", 
            "correlation": "Correlation",
            "average": "Average", 
            "median": "Median", 
            "mode": "Mode", 
            "counting": "Counting", 
            "range": "Range",
            "boolean_and": "Boolean And", 
            "boolean_or": "Boolean Or",
            "definitional": "Definitional",
            "causal_explanation": "Causal Explanation", 
            "opinion": "Opinion"}

explanation_category = {"Arithmetic": "Questions in this category require some piece of basic arithmetic to be performed (e.g. addition, subtraction, multiplication, division).",
"Standard Deviation": "Questions in this category require the standard deviation to be calculated over a set of data points.",
"Correlation": "Questions in this category require a correlation to be calculated over a set of data points.",
"Average": "Questions in this category require an average value to be calculated over a collection of values or data points.",
"Median": "Questions in this category require the median value to be found in a collection of values.",
"Mode": "Questions in this category require the most common value to be found in a collection of values.",
"Counting": "Questions in this category require that a collection of items be counted in order to answer the question.",
"Range": "Questions in this category require the range of values to be found in a collection of values.",
"Qualitative Property Retrieval": "Questions in this category require a single property to be retrieved about a given entity.",
"Numeric Retrieval": "Questions in this category require a numeric value to be retrieved.",
"Boolean Retrieval": "Questions in this category require a boolean value to be retrieved or produced given a set of properties or text regarding an entity.",
"Datetime Retrieval": "Questions in this category require a datetime value to be retrieved.",
"Set Retrieval": "Questions in this category require a set of values to be retrieved.",
"Qualitative Property Multihop Retrieval": "Questions that require a sequence of simple retrieval questions to be answered.",
"Numeric Comparison": "Questions in this category require multiple numeric values to be found and compared in order to determine which is greater, lesser, equal, etc.",
"Datetime Comparison": "Questions in this category require multiple datetime values to be found and compared in order to determine which is first, last, the same, etc.",
"Qualitative Comparison": "Questions in this category require qualitative properties of entities to be found and compared.",
"Superlative": "Questions in this category require that multiple values be found and ranked in order to determine the top value.",
"Set Intersection": "Questions in this category require that at least two sets of values be found in order to perform an intersection operation and find the common elements.",
"Set Union": "Questions in this category require that at least two sets of values be found in order to perform a union operation and merge the sets together into one.",
"Set Difference": "Questions in this category require that at least two sets of values be found in order to find the elements that are in one set, but not in the other sets.",
"Mathematical Comparison": "Questions in this category can be viewed as inheriting from Metric Comparison and Mathematics as they require both a mathematical computation to be performed, as well as a comparison of the computed values.",
"Set Property Satisfaction": "Questions in this category require that a set of entities that satisfy a specific property are found.",
"Boolean And": "Questions in this category require a boolean AND expression to be evaluated from a collection of boolean values.", 
"Boolean Or": "Questions in this category require a boolean OR expression to be evaluated from a collection of boolean values.",
"Definitional": "Questions in this category require that the definition or meaning of an entity or word is provided to the user.",
"Causal Explanation": "Questions in this category require some kind of description of why an event has occurred or why something is the way it is.",
"Opinion": "Questions in this category require an opinion."}

@app.route('/')
def home():
    return render_template(
        'q-cat-home-page.html',
        category = current_category
    )

@app.route('/question', methods=['POST'])
def categorize():
    question = request.form['entered_question']
    result = qcat.classify(question)
    rcategory = formatting_category[result.top_label['label']]
    return render_template(
        'q-cat-home-page.html',
        rquestion = question,
        category = rcategory,
        confidence = round(result.top_label['score'], 2),
        explanation = explanation_category[rcategory]
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
