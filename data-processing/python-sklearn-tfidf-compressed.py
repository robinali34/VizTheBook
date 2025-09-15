# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Read recipe inputs
largest_raw_compressed = dataiku.Dataset("largest-raw-compressed")
largest_raw_compressed_df = largest_raw_compressed.get_dataframe()

tfidf = TfidfVectorizer().fit_transform(largest_raw_compressed_df["body_text"])

largest_raw_compressed_df["similarity_scores"] = ""

for idx,row in largest_raw_compressed_df.iterrows():
    cosine_similarities = linear_kernel(tfidf[idx:idx+1], tfidf).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-6:-1]
    related_doc_titles = []
    for i, indx in enumerate(related_docs_indices):
        if i > 0:
            title = largest_raw_compressed_df.iloc[indx]["title"]
            related_doc_titles.append({title: cosine_similarities[indx]})
        
    largest_raw_compressed_df.set_value(idx,"similarity_scores",related_doc_titles)


tf_idf_compressed_df = largest_raw_compressed_df # For this sample code, simply copy input to output
tf_idf_compressed_df.drop("body_text", axis=1, inplace=True)


# Write recipe outputs
tf_idf_compressed = dataiku.Dataset("tf-idf-compressed")
tf_idf_compressed.write_with_schema(tf_idf_compressed_df)