from tkinter.tix import IMAGE
import cv2
from cv2 import waitKey
import numpy as np
import pickle
import os
import sqlite3
import random

image_x, image_y = 50, 50


def get_hand_hist():
    with open("C:\\Users\\91746\\Desktop\\check\\isl\\hist", "rb") as f:
        hist = pickle.load(f)
    return hist


def init_create_folder_database():
    # create the folder and database if not exist
    if not os.path.exists("gestures"):
        os.mkdir("gestures")
    if not os.path.exists("gesture_db.db"):

        conn = sqlite3.connect("gesture_db.db")
        # create_table_cmd = "DELETE FROM gesture"
        create_table_cmd = "CREATE TABLE gesture ( g_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, g_name TEXT NOT NULL )"
        conn.execute(create_table_cmd)
        conn.commit()


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def store_in_db(g_id, g_name):
    conn = sqlite3.connect("gesture_db.db")

    cmd = "INSERT INTO gesture (g_id, g_name) VALUES (%s, \'%s\')" % (
        g_id, g_name)
    print(cmd)
    try:
        conn.execute(cmd)
    except sqlite3.IntegrityError:
        choice = input(
            "g_id already exists. Want to change the record? (y/n): ")
        if choice.lower() == 'y':
            cmd = "UPDATE gesture SET g_name = \'%s\' WHERE g_id = %s" % (
                g_name, g_id)
            conn.execute(cmd)
        else:
            print("Doing nothing...")
            return
    conn.commit()


# For static images:
IMAGE_FILES = []

# Defining Paths
pathToImage = os.path.join(os.getcwd(), "gestures")

# For loading all Images from Folder
def load_images_from_folder():
    images = []
    for filename in os.listdir(pathToImage):
        images.append(os.path.join(pathToImage, filename))
    return images


def store_images(g_id,check):
    less = 0
    if check == True:
        print("run")
        less = 1
    print(g_id-less)
    picture_no = 1
    for image in os.listdir(IMAGE_FILES[g_id-less]):
        image = os.path.join(IMAGE_FILES[g_id-less],image)
        print(image)
        img = cv2.imread(image)
        kernel = np.ones((5, 5), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        hsvim = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([0, 48, 80], dtype="uint8")
        upper = np.array([20, 255, 255], dtype="uint8")
        skinRegionHSV = cv2.inRange(hsvim, lower, upper)
        blurred = cv2.blur(skinRegionHSV, (2, 2))
        ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY)
        char = chr(g_id+65)
        print(char)
        Path = "C:\\Users\\91746\\Desktop\\check\\isl\\gestures\\" + char
        
        if os.path.isdir(Path) == False:
            os.mkdir(Path)
        joining_folder = str(char) 
        Path = os.path.join(Path,joining_folder)
         
        Path = Path + str(picture_no)+".jpg"
        
        cv2.imwrite(Path, thresh)
         
        picture_no = picture_no + 1


init_create_folder_database()

IMAGE_FILES = load_images_from_folder()
print(len(IMAGE_FILES))
check = False
for one in range(65,68):
    g_id = one
    if g_id == 74:
        continue
    if one >= 74:
        check = True
    g_name = chr(one)
    store_in_db(g_id-64, g_name)
    # store_images(g_id-65,check)
