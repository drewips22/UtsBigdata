# WordCount with DataFrame API
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, desc

spark = SparkSession.builder.appName("DFWordCount").getOrCreate()
df = spark.read.text("input.txt")
words = df.select(explode(split(col("value"), " ")).alias("word")).filter(col("word")!="")
counts = words.groupBy("word").count().orderBy(desc("count"))
counts.show(10)
spark.stop()
