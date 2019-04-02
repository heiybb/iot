from matplotlib import pyplot as plt
import sqlite_lib

timestamp, temp, hum, xTicks = [], [], [], []

data = sqlite_lib.get_analytics_data()

# print(data)

for row in data:
    timestamp.append(row[0].split(" ")[1][:5])
    temp.append(row[1])
    hum.append(row[2])

for x in range(0, 25, 2):
    xTicks.append("{:02}:00".format(x))

fig = plt.figure(dpi=320, figsize=(10, 5))
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()

ax1.plot(timestamp, temp, 'r-')
ax2.plot(timestamp, hum, 'b-')

ax1.set_xticks(xTicks)
ax1.set_ylabel('Temperature(℃)', color='r')
ax2.set_ylabel('Humidity(%)', color='b')

fig.autofmt_xdate()
fig.savefig('matplot.png', dpi=fig.dpi)
plt.show()
