from sense_hat import SenseHat
from datetime import datetime
import os
import shutil
from logzero import logger
from datetime import datetime
HEADER = "time,yaw,pitch,roll,compassNorth,magnetometerX,magnetometerY,magnetometerZ,gyroscopeX,gyroscopeY,gyroscopeZ,accelerometerX,accelerometerY,accelerometerZ,humidity,temperature,pressure"

def create_folder(directory):
  folder = directory
  os.makedirs(folder, exist_ok = True)
  csvPath = os.path.join(folder, "data.csv")
  file = open(csvPath, "w")
  imageIndex = len([f for f in os.listdir(folder) if f.endswith('.jpg')])
  file.write(HEADER + '\n')
  sense_hat = SenseHat()

def retrieve_data():
    orientation = self.sense_hat.get_orientation()
    compassNorth = self.sense_hat.get_compass()
    magnetometer = self.sense_hat.get_compass_raw()
    gyroscope = self.sense_hat.get_gyroscope_raw()
    accelerometer = self.sense_hat.get_accelerometer_raw()
    humidity = self.sense_hat.get_humidity()
    temperature = self.sense_hat.get_temperature()
    pressure = self.sense_hat.get_pressure()

    dataExact = [datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f'),orientation['yaw'],orientation['pitch'],orientation['roll'],compassNorth,magnetometer['x'],magnetometer['y'],magnetometer['z'],gyroscope['x'],gyroscope['y'],gyroscope['z'],accelerometer['x'],accelerometer['y'],accelerometer['z'],humidity,temperature,pressure]
    dataRounded = [round(x, 2) if isinstance(x, float) else x for x in dataExact]

    dataStr = ",".join(map(str, dataRounded))
    self.file.write(dataStr + '\n')
    dataRoundedStr = ",".join(map(str, dataRounded))
    logger.info(f"Recorded Data: {dataRoundedStr}")

def copyImage(path)
  
  

  
