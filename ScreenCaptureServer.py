#Program created by n00nY
#Contact info:
#       Reddit: https://www.reddit.com/user/CaptainReeetardo
#       GitHub: https://github.com/N00NY/
#For Windows only!!!

from PIL import ImageGrab, Image, ImageTk, ImageFile
import tkinter
import time
from ctypes import windll
import win32api, win32con
import threading
import socket

ImageFile.LOAD_TRUNCATED_IMAGES = True #I don't know what that does, but it works
path = "C:\\screen.jpg"  #Can be changed to your hearts content
MAX = 200000 #Maximum bytes received
main = None 
label = None
alphabet = [] #Used for keylogger not a pretty way but an efficient one
for i in range(65, 91):
    alphabet.append(i)
for i in range(48,58):
    alphabet.append(i)
alphabet.append(ord("\t"))
alphabet.append(ord(" "))
alphabet.append(win32con.VK_DIVIDE) #Numpad /
alphabet.append(win32con.VK_MULTIPLY) #Numpad *
alphabet.append(win32con.VK_SUBTRACT) #Numpad -
alphabet.append(win32con.VK_ADD) #Numpad +
alphabet.append(188) # VK_OEM_COMMA
alphabet.append(190) # VK_OEM_PERIOD
alphabet.append(46) # VK_DELETE
alphabet.append(13) # VK_RETURN
alphabet.append(8) # VK_BACK
alphabet.sort()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #First socket used for image and cursor position transfer
s.bind(("", 1337)) #Your IP and port
s.listen(2)

def getLetter():
    global alphabet

    for i in alphabet:
        if win32api.GetAsyncKeyState(i) < 0:
            return str(i)
    return "No data"
        
def getCursorPositionLocal():
    global main

    mx = abs(main.winfo_x()) 
    my = abs(main.winfo_y()) 
    mpx = abs(main.winfo_pointerx())
    mpy = abs(main.winfo_pointery())
    if (mpx >= mx and mpx<= mx+1280) and (mpy >= my and mpy <= my+720):
        x = abs(main.winfo_pointerx()) - abs(mx)
        x = str(round(x * 1.5))
        y = abs(main.winfo_pointery()) - abs(my)
        y = str(round(y * 1.5))
        mes = x + "x"  + y
        return True
    else:
        return False
    
def getMouseClick():
    mc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mc.bind(("", 1338))
    mc.listen(2)
    c = mc.accept()[0]
    while True:
        try:
            ret = getCursorPositionLocal()
            if win32api.GetAsyncKeyState(0x01) < 0 and ret:
                c.send(b"LeftMouseButton")
                print("[ + ] Left Click")
            elif win32api.GetAsyncKeyState(0x02) < 0 and ret:
                c.send(b"RightMouseButton")
                print("[ + ] Right Click")
            else:
                letter = getLetter()
                if letter == "No data":
                    c.send(b"No data")
                else:
                    c.send(letter.encode())
        except:
            continue
        time.sleep(0.07)
    
def getCursorPosition(con):
    #To cut it down
    #This function sends the cursor position if the cursor is inside the
    #tkinter window or main
    global main
    
    mx = abs(main.winfo_x())
    my = abs(main.winfo_y())
    mpx = abs(main.winfo_pointerx())
    mpy = abs(main.winfo_pointery())
    print("Not yet sent")
    if (mpx >= mx and mpx<= mx+1280) and (mpy >= my and mpy <= my+720):
        x = abs(main.winfo_pointerx()) - abs(mx)
        x = str(round(x * 1.5))
        y = abs(main.winfo_pointery()) - abs(my)
        y = str(round(y * 1.5))
        mes = x + "x"  + y
        print(mes)
        con.send(mes.encode()) #CursorPos
        print("sent")
    else:
        con.send(b"No data") #  4

def getScreen(path):
    global main
    global label
    global s
    global MAX

    t_mouse = threading.Thread(target=getMouseClick) #Keylogger
    time.sleep(2)
    print("[ * ] Waiting for connection")
    con, addr = s.accept()
    print("[ + ]" + addr + " has  connected")
    t_mouse.start() #Starts Keylogger
    print("[ + ] getMouseAndKeyboard started")
    img = True # decides between img1 and img2
    while True:
        try:
            mes = con.recv(MAX).decode()
            if mes == "sending": #Checks if mes is the start of a new image
                print(mes + str(len(mes)))
                f = open(path, "wb")
                f.write(con.recv(MAX)) # first part of image
                time.sleep(0.001)
                f.write(con.recv(MAX)) # second part of image
                f.close()
                print("[ + ] Image received")
                #Uses two image variable to eliminate flickering
                #Which is quite annoying, trust me
                #And it's a simple fix on top of that
                if img:
                    img1  = Image.open(path)
                    img1 = img1.resize((1280, 720))
                    img1 = ImageTk.PhotoImage(img1)
                    label["image"] = img1
                    label.update()
                    img = False
                else:
                    img2  = Image.open(path)
                    img2 = img2.resize((1280, 720))
                    img2 = ImageTk.PhotoImage(img2)
                    label["image"] = img2
                    label.update()
                    img = True
                time.sleep(0.01)
                print("[ * ] Getting Cursor")
                getCursorPosition(con)
                time.sleep(0.01)
            elif mes == "No data":
                con.send(b"No data")
                continue
        except KeyboardInterrupt: #Doesn't work
            label["image"] = None
            label.update()
            main.geometry("800x600")
            main.update()
            con.send(b"No data")
            break
        except OSError:
            time.sleep(0.1)
            con.send(b"No data")
        except ConnectionResetError:
            con.close()
            s.close()
            break
        except:
            con.send(b"No data")
    #print("[ + ] Success")
    return

def main():
    global main
    global label
    global path
    
    main = tkinter.Tk()
    label = tkinter.Label(main)
    label.place(x=0, y=0)
    main.geometry("1280x720+50+50")
    main.resizable(False, False)
    main.overrideredirect(1)#no window frame for better measurments
    print("[ + ] getScreen started")
    main.mainloop()

t_main = threading.Thread(target=main)
t_main.setDaemon(True)# I don't if changes anything at the performance
t_main.start()
time.sleep(3)
t = threading.Thread(target=getScreen, args=(path,))
t.start()
