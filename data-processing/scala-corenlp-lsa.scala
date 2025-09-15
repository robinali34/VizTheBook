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

import org.apache.spark.ml.feature.{CountVectorizer, CountVectorizerModel, HashingTF, IDF}
 
val cvModel: CountVectorizerModel = new CountVectorizer()
  .setInputCol("filtered")
  .setOutputCol("rawFeatures")
  .fit(lemmatized_large)
 
val featurizedDataDF = cvModel.transform(lemmatized_large)
 
val idf = new IDF()
  .setInputCol("rawFeatures")
  .setOutputCol("TFIDFfeatures")
 
val idfModel = idf.fit(featurizedDataDF)
val tfidf_large = idfModel.transform(featurizedDataDF)

import org.apache.spark.mllib.linalg.{Vectors, Vector => MLLibVector}
import org.apache.spark.ml.linalg.{Vector => MLVector}

 
val vecRdd = tfidf_large.select("TFIDFfeatures").rdd.map { 
    row => Vectors.fromML(row.getAs[MLVector]("TFIDFfeatures"))
}

import org.apache.spark.mllib.linalg.distributed.RowMatrix
 
val mat = new RowMatrix(vecRdd)
val k = 50
val svd = mat.computeSVD(k, computeU=true)

import scala.collection.mutable.ArrayBuffer
import org.apache.spark.mllib.linalg.{Matrix,
  SingularValueDecomposition}
import org.apache.spark.mllib.linalg.distributed.RowMatrix
 
def topTermsInTopConcepts(
    svd: SingularValueDecomposition[RowMatrix, Matrix],
    numConcepts: Int,
    numTerms: Int, termIds: Array[String])
  : Seq[Seq[(String, Double)]] = {
  val v = svd.V
  val topTerms = new ArrayBuffer[Seq[(String, Double)]]()
  val arr = v.toArray
  for (i <- 0 until numConcepts) {
    val offs = i * v.numRows
    val termWeights = arr.slice(offs, offs + v.numRows).zipWithIndex
    val sorted = termWeights.sortBy(-_._1)
    topTerms += sorted.take(numTerms).map {
      case (score, id) => (termIds(id), score)
    }
  }
  topTerms   
}

print(topTermsInTopConcepts(svd, 10, 10, cvModel.vocabulary).mkString("\n\n"))

val lsa = tfidf_large;

dkuContext.save("lsa", lsa);
