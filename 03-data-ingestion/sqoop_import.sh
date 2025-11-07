# Sqoop: Import MySQL → HDFS
# MySQL prep
mysql -u root -p <<'SQL'
CREATE DATABASE IF NOT EXISTS company;
USE company;
CREATE TABLE IF NOT EXISTS employees (id INT, name VARCHAR(50));
INSERT INTO employees VALUES (1,'Andi'),(2,'Budi'),(3,'Citra');
SQL

# Ensure mysql-connector-java-*.jar is in $SQOOP_HOME/lib
$SQOOP_HOME/bin/sqoop import   --connect jdbc:mysql://localhost/company   --username root   --password 'your_password'   --table employees   --target-dir /user/hadoop/employees   -m 1

hdfs dfs -ls /user/hadoop/employees
hdfs dfs -cat /user/hadoop/employees/part-m-00000
