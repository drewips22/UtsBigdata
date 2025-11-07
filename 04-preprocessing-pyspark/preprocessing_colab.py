# Preprocessing with PySpark (Colab-ready)
# !pip install pyspark findspark

import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder.master("local[*]").appName("PraktikumPreprocessing").getOrCreate()

data_kotor = [
    (1,'Budi Susanto',25,5500000,'L','2022-01-15','Jakarta','Transaksi berhasil, barang bagus'),
    (2,'Ani Lestari',None,8000000,'P','2022-02-20','Bandung','Pengiriman cepat dan barang sesuai'),
    (3,'Candra Wijaya',35,12000000,'L','2022-01-18','Surabaya','Sangat puas dengan pelayanannya'),
    (4,'Dewi Anggraini',22,4800000,'P','2022-03-10','JKT','Barang diterima dalam kondisi baik'),
    (5,'Eka Prasetyo',45,15000000,'L','2022-04-01','Jakarta','Transaksi gagal, mohon diperiksa'),
    (6,'Budi Susanto',25,5500000,'L','2022-01-15','Jakarta','Transaksi berhasil, barang bagus'),
    (7,'Fina Rahmawati',29,9500000,'P','2022-05-12','Bandung',None),
    (8,'Galih Nugroho',31,-7500000,'L','2022-06-25','Surabaya','Barang oke'),
    (9,'Hesti Wulandari',55,25000000,'P','2022-07-30','Jakarta','Pelayanan ramah dan cepat'),
    (10,'Indra Maulana',150,6200000,'L','2022-08-05','Medan','Produk original')
]

schema = StructType([
    StructField("id_pelanggan", IntegerType(), True),
    StructField("nama", StringType(), True),
    StructField("usia", IntegerType(), True),
    StructField("gaji", IntegerType(), True),
    StructField("jenis_kelamin", StringType(), True),
    StructField("tgl_registrasi", StringType(), True),
    StructField("kota", StringType(), True),
    StructField("ulasan", StringType(), True)
])

df = spark.createDataFrame(data=data_kotor, schema=schema)

# Missing values
df_missing = df.select([count(when(isnull(c), c)).alias(c) for c in df.columns])
mean_usia = df.select(mean(df['usia'])).collect()[0][0]
df_bersih = df.na.fill({'usia': int(mean_usia)}).na.fill({'ulasan': 'Tidak ada ulasan'})

# Duplicates
df_bersih = df_bersih.dropDuplicates()

# Inconsistencies & noise
df_bersih = df_bersih.withColumn("kota", when(col("kota")=="JKT","Jakarta").otherwise(col("kota")))
df_bersih = df_bersih.withColumn("gaji", abs(col("gaji"))).filter(col("usia") <= 100)

# Aggregation
df_agregat = df_bersih.groupBy("kota").agg(count("id_pelanggan").alias("jumlah_pelanggan"), avg("gaji").alias("rata_rata_gaji"))

# Binning
from pyspark.ml.feature import Bucketizer, VectorAssembler, StandardScaler, MinMaxScaler, StringIndexer, OneHotEncoder, Tokenizer, HashingTF, IDF
splits = [0,20,40,float('inf')]
df_binned = Bucketizer(splits=splits, inputCol="usia", outputCol="kelompok_usia").transform(df_bersih)

# Scaling
assembler = VectorAssembler(inputCols=["usia","gaji"], outputCol="fitur_numerik")
df_vec = assembler.transform(df_bersih)
std_model = StandardScaler(inputCol="fitur_numerik", outputCol="fitur_standar", withStd=True, withMean=True).fit(df_vec)
df_std = std_model.transform(df_vec)
mm_model = MinMaxScaler(inputCol="fitur_numerik", outputCol="fitur_normal").fit(df_vec)
df_mm = mm_model.transform(df_vec)

# Feature engineering (date)
df_eng = df_bersih.withColumn("timestamp_reg", to_timestamp("tgl_registrasi","yyyy-MM-dd"))
df_eng = df_eng.withColumn("tahun_reg", year("timestamp_reg")).withColumn("bulan_reg", month("timestamp_reg")).withColumn("hari_dalam_minggu", dayofweek("timestamp_reg"))

# Categorical encoding
idx_jk = StringIndexer(inputCol="jenis_kelamin", outputCol="jk_index").fit(df_eng)
idx_kota = StringIndexer(inputCol="kota", outputCol="kota_index").fit(df_eng)
df_idx = idx_kota.transform(idx_jk.transform(df_eng))
ohe = OneHotEncoder(inputCols=["jk_index","kota_index"], outputCols=["jk_ohe","kota_ohe"]).fit(df_idx)
df_enc = ohe.transform(df_idx)

# Text TF-IDF
tok = Tokenizer(inputCol="ulasan", outputCol="kata")
df_tok = tok.transform(df_enc)
tf = HashingTF(inputCol="kata", outputCol="tf_raw", numFeatures=20)
df_tf = tf.transform(df_tok)
idf = IDF(inputCol="tf_raw", outputCol="fitur_tfidf").fit(df_tf)
df_tfidf = idf.transform(df_tf)

print("Agregat per kota:")
df_agregat.show()
print("Contoh TF-IDF:")
df_tfidf.select("ulasan","fitur_tfidf").show(truncate=False)

spark.stop()
