from pushbullet import Pushbullet
pb = Pushbullet("o.CZT6a02IxSwl42MOgnWNzX8qCadA9dRV")
   
print("Devices:", pb.devices)
pb.push_note("Test", "Hello from RPi")
