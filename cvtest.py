import cv2 as cv
import numpy as np

print(np.array([1,1,2]))

data = cv.imread('./samples/results/8.jpg')

# print(data)



cv.namedWindow('test',0)
cv.resizeWindow('test',400,800)


cv.imshow('test', data)



cv.waitKey(0)
cv.destoryAllWindows()