import requests
import sqlite3
from datetime import datetime
import os

cwd = os.path.dirname(os.path.realpath(__file__))

#db stuff
dire = f'{cwd}/records.db'
conn = sqlite3.connect(dire)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS data (ts, temp, humid, rad, window, feel, home);")

# fetch temp
temp = requests.get('http://pi.hole:8000/fetch').json()
state = requests.get('http://pi.hole:8000/state').json()

ts = datetime.now().replace(microsecond=0)
if temp:
    c.execute("""insert into data values (?, ?, ?, ?, ?, ?, ?);""",
              (ts, temp["temp"], temp["hum"], state["rad"], state["window"], state["feel"], state["home"]))
    conn.commit()
    print(f"[{ts}] Committed room temp!")
else:
    print(f"[{ts}] Failed to commit room temp!")

conn.close()
