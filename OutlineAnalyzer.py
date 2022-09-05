import matplotlib.pyplot as plt
import numpy as np
import cv2
import csv
import easygui
import os

# Contour and image file
text = open(easygui.fileopenbox("Open Contour File"))
imageFile = easygui.fileopenbox("Open Image File")
image = cv2.imread(imageFile)
# Extract image size
h, w, c = image.shape

# Extracted data: 0: Orientation, 1: Aspect ratio
to_csv = []

for line in text:
    points = []
    data = line.split(',') # seperator between coordinate in outline file
    i=0
    # Read outline file
    for pos in data:
        if (i%2 == 1):
            x = int(pos)
            point = [y,x]
            points.append(point)
        else:
            y = int(pos)
        i = i+1
        
    # Create & draw openCV contour
    ctr = np.array(points).reshape((-1,1,2)).astype(np.int32)
    cv2.drawContours(image,[ctr],0,(255,0,0),1)

    # Fit ellipse and calculate area and fitting error
    ellipse = cv2.fitEllipse(ctr)        
    ellipseArea = np.pi*ellipse[1][0]*ellipse[1][1]/4
    error = abs(cv2.contourArea(ctr)-ellipseArea)/cv2.contourArea(ctr)
    # Exclude ellipses with high error and small fits at the borders of the image (drawn red)
    if ((error > 0.50) or (ellipseArea < 4000) and (((ellipse[0][1] - ellipse[1][1]/2) < 0) or ((ellipse[0][0] - ellipse[1][0]/2) < 0) or ((ellipse[0][1] + ellipse[1][1]/2) > h) or ((ellipse[0][0] + ellipse[1][0]/2) > w))):
        cv2.ellipse(image, ellipse, (0, 0, 255), 2)
    else:
        to_csv.append([ellipse[2], ellipse[1][0]/ellipse[1][1]])
        
        if(ellipse[2] < 45):
            cv2.ellipse(image, ellipse, (255, 0, 0), 2)
        elif(ellipse[2] < 90):
            cv2.ellipse(image, ellipse, (255, 255, 0), 2)
        elif(ellipse[2] < 135):
            cv2.ellipse(image, ellipse, (0, 255, 0), 2)
        else:
            cv2.ellipse(image, ellipse, (0, 255, 255), 2)

# Write and show image with fitted ellipses
outputImage = os.path.dirname(imageFile) + '/' + os.path.basename(imageFile).split('.')[0] + '-mod.tif'
print (outputImage)
cv2.imwrite(outputImage, image)
image = cv2.resize(image, (1280, 720))
cv2.imshow('image', image)

outputCSV = os.path.dirname(imageFile) + '/' + os.path.basename(imageFile).split('.')[0] + '-orientation.csv'
# Write results to CSV file
with open(outputCSV, 'w') as file:
    writer = csv.writer(file, delimiter = ';')
    writer.writerow(['Orientation', 'aspect_ratio'])

    writer.writerows(to_csv)

text.close()
