# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
map_dataset = dataiku.Dataset("map-dataset")
map_dataset_df = map_dataset.get_dataframe()

processed = []
rows = []

for idx, row in map_dataset_df.iterrows():
    title = row["title"]
    if not title in processed:
        locations = []

        book_rows = map_dataset_df.loc[map_dataset_df["title"] == title]

        for _, r in book_rows.iterrows():
            locations.append({
                "text": r["text"],
                "lat": r["lat"],
                "long": r["long"],
                "count": r["count"]
            })
        rows.append({
            "title": title,
            "locations": locations
        })
        processed.append(title)


map_final_df = pd.DataFrame(rows)


# Write recipe outputs
map_final = dataiku.Dataset("map-final")
map_final.write_with_schema(map_final_df)