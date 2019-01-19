#Program created by n00nY
#Contact info:
#       Reddit: https://www.reddit.com/user/CaptainReeetardo
#       GitHub: https://github.com/N00NY/
#For Windows only!!!

import socket
import time
from ctypes import windll
import win32api, win32con
from PIL import ImageGrab, Image
import threading      
            
def getMouseAndKeyboard():
    mc = socket.socket() #Second socket used for keylogger
    mc.connect(("", 1338)) #IP and port of server
    print("[ + ] Mouse And Keyboard Connected")
    rb = True
    while True:
        event = mc.recv(1024).decode() #Server input
        if event.startswith("LeftMouseButton"):
            x, y = win32api.GetCursorPos()
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        elif event.startswith("RightMouseButton"):
            x, y = win32api.GetCursorPos()
            if rb:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN , x, y, 0, 0)
                rb = False
            else:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
                rb = True
        elif event.startswith("No data"):
            continue
        else:
            event = int(event)
            win32api.keybd_event(event, 0, 0, 0)
            win32api.keybd_event(event, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.07)

def main():
    MAX = 200000 #Maximum bytes received
    path = "C:\\s.jpg" #Can be changed to your hearts contents
    s = socket.socket() #First socket used for image and cursor position transfer
    s.connect(("", 1337)) #IP and port of server
    #print("Connected")
    user = windll.user32
    user.SetProcessDPIAware() #Used to get image of fullscreen
    while True:
        im = ImageGrab.grab() #Create a screenshot
        im.save(path)
        try:
            f = open(path, "rb") #Open the saved screenshot
            con = f.read()
            f.close()
            print("[ + ] Sending Image")
            if len(con) % 2 == 0:#Can't send the image in at once but two parts will do
                #print("Even")
                s.send(b"sending")
                s.sendall(con[0:int(len(con)/2)])
                time.sleep(0.001)
                s.sendall(con[int(len(con)/2):len(con)])
            else:
                #print("Odd")
                s.send(b"sending") # 1
                s.sendall(con[0:int(len(con)/2 + 0.5)])
                time.sleep(0.001)
                s.sendall(con[int(len(con)/2 + 0.5):len(con)])
            print("[ + ] Image sent")
        except:
            s.send(b"No data")
            print("[ - ] Image not sent")
            continue
        print("[ * ] Awaiting Cursor Position...")
        try:
            mes = s.recv(MAX).decode() #Receives the cursor position
            if mes.startswith("No data"):
                #print(mes)
                continue
            else:
                x, y = int(mes.split("x")[0]), int(mes.split("x")[1])
                print("Coordinates", x, y)
                win32api.SetCursorPos((x, y))
        except ValueError:
            continue
            

t_main = threading.Thread(target=main)# Used for screenshot and 
t_main.start()
time.sleep(1)
t_mouse = threading.Thread(target=getMouseAndKeyboard) #Used for taking server inputs
t_mouse.start()
