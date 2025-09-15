# -*- coding: utf-8 -*-
from operator import itemgetter
import ast

import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
tf_idf_compressed = dataiku.Dataset("tf-idf-compressed")
tf_idf_compressed_df = tf_idf_compressed.get_dataframe()
ner_python_compressed = dataiku.Dataset("ner-python-compressed")
ner_python_compressed_df = ner_python_compressed.get_dataframe()

top_entities = ["top_people", "top_org", "top_gpe", "top_norp", "top_product", "top_law", "top_event", "top_fac", "top_loc", "top_work_of_art", "top_language"]

book_rel_info = []
for idx, row in tf_idf_compressed_df.iterrows():
    source = row["title"]

    sim_scores = ast.literal_eval(row["similarity_scores"])
    for score in sim_scores:
        top_ents = []
        target = list(score)[0]

        for entity in top_entities:
            top_entity_source = ast.literal_eval(ner_python_compressed_df.loc[ner_python_compressed_df['title'] == source, entity].values[0])
            top_entity_target = ast.literal_eval(ner_python_compressed_df.loc[ner_python_compressed_df['title'] == target, entity].values[0])

            for s in top_entity_source:
                for t in top_entity_target:
                    if s[0] == t[0]:
                        top_ents.append((s[0], s[1]+t[1]))

        for top in sorted(top_ents, key=lambda x: x[1], reverse=True)[:3]:
            book_rel_info.append({
                "source": source,
                "target": target,
                "value": top[1],
                "keyword": top[0]
            })
graph = pd.DataFrame(book_rel_info)

book_rel_info_df = graph


# Write recipe outputs
book_rel_info = dataiku.Dataset("book_rel_info")
book_rel_info.write_with_schema(book_rel_info_df)