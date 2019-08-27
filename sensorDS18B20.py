import os
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices'
device_file = base_dir + '28-021491775f69' + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'f')
    lines = f.readLines()
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
        tem_c = float(temp_string) /1000
        return temp_c
    
while True:
    print read_temp()
    time.sleep(1)

        