# Implementasi Endpoint Transaksi Booking & Pengaman Race Condition (asyncio.Lock)
import asyncio
from fastapi import APIRouter, BackgroundTasks, HTTPException, status, Query
from typing import List, Optional
from database import get_db_connection
from models import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transaksi Booking"])

# Lock untuk mencegah race condition saat potong stok
stok_lock = asyncio.Lock()

# Ubah ke False kalau mau ngetes simulasi race condition
USE_LOCK_MECHANISM = True

async def potong_stok_logic(house_id: int, qty: int) -> bool:
    db = await get_db_connection()
    try:
        if USE_LOCK_MECHANISM:
            async with stok_lock:
                cursor = await db.execute("SELECT stok FROM houses WHERE id = ?", (house_id,))
                row = await cursor.fetchone()
                if not row or row["stok"] < qty:
                    return False
                
                await asyncio.sleep(0.01)
                await db.execute("UPDATE houses SET stok = stok - ? WHERE id = ?", (qty, house_id))
                await db.commit()
                return True
        else:
            cursor = await db.execute("SELECT stok FROM houses WHERE id = ?", (house_id,))
            row = await cursor.fetchone()
            
            await asyncio.sleep(0.01)
            
            if not row or row["stok"] < qty:
                return False
                
            await db.execute("UPDATE houses SET stok = stok - ? WHERE id = ?", (qty, house_id))
            await db.commit()
            return True
    finally:
        await db.close()

async def proses_transaksi_background(trx_id: int, house_id: int, qty: int):
    db = await get_db_connection()
    try:
        await db.execute("UPDATE transactions SET status = 'processing' WHERE id = ?", (trx_id,))
        await db.commit()
        
        sukses = await potong_stok_logic(house_id, qty)
        await asyncio.sleep(3)
        
        final_status = "completed" if sukses else "failed"
        await db.execute("UPDATE transactions SET status = ? WHERE id = ?", (final_status, trx_id))
        await db.commit()
    finally:
        await db.close()

@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def create_transaction(data: TransactionCreate, bg: BackgroundTasks):
    db = await get_db_connection()
    try:
        cursor = await db.execute("SELECT stok FROM houses WHERE id = ?", (data.house_id,))
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit perumahan tidak ditemukan")
        
        if row["stok"] < data.jumlah_unit:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Stok unit perumahan habis atau tidak mencukupi")
            
        cursor = await db.execute(
            "INSERT INTO transactions (house_id, nama_pemesan, jumlah_unit, status) VALUES (?, ?, ?, 'pending')",
            (data.house_id, data.nama_pemesan, data.jumlah_unit)
        )
        await db.commit()
        trx_id = cursor.lastrowid
        
        bg.add_task(proses_transaksi_background, trx_id, data.house_id, data.jumlah_unit)
        
        return {
            "id": trx_id,
            "house_id": data.house_id,
            "nama_pemesan": data.nama_pemesan,
            "jumlah_unit": data.jumlah_unit,
            "status": "pending",
            "message": "Transaksi booking diproses di latar belakang"
        }
    finally:
        await db.close()

@router.get("", response_model=List[TransactionResponse])
async def list_transactions(status_filter: Optional[str] = Query(None, alias="status")):
    db = await get_db_connection()
    try:
        if status_filter:
            cursor = await db.execute("SELECT * FROM transactions WHERE status = ?", (status_filter,))
        else:
            cursor = await db.execute("SELECT * FROM transactions")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()

@router.get("/{trx_id}", response_model=TransactionResponse)
async def get_transaction(trx_id: int):
    db = await get_db_connection()
    try:
        cursor = await db.execute("SELECT * FROM transactions WHERE id = ?", (trx_id,))
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaksi tidak ditemukan")
        return dict(row)
    finally:
        await db.close()