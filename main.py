from fastapi import FastAPI
import requests, json

app = FastAPI()

# ✅ Number normalization helper
def normalize_number(number: str) -> str:
    number = number.strip()
    if not number.startswith("+"):
        if number.startswith("91"):
            return "+" + number
        else:
            return "+91" + number
    return number

@app.get("/")
def home():
    return {"status": "ok", "developer": "@iacceptescrow2"}

# ✅ Ignore favicon.ico requests to prevent 400 errors
@app.get("/favicon.ico")
def favicon():
    return {}

@app.get("/lookup")
def lookup(number: str):
    normalized = normalize_number(number)
    headers = {
        'authority': 'chut.voidnetwork.in',
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://chut.voidnetwork.in',
        'referer': 'https://chut.voidnetwork.in/',
        'user-agent': 'Mozilla/5.0'
    }
    json_data = {'type': 'mobile', 'term': normalized}
    try:
        r = requests.post("https://chut.voidnetwork.in/api", headers=headers, json=json_data)
        data = r.json()
        return {
            "developer": "@iacceptescrow2",
            "number": normalized,
            "response": data
        }
    except Exception as e:
        return {"error": str(e), "developer": "@iacceptescrow2"}
