# Team: Piberry, Authors: Erik, Sam
from picamera import PiCamera
from time import sleep
from datetime import datetime
from pathlib import Path
from logzero import logger, logfile
from exif import Image
import numpy as np
import cv2
import os
import SensorData

# constants
ROOT_FOLDER = (Path(__file__).parent).resolve()
LOG_FILE = ROOT_FOLDER / "AstroPi.log"
RESOLUTION = (4056, 3040) # resolution of the Pi camera
CALCULATION_TIME = 570 #seconds, time allowed for speed calculation # MEANT TO BE 570
GSD = 0.1243 # Ground Sampling Distance, km per pixel
INTERVAL = 3 #seconds 

def getTime(imagePath):
    """Get the time the image was taken from the exif data of the image."""
    with open(imagePath, 'rb') as imageFile:
        image = Image(imageFile)
        return datetime.strptime(image.datetime, "%Y:%m:%d %H:%M:%S")

def distanceFromMatches(matches, kp1, kp2):
    """Calculate the pixel distance between the matched keypoints in the two images."""
    return np.mean([np.hypot(kp1[match.queryIdx].pt[0]-kp2[match.trainIdx].pt[0], kp1[match.queryIdx].pt[1]-kp2[match.trainIdx].pt[1]) for match in matches])

def getMatchesAndKeyPoints(image1, image2):
    """Get the matches and keypoints of the two images using Open CV."""
    orb = cv2.ORB_create()
    kp1, desc1 = orb.detectAndCompute(image1, None)
    kp2, desc2 = orb.detectAndCompute(image2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    return bf.match(desc1,desc2), kp1, kp2

def writeMeanSpeed(meanSpeed):
    """Write the mean speed to a file, to 6 characters."""
    with open(str(ROOT_FOLDER / "result.txt"), "w") as speedFile:
        speed = str(meanSpeed)
        speed = speed[:min(len(speed),6)]
        speedFile.write(speed)

def main():    
    # setup camera
    camera = PiCamera()
    camera.resolution = RESOLUTION

    imagePaths = [] # list of captured image paths
    meanSpeed = 0 # mean calculated speed
    speedCalcCounter = 0 # number of speeds calculated

    # capture images and calculate speed within the runtime
    while (datetime.now() - startTime).total_seconds() < CALCULATION_TIME:
        current_image_path = ROOT_FOLDER / f"image{len(imagePaths)}.jpg"
        if SensorData.space_remaining(ROOT_FOLDER):
            camera.capture(str(current_image_path))
            imagePaths.append(current_image_path)
            logger.info(f"Successfully took image {len(imagePaths)}.")
        else:
            logger.warning(SensorData.space_remaining(ROOT_FOLDER))
            logger.warning("Unable to store image, capacity exceeded")

        # calculate speed if there are at least two images
        if len(imagePaths) > 2:
            # consider last two images for speed calculation
            oldStrPath = str(imagePaths[-2])
            oldImage = cv2.imread(oldStrPath)
            oldImageTime = getTime(oldStrPath)
            newStrPath = str(imagePaths[-1])
            newImage = cv2.imread(newStrPath)
            newImageTime = getTime(newStrPath)
            timeDelta = (newImageTime - oldImageTime).total_seconds()

            # compute matches and keypoints using cv2
            matches, kp1, kp2 = getMatchesAndKeyPoints(oldImage, newImage)

            # calculate speed if there are matches
            if len(matches) > 0:
                speed = distanceFromMatches(matches, kp1, kp2)*GSD/timeDelta
                if(6.3<=speed<=8.9):
                    meanSpeed = (meanSpeed*speedCalcCounter + speed)/(speedCalcCounter+1)
                    speedCalcCounter += 1
                    logger.info(f"Speed: {speed} km/s, Mean speed: {meanSpeed} km/s")
                else:
                    logger.info(f"Speed {speed} km/s was too high/low and rejected as an outlier")
        if speedCalcCounter%3==0:
            SensorData.dump_sensor_data(ROOT_FOLDER,current_image_path)
        sleep(INTERVAL) # wait before taking next image

    camera.close()

    # delete images
    imageKeepInterval = np.ceil(len(imagePaths)/40)
    for i in range(len(imagePaths)):
        if i % imageKeepInterval != 0:
            os.remove(str(imagePaths[i])) 

    # write mean speed to file
    writeMeanSpeed(meanSpeed)

# entry point
if __name__ == "__main__":
    startTime = datetime.now()
    logfile(str(LOG_FILE))

    try:
        main()
    except Exception as e:
        logger.error(e)
        # raise e # uncomment to rethrow the exception. Useful when debugging.
    finally:
        logger.info("Program ended.")
