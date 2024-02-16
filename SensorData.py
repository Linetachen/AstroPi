from sense_hat import SenseHat
from datetime import datetime
import os
import shutil
from logzero import logger

DATA_CAPACITY_BYTES = 260000000 # 260MB
IMAGE_LIMIT = 41
APPROXIMATE_IMAGE_SIZE_BYTES = 5000000 # 5MB

HEADER = "time,yaw,pitch,roll,compassNorth,magnetometerX,magnetometerY,magnetometerZ,gyroscopeX,gyroscopeY,gyroscopeZ,accelerometerX,accelerometerY,accelerometerZ,humidity,temperature,pressure"

def record_sensor_data(sense_hat, file):
    orientation = sense_hat.get_orientation()
    compassNorth = sense_hat.get_compass()
    magnetometer = sense_hat.get_compass_raw()
    gyroscope = sense_hat.get_gyroscope_raw()
    accelerometer = sense_hat.get_accelerometer_raw()
    humidity = sense_hat.get_humidity()
    temperature = sense_hat.get_temperature()
    pressure = sense_hat.get_pressure()

    data_exact = [datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f'), orientation['yaw'], orientation['pitch'], orientation['roll'], compassNorth, magnetometer['x'], magnetometer['y'], magnetometer['z'], gyroscope['x'], gyroscope['y'], gyroscope['z'], accelerometer['x'], accelerometer['y'], accelerometer['z'], humidity, temperature, pressure]
    data_rounded = [round(x, 2) if isinstance(x, float) else x for x in data_exact]

    data_str = ",".join(map(str, data_rounded))
    file.write(data_str + '\n')

    data_rounded_str = ",".join(map(str, data_rounded))
    logger.info(f"Recorded Data: {data_rounded_str}")

def copy_image(path, dump_folder):
    image_size = os.path.getsize(path)
    if not os.path.exists(path):
        logger.error(f"Image {path} does not exist. Could not copy to data folder.")
        return
    elif not space_remaining(dump_folder, image_size):
        logger.error(f"Insufficient space remaining to store image {path}.")
        return
    elif len([f for f in os.listdir(dump_folder) if f.endswith('.jpg')]) >= IMAGE_LIMIT:
        logger.error(f"Image limit reached. Could not store image {path}.")
        return
    else:
        image_name = f"image_{datetime.now().strftime('%Y-%m-%d_%H%M%S%f')}.jpg"
        image_path = os.path.join(dump_folder, image_name)
        shutil.copy(path, image_path)
        logger.info(f"Image {path} copied as {image_name}.")

def space_remaining(dump_folder, size):
    return (DATA_CAPACITY_BYTES - sum(os.path.getsize(os.path.join(dump_folder, f)) for f in os.listdir(dump_folder) if os.path.isfile(os.path.join(dump_folder, f)))) > size

def dump_sensor_data(directory):
    dump_folder = directory
    os.makedirs(dump_folder, exist_ok=True)

    csv_path = os.path.join(dump_folder, "data.csv")
    with open(csv_path, "w") as file:
        file.write(HEADER + '\n')
        sense_hat = SenseHat()

        while True:
            record_sensor_data(sense_hat, file)
            # Assuming path is the path to an image
            # copy_image(path, dump_folder)

if __name__ == "__main__":
    dump_sensor_data("your_directory_path")
