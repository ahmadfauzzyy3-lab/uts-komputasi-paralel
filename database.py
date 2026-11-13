import aiosqlite

DB_NAME = "perumahan.db"

async def get_db_connection():
    db = await aiosqlite.connect(DB_NAME)
    db.row_factory = aiosqlite.Row
    return db

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
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
        await db.commit()