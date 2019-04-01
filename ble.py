import bluetooth

while True:
    print("Scanning...")
    nearbyDevices = bluetooth.discover_devices()

    for macAddress in nearbyDevices:
        if '40:4E:36:A9:DF:4D' in macAddress:
            print("Muggle's Pixel2 Found")
            # push to pushbullet
            # TODO finish pushbullet 
