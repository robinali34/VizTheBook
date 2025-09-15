import com.dataiku.dss.spark._
import org.apache.spark.SparkContext
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.functions._

import com.databricks.spark.corenlp.functions.lemma

val sparkConf    = DataikuSparkContext.buildSparkConf()
val sparkContext = SparkContext.getOrCreate(sparkConf)
val sqlContext   = new SQLContext(sparkContext)
val dkuContext   = DataikuSparkContext.getContext(sparkContext)

val version = "3.6.0"
val model = s"stanford-corenlp-$version-models" // append "-english" to use the full English model
val jars = sparkContext.asInstanceOf[{def addedJars: scala.collection.mutable.Map[String, Long]}].addedJars.keys // use sc.listJars in Spark 2.0

import scala.sys.process._
s"wget https://repo1.maven.org/maven2/edu/stanford/nlp/stanford-corenlp/$version/$model.jar -O /tmp/$model.jar".!!
sparkContext.addJar(s"/tmp/$model.jar")

// Recipe inputs
val largest_raw = dkuContext.getDataFrame(sqlContext, "largest-raw_prepared")
val lemmatized = largest_raw.withColumn("lemmatized", lemma(col("text")))

import scala.io.Source
val coreNLPStopWordsGitHub = "https://raw.githubusercontent.com/stanfordnlp/CoreNLP/master/data/edu/stanford/nlp/patterns/surface/stopwords.txt"
val words = Source.fromURL(coreNLPStopWordsGitHub)
val additionalStopWords = "#BEGINPOST\n_\n|\n\\\n\\\\\n/\n//\n||\n???\n0/0\nn\n2/2\n--\n"
val stopWordsList = (additionalStopWords+words.mkString).split("\n")
import org.apache.spark.ml.feature.StopWordsRemover
 
val remover = new StopWordsRemover()
  .setInputCol("lemmatized")
  .setOutputCol("filtered")
  .setStopWords(stopWordsList)
 
val lemmatized_large = remover.transform(lemmatized)

// Recipe outputs
dkuContext.save("largest-raw-cleaned-lemma", lemmatized_large);
