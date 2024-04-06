from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

client = APIClient()


class WalletTest(TestCase):
    def test_create_wallet_successful(self):
        result = client.post("/wallets/")
        print(f"{result.status_code=}")
        print(f"{result.json()=}")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result.json()["balance"], "0.00")

    def test_deposit_wallet_negative_balance(self):
        result = client.post("/wallets/")
        print(f"{result.status_code=}")
        print(f"{result.json()=}")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        wallet_id = result.json()["uuid"]
        data = {"balance": -10.10}

        result = client.post(f"/wallets/{wallet_id}/deposit", data=data, format="json")
        print(f"{result.status_code=}")
        print(f"{result.json()=}")

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            result.json()["balance"][0],
            "Ensure this value is greater than or equal to 0.00.",
        )

    def test_deposit_wallet_successful(self):
        result = client.post("/wallets/")
        print(f"{result.status_code=}")
        print(f"{result.json()=}")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        wallet_id = result.json()["uuid"]
        data = {"balance": 10.23}

        result = client.post(f"/wallets/{wallet_id}/deposit", data=data, format="json")
        print(f"{result.status_code=}")
        print(f"{result.json()=}")

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.json()["balance"], str(data["balance"]))

    # test delete wallet

    # test update wallet info

    # ...
