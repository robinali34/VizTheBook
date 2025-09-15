# -*- coding: utf-8 -*-
import dataiku
from dataiku import spark as dkuspark
from pyspark import SparkContext
from pyspark.sql import SQLContext

from pyspark.sql import functions as F

sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)

# Read recipe inputs
count_keywords_by_section = dataiku.Dataset("count-keywords-by-section")
count_keywords_by_section_df = dkuspark.get_dataframe(sqlContext, count_keywords_by_section)

streamgraph_dataset_df = count_keywords_by_section_df.groupBy("title", "author").agg(F.collect_list("keyword_counts").alias("keyword_score"))

# Write recipe outputs
streamgraph_dataset = dataiku.Dataset("streamgraph-dataset")
dkuspark.write_with_schema(streamgraph_dataset, streamgraph_dataset_df)
