import socket
import struct
import threading

LOCATION_TIME=0          
LOCATION_LAPTIME=1       
LOCATION_LAPDISTANCE=2
LOCATION_TOTALDISTANCE=3
LOCATION_X=4
LOCATION_Y=5
LOCATION_Z=6
LOCATION_SPEED=7
LOCATION_XV=8
LOCATION_YV=9
LOCATION_ZV=10
LOCATION_XR=11
LOCATION_YR=12
LOCATION_ZR=13
LOCATION_XD=14
LOCATION_YD=15
LOCATION_ZD=16
LOCATION_SUSP_POS_BL=17
LOCATION_SUSP_POS_BR=18
LOCATION_SUSP_POS_FL=19
LOCATION_SUSP_POS_FR=20
LOCATION_SUSP_VEL_BL=21
LOCATION_SUSP_VEL_BR=22
LOCATION_SUSP_VEL_FL=23
LOCATION_SUSP_VEL_FR=24
LOCATION_WHEEL_SPEED_BL=25
LOCATION_WHEEL_SPEED_BR=26
LOCATION_WHEEL_SPEED_FL=27
LOCATION_WHEEL_SPEED_FR=28
LOCATION_THROTTLE=29
LOCATION_STEER=30
LOCATION_BRAKE=31
LOCATION_CLUTCH=32
LOCATION_GEAR=33
LOCATION_GFORCE_LAT=34
LOCATION_GFORCE_LON=35
LOCATION_LAP=36
LOCATION_ENGINERATE=37
LOCATION_SLI_PRO_NATIVE_SUPPORT=38
LOCATION_CAR_POSITION=39
LOCATION_KERS_LEVEL=40
LOCATION_KERS_MAX_LEVEL=41
LOCATION_DRS=42
LOCATION_TRACTION_CONTROL=43
LOCATION_ANTI_LOCK_BRAKES=44
LOCATION_FUEL_IN_TANK=45
LOCATION_FUEL_CAPACITY=46
LOCATION_IN_PITS=47
LOCATION_SECTOR=48
LOCATION_SECTOR1_TIME=49
LOCATION_SECTOR2_TIME=50
LOCATION_BRAKES_TEMP=51
LOCATION_WHEELS_PRESSURE=52
LOCATION_TEAINFO=53
LOCATION_TOTAL_LAPS=54
LOCATION_TRACK_SIZE=55
LOCATION_LAST_LAP_TIME=56
LOCATION_MAX_RPM=57
LOCATION_IDLE_RPM=58
LOCATION_MAX_GEARS=59
LOCATION_SESSIONTYPE=61
LOCATION_DRSALLOWED=62
LOCATION_TRACK_NUMBER=63
LOCATION_VEHICLEFIAFLAGS=64

DIRT_IP = ""
DIRT_PORT = 20777

import tkinter as tk

root = tk.Tk()
root.title("Telemetry")
root.attributes('-topmost', True)

canvas = tk.Canvas(root, width=800, height=100, bg="white")
rpmLine = canvas.create_line(0, 0, 0, 0, fill="blue", width=150)
canvas.pack(fill='none', expand=False, pady=0, padx=0,)

labelGear = tk.Label(root,pady=0, text="0", font=("Helvetica", 300))
labelSpeed = tk.Label(root,pady=0, text="0 km/h", font=("Helvetica", 20))

labelGear.pack(fill='none', expand=False, pady=0, padx=0)
labelSpeed.pack(fill='none', expand=False, pady=0, padx=0)

baseX=90
baseY=90

sizeX=100
sizeY=5

spaceX=25

gearBoxes = [None] * 6

for i in range(5):

    extraHeight=0

    match i+1:
        case 1:
            extraHeight=0
        case 2:
            extraHeight=2
        case 3:
            extraHeight=5
        case 4:
            extraHeight=2
        case 5:
            extraHeight=0

    gearBoxes[i+1] = canvas.create_rectangle(baseX + sizeX * i + spaceX*i, baseY, baseX + spaceX * i + sizeX * (i+1), baseY + sizeY + extraHeight, outline="lightGray", fill="lightGray", width=4)

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock.bind((DIRT_IP, DIRT_PORT))
sock.settimeout(3600)

print(f"Connected")

def listenSocket():
    while True:
        try:
            data, addr = sock.recvfrom(4096)
            text = struct.unpack('f' * (len(data) // 4), data)         
            root.after(0, updateUi, text)
        except KeyboardInterrupt:
            print("Execution ended")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

def updateUi(text):
    gear = int(text[LOCATION_GEAR])
    labelGear.config(text=f"{gear}")
    labelSpeed.config(text=f"{round(text[LOCATION_SPEED]*3.6,1)} km/h")
    canvas.coords(rpmLine,0, 0, text[LOCATION_ENGINERATE]/200*100*2, 0)
    if text[LOCATION_ENGINERATE] < 640:
        canvas.itemconfig(rpmLine, fill="green")
    elif text[LOCATION_ENGINERATE] < 736:
        canvas.itemconfig(rpmLine, fill="yellow")
    else:
        canvas.itemconfig(rpmLine, fill="red")

    canvas.itemconfig(gearBoxes[1], fill="lightGray")
    canvas.itemconfig(gearBoxes[2], fill="lightGray")
    canvas.itemconfig(gearBoxes[3], fill="lightGray")
    canvas.itemconfig(gearBoxes[4], fill="lightGray")
    canvas.itemconfig(gearBoxes[5], fill="lightGray")
     
    if gear > 0:
        canvas.itemconfig(gearBoxes[gear], fill="purple")

thread = threading.Thread(target=listenSocket, daemon=True)
thread.start()

root.mainloop()