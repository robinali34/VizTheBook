# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

import spacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
nlp.max_length = 4051879

# Read recipe inputs
largest_raw_compressed = dataiku.Dataset("largest-raw-compressed")
largest_raw_compressed_df = largest_raw_compressed.get_dataframe()

def get_top_entity(x, entity):
    entity_list = []

    tokens = nlp(x["body_text"])
    for ent in tokens.ents:
        if ent.label_ == entity:
            entity_list.append(ent.text)

    return Counter(entity_list).most_common(20)

largest_raw_compressed_df["top_people"] = largest_raw_compressed_df.apply(lambda x: get_top_entity(x, "PERSON"), axis=1)
largest_raw_compressed_df["top_norp"] = largest_raw_compressed_df.apply(lambda x: get_top_entity(x, "NORP"), axis=1)
largest_raw_compressed_df["top_org"] = largest_raw_compressed_df.apply(lambda x: get_top_entity(x, "ORG"), axis=1)
largest_raw_compressed_df["top_gpe"] = largest_raw_compressed_df.apply(lambda x: get_top_entity(x, "GPE"), axis=1)
largest_raw_compressed_df["top_event"] = largest_raw_compressed_df.apply(lambda x: get_top_entity(x, "EVENT"), axis=1)
largest_raw_compressed_df["top_fac"] = largest_raw_compressed_df.apply(lambda x: get_top_entity(x, "FAC"), axis=1)
largest_raw_compressed_df["top_loc"] = largest_raw_compressed_df.apply(lambda x: get_top_entity(x, "LOC"), axis=1)
largest_raw_compressed_df["top_product"] = largest_raw_compressed_df.apply(lambda x: get_top_entity(x, "PRODUCT"), axis=1)
largest_raw_compressed_df["top_work_of_art"] = largest_raw_compressed_df.apply(lambda x: get_top_entity(x, "WORK_OF_ART"), axis=1)
largest_raw_compressed_df["top_law"] = largest_raw_compressed_df.apply(lambda x: get_top_entity(x, "LAW"), axis=1)
largest_raw_compressed_df["top_language"] = largest_raw_compressed_df.apply(lambda x: get_top_entity(x, "LANGUAGE"), axis=1)

ner_python_compressed_df = largest_raw_compressed_df # For this sample code, simply copy input to output


# Write recipe outputs
ner_python_compressed = dataiku.Dataset("ner-python-compressed")
ner_python_compressed.write_with_schema(ner_python_compressed_df)