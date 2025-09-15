# -*- coding: utf-8 -*-
import dataiku
from dataiku import spark as dkuspark
from pyspark import SparkContext
from pyspark.sql import SQLContext

from pyspark.sql.functions import explode, col

sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)

# Read recipe inputs
sparknlp_large_lemma = dataiku.Dataset("sparknlp-large-lemma")
sparknlp_large_lemma_df = dkuspark.get_dataframe(sqlContext, sparknlp_large_lemma)

sparknlp_large_wc_df = sparknlp_large_lemma_df.withColumn('exploded_text', explode(col('finished_clean_lemma'))) \
    .groupby('title', 'id', 'exploded_text') \
    .count()

# Write recipe outputs
sparknlp_large_wc = dataiku.Dataset("sparknlp-large-wc")
dkuspark.write_with_schema(sparknlp_large_wc, sparknlp_large_wc_df)
