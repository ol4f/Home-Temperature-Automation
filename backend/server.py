from fastapi import FastAPI, HTTPException
import serial
import time
import json
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import sqlite3

linux = True

if linux: device = '/dev/ttyUSB0'
else: device = 'COM9'

arduino = serial.Serial(device, 1200, timeout=1)

if arduino.isOpen():
    print("{} connected!".format(arduino.port))
app = FastAPI()

cwd = os.path.dirname(os.path.realpath(__file__))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

values = {"rad": 3.5, "window": "closed", "feel": "ok", "home": 1}

def read_config():
    with open(f'{cwd}/config.json', encoding="UTF-8") as f:
        return json.load(f)

def write_config(cfg):
    try:
        with open(f'{cwd}/config.json', "w", encoding="UTF-8") as f:
            json.dump(cfg, f)
    except Exception as e:
        raise e

    #write config if doesn't exist
try:
    if read_config() == {}:
        with open(f'{cwd}/config.json', "w", encoding="UTF-8") as f:
            json.dump(values, f)
except:
    with open(f'{cwd}/config.json', "w", encoding="UTF-8") as f:
        json.dump(values, f)

values = read_config()

class Values(BaseModel):
    rad: float
    window: str
    feel: str
    home: int

def get_temp():
    try:
        while True:
            cmd = "1"
            arduino.write(cmd.encode())
            time.sleep(0.1) #wait for arduino to answer
            while arduino.inWaiting() == 0: pass
            if arduino.inWaiting() > 0:
                answer = arduino.readline()
                return json.loads(answer.decode("utf-8").strip())
    except:
        raise

def get_data():
    try:
        dire = f'{cwd}/records.db'
        conn = sqlite3.connect(dire)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        sql_temp = """select * from data;"""
        sql_weather = """select * from weather;"""

        temp_data = [dict(row) for row in c.execute(sql_temp).fetchall()]
        weather_data = [dict(row) for row in c.execute(sql_weather).fetchall()]
        return {"temperature": temp_data, "weather": weather_data}

    except:
        raise

@app.get("/")
async def root():
    try:
        return {"message": "Hello World"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))

@app.get("/fetch")
async def fetch():
    try:
        return get_temp()
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))

@app.get("/history")
async def history():
    try:
        return get_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))

@app.put("/state")
async def put_values(val: Values):
    try:
        if val.rad:
            values["rad"] = val.rad
        if val.window:
            values["window"] = val.window
        if val.feel:
            values["feel"] = val.feel
        if val.home:
            values["home"] = val.home

        write_config(values)
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))

@app.get("/state")
async def get_values():
    try:
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))
