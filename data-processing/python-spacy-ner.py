# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

## NLP imports
import spacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

# Read recipe inputs
largest_raw_prepared = dataiku.Dataset("largest-raw_prepared")
largest_raw_prepared_df = largest_raw_prepared.get_dataframe()

tokens = nlp(''.join(str(largest_raw_prepared_df.text.tolist())))


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

ner_python_df = largest_raw_prepared_df # For this sample code, simply copy input to output


# Write recipe outputs
ner_python = dataiku.Dataset("ner-python")
ner_python.write_with_schema(ner_python_df)
