import pygatt

service_uuid = '7b183224-9168-443e-a927-7aeea07e8105'
count_uuid = '292bd3d2-14ff-45ed-9343-55d125edb721'
rw_uuid = '56cd7757-5f47-4dcd-a787-07d648956068'
data_uuid = 'fec26ec4-6d71-4442-9f81-55bc21d658d6'

print("Trying to find bluetooth adapter")
adapter = pygatt.BGAPIBackend()
print("initialize BT adapter")
adapter.start()
print("Trying to find NIST ET devices")
devices = adapter.scan(timeout=3  )
et_devices = []
for d in devices:
    if 'NIST' in d['name']:
        et_devices.append(d)
        print(d['name'], d['address'])

for d in et_devices:
    print("Connecting...")
    device = adapter.connect(d['address'], timeout=1)
    print("Read rw")
    rw_value = device.char_read(rw_uuid, timeout=1)
    print(d['name'], count_value)
    device.disconnect()

adapter.stop()

