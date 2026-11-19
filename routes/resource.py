# routes/resource.py
from fastapi import APIRouter, HTTPException, status
import aiosqlite
from models import ResourceCreate, ResourceResponse

router = APIRouter(tags=["Resource Unit Perumahan"])
DB_NAME = "perumahan.db"


@router.get("/resource", response_model=list[ResourceResponse])
async def get_resources(skip: int = 0, limit: int = 10):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM resources LIMIT ? OFFSET ?", (limit, skip)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


@router.get("/resource/{id}", response_model=ResourceResponse)
async def get_resource_by_id(id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM resources WHERE id = ?", (id,)
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Unit perumahan tidak ditemukan",
                )
            return dict(row)


@router.post(
    "/resource",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_resource(data: ResourceCreate):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """INSERT INTO resources (tipe_rumah, lokasi_blok, harga, deskripsi, stok)
               VALUES (?, ?, ?, ?, ?)""",
            (data.tipe_rumah, data.lokasi_blok, data.harga, data.deskripsi, data.stok),
        )
        await db.commit()
        res_id = cursor.lastrowid
        return {**data.model_dump(), "id": res_id}


@router.put("/resource/{id}", response_model=ResourceResponse)
async def update_resource(id: int, data: ResourceCreate):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """UPDATE resources
               SET tipe_rumah = ?, lokasi_blok = ?, harga = ?, deskripsi = ?, stok = ?
               WHERE id = ?""",
            (
                data.tipe_rumah,
                data.lokasi_blok,
                data.harga,
                data.deskripsi,
                data.stok,
                id,
            ),
        )
        await db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unit perumahan tidak ditemukan",
            )
        return {**data.model_dump(), "id": id}


@router.delete("/resource/{id}", status_code=status.HTTP_200_OK)
async def delete_resource(id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("DELETE FROM resources WHERE id = ?", (id,))
        await db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unit perumahan tidak ditemukan",
            )
        return {"message": f"Unit perumahan dengan ID {id} berhasil dihapus permanen"}
