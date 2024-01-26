# import a load of libraries to make stuff easier
from exif import Image
from datetime import datetime
import cv2
import math
import time
from PIL import Image as pilimg

while True:
    print("git gud")

start_time = time.time()
def get_time(image):
    with open(image, 'rb') as image_file: # open the image
        img = Image(image_file)
        time_str = img.get("datetime_original") # get the time at which the image was taken
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    return time
    
    
def get_time_difference(image_1, image_2):
    time_1 = get_time(image_1) # finds the time when image 1 was taken
    time_2 = get_time(image_2) # finds the time when image 2 was taken
    time_difference = time_2 - time_1
    return time_difference.seconds # returns the difference


def convert_to_cv(image_1, image_2): # idk what a cv is
    image_1_cv = cv2.imread(image_1, 0)
    image_2_cv = cv2.imread(image_2, 0)
    return image_1_cv, image_2_cv


def calculate_features(image_1, image_2, feature_number): # I think this uses some code from the library to identify things in the images
    orb = cv2.ORB_create(nfeatures = feature_number)
    keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
    keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
    return keypoints_1, keypoints_2, descriptors_1, descriptors_2


def calculate_matches(descriptors_1, descriptors_2): # uses more code from the library
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = brute_force.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches
    

def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
    match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:100], None)
    resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
    cv2.imshow('matches', resize)
    cv2.waitKey(0)
    cv2.destroyWindow('matches')
    
    
def find_matching_coordinates(keypoints_1, keypoints2, matches): # finds the co-ordinates of the features
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


def calculate_mean_distance(coordinates_1, coordinates_2): # finds the distance between them
    all_distances = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference)
        all_distances = all_distances + distance
    return all_distances / len(merged_coordinates)


def calculate_speed_in_kmps(feature_distance, GSD, time_difference): # divides the distance by the time to get the speed that the camera is travelling
    distance = feature_distance * GSD / 100000
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
    
    


#image_1 = 'photo_07464.jpg'
#image_2 = 'photo_07465.jpg'
#speed = 7.255443210895204
#new_speed = 6.212950503281697

image_1 = 'photo_07004.jpg'
image_2 = 'photo_07005.jpg'
#speed = 11.527350516701844
#new_speed = 9.7389745988263

#image_1 = 'photo_07003.jpg'
#image_2 = 'photo_07004.jpg'
#speed = 7.528906993825855

#image_1 = 'photo_06313.jpg'
#image_2 = 'photo_06314.jpg'
#speed = 5.64648007478286

#image_1 = 'photo_06312.jpg'
#image_2 = 'photo_06313.jpg'
#speed = 6.2210706544142935

#image_1 = 'photo_05516.jpg'
#image_2 = 'photo_05517.jpg'
#speed = 6.707820556434495

#image_1 = 'photo_05515.jpg'
#image_2 = 'photo_05516.jpg'
#speed = 10.485076638039637

#image_1 = 'photo_01934.jpg'
#image_2 = 'photo_01935.jpg'
#speed = 9.24535211665262

#image_1 = 'photo_01933.jpg'
#image_2 = 'photo_01934.jpg'
#speed = 8.85116509420096

#image_1 = 'photo_01931.jpg'
#image_2 = 'photo_01932.jpg'
#speed = 8.692062912404847

#image_1 = 'photo_01929.jpg'
#image_2 = 'photo_01930.jpg'
#speed = 7.145185430170688

#image_1 = 'photo_1760.jpg'
#image_2 = 'photo_1761.jpg'
#speed = 2.0302498517875107

#image_1 = 'photo_1758.jpg'
#image_2 = 'photo_1759.jpg'
#speed = 2.0888690569461397

#image_1 = 'photo_1756.jpg'
#image_2 = 'photo_1757.jpg'
#speed = 2.139276714445157

#image_1 = 'photo_1754.jpg'
#image_2 = 'photo_1755.jpg'
#speed = 2.2288706053420655

#image_1 = 'photo_1752.jpg'
#image_2 = 'photo_1753.jpg'
#speed = 2.272836241275956

#image_1 = 'photo_1750.jpg'
#image_2 = 'photo_1751.jpg'
#speed = 2.6409245764344123

#image_1 = 'photo_1748.jpg'
#image_2 = 'photo_1749.jpg'
#speed = 2.208142791391556

#image_1 = 'photo_1746.jpg'
#image_2 = 'photo_1747.jpg'
#speed = 2.580619485972105

#image_1 = 'photo_1744.jpg'
#image_2 = 'photo_1745.jpg'
#speed = 2.13177392365962

#image_1 = 'photo_1742.jpg'
#image_2 = 'photo_1743.jpg'
#speed = 2.1966494892614525

#image_1 = 'photo_0686.jpg'
#image_2 = 'photo_0687.jpg'
#speed = 7.696443390013672

#image_1 = 'photo_0684.jpg'
#image_2 = 'photo_0685.jpg'
#speed = 7.904148842067634

#image_1 = 'photo_0682.jpg'
#image_2 = 'photo_0683.jpg'
#speed = 8.899269644172081

#image_1 = 'photo_0681.jpg'
#image_2 = 'photo_0682.jpg'
#speed = 11.140909556537332

#image_1 = 'photo_0679.jpg'
#image_2 = 'photo_0680.jpg'
#speed = 16.87536695144639

#image_1 = 'photo_0677.jpg'
#image_2 = 'photo_0678.jpg'
#speed = 7.681244528890498

#image_1 = 'photo_0675.jpg'
#image_2 = 'photo_0676.jpg'
#speed = 8.336407492269805

#image_1 = 'photo_0673.jpg'
#image_2 = 'photo_0674.jpg'
#speed = 8.450693100227497

#image_1 = 'photo_00154.jpg'
#image_2 = 'photo_00155.jpg'
#speed = 11.315244704839845 



time_difference = get_time_difference(image_1, image_2) #get time difference between images
image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) #create opencfv images objects
keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) #get keypoints and descriptors
matches = calculate_matches(descriptors_1, descriptors_2) #match descriptors
#display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches) #display matches
coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)
print(speed)


validated_coordinates_1, validated_coordinates_2 = validate_matching_coordinates(image_1, image_2, coordinates_1, coordinates_2, 50)
average_feature_distance = calculate_mean_distance(validated_coordinates_1, validated_coordinates_2)
speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)


print(str(len(validated_coordinates_1)) + "/"+str(len(coordinates_1))+" coordinates validated. New speed: " + str(speed))


# uhhhhhhhhhhhhhhhhhhhhh.....


  ____ ___ _____    ____ _   _ ____  
 / ___|_ _|_   _|  / ___| | | |  _ \ 
| |  _ | |  | |   | |  _| | | | | | |
| |_| || |  | |   | |_| | |_| | |_| |
 \____|___| |_|    \____|\___/|____/ 
  ____ ___ _____    ____ _   _ ____  
 / ___|_ _|_   _|  / ___| | | |  _ \ 
| |  _ | |  | |   | |  _| | | | | | |
| |_| || |  | |   | |_| | |_| | |_| |
 \____|___| |_|    \____|\___/|____/ 
  ____ ___ _____    ____ _   _ ____  
 / ___|_ _|_   _|  / ___| | | |  _ \ 
| |  _ | |  | |   | |  _| | | | | | |
| |_| || |  | |   | |_| | |_| | |_| |
 \____|___| |_|    \____|\___/|____/ 
  ____ ___ _____    ____ _   _ ____  
 / ___|_ _|_   _|  / ___| | | |  _ \ 
| |  _ | |  | |   | |  _| | | | | | |
| |_| || |  | |   | |_| | |_| | |_| |
 \____|___| |_|    \____|\___/|____/ 
  ____ ___ _____    ____ _   _ ____  
 / ___|_ _|_   _|  / ___| | | |  _ \ 
| |  _ | |  | |   | |  _| | | | | | |
| |_| || |  | |   | |_| | |_| | |_| |
 \____|___| |_|    \____|\___/|____/ 
  ____ ___ _____    ____ _   _ ____  
 / ___|_ _|_   _|  / ___| | | |  _ \ 
| |  _ | |  | |   | |  _| | | | | | |
| |_| || |  | |   | |_| | |_| | |_| |
 \____|___| |_|    \____|\___/|____/ 
  ____ ___ _____    ____ _   _ ____  
 / ___|_ _|_   _|  / ___| | | |  _ \ 
| |  _ | |  | |   | |  _| | | | | | |
| |_| || |  | |   | |_| | |_| | |_| |
 \____|___| |_|    \____|\___/|____/ 
  ____ ___ _____    ____ _   _ ____  
 / ___|_ _|_   _|  / ___| | | |  _ \ 
| |  _ | |  | |   | |  _| | | | | | |
| |_| || |  | |   | |_| | |_| | |_| |
 \____|___| |_|    \____|\___/|____/ 
  ____ ___ _____    ____ _   _ ____  
 / ___|_ _|_   _|  / ___| | | |  _ \ 
| |  _ | |  | |   | |  _| | | | | | |
| |_| || |  | |   | |_| | |_| | |_| |
 \____|___| |_|    \____|\___/|____/ 

