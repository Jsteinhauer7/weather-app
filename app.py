import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    try:
        response = requests.get(url)
        data = response.json()
    except requests.exceptions.ConnectionError:
        return None, None
    
    if "results" not in data:
        return None, None
    
    location = data["results"][0]
    return location["latitude"], location["longitude"] 

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url)
        data = response.json()
    except requests.exceptions.ConnectionError:
        return None
    return data["current_weather"]

def describe_weather(code):
    if code == 0:
        return "Clear sky", "☀️", "#f9a825", "#fff9e6"
    elif code in [1, 2, 3]:
        return "Partly cloudy", "⛅️", "#78909c", "#eceff1"
    elif code in [61, 63, 65]:
        return "Rainy", "🌧️", "#1565c0", "#e3f2fd"
    elif code in [71, 73, 75]:
        return "Snowy", "❄️", "#80deea", "#e0f7fa"
    else:
        return "Mixed conditions","🌤️", "#7b64c8", "#ede7f6"
    
@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        lat, lon = get_coordinates(city)

        if lat is None:
            error = "City not found. Please try again."
        else:
            weather = get_weather(lat, lon)
            if weather is None:
                error = "Could not fetch weather data."
            else:
                temp_c = weather["temperature"]
                temp_f = round((temp_c * 9/5) + 32, 1)
                condition, emoji, color, bg = describe_weather(weather["weathercode"])
                weather_data = {
                    "city": city.title(),
                    "temp_f": temp_f,
                    "temp_c": temp_c,
                    "condition": condition,
                    "emoji": emoji,
                    "color": color,
                    "bg": bg,
                    "wind": weather["windspeed"]
                }

    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)