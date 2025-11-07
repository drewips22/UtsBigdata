# Laporan Praktikum Big Data — HDFS, Spark, Ingestion, dan Preprocessing

**Nama**: Andrew Ilham Putra Sibuea  
**Tanggal**: 2025-11-06

---

## Ringkasan Eksekutif
Laporan ini merangkum empat aspek utama proyek Big Data: (1) penyimpanan (HDFS, MongoDB, Cassandra), (2) pemrosesan (MapReduce, Spark RDD, dan Spark DataFrame untuk Word Count), (3) integrasi data (Sqoop, Flume, Kafka), dan (4) pra‑pemrosesan data (PySpark). Seluruh langkah berdasar modul praktikum yang Anda sediakan.

## 1. Penyimpanan Data Besar: HDFS, MongoDB, Cassandra
- **HDFS**: disiapkan via image Hadoop single node; format NameNode, jalankan `start-dfs.sh`, uji operasi `mkdir/put/ls/cat` dan verifikasi pemecahan blok pada berkas besar.  
- **MongoDB**: jalankan container, CRUD dasar, indeks pada `nim`, serta contoh sorting & nested JSON.  
- **Cassandra**: definisi keyspace, pembuatan tabel `mahasiswa`, insert massal, dan contoh `ALLOW FILTERING`.  

## 2. Pemrosesan — Word Count
### 2.1 MapReduce (Hadoop Streaming)
- **Mapper** mengubah token → pasangan `(kata,1)`; **Reducer** mengakumulasi frekuensi. Output ditulis ke HDFS.  
### 2.2 Spark RDD
- Rantai transformasi: `flatMap → map → reduceByKey`; aksi `takeOrdered`/`collect` memicu eksekusi (lazy evaluation).  
### 2.3 Spark DataFrame
- Transformasi terstruktur: `read.text → split+explode → groupBy().count() → orderBy(desc)`. Umumnya tercepat berkat Catalyst Optimizer.  

**Temuan**: DataFrame > RDD >> MR untuk workload yang sama (beban I/O disk MR paling besar).

## 3. Integrasi Data — Sqoop, Flume, Kafka
- **Sqoop**: impor tabel `employees` (MySQL) ke direktori HDFS (`-m 1` untuk mapper tunggal).  
- **Flume**: agen `netcat → memory channel → logger sink` untuk aliran log sederhana.  
- **Kafka**: inisialisasi Zookeeper & broker, buat topic `uji-praktikum`, uji producer/consumer dari CLI.  

## 4. Pra‑Pemrosesan Data — PySpark (Colab)
- **Cleaning**: imputasi `usia` (mean), isi `ulasan` kosong, hapus duplikat, standarisasi label kota (`JKT`→`Jakarta`), perbaiki `gaji` negatif, filter outlier usia (>100).  
- **Transformasi**: pengelompokan (rata-rata gaji & jumlah pelanggan), binning usia (remaja/dewasa/paruh baya), standardization & min‑max scaling.  
- **Feature Engineering**: ekstraksi fitur tanggal, encoding kategorikal (StringIndexer + OHE), dan TF‑IDF dari `ulasan`.

## Hasil & Bukti Implementasi
- Script & konfigurasi lengkap tersedia pada subfolder modul.  
- Jalur cepat eksekusi disediakan pada setiap `README.md`.

## Evaluasi Kinerja (Singkat)
- **MR** I/O intensif (disk), cocok untuk batch sederhana & interoperabilitas ekosistem Hadoop lama.  
- **Spark RDD** in‑memory, lebih cepat untuk transformasi berulang; baik untuk kontrol granular.  
- **Spark DataFrame** memanfaatkan optimasi kueri; paling ringkas dan umumnya tercepat.  

## Saran Pengembangan
1. Tambah _benchmark_ terukur (dataset ≥1GB) dan catat waktu MR, RDD, DF di mesin yang sama.
2. Jadikan pipeline ingestion → preprocessing → storage/warehouse → analitik dashboard (Spark SQL + Delta/Iceberg).

## Daftar Berkas Penting
- `01-hdfs-mongodb-cassandra/` — perintah HDFS, skrip MongoDB, skema Cassandra.
- `02-spark-wordcount/` — `mapper.py`, `reducer.py`, `rdd_wordcount.py`, `df_wordcount.py`.
- `03-data-ingestion/` — `sqoop_import.sh`, `netcat-logger.conf`, `kafka_quickstart.sh`.
- `04-preprocessing-pyspark/` — `preprocessing_colab.py`.

---

## Lampiran — Cuplikan Kode
### Mapper (Hadoop Streaming)
```python
#!/usr/bin/env python3
import sys
for line in sys.stdin:
    words = line.strip().split()
    for word in words:
        print(f"{word.lower()}\t1")
```
### Reducer (Hadoop Streaming)
```python
#!/usr/bin/env python3
import sys
from itertools import groupby
for key, group in groupby(sys.stdin, key=lambda x: x.split('\t', 1)[0]):
    try:
        total = sum(int(line.split('\t', 1)[1].strip()) for line in group)
        print(f"{key}\t{total}")
    except ValueError:
        pass
```
### Spark RDD Word Count
```python
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
```
### Spark DataFrame Word Count
```python
# WordCount with DataFrame API
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, desc

spark = SparkSession.builder.appName("DFWordCount").getOrCreate()
df = spark.read.text("input.txt")
words = df.select(explode(split(col("value"), " ")).alias("word")).filter(col("word")!="")
counts = words.groupBy("word").count().orderBy(desc("count"))
counts.show(10)
spark.stop()
```

---

**Sumber Modul (disediakan pengunggah)**
- Modul Storage HDFS/MongoDB/Cassandra.
- Modul Spark Word Count (MR vs RDD vs DataFrame).
- Modul Data Integrasi (Sqoop, Flume, Kafka).
- Modul Preprocessing (PySpark).