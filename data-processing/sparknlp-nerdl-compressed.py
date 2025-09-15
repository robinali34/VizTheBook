# -*- coding: utf-8 -*-
import dataiku
from dataiku import spark as dkuspark
from pyspark import SparkContext
from pyspark.sql import SQLContext

## Spark NLP imports
from sparknlp.base import Finisher, DocumentAssembler
from sparknlp.annotator import BertEmbeddings, Tokenizer, Normalizer, SentenceDetector, NerDLModel, NerConverter
from pyspark.ml import Pipeline
import sparknlp

sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)

# Read recipe inputs
largest_raw_compressed = dataiku.Dataset("largest-raw-compressed")
largest_raw_compressed_df = dkuspark.get_dataframe(sqlContext, largest_raw_compressed)

document = DocumentAssembler()\
    .setInputCol("body_text")\
    .setOutputCol("document")

sentence = SentenceDetector()\
    .setInputCols(['document'])\
    .setOutputCol('sentence')

token = Tokenizer()\
    .setInputCols(['sentence'])\
    .setOutputCol('token')

bert = BertEmbeddings.load('/home/dataiku/bert_base_cased/') \
 .setInputCols(["sentence",'token'])\
 .setOutputCol("bert")\
 .setCaseSensitive(False)

loaded_ner_model = NerDLModel.load("/home/dataiku/ner_dl_bert/")\
 .setInputCols(["sentence", "token", "bert"])\
 .setOutputCol("ner")

converter = NerConverter()\
  .setInputCols(["document", "token", "ner"])\
  .setOutputCol("ner_span")

ner_prediction_pipeline = Pipeline(
    stages = [
        document,
        sentence,
        token,
        bert,
        loaded_ner_model,
        converter])

# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a SparkSQL dataframe
large_compressed_nerdl_df = ner_prediction_pipeline.fit(largest_raw_compressed_df).transform(largest_raw_compressed_df)

# Write recipe outputs
large_compressed_nerdl = dataiku.Dataset("large-compressed-nerdl")
dkuspark.write_with_schema(large_compressed_nerdl, large_compressed_nerdl_df)
