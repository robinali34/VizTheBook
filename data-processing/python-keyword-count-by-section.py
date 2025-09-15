# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import ast
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import re
import string

def get_top_entity_count(row, entity, text):
    parsed_row = ast.literal_eval(row[entity].tolist()[0])
    if len(parsed_row) > 0:
        top_count = 0
        top_entity = parsed_row[0][0]

        if top_entity in text:
            top_count += sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(top_entity), text))

        return top_entity.translate(None, string.punctuation), top_count
    return None, None

# Read recipe inputs
ner_python_compressed = dataiku.Dataset("ner-python-compressed")
ner_python_compressed_df = ner_python_compressed.get_dataframe()
largest_raw_prepared = dataiku.Dataset("largest-raw_prepared")
largest_raw_prepared_df = largest_raw_prepared.get_dataframe()

largest_raw_prepared_df["keyword_counts"] = ""

for index, row in largest_raw_prepared_df.iterrows():
    top_person_count = 0
    top_norp_count = 0
    top_org_count = 0
    top_gpe_count = 0
    top_event_count = 0

    top_fac_count = 0
    top_loc_count = 0
    top_product_count = 0
    top_work_of_art_count = 0
    top_law_count = 0
    top_language_count = 0
    counts_record = {}

    title = row["title"]
    keywords_row = ner_python_compressed_df.loc[ner_python_compressed_df["title"] == title]

    top_person, top_person_count = get_top_entity_count(keywords_row, "top_people", row["text"])
    top_norp, top_norp_count = get_top_entity_count(keywords_row, "top_norp", row["text"])
    top_org, top_org_count = get_top_entity_count(keywords_row, "top_org", row["text"])
    top_gpe, top_gpe_count = get_top_entity_count(keywords_row, "top_gpe", row["text"])
    top_event, top_event_count = get_top_entity_count(keywords_row, "top_event", row["text"])

    top_fac, top_fac_count = get_top_entity_count(keywords_row, "top_fac", row["text"])
    top_loc, top_loc_count = get_top_entity_count(keywords_row, "top_loc", row["text"])
    top_product, top_product_count = get_top_entity_count(keywords_row, "top_product", row["text"])
    top_work_of_art, top_work_of_art_count = get_top_entity_count(keywords_row, "top_work_of_art", row["text"])
    top_law, top_law_count = get_top_entity_count(keywords_row, "top_law", row["text"])
    top_language, top_language_count = get_top_entity_count(keywords_row, "top_language", row["text"])

    if top_person:
        counts_record[top_person] = top_person_count

    if top_norp:
        counts_record[top_norp] = top_norp_count

    if top_org:
        counts_record[top_org] = top_org_count

    if top_gpe:
        counts_record[top_gpe] = top_gpe_count

    if top_event:
        counts_record[top_event] = top_event_count

    if top_loc:
        counts_record[top_loc] = top_loc_count

    if top_product:
        counts_record[top_product] = top_product_count

    if top_work_of_art:
        counts_record[top_work_of_art] = top_work_of_art_count

    if top_law:
        counts_record[top_law] = top_law_count

    if top_fac:
        counts_record[top_fac] = top_fac_count

    if top_language:
        counts_record[top_language] = top_language_count

    counts_record["decile"] = row["id"]
    largest_raw_prepared_df.at[index, "keyword_counts"] = counts_record

count_keywords_by_section_df = largest_raw_prepared_df


# Write recipe outputs
count_keywords_by_section = dataiku.Dataset("count-keywords-by-section")
count_keywords_by_section.write_with_schema(count_keywords_by_section_df)