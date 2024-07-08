# Questo script server ad ottenere la maschera binaria a partire da un file testuale che definisce il poligono, della maschera, per verificare la correttezza
# del poligono generato.
# IMPORTANTE: potrebbe essere necessario modificare il path al file testuale in ingresso

import cv2
import numpy as np

W = 331
H = 152

# Read polygon vertices from the text file
with open('test.txt', 'r') as file:
    # Read all coordinates from the file and convert them to integers
    lines_list = file.readlines()

coordinates = []
for e in lines_list:
    tmp = e.split()
    coordinates.append([float(i) for i in tmp])

polygon_vertices = []
for coordinate in coordinates:
    coordinate.pop(0)
    polygon_vertices.append([(coordinate[i] * W, coordinate[i+1] * H) for i in range(0, len(coordinate), 2)])

mask = np.zeros((H, W), dtype=np.uint8)

pts = []
for polygon in polygon_vertices:
    pts.append(np.array(polygon, np.int32))

ptss = []
for p in pts:
    ptss.append(p.reshape((-1, 1, 2)))

for pts in ptss:
    cv2.fillPoly(mask, [pts], 255)


cv2.imshow('name', mask)
cv2.waitKey()
