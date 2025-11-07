# Big Data Practicum — End‑to‑End
_All-in-one repo prepared for Andrew Ilham (TI) — 2025-11-06_

This repository implements and documents four practicum modules:
1. **Storage Tools**: HDFS, MongoDB, Cassandra — install, run, and basic to advanced ops.
2. **Processing**: Word Count via Hadoop Streaming (MapReduce), Spark RDD, Spark DataFrame.
3. **Data Integration**: Sqoop, Flume, Kafka pipelines.
4. **Data Preprocessing**: PySpark (Colab-ready).

## Quick Start
- Clone or unzip this repo.
- Follow each module's `README.md` for step-by-step commands.
- Use the consolidated report: `REPORT.md` (ready to print or convert to PDF).

## Structure
```
.
├── 01-hdfs-mongodb-cassandra/
├── 02-spark-wordcount/
├── 03-data-ingestion/
├── 04-preprocessing-pyspark/
└── REPORT.md
```

## Suggested push to GitHub
```bash
cd big-data-practicum-repo
git init
git add .
git commit -m "Big Data Practicum — HDFS, Spark, Sqoop/Flume/Kafka, Preprocessing"
# Create a new repo on GitHub first, then:
git remote add origin <YOUR_GITHUB_REPO_URL>
git branch -M main
git push -u origin main
```
