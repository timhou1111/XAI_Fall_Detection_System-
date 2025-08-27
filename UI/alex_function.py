import os
import re
import cv2 # opencv
import base64
import sys
import glob
import copy
import time
import numpy as np
import pandas as pd
import mediapipe as mp
# import serial
import requests # line-notify
# import win32api #pip install pypiwin32
import threading #多執行序
from ftplib import FTP
from PIL import Image,ImageDraw,ImageFont #顯示中文字型
# import threading #多執行序
import sqlite3
#==============================================================
import json  
#import paho.mqtt.client as mqtt
#==============================================================
# 20230117-alex-windows與linux的路徑自動切換
from pathlib import Path
#==============================================================
# import winsound #發出警示音 for windows
# duration30 = 3000  # millisecond
# duration20 = 2000  # millisecond
# duration10 = 1000  # millisecond
# freq220 = 220  # Hz
# freq330 = 330  # Hz
# freq440 = 440  # Hz
# 20230117-alex-winsound linux不支援

from pygame import mixer


#pip install playsound==1.2.2
# from playsound import playsound #播放聲音 
# import pygame
# #windows 系统： 蜂鸣声
# ==============================================================

#https://www.learncodewithmike.com/2020/12/read-excel-file-using-pandas.html

class alexmsg():
    def ShowMsg(_id):
        df = pd.read_excel("setup_message.xlsx")
        print(df)
        
# class alexmqtt():
# #======================================================
#     # 以下為 mqtt
#     #======================================================
#     # 20230107-alex-傳送文字檔
#     def mqtt_publish(_setup_mqtt,_setup_machine,_CamID,_Msg):
#         mqttt = threading.Thread(target=alexmqtt.mqtt_publist_send,daemon=True,args=(_setup_mqtt,_setup_machine,_CamID,_Msg,))
#         mqttt.start()

#     def mqtt_publist_send(_setup_mqtt,_setup_machine,_CamID,_Msg):
#         # 連線設定
#         # 初始化地端程式
#         #client = mqtt.Client()
#         # # 設定登入帳號密碼
#         # client.username_pw_set("kaikaihsu","k250035k")
#         # # 設定連線資訊(IP, Port, 連線時間)
#         # client.connect("www.hsukai.com", 1883, 60)
#         # 設定登入帳號密碼
#         client.username_pw_set(str(_setup_mqtt[0]),str(_setup_mqtt[1]))
#         # 設定連線資訊(IP, Port, 連線時間)
#         client.connect(str(_setup_mqtt[2]),int(_setup_mqtt[3]),int(_setup_mqtt[4]))

#         # 取得現在時間
#         localtime = time.localtime()
#         date_temp = time.strftime("%Y%m%d", localtime)
#         time_temp = time.strftime("%H%M%S", localtime)
#         jsonmsg = {'MachineID' : str(_setup_machine[0]) , 'Date' : date_temp,'Time' : time_temp,'CamID' : _CamID,'Msg' : _Msg}
#         # print (json.dumps(jsonmsg))
#         #要發布的主題和內容
#         client.publish(_setup_mqtt[5], json.dumps(jsonmsg, ensure_ascii=False).encode('utf8'))
#         # client.publish("Try/MQTT", json.dumps(payload, ensure_ascii=False).encode('utf8')) #顯示中文

#     # 20230107-alex-傳送陣列資料
#     def mqtt_publish_array(_setup_mqtt,_Msg):
#         mqttt = threading.Thread(target=alexmqtt.mqtt_publish_array_send,daemon=True,args=(_setup_mqtt,_Msg,))
#         mqttt.start()

#     def mqtt_publish_array_send(_setup_mqtt,_Msg):
#         # 連線設定
#         # 初始化地端程式
#         client = mqtt.Client()
#         # # 設定登入帳號密碼
#         # client.username_pw_set("kaikaihsu","k250035k")
#         # # 設定連線資訊(IP, Port, 連線時間)
#         # client.connect("www.hsukai.com", 1883, 60)
#         # 設定登入帳號密碼
#         client.username_pw_set(str(_setup_mqtt[0]),str(_setup_mqtt[1]))
#         # 設定連線資訊(IP, Port, 連線時間)
#         client.connect(str(_setup_mqtt[2]),int(_setup_mqtt[3]),int(_setup_mqtt[4]))
#         MQTT_MESSAGE = json.dumps(_Msg.tolist())
#         client.publish(_setup_mqtt[5], MQTT_MESSAGE)
#         #要發布的主題和內容
#         # client.publish(_PublishID, json.dumps(_Msg, ensure_ascii=False).encode('utf8'))
#         # client.publish("Try/MQTT", json.dumps(payload, ensure_ascii=False).encode('utf8')) #顯示中文

#     # 20230107-alex-傳送資料流
#     def mqtt_publish_bytearray(_setup_mqtt,_Image):
#         mqttt = threading.Thread(target=alexmqtt.mqtt_publish_bytearray_send,daemon=True,args=(_setup_mqtt,_Image,))
#         mqttt.start()

#     def mqtt_publish_bytearray_send(_setup_mqtt,_Image):
#         # 連線設定
#         # 初始化地端程式
#         client = mqtt.Client()
#         # # 設定登入帳號密碼
#         # client.username_pw_set("kaikaihsu","k250035k")
#         # # 設定連線資訊(IP, Port, 連線時間)
#         # client.connect("www.hsukai.com", 1883, 60)
#         # 設定登入帳號密碼
#         client.username_pw_set(str(_setup_mqtt[0]),str(_setup_mqtt[1]))
#         # 設定連線資訊(IP, Port, 連線時間)
#         client.connect(str(_setup_mqtt[2]),int(_setup_mqtt[3]),int(_setup_mqtt[4]))

#         # Encoding the Frame
#         _, buffer = cv2.imencode('.jpg', _Image)
#         # Converting into encoded bytes
#         jpg_as_text = base64.b64encode(buffer)
#         # Publishig the Frame on the Topic home/server
#         client.publish(_setup_mqtt[5], jpg_as_text)
        
#         # client.publish(_PublishID, _Image,2)
#         # 0不確認是否成功 , 1 回傳值如果有成功就不重發，(重發有可能造成多次一樣資料) ,2回傳是否成功，吃資源但不會造成重覆發送

class alexsqlite():
    # 20230207-alex-新增 事件反饋
    def _event_report_insert(cdate,ctime,customid,camsn,action_id,action_name,filename,mov_file,state,chk,useflag):
        cmd = "insert into event_report (createdate,createtime,customid,camsn,action_id,action_name,filename,mov_file,state,chk,useflag)"
        cmd = cmd + "values('" +cdate + "','" + ctime + "','" + customid + "','" + camsn + "','" + action_id + "','" + action_name + "','" + filename + "','" + mov_file + "','" + state + "','" + chk + "','" + useflag + "')"
        db = sqlite3.connect('ActionDetection.sqlite3')
        cursor = db.cursor()
        cursor.execute(cmd)
        db.commit()
        db.close()
    
    # 20230207-alex-取得 事件反饋列表
    def _event_report_select():
        db = sqlite3.connect('ActionDetection.sqlite3')
        cursor = db.cursor()
        cursor.execute("select * from  event_report where useflag='Y' and chk='N'")
        rows = cursor.fetchall()
        db.close()
        return rows
    
    # 20230208-alex-修改 事件反饋狀態
    def _event_report_edit(eid , state , chk):
        cmd = "update event_report set state='" + state + "' , chk ='" + chk + "' where eid=" + eid + " and useflag='Y'"
        db = sqlite3.connect('ActionDetection.sqlite3')
        cursor = db.cursor()
        cursor.execute(cmd)
        db.commit()
        db.close()
    # 202302028-alex get event_report value
    def _event_report_getvalue(type,id):
        db = sqlite3.connect('ActionDetection.sqlite3')
        cursor = db.cursor()
        if type=='file':
            cursor.execute("select filename from event_report where eid=" + id + " and useflag='Y' and chk='N'")
        elif type=='mov':
            cursor.execute("select mov_file from event_report where eid=" + id + " and useflag='Y' and chk='N'")
        rows = cursor.fetchall()
        db.close()
        return rows[0][0]

    # 20230206-alex- insert event-miss - 新增 未判定之事件
    def insert_event_miss(sdate,stime,edate,etime,customid,camsn,action_id,action_name,filename,state,chk,useflag):
        cmd = "insert into event_miss (sdate,stime,edate,etime,customid,camsn,action_id,action_name,filename,state,chk,useflag)"
        cmd = cmd + "values('" + sdate + "','" + stime + "','" + edate + "','" + etime + "','" + customid + "','" + camsn + "','" + action_id + "','" + action_name + "','" + filename + "','" + state + "','" + chk + "','" + useflag + "')"
        db = sqlite3.connect('ActionDetection.sqlite3')
        cursor = db.cursor()
        cursor.execute(cmd)
        db.commit()
        db.close()
        
    # 20230206-alex-取得 未判定之事件列表
    def select_event_miss():
        db = sqlite3.connect('ActionDetection.sqlite3')
        cursor = db.cursor()
        cursor.execute("select * from  event_miss where useflag='Y' and chk='N'")
        rows = cursor.fetchall()
        db.close()
        
        return rows
        
class alexfun():
    #======================================================
    # 以下為 通用
    #======================================================
    # 上傳到 azure
    def ftpupload(localfilename,ftp_save_filename):
        try:
            ftp = FTP()
            timeout = 30
            port = 21
            ftp.encoding = 'big5' # iis 的 只充許上傳utf8要關掉
            ftp.connect('13.76.160.69',port,timeout) # 連線FTP伺服器
            ftp.login('ftpclock','Ema9453') # 登入
            # print(ftp.getwelcome())  # 獲得歡迎資訊 
            ftp.cwd('WebSite/ailog')    # 設定FTP目錄
            
            # list = ftp.nlst()       # 獲得目錄列表
            # for name in list:
            #     print(name)             # 列印檔名字
            # path = name    # 檔案儲存路徑
            # f = open(path,'wb')         # 開啟要儲存檔案
            
            # file_local = os.path.abspath(os.getcwd()) + '\\' + localfilename # 取得現在程式目錄下的 localfilename
            
            fp = open(localfilename, 'rb') # 讀取檔案
            bufsize = 1024  # 設置緩沖器大小
            uploadfilename = localfilename # 上傳後的儲存名稱
            ## ftp.retrbinary(filename,f.write) # 儲存FTP上的檔案
            ## ftp.delete(name)            # 刪除FTP檔案
            # print(uploadfilename)
            ftp.storbinary('STOR ' + ftp_save_filename, fp,bufsize) # 上傳FTP檔案
            ftp.set_debuglevel(0)
            ftp.close()
            # ftp.quit()                  # 退出FTP伺服器
            # print('===============================')
            # print("警示資訊上傳ftp成功.")
        except:
            print('===============================')
            print("警示資訊回傳失敗，請檢查網路與相關設定.")
    
    # line notify 通知
    def lineNotifyMessage(msg,detect_pix_path):
        # 20221205-alex-讀取警示button是否開啟設定值
        _line_notify_token = alexfun.readtxt_tonparray('setup_linenotify.txt')
        # token ="QhWaztnYcwhACe9C3GoMpW85IFv8VkfsatOlJxyFdLH"
        headers = {
            "Authorization": "Bearer " + _line_notify_token[0]
            # "Content-Type" : "application/x-www-form-urlencoded"
        }
        payload = {'message': msg }
        #上傳想要傳送的圖片
        # print(str(detect_pix_path))
        image = {'imageFile' : open(str(detect_pix_path), 'rb')}
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload, files = image)
        return r.status_code
    #======================================================
    # 以下為 啟動cam
    #======================================================
    def if_integer(string):
        reg_exp = "[-+]?\d+$"
        return re.match(reg_exp, string) is not None

    def star_cam(camsn,connect,_width,_height):
        cap = ''
        if len(connect) > 1:
            cap = cv2.VideoCapture(str(connect))
        else:
            cap = cv2.VideoCapture(int(connect))
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(_width))
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(_height))
        fourcc_cap = cv2.VideoWriter_fourcc(*'MJPG')
        cap.set(cv2.CAP_PROP_FOURCC, fourcc_cap)
        cap.set(cv2.CAP_PROP_FPS, 30)

        _mov_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        _mov_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        _mov_fps = cap.get(cv2.CAP_PROP_FPS)
        # if _mov_fps <= 24:
        #     _mov_fps = 24
        _mov_fps = 6
        ret, frame = cap.read()
    
        # localtime = time.localtime()
        # lttime = time.strftime("%Y%m%d_%H%M%S", localtime)
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # out = cv2.VideoWriter('./movie/webcam1_pose_record_' + str(camsn) + '_' + str(lttime) + '.mp4',fourcc, _mov_fps, (_mov_width,_mov_height))

        return ret,cap

    def chkrtsp(rtsp):
        response = os.system("ping -c 1 " + rtsp)
        if response == 0:
            return True
        else:
            return False
    #======================================================
    # 以下為 姿態偵測區
    #======================================================
    # 20221122-alex-偵測姿式是否改變
    def pose_ischange(narray1,narray2):
        chk = False
        
        if np.allclose(narray1, narray2, rtol=0.4, atol=0.4, equal_nan=True) == False:
            chk = False
            # print("False") #姿式不同
        else:
            chk = True
            # print("True") #姿式相同
        
        return chk
 
    
    #建立資料並上傳 加傳line notify
    def punch_txt(machineid,_camid,_alert_dir,action_id,action_cname,image,frame_temp,mov_width,mov_height):
        # 取得現在時間
        localtime = time.localtime()
        date_temp = time.strftime("%Y%m%d", localtime)
        times_temp = time.strftime("%Y%m%d_%H%M%S", localtime)
        ad_dir_path = 'AD_info' #上傳資訊儲存目錄
        if not os.path.exists(ad_dir_path):
            os.mkdir(ad_dir_path)
            
        if not os.path.exists(ad_dir_path + "/" + date_temp):
            os.mkdir(ad_dir_path + "/" + date_temp)

        # 現在路徑 + 儲存目錄 + 現在時間 + 檔名
        ad_file_path = os.path.join(os.getcwd(), str(ad_dir_path),str(date_temp),str(machineid) + '_' + str(times_temp) + '_' + str(_camid) + '_' + str(action_cname) + '.txt')
        ftp_save_filename = str(machineid) + '_' + str(times_temp) + '_' + str(_camid) + '_' + str(action_id) + '.txt'
        # punch_file_simple_path = "./punch/" + str(timestamp) + '_' + name + '_0.txt'
        # print(ad_file_path)

        # 建立txt檔並上傳FTP
        if not os.path.isfile(str(ad_file_path)):
            f = open(ad_file_path, 'w')
            f.write(str(machineid) + '_' + str(times_temp) + '_' + str(_camid) + '_' + str(action_cname))
            f.close()

            # try:
            alexfun.ftpupload(ad_file_path,ftp_save_filename)
            # tftp = threading.Thread(target=alexfun.ftpupload,daemon=True,args=(ad_file_path,ftp_save_filename,))
            # tftp.start()

            #LINE NOTIFY
            # _alert_time_1 = time.strftime("%Y%m%d_%H%M%S", localtime)
            
            if not os.path.exists(str(_alert_dir)):
                os.mkdir(str(_alert_dir))
            
            if not os.path.exists(str(_alert_dir) + "/" + str(date_temp)):
                os.mkdir(str(_alert_dir) + "/"  + str(date_temp))

            filename = str(_alert_dir) + '/' + str(date_temp) + '/' + str(machineid) + '_'  + str(times_temp) + '_' + str(_camid) + '_' + str(action_id) + '.jpg'
            mov_file = str(_alert_dir) + '/' + str(date_temp) + '/' + str(machineid) + '_'  + str(times_temp) + '_' + str(_camid) + '_' + str(action_id) + '.mp4'
            # print(filename)
            cv2.imwrite(filename, image)
            alexfun.lineNotifyMessage(str(_camid) + '_' + str(action_cname) + ' 通知',filename)
            
            # 20230205-alex- insert into sqlite3 database
            cdate = time.strftime("%Y%m%d", localtime)
            ctime = time.strftime("%H%M%S", localtime)            
            alexsqlite._event_report_insert(cdate,ctime,machineid,_camid,action_id,action_cname,filename,mov_file,'S','N','Y')
            
            # 20230206-alex-save frame_temp 35frame
            _mov_fps = 10
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            # print(mov_width)
            # print(mov_height)
            frame_temp_out = cv2.VideoWriter(mov_file, fourcc, _mov_fps, (mov_width, mov_height))
            for temp in frame_temp:
                frame_temp_out.write(temp)
            frame_temp_out.release()
            
    # #建立資料並上傳(不傳line notify)
    def punch_txt_log(machineid,_camid,_msg):
        # 取得現在時間
        localtime = time.localtime()
        date_temp = time.strftime("%Y%m%d", localtime)
        times_temp = time.strftime("%Y%m%d_%H%M%S", localtime)
        ad_dir_path = 'AD_info' #上傳資訊儲存目錄
        if not os.path.exists(ad_dir_path):
            os.mkdir(ad_dir_path)
            
        if not os.path.exists(ad_dir_path + "/" + date_temp):
            os.mkdir(ad_dir_path + "/" + date_temp)

        # 現在路徑 + 儲存目錄 + 現在時間 + 檔名
        ad_file_path = os.path.join(os.getcwd(), str(ad_dir_path),str(date_temp),str(machineid) + '_' + str(times_temp) + '_' + str(_camid) + '_' + str(_msg) + '.txt')
        ftp_save_filename = str(machineid) + '_' + str(times_temp) + '_' + str(_camid) + '_' + str(_msg) + '.txt'
        # punch_file_simple_path = "./punch/" + str(timestamp) + '_' + name + '_0.txt'
        # 建立txt檔並上傳FTP
        if not os.path.isfile(ad_file_path):
            f = open(ad_file_path, 'w')
            f.write(str(machineid) + '_' + str(times_temp) + '_' + str(_camid) + '_' + str(_msg))
            f.close()
            # try:
            alexfun.ftpupload(ad_file_path,ftp_save_filename)
            # tftp = threading.Thread(target=alexfun.ftpupload,daemon=True,args=(ad_file_path,ftp_save_filename,))
            # tftp.start()
            
    #=====================================================
    # # 把警示圖片發到LineNotify
    # def puch_linenoitfy(webcamsn,_alert_dir,actions,actions_cname,image):
    #     localtime = time.localtime()
    #     _alert_time_1 = time.strftime("%Y%m%d_%H%M%S", localtime)
    #     cv2.imwrite(_alert_dir + '/' + _alert_time_1 + '_' + webcamsn + '_' + actions + '.jpg' , image)
    #     alexfun.lineNotifyMessage(actions_cname + ' 通知',_alert_dir + '/' + _alert_time_1 + '_' + webcamsn + '_' + actions + '.jpg')
    #=====================================================
    # 讀入txt裡所有的動作並轉成numpy.array
    def readtxt_tonparray(filename):
        filename = Path(filename)
        file = open(filename,'r', encoding='UTF-8')
        list_arr = file.readlines()
        l = len(list_arr)
        for i in range(l):
            list_arr[i] = list_arr[i].strip()
            list_arr[i] = list_arr[i].strip('[]')
            list_arr[i] = list_arr[i].strip(",")
        a = np.array(list_arr)
        a.astype(str)
        file.close()
        return a
    #======================================================
    # 把cv2轉成pil寫上中文再轉回cv2
    def Draw_ch_txt(image,position,color,strtxt):
        #20221103-alex-設定中文字型
        font = ImageFont.truetype('./Fonts/NotoSansCJKtc-Medium.otf', 30, encoding='utf-8')
        img_PIL = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # 文字輸出位置
        # position = (120, 200)
        # 輸出內容
        # str = '開始轉換'
        # 需要先把輸出的中文字元轉換成Unicode編碼形式
        # strtxt = strtxt.encode('utf-8')
        draw = ImageDraw.Draw(img_PIL)
        draw.text(position, strtxt, font=font, fill=color)
        img_OpenCV = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR) #把PIL轉成cv2
        return img_OpenCV

    # 把cv2轉成pil寫上中文再轉回cv2 - 可自訂字型大小
    def Draw_ch_txt_size(image,fontsize,position,color,strtxt):
        #20221103-alex-設定中文字型
        font = ImageFont.truetype('fonts/NotoSansCJKtc-Medium.otf', fontsize, encoding='utf-8')
        img_PIL = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # 文字輸出位置
        # position = (120, 200)
        # 輸出內容
        # str = '開始轉換'
        # 需要先把輸出的中文字元轉換成Unicode編碼形式
        # strtxt = strtxt.encode('utf-8')
        draw = ImageDraw.Draw(img_PIL)
        draw.text(position, strtxt, font=font, fill=color)
        img_OpenCV = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR) #把PIL轉成cv2
        return img_OpenCV
    #======================================================
    # 20221120 - alex - 把actions_color裡面的hex數值(ffffff)轉換成rgb(255,255,255)
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb
    #======================================================
    # 發出警示音
    def play_sound():
        # pygame.mixer.init()
        # pygame.mixer.music.load('bbb.mp3')
        # pygame.mixer.music.play()
        # winsound.Beep(freq220, duration20)
        # winsound.Beep(freq330, duration20)
        # winsound.Beep(freq440, duration20)  
        mixer.init() 
        beep=mixer.Sound("bbb.mp3")
        beep.play()
        time.sleep(3)
    #======================================================
    # 把訊息寫到image上(支援中文)
    def prep_alert_msg(image):
        image = alexfun.Draw_ch_txt_size(image,50,(3,10),(0, 255, 0),'按下q鍵結束預覽')
        image = alexfun.Draw_ch_txt_size(image,50,(3,80),(0, 255, 0),'並於6秒後開始錄製.')
        return image   
    #==============================================================
    # 轉成灰階並做圖像二值化
    def optimization(image):
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        output1 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        img_gray2 = cv2.medianBlur(img_gray, 5)   # 模糊化
        output2 = cv2.adaptiveThreshold(img_gray2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return img_gray
    #======================
class alexface():
    #======================================================
    #======================================================
    # 以下為 人臉辨識區
    #======================================================
    # 人臉辨識
    # 畫線
    def drop_line(frame,x1,y1,x2,y2):
        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    
    def get_detect_area(cam_width,cam_height):
        # 上左x
        lux1 = int(cam_width / 8) 
        # 上左y
        luy1 = int(cam_height / 8)
        width_area = int(cam_width-lux1)
        height_area = int(cam_height-luy1)
        return lux1,luy1,width_area,height_area

    # 畫出限制區
    def detect_area(frame,cam_width,cam_height):
        # 置直中線
        # cf.drop_line(frame,int(cam_width/2),0,int(cam_width/2),int(cam_height))
        # 上左橫線
        lux1 = int(cam_width / 4) / 2
        lux2 = lux1 + int(lux1)            
        # 上右橫線
        rux1 = int(cam_width /4 ) * 3
        rux2 = int(cam_width /4 ) * 3 + lux1    
        # 下左橫線
        ldx1 = lux1
        ldx2 = lux1 + int(lux1)
        # 下右橫線
        rdx1 = int(cam_width / 4) * 3
        rdx2 = int(cam_width / 4) * 3 + lux1

        # 上左直線
        luy1 = int(cam_height / 8)
        luy2 = int(cam_height / 2) - luy1
        # 上右直線
        ruy1 = luy1
        ruy2 = luy2
        # 左下直線
        ldy1 = int(cam_height / 2) + luy1
        ldy2 = int(cam_height) - luy1
        #右下直線
        rdy1 = ldy1
        rdy2 = ldy2
        
        # 左上/右上/左下/右下 橫線
        alexfun.drop_line(frame,lux1,luy1,lux2,luy1)                    
        alexfun.drop_line(frame,rux1,luy1,rux2,luy1)             
        alexfun.drop_line(frame,ldx1,ldy2,ldx2,ldy2)
        alexfun.drop_line(frame,rdx1,ldy2,rdx2,rdy2)

        # 左上/右上/左下/右下 直線
        alexfun.drop_line(frame,lux1,luy1,lux1,luy2)
        alexfun.drop_line(frame,rux2,luy1,rux2,luy2)
        alexfun.drop_line(frame,lux1,ldy1,lux1,ldy2)
        alexfun.drop_line(frame,rux2,rdy1,rux2,rdy2)
        
    def img_resize(self,image):
        height, width = image.shape[0], image.shape[1]
        # 设置新的图片分辨率框架
        width_new = 640
        height_new = 480
        # 判断图片的长宽比率
        if width / height >= width_new / height_new:
            img_new = cv2.resize(image, (width_new, int(height * width_new / width)))
        else:
            img_new = cv2.resize(image, (int(width * height_new / height), height_new))

        del image
        return img_new

    def img_save(self,model_path,userid,username,image):
        # 檢查目錄是否存在
        if not os.path.isdir(model_path):
            os.mkdir(model_path)

        # 檢查目錄+ userid目錄是否存在
        if not os.path.isdir(model_path + '/' + userid):
            os.mkdir(model_path + '/' + userid) #目錄不在建立目錄
        else:
            #目錄存在清除裡面所有檔案
            ds = os.listdir(model_path + '/' + userid)
            for d in ds:
                if os.path.isfile(model_path + '/' + userid + '/' + d): #如果列表項是檔案
                    os.remove(model_path + '/' + userid + '/' + d) #直接刪除    

        cv2.imwrite(model_path + '/' + userid + '/' + username + '.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 100])

    def compute(self,img, min_percentile, max_percentile):
        max_percentile_pixel = np.percentile(img, max_percentile)
        min_percentile_pixel = np.percentile(img, min_percentile)

        return max_percentile_pixel, min_percentile_pixel

    def aug(self,src):
        """圖像亮度增強"""
        # if self.get_lightness(src)>130:
        #     print("圖片亮度足夠，不做增強")
        # # 先計算分位點，去掉像素值中少數異常值，這個分位點可以自己配置。
        # # 比如1中直方圖的紅色在0到255上都有值，但是實際上像素值主要在0到20內。
        max_percentile_pixel, min_percentile_pixel = self.compute(src, 1, 99)
        
        # 去掉分位值區間之外的值
        src[src>=max_percentile_pixel] = max_percentile_pixel
        src[src<=min_percentile_pixel] = min_percentile_pixel

        # 將分位值區間拉伸到0到255，這裏取了255*0.1與255*0.9是因爲可能會出現像素值溢出的情況，所以最好不要設置爲0到255。
        out = np.zeros(src.shape, src.dtype)
        cv2.normalize(src, out, 255*0.1,255*0.9,cv2.NORM_MINMAX)

        return out

    def get_lightness(self,src):
        # 計算亮度
        hsv_image = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
        lightness = hsv_image[:,:,2].mean()
        return  lightness

    def imgeAdjustmentLightness(self,img) :
        B, G, R = cv2.split(img)
        b = copy.deepcopy(B)
        g = copy.deepcopy(G)
        r = copy.deepcopy(R)
        for row in range(len(b)) :
            for col in range(len(b[row])) :
                b[row][col] = b[row][col] + 20
                g[row][col] = g[row][col] + 20
                r[row][col] = r[row][col] + 20
        merged = cv2.merge([b, g, r])
        return merged

    def modify_lightness_saturation(self,img):

        origin_img = img

        # 圖像歸一化，且轉換為浮點型
        fImg = img.astype(np.float32)
        fImg = fImg / 255.0

        # 顏色空間轉換 BGR -> HLS
        hlsImg = cv2.cvtColor(fImg, cv2.COLOR_BGR2HLS)
        hlsCopy = np.copy(hlsImg)

        lightness = 0 # lightness 調整為  "1 +/- 幾 %"
        saturation = 300 # saturation 調整為 "1 +/- 幾 %"

        # 亮度調整
        hlsCopy[:, :, 1] = (1 + lightness / 100.0) * hlsCopy[:, :, 1]
        hlsCopy[:, :, 1][hlsCopy[:, :, 1] > 1] = 1  # 應該要介於 0~1，計算出來超過1 = 1

        # 飽和度調整
        hlsCopy[:, :, 2] = (1 + saturation / 100.0) * hlsCopy[:, :, 2]
        hlsCopy[:, :, 2][hlsCopy[:, :, 2] > 1] = 1  # 應該要介於 0~1，計算出來超過1 = 1

        # 顏色空間反轉換 HLS -> BGR 
        result_img = cv2.cvtColor(hlsCopy, cv2.COLOR_HLS2BGR)
        result_img = ((result_img * 255).astype(np.uint8))
        return result_img
        # print("High Saturation:")
        # show_img(result_img)