'''
Author: Adriel Varela
Last Modified: 17-JAN-2022
ABOUT: simple image segmentation using watershed algorithm on a single jpg.
Currently learning to use openCV library, and learn uses of different types of
image detection techniques.
'''


import cv2
import numpy as np
from matplotlib import cm

# import the image we want to use
husky = cv2.imread('C:/Users/adrie/Desktop/Images for CV/husky1.jpg')

# make copy and templates for segments & markers
husky_copy = np.copy(husky)
# markers only need a b/w image
markers = np.zeros(husky.shape[:2],dtype=np.int32)
segments = np.zeros(husky.shape,dtype=np.uint8)

# ------ EDIT: moved this to 1 line in if loops
# get colors and arrange in a tuple with scaled values(0-255)
# color = tuple(np.array(cm.tab10(0)[:3])*255)
# put colors into an array -- the indiv color values (X,X,X) need to be
# in a tuple for opencv

colors = []
for i in range(10):
    # Open cv needs tuples for color, change output of numpy.array() to tuple and append to empty array
    colors.append(tuple(np.array(cm.tab10(i)[:3])*255))


# create fxn to show seeds for watershed(1 img - display to user, 2nd img - seeds for watershed)
marker_updated = False
current_marker = 1
def draw_seed(event,x,y,flag,param):
    global marker_updated
    if event == cv2.EVENT_LBUTTONDOWN:
        # user display
        cv2.circle(husky_copy,(x,y),10,colors[current_marker],-1)
        # for watershed
        cv2.circle(markers,(x,y),10,current_marker,-1)
        marker_updated = True


cv2.namedWindow('Husky')
cv2.setMouseCallback('Husky',draw_seed)

while True:
    cv2.imshow('Husky',husky_copy)
    cv2.imshow('Segments',segments)

    # close the windows w/ esc
    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k == ord('c'):
        # pressing c will resett the images clearing seeds
        husky_copy = husky.copy()
        markers = np.zeros(husky.shape[:2],dtype=np.int23)
        segments = np.zeros(husky.shape,dtype=np.uint8)
    elif k > 0 and chr(k).isdigit():
        #indexing through colors 0-9
        current_marker = int(chr(k))

    if marker_updated:
        # performing watershed on the original image and markers created with fxn:draw_seed
        # a copy of marker created b/c original markers img is being used by fxn:draw_seed
        markers_copy = markers.copy()
        cv2.watershed(husky,markers_copy)
        for color_ind in range(10):
            # color through a numpy call
            # each time marker_updated set to True by fxn: draw_seed will iterate through loop at 0,
            # bc markers_copy is a np.zeros() array, pixels at 0 will be set to value (X,X,X) indexed
            # by colors[color_ind]
            segments[markers_copy == (color_ind)] = colors[color_ind]

cv2.destroyAllWindows()


