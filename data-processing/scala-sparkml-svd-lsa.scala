import com.dataiku.dss.spark._
import org.apache.spark.SparkContext
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.functions._
import org.apache.spark.ml.feature.{CountVectorizer, CountVectorizerModel}

val sparkConf    = DataikuSparkContext.buildSparkConf()
val sparkContext = SparkContext.getOrCreate(sparkConf)
val sqlContext   = new SQLContext(sparkContext)
val dkuContext   = DataikuSparkContext.getContext(sparkContext)

// Recipe inputs
val tfidf_large = dkuContext.getDataFrame(sqlContext, "tfidf-large")

val cvModel: CountVectorizerModel = new CountVectorizer()
  .setInputCol("filtered")
  .setOutputCol("rawFeatures2")
  .fit(tfidf_large)

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

val svd_large = tfidf_large;

// Recipe outputs
dkuContext.save("svd-large", svd_large);
