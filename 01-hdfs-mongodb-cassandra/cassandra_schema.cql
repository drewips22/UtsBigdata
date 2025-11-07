
CREATE KEYSPACE praktikum WITH replication = {'class': 'SimpleStrategy','replication_factor': 1};
USE praktikum;
CREATE TABLE mahasiswa (
  nim text PRIMARY KEY,
  nama text,
  jurusan text
);
INSERT INTO mahasiswa (nim, nama, jurusan) VALUES ('12345','Budi','Informatika');
INSERT INTO mahasiswa (nim, nama, jurusan) VALUES ('12346','Citra','Sistem Informasi');
INSERT INTO mahasiswa (nim, nama, jurusan) VALUES ('12347','Dewi','Teknik Komputer');
SELECT * FROM mahasiswa;
SELECT * FROM mahasiswa WHERE jurusan='Informatika' ALLOW FILTERING;
