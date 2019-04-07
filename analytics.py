from matplotlib import pyplot as plt
from pyecharts import Line

import sqlite_lib


class Analytics:
    @staticmethod
    def main():
        Analytics.gen_img_matplot()
        Analytics.gen_img_lib2()

    @staticmethod
    def gen_img_matplot():
        data = sqlite_lib.get_analytics_data()
        timestamp, temp_set, hum_set = [], [], []
        x_ticks = []
        # Split the data and inert into appropriate set
        for row in data:
            timestamp.append(row[0].split(" ")[1][:5])
            temp_set.append(row[1])
            hum_set.append(row[2])

        # Generate hour stamp from 00:00 to 24:00
        for hour_stamp in range(0, 25, 2):
            x_ticks.append("{:02}:00".format(hour_stamp))

        fig = plt.figure(dpi=320, figsize=(10, 5))
        ax1 = fig.add_subplot(1, 1, 1)
        ax2 = ax1.twinx()

        ax1.plot(timestamp, temp_set, 'r-')
        ax2.plot(timestamp, hum_set, 'b-')

        ax1.set_xticks(x_ticks)
        ax1.set_xticklabels(x_ticks, rotation=45)
        ax1.set_ylabel('Temperature(℃)', color='r')
        ax2.set_ylabel('Humidity(%)', color='b')
        ax1.set_title("2019-04-02 Temperature Humidity Line Chart")
        fig.autofmt_xdate()
        fig.savefig('matplot.png')
        # plt.show()

    @staticmethod
    def gen_img_lib2():
        data = sqlite_lib.get_analytics_echart_data()
        timestamp, temp_set, hum_set = [], [], []
        for row in data:
            timestamp.append(row[0])
            temp_set.append(row[1])
            hum_set.append(row[2])

        line = Line("Temperature Humidity Chart")
        line.add("Temperature", timestamp, temp_set,
                 mark_line=['average'], mark_point=["max", "min"], is_smooth=True)
        line.add("Humidity", timestamp, hum_set,
                 mark_line=['average'], mark_point=["max", "min"], is_smooth=True)
        line.render("TwoDayTH.html")


if __name__ == '__main__':
    ANL = Analytics()
    ANL.main()
