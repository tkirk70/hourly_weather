import requests
import pandas as pd
import sqlite3
import time
import os
from datetime import datetime

# Access the API key from the environment variable
api_key = os.getenv('API_KEY')
print(api_key)

# Define the file name and the data to write
file_name = 'log.txt'
now = datetime.now()




cities = ['Columbus', 'Charlotte', 'Cleveland', 'Stanwood', 'Tucson', 'Tampa', 'Milwaukee']
# cities = ['Columbus']


for city in cities:
    params = {'q': f'{city}', 'appid': api_key, 'units' : 'imperial'}
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
    print(response)
    # print(response.json())
    j = response.json()

    status = response.status_code

    # Open the file in append mode ('a') which creates the file if it doesn't exist
    with open(file_name, 'a') as file:
        file.write(api_key)
        file.write(" ")
        file.write(str(status))
        file.write(" ")
        file.write(j)
        file.write(" ")
        file.write(str(now))
        file.write(" ")
    # Convert to datetime object
    try:
        dt_object = datetime.fromtimestamp(j['dt'])
    except:
        dt_object = None
    
    # Convert to pandas datetime64[ns]
    date1 = pd.to_datetime(dt_object.date())
    time1 = pd.to_datetime(dt_object.time().strftime('%H:%M:%S'))

    dict_ = {
    'location' : j['name'],
    'description' : j['weather'][0]['main'],
    'temp_f' : j['main']['temp'],
    'feels_like' : j['main']['feels_like'],
    'humidity': j['main']['humidity'],
    'wind_speed_mph' : j['wind']['speed'],
    'precipitation_mm_per_h': j.get('rain', {}).get('1h', 0),
    'snow_mm_per_h' : j.get('snow', {}).get('1h', 0),
    'timestampunix' : dt_object,
    'timestamp' : dt_object,
    'dateobj' : dt_object.strftime("%Y-%m-%d"),
    'timeobj': dt_object.strftime("%H:%M:%S"),
    'date1' : date1,
    'time1' : time1
    }
    df_new = pd.DataFrame([dict_])
    conn = sqlite3.connect("data/weather.db")

    df_new.to_sql('weather', conn, if_exists='append', index=False)
    time.sleep(1)
    # Close the connection
    conn.close()
    time.sleep(1)
