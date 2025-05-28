from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

WEATHER_API_KEY = "366fd563131a4af1bd962603252105"
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"

@app.route('/', methods=['GET'])
def home():
    return "MCP Weather API'ye hoş geldiniz. Hava durumu için /weather?city=SehirAdi kullanın.", 200

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Şehir adı girilmedi."}), 400

    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "lang": "tr"
    }
    try:
        response = requests.get(WEATHER_API_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return jsonify({
            "şehir": data.get("location", {}).get("name"),
            "ülke": data.get("location", {}).get("country"),
            "sıcaklık_c": data.get("current", {}).get("temp_c"),
            "durum": data.get("current", {}).get("condition", {}).get("text"),
            "ikon": data.get("current", {}).get("condition", {}).get("icon"),
            "son_güncelleme": data.get("current", {}).get("last_updated")
        })
    except requests.RequestException as e:
        return jsonify({"error": "API isteği başarısız oldu.", "detay": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
