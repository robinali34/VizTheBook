import com.dataiku.dss.spark._
import org.apache.spark.SparkContext
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.functions._

val sparkConf    = DataikuSparkContext.buildSparkConf()
val sparkContext = SparkContext.getOrCreate(sparkConf)
val sqlContext   = new SQLContext(sparkContext)
val dkuContext   = DataikuSparkContext.getContext(sparkContext)

val largest_raw_cleaned_lemma = dkuContext.getDataFrame(sqlContext, "largest-raw-cleaned-lemma")

import org.apache.spark.ml.feature.{CountVectorizer, CountVectorizerModel, HashingTF, IDF}
 
val cvModel: CountVectorizerModel = new CountVectorizer()
  .setInputCol("filtered")
  .setOutputCol("rawFeatures")
  .fit(largest_raw_cleaned_lemma)
 
val featurizedDataDF = cvModel.transform(largest_raw_cleaned_lemma)
 
val idf = new IDF()
  .setInputCol("rawFeatures")
  .setOutputCol("TFIDFfeatures")
 
val idfModel = idf.fit(featurizedDataDF)
val tfidf_large = idfModel.transform(featurizedDataDF)

// Recipe outputs
dkuContext.save("tfidf-large", tfidf_large);
