import bluetooth

from monitorAndNotify import MonitorData
from push_service import PushThread

SEND = False
while not SEND:
    print("Scanning...")
    nearbyDevices = bluetooth.discover_devices()

    for macAddress in nearbyDevices:
        if '40:4E:36:A9:DF:4D' in macAddress:
            print("Muggle's Pixel2 Found")
            MON = MonitorData()
            PushThread('BLE Notify', MON.to_string()).start()
            SEND = True
            break
