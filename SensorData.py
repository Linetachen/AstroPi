from sense_hat import SenseHat
from datetime import datetime
import os
import shutil
from logzero import logger

DATA_CAPACITY_BYTES = 250000000  # 260MB
IMAGE_LIMIT = 41
APPROXIMATE_IMAGE_SIZE_BYTES = 5000000  # 5MB

HEADER = "time,yaw,pitch,roll,compassNorth,magnetometerX,magnetometerY,magnetometerZ,gyroscopeX,gyroscopeY,gyroscopeZ,accelerometerX,accelerometerY,accelerometerZ,humidity,temperature,pressure"

def record_sensor_data(sense_hat, file):
    """Records sensor data to the CSV file."""
    # Get sensor data
    orientation = sense_hat.get_orientation()
    compassNorth = sense_hat.get_compass()
    magnetometer = sense_hat.get_compass_raw()
    gyroscope = sense_hat.get_gyroscope_raw()
    accelerometer = sense_hat.get_accelerometer_raw()
    humidity = sense_hat.get_humidity()
    temperature = sense_hat.get_temperature()
    pressure = sense_hat.get_pressure()
    # Format data
    data_exact = [datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f'), orientation['yaw'], orientation['pitch'],
                  orientation['roll'], compassNorth, magnetometer['x'], magnetometer['y'], magnetometer['z'],
                  gyroscope['x'], gyroscope['y'], gyroscope['z'], accelerometer['x'], accelerometer['y'],
                  accelerometer['z'], humidity, temperature, pressure]
    data_rounded = [round(x, 2) if isinstance(x, float) else x for x in data_exact]
    # Write data to file
    data_str = ",".join(map(str, data_rounded))
    file.write(data_str + '\n')
    # Also record rounded values to the log
    data_rounded_str = ",".join(map(str, data_rounded))
    logger.info(f"Recorded Data: {data_rounded_str}")


def space_remaining(dump_folder):
    size = DATA_CAPACITY_BYTES
    """Returns True if there is enough space remaining to store a file of size 'size'."""
    return (DATA_CAPACITY_BYTES - sum(os.path.getsize(os.path.join(dump_folder, f)) for f in os.listdir(dump_folder) if os.path.isfile(os.path.join(dump_folder, f)))) < size

def dump_sensor_data(directory, image_path):
    """Manages dumping sensor data to a CSV and copies an image."""
    dump_folder = directory
    os.makedirs(dump_folder, exist_ok=True)

    csv_path = os.path.join(dump_folder, "data.csv")
    # Check if the file already exists
    file_exists = os.path.exists(csv_path)
    with open(csv_path, "a") as file:
        # Write header only if the file doesn't exist
        if not file_exists:
            file.write(HEADER + '\n')
        sense_hat = SenseHat()
        record_sensor_data(sense_hat, file)
