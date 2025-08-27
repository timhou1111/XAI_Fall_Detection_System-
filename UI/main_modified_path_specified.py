import tkinter as tk
from moviepy.editor import *
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


def play_video(filepath):
    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        print("Error opening video file.")
        return

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame_resized = cv2.resize(frame, (400, 300))
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            img = ImageTk.PhotoImage(frame_pil)
            label.config(image=img)
            label.image = img
            label.after(10, update_frame)
        else:
            cap.release()

    update_frame()

def open_file():
    filetypes = (("MP4 files", "*.mp4"), ("All files", "*.*"))
    filepath = filedialog.askopenfilename(
        title="Select a file", filetypes=filetypes)
    if filepath:
        video = VideoFileClip(filepath)
        #video.preview() 影片播放
    if filepath:
        cap = cv2.VideoCapture(filepath) #讀入mp4檔案，要記得加mp4
        mp_pose = mf.mp.solutions.pose
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                    keypoints_list = []
                    for frame_num in range(30):#抓取30幀
                        ret, frame = cap.read()
                        image, results = mf.mediapipi_pose.mediapipe_detection(frame, pose) #建立point
                        # print(results)
                        # Draw landmarks
                        mf.mediapipi_pose.draw_landmarks(image, results) #畫面point
                        keypoints , lm  = mf.mediapipi_pose.extract_keypoints_HCLC(image,results)
                        keypoints = lm
                        keypoints_list.append(keypoints)
                    for i in range(len(keypoints_list)-1):
                        keypoints2 = []
                        keypoints2.append(mf.mediapipi_pose.distance_avg_SHCLC(keypoints_list[i+1][0],keypoints_list[i+1][1],keypoints_list[i][0],keypoints_list[i][1],30))
                        keypoints2.append(mf.mediapipi_pose.distance_avg_SHCLC(keypoints_list[i+1][2],keypoints_list[i+1][3],keypoints_list[i][2],keypoints_list[i][3],30))
                        keypoints2.append(mf.mediapipi_pose.distance_avg_SHCLC(keypoints_list[i+1][4],keypoints_list[i+1][5],keypoints_list[i][4],keypoints_list[i][5],30))
                        keypoints2.append(mf.mediapipi_pose.distance_avg_SHCLC(keypoints_list[i+1][6],keypoints_list[i+1][7],keypoints_list[i][6],keypoints_list[i][7],30))    
                    print(keypoints2)
                    static_text = "SHCLC數值"
                    shoulder_var.set("肩膀SHCLC：" + str(round(keypoints2[0], 4)))
                    hip_var.set("髖部SHCLC：" + str(round(keypoints2[1], 4)))
                    knee_var.set("膝蓋SHCLC：" + str(round(keypoints2[2], 4)))
                    ankle_var.set("腳踝SHCLC：" + str(round(keypoints2[3], 4)))


    play_video(filepath)
    keypoints2_np = np.array(keypoints2)
    index_of_max_value = np.argmax(keypoints2)
    result_var.set("模型預測結果：" + str(model.predict([keypoints2])))
    print(str(model.predict([keypoints2])))
    if str(model.predict([keypoints2])) != "['stand_normal']":
        if index_of_max_value==0:
            rule_var.set("肩膀位移幅度較大的跌倒")
        elif index_of_max_value==1:
            rule_var.set("髖部位移幅度較大的跌倒")
        elif index_of_max_value==2:
            rule_var.set("膝蓋位移幅度較大的跌倒")
        elif index_of_max_value==3:
            rule_var.set("腳踝位移幅度較大的跌倒")
    else:
         rule_var.set("")
    

    
    
    exp = explainer.explain_instance(data_row=keypoints2_np, predict_fn=model.predict_proba)
    exp.save_to_file('lime_output.html')
    label = tk.Label(window, text="Lime解釋結果", font=("Helvetica", 20))
    lime_var_1.set(str(str(exp.as_list()[0])))
    lime_var_2.set(str(str(exp.as_list()[1])))
    lime_var_3.set(str(str(exp.as_list()[2])))
    lime_var_4.set(str(str(exp.as_list()[3])))



window = tk.Tk()
window.title("UIUX")
window.geometry("800x900")  # Adjusted the window size for better spacing and visibility

canvas = tk.Canvas(window, bg="#f2f2f2")
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Load your model and Lime explainer
model = joblib.load("random_forest.joblib")
with open(r"C:\Users\Owner\Desktop\政大\UI\lime_explainer_2.pkl", 'rb') as f:
    explainer = dill.load(f)

# Main title
label = tk.Label(frame, text="馬偕防跌倒XAI", font=("Helvetica", 26, "bold"), bg="#f2f2f2", anchor='center')
label.pack(pady=20)

# Variables for the labels
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

# SHCLC results
result_frame = tk.Frame(frame)
result_frame.pack(pady=15)
tk.Label(result_frame, text="SHCLC數值結果:", font=("Helvetica", 18)).grid(row=0, columnspan=2, )
tk.Label(result_frame, textvariable=shoulder_var, font=("Helvetica", 16)).grid(row=1, column=1, )
tk.Label(result_frame, textvariable=hip_var, font=("Helvetica", 16)).grid(row=2, column=1, )
tk.Label(result_frame, textvariable=knee_var, font=("Helvetica", 16)).grid(row=3, column=1, )
tk.Label(result_frame, textvariable=ankle_var, font=("Helvetica", 16)).grid(row=4, column=1, )

# Prediction and Lime results
result_var_label = tk.Label(frame, textvariable=result_var, font=("Helvetica", 16), anchor='center')
result_var_label.pack(pady=10, padx=20, fill=tk.X)

rule_var_label = tk.Label(frame, textvariable=rule_var, font=("Helvetica", 14), anchor='center', fg="red")
rule_var_label.pack(pady=10, padx=20, fill=tk.X)

lime_frame = tk.Frame(frame)
lime_frame.pack(pady=15)
tk.Label(lime_frame, text="Lime解釋結果:", font=("Helvetica", 18)).grid(row=0, columnspan=2, )
tk.Label(lime_frame, textvariable=lime_var_1, font=("Helvetica", 14)).grid(row=1, column=1, )
tk.Label(lime_frame, textvariable=lime_var_2, font=("Helvetica", 14)).grid(row=2, column=1, )
tk.Label(lime_frame, textvariable=lime_var_3, font=("Helvetica", 14)).grid(row=3, column=1, )
tk.Label(lime_frame, textvariable=lime_var_4, font=("Helvetica", 14)).grid(row=4, column=1, )

# Upload video button
button = tk.Button(frame, text="選擇影片檔案", command=open_file, font=("Helvetica", 16, "bold"), bg="#4CAF50", fg="white", bd=0, padx=20, pady=10)
button.pack(pady=20, anchor="center")



# Button to open the LIME visualization in a web browser
def open_lime_result():
    import webbrowser
    webbrowser.open(r"C:\Users\Owner\Desktop\政大\UI\lime_output.html")

lime_button = tk.Button(frame, text="查看LIME結果", command=open_lime_result, font=("Helvetica", 14))
lime_button.pack(pady=20, anchor="center")


window.mainloop()