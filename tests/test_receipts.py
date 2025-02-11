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

    bad_data = {
        "retailer": "Hellow@world",  # invalid retailer cannot have @
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:13",
        "total": "1",  # invalid total - missing decimal
        "items": [
            {
                "shortDescription": "Pepsi - 12-oz",
                "price": "1.",
            }  # invalid price - missing digits after decimal
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

    def test_get_points_not_found(self, test_client: TestClient):
        id = "63f14c54-4903-4408-8773-b4c34a9d1d7a"
        response = test_client.get(f"/receipts/{id}/points")
        assert response.status_code == 404
        assert response.json()["message"] == "No receipt found for that ID."

    def test_check_bad_request(self, test_client: TestClient):
        response = test_client.post(f"/receipts/process", json=self.bad_data)
        assert response.status_code == 400
        assert response.json()["message"] == "The receipt is invalid."
