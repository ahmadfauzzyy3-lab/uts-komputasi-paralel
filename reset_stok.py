import asyncio
import aiosqlite

async def main():
    async with aiosqlite.connect("perumahan.db") as db:
        await db.execute("UPDATE houses SET stok = 1 WHERE id = 1")
        await db.commit()
        print("Stok unit ID 1 berhasil di-reset menjadi 1")

if __name__ == "__main__":
    asyncio.run(main())
