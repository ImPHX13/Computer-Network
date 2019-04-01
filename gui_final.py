from tkinter import*
import scipy.io
import pickle
from PIL import ImageTk,Image  
import socket
import cv2
import numpy as np
import time
import sys
import threading
import os
global ipc 
global ipr
ipc=' '  #enter IP of other laptop
ipr=' ' #enter IP of this laptop
global change
change=0
global stt
global flag
flag=0
stt=0

def receive():
  global stt
  HOST = ipr
  PORT = 5050

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print('Socket created')

  s.bind((HOST, PORT))
  print('Socket bind complete')

  s.listen(10)
  print('Socket now listening')

  conn, addr = s.accept()

  while True:
      #receive max 100k bytes
      data = conn.recv(100000)
      #print(sys.getsizeof(data))
      #check if data received is credible
      if(sys.getsizeof(data)>5000 and sys.getsizeof(data)<20000):
          nparr = np.fromstring(data, np.uint8)
          frame = cv2.imdecode(nparr, 1)
          try:
              cv2.imshow('frame', frame)
              cv2.waitKey(5) & 0XFF
          except:
              print("LOSS")
      else:
          print("small")
      #cv2.destroyAllWindows()
      data=''
      if stt:
      	break
      	flag=1

def send():
  global stt	
  cap = cv2.VideoCapture(0)
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((ipc, 5050))

  while(True):
      # Capture frame-by-frame
      ret, frame = cap.read()

      # Our operations on the frame come here
      gray = cv2.cvtColor(frame, cv2.IMREAD_COLOR)

      # Display the resulting frame
      #cv2.imshow('frame',gray)
      if(change==1):
      	frame=cv2.bitwise_not(frame)
		# frame = cv2.cvtColor(frame, cv2.COLOR_RGB2Luv)
		# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #use some filter	

      #encode image to send on network
      encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 20]
      data = cv2.imencode('.jpg', frame, encode_param)[1].tostring()
      print(sys.getsizeof(data))

    
      sock.sendall(data)
      if(stt):
      	break


  # When everything done, release the capture
  cap.release()
  cv2.destroyAllWindows()










def register_user():
 
  with open(r'''C:\Users\Aushim\Desktop\CNproject\users.txt''', "rb") as myFile:
    users = pickle.load(myFile)
  username_info = usernamer.get()
  password_info = passwordr.get()
  users[username_info]=password_info
  with open(r'''C:\Users\Aushim\Desktop\CNproject\users.txt''', "wb") as myFile:
    pickle.dump(users, myFile)
  
  Label(screen1, text = "Registration Sucess", fg = "green" ,font = ("calibri", 11)).pack()
 
def log_user():
 
  username_info1 = usernamel.get()
  password_info1 = passwordl.get()
  with open(r'''C:\Users\Aushim\Desktop\CNproject\users.txt''', "rb") as myFile:
    users = pickle.load(myFile)
  print(username_info1,password_info1)
  try:
        (users[username_info1])
  except:
    screen2.destroy()
  if users[username_info1]!=password_info1:
    Label(screen2, text = "Wrong password", fg = "green" ,font = ("calibri", 11)).pack()    
  else:
   screen.destroy()
   video_screen()

    
 
  
def register():
  global screen1
  global usernamer
  global passwordr  
  screen1 = Toplevel(screen)
  screen1.title("Register")
  screen1.geometry("300x250")
  usernamer = StringVar()
  passwordr = StringVar()
 
  Label(screen1, text = "Please enter details below").pack()
  Label(screen1, text = "").pack()
  Label(screen1, text = "Username * ").pack()
  username_entry = Entry(screen1, textvariable = usernamer)
  username_entry.pack()
  Label(screen1, text = "Password * ").pack()
  password_entry =  Entry(screen1, textvariable = passwordr)
  password_entry.pack()
  Label(screen1, text = "").pack()
  Button(screen1, text = "Register", width = 10, height = 1, command = register_user).pack()
 
def login():
  global screen2
  screen2 = Toplevel(screen)
  screen2.title("Login")
  screen2.geometry("300x250")
  global usernamel
  global passwordl
  usernamel = StringVar()
  passwordl = StringVar()
 
  Label(screen2, text = "Please enter details below").pack()
  Label(screen2, text = "").pack()
  Label(screen2, text = "Username * ").pack()
  username_entry = Entry(screen2, textvariable = usernamel)
  username_entry.pack()
  Label(screen2, text = "Password * ").pack()
  password_entry =  Entry(screen2, textvariable = passwordl)
  password_entry.pack()
  Label(screen2, text = "").pack()
  Button(screen2, text = "Login", width = 10, height = 1, command = log_user).pack()
  print("Login session started")
  
  
  
 
def main_screen():
  global username
  global password
  global screen
  global d
  d={} 
  screen = Tk()
  screen.configure(background='grey38')
  screen.geometry("1200x1800")
  screen.title("WHO ARE YOU")
  Label(text = "Video Streaming Service", bg = "grey21", fg='white',width = "300", height = "2", font = ("Calibri", 13)).pack()
  canvas = Canvas(screen, width = 700, height = 400, bg='grey33',  highlightthickness=0,relief='ridge')  
  canvas.pack()  
  img = ImageTk.PhotoImage(Image.open('C:\\Users\\Aushim\\Desktop\\CNproject\\2peeps.jpg'))  
  canvas.create_image(0,-10, image=img, anchor='nw')  
  Button(text = "Login", height = "2", width = "30", command = login).place(x=500,y=500)
  Button(text = "Register",height = "2", width = "30", command = register).place(x=500,y=600)
  screen.mainloop()

def both():
  
  global t2
  global t1
  t1 = threading.Thread(target=send, name='t1') 
  t2 = threading.Thread(target=receive, name='t2')   

  # starting threads 
  t2.start()
  time.sleep(5)  #AAkash change this on your laptop
  t1.start() 
   

  # wait until all threads finish 
  # t1.join() 
  # t2.join() 



def ch():
  global change
  change=not(change)

def sen():
  global f
  t3 = threading.Thread(target=send, name='t3') 
  t3.start()

def rec():
  global f1
  t4 = threading.Thread(target=receive, name='t4') 
  t4.start()
   
def st():
	global stt
	stt=1
  
def video_screen():
    global stt
    s=Tk()
    #screen2.destroy()
    s.geometry("1200x1800")
    s.title("Choose")
    Label(text = "Video Streaming Service", bg = "grey21", fg='white',width = "300", height = "2", font = ("Calibri", 13)).pack()
    canvas = Canvas(s, width = 700, height = 400, bg='grey33',  highlightthickness=0,relief='ridge')  
    canvas.pack()  
    img = ImageTk.PhotoImage(Image.open('C:\\Users\\Aushim\\Desktop\\CNproject\\2peeps.jpg'))  
    canvas.create_image(0,-10, image=img, anchor='nw')  
    Button(text = "Send", height = "2", width = "30", command = sen).place(x=500,y=500)
    Button(text = "Receive",height = "2", width = "30", command = rec).place(x=500,y=600)
    Button(text = "Conference", height = "2", width = "30", command = both).place(x=500,y=700)
    Button(text = "Activate filter", height = "2", width = "30", command = ch).place(x=300,y=400)
    Button(text = "Stop", height = "2", width = "30", command = st).place(x=300,y=500)
    if(stt):
    	s.destroy()
    	sys.exit()
    s.mainloop()
 
 
main_screen()
  
