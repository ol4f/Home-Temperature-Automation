import xmltodict
import requests
import sqlite3
from datetime import datetime
import os

class Weather:
    def __init__(self, i):
        self.name = i["name"]
        self.phenomenon = i["phenomenon"]
        self.visibility = i["visibility"]
        self.precipitations = i["precipitations"]
        self.pressure = i["airpressure"]
        self.humidity = i["relativehumidity"]
        self.temperature = i["airtemperature"]
        self.windDirection = i["winddirection"]
        self.windSpeed = i["windspeed"]
        self.windSpeedMax = i["windspeedmax"]


def fetch_observations():
    data = xmltodict.parse(requests.get("https://www.ilmateenistus.ee/ilma_andmed/xml/observations.php").text)["observations"]
    return data

def get_station(observations, name):
    for station in observations["station"]:
        if station["name"] == name:
            return station

cwd = os.path.dirname(os.path.realpath(__file__))

#db stuff
dire = f'{cwd}/records.db'
conn = sqlite3.connect(dire)
c = conn.cursor()
sql = """CREATE TABLE IF NOT EXISTS weather (ts, temperature, humidity, pressure, phenomenon, precipitations, windSpeed, windSpeedMax, windDirection);"""
c.execute(sql)

w = Weather(get_station(fetch_observations(), "Tartu-Tõravere"))

ts = datetime.now().replace(microsecond=0, second=0, minute=0)
c.execute("""insert into weather values (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
          (ts, w.temperature, w.humidity, w.pressure, w.phenomenon, w.precipitations, w.windSpeed, w.windSpeedMax, w.windDirection))
conn.commit()
print(f"[{ts}] Committed weather!")
conn.close()
