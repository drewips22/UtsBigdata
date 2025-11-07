
#!/usr/bin/env bash
hdfs namenode -format
start-dfs.sh
jps
hdfs dfs -mkdir -p /praktikum
hdfs dfs -put dataset.csv /praktikum/
hdfs dfs -ls /praktikum/
hdfs dfs -cat /praktikum/dataset.csv
hdfs fsck /praktikum -files -blocks
