import array as arr
import numpy as np

import cv2


def boundingBoxFinder(path, debug=False):
    # Path for pictures
    print("Path: " + path)

    # Reads the picture by path and converts the color system to HSV
    image = cv2.imread(path)
    image_inv = ~image
    cv2.imwrite("image_inv.jpg", image_inv)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Range for lower red
    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    
    # Range for upper range
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_red,upper_red)
    
    # Generating the final mask to detect red color
    mask = mask1+mask2
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if debug:
        target = cv2.bitwise_and(image,image, mask=mask)
        cv2.imwrite("target.png", target)

    # Finds the biggest bounding box
    biggest_box = _find_biggest_box(contours)

    # informs if no red box was found
    if (len(biggest_box) == 0):
        raise Exception("Error: No red objects found!")

    # Coords for the bounding box converts from float to integer
    first_coord = np.array([int(biggest_box[1]), int(biggest_box[2])])
    second_coord = np.array([int(biggest_box[1] + biggest_box[3]), int(biggest_box[2])])
    third_coord = np.array([int(biggest_box[1]), int(biggest_box[2] + biggest_box[4])])
    fourth_coord = np.array([int(biggest_box[1] + biggest_box[3]), int(biggest_box[2] + biggest_box[4])])

    # Coords inserted into a tuple
    coords = np.array([first_coord, second_coord, third_coord, fourth_coord])

    if debug:
        img = cv2.rectangle(image, (int(biggest_box[1]), int(biggest_box[2])), (int(biggest_box[1]+biggest_box[3]), int(biggest_box[2]+biggest_box[4])), (0, 255, 0), 2)
        cv2.imwrite("box.jpg", img)

    return coords


def _find_biggest_box(contours):
    i = 0
    biggest_box = []
    biggest_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)

        if(area > 800):
            x, y, w, h = cv2.boundingRect(contour)
            box = arr.array('f', [area, x, y, w, h])

            # Checks if the new area is the biggest area
            if(box[0] >= biggest_area and _matches_flag_ratio(box[4], box[3])):
                biggest_area = box[0]       
                biggest_box = arr.array('f', [box[0], box[1], box[2], box[3], box[4]])

            i = i + 1

    return biggest_box


def _matches_flag_ratio(height, width):
    flag_height_width_ratio = 7.14

    return abs(height / width - flag_height_width_ratio) < 3
