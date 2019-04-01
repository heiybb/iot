"""
Generate csv file according to the data selected from the database
"""
import csv

import jsonlib
import sqlite_lib

CSV_FILE = './report.csv'


def main():
    """
    Mark different status according to the json file bound limit
    :return: None
    """
    with open(CSV_FILE, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Date", "Status"])
        csv_data = sqlite_lib.get_csv_data()
        for row in csv_data:
            line = [row[0]]
            status = jsonlib.get_report_msg(row[1], row[2], row[3], row[4])
            # one of the value beyond the bound limit
            if status != '':
                line.append("BAD: " + status)
            # every value is normal
            else:
                line.append('OK')
            writer.writerow(line)


# Execute program.
if __name__ == "__main__":
    main()
