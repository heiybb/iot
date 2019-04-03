import bluetooth

from monitorAndNotify import MonitorData
from push_service import PushThread


class BLENotify:
    @staticmethod
    def ble_search_notify():
        attempt = 10
        while attempt > 0:
            print("Scanning...")
            nearby_devices = bluetooth.discover_devices()

            for mac_address in nearby_devices:
                if '40:4E:36:A9:DF:4D' in mac_address:
                    print("Muggle's Pixel2 Found")
                    mon = MonitorData()
                    PushThread('BLE Notify', mon.to_string()).start()
                    return

            attempt = attempt - 1
            print("Remain attempts:", attempt)


if __name__ == '__main__':
    BLENotify.ble_search_notify()
