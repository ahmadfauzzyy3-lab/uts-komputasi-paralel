from pydantic import BaseModel, Field

class ResourceBase(BaseModel):
    tipe_rumah: str = Field(..., example="Naila Residence Tipe 50+")
    lokasi_blok: str = Field(..., example="Blok A1")
    harga: float = Field(..., example=350000000.0)
    deskripsi: str = Field(..., example="2 Kamar Tidur, 1 Kamar Mandi")
    stok: int = Field(..., example=5)

class ResourceCreate(ResourceBase):
    pass

class ResourceResponse(ResourceBase):
    id: int

    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    house_id: int = Field(..., example=1)
    jumlah_unit: int = Field(..., example=1)

class TransactionResponse(BaseModel):
    id: int
    house_id: int
    jumlah_unit: int
    status: str

    class Config:
        from_attributes = True