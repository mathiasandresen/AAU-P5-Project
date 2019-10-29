import cv2
import numpy as np 
import array as arr

def boundingBoxFinder(path):
    #Path for pictures
    #path = r'C:\Users\choko\OneDrive\Dokumenter\Python\ImageStuff\test.jpg'

    #Reads the picture by path
    image = cv2.imread(path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    cv2.namedWindow('Tracking', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Tracking', 600,600)
    cv2.imshow('Tracking', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #HSV range for the color red
    lower_red = np.array([161, 155, 84])
    upper_red = np.array([179, 255, 255])

    #Mask after the HSV colors and contours 
    mask = cv2.inRange(hsv, lower_red, upper_red)
    (contours,_) = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0
    biggestBox = []
    biggestArea = 0

    #Finds the biggest bounding box
    for contour in contours:
        area = cv2.contourArea(contour)
    
        if(area > 800):
            x, y, w, h = cv2.boundingRect(contour)
            box = arr.array('f', [area, x, y, w, h])

            if(box[0] >= biggestArea): 
                biggestArea = box[0]       
                biggestBox = arr.array('f', [box[0], box[1], box[2], box[3], box[4]])
    
            i = i + 1

    #Creates a rectangle on the biggest colored object
    image = cv2.rectangle(image, (int (biggestBox[1]), int (biggestBox[2])), (int (biggestBox[1]) + int (biggestBox[3]), int (biggestBox[2]) + int (biggestBox[4])),(0,0,255), 5)

    #Coords for the bounding box converts from float to integer
    firstCoord = (int (biggestBox[1]), int (biggestBox[2]))
    secondCoord = (int (biggestBox[1] + biggestBox[3]), int (biggestBox[2]))
    thirdCoord = (int (biggestBox[1]), int (biggestBox[2] + biggestBox[4]))
    fourthCoord = (int (biggestBox[1] + biggestBox[3]), int (biggestBox[2] + biggestBox[4]))

    #Coords inserted into a tuple
    coords = (firstCoord, secondCoord, thirdCoord, fourthCoord)

    #Output windows
    """
    cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Detection', 600,600)
    cv2.imshow("Detection", mask)
    cv2.namedWindow('Tracking', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Tracking', 600,600)
    cv2.imshow('Tracking', image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """

def returnCoords():
    return coords
