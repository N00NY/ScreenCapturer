#Program created by n00nY
#Contact info:
#       Reddit: https://www.reddit.com/user/CaptainReeetardo
#       GitHub: https://github.com/N00NY/

from PIL import ImageGrab, Image, ImageFile
import ctypes
import glob

ImageFile.LOAD_TRUNCATED_IMAGES = True
u = ctypes.windll.user32
u.SetProcessDPIAware()
def createGIF(path):
    img = Image.new("RGB", (1280, 720), (255, 255, 255))
    g = glob.glob(path + "\\*")
    frames = []
    print("[ * ] Creating GIF...")
    for i in g:
        tmp = Image.open(i)
        tmp.resize((1280, 720))
        frames.append(tmp)
    img.save(path + "\\your_gif.gif", format="GIF", append_images=frames[0:], save_all=True, duration=150, loop=0)
    print("[ + ] Saved created gif to " + path)

def makeImagesForGIF(path, screenshots):
    print("[ * ] Creating screenshots...")
    for i in range(screenshots):
        img = ImageGrab.grab()
        tmp = "s"*(i+1) + ".jpg"
        img.save(path + "\\{}".format(tmp))
        time.sleep(0.2) #kinda like fps
    print("[ + ] Saved images to " + path)

#createGIF(path) #the path you want to save the images to
#makeImagesForGIF(path, screenshots) #path of images you want to create a GIF of plus how many images should be taken

