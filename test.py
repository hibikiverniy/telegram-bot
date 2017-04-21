from imagetomp4 import videowriter
import cv2
import PIL
import os


a = PIL.Image.open(os.getcwd() + '/test/1'+'.png')
b = PIL.Image.open(os.getcwd() + '/test/2'+'.png')
a.save(os.getcwd() + '/list/a'+'.png')
b.save(os.getcwd() + '/list/b'+'.png')
videowriter(a, b)
