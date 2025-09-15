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
largest_raw_prepared = dataiku.Dataset("largest-raw_prepared")
largest_raw_prepared_df = dkuspark.get_dataframe(sqlContext, largest_raw_prepared)

document = DocumentAssembler()\
    .setInputCol("text")\
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
sparknlp_large_ner_dl_df = ner_prediction_pipeline.fit(largest_raw_prepared_df).transform(largest_raw_prepared_df)

# Write recipe outputs
sparknlp_large_ner_dl = dataiku.Dataset("sparknlp-large-ner-dl")
dkuspark.write_with_schema(sparknlp_large_ner_dl, sparknlp_large_ner_dl_df)
