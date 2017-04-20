from imagetomp4 import videowriter
import cv2
import PIL
import os


a = PIL.Image.open(os.getcwd() + '/test/1'+'.png')
b = PIL.Image.open(os.getcwd() + '/test/2'+'.png')
videowriter(a, b)
