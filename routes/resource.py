# routes/resource.py
from fastapi import APIRouter, HTTPException, status
import aiosqlite
from models import ResourceCreate, ResourceResponse

router = APIRouter()
DB_NAME = "perumahan.db"

@router.get("/resource", response_model=list[ResourceResponse])
async def get_resources(skip: int = 0, limit: int = 10):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM resources LIMIT ? OFFSET ?", (limit, skip)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

@router.post("/resource", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(data: ResourceCreate):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """INSERT INTO resources (nama, kategori, jumlah_kamar, jumlah_kamar_mandi, harga, stok) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (data.nama, data.kategori, data.jumlah_kamar, data.jumlah_kamar_mandi, data.harga, data.stok)
        )
        await db.commit()
        res_id = cursor.lastrowid
        return {**data.dict(), "id": res_id}