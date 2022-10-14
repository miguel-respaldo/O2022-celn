#!/usr/bin/env python3
# vi: set shiftwidth=4 tabstop=8 expandtab:
import numpy as np
import cv2 as cv
import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 10001        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        newbimg = list()
        cont=0
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(4096)
                print("resiviendo", cont)
                cont +=1
                if not data:
                    print("break")
                    break
                newbimg.extend(list(data))
                print(len(newbimg))

            print("fuera del while")
            color = np.ndarray(shape=(480,640,3), dtype='uint8',
                                buffer=bytearray(newbimg))

            gris = cv.cvtColor(color, cv.COLOR_BGR2GRAY)

            # La convierte en arreglo lineal
            img1d = gris.flatten()
            # Creo un bytearray con el tamaño del arreglo lineal
            imgbyte = bytearray(img1d.size)
            # Copio el arreglo al bytearray
            for i in range(img1d.size):
                imgbyte[i] = img1d[i]
            conn.sendall(data)

