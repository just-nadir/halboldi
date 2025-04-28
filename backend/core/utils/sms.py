import requests
from core.models import SMSLog  # qo‘shiladi


ESKIZ_BASE_URL = "https://notify.eskiz.uz"
EMAIL = "abdullayevamalika880@gmail.com"
PASSWORD = "KHgkYNJx3wOZaTx6OOJjBlUf9QwrZjWkUAZn7BPQ"

# Tokenni saqlash (global)
api_token = None


def get_token():
    global api_token
    if api_token:
        return api_token

    url = f"{ESKIZ_BASE_URL}/api/auth/login"
    data = {
        "email": EMAIL,
        "password": PASSWORD
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        api_token = response.json()['data']['token']
        return api_token
    else:
        raise Exception("Eskiz token olishda xatolik: ", response.text)


def send_sms(phone_number, message):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "mobile_phone": phone_number.replace('+998', ''),
        "message": message,
        "from": "4546",
        "callback_url": ""
    }

    url = f"{ESKIZ_BASE_URL}/api/message/sms/send"
    response = requests.post(url, headers=headers, data=data)

    # 🔴 Log saqlash (muvaffaqiyat yoki xato holatida)
    SMSLog.objects.create(
        phone=phone_number,
        message=message,
        success=response.status_code == 200
    )

    if response.status_code == 200:
        print("✅ SMS yuborildi:", phone_number)
    else:
        print("❌ SMS yuborilmadi:", response.text)
