# -*- coding: utf-8 -*-
import dataiku
from dataiku import spark as dkuspark
from pyspark import SparkContext
from pyspark.sql import SQLContext

## Spark NLP imports
from sparknlp.base import Finisher, DocumentAssembler
from sparknlp.annotator import Tokenizer, Normalizer, LemmatizerModel, StopWordsCleaner
from pyspark.ml import Pipeline
import sparknlp

## NLTK import
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
eng_stopwords = stopwords.words("english")

## Create Spark and SQL Contexts
sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)

# Read recipe inputs
largest_raw_prepared = dataiku.Dataset("largest-raw_prepared")
largest_raw_prepared_df = dkuspark.get_dataframe(sqlContext, largest_raw_prepared)

document = DocumentAssembler() \
    .setInputCol('text') \
    .setOutputCol('document')
    
token = Tokenizer() \
    .setInputCols(['document']) \
    .setOutputCol('token')
    
normal = Normalizer() \
    .setInputCols(['token']) \
    .setOutputCol('normalized') \
    .setLowercase(True)
    
lemmatizer = LemmatizerModel.load("/home/dataiku/lemma/") \
    .setInputCols(['normalized']) \
    .setOutputCol('lemma')
    
stopwords = StopWordsCleaner() \
    .setInputCols(['lemma']) \
    .setOutputCol('clean_lemma') \
    .setCaseSensitive(False) \
    .setStopWords(eng_stopwords)
    
finish = Finisher() \
    .setInputCols(['clean_lemma']) \
    .setCleanAnnotations(False)
    
pipeline = Pipeline().setStages([
    document,
    token,
    normal,
    lemmatizer,
    stopwords,
    finish
])


sparknlp_large_lemma_df = pipeline.fit(largest_raw_prepared_df).transform(largest_raw_prepared_df)

# Write recipe outputs
sparknlp_large_lemma = dataiku.Dataset("sparknlp-large-lemma")
dkuspark.write_with_schema(sparknlp_large_lemma, sparknlp_large_lemma_df)

