# Questo script serve a determinare la distribuzione spaziale dei loghi sintetici incollati sulle immagini di background
# IMPORTANTE: potrebbe essere necessario modificare il path alla cartella contenente il dataset delle immagini sintetiche


import numpy as np
import matplotlib.pyplot as plt

import cv2 as cv
import os

def get_bbox_coord(img):
    coord = np.where(img==np.full_like(img, 255))
        
    first_row = min(coord[0].tolist())
    first_col = min(coord[1].tolist())
    
    return first_row, first_col 


path_input_dir = ".\\truth_synthetic"
point_counter = np.zeros((500, 500))
count = 0

for fname in os.listdir(path_input_dir):
    path_img = path_input_dir + "\\" + fname
    img = cv.imread(path_img)
    h,w,_ = img.shape
    coord = get_bbox_coord(img)
    coord = ((coord[0] * 500) // h , (coord[1] * 500) // w)
    point_counter[coord] += 1


max_v = np.amax(point_counter)
print(max_v)
point_counter = (point_counter * 255) // max_v

cv.imshow("img distribution", point_counter)
cv.waitKey()
exit()

p_coords = [[k[0], k[1], v] for k, v in point_counter.items()]
p_coords = np.asarray(p_coords)

X = p_coords[::,0]
Y = p_coords[::,1]
Z = p_coords[::,2]

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.scatter(X, Y, Z)
ax.set_title('scattered')
plt.show()