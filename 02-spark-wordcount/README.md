# Module 02 — Spark Word Count (MR vs RDD vs DataFrame)

## Input
Place a large text at `input.txt` (you can concatenate multiple files).

## Hadoop Streaming (MapReduce)
```bash
hdfs dfs -mkdir -p /user/latihan_mr/input
hdfs dfs -put input.txt /user/latihan_mr/input
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar   -files mapper.py,reducer.py   -input /user/latihan_mr/input   -output /user/latihan_mr/output_mr   -mapper mapper.py   -reducer reducer.py
```

## Spark RDD
```bash
spark-submit rdd_wordcount.py
```

## Spark DataFrame
```bash
spark-submit df_wordcount.py
```

## Catatan
- RDD lazily evaluated; eksekusi terjadi saat aksi (e.g., `takeOrdered`, `count`, `collect`).
- DataFrame memanfaatkan Catalyst Optimizer → biasanya lebih cepat dari RDD, dan jauh lebih cepat dari MR untuk workload yang sama.
