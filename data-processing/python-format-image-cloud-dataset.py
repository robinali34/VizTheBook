# -*- coding: utf-8 -*-
import ast

import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
ner_python_compressed = dataiku.Dataset("ner-python-compressed")
ner_python_compressed_df = ner_python_compressed.get_dataframe()

top_entities = ["top_people", "top_org", "top_gpe", "top_norp", "top_product", "top_law", "top_event", "top_fac", "top_loc", "top_work_of_art", "top_language"]

books = []

for idx, row in ner_python_compressed_df.iterrows():
    top_ents = []
    for entity in top_entities:
        ent = ast.literal_eval(row[entity])
        for e in ent:
            top_ents.append({
                "keyword": e[0],
                "value": e[1]
            })

    books.append({
        "title": row["title"],
        "keywords": sorted(top_ents, key=lambda x: x["value"], reverse=True)[:5]
    })

image_cloud_df = pd.DataFrame(books)


# Write recipe outputs
image_cloud = dataiku.Dataset("image-cloud")
image_cloud.write_with_schema(image_cloud_df)