# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
book_rel_info = dataiku.Dataset("book_rel_info")
book_rel_info_df = book_rel_info.get_dataframe()
largest_raw_prepared = dataiku.Dataset("largest-raw_prepared")
largest_raw_prepared_df = largest_raw_prepared.get_dataframe()

book_sections = []
for idx, book in book_rel_info_df.iterrows():
    title = book["source"]
    keyword = book["keyword"]

    book_rows = largest_raw_prepared_df.loc[largest_raw_prepared_df['title'] == title]

    best_section = ""
    best_section_count = 0

    for indx, row in book_rows.iterrows():
        count = row["text"].count(keyword)
        if count > best_section_count:
            best_section = row["text"]
            best_section_count = count

    book_sections.append({
        "title": title,
        "keyword": keyword,
        "section": best_section
    })


book_info_df = pd.DataFrame(book_sections)


# Write recipe outputs
book_info = dataiku.Dataset("book_info")
book_info.write_with_schema(book_info_df)