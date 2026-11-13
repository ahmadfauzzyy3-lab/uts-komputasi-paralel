# Proyek UTS Komputasi Paralel - Ahmat Fauzi
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from routes.resource import router as resource_router
from routes.transaction import router as transaction_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inisialisasi tabel database saat aplikasi pertama kali berjalan
    await init_db()
    yield

app = FastAPI(
    title="API Perumahan - UTS Komputasi Paralel",
    description="Sistem Booking Unit Perumahan Async & Concurrency Safe",
    version="1.0.0",
    lifespan=lifespan
)

# Registrasi router
app.include_router(resource_router)
app.include_router(transaction_router)

@app.get("/")
async def root():
    return {"message": "Selamat datang di API Perumahan UTS Komputasi Paralel & Terdistribusi"}
