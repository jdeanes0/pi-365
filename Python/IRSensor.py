import evdev
import time
import sys
import subprocess
import threading
import ArrowAdjust
from collections import deque

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
            48910: "\n",
            2147483647: "err"
            }

def debounce_input():
    global recent_events
    if time.time() - timer > 0.2: 
        manage_timer()
        if len(recent_events) > 0:
            recent_events.pop()

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
    #print("increasing volume")
    return

def volume_down_proc():
    subprocess.run(["python", "VolumeAdjust.py", "--level", "-5"])    
    return

def get_ir_device():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if (device.name == "gpio_ir_recv"):
            print ("Ready for input!")
            sys.stdout.flush()
            return device
    print("no device found!")

def manage_timer():
    global timer
    timer = time.time()

dev = get_ir_device()

print("""Group Eleven:
    Austin Comeaux, Christian Pross, Jeremy Perando, Jonathan Eanes""")
print(list(range(48911, 48922)))

recent_events = deque()
active_threads = []

# debouncing timer to keep multiple inputs out
timer = time.time()
num_events = 0
while(True):
    event = dev.read_one()
    #debounce_input()
    if (event):
        if event.value == 0:
            continue
        if event.value in recent_events:
            debounce_input()
            continue
        debounce_input()
        num_events += 1
        print(num_events)

        recent_events.appendleft(event.value)
        clean_threads()
        #print("Raw value", event.value)
        #print("Recieved command", MASTER_KEY[event.value])
        if MASTER_KEY[event.value] != "err":
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
        #if MASTER_KEY[event.value] == 'up':
            #ArrowAdjust.scroll(10)   This is broken
            #print("Up")
        #if MASTER_KEY[event.value] == 'down':
            #ArrowAdjust.scroll(-10)
            #print("Down")
        #except:

        #print(event.value)
        sys.stdout.flush()

