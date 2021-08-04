import unittest
from app import app


class User(unittest.TestCase):

    def setUp(self):
        email = "test_email"
        password = "test_password"
        self.sign_up_data = {
            "email": email,
            "password": password,
            "city": "karachi",
            "country": "pakistan"
        }
        self.login_data = {
            "email": email,
            "password": password,
        }

    def test_sign_up(self):
        url = "/signup"
        with app.test_client() as c:
            resp = c.post(url, json=self.sign_up_data, content_type="application/json")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json.get("response_code"), "00")

    def test_login(self):
        url = "/login"
        with app.test_client() as c:
            resp = c.post(url, json=self.login_data, content_type="application/json")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json.get("response_code"), "00")
            user_id = resp.json.get("id")
            session_key = resp.json.get("session_key")

            url = f"/get_user/{user_id}"
            headers = {"x-access-token": session_key}
            resp = c.get(url, headers=headers)
            self.assertEqual(resp.status_code, 200)

            #Unauthorized Getting data
            headers = {"x-access-token": "random session key"}
            resp = c.get(url, headers=headers)
            self.assertEqual(resp.status_code, 401)
