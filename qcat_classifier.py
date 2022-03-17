# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 19:16:37 2022

@author: Ethan
"""
import torch
from transformers import DistilBertTokenizerFast     #docs: https://huggingface.co/docs/transformers/model_doc/distilbert#transformers.DistilBertTokenizerFast
from transformers import DistilBertForSequenceClassification, Trainer, TrainingArguments
from transformers import TextClassificationPipeline, BertConfig, AutoConfig, PretrainedConfig

# next step: plot confidence?
# figure out how to integrate into website (importing modules, etc)

"""
Container for the Qcat classifier model.
"""
class Qcat:
  # maybe keep a static dict of parent-labels?

  def __init__(self):
    # load the model from huggingface hub and save it in this object
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
    
qcat = Qcat()
results = qcat.classify("how many living presidents are there?")
print(results.top_label)
