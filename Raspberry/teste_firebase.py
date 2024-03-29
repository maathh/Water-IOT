import json
import os
import glob
import time
from datetime import datetime
from firebase import firebase

urlFirebase = "https://smart-water-168ca.firebaseio.com/"
user = "admin"

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

firebase = firebase.FirebaseApplication(urlFirebase)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        
        data = {
            "celsius": temp_c,
            "fahrenheit": temp_f,
        }
        
        return data

result = firebase.get('/one', None)

while True:
    jsonTemp = read_temp()
    data = datetime.now()
    jsonTemp['datatime'] =data
    firebase.post('/user/'+user,jsonTemp)
    print(jsonTemp)
    time.sleep(60)
