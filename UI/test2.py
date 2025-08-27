import tkinter as tk
from moviepy.editor import *
from tkinter import filedialog
from tkhtmlview import HTMLLabel
from PIL import Image, ImageTk
import pygame
from tkinter import filedialog
import os
import cv2
import time
import numpy as np
from matplotlib import pyplot as plt
#==============================================================
#檔案處理用
import threading
import glob
import shutil
from os import listdir
from os.path import isfile, isdir, join
import joblib
from sklearn.ensemble import RandomForestClassifier
import dill
#==============================================================
from alex_function import alexfun #其它自寫function
import mediapipe_function as mf

shoulder_var = tk.StringVar()
hip_var = tk.StringVar()
knee_var = tk.StringVar()
ankle_var = tk.StringVar()
result_var = tk.StringVar()
rule_var = tk.StringVar()
lime_var_1 = tk.StringVar()
lime_var_2 = tk.StringVar()
lime_var_3 = tk.StringVar()
lime_var_4 = tk.StringVar()

