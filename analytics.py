from matplotlib import pyplot as plt

import sqlite_lib

dates, temp, hum = [], [], []

data = sqlite_lib.get_analytics_data()
print(data)

for row in data:
    dates.append(row[0])
    temp.append(row[1])
    hum.append(row[2])

fig = plt.figure(dpi=320, figsize=(8, 5))
ax = fig.add_subplot(111)
ax.plot(dates, temp, '-', label='Temperature')
ax2 = ax.twinx()
ax2.plot(dates, hum, '-r', label='Humidity')

fig.legend(loc=1, bbox_to_anchor=(1, 1), bbox_transform=ax.transAxes)

# ax.set_xlabel("Date")
ax.set_ylabel("Temperature (F)")
ax2.set_ylabel("Humidity (%)")

# fig.autofmt_xdate()
plt.legend()
plt.show()
plt.savefig('0.png')
