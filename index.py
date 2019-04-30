from tkinter import *
import sqlite3
import cv2
import numpy as np
from datetime import datetime as dt
import time
import os
import smtplib
import getpass
from email.mime.text import MIMEText  #MIME-multipurpose internet mail extensions
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart


def prgm():
    cap= cv2.VideoCapture(0)
    i=0
    j=11
    Sum_of_frames=0             
    filename='D:\\out.avi'
    codec=cv2.VideoWriter_fourcc('X','V','I','D')       #4 character code
    framerate=30
    resolution= (640,480)
    Vidfile=cv2.VideoWriter(filename,codec,framerate,resolution)
    low=np.array([50])
    high=np.array([190])
    if cap.isOpened():
        ret,frame=cap.read()
    else:
        ret=False
    while ret:
        ret,frame=cap.read()
        while i!=50:            #i-> no. of frames
            i+=1
            ret,frame=cap.read()
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            image_mask=cv2.inRange(gray,low,high)
            if i<40:
                continue
            if 40<=i<50:
                Sum_of_frames+=np.sum(image_mask)
            elif i==50:
                Avg_of_frames=Sum_of_frames/10
                print('Avg_of_frames= ',Avg_of_frames)
        while j<5:              #for new static frame
            j+=1
            ret,frame=cap.read()
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            image_mask=cv2.inRange(gray,low,high)
            if j<5:
                Sum_of_frames+=np.sum(image_mask)
            elif j==5:
                Avg_of_frames=Sum_of_frames/4
                print('Avg_of_frames= ',Avg_of_frames)
            
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        image_mask=cv2.inRange(gray,low,high)
        #print(np.sum(image_mask))
        cv2.imshow("original video feed",frame)
        org_frame=np.sum(image_mask)
        Vidfile.write(frame)
        #cv2.imshow('imgmask',image_mask)
        path="F:\\New folder\img"
        ext='.jpg'
        now=dt.now()
        outpath=path+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)+ext
        
        if org_frame>(1.10*Avg_of_frames) or org_frame<(0.90*Avg_of_frames):
            print("There is Some Major changes in room")
            Sum_of_frames=0
            j=0
            cv2.imwrite(outpath,frame)
            maiill(outpath)
        
        if cv2.waitKey(1)==27:
            cv2.destroyAllWindows()
            Vidfile.release()
            cap.release()
            break
     

root = Tk()
root.title("Python: Simple Login Application")
width = 400
height = 280
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

#==============================METHODS========================================
def Database():
    global conn, cursor
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")       
    cursor.execute("SELECT * FROM `member` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `member` (username, password) VALUES('admin', 'admin')")
        conn.commit()
    
def Login(event=None):
    Database()


    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            HomeWindow()
            USERNAME.set("admin")
            PASSWORD.set("admin")
            lbl_text.config(text="")
        else:
            lbl_text.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")   
    cursor.close()
    conn.close()

def HomeWindow():
    root=Tk()
    root.title("WELCOME!")
    width = 800
    height = 280
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)

    Top = Frame(root, bd=2,  relief=RIDGE)
    Top.pack(side=TOP, fill=X)
    Form = Frame(root, height=200)
    Form.pack(side=TOP, pady=20)

    EMAIL = StringVar()

    lbl_title = Label(Top, text = "WELCOME", font=('arial', 15))
    lbl_title.pack(fill=X)
    lbl_title = Label(Top, text = "Let's see what's happening in our house! For details,check your mail.", font=('arial', 15))
    lbl_title.pack(fill=X)
    #lbl_username = Label(Form, text = "Email-id:", font=('arial', 14), bd=15)
    #lbl_username.grid(row=0, sticky="e")
    #lbl_text = Label(Form)
    #lbl_text.grid(row=2, columnspan=2)

    #username = Entry(Form, textvariable=EMAIL, font=(14))
    #username.grid(row=0, column=1)

    btn_login = Button(Form, text="OK", width=45, command=prgm())
    btn_login.grid(pady=25, row=3, columnspan=2)

       
#==============================VARIABLES======================================
USERNAME = StringVar()
PASSWORD = StringVar()

#==============================FRAMES=========================================
Top = Frame(root, bd=2,  relief=RIDGE)
Top.pack(side=TOP, fill=X)
Form = Frame(root, height=200)
Form.pack(side=TOP, pady=20)

#==============================LABELS=========================================
lbl_title = Label(Top, text = "Python: Simple Login Application", font=('arial', 15))
lbl_title.pack(fill=X)
lbl_username = Label(Form, text = "Username:", font=('arial', 14), bd=15)
lbl_username.grid(row=0, sticky="e")
lbl_password = Label(Form, text = "Password:", font=('arial', 14), bd=15)
lbl_password.grid(row=1, sticky="e")
lbl_text = Label(Form)
lbl_text.grid(row=2, columnspan=2)

#==============================ENTRY WIDGETS==================================
username = Entry(Form, textvariable=USERNAME, font=(14))
username.grid(row=0, column=1)
password = Entry(Form, textvariable=PASSWORD, show="*", font=(14))
password.grid(row=1, column=1)

#==============================BUTTON WIDGETS=================================
btn_login = Button(Form, text="Login", width=45, command=Login)
btn_login.grid(pady=25, row=3, columnspan=2)
btn_login.bind('<Return>', Login)



def maiill(path):
    app_data=open(path,'rb').read()
    msg=MIMEMultipart()
    msg['Subject']='python test code'
    msg['From']='jainayushi200@gmail.com'
    password='godietathanshi'
    msg['To']='ayushijain.it19@jecrc.ac.in'
    message='there are some changes in your house'
    text=MIMEText(message)
    msg.attach(text)
    doc=MIMEApplication(app_data,name=os.path.basename(path))
    msg.attach(doc)
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()   #extended smtp or enhanced high light output
    s.starttls()
    s.ehlo()
    s.login(msg['From'],password)
    s.sendmail(msg['From'],msg['To'],msg.as_string())
    s.quit()



