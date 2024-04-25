import evdev
import time
import sys
import subprocess
import threading
import ArrowAdjust

MASTER_KEY = {
            48912: 1,
            48913: 2,
            48914: 3,
            48916: 4,
            48917: 5,
            48918: 6,
            48920: 7,
            48921: 8,
            48922: 9,
            48896: "volume-",
            48897: "pause",
            48898: "volume+",
            48900: "setup",
            48902: "stop",
            48901: "up",
            48906: "right",
            48909: "down",
            48904: "left",
            48905: "enter",
            48908: 0,
            48910: "\n"
            }
def clean_threads():
    global active_threads
    dead_threads = [t for t in active_threads if not t.is_alive()]
    for t in dead_threads:
        t.join()
    active_threads = [t for t in active_threads if t.is_alive()]

def firefox_proc():
    subprocess.run(["firefox"])    
    return

def volume_up_proc():
    subprocess.run(["python", "VolumeAdjust.py", "--level", "5"])    
    print("increasing volume")
    return

def volume_down_proc():
    subprocess.run(["python", "VolumeAdjust.py", "--level", "-5"])    
    return


def get_ir_device():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if (device.name == "gpio_ir_recv"):
            print ("Using device", device.path, "n")
            sys.stdout.flush()
            return device
    print("no device found!")

dev = get_ir_device()

print("""Group Eleven:
    Austin Comeaux, Christian Pross, Jeremy Perando, Jonathan Eanes""")
print(list(range(48911, 48922)))

active_threads = []
while(True):
    event = dev.read_one()
    if (event):
        if event.value == 0:
            continue
        #try:

        clean_threads()
        print("Raw value", event.value)
        print("Recieved command", MASTER_KEY[event.value])
        print(MASTER_KEY[event.value])
        sys.stdout.flush()
        if MASTER_KEY[event.value] == 0:
            t1 = threading.Thread(target=firefox_proc)
            t1.start()
            active_threads.append(t1)
        if MASTER_KEY[event.value] == 'volume+':
            t1 = threading.Thread(target=volume_up_proc)
            t1.start()
            active_threads.append(t1)
        if MASTER_KEY[event.value] == 'volume-':
            t1 = threading.Thread(target=volume_down_proc)
            t1.start()
            active_threads.append(t1)
        if MASTER_KEY[event.value] == 'up':
            ArrowAdjust.scroll(10)
        if MASTER_KEY[event.value] == 'down':
            ArrowAdjust.scroll(-10)
        time.sleep(.1)
        #except:

        print(event.value)
        sys.stdout.flush()

