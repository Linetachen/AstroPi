# Team: Piberry, Authors: Louise, 
#For mission SpaceLab
#Our code aims to use colour analysis to validate if the coordinates are actually matches
#TO DO: make error code, get sensor input, test on the actual pi, possibly play around with the colours of the input images

import os
from exif import Image
from datetime import datetime
import cv2
import math
import time
from time import sleep
from PIL import Image as pilimg
from PIL import *
from pathlib import Path
from picamera import PiCamera
from datetime import datetime

GSD = 0.1243 #for 5mm lens
numPhotos = 42
baseFolder = (Path(__file__).parent).resolve()
timeAllowed = 570 #9m30s
startTime = None
imageCount = 0
num = 0
count = 0


#function I made to take the pictures which I havent tested and probably should including some code I borrowed
def take_pictures(photos):
    camera = PiCamera()
    imageDir = baseFolder / "images"
    
    camera.start_preview()
    for i in range (photos):
        time.sleep(5)
        camera.capture((imageDir / f'image_{i}.jpg'))

    camera.stop_preview()
    camera.close()

def giveResult(value):
    with open(str(baseFolder / 'result.txt'), 'w') as file:
        file.write(f'speed = {value}')
        file.write(f'End time: {endTime.strftime('%Y-%m-%d %H:%M:%S')}') #no clue why theres an error here


def get_time(image): #opens the images and gets the time they were taken
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    return time

def get_time_difference(image_1, image_2): #gets the time difference
    time_1 = get_time(image_1)
    time_2 = get_time(image_2)
    time_difference = time_2 - time_1
    return time_difference.seconds

def convert_to_cv(image_1, image_2):#converts to cv (external python lib that uses NumPy and other stuff to do things with images)
    image_1_cv = cv2.imread(image_1,cv2.IMREAD_GRAYSCALE) # idk what that does. <--
    image_2_cv = cv2.imread(image_2,cv2.IMREAD_GRAYSCALE)
    return image_1_cv, image_2_cv
    
def calculate_features(image_1, image_2, feature_number):#uses ORB which is a complicated object detection software within opencv
    orb = cv2.ORB_create(nfeatures = feature_number)
    keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
    keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
    return keypoints_1, keypoints_2, descriptors_1, descriptors_2

def calculate_matches(descriptors_1, descriptors_2):#calculates the matches between the two images
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = brute_force.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):#clue in name of func- comment out destroy window line to see how it works 
    match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:100], None)
    resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
    cv2.imshow('matches', resize)
    cv2.waitKey(0)
    #cv2.destroyWindow('matches')
    
def find_matching_coordinates(keypoints_1, keypoints_2, matches):#finds the matching coordinates
    coordinates_1 = []
    coordinates_2 = []
    for match in matches:
        image_1_idx = match.queryIdx
        image_2_idx = match.trainIdx
        (x1,y1) = keypoints_1[image_1_idx].pt
        (x2,y2) = keypoints_2[image_2_idx].pt
        coordinates_1.append((x1,y1))
        coordinates_2.append((x2,y2))
    return coordinates_1, coordinates_2

def calculate_mean_distance(coordinates_1, coordinates_2):#clue in name of function
    all_distances = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference)
        all_distances = all_distances + distance
    return all_distances / len(merged_coordinates)
    
def calculate_speed_in_kmps(feature_distance, GSD, time_difference):#self explanatory (I hope)
    distance = feature_distance * GSD 
    speed = distance / time_difference
    return speed

def validate_matching_coordinates(image_1, image_2, coordinates_1, coordinates_2, sensitivity):
    img1 = pilimg.open(image_1)
    img2 = pilimg.open(image_2)

    res_1 = []
    res_2 = []
    
    diff_thr = sensitivity
    for i in range(len(coordinates_1)):
        c_1 = img1.getpixel((coordinates_1[i][0],coordinates_1[i][1]))
        c_2 = img2.getpixel((coordinates_2[i][0],coordinates_2[i][1]))
        
        diff = 0
        for j in range(3):
            diff += abs(c_1[j]-c_2[j])
        
        if(diff <= diff_thr):
            res_1.append(coordinates_1[i])
            res_2.append(coordinates_2[i])
    return res_1, res_2



#main code
startTime = datetime.now()
with open(str(baseFolder / 'result.txt'), 'w') as file:
        file.write(f'Start time: {startTime.strftime('%Y-%m-%d %H:%M:%S')}')


while (datetime.now() - startTime).total_seconds() < timeAllowed and imageCount <= numPhotos:
    camera = PiCamera()
    path = baseFolder / Path(f"./image{num}.jpg")
    camera.capture(path)
    num+=1
    camera.close()
    imageCount+=1
    time.sleep(5)
    if num >= 2:
        image_1 = f'image{num-1}.jpg'
        image_2 = f'image{num}.jpg'
        time_difference = get_time_difference(image_1, image_2) # Get time difference between images
        image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) # Create OpenCV image objects
        keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) # Get keypoints and descriptors
        matches = calculate_matches(descriptors_1, descriptors_2) # Match descriptors
        #display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches) # Display matches
        coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
        validated_coordinates_1, validated_coordinates_2 = validate_matching_coordinates(image_1, image_2, coordinates_1, coordinates_2, 50)
        average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
        speedTotal = speed + calculate_speed_in_kmps(average_feature_distance, GSD, time_difference)
        os.remove(f'image{num-1}.jpg')
        count+=1

endTime = datetime.now()
giveResult(speedTotal/count)

        