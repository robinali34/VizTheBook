import com.dataiku.dss.spark._
import org.apache.spark.SparkContext
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.functions._

val sparkConf    = DataikuSparkContext.buildSparkConf()
val sparkContext = SparkContext.getOrCreate(sparkConf)
val sqlContext   = new SQLContext(sparkContext)
val dkuContext   = DataikuSparkContext.getContext(sparkContext)

// Recipe inputs
val largest_raw_prepared = dkuContext.getDataFrame(sqlContext, "largest-raw_prepared")

// TODO: Write here your actual code that computes the outputs
val largest_raw_compressed = largest_raw_prepared.groupBy("title").agg(concat_ws("\n", collect_list("text")) as "body_text")

// Recipe outputs
dkuContext.save("largest-raw-compressed", largest_raw_compressed);
