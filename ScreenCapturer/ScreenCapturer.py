#Program created by n00nY
#Contact info:
#       Reddit: https://www.reddit.com/user/CaptainReeetardo
#       GitHub: https://github.com/N00NY/
#For Windows only!!!

from PIL import ImageGrab, Image, ImageTk, ImageFile
from ctypes import windll
import win32api, win32con
import threading
import tkinter
import socket
import time

class ScreenCaptureServer:

    def __init__(self, path, ip, port, x, y):
        self.x = x #x-coordinate of Displayed Screen
        self.y = y #y-coordinate of Displayed Screen
        self.ip = ip
        self.port = port
        self.path = path #path of saved Image
        ImageFile.LOAD_TRUNCATED_IMAGES = True #I don't really know what this does
        self.MAX = 200000 #Maximum bytes received
        self.main = None
        self.label = None
        self.alphabet = [] #Used for keylogger not a pretty way but an efficient one
        for i in range(65, 91):
            self.alphabet.append(i)
        for i in range(48,58):
            self.alphabet.append(i)
        self.alphabet.append(ord("\t"))
        self.alphabet.append(ord(" "))
        self.alphabet.append(win32con.VK_DIVIDE) #Numpad /
        self.alphabet.append(win32con.VK_MULTIPLY) #Numpad *
        self.alphabet.append(win32con.VK_SUBTRACT) #Numpad -
        self.alphabet.append(win32con.VK_ADD) #Numpad +
        self.alphabet.append(188) # VK_OEM_COMMA
        self.alphabet.append(190) # VK_OEM_PERIOD
        self.alphabet.append(46) # VK_DELETE
        self.alphabet.append(13) # VK_RETURN
        self.alphabet.append(8) # VK_BACK
        self.alphabet.sort()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #First socket used for image and cursor position transfer
        self.s.bind((ip, port)) #Your IP and port
        self.s.listen(2)

    def getLetter(self):
        for i in self.alphabet:
            if win32api.GetAsyncKeyState(i) < 0: #If Key is pressed
                return str(i)
        return "No data"

    def getCursorPositionLocal(self):
        mx = abs(sekf.main.winfo_x()) 
        my = abs(self.main.winfo_y()) 
        mpx = abs(self.main.winfo_pointerx())
        mpy = abs(self.main.winfo_pointery())
        if (mpx >= mx and mpx<= mx+1280) and (mpy >= my and mpy <= my+720):
            x = abs(self.main.winfo_pointerx()) - abs(mx)
            x = str(round(x * 1.5))
            y = abs(self.main.winfo_pointery()) - abs(my)
            y = str(round(y * 1.5))
            mes = x + "x"  + y
            return True
        else:
            return False
        

    def getMouseAndKeyboard(self):
        mc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Second socket: for keylogger
        mc.bind((self.ip, 1338))
        mc.listen(2)
        c = mc.accept()[0]
        while True:
            try:
                ret = self.getCursorPositionLocal()
                if win32api.GetAsyncKeyState(0x01) < 0 and ret:
                    c.send(b"LeftMouseButton")
                    #print("[ + ] Left Click")
                elif win32api.GetAsyncKeyState(0x02) < 0 and ret:
                    c.send(b"RightMouseButton")
                    #print("[ + ] Right Click")
                else:
                    letter = self.getLetter()
                    if letter == "No data":
                        c.send(b"No data")
                    else:
                        c.send(letter.encode())
            except:
                continue
            time.sleep(0.07)

    def getCursorPosition(self, con):
        mx = abs(self.main.winfo_x())
        my = abs(self.main.winfo_y())
        mpx = abs(self.main.winfo_pointerx())
        mpy = abs(self.main.winfo_pointery())
        #print("Not yet sent")
        if (mpx >= mx and mpx<= mx+1280) and (mpy >= my and mpy <= my+720):
            x = abs(self.main.winfo_pointerx()) - abs(mx)
            x = str(round(x * 1.5))
            y = abs(self.main.winfo_pointery()) - abs(my)
            y = str(round(y * 1.5))
            mes = x + "x"  + y
            #print(mes)
            con.send(mes.encode()) #CursorPosisition
            #print("sent")
        else:
            con.send(b"No data")

    def getScreen(self, path):
        t_mouse = threading.Thread(target=self.getMouseAndKeyboard) #Keylogger
        time.sleep(2)
        print("[ * ] Waiting for connection...")
        con, addr = self.s.accept()
        print("[ + ]" + addr[0] + " has  connected on port " + str(addr[1]))
        t_mouse.start() #Starts Keylogger
        ("[ + ] getMouseAndKeyboard started")
        img = True # decides between img1 and img2
        while True:
            try:
                mes = con.recv(self.MAX).decode()
                if mes == "sending": #Checks if mes is the start of a new image
                    #print(mes + str(len(mes)))
                    f = open(path, "wb")
                    f.write(con.recv(self.MAX)) # first part of image
                    time.sleep(0.001)
                    f.write(con.recv(self.MAX)) # second part of image
                    f.close()
                    #print("[ + ] Image received")
                    #Uses two image variable to eliminate flickering
                    #Which is quite annoying, trust me
                    #And it's a simple fix on top of that
                    if img:
                        img1 = Image.open(path)
                        img1 = img1.resize((1280, 720))
                        img1 = ImageTk.PhotoImage(img1)
                        self.label["image"] = img1
                        self.label.update()
                        img = False
                    else:
                        img2  = Image.open(path)
                        img2 = img2.resize((1280, 720))
                        img2 = ImageTk.PhotoImage(img2)
                        self.label["image"] = img2
                        self.label.update()
                        img = True
                    time.sleep(0.01)
                    #print("[ * ] Getting Cursor")
                    self.getCursorPosition(con)
                    time.sleep(0.01)
                elif mes == "No data":
                    con.send(b"No data")
                    continue
            except KeyboardInterrupt: #Doesn't work
                self.label["image"] = None
                self.label.update()
                self.main.geometry("800x600")
                self.main.update()
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

    def CreateTkinter(self, x, y):
        self.main = tkinter.Tk()
        self.label = tkinter.Label(self.main)
        self.label.place(x=0, y=0)
        self.main.geometry("1280x720+{0}+{1}".format(x, y)) #Change the +50+50 part to place the window
        self.main.resizable(False, False)
        self.main.overrideredirect(1) #No windowframe for better measurments
        #print("[ + ] getScreen started")
        self.main.mainloop()

    def record(self):
        t_main = threading.Thread(target=self.CreateTkinter, args=(self.x, self.y))
        t_main.setDaemon(True)
        t_main.start()
        time.sleep(3)
        t = threading.Thread(target=self.getScreen, args=(self.path,))
        t.start()

    def destroy(self): #Kills the process
        import os

        os.kill(os.getpid(), 1)


class ScreenCaptureClient:

    def __init__(self, path, ip, port):
        self.path = path #Path of stored screencap
        self.ip = ip
        self.port = port
        self.MAX = 200000 #Maximum bytes received
        self.s = socket.socket()#First socket used for image and cursor position transfer
        user = windll.user32
        user.SetProcessDPIAware() #Used to get image of fullscreen

    def getMouseAndKeyboard(self):
        mc = socket.socket() #Second socket used for keylogger
        mc.connect((self.ip, 1338)) #IP and port of server
        #print("[ + ] Mouse And Keyboard Connected")
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

    def record(self):
        self.s.connect((self.ip, self.port))#IP and port of server
        time.sleep(3)
        t_mouse = threading.Thread(target=self.getMouseAndKeyboard) #Used for taking server inputs
        t_mouse.start()
        while True:
            im = ImageGrab.grab() #Create a screenshot
            im.save(self.path)
            try:
                f = open(self.path, "rb") #Open the saved screenshot
                con = f.read()
                f.close()
                #print("[ + ] Sending Image")
                if len(con) % 2 == 0:#Can't send the image in at once but two parts will do
                    #print("Even")
                    self.s.send(b"sending")
                    self.s.sendall(con[0:int(len(con)/2)])
                    time.sleep(0.001)
                    self.s.sendall(con[int(len(con)/2):len(con)])
                else:
                    #print("Odd")
                    self.s.send(b"sending") # 1
                    self.s.sendall(con[0:int(len(con)/2 + 0.5)])
                    time.sleep(0.001)
                    self.s.sendall(con[int(len(con)/2 + 0.5):len(con)])
                #print("[ + ] Image sent")
            except:
                self.s.send(b"No data")
                #print("[ - ] Image not sent")
                continue
            #print("[ * ] Awaiting Cursor Position...")
            try:
                mes = self.s.recv(self.MAX).decode() #Receives the cursor position
                if mes.startswith("No data"):
                    #print(mes)
                    continue
                else:
                    x, y = int(mes.split("x")[0]), int(mes.split("x")[1])
                    #print("Coordinates", x, y)
                    win32api.SetCursorPos((x, y))
            except ValueError:
                continue

    def destroy(self):
        import os

        os.kill(os.getpid(), 1)
