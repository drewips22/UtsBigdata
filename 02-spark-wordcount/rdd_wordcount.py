# WordCount with RDD API
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("RDDWordCount").getOrCreate()

lines = spark.sparkContext.textFile("input.txt")
counts = (lines.flatMap(lambda l: l.lower().split())
               .map(lambda w: (w,1))
               .reduceByKey(lambda a,b: a+b))
print("\nTop 10 words:")
for w,c in counts.takeOrdered(10, key=lambda x: -x[1]):
    print(w, c)

spark.stop()
