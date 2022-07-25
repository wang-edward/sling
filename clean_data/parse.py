import json
import math
import os
import random

import numpy as np

import cv2
import torch
import torch.nn as nn

import matplotlib.pyplot as plt

from torch.utils.data import Dataset
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

def compute_difference(x):
    diff = []

    for i, xx in enumerate(x):
        temp = []
        for j, xxx in enumerate(x):
            if i != j:
                temp.append(xx - xxx)

        diff.append(temp)

    return diff

def calc_distance(x0, y0, x1, y1):
    return np.sqrt((x1-x0)**2 + (y1-y0)**2)

def od(x,y, index1, index2):
    return calc_distance(x[index1],y[index1],x[index2],y[index2])

def read_pose_file(filepath):
    #body_pose_exclude = {9, 10, 11, 22, 23, 24, 12, 13, 14, 19, 20, 21}

    try:
        content = json.load(open(filepath))["people"][0]
    except IndexError:
        return None

    body_pose = content["pose_keypoints_2d"]
    left_hand_pose = content["hand_left_keypoints_2d"]
    right_hand_pose = content["hand_right_keypoints_2d"]

    #print("left:  {0}".format(len(left_hand_pose)))
    #print("right: {0}".format(len(right_hand_pose)))

    x = [v for i, v in enumerate(right_hand_pose) if i%3==0]
    y = [v for i, v in enumerate(right_hand_pose) if i%3==1]

    #my_lx = [v for i, v in enumerate(left_hand_pose) if i%3==0]
    #my_xy = [v for i, v in enumerate(left_hand_pose) if i%3==1

    finger_lens = {}
    finger_lens[0] = od(x,y,2,3) + od(x,y,3,4)
    finger_lens[1] = od(x,y,5,6) + od(x,y,6,7) + od(x,y,7,8)
    finger_lens[2] = od(x,y,9,10) + od(x,y,10,11) + od(x,y,11,12)
    finger_lens[3] = od(x,y,13,14) + od(x,y,14,15) + od(x,y,15,16)
    finger_lens[4] = od(x,y,17,18) + od(x,y,18,19) + od(x,y,19,20)

    sum = 0
    for i in finger_lens:
        sum+=i
    if (sum > 0):
        return finger_lens
    return None

#os.chdir("pose_per_individual_videos"
directory = "pose_per_individual_videos"

final = {}

os.chdir(directory)
for id_dir in os.listdir():
    if (id_dir != ".DS_Store"):
        os.chdir(id_dir)
        list_files = os.listdir()
        for i in list_files:
            temp = read_pose_file(i)
            if (temp == None or temp[0] == 0):
                print(0)
            else:
                final[id_dir] = temp
                break
        #temp = read_pose_file("image_00001_keypoints.json")
        #if (temp!=None):
            #final[id_dir] = temp
        os.chdir('..')

os.chdir('..')
with open("finger_data.json", "w") as write_file:
    json.dump(final, write_file)

