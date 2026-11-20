**Video Presentasi (YouTube):** https://www.youtube.com/watch?v=dpDBnTi1Wi4

# Sistem Backend Booking Unit Perumahan Naila Residence

Proyek Ujian Tengah Semester (UTS) mata kuliah **Komputasi Paralel dan Terdistribusi** — implementasi Asynchronous REST API menggunakan **FastAPI**, **aiosqlite**, **BackgroundTasks**, dan **asyncio.Lock**.

- **Nama:** Ahmat Fauzi
- **NIM:** 231220082
- **Kelas:** TI 33
- **Laporan Lengkap:** [docs/laporan_uts.pdf](docs/laporan_uts.pdf)

## Struktur Proyek
- `main.py` — Inisialisasi aplikasi FastAPI & registrasi router
- `database.py` — Koneksi basis data asinkron SQLite (`aiosqlite`)
- `models.py` — Skema validasi request/response Pydantic
- `routes/resource.py` — Endpoint CRUD unit perumahan (`/resource`)
- `routes/transaction.py` — Endpoint transaksi asinkron, `BackgroundTasks`, & `asyncio.Lock` (`/transactions`)
- `seed.py` — Inisialisasi data awal unit perumahan
- `test_race.py` — Pengujian konkurensi (*race condition*) serentak
- `locustfile.py` — Skenario pengujian beban (*load testing*) dengan Locust

## Cara Menjalankan
```bash
pip install -r requirements.txt
python3 seed.py
uvicorn main:app --port 8000
