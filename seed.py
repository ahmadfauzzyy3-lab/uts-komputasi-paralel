import asyncio
import aiosqlite

async def seed_data():
    async with aiosqlite.connect("perumahan.db") as db:
        # Hapus tabel lama agar struktur kolom diperbarui total
        await db.execute("DROP TABLE IF EXISTS resources")
        await db.execute("DROP TABLE IF EXISTS transactions")
        
        # Buat ulang tabel resources dengan kolom Naila Residence Tipe 50+
        await db.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipe_rumah TEXT NOT NULL,
                lokasi_blok TEXT NOT NULL,
                harga REAL NOT NULL,
                deskripsi TEXT NOT NULL,
                stok INTEGER NOT NULL CHECK (stok >= 0)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                house_id INTEGER NOT NULL,
                jumlah_unit INTEGER NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (house_id) REFERENCES resources (id)
            )
        """)

        # Data Resmi Naila Residence Tipe 50+
        houses = [
            ("Naila Residence Tipe 50+", "Blok A1", 350000000.0, "2 Kamar Tidur, 1 Kamar Mandi, Dapur Standar", 5),
            ("Naila Residence Tipe 50+", "Blok A2", 350000000.0, "2 Kamar Tidur, 1 Kamar Mandi, Carport", 3),
            ("Naila Residence Tipe 50+", "Blok A3", 355000000.0, "2 Kamar Tidur, 1 Kamar Mandi, Taman Depan", 4),
            ("Naila Residence Tipe 50+ Hook", "Blok B1", 380000000.0, "2 Kamar Tidur, 1 Kamar Mandi, Tanah Ekstra Hook", 2),
            ("Naila Residence Tipe 50+", "Blok B2", 350000000.0, "2 Kamar Tidur, 1 Kamar Mandi, Minimalis Modern", 6),
            ("Naila Residence Tipe 50+", "Blok B3", 350000000.0, "2 Kamar Tidur, 1 Kamar Mandi, Kanopi Samping", 4),
            ("Naila Residence Tipe 50+ Premium", "Blok C1", 395000000.0, "3 Kamar Tidur, 2 Kamar Mandi, Finishing Premium", 2),
            ("Naila Residence Tipe 50+", "Blok C2", 350000000.0, "2 Kamar Tidur, 1 Kamar Mandi, Listrik 1300W", 3),
            ("Naila Residence Tipe 50+", "Blok C3", 350000000.0, "2 Kamar Tidur, 1 Kamar Mandi, Air Bersih PDAM", 5),
            ("Naila Residence Tipe 50+ Hook", "Blok D1", 385000000.0, "3 Kamar Tidur, 2 Kamar Mandi, Posisi Hook Eksklusif", 1)
        ]
        
        await db.executemany(
            """INSERT INTO resources (tipe_rumah, lokasi_blok, harga, deskripsi, stok) 
               VALUES (?, ?, ?, ?, ?)""",
            houses
        )
        await db.commit()
        print("SUCCESS: 10 Data Naila Residence Tipe 50+ berhasil dimasukkan!")

if __name__ == "__main__":
    asyncio.run(seed_data())