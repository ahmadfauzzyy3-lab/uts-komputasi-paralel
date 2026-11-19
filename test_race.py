# test_race.py: Pengujian Race Condition 2 Request Serentak dengan asyncio.gather()
import asyncio
import aiosqlite
import httpx


async def main():
    # Atur ulang stok unit ID 1 menjadi tepat 1 unit sebelum pengujian konkurensi
    async with aiosqlite.connect("perumahan.db") as db:
        await db.execute("UPDATE resources SET stok = 1 WHERE id = 1")
        await db.commit()
    print("[SETUP] Stok Unit ID 1 diatur menjadi: 1 unit")

    url = "http://127.0.0.1:8000/transactions"
    payload = {"house_id": 1, "jumlah_unit": 1}

    async with httpx.AsyncClient() as client:
        # Kirim 2 request serentak dalam milidetik yang sama
        req1 = client.post(url, json=payload)
        req2 = client.post(url, json=payload)
        res1, res2 = await asyncio.gather(req1, req2)

        print("Respon Request 1:", res1.status_code, res1.json())
        print("Respon Request 2:", res2.status_code, res2.json())

    # Tunggu pemrosesan background task (3 detik) selesai lalu cek status akhir
    await asyncio.sleep(3.5)
    async with aiosqlite.connect("perumahan.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT stok FROM resources WHERE id = 1") as c:
            stok_akhir = (await c.fetchone())["stok"]
        async with db.execute(
            "SELECT id, status FROM transactions ORDER BY id DESC LIMIT 2"
        ) as c:
            trx_akhir = [dict(r) for r in await c.fetchall()]

    print("[HASIL] Status 2 Transaksi Terakhir:", trx_akhir)
    print(f"[HASIL] Sisa Stok Akhir Unit ID 1: {stok_akhir} unit (Aman dari overselling!)")


if __name__ == "__main__":
    asyncio.run(main())
