#!/usr/bin/python3.5
#this shebang doesn't actually work for me???

# want to make your mouse slower?
# google it.... here are some hints
# xinput  --set-prop  insert_device_id_here  "Device Accel Constant Deceleration"  3
# For Logitech: xinput --set-prop 11 "304" -1.0

# record a screen cast
# ffmpeg -video_size 1800x900 -framerate 25 -f x11grab -i :0.0+100,200 pongtrials.mp4

import pygame
#import asyncio
#import datetime
#import random
#import socket
#import traceback
import string
from sys import stdout
from time import sleep
from pygame.locals import *

# trying to implement threading for smartphone control via UDP / commented out now
'''
from multiprocessing import Queue
from threading import Thread

q = Queue()

host = "192.168.0.5"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

def getUDPmessage():
	message, address = s.recvfrom(8192)
	def my_callback(channel):
		q.put(True)

t = Thread(target=getUDPmessage)
t.daemon = True
t.start()
'''

#lets preload images to use as the ball and paddle!!!
myimage = pygame.image.load("eugene.png")
imagerect = myimage.get_rect().size
image_rect_x, image_rect_y = imagerect
print(image_rect_x)
print(image_rect_y)

myimage2 = pygame.image.load("paddle_slug.png")
imagerect2 = myimage2.get_rect().size
image2_rect_x, image2_rect_y = imagerect2
print(image2_rect_x)
print(image2_rect_y)

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

pygame.init()
#Initializing the display window
size = (1800,900)
screen = pygame.display.set_mode(size)
#screen = pygame.display.set_mode((size), pygame.FULLSCREEN)
pygame.display.set_caption("pong")
pygame.mouse.set_visible(0)
#Starting coordinates of the paddle
rect_x = 1375
rect_y = 0
#initial position of the mouse
rect_mouse_x = 1375
rect_mouse_y = 0
#initial position of the ball
ball_x = 350
ball_y = 111
#speed of the ball
ball_change_x = 7
ball_change_y = 7
hits = 0
misses = 0

#draws the paddle. Also restricts its movement between the edges
#of the window.
def drawrect(screen,x,y):
    if x <= 0:
        x = 0
    if x >= (1800-150):
        x = (1800-150)
    pygame.draw.rect(screen,RED,[x,y,150,30])

#game's main loop
done = False
clock=pygame.time.Clock()

pygame.mouse.set_pos(rect_mouse_x, rect_mouse_y)

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				done = True
			elif event.key == K_c:
				# recenter your paddle or your swivel stool if that's what your into
                                pygame.mouse.set_pos(1375,450)
		elif event.type == pygame.MOUSEMOTION:
			#print("mouse at {}".format(event.pos))
			#print(score)
			#stdout.flush()
			#print("mouse reletive {}".format(event.rel))
			rect_mouse_x, rect_mouse_y = event.pos
			rect_mouse_y = 0
			rect_mouse_x = 3.5 * (1650 - rect_mouse_x)

	# get data and print it, add the mapping code after this socket is tested
	# message, address = s.recvfrom(8192)
	# data = message.split(",")
	# q.get()
	# print(message)
	# gyro = data[4]
	# print(gyro)
	# well that's not working....


	screen.fill(WHITE)
	rect_x = rect_mouse_x
	rect_y = 880
	ball_x += ball_change_x 
	#* ((hits*0.1)+1)
	ball_y += ball_change_y 
	#* ((hits*0.1)+1)


#this handles the movement of the ball - corner conditions
	if ball_x<0: #left
		ball_x=0
		ball_change_x = ball_change_x * -1
	elif ball_x> 1800 - image_rect_x: #right
		ball_x= 1800 - image_rect_x
		ball_change_x = ball_change_x * -1
	elif ball_y<1:#top
		ball_y=1
		ball_change_y = ball_change_y * -1
	elif (ball_x+(image_rect_x/2))>rect_x and (ball_x+(image_rect_x/2))<rect_x+image2_rect_x and ball_y > (900 - image2_rect_y - image_rect_y):#bottom w paddle hit
		ball_change_y = ball_change_y * -1
		hits = hits + 1
	elif ball_y>900- image_rect_y:#bottom w paddle miss
		ball_change_y = ball_change_y * -1
		misses = misses + 1


	#drawball(screen,ball_x,ball_y)
	#pygame.draw.rect(screen,BLACK,[ball_x,ball_y,20,20])
	#screen.blit(myimage, (ball_x, ball_y))
	#drawpaddle(screen,ball_x,ball_y)
	#drawrect(screen,rect_x,rect_y)
	screen.blit(myimage2, (rect_x, 900 - image2_rect_y))
	screen.blit(myimage, (ball_x, ball_y))

	#score board and some debug output
	font= pygame.font.SysFont('Calibri', 75, False, False)
	small_font= pygame.font.SysFont('Calibri', 25, False, False)
	text = font.render("Hits = " + str(hits), True, BLACK)
	text_mouse = small_font.render("Mouse X Postion = " + str(rect_mouse_x), True, BLACK)
	text2 = font.render("Misses = " + str(misses), True, BLACK)
	screen.blit(text,[550,400])
	screen.blit(text2,[950,400])
	screen.blit(text_mouse,[100,100])


	pygame.display.flip()
	clock.tick(30)

pygame.quit()

