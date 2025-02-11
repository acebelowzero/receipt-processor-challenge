from fastapi.testclient import TestClient


class TestReceipts:
    test_client: TestClient

    sample_data = {
        "retailer": "Walgreens",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "08:13",
        "total": "2.65",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
            {"shortDescription": "Dasani", "price": "1.40"},
        ],
    }

    id = None

    def test_create_receipt(self, test_client: TestClient):
        response = test_client.post("/receipts/process", json=self.sample_data)
        assert response.status_code == 200
        assert response.json().get("id")

    def test_get_points(self, test_client: TestClient):
        response = test_client.post("/receipts/process", json=self.sample_data)
        id = response.json().get("id")
        response = test_client.get(f"/receipts/{id}/points")

        assert response.status_code == 200
        assert response.json().get("points")
        assert response.json().get("points") == 15
