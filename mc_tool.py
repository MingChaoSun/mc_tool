import os, sys
import time

import numpy as np

from PIL import Image,ImageDraw
import matplotlib.pyplot as plt

#dir:
#
#dir_namerule(root,pre,namerange,range_formate,ed)
#dir(root,type,addroot[True/False]])
#pathtrans(path_list,rule,type["str"/"int"])

#For free
draw_list = []

#Dir all files from directory by name rule
def dir_namerule(root,pre,namerange,range_formate,ed):

	filelist = []

	formate = "%0" + str(range_formate) + "d"

	for i in namerange:

		filelist.append(root + pre + formate % i + ed)

	return filelist

#Dir all files from directory
def dir(root,type = 'f',addroot = True):

    dirList = []
    
    fileList = []  

    files = os.listdir(root)  

    for f in files:

        if(os.path.isdir(root + f)):  
             
            if addroot == True:
            
            	dirList.append(root + f)

            else:

            	dirList.append(f)


        if(os.path.isfile(root + f)):  
          
            if addroot == True:
            
            	fileList.append(root + f)

            else:

            	fileList.append(f)

    if type == "f":

    	return fileList

    elif type == "d":

    	return dirList

    else:

    	print "ERROR: TMC.dir(root,type) type must be [f] for file or [d] for dir"

    	return 0

#Trans path by type
def pathtrans(path_list,rule,type = "str"):

	list_trans = []

	temp = ""

	for p in path_list:

		temp = p

		for r in rule:

			p = p.split(r[0])[r[1]]

		if type == "str":

			list_trans.append(p)

		elif type == "int":

			list_trans.append(int(p))


	return list_trans

def readfile(file_path,split = ",",firstline = 0,withhead = False,head = "default",emptyflag = 0):

	data = {}

	headlist = []

	index = 0

	#get head
	with open(file_path, "r") as f:

		lines = f.readlines()

		if len(lines) == 0:

			print "WARNING: TMC.readfile(file_path,split,firstline,withhead,head) EMPTY FILE , emptyflag is ",emptyflag

			return emptyflag

		else :
		
			line_f_s = lines[firstline].strip().split(split)

			if head == "default":

				headlist.append("line_num")

				for h in range(len(line_f_s)):

					headlist.append("col_" + str(h))

			elif head == "firstline":

				headlist.append("line_num")

				firstline = firstline + 1

				for h in line_f_s:

					headlist.append(str(h))

			elif type(head) is list:

				for h in line_f_s:

					headlist.append("col_$_discard")

				for h in head:

					headlist[h[1] + 1] = h[0]

				headlist.append("line_num")

			else:

				print "ERROR: TMC.readfile(file_path,split,firstline,withhead,head) head must be [default] or [firstline] or a list"

			for k,h in enumerate(headlist):

				if h != "col_$_discard":

					data[h] = []



			#read file
			for line in lines:

				if index >= firstline:

					line_s = line.strip().split(split)

					for k,h in enumerate(headlist):

						if h == "line_num":

							data[h].append(index)

						elif h != "col_$_discard":

							data[h].append(line_s[k-1])

				index = index + 1

		return data

def tofile(file_path,data,split = ",",firstline = 0,withhead = False):

	if os.path.exists(file_path):

		print "WARNING: TMC.tofile(file_path,data,split,firstline,withhead) File is already exist"

		file_path = file_path + ".new"

	with open(file_path, "w") as f:

		if withhead == True:

			for i,(k,v) in enumerate(data.items()):

				if i == 0:

					f.writelines(k)

					rows = len(v)

				else:

					f.writelines(split + k)

			f.writelines("\n")


		for r in range(rows):

			for i,(k,v) in enumerate(data.items()):

				if i == 0:

					f.writelines(str(v[r]))

				else:

					f.writelines(split + str(v[r]))

			f.writelines("\n")


def PILImage(file_img):

	img = Image.open(file_img)

	draw = ImageDraw.Draw(img)

	draw_list.append(draw)

	return img,draw

def PILImage_drawbox(draw,box,color=(0,255,0),label="NULL",labelcolor = "default"):

	box_d = []

	#x1y1
	box_d.append(float(box[0]))
	box_d.append(float(box[1]))

	#x2y1
	box_d.append(float(box[2]))
	box_d.append(float(box[1]))

	#x2y2
	box_d.append(float(box[2]))
	box_d.append(float(box[3]))

	#x1y2
	box_d.append(float(box[0]))
	box_d.append(float(box[3]))

	#x1y1
	box_d.append(float(box[0]))
	box_d.append(float(box[1]))

	if labelcolor == "default":

		labelcolor = color

	if label == "NULL":

		draw.line(box_d,fill=color,width=2)

	else:

		draw.line((box_d[0] - 1, box_d[1] - 8,box_d[0] + 6*len(label) + 2, box_d[1] - 8 ),fill=labelcolor,width=15)

		draw.text((box_d[0] + 1, box_d[1] - 12),label)

		draw.line(box_d,fill=color,width=2)

def color(name):

	if name == "red":

		return (255,0,0)

	if name == "green":

		return (0,255,0)

	if name == "blue":

		return (0,0,255)

	if name == "lightblue":

		return (85,200,240)

	if name == "blackishgreen":

		return (50,120,0)

	if name == "purple":

		return (255,0,255)

	if name == "deeppurple":

		return (110,40,125)

	if name == "lightpurple":

		return (210,35,255)

	if name == "orange":

		return (255,65,20)


def free():

	for d in draw_list:

		del d

#x1,y1,x2,y2 To left,right,top,bottom
def boxtoboundary(box):

	left = box[0]
	right = box[2]
	top = box[1]
	bottom = box[3]

	return left,right,top,bottom

#compute iou for two boxes
def iou(box_i,box_j):

	left_i,right_i,top_i,bottom_i = boxtoboundary(box_i)

	left_j,right_j,top_j,bottom_j = boxtoboundary(box_j)

	area_i = (right_i - left_i)*(bottom_i - top_i)

	area_j = (right_j - left_j)*(bottom_j - top_j)

	left_overlap = max(left_i,left_j)
	right_overlap = min(right_i,right_j)
	top_overlap = max(top_i,top_j)
	bottom_overlap = min(bottom_i,bottom_j)

	if right_overlap - left_overlap > 0 and bottom_overlap - top_overlap > 0:

		area_overlap = (right_overlap - left_overlap)*(bottom_overlap - top_overlap)
		area_union = area_i + area_j - area_overlap
		
		iou = area_overlap/area_union

		return iou

	else:

		return 0


