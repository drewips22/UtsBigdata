// MongoDB sample script
use praktikum
db.mahasiswa.insertOne({ nim: "12345", nama: "Andi", jurusan: "Informatika" })
db.mahasiswa.insertMany([
  { nim: "12346", nama: "Budi", jurusan: "Sistem Informasi" },
  { nim: "12347", nama: "Citra", jurusan: "Teknik Komputer" }
])
db.mahasiswa.createIndex({ nim: 1 })
db.mahasiswa.find().sort({ nama: 1 })
