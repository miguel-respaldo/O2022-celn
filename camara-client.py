#!/usr/bin/env python3
# vi: set shiftwidth=4 tabstop=8 expandtab:
import numpy as np
import cv2 as cv
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 10000        # The port used by the server

camara = cv.VideoCapture(0)

if not camara.isOpened():
    print("No puedo abrir la camara")
    exit(1)

while True:
    # Leemos la imagen de la camara
    ret, imagen = camara.read()

    if not ret:
        print("No podemos capturar la imagen de la camara")
        break

    # La convierte en arreglo lineal
    img1d = imagen.flatten()
    # Creo un bytearray con el tamaño del arreglo lineal
    imgbyte = bytearray(img1d.size)
    # Copio el arreglo al bytearray
    for i in range(img1d.size):
        imgbyte[i] = img1d[i]

    newbimg = list()

    #gris = cv.cvtColor(imagen, cv.COLOR_BGR2GRAY)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(imgbyte)
        while True:
            data = s.recv(4096)
            if not data:
                break
            newbimg.extend(list(data))

    gris = np.ndarray(shape=(480,640), dtype='uint8',
                      buffer=bytearray(newbimg))
    
    cv.imshow("Camara", gris)

    if cv.waitKey(1) == 27:
        break

camara.release()
cv.destroyAllWindows()
