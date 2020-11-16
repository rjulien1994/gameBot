from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import os, os.path

limits = [0,200,960,760]
gameSize = [
	limits[2] - limits[0],
	limits[3] - limits[1]
	]
#fight notice (720, 855)
#height cutbax 50px / 560
cutTime = 0

while keyboard.is_pressed('1') == False:
	pos = pyautogui.position()
	limits[0] = pos.x
	limits[1] = pos.y

while keyboard.is_pressed('2') == False:
	pos = pyautogui.position()
	limits[2] = pos.x
	limits[3] = pos.y

print(limits)

def locateItem(box, image, conf=1, gray=False):
	try:
		if pyautogui.locateOnScreen(image, region=(max(0,box[0]),box[1],box[2],box[3]), confidence=conf) != None:
			loc = pyautogui.locateOnScreen(image, region=(box[0],box[1],box[2],box[3]), confidence=conf, grayscale=gray)
			return loc
		return False
	except:
		return False

def center(pos):
	dot = [
		pos.left + int(pos.width/2),
		pos.top + int(pos.height/2)
		]
	return dot

def click(x, y):
	mousePos = pyautogui.position()
	win32api.SetCursorPos((x, y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
	time.sleep(0.02)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
	win32api.SetCursorPos((mousePos.x, mousePos.y))

def cutTree(tree, pos):
	click(pos[0], pos[1])
	area = [
		pos[0] - int(gameSize[0]/6),	#select area where confirmation box may appear
		pos[1] - int(gameSize[1]/6),	#Based on size of game screen
		pos[0] + int(gameSize[0]/6),
		pos[1] + int(gameSize[1]/6),
		]
	
	time.sleep(0.4 + random.randint(0,700)/1000)
	cutBox = locateItem(area,'{}/cutBox.PNG'.format(tree), 0.8)
	if cutBox:
		print(cutBox)
		click(cutBox.left + int(cutBox.width/2), cutBox.top + int(3*cutBox.height/4))
		time.sleep(2)

		return True
	return cutBox

def searchTrees(treeList, sample=limits):
	for t in treeList:
		db = os.listdir('{}/.'.format(t))
		db.remove('cutBox.PNG')
		match = 0
		for pic in db:
			link = '{}/{}'.format(t, pic)
			tree = locateItem(sample, link, conf=0.7)
			if tree:
				match += 1
				if match == 2:
					return t, tree
	return False

def searchExit(dir=0):
	direction = [[0,130,1150,790], [0,130,900,790], [0,130,1150,540], [250,130,1150,790], [0,580,1150,790]]
	db = os.listdir('exits/.')
	match = 0
	for pic in db:
		link = 'exits/{}'.format(pic)
		exit = locateItem(direction[dir], link, conf=0.8, gray=True)
		if exit:
			match += 1
			if match == 2:
				return exit
	return False

def getDirection(exit):
	direction = [0,0]
	if exit[0] < 150:
		direction = [-1,0]
	elif exit[0] > 1000:
		direction = [1,0]
	elif exit[1] < 280:
		direction = [0,-1]
	elif exit[1] > 640:
		direction = [0,1]
	return direction



while True:
	item = searchTrees(['Oak','Ash', 'Chestnut', 'Walnut'])	#items you are looking for
	if item:	#if something found and we assume the character is not busy

		name = item[0]	#gets name of item for file reference
		position = item[1]	#store position and size info on item
		itemCenter = center(position)	#tries to locate center of item
		print('maybe')

		treeArea = [
			itemCenter[0] - int(6*position.width/10),
			itemCenter[1] - int(6*position.height/10),
			itemCenter[0] + int(6*position.width/10),
			itemCenter[1] + int(6*position.height/10)
			]
		dbCheck = searchTrees([name], treeArea)
		cutTime = time.time() + 15
		if dbCheck and cutTime > time.time():
			cutting = cutTree(name, itemCenter)
			print('Trying to cut a {} at [{}:{}]'.format(name, itemCenter[0],itemCenter[1]))
			while dbCheck:
				dbCheck = searchTrees([name], treeArea)
				print('waiting to stop cutting')


		#if cutting:
		#	cutTime = time.time() + random.randint(100,278)/100 + 11
		#else:
		#	cutTime = time.time() + random.randint(100,400)/100 + 2 


	else:
		print('Nothing Found')
		time.sleep(0.3)
		
	
