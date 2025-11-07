# Module 01 — Storage Tools: HDFS, MongoDB, Cassandra

## HDFS (Single Node via Docker)
```bash
docker pull sequenceiq/hadoop-docker:2.7.0
docker run -it sequenceiq/hadoop-docker:2.7.0 /etc/bootstrap.sh -bash

# inside container
hdfs namenode -format
start-dfs.sh
jps
hdfs dfs -mkdir -p /praktikum
hdfs dfs -put dataset.csv /praktikum/
hdfs dfs -ls /praktikum/
hdfs dfs -cat /praktikum/dataset.csv
```
> Latihan: Upload file >100MB dan periksa pemecahan blok (`hdfs fsck /praktikum -files -blocks`).
  
## MongoDB (Docker)
```bash
docker run -d -p 27017:27017 --name mongo mongo:latest
docker exec -it mongo mongosh
```
Mongo shell:
```javascript
use praktikum
db.mahasiswa.insertOne({ nim: "12345", nama: "Andi", jurusan: "Informatika" })
db.mahasiswa.find()
db.mahasiswa.insertMany([
  { nim: "12346", nama: "Budi", jurusan: "Sistem Informasi" },
  { nim: "12347", nama: "Citra", jurusan: "Teknik Komputer" }
])
db.mahasiswa.createIndex({ nim: 1 })
db.mahasiswa.find().sort({ nama: 1 })
```
> Latihan: Simpan nested JSON (alamat, kontak) dalam satu dokumen.

## Cassandra (Docker)
```bash
docker run --name cassandra -d -p 9042:9042 cassandra:latest
docker exec -it cassandra cqlsh
```
CQL:
```sql
CREATE KEYSPACE praktikum WITH replication = {'class': 'SimpleStrategy','replication_factor': 1};
CREATE TABLE mahasiswa (nim text PRIMARY KEY, nama text, jurusan text);
INSERT INTO mahasiswa (nim, nama, jurusan) VALUES ('12345','Budi','Informatika');
SELECT * FROM mahasiswa;
-- Lanjutan
INSERT INTO mahasiswa (nim, nama, jurusan) VALUES ('12346','Citra','Sistem Informasi');
INSERT INTO mahasiswa (nim, nama, jurusan) VALUES ('12347','Dewi','Teknik Komputer');
SELECT * FROM mahasiswa WHERE jurusan='Informatika' ALLOW FILTERING;
```
> Latihan: Coba 2-node cluster (Docker Compose) dan amati distribusi data.
