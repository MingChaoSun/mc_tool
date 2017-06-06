import mc_tool as mct

#Define Path
path_img = "../depthimg/image_2/"
path_label = "../depthimg/label_2/"
path_evaluation = "./val_with_KITTI_newCover_v1_60000_evaluation_0.1/"

img_w = 1242
img_h = 375

#Read Files
path_result = path_evaluation + "result/"
path_evaluation = path_evaluation + "data/"

filelist_evaluation = mct.dir(path_evaluation,type = 'f',addroot = True)

process_list = mct.pathtrans(filelist_evaluation,[("/",-1),(".",0)],type = "int")

filelist_img = mct.dir_namerule(path_img,"",process_list,6,".png")
filelist_label = mct.dir_namerule(path_label,"",process_list,6,".txt")
filelist_result = mct.dir_namerule(path_result,"",process_list,6,".png")

for i in range(len(process_list)):

	print "process:",process_list[i]
	print "evaluation_file:",filelist_evaluation[i]
	print "image_source:",filelist_img[i]
	print "label_source:",filelist_label[i]
	print "image_output:",filelist_result[i]

	#Read Source File To DataFrea
	img_s,draw_s = mct.PILImage(filelist_img[i])

	label = mct.readfile(filelist_label[i],split=" ",head = [("type",0),("x1",4),("y1",5),("x2",6),("y2",7)])
	evaluation = mct.readfile(filelist_evaluation[i],split=" ",head = [("type",0),("x1",4),("y1",5),("x2",6),("y2",7),("confidence",-1)])

	#Analysis Boxes

	box_l = []
	box_e = []

	GT_good = []
	Predict_good = []

	GT_highiou = []
	Predict_highiou = []

	#Case1 iou(label,evaluation) > 0.7
	for k_l,v_l in enumerate(label["line_num"]):

		if label["type"][k_l] == "Car" or label["type"][k_l] == "Van":

			box_l = [float(label["x1"][k_l]),float(label["y1"][k_l]),float(label["x2"][k_l]),float(label["y2"][k_l])]

		if evaluation != 0 and len(box_l) > 0:

			for k_e,v_e in enumerate(evaluation["line_num"]):

				box_e = [float(evaluation["x1"][k_e]),float(evaluation["y1"][k_e]),float(evaluation["x2"][k_e]),float(evaluation["y2"][k_e])]
				
				if mct.iou(box_l,box_e) - 0.7 > 0.0001:

					GT_good.append(k_l)
					Predict_good.append(k_e)

				if mct.iou(box_l,box_e) - 0.5 > 0.0001:

					GT_highiou.append(k_l)
					Predict_highiou.append(k_e)

	#Draw Boxes 
	for k,v in enumerate(label["line_num"]):

		if label["type"][k] == "Car" or label["type"][k] == "Van":

			if k in GT_good:

				mct.PILImage_drawbox(draw_s,[label["x1"][k],label["y1"][k],label["x2"][k],label["y2"][k]],color=mct.color("green"),label="GT" + label["type"][k],labelcolor=mct.color("blackishgreen"))

			elif k in GT_highiou:

				mct.PILImage_drawbox(draw_s,[label["x1"][k],label["y1"][k],label["x2"][k],label["y2"][k]],color=mct.color("green"),label="IOUGT" + label["type"][k],labelcolor=mct.color("blackishgreen"))

			else:

				mct.PILImage_drawbox(draw_s,[label["x1"][k],label["y1"][k],label["x2"][k],label["y2"][k]],color=mct.color("red"),label="BadGT" + label["type"][k])

	if evaluation != 0:

		for k,v in enumerate(evaluation["line_num"]):

			if k in Predict_good:

				mct.PILImage_drawbox(draw_s,[evaluation["x1"][k],evaluation["y1"][k],evaluation["x2"][k],evaluation["y2"][k]],color=mct.color("lightblue"),label=("%.4f" % float(evaluation["confidence"][k])))
	
			elif k in Predict_highiou:

				mct.PILImage_drawbox(draw_s,[evaluation["x1"][k],evaluation["y1"][k],evaluation["x2"][k],evaluation["y2"][k]],color=mct.color("orange"),label=("%.4f" % float(evaluation["confidence"][k])))

			else:

				mct.PILImage_drawbox(draw_s,[evaluation["x1"][k],evaluation["y1"][k],evaluation["x2"][k],evaluation["y2"][k]],color=mct.color("lightpurple"),label=("%.4f" % float(evaluation["confidence"][k])),labelcolor=mct.color("deeppurple"))

	#Save Result
	img_s.save(filelist_result[i])

	mct.free()

print "ALL DONE"
