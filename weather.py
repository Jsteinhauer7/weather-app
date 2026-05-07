import requests

def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    try:
        response = requests.get(url)
        data = response.json()
    except requests.exceptions.ConnectionError:
        return None, none
    
    if "results" not in data:
        return None, none
    
    location = data["results"][0]
    return location["latitude"], location["longitude"]

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url)
        data = response.json()
    except requests.exceptions.ConnectionError:
        return None, none
    return data["current_weather"]
    

def describe_weather(code):
    if code == 0:
        return "Clear sky"
    elif code in [1, 2, 3]:
        return "Partly cloudy"
    elif code in [61, 63, 65]:
        return "Rainy"
    elif code in [71, 73, 75]:
        return "Snowy"
    else:
        return "Mixed conditions"
    
city = input("Enter a city: ")
lat, lon = get_coordinates(city)

if lat is None:
    print("City not found.")
else:
    weather = get_weather(lat, lon)
    if weather is None:
        print("Could not fetch weather data")
    else:
        temp_c = weather["temperature"]
        temp_f = round((temp_c * 9/5) + 32, 1)
        condition = describe_weather(weather["weathercode"])
        print(f"\nWeather in {city}:")
        print(f"Temperature: {temp_f}°F ({temp_c}°C)")
        print(f"Condition: {condition}")
        print(f"Wind speed: {weather['windspeed']} km/h")