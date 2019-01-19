# ScreenCapturer
Like a VNC but worse

As the title mentions this piece of marvelous software captures the screen of one PC (client) on the network and eventually sends the data back to you (server). Sadly it just supports Windows. This is caused by the fact that I used the win32api which obviously only supports Windows. It also uses two socket which I explain later on.

Going over to the main idea. The idea was that the client (Someone connected to you) sends images over and over to the server (you) which displays the images one by one multiple times in a second. The maximum framerate averages around 15 fps, if you're lucky and the image quality is not that optimal as it scales an Full HD image down to a HD image. Which is meh. 
This part goes over the first created socket. The socket is specialized on the image transfer and mouse movement.

"Like a VNC but worse" 

Well I didn't wrote that just for fun. Because as the program progressed and I finally got a 'moving' image, another idea arose in my mind. Why not take control over the clients keyboard and mouse?
Essentially if it comes down to it, it is just another keylogger. This keylogger takes the inputs of the server and then forwards them to the client. So if you move the mouse inside the projected image on your PC it also moves the cursor on the clientside. If you left/right click on your PC it also does so on the clientside. You get the idea. At the moment it processes the keys a through z, 0 to 9, listens to the VK_OEM_COMMA and VK_OEM_PERIOD key. It also uses the arithmetic operators on the numpad. And only those on the numpad. As for Return, Backspace, Spacebar, Tab, Delete, it also recognises those. This works totally fine but sometimes it generates multiple character inputs on the clientside which I don't have an answer to, yet.
This part goes over the second created socket. The socket is specialized on the, you guessed it, keylogger part.

So I didn't even went over to the part of trying it with one socket because just thinking about it gives me headaches.

Serverside:
![alt text](https://github.com/N00NY/ScreenCapturer/blob/master/examples/server.gif)

Clientside:
![alt text](https://github.com/N00NY/ScreenCapturer/blob/master/examples/client.gif)

These are gifs of the class ScreenCapturer. It's basically a module that contains the clientside (ScreenCaptureClient) and the the serverside (ScreenCaptureServer). Remember, first start the server and afterwards the client.
And another problem occured. It seems that it sometimes works and sometimes not. I don't know why this happens and I'll try to fix it later on because I have a pretty good guess what might be causing it to crash or not work randomly. But for now it's like a 50/50 chance of either success or failure.
I'll also provide you with footage taken of a working session.

If you should've questions, please ask them right away (https://www.reddit.com/user/CaptainReeetardo)! I'll try to answer them as soon as possible.
