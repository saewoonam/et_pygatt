import pygatt
import sys
import time

service_uuid = '7b183224-9168-443e-a927-7aeea07e8105'
count_uuid = '292bd3d2-14ff-45ed-9343-55d125edb721'
rw_uuid = '56cd7757-5f47-4dcd-a787-07d648956068'
data_uuid = 'fec26ec4-6d71-4442-9f81-55bc21d658d6'

print("Trying to find bluetooth adapter")
adapter = pygatt.GATTToolBackend()
adapter.start()
devices = adapter.scan(run_as_root=True, timeout=3  )
name = sys.argv[1]

if False:
    #adapter = pygatt.BGAPIBackend()
    print("initialize BT adapter")
    adapter.start()
    print("Trying to find NIST ET devices")
    devices = adapter.scan(run_as_root=True, timeout=3  )
# devices = adapter.scan(timeout=10  )
et_devices = []
for d in devices:
    if d['name'] is not None:
        if 'NIST' in d['name']:
            et_devices.append(d)
            print(d['name'], d['address'])
            if name==d['name']:
                print("found")
                break
global done
done = False
def data_handler_cb(handle, value):
    """
        Indication and notification come asynchronously, we use this function to
        handle them either one at the time as they come.
    :param handle:
    :param value:
    :return:
    """
    global done
    print(f"Data: {value}")
    done = True

if True:
    print("Connecting ",d['name'])
    connected = False
    if not connected:
        try:
            device = adapter.connect(d['address'])
            connected = True
            print("Read rw")
            rw_value = device.char_read(rw_uuid)
            print(d['name'], rw_value)
            count = device.char_read(count_uuid)
            count = int.from_bytes(count, byteorder='little')
            print(d['name'], count)
            device.subscribe(data_uuid, callback=data_handler_cb, indication=False)
            device.char_write(rw_uuid, b'I')
            while not done:
                time.sleep(0.01)
            device.disconnect()
        except Exception as e:
            print(e)
            # print('trying again')

adapter.stop()

