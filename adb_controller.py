import os
import time
import re
import cv2

import settings
import image_processor

def test():
	# process = os.system("adb -s 127.0.0.1:62028 shell pm list packages")
	process = os.system("adb -s 127.0.0.1:62028 shell input swipe 1200 340 1200 181 2000")
	# process = os.system("adb -s 127.0.0.1:62028 shell input tap 1200 340")
	# process = os.system("adb -s 127.0.0.1:62028 shell input tap 30 30")

def check_internet_lag():
	lag_timer = 1
	while 1:
		if lag_timer >= 1.5:
			lag_timer = 1.5
		if not wait_till_match_any([r"template_images\internet_lag.png"],[0.4],True,lag_timer,0,log = False,scope=([625,710,600,690])):
			break
		else:
			print("Internet lag detected!!!")
			time.sleep(1)
			lag_timer +=1
			continue

def swipe(from_loc,to_loc,use_time):
	print("AdbController:Swipe from "+str(from_loc)+" to "+str(to_loc)+" by "+str(use_time)+" millisecond")
	process = os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" shell input swipe "
		+str(from_loc[0])+" "+str(from_loc[1])+" "+str(to_loc[0])+" "+str(to_loc[1])+" "+str(use_time))
	time.sleep(use_time/1000)
	time.sleep(2)

def stop_app():
	
	os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" shell am force-stop "+settings.package_name)
	
	time.sleep(1)

last_click_loc = None

def click(location,chk_net = True):
	
	print("AdbController: Tap "+str(location[0])+" "+str(location[1]))
	
	last_click_loc = location
	
	os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" shell input tap "+str(location[0])+" "+str(location[1]))
	# while wait_till_match_any([r"template_images\internet_lag.png"],[0.1],True,3,0,settings.accidents):
	# 	continue
	if chk_net == True:
		check_internet_lag()
	# time.sleep(0.5)

def screenshot(path):
	os.system("\""+settings.adb_path+"\""+" -s "+settings.device_address+" exec-out screencap -p > " + path)
	time.sleep(0.5)

def check_if_accidents(accidents , log=False):
	if log == True:
		print("AdbController:Check if any accidents : "+str(accidents["paths"]))
	
	for index in range(0,len(accidents["paths"])):
		match_loc = image_processor.match_template(
			settings.screenshot_path,accidents["paths"][index],accidents["thresholds"][index],True,print_debug = False)
		
		if(match_loc != None):
			if log == True:
				print("AdbController: Accidents "+str(accidents["paths"][index]+" occur, and now should "+accidents["methods"][index]))
			
			if(accidents["click_offset"][index] != None):
				match_loc = (match_loc[0] + accidents["click_offset"][index][0],match_loc[1] + accidents["click_offset"][index][1])
				time.sleep(5)
			if(accidents["methods"][index] == "click"):
				click(match_loc)
				return accidents["methods"][index]
				time.sleep(5)
			if(accidents["methods"][index] == "restart"):
				return accidents["methods"][index]
				time.sleep(5)
			print("Unkonw method")
			
			return "restart"
			time.sleep(5)
	if log == True:
		print("AdbController: No Accident")

def wait_till_match_any(template_paths,thresholds,return_center,max_time,step_time,accidents=None,scope = None,except_locs = None ,log = True):
	if log == True:
		print("AdbController: Start to wait till match screenshot by any "+str(template_paths)+" for up to "+str(max_time)+" seconds  ....")
	time_start = time.time()
	match_loc = None

	while(True):
		screenshot(settings.screenshot_path)
		for index in range(0,len(template_paths)):
			match_loc = image_processor.match_template(
				settings.screenshot_path,template_paths[index],thresholds[index],return_center,scope = scope,except_locs = except_locs,print_debug=log)
			if(match_loc != None):
				return match_loc
		if(time.time() - time_start > max_time):
			if log == True:
				print("AdbController: Reach max_time but failed to match")
			return None
		if(accidents != None):
			re = check_if_accidents(accidents)
			if(re == "restart"):return "restart"
		time.sleep(step_time)

	return None

#any
def wait_to_match_and_click(
	template_paths,thresholds,return_center,max_time,step_time,accidents = None,click_offset = None,scope = None,except_locs = None
	, chk_net = True):
	re = wait_till_match_any(template_paths,thresholds,return_center,max_time,step_time,accidents,scope = scope,except_locs = except_locs)
	if(re == "restart"):
		return "restart"
	if(re == None):
		print("Cannot find "+str(template_paths))
		return "failed"
	if(click_offset != None):
		re = (re[0]+click_offset[0],re[1]+click_offset[1])
	click(re)
	if chk_net == True:
		check_internet_lag()
	return "success"

#match any
def wait_while_match(template_paths,thresholds,max_time,step_time,accidents = None,scope = None,except_locs = None):
	print("Start to wait while match screenshot by "+str(template_paths)+" for up to "+str(max_time)+" seconds  ....")
	time_start = time.time()
	while(True):
		screenshot(settings.screenshot_path)
		for i in range(0,len(template_paths)):
			match_loc = image_processor.match_template(
				settings.screenshot_path,template_paths[i],thresholds[i],True,scope = scope,except_locs=except_locs)
			if(match_loc != None):
				break
		if(match_loc == None or time.time() - time_start > max_time):
			return "over wait"
		if(accidents != None):
			re = check_if_accidents(accidents)
			if(re == "restart"):
				return "restart"
		time.sleep(step_time)


def wait_till_match_any_text(aim_texts = [],max_time = 1,step_time = 1,scope = None):
	print("AdbController: Start to wait till match screenshot by any text"+str(aim_texts)+" for up to "+str(max_time)+" seconds  ....")
	time_start = time.time()
	match_loc = None

	while(True):
		screenshot(settings.screenshot_path)
		result = image_processor.easyocr_read(settings.screenshot_path, True, scope)
		for reline in result:
			re_text = reline[1].replace(" ","")
			for aim_text in aim_texts:
				k = re.findall(aim_text,re_text)
				if(len(k)>0):
					return reline
		if(time.time() - time_start > max_time):
			print("AdbController: Reach max_time but failed to match")
			return None
		time.sleep(step_time)


def wait_till_match_any_text_and_click(aim_texts = [],max_time = 1,step_time = 1,scope = None, chk_net = True):
	print("AdbController: Start to wait till match screenshot by any text"+str(aim_texts)+" for up to "+str(max_time)+" seconds  ....")
	time_start = time.time()
	match_loc = None

	while(True):
		screenshot(settings.screenshot_path)
		result = image_processor.easyocr_read(settings.screenshot_path,True,scope)
		matched_result = []
		for reline in result:
			re_text = reline[1].replace(" ","")
			for aim_text in aim_texts:
				print("aim text is :" + str(aim_text) + " and re text is " + str(re_text) )
				k = re.findall(aim_text,re_text)
				if(len(k)>0):
					matched_result.append(reline)
				# 	print("MATCHED! " + str(reline))
				# print("k < 0")
		for i in matched_result:
			print("found targeted text , clicking : "+ str(i[0][0]))
			click([i[0][0][0]+scope[2], i[0][0][1]+scope[0]]) #normalizing the crop
			# click(i[0][0])
		if chk_net == True:
			check_internet_lag()
		return matched_result
		if(time.time() - time_start > max_time):
			print("AdbController: Reach max_time but failed to match")
			return None
		time.sleep(step_time)


