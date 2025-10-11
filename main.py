from fastapi import FastAPI, HTTPException
import requests
import re

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

REQUIRED_API_KEY = "ishu@1"

# ✅ Helper to remove URLs from JSON recursively
def remove_links(obj):
    url_pattern = re.compile(r"https?://\S+")
    
    if isinstance(obj, dict):
        return {k: remove_links(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [remove_links(i) for i in obj]
    elif isinstance(obj, str):
        return url_pattern.sub("", obj)  # completely remove link
    else:
        return obj

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/lookup")
def lookup(key: str = "", number: str = ""):
    # ✅ API Key check
    if key != REQUIRED_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")

    # ✅ Validate number
    if not number:
        raise HTTPException(status_code=400, detail="Missing 'number' parameter")

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
        r = requests.post("https://chut.voidnetwork.in/api", headers=headers, json=json_data, timeout=10)
        r.raise_for_status()
        data = r.json()

        # ✅ Remove unwanted keys like join_backup and join_main
        data.pop("join_backup", None)
        data.pop("join_main", None)

        # ✅ Remove any links inside remaining data
        sanitized = remove_links(data)

        return sanitized

    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Upstream request failed: {str(e)}")
