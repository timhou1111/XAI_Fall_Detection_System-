import os
import cv2 # opencv
import copy
import numpy as np
import mediapipe as mp
import math


# mp_holistic = mp.solutions.holistic # Holistic model
mp_pose = mp.solutions.pose # Pose model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities
mp_drawing_styles = mp.solutions.drawing_styles

class mediapipi_pose():
    # 20221226-alex-Holistic改成使用pose(只抓支體不抓手跟臉)
    #model 姿態推論
    def mediapipe_detection(image, pose):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
        image.flags.writeable = False                  # Image is no longer writeable
        results = pose.process(image)                 # Make prediction
        image.flags.writeable = True                   # Image is now writeable 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
        return image, results

    # 20221226-alex-把holistic改成pose (只抓身體不抓臉跟手)
    #畫出身體肢幹
    def draw_landmarks(image, results):
        # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS) # Draw face connections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()) # Draw pose connections
        # mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS) #（3D）
        # mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_pose.HAND_CONNECTIONS) # Draw left hand connections
        # mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_pose.HAND_CONNECTIONS) # Draw right hand connections

    # # 20221226-alex-把holistic改成pose (只抓身體不抓臉跟手)
    # #取得身體支幹point                            
    # def extract_keypoints(results):
    #     pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    #     # face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    #     lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    #     rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    #     # return np.concatenate([pose, face, lh, rh])
    #     return np.concatenate([pose, lh, rh])

    # 20221226-alex-把holistic改成pose (只抓身體不抓臉跟手)
    #取得身體支幹point                            
    def extract_keypoints(results):
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
        # return np.concatenate([pose]) # 如果沒有資料合併就不要用np.concatenate不然會出錯
        return pose
    
    
    #取得身體支幹point                            
    def extract_keypoints_custom(image,results):
        w,h,c = image.shape
        pose = []
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
        # # return np.concatenate([pose]) # 如果沒有資料合併就不要用np.concatenate不然會出錯
        # return pose
        # pose.append(results.pose_landmarks.landmark[0])
        
        lmslist = []
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                if id==11: #左肩
                    cx, cy ,cz , cv = float(lm.x) * w, float(lm.y) * h, float(lm.z),float(lm.visibility)
                    lmslist.append(cx)
                    lmslist.append(cy)
                    # lmslist.append(cz)
                    # lmslist.append(cv)
                    
                elif id==12: #右肩
                    cx, cy ,cz , cv = float(lm.x) * w, float(lm.y) * h, float(lm.z),float(lm.visibility)
                    lmslist.append(cx)
                    lmslist.append(cy)
                    # lmslist.append(cz)
                    # lmslist.append(cv)
                elif id==23: #左腰
                    cx, cy ,cz , cv = float(lm.x) * w, float(lm.y) * h, float(lm.z),float(lm.visibility)
                    lmslist.append(cx)
                    lmslist.append(cy)
                    # lmslist.append(cz)
                    # lmslist.append(cv)

                elif id==24: #右腰
                    cx, cy ,cz , cv = float(lm.x) * w, float(lm.y) * h, float(lm.z),float(lm.visibility)
                    lmslist.append(cx)
                    lmslist.append(cy)
                    # lmslist.append(cz)
                    # lmslist.append(cv)
                elif id==25: #左膝蓋
                    cx, cy ,cz , cv = float(lm.x) * w, float(lm.y) * h, float(lm.z),float(lm.visibility)
                    lmslist.append(cx)
                    lmslist.append(cy)
                    # lmslist.append(cz)
                    # lmslist.append(cv)
                elif id==26: #右膝蓋
                    cx, cy ,cz , cv = float(lm.x) * w, float(lm.y) * h, float(lm.z),float(lm.visibility)
                    lmslist.append(cx)
                    lmslist.append(cy)
                    # lmslist.append(cz)
                    # lmslist.append(cv)
                elif id==27: #左腳踝
                    cx, cy ,cz , cv = float(lm.x) * w, float(lm.y) * h, float(lm.z),float(lm.visibility)
                    lmslist.append(cx)
                    lmslist.append(cy)
                    # lmslist.append(cz)
                    # lmslist.append(cv)
                elif id==28: #右腳踝
                    cx, cy ,cz , cv = float(lm.x) * w, float(lm.y) * h, float(lm.z),float(lm.visibility)
                    lmslist.append(cx)
                    lmslist.append(cy)
                    # lmslist.append(cz)
                    # lmslist.append(cv)
        # print(lmslist)
        arr = np.array(lmslist)
        return pose,arr

    # 20230612-alex-計算兩座標點中心平均值
    # human center line coordinate(HCLC)
    # 人體中心線坐標
    def distance_avg_HCLC(left_x,right_x):
        x = (left_x+right_x) / 2
        return x
    
    
    
    # 取得左右肩，左右腰，左右膝，左右踝 八個點的平均值
    # 11 12 23 24 25 26 27 28
    def extract_keypoints_HCLC(image,results):
        w,h,c = image.shape
        pose = []
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
        # # return np.concatenate([pose]) # 如果沒有資料合併就不要用np.concatenate不然會出錯
        # return pose
        # pose.append(results.pose_landmarks.landmark[0])
        
        lmslist = []
        # 取得左右肩的平均值
        x11 = results.pose_landmarks.landmark[11].x * w
        y11 = results.pose_landmarks.landmark[11].y * h

        x12 = results.pose_landmarks.landmark[12].x * w
        y12 = results.pose_landmarks.landmark[12].y * h

        x23 = results.pose_landmarks.landmark[23].x * w
        y23 = results.pose_landmarks.landmark[23].y * h

        x24 = results.pose_landmarks.landmark[24].x * w
        y24 = results.pose_landmarks.landmark[24].y * h

        x25 = results.pose_landmarks.landmark[25].x * w
        y25 = results.pose_landmarks.landmark[25].y * h

        x26 = results.pose_landmarks.landmark[26].x * w
        y26 = results.pose_landmarks.landmark[26].y * h

        x27 = results.pose_landmarks.landmark[27].x * w
        y27 = results.pose_landmarks.landmark[27].y * h

        x28 = results.pose_landmarks.landmark[28].x * w
        y28 = results.pose_landmarks.landmark[28].y * h

        lmslist.append(mediapipi_pose.distance_avg_HCLC(x11,x12))
        lmslist.append(mediapipi_pose.distance_avg_HCLC(y11,y12))
        
        lmslist.append(mediapipi_pose.distance_avg_HCLC(x23,x24))
        lmslist.append(mediapipi_pose.distance_avg_HCLC(y23,y24))
        
        lmslist.append(mediapipi_pose.distance_avg_HCLC(x25,x26))
        lmslist.append(mediapipi_pose.distance_avg_HCLC(y25,y26))
        
        lmslist.append(mediapipi_pose.distance_avg_HCLC(x27,x28))
        lmslist.append(mediapipi_pose.distance_avg_HCLC(y27,y28))

        arr = np.array(lmslist)
        return pose,arr
    
    
    # 20230612-alex-計算歐式距離
    # Euclidean distance formula
    def distance_avg_EDF(x1,y1,x2,y2):
        Dis=math.sqrt((x1-x2)**2+(y1-y2)**2)
        # print("Distance = {:.2f}".format(Dis))
        return Dis
    
    # 20230612-alex-計算歐式距離並除以time
    # speed of HCLC (SHCLC)
    def distance_avg_SHCLC(x1,y1,x2,y2,t):
        Dis=math.sqrt((x1-x2)**2+(y1-y2)**2)
        out = Dis / t
        return out

    # 取得左右肩，左右腰，左右膝，左右踝 八個點的平均值
    # 11 12 23 24 25 26 27 28
    def extract_keypoints_SHCLC(image,results):
        w,h,c = image.shape
        pose = []
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
        # # return np.concatenate([pose]) # 如果沒有資料合併就不要用np.concatenate不然會出錯
        # return pose
        # pose.append(results.pose_landmarks.landmark[0])
        
        lmslist = []
       
        # 取得左右肩的平均值
        x11 = results.pose_landmarks.landmark[11].x * w
        y11 = results.pose_landmarks.landmark[11].y * h

        x12 = results.pose_landmarks.landmark[12].x * w
        y12 = results.pose_landmarks.landmark[12].y * h

        x23 = results.pose_landmarks.landmark[23].x * w
        y23 = results.pose_landmarks.landmark[23].y * h

        x24 = results.pose_landmarks.landmark[24].x * w
        y24 = results.pose_landmarks.landmark[24].y * h

        x25 = results.pose_landmarks.landmark[25].x * w
        y25 = results.pose_landmarks.landmark[25].y * h

        x26 = results.pose_landmarks.landmark[26].x * w
        y26 = results.pose_landmarks.landmark[26].y * h

        x27 = results.pose_landmarks.landmark[27].x * w
        y27 = results.pose_landmarks.landmark[27].y * h

        x28 = results.pose_landmarks.landmark[28].x * w
        y28 = results.pose_landmarks.landmark[28].y * h

        # lmslist.append(mediapipi_pose.distance_avg_SHCLC(x11,y11,x12,y12,30))
        # lmslist.append(mediapipi_pose.distance_avg_SHCLC(x23,y23,x24,y24,30))
        # lmslist.append(mediapipi_pose.distance_avg_SHCLC(x25,y25,x26,y26,30))
        # lmslist.append(mediapipi_pose.distance_avg_SHCLC(x27,y27,x28,y28,30))

        # lmslist.append(mediapipi_pose.distance_avg(results.pose_landmarks.landmark[11][0],results.pose_landmarks.landmark[11][1],results.pose_landmarks.landmark[12][0],results.pose_landmarks.landmark[12][1]))
        # print(results.pose_landmarks.landmark[11].x * w)
        # print(results.pose_landmarks.landmark[11].y * h)
        # print(results.pose_landmarks.landmark[12].x * w)
        # print(results.pose_landmarks.landmark[12].y * h)
        # print(lmslist)
        
        
        
        arr = np.array(lmslist)
        return pose,arr

# def draw_styled_landmarks(image, results):
    # # Draw face connections
    # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS, 
    #                          mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
    #                          mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
    #                          ) 
    # # Draw pose connections
    # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
    #                          mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
    #                          mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
    #                          ) 
    # # Draw left hand connections
    # mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
    #                          mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
    #                          mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
    #                          ) 
    # # Draw right hand connections  
    # mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
    #                          mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
    #                          mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
    #                          ) 