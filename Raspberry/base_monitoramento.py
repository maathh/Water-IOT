import sys
import os
import glob
import time
import json
import firebase_admin

from datetime import datetime
from firebase_admin import credentials
from google.cloud import firestore

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

project_id = "smart-water-168ca"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/Desktop/smart-water-168ca-d9f996738e27.json"
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})
db = firestore.Client()
    
def generateID():
    data = datetime.now()
    sensorBase_ref = db.collection(u'sensorBase').document()
    sensorBase_ref.set({
        "registration": data,
        "location": ""
    })
    return sensorBase_ref.id
    
def getSensorBase_id():
    overwrite = False
    id_sensorBase = 0
    
    try:
        with open('sensorBase.json', 'r') as f:
            
            jsonfile = f.read()
            sensorBase_json = json.loads(jsonfile)

            if sensorBase_json['id_sensorBase'] == False:
                id_sensorBase = generateID()
                overwrite = True
            else:
                id_sensorBase = sensorBase_json['id_sensorBase']
                
    except:
        id_sensorBase = generateID()
        overwrite = True
        
    if overwrite == True:
        with open('sensorBase.json', 'w+') as f:   
            datastore = {"id_sensorBase": id_sensorBase}
            json.dump(datastore, f)
        
    return id_sensorBase

idSensorBase= getSensorBase_id()

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
        }
        
        return data

while True:

    jsonTemp = read_temp()
    data = datetime.now()
    jsonTemp['id_sensorBase'] =idSensorBase
    jsonTemp['datatime'] =data

    doc_base = db.collection(u'sensorBase/'+idSensorBase+"/sensorData")
    doc_base.add(jsonTemp)
    print("Deu Certo!")
    time.sleep(10)


