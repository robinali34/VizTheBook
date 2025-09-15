# -*- coding: utf-8 -*-
import ast
import json

import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
count_keywords_by_section = dataiku.Dataset("count-keywords-by-section")
count_keywords_by_section_df = count_keywords_by_section.get_dataframe()

def agg_function(x):
    combined = []
    for t in x:
        combined.append(ast.literal_eval(t))
    return combined


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

streamgraph_dataset_py_df = count_keywords_by_section_df.groupby(['title', 'author'])["keyword_counts"].agg(lambda x: agg_function(x)).reset_index(name="keyword_score")
# Write recipe outputs
streamgraph_dataset_py = dataiku.Dataset("streamgraph-dataset-py")
streamgraph_dataset_py.write_with_schema(streamgraph_dataset_py_df)
