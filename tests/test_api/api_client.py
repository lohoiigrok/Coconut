import requests
from test_super_duper.constants import AUTH_BASE_URL, HEADERS, LOGIN_ENDPOINT, SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD

print("🔍 DEBUG авторизации...")
print(f"URL: {AUTH_BASE_URL}{LOGIN_ENDPOINT}")
print(f"Email: {SUPER_ADMIN_EMAIL}")
print(f"Password: {SUPER_ADMIN_PASSWORD}")

payload = {
    "email": SUPER_ADMIN_EMAIL,
    "password": SUPER_ADMIN_PASSWORD
}

print(f"Payload: {payload}")

response = requests.post(
    f"{AUTH_BASE_URL}{LOGIN_ENDPOINT}",
    json=payload,
    headers=HEADERS
)

print(f"Status: {response.status_code}")
print(f"Response headers: {dict(response.headers)}")
print(f"Response body: {response.text}")

if response.status_code == 200:
    data = response.json()
    token = data.get("accessToken")
    print(f"✅ Токен: {token[:50]}...")
else:
    print("❌ Логин не прошёл, нуждаются в проверке креды или endpoint")