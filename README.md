# ScreenCapturer
Like a VNC but worse

As the title mentions this piece of marvelous software captures the screen of one PC (client) on the network and eventually sends the data back to you (server). Sadly it just supports Windows. This is caused by the fact that I used the win32api which obviously only supports Windows. It also uses two socket which I explain later on.

Going over to the main idea. The idea was that the client (Someone connected to you) sends images over and over to the server (you) which displays the images one by one multiple times in a second. The maximum framerate averages around 15 fps, if you're lucky and the image quality is not that optimal as it scales an Full HD image down to a HD image. Which is meh. 
This part goes over the first created socket. The socket is specialized on the image transfer and mouse movement.

"Like a VNC but worse" 

Well I didn't wrote that just for fun. Because as the program progressed and I finally got a 'moving' image another idea arose in my mind. Why not take control over the clients keyboard and mouse?
Essentially if it comes down to it, it is just another keylogger. This keylogger takes the inputs of the server and then forwards them to the client. So if you move the mouse inside the projected image on your PC it also moves the cursor on the clientside. If you left/right click on your PC it also does so on the clientside. You get the idea. At the moment processes the keys a through z,
0 to 9, listens to the VK_OEM_COMMA and VK_OEM_PERIOD key. It also uses the arithmetic operators on the numpad. And only those on the numpad. As for Return, Backspace, Spacebar, Tab, Delete, it also recognises those. This works totally fine but sometimes it generates multiple character inputs on the clientside which I don't have an answer to, yet.
This part goes over the second created socket. The socket is specialized on the, you guessed it, keylogger part.

So I didn't even went over to the part of trying it with one socket because just thinking about it gives me headaches.

For the source code, I guess it makes more sense that I'll just make comments and try to explain it as best and short as possible.
I don't have footage of it, yet, but I'll add something over the weekend, most likely a gif. And source code I have yet to comment properly.

![alt text](https://media.giphy.com/media/13CoXDiaCcCoyk/giphy.gif)
#Btw I don't own this GIF
