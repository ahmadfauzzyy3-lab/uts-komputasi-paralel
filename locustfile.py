# Simulasi Load Testing API Booking Unit Naila Residence menggunakan Locust
from locust import HttpUser, task, between

class PerumahanUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(2)
    def read_resource(self):
        # Skenario Read: GET /resource
        self.client.get("/resource?skip=0&limit=10", name="GET /resource")

    @task(1)
    def create_transaction(self):
        # Skenario Write: POST /transactions
        payload = {
            "house_id": 1,
            "jumlah_unit": 1
        }
        self.client.post("/transactions", json=payload, name="POST /transactions")