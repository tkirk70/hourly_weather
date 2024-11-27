import requests
import sqlite3
import os
from datetime import datetime

# Fetch weather data from OpenWeather
def fetch_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    return response.json()

# Store data in SQLite database
def store_data(db_name, data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather
                      (id INTEGER PRIMARY KEY, city TEXT, temperature REAL, 
                       description TEXT, timestamp TEXT)''')
    cursor.execute('''INSERT INTO weather (city, temperature, description, timestamp)
                      VALUES (?, ?, ?, ?)''', 
                   (data['name'], data['main']['temp'], data['weather'][0]['description'], datetime.now()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    api_key = os.getenv('OPENWEATHER_API_KEY')
    city = "Tokyo"
    weather_data = fetch_weather(api_key, city)
    store_data('weather_data.db', weather_data)
