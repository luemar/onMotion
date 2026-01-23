from pushbullet import Pushbullet
pb = Pushbullet("o.CZT6a02IxSwl42MOgnWNzX8qCadA9dRV")

for device in pb.devices:
    print(f"Device: {device.nickname}")
    print(f"Has SMS: {hasattr(device, 'push_sms')}")
