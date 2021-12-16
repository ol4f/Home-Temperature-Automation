import requests
import os
import matplotlib.pyplot as plt
from datetime import datetime

cwd = os.path.dirname(os.path.realpath(__file__))

data = requests.get("http://pi.hole:8000/history").json()["temperature"]

print(data)

time = list()
temp = list()
humid = list()

for i in data:
    time.append(datetime.strptime(i["ts"], "%Y-%m-%d %H:%M:%S"))

for i in data:
    temp.append(float(i["temp"]))

for i in data:
    humid.append(float(i["humid"]))

fig, ax1 = plt.subplots(figsize=(10, 6), dpi=100)

color = 'tab:blue'
ax1.set_xlabel('Datetime')
ax1.set_ylabel('Temperature (°C)', color=color)
ax1.plot(time, temp, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:orange'
ax2.set_ylabel('Humidity (%)', color=color)  # we already handled the x-label with ax1
ax2.plot(time, humid, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()