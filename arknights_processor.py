import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import pubManager
import time
import re
import cv2
import random
import ctypes

import settings
import image_processor
import adb_controller

'''
version 1
hiring_priority_list =  [["重装干员", "生存"], ["生存", "防护"], ["输出", "防护"], ["辅助干员", "削弱"], ["术士干员", "减速", "输出"], ["特种干员", "生存"], ["辅助干员", "输出"], ["术士干员", "治疗"], ["医疗干员", "支援"], ["资深干员"], ["召唤"], ["控场"], ["爆发"], ["位移", "防护"], ["位移", "减速"], ["位移", "输出"], ["特种干员", "生存"], ["特种干员", "减速"], ["特种干员", "输出"], ["削弱", "群攻"], ["削弱", "特种干员"], ["削弱", "近战位"], ["削弱", "快速复活"], ["支援", "费用回复"], ["支援", "治疗"],["近卫干员", "防护"], ["治疗", "输出"], ["治疗", "减速"], ["支援", "输出"], ["快速复活"], ["特种干员"], ["削弱"], ["支援"], ["先锋干员", "治疗"],  ["近卫干员", "支援"], ["近卫干员", "减速"], ["狙击干员", "削弱"], ["狙击干员", "生存"], ["狙击干员", "减速"],  ["重装干员", "位移"], ["术士干员", "减速"], ["术士干员", "削弱"], ["近战位", "减速"], ["远程位", "生存"], ["远程位", "支援"],  ["治疗", "费用回复"], ["输出", "减速"], ["群攻", "减速"], ["位移"], ["支援"], ["削弱"], ["机械支援"]]
'''
#version 2


# hiring_priority_list =  [["重装干员", "生存"], ["生存", "防护"], ["输出", "防护"], ["辅助干员", "削弱"], ["术师干员", "减速", "输出"], ["特种干员", "生存"], ["辅助干员", "输出"], ["术师干员", "治疗"],  ["资深干员"], ["召唤"], ["控场"], ["爆发"], ["位移", "防护"], ["位移", "减速"], ["位移", "输出"], ["特种干员", "生存"], ["特种干员", "减速"], ["特种干员", "输出"], ["削弱", "群攻"], ["削弱", "特种干员"], ["削弱", "近战位"], ["削弱", "快速复活"], ["支援", "费用回复"], ["近卫干员", "防护"], ["治疗", "输出"], ["治疗", "减速"],["重装干员", "位移"],  ["支援", "输出"], ["支援", "治疗"],["医疗干员", "支援"],["快速复活"], ["特种干员"], ["削弱"], ["支援"], ["先锋干员", "治疗"],  ["近卫干员", "支援"], ["近卫干员", "减速"], ["狙击干员", "削弱"], ["狙击干员", "生存"], ["狙击干员", "减速"],  ["术师干员", "减速"], ["术师干员", "削弱"], ["近战位", "减速"], ["远程位", "生存"], ["远程位", "支援"],  ["治疗", "费用回复"], ["输出", "减速"], ["群攻", "减速"], ["位移"], ["支援"], ["削弱"]]



#spliting list into two lists and append later to avoid 3.8 UTF 8 length bug with Non UTF 8 error.

hiring_priority_list = [['控场'], ['爆发'], ['召唤'], ['近卫干员', '防护'], ['狙击干员', '爆发'], ['重装干员', '输出'], ['重装干员', '生存'], ['重装干员', '位移'], ['辅助干员', '控场'], ['辅助干员', '输出'], ['辅助干员', '削弱'], ['辅助干员', '召唤'], ['术师干员', '治疗'], ['特种干员', '控场'], ['特种干员', '输出'], ['特种干员', '生存'], ['特种干员', '减速'], ['特种干员', '削弱'], ['先锋干员', '控场'], ['先锋干员', '支援'], ['近战位', '控场'], ['近战位', '削弱'], ['远程位', '控场'], ['远程位', '爆发'], ['远程位', '召唤'], ['控场', '费用回复'], ['控场', '减速'], ['控场', '快速复活'], ['控场', '召唤'], ['爆发', '输出'], ['治疗', '输出'], ['治疗', '减速'], ['支援', '费用回复'], ['输出', '防护'], ['输出', '位移'], ['生存', '防护'], ['群攻', '削弱'], ['防护', '位移'], ['减速', '位移'], ['削弱', '快速复活'], ['近卫干员', '近战位', '防护'], ['近卫干员', '输出', '防护'], ['狙击干员', '远程位', '爆发'], ['狙击干员', '爆发', '输出'], ['狙击干员', '群攻', '削弱'], ['重装干员', '近战位', '输出'], ['重装干员', '近战位', '生存'], ['重装干员', '近战位', '位移'], ['重装干员', '输出', '生存'], ['重装干员', '输出', '防护'], ['重装干员', '生存', '防护'], ['重装干员', '防护', '位移'], ['辅助干员', '远程位', '控场'], ['辅助干员', '远程位', '输出'], ['辅助干员', '远程位', '削弱'], ['辅助干员', '远程位', '召唤'], ['辅助干员', '控场', '减速'], ['辅助干员', '控场', '召唤'], ['辅助干员', '输出', '减速'], ['术师干员', '远程位', '治疗'], ['术师干员', '治疗', '输出'], ['术师干员', '治疗', '减速'], ['术师干员', '输出', '减速']]

hiring_priority_list += ['特种干员', '近战位', '控场'], ['特种干员', '近战位', '输出'], ['特种干员', '近战位', '生存'], ['特种干员', '近战位', '减速'], ['特种干员', '近战位', '削弱'], ['特种干员', '控场', '快速复活'], ['特种干员', '输出', '生存'], ['特种干员', '输出', '位移'], ['特种干员', '减速', '位移'], ['特种干员', '削弱', '快速复活'], ['先锋干员', '近战位', '控场'], ['先锋干员', '近战位', '支援'], ['先锋干员', '控场', '费用回复'], ['先锋干员', '支援', '费用回复'], ['近战位', '控场', '费用回复'], ['近战位', '控场', '快速复活'], ['近战位', '支援', '费用回复'], ['近战位', '输出', '防护'], ['近战位', '输出', '位移'], ['近战位', '生存', '防护'], ['近战位', '防护', '位移'], ['近战位', '减速', '位移'], ['近战位', '削弱', '快速复活'], ['远程位', '控场', '减速'], ['远程位', '控场', '召唤'], ['远程位', '爆发', '输出'], ['远程位', '治疗', '输出'], ['远程位', '治疗', '减速'], ['远程位', '群攻', '削弱'], ['治疗', '输出', '减速'], ['输出', '生存', '防护'], ['特种干员'], ['支援'], ['削弱'], ['快速复活'], ['位移'], ['近卫干员', '支援'], ['近卫干员', '减速'], ['狙击干员', '生存'], ['狙击干员', '减速'], ['狙击干员', '削弱'], ['医疗干员', '支援'], ['术师干员', '减速'], ['术师干员', '削弱'], ['特种干员', '近战位'], ['特种干员', '防护'], ['特种干员', '快速复活'], ['特种干员', '位移'], ['先锋干员', '治疗'], ['近战位', '支援'], ['近战位', '减速'], ['近战位', '快速复活'], ['近战位', '位移'], ['远程位', '支援'], ['远程位', '生存'], ['远程位', '削弱'], ['治疗', '支援'], ['治疗', '费用回复'], ['支援', '输出'], ['输出', '减速'], ['输出', '削弱'], ['群攻', '减速'], ['防护', '快速复活'], ['近卫干员', '近战位', '支援'], ['近卫干员', '近战位', '减速'], ['近卫干员', '支援', '输出'], ['近卫干员', '输出', '减速'], ['狙击干员', '远程位', '生存'], ['狙击干员', '远程位', '减速'], ['狙击干员', '远程位', '削弱'], ['狙击干员', '输出', '生存'], ['狙击干员', '输出', '减速'], ['狙击干员', '输出', '削弱'], ['狙击干员', '群攻', '减速'], ['医疗干员', '远程位', '支援'], ['医疗干员', '治疗', '支援'], ['术师干员', '远程位', '减速'], ['术师干员', '远程位', '削弱'], ['术师干员', '输出', '削弱'], ['术师干员', '群攻', '减速'], ['特种干员', '近战位', '防护'], ['特种干员', '近战位', '快速复活'], ['特种干员', '近战位', '位移'], ['特种干员', '防护', '快速复活'], ['先锋干员', '近战位', '治疗'], ['先锋干员', '治疗', '费用回复'], ['近战位', '治疗', '费用回复'], ['近战位', '支援', '输出'], ['近战位', '输出', '减速'], ['近战位', '防护', '快速复活'], ['远程位', '治疗', '支援'], ['远程位', '输出', '生存'], ['远程位', '输出', '减速'], ['远程位', '输出', '削弱'], ['远程位', '群攻', '减速']

# hiring_priority_list2 =[['重装干员', '生存'], ['控场'], ['爆发'], ['召唤'], ['近卫干员', '防护'], ['狙击干员', '爆发'], ['重装干员', '输出'],  ['重装干员', '位移'], ['辅助干员', '控场'], ['辅助干员', '输出'], ['辅助干员', '削弱'], ['辅助干员', '召唤'], ['特种干员', '控场'], ['特种干员', '输出'], ['特种干员', '生存'], ['特种干员', '减速'], ['特种干员', '削弱'], ['先锋干员', '控场'], ['先锋干员', '支援'], ['近战位', '控场'], ['近战位', '削弱'], ['远程位', '控场'], ['远程位', '爆发'], ['远程位', '召唤'], ['控场', '费用回复'], ['控场', '减速'], ['控场', '快速复活'], ['控场', '召唤'], ['爆发', '输出'], ['支援', '费用回复'], ['输出', '防护'], ['输出', '位移'], ['生存', '防护'], ['群攻', '削弱'], ['防护', '位移'], ['减速', '位移'], ['削弱', '快速复活'], ['近卫干员', '近战位', '防护'], ['近卫干员', '输出', '防护'], ['狙击干员', '远程位', '爆发'], ['狙击干员', '爆发', '输出'], ['狙击干员', '群攻', '削弱'], ['重装干员', '近战位', '输出'], ['重装干员', '近战位', '生存'], ['重装干员', '近战位', '位移'], ['重装干员', '输出', '生存'], ['重装干员', '输出', '防护'], ['重装干员', '生存', '防护'], ['重装干员', '防护', '位移'], ['辅助干员', '远程位', '控场'], ['辅助干员', '远程位', '输出']]

# hiring_priority_list2 += [['辅助干员', '远程位', '削弱'], ['辅助干员', '远程位', '召唤'], ['辅助干员', '控场', '减速'], ['辅助干员', '控场', '召唤'], ['辅助干员', '输出', '减速'], ['特种干员', '近战位', '控场'], ['特种干员', '近战位', '输出'], ['特种干员', '近战位', '生存'], ['特种干员', '近战位', '减速'], ['特种干员', '近战位', '削弱'], ['特种干员', '控场', '快速复活'], ['特种干员', '输出', '生存'], ['特种干员', '输出', '位移'], ['特种干员', '减速', '位移'], ['特种干员', '削弱', '快速复活'], ['先锋干员', '近战位', '控场'], ['先锋干员', '近战位', '支援'], ['先锋干员', '控场', '费用回复'], ['先锋干员', '支援', '费用回复'], ['近战位', '控场', '费用回复'], ['近战位', '控场', '快速复活'], ['近战位', '支援', '费用回复'], ['近战位', '输出', '防护'], ['近战位', '输出', '位移'], ['近战位', '生存', '防护'], ['近战位', '防护', '位移'], ['近战位', '减速', '位移'], ['近战位', '削弱', '快速复活'], ['远程位', '控场', '减速'], ['远程位', '控场', '召唤'], ['远程位', '爆发', '输出'], ['远程位', '群攻', '削弱'], ['输出', '生存', '防护'], ['特种干员'], ['支援'], ['削弱'], ['快速复活'], ['位移'], ['近卫干员', '支援'], ['近卫干员', '减速'], ['狙击干员', '生存'], ['狙击干员', '群攻'], ['狙击干员', '减速'], ['狙击干员', '削弱'], ['医疗干员', '支援'], ['术师干员', '减速']]

less_priority_list = [["减速"], ["生存"], ["防护"], ["费用回复"], ["治疗"], ["输出"],["群攻"]]

def stop_app():
	print("ArknightsController:Stop the App  ....")
	adb_controller.stop_app()

def start_app():
	print("ArknightsController:Start the App  ....")
	re = adb_controller.wait_to_match_and_click([r"template_images\start0.png"],[0.3],True,60,2)
	if(re == "restart"):return re

	print("ArknightsController:Wait to click Yellow Start Button  ....")
	time.sleep(5)
	re = adb_controller.wait_to_match_and_click([r"template_images\start1.png"],[0.15],True,300,1.123)
	if(re == "restart"):return re

	print("ArknightsController:Wait to click Start Wake Button  ....")
	time.sleep(5)
	re = adb_controller.wait_to_match_and_click([r"template_images\start2.png"],[0.1],True,30,1.123)
	if(re == "restart"):return re

	print("ArknightsController:Wait to get in Main Page  ....")
	re = adb_controller.wait_till_match_any([r"template_images\level0.png"],[0.1],True,60,3,settings.accidents)
	if(re == "restart"):return re


def restart_app():
	print("ArknightsController:Start to Restart  ....")
	stop_app()
	start_app()

def start_app():
	print("ArknightsController:Start arknight  ....")
	start_app()

def go_level():
	
	print("ArknightsController:Start to run Level  ....")

	#get to the level
	re  = adb_controller.wait_to_match_and_click([r"template_images\level0.png"],[0.1],True,20,1,settings.accidents)
	if(re == "restart"):return re

	success_in_t_level = False
	last_t_level_image = ""
	if(len(settings.auto_t_level) > 0):#temp level
		for temp_image in settings.auto_t_level :
			last_t_level_image = temp_image
			re = adb_controller.wait_to_match_and_click([temp_image],[0.1],True,30,1)
			re = adb_controller.wait_to_match_and_click([temp_image],[0.1],True,5,1)
			if(re == "success"):
				success_in_t_level = True
			else:
				success_in_t_level = False

	if(success_in_t_level == False):#temp failed

		re = adb_controller.wait_to_match_and_click(
					[r"template_images\level1.png"
					,r"template_images\level1_2.png"],[0.1,0.1],True,20,1)
		if(re == "restart"):return re

		re = adb_controller.wait_to_match_and_click([r"template_images\level2_ce.png"],[0.1],True,10,1)
		if(re == "success"):#Can Make Money, go ce level
			re = adb_controller.wait_to_match_and_click(
				[r"template_images\level3_ce{}.png".format(settings.auto_ce_level)],[0.1],True,5,1)
			if(re == "restart"):
				return re
			if(re == "failed"):
				adb_controller.swipe((800,400),(400,400),1000)
				time.sleep(1)
				re = adb_controller.wait_to_match_and_click(
					[r"template_images\level3_ce{}.png".format(settings.auto_ce_level)],[0.1],True,10,1)
				if(re == "failed"):
					print("ERROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOR")
					print("ArknightsController:Can not match " 
						+ r"template_images\level3_ce{}.png".format(settings.auto_ce_level))
		else: #Can only make exp,go ls level
			re = adb_controller.wait_to_match_and_click(
				[r"template_images\level2_ls.png"],[0.1],True,20,1)
			if(re == "restart"):return re
			re = adb_controller.wait_to_match_and_click(
				[r"template_images\level3_ls{}.png".format(settings.auto_ls_level)],[0.1],True,20,1)
			if(re == "failed"):
				adb_controller.swipe((800,400),(400,400),1000)
				time.sleep(1)
				re = adb_controller.wait_to_match_and_click(
					[r"template_images\level3_ls{}.png".format(settings.auto_ls_level)],[0.1],True,20,1)
				if(re == "failed"):
					print("ERROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOR")
					print("ArknightsController:Can not match " 
						+ r"template_images\level3_ce{}.png".format(settings.auto_ce_level))

	#repeat the level
	while(True):
		re = adb_controller.wait_to_match_and_click([r"template_images\level8.png"],[0.02],True,6,2)
		if(re == "restart"):return re

		if(success_in_t_level == False):
			re = adb_controller.wait_to_match_and_click([r"template_images\level4.png"],[0.01],True,20,2)
			if(re == "restart"):return re
		else:
			re = adb_controller.wait_to_match_and_click([last_t_level_image],[0.01],True,30,2)
			if(re == "restart"):return re
		
		re = adb_controller.wait_to_match_and_click([r"template_images\level5.png"],[0.01],True,20,2,settings.accidents)
		if(re == "restart"):return re
		if(re == "failed"):return re
		re = adb_controller.wait_till_match_any([r"template_images\level6.png"],[0.01],True,20,1)
		if(re == "restart"):return re
		re = adb_controller.wait_while_match([r"template_images\level6.png"],[0.01],600,10)
		if(re == "restart"):return re

		time.sleep(5)
		re = adb_controller.wait_to_match_and_click([r"template_images\level7.png",r"template_images\level7-2.png"]
			,[0.2,0.2],True,600,2,settings.accidents,click_offset=[300,-300])
		if(re == "failed" or re == "restart"):return "restart"
		re = adb_controller.wait_to_match_and_click([r"template_images\level7.png"],[0.2],True,10,2,settings.accidents)

	print("ArknightsController:Finished go level  ....")	
	return "success"

crew_rects={
	"up_left_loc":[(417,96),(417,360),(561,96),(561,360)
				,(705,96),(705,360),(849,96),(849,360)
				,(993,96),(993,360),(1137,96),(1137,360)]
	,"witdth":123
	,"height":257
}

def go_infrastructure():

		
	print("ArknightsController:Start to run Infrastructure  ....")
	#get in the Infrastructure
	re  = adb_controller.wait_to_match_and_click([r"template_images\infrastructure1.png"],[0.1],True,6,1,settings.accidents)
	if(re == "restart"):return re
	time.sleep(5)
	adb_controller.click([1,1])
	re = adb_controller.wait_till_match_any([r"template_images\infrastructure2.png"],[0.1],True,6,1)
	if(re == "restart"):return re

	print("ArknightsController:Start to Collect Goods  ....")
	#new logic
	time.sleep(2)
	# adb_controller.swipe((400,400),(800,400),2000)
	# time.sleep(1)

	re = "success"
	#clicking indivdiual ones are highly inefficient compared to collect all but leaving it for operator reset later.
	# while(re == "success"):
		

		# re = adb_controller.wait_to_match_and_click(
		# 	[r"template_images\infrastructure3.png",r"template_images\infrastructure4.png"],[0.1,0.1],True,5,1)
		# time.sleep(1.5)

	print("ArknightsController:Check Blue Notification  ....")
	re = adb_controller.wait_to_match_and_click([r"template_images\infrastructure5.png"],[0.05],True,3,0,settings.accidents)
	# re = adb_controller.wait_to_match_and_click([r"template_images\infrastructure5.png"],[0.05],True,5,3)
	# time.sleep(1)
	if(re == "success"):
		print("ArknightsController:Collect Trust  ....")
		re = adb_controller.wait_to_match_and_click([r"template_images\infrastructure6.png"],[0.05],True,3,0,settings.accidents)
		print("ArknightsController:Collect Goods ....")
		re = adb_controller.wait_to_match_and_click([r"template_images\yellow_infra.png"],[0.05],True,3,0,settings.accidents)
		# time.sleep(1)
		re = adb_controller.wait_to_match_and_click([r"template_images\blue_infra.png"],[0.05],True,3,0,settings.accidents)
		# time.sleep(2)
		#replaced by go drone
		re = go_drone_inside()
		# re = adb_controller.click([400,200])
		#replaced
		# time.sleep(1)
		# print("ArknightsController:Get Back  ....")
		# re = adb_controller.wait_to_match_and_click([r"template_images\infrastructure7.png"],[0.1],True,10,2,settings.accidents)
		# re = adb_controller.wait_to_match_and_click([r"template_images\infrastructure7_2.png"],[0.1],True,5,2,settings.accidents)
		# print("ArknightsController:Get In  ....")
		# time.sleep(2)
		# re  = adb_controller.wait_to_match_and_click([r"template_images\infrastructure1.png"],[0.1],True,20,1,settings.accidents)
		# time.sleep(10)
	else:
		print("ArknightsController:Do not find Blue Notification  ....")
		adb_controller.click([150,410])
		# time.sleep(1)
		re = go_drone_inside()

	print("ArknightsController:Change the Crew  ....")
	re  = adb_controller.wait_to_match_and_click([r"template_images\infrastructure8.png"],[0.1],True,5,0,accidents = settings.accidents)
	time.sleep(2)


	#remove first row to preserve 永动车
	adb_controller.swipe((1000,600),(1000,400),2000)
	#Get Down
	re  = adb_controller.wait_to_match_and_click([r"template_images\infrastructure9.png"],[0.1],True,5,0,accidents = settings.accidents)
	while(True):#scoll
		#revised instead of clicking each operator, lay off entire row
		matched_locs = []
		re = "success"
		while(re == "success"):
			re  = adb_controller.wait_to_match_and_click([r"template_images\layoff.png"],[0.1],False,1.5,0,scope =(120,720,1170,1235),accidents = settings.accidents,except_locs = matched_locs)
			
			if(image_processor.last_match_loc != None):
				matched_locs.append(image_processor.last_match_loc)

			# print(image_processor.last_match_loc, " matched: ",matched_locs)
			if re != "success":
				re  = adb_controller.wait_to_match_and_click([r"template_images\red_confirm1.png"],[0.1],True,1,0,settings.accidents)
			# time.sleep(3)
			# re  = adb_controller.wait_to_match_and_click(
			# 	[r"template_images\infrastructure10.png"
			# 	,r"template_images\infrastructure11.png"
			# 	,r"template_images\infrastructure11_2.png"
			# 	,r"template_images\infrastructure11_3.png"
			# 	,r"template_images\infrastructure11_4.png"
			# 	]
			# 	,[0.1,0.1,0.1,0.1,0.1],False,5,1,accidents = settings.accidents
			# 	,click_offset = (-20,25),scope = (118,696,618,1226),except_locs = matched_locs)

			

		adb_controller.screenshot(r"temp_screenshot\last_screenshot.png")
		adb_controller.swipe((1000,600),(1000,110),2000)
		time.sleep(1)
		adb_controller.screenshot(r"temp_screenshot\screenshot.png")
		if(image_processor.match_template(r"temp_screenshot\last_screenshot.png",r"temp_screenshot\screenshot.png",0.01,False) == (0,0)):
			break


	print("ArknightsController:Finished Laying off the Crew  ....")


	print("ArknightsController:Start to Station the Crew  ....")

	print("ArknightsController:Get Out  ....")
	re = adb_controller.wait_to_match_and_click([r"template_images\infrastructure7.png"],[0.1],True,5,0,settings.accidents)
	print("ArknightsController:Get In  ....")
	re  = adb_controller.wait_to_match_and_click([r"template_images\infrastructure8.png"],[0.1],True,5,0,accidents = settings.accidents)

	#Get On
	while(True):#Repeat Scorll
		matched_locs = []
		re = "success"
		while(re == "success"):
			# adb_controller.screenshot(r"temp_screenshot\last_screenshot.png")
			re  = adb_controller.wait_to_match_and_click(
				[r"template_images\infrastructure13.png"
				,r"template_images\infrastructure13_2.png"
				,r"template_images\infrastructure13_3.png"
				,r"template_images\infrastructure13_4.png"
				,r"template_images\infrastructure13_5.png"
				,r"template_images\infrastructure13_6.png"
				],[0.02,0.02,0.02,0.02,0.02,0.02],True,3,0
				,accidents = settings.accidents,scope = (118,720,618,1226),except_locs = matched_locs)
			
			if(re == "success"):
				matched_locs.append(image_processor.last_match_loc)
				# print("KKK:"+str(matched_locs))
				# time.sleep(2)
				clicked_nums = 0
				for rect_index in range(0,len(crew_rects["up_left_loc"])):
					print("ArknightsController: Check rect_index = "+str(rect_index))
					re2 = adb_controller.wait_till_match_any(
						[r"template_images\infrastructure16.png"
						,r"template_images\infrastructure16_2.png"
						,r"template_images\infrastructure16_3.png"
						,r"template_images\infrastructure16_4.png"
						,r"template_images\infrastructure16_5.png"
						,r"template_images\infrastructure16_6.png"
						,r"template_images\infrastructure16_7.png"
						,r"template_images\alt_operator.png"]
						,[0.05,0.05,0.05,0.05,0.02,0.1,0.1,0.35],True,1,0,scope = (
							crew_rects["up_left_loc"][rect_index][1]-40
							,crew_rects["up_left_loc"][rect_index][1] + crew_rects["height"]
							,crew_rects["up_left_loc"][rect_index][0]-40
							,crew_rects["up_left_loc"][rect_index][0] + crew_rects["witdth"]
							)
						)
					if(re2 != None):
						print("ArknightsController: Crew "+str(rect_index)+" is already in work/rest")
						continue
					adb_controller.click((crew_rects["up_left_loc"][rect_index][0] + crew_rects["witdth"]/2
						,crew_rects["up_left_loc"][rect_index][1] + crew_rects["height"]/2) , chk_net = False)
					clicked_nums = clicked_nums + 1
					if(clicked_nums >= 5):
						break

				print("ArknightsController: Current Crew have stationed")

				re2  = adb_controller.wait_to_match_and_click(
					[r"template_images\infrastructure15.png"
					,r"template_images\infrastructure15_2.png"
					],[0.1,0.1],True,5,0,accidents = settings.accidents)
				# time.sleep(4)

		adb_controller.screenshot(r"temp_screenshot\last_screenshot.png")
		time.sleep(2)
		adb_controller.swipe((1000,600),(1000,150),2000)
		time.sleep(1)
		adb_controller.screenshot(r"temp_screenshot\screenshot.png")

		if(image_processor.match_template(r"temp_screenshot\last_screenshot.png",r"temp_screenshot\screenshot.png",0.01,False) == (0,0)):
			break

	print("ArknightsController:Finished go infrastructure  ....")
	return "success"

def go_visit_friends():
	print("ArknightsController:Start to visit friends  ....")
	re  = adb_controller.wait_to_match_and_click([r"template_images\friends1.png"],[0.1],True,8,2,settings.accidents)
	if(re == "restart"):return re
	re  = adb_controller.wait_to_match_and_click([r"template_images\friends2.png"],[0.1],True,8,2,settings.accidents)
	if(re == "restart"):return re
	re  = adb_controller.wait_to_match_and_click([r"template_images\friends3.png"],[0.1],True,8,2,settings.accidents)
	if(re == "restart"):return re

	visit_times = 1
	# while(visit_times < 13) and adb_controller.wait_till_match_any([r"template_images\friends_orange.png"],[0.1],True,10,2,settings.accidents):
	while not((visit_times > 12) or adb_controller.wait_till_match_any([r"template_images\friends4.png"],[0.1],True,3,2,settings.accidents)):
		# re  = adb_controller.wait_to_match_and_click([r"template_images\friends_orange.png"],[0.1],True,20,2,settings.accidents)
		adb_controller.click((1174,632))

		
		# time.sleep(3)
		# re  = adb_controller.wait_to_match_and_click([r"template_images\friends4.png"],[0.1],True,20,2,settings.accidents)
		# if(re == "restart" or re == "failed"):return "restart"
		visit_times = visit_times + 1 

	print("ArknightsController:Finished visiting friends  ....")
	time.sleep(3)
	return "success"
	

def go_collect_quests():
	print("ArknightsController:Start to collect quest rewards  ....")
	re  = adb_controller.wait_to_match_and_click([r"template_images\quest1.png"],[0.1],True,10,1,settings.accidents)
	if(re == "restart"):return re
	# re  = adb_controller.wait_to_match_and_click([r"template_images\quest2.png"],[0.1],True,10,1,settings.accidents)
	# if(re == "restart"):return re

	re  = adb_controller.wait_to_match_and_click([r"template_images\quest3.png"],[0.1],True,3,1,settings.accidents)
	if(re == "restart"):return re
	re  = adb_controller.wait_to_match_and_click([r"template_images\quest2.png"],[0.1],True,3,4,settings.accidents)
	if(re == "restart"):return re
	re  = adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,3,2,settings.accidents)
	# time.sleep(1)
	
	# time.sleep(3)
	re  = adb_controller.wait_to_match_and_click([r"template_images\quest4.png"],[0.1],True,3,1,settings.accidents)
	if(re == "restart"):return re
	re  = adb_controller.wait_to_match_and_click([r"template_images\quest2.png"],[0.1],True,3,4,settings.accidents)
	if(re == "restart"):return re
	re  = adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,3,2,settings.accidents)
	# time.sleep(1)

	# re  = adb_controller.wait_to_match_and_click([r"template_images\quest5.png"],[0.1],True,10,1,settings.accidents)
	# if(re == "restart"):return re
	# re  = adb_controller.wait_to_match_and_click([r"template_images\quest2_2.png"],[0.1],True,10,1,settings.accidents)
	# if(re == "restart"):return re
	print("ArknightsController:Finished to collect quest rewards  ....")
	return "success"

def go_collect_mail():
	print("ArknightsController:Start to collect mail  ....")
	re  = adb_controller.wait_to_match_and_click([r"template_images\mail1.png"],[0.1],True,3,1,settings.accidents)
	if(re == "restart"):return re
	re  = adb_controller.wait_to_match_and_click([r"template_images\mail2.png"],[0.1],True,3,1,settings.accidents)
	if(re == "restart"):return re
	adb_controller.wait_to_match_and_click([r"template_images\accident_daily_gift.png"],[0.1],True,10,2)

	print("ArknightsController:Finished to collect mail  ....")
	return "success"

def go_shop():
	print("ArknightsController:Start to go shop  ....")
	re  = adb_controller.wait_to_match_and_click([r"template_images\shop1.png"],[0.1],True,5,2,settings.accidents)
	if(re == "restart"):return re
	# time.sleep(2)
	re  = adb_controller.wait_to_match_and_click([r"template_images\shop2.png"],[0.1],True,4,2,settings.accidents)
	if(re == "restart"):return re
	# time.sleep(2)

	if(re == "restart"):return re
	re  = adb_controller.wait_to_match_and_click([r"template_images\shop3.png"],[0.1],True,3,2,settings.accidents)
	# time.sleep(2)
	if(re == "restart"):return re
	re  = adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,3,2,settings.accidents)
	if(re == "restart"):return re

	

	while(True):
		while (adb_controller.wait_to_match_and_click([r"template_images\99discount.png"],[0.005],True,2.5,0,settings.accidents) == "success"):
		# re  = adb_controller.wait_to_match_and_click([r"template_images\99discount.png"],[0.005],True,2,2,settings.accidents)
		# if(re == "success"):
			adb_controller.wait_to_match_and_click([r"template_images\shop6.png"],[0.1],True,5,0,settings.accidents)
			# time.sleep(2)
			adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,5,0,settings.accidents)

		while (adb_controller.wait_to_match_and_click([r"template_images\95discount.png"],[0.005],True,2.5,0,settings.accidents) == "success"):
		# re  = adb_controller.wait_to_match_and_click([r"template_images\99discount.png"],[0.005],True,2,2,settings.accidents)
		# if(re == "success"):
			adb_controller.wait_to_match_and_click([r"template_images\shop6.png"],[0.1],True,5,0,settings.accidents)
			# time.sleep(2)
			adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,5,0,settings.accidents)
			
		while (adb_controller.wait_to_match_and_click([r"template_images\75discount.png"],[0.005],True,2.5,0,settings.accidents) == "success"):
		# re  = adb_controller.wait_to_match_and_click([r"template_images\75discount.png"],[0.005],True,2,2,settings.accidents)
		# if(re == "success"):
			adb_controller.wait_to_match_and_click([r"template_images\shop6.png"],[0.1],True,2.5,0,settings.accidents)
			# time.sleep(2)
			adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,2.5,0,settings.accidents)
			
		

		while (adb_controller.wait_to_match_and_click([r"template_images\red_card.png"],[0.1],True,2.5,0,settings.accidents) == "success"):
		# if(re == "success"):
			adb_controller.wait_to_match_and_click([r"template_images\shop6.png"],[0.1],True,2.5,0,settings.accidents)
			if adb_controller.wait_till_match_any([r"template_images\shop6.png"],[0.1],True,1,0,settings.accidents):
				print("NOT enough credit!")
				adb_controller.click([1,1])
				break
			# time.sleep(2)
			adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,2.5,0,settings.accidents)
			# continue
	
		while (adb_controller.wait_to_match_and_click([r"template_images\hire_card.png"],[0.1],True,2.5,0,settings.accidents) == "success"):
		# re  = adb_controller.wait_to_match_and_click([r"template_images\hire_card.png"],[0.1],True,2,2,settings.accidents)
		# if(re == "success"):
			adb_controller.wait_to_match_and_click([r"template_images\shop6.png"],[0.1],True,2.5,0,settings.accidents)
			if adb_controller.wait_till_match_any([r"template_images\shop6.png"],[0.1],True,1,0,settings.accidents):
				print("NOT enough credit!")
				adb_controller.click([1,1])
				break
			# time.sleep(2)
			adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,2.5,0,settings.accidents)
			# continue
	



		while int(image_processor.easyocr_read(settings.screenshot_path, True, scope = (20,60,1140,1203) , num_only = True)[0][1]) > 300:
			re  = adb_controller.wait_to_match_and_click([r"template_images\50discount.png"],[0.005],True,2,0,settings.accidents)
			# re  = adb_controller.wait_to_match_and_click(
			# 	[r"template_images\75discount.png",r"template_images\50discount.png"],[0.1,0.1],True,10,2,settings.accidents)
			if(re == "success"):
				adb_controller.wait_to_match_and_click([r"template_images\shop6.png"],[0.1],True,2.5,0,settings.accidents)
				# time.sleep(2)
				adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,2.5,0,settings.accidents)
				# time.sleep(1)
				adb_controller.screenshot(settings.screenshot_path)
				continue
			else:
				break

		time.sleep(1)

		adb_controller.screenshot(settings.screenshot_path)

		if int(image_processor.easyocr_read(settings.screenshot_path, True, scope = (20,60,1140,1203), num_only = True)[0][1]) > 300:
			#doesn't seen to be working as OCR detects tags even already bought


			# re  = adb_controller.wait_till_match_any_text_and_click(["固源岩","装置","赤金","初级作战记录","异铁","糖","龙门币","碳素"],3,1,scope = (405,430,60,1250))
			# # re  = adb_controller.wait_to_match_and_click(
			# # 	[r"template_images\75discount.png",r"template_images\50discount.png"],[0.1,0.1],True,10,2,settings.accidents)
			# if(re == "success"):
			# 	adb_controller.wait_to_match_and_click([r"template_images\shop6.png"],[0.1],True,5,2,settings.accidents)
			# 	adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,5,2,settings.accidents)
			# 	continue
			# else:
			# 	break

			adb_controller.click([1150,520])
			# re  = adb_controller.wait_to_match_and_click(
			# 	[r"template_images\75discount.png",r"template_images\50discount.png"],[0.1,0.1],True,10,2,settings.accidents)
			
			re = adb_controller.wait_to_match_and_click([r"template_images\shop6.png"],[0.1],True,2.5,0,settings.accidents)
			re = adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,2.5,0,settings.accidents)
			# time.sleep(1)
			adb_controller.screenshot(settings.screenshot_path)

			if int(image_processor.easyocr_read(settings.screenshot_path, True, scope = (20,60,1140,1203), num_only = True)[0][1]) > 300:
				adb_controller.click([880,520])
				re = adb_controller.wait_to_match_and_click([r"template_images\shop6.png"],[0.1],True,2.5,0,settings.accidents)
				re = adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,2.5,0,settings.accidents)

			else:
				break
			# time.sleep(3)

			if int(image_processor.easyocr_read(settings.screenshot_path, True, scope = (20,60,1140,1203), num_only = True)[0][1]) > 300:
				adb_controller.click([620,520])
				re = adb_controller.wait_to_match_and_click([r"template_images\shop6.png"],[0.1],True,2.5,0,settings.accidents)
				re = adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,2.5,0,settings.accidents)
				# time.sleep(1)
			else:
				break

			#4
			if int(image_processor.easyocr_read(settings.screenshot_path, True, scope = (20,60,1140,1203), num_only = True)[0][1]) > 300:
				adb_controller.click([360,520])
				re = adb_controller.wait_to_match_and_click([r"template_images\shop6.png"],[0.1],True,2.5,0,settings.accidents)
				re = adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,2.5,0,settings.accidents)
				# time.sleep(1)
			else:
				break


			if int(image_processor.easyocr_read(settings.screenshot_path, True, scope = (20,60,1140,1203) , num_only = True)[0][1]) > 300:
				adb_controller.click([140,520])
				re = adb_controller.wait_to_match_and_click([r"template_images\shop6.png"],[0.1],True,2.5,0,settings.accidents)
				re = adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,2.5,0,settings.accidents)
				# time.sleep(1)
			else:
				break	
			break		

			# if(re == "success"):
			# 	adb_controller.click([880,520])
			# 	re = adb_controller.wait_to_match_and_click([r"template_images\shop6.png"],[0.1],True,5,2,settings.accidents)
			# 	re = adb_controller.wait_to_match_and_click([r"template_images\shop7.png"],[0.1],True,5,2,settings.accidents)
			# else:
				# break
			
		break

	print("ArknightsController:Finished to shop  ....")
	return "success"

def go_hire_crew():
	# while (1):
	# 	five_hire_tags= []
	# 	best_combination = []
	# 	adb_controller.screenshot(settings.screenshot_path)
	# 	result = image_processor.easyocr_read(settings.screenshot_path, True, scope = (367,500,338,900))
	# 	stop_tags = 0
	# 	for reline in result:
	# 		re_text = reline[1].replace(" ","")
	# 		five_hire_tags.append(re_text)
	# 		if reline[1] == "立即招募":
	# 			print("matched and clicking now")
	# 			print(reline[0][0][0])
	# 			adb_controller.click([reline[0][0][0]+338, reline[0][0][1]+367])

	# 	adb_controller.screenshot(settings.screenshot_path)
	# 	result = image_processor.easyocr_read(settings.screenshot_path, True, scope = (367,500,338,900))
	# 	adb_controller.screenshot(settings.screenshot_path)
	# test = 0
	# while(True):

		# if test == 1:
		# 	continue
		# else:
		# 	adb_controller.swipe((1000,600),(1000,400),2000)
		# 	test = 1
		# re  = adb_controller.wait_till_match_any_text(["固源岩","装置","赤金","初级作战记录","异铁","糖","龙门币","碳素"],3,1,scope = (150,430,20,1200))
		# adb_controller.screenshot(settings.screenshot_path)
		# result = image_processor.easyocr_read(settings.screenshot_path, True, scope = (20,60,1165,1200))

		# print(result[0][1],int(result[0][1])>57)

		# adb_controller.screenshot(settings.screenshot_path)

	print("ArknightsController:Start to hire crew  ....")
	re  = adb_controller.wait_to_match_and_click([r"template_images\hire1.png"],[0.1],True,10,0,settings.accidents)
	if(re == "restart"):return re
	# time.sleep(3)
	print("ArknightsController:Try to collect crew  ....")
	while(True):
		re  = adb_controller.wait_to_match_and_click([r"template_images\hire2.png"],[0.1],True,3,0,settings.accidents)
		if(re == "success"):
			# time.sleep(2)
			re2  = adb_controller.wait_to_match_and_click([r"template_images\hire3.png"],[0.1],True,3,0,settings.accidents)
			# time.sleep(2)
			#added
			adb_controller.click([1,1])
			quick_check = adb_controller.wait_till_match_any(
			[r"template_images\hire4.png"
			,r"template_images\hire4_2.png"
			,r"template_images\hire4_3.png"
			,r"template_images\hire4_4.png"]
			,[0.1,0.1,0.1,0.1],True,2,0,settings.accidents)
			while (quick_check == None):
				adb_controller.click((1,1))
				quick_check = adb_controller.wait_till_match_any(
				[r"template_images\hire4.png"
				,r"template_images\hire4_2.png"
				,r"template_images\hire4_3.png"
				,r"template_images\hire4_4.png"]
				,[0.1,0.1,0.1,0.1],True,5,0,settings.accidents)

		else:
			break

	print("ArknightsController:Try to begin collect crew  ....")
	while(True):
		re  = adb_controller.wait_to_match_and_click(
			[r"template_images\hire4.png"
			,r"template_images\hire4_2.png"
			,r"template_images\hire4_3.png"
			,r"template_images\hire4_4.png"]
			,[0.05,0.05,0.05,0.05],True,5,0.5,settings.accidents)
		if(re == "success"):
			# time.sleep(2)
			# re2  = adb_controller.wait_to_match_and_click(
			# 	[r"template_images\hire5.png"],[0.1],False,4,0,settings.accidents,click_offset = (225,180),chk_net = False)
			# putting above line before clicking hire to save time for potential refresh

			#original check and stop func
			# re2 = adb_controller.wait_till_match_any_text(settings.go_hire_stop_options,5,0,scope = (343,500,338,900))
			# if(re2 != None):
			# 	print("ArknightsController:Found stop option in {},so stop".format(str(settings.go_hire_stop_options)))
			# 	return "success"

			#new logic
			#["群攻","快速复活","术师干员"]
			# print("NEW LOGITECH!!!!!!!!!!!!!!!!!!!!!!!")
			five_hire_tags= []
			best_combination = []
			adb_controller.screenshot(settings.screenshot_path)
			result = image_processor.easyocr_read(settings.screenshot_path, True, scope = (367,500,338,900))
			stop_tags = 0
			for reline in result:
				re_text = reline[1].replace(" ","")
				five_hire_tags.append(re_text)
			#new stop trigger func
			for i in settings.go_hire_stop_options:
				if i in five_hire_tags:
					print("ArknightsController:Found stop option in {},so stop".format(str(settings.go_hire_stop_options)))
					stop_tags = 1

			if stop_tags == 1:
				break

			for i in hiring_priority_list:
				if set(i).issubset(five_hire_tags):
					best_combination = i
					print("found high priority combo: ",best_combination)
					break#fuck i forgot to break, there fore choosing the least priority combo
			if best_combination != []:
				# adb_controller.wait_till_match_any_text_and_click(best_combination,3,0,scope = (367,500,338,900) , chk_net = False)
				# old method, inefficent, using OCR for the second time, below is attempt to optimize
				for b in best_combination:
					for r in result:
						if r[1] in b:
							adb_controller.click([r[0][0][0]+338, r[0][0][1]+367])

			else:
				for i in less_priority_list:
					if set(i).issubset(five_hire_tags):
						best_combination.append(i)


				if best_combination != []:
					print("less priority combo found : ", best_combination)
						# adb_controller.wait_till_match_any_text_and_click(i,3,0,scope = (367,500,338,900) , chk_net = False) # this uses ocr uncessarily can be optimized.
				#new testing function to refresh if less priority tags are less than 3

				# old method, inefficent, using OCR for the second time, below is attempt to optimize
					for b in best_combination:
						for r in result:

							if r[1] in b:
								adb_controller.click([r[0][0][0]+338, r[0][0][1]+367])

				if len(best_combination) < 3:
					refresh_count = image_processor.easyocr_read(settings.screenshot_path, True, scope = (72,100,870,960))[0][1]#(y1, y2, x1,x2)
					print(refresh_count)
					#if retry count is larger than 3 and no good tags, then refresh, otherwise, select random 3
					if refresh_count == "联络次数3/3" or refresh_count == "联络次数2/3":
						print("using refresh to get potential better tags!")
						# re2  = adb_controller.wait_to_match_and_click(
						# [r"template_images\hire6.png"],[0.1],False,10,2,settings.accidents,click_offset = (195,-12))

						re2  = adb_controller.wait_to_match_and_click(
					[r"template_images\refresh1.png"],[0.1],True,3,0,settings.accidents)
						re2  = adb_controller.wait_to_match_and_click(
					[r"template_images\red_confirm1.png"],[0.1],True,3,0,settings.accidents)
						# time.sleep(3)
						re2  = adb_controller.wait_to_match_and_click(
					[r"template_images\back.png"],[0.1],True,3,0,settings.accidents)
						# time.sleep(1)
						continue

				
				#click any 3 less priority
			print("\nFive tags are: " + str(five_hire_tags))
			# time.sleep(10)
			#check = adb_controller.wait_till_match_any_text_and_click(hiring_priority_list,3,1,scope = (367,500,338,900))
			#print("ANKSJDKASJDKSAJD" + str(check))

			
			if best_combination == []:
				adb_controller.screenshot(settings.screenshot_path)
				refresh_count = image_processor.easyocr_read(settings.screenshot_path, True, scope = (72,100,870,960))[0][1]#(y1, y2, x1,x2)
				print(refresh_count)
				#if retry count is larger than 3 and no good tags, then refresh, otherwise, select random 3
				if refresh_count == "联络次数0":
					# re2  = adb_controller.wait_to_match_and_click(
					# [r"template_images\hire6.png"],[0.1],False,10,2,settings.accidents,click_offset = (195,-12))
					# adb_controller.wait_till_match_any_text_and_click(five_hire_tags,3,0,scope = (367,500,338,900) , chk_net = False)
					#above old method, inefficent, using OCR for the second time, below is attempt to optimize
					for r in result:
						adb_controller.click([r[0][0][0]+338, r[0][0][1]+367])
				else:
					re2  = adb_controller.wait_to_match_and_click(
				[r"template_images\refresh1.png"],[0.1],True,3,0,settings.accidents)
					re2  = adb_controller.wait_to_match_and_click(
				[r"template_images\red_confirm1.png"],[0.1],True,3,0,settings.accidents)
					# time.sleep(3)
					re2  = adb_controller.wait_to_match_and_click(
				[r"template_images\back.png"],[0.1],True,3,0,settings.accidents)
					# time.sleep(1)
					continue
					#click refresh, and restart the loop


			# end of new logic

			#click 9 hour
			re2  = adb_controller.wait_to_match_and_click(
				[r"template_images\hire5.png"],[0.1],False,4,0,settings.accidents,click_offset = (225,180),chk_net = False)

			#click hire
			re2  = adb_controller.wait_to_match_and_click(
				[r"template_images\hire7.png"],[0.1],True,2,0,settings.accidents)
			# time.sleep(7)
		else:
			break

	print("ArknightsController:Finished to hire crew  ....")
	return "success"

def go_clue_get_in():
	re  = adb_controller.wait_to_match_and_click([r"template_images\gclue1.png"],[0.1],True,10,1,settings.accidents)
	re = adb_controller.wait_till_match_any([r"template_images\gclue2.png"],[0.1],True,20,1)
	if(re == "restart"):return re
	adb_controller.click([1,1])#check lag
	adb_controller.swipe((800,400),(400,400),2000)
	adb_controller.click([1,1])#check lag
	re  = adb_controller.wait_to_match_and_click([r"template_images\gclue3.png"],[0.1],True,10,1,settings.accidents)
	re  = adb_controller.wait_to_match_and_click([r"template_images\gclue4.png"],[0.1],True,10,1,settings.accidents)
	#new , check if finished exchange clue
	adb_controller.screenshot(r"temp_screenshot\screenshot.png")

	adb_controller.screenshot(settings.screenshot_path)
	if image_processor.match_template(settings.screenshot_path, r"template_images\finished_exchange.png", scope=(70,160,20,350)):
		adb_controller.wait_to_match_and_click([r"template_images\back.png"],[0.1],True,3,1,settings.accidents)
	
# Require get in first
def recieve_clue_from_friends():
	return 0
def go_clue_get_on_clue():
	re  = adb_controller.wait_to_match_and_click([r"template_images\gclue5.png"],[0.1],True,10,2,settings.accidents)
	# time.sleep(1)
	re  = adb_controller.wait_to_match_and_click([r"template_images\clue_inbox.png"],[0.1],True,10,2,settings.accidents)
	for tab_index in range(1,8):
		re  = adb_controller.wait_to_match_and_click([r"template_images\gclue6_{}.png".format(tab_index)],[0.1],True,10,2,settings.accidents,chk_net=False)
		re = adb_controller.wait_till_match_any(
			[r"template_images\gclue7_1.png",r"template_images\gclue7_2.png"],[0.1,0.1],True,3,1,scope = (148,330,879,1268))
		if(re == None):
			adb_controller.click((1094,238))
		# time.sleep(2)
	re= adb_controller.click([1,1])
	#originally back then enter again
	# re  = adb_controller.wait_to_match_and_click([r"template_images\gclue11.png"],[0.1],True,10,2,settings.accidents)
	# re  = adb_controller.wait_to_match_and_click([r"template_images\gclue4.png"],[0.1],True,10,2,settings.accidents)

def go_send_additional_clue():
	
	re  = adb_controller.wait_to_match_and_click([r"template_images\gclue12.png"],[0.01],True,10,2,settings.accidents)

	for tab_index in range(1,8):

		re  = adb_controller.wait_to_match_and_click(
			[r"template_images\gclue18_{}.png".format(tab_index)],[0.1],True,5,1,settings.accidents,chk_net = False)

		re3  = adb_controller.wait_to_match_and_click(
					[r"template_images\gclue13.png"],[0.1],True,1,0,settings.accidents,scope = (136,334,14,423),chk_net= False)
		if(re3 == "success"):
			for i in range(12):
					adb_controller.click((1120,680),chk_net=False)#reset to first page

		if(re == None):
			print("ArknightsController:ERROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOR cannot find number tab  ....")
			return "ERROR"
		

		if(re == "success"):
			
			direction = "No"
			#new
			clue_priority ="today"
			matched_locs = []
			#end of new
			while(True):
				# original skips first clue, below includes first clue, also moving down to the while loop
				# re  = adb_controller.wait_to_match_and_click(
				# 	[r"template_images\gclue13.png"],[0.1],True,3,1,settings.accidents,scope = (336,534,14,423))
				re3  = adb_controller.wait_to_match_and_click(
					[r"template_images\gclue13.png"],[0.1],True,2,0,settings.accidents,scope = (136,334,14,423),chk_net= False)
				if re3 != "success":
					break

				re2 = adb_controller.wait_till_match_any(
					[r"template_images\gclue14.png"],[0.01],True,2,0,scope = (68,633,819,1157) , except_locs = matched_locs)
				
				if(image_processor.last_match_loc != None):
					matched_locs.append(image_processor.last_match_loc)

				if(re2 == None):

					scroll_result = None

					if(direction == "No" or direction == "right"):
						scroll_result  = adb_controller.wait_to_match_and_click(
							[r"template_images\gclue15.png"],[0.1],True,3,0,settings.accidents,scope = (635,710,1060,1253))
						if (scroll_result == "success"):
							matched_locs = []
					else:
						scroll_result  = adb_controller.wait_to_match_and_click(
							[r"template_images\gclue16.png"],[0.1],True,3,0,settings.accidents,scope = (635,710,1060,1253))
						if (scroll_result == "success"):
							matched_locs = []

					if(scroll_result != "success"):
						break
					else:
						continue

				else:
					if adb_controller.wait_till_match_any(
					# [r"template_images\active_today.png", r"template_images\active_yesterday.png"],[0.01],True,5,0,scope = (140,640,700,835)):
					[r"template_images\active_today.png", r"template_images\active_yesterday.png"],[0.015,0.015],True,1,0,scope = (int(re2[1]+50),int(re2[1])+130,700,835)):
						adb_controller.click((1187,re2[1]))
						
					# break

	re  = adb_controller.wait_to_match_and_click([r"template_images\gclue17.png"],[0.1],True,5,0,settings.accidents)




def go_clue_get_new_clue():
	for repeat_time in range(2):
		re  = adb_controller.wait_to_match_and_click(
			[r"template_images\gclue9.png",r"template_images\gclue9_2.png"]
			,[0.1,0.1],False,10,2,settings.accidents,click_offset = (-20,44))
		if(re == "success"):
			re  = adb_controller.wait_to_match_and_click([
				r"template_images\gclue10.png",r"template_images\gclue10_1.png"],[0.1,0.1],True,10,2,settings.accidents)
			# time.sleep(5)
			adb_controller.click([1,1])#go back to previous screen if needed
			# time.sleep(2)
		else:
			break;


def go_clue():

	print("ArknightsController:Start to Go Clue -- Get in ....")
	go_clue_get_in()

	print("ArknightsController:Start to Go Clue -- Get new clue  ....")
	go_clue_get_new_clue()

	print("ArknightsController:Start to Go Clue -- Get on new clue  ....")
	go_clue_get_on_clue()

	print("ArknightsController:Start to Go Clue -- Try unlock clue  ....")
	re  = adb_controller.wait_to_match_and_click([r"template_images\gclue8.png"],[0.1],True,10,2,settings.accidents)
	if(re == "success"):
		re  = adb_controller.wait_to_match_and_click([r"template_images\gclue4.png"],[0.1],True,10,2,settings.accidents)

	print("ArknightsController:Start to Go Clue -- Send additional clue  ....")
	go_send_additional_clue()

	print("ArknightsController:Start to Go Clue -- Get new clue  ....")
	go_clue_get_new_clue()

	print("ArknightsController:Finished to Go Clue  ....")
	return "success"

def go_drone():
	print("ArknightsController:Start to Go Drone -- Get in ....")
	re  = adb_controller.wait_to_match_and_click([r"template_images\infrastructure1.png"],[0.1],True,20,1,settings.accidents)
	if(re == "restart"):return re
	time.sleep(5)

	adb_controller.swipe((400,400),(800,400),2000)
	time.sleep(2)

	re  = adb_controller.wait_to_match_and_click([r"template_images\drone1.png"],[0.1],True,20,1,settings.accidents)
	if(re != "success"):
		return "end"

	re  = adb_controller.wait_to_match_and_click([r"template_images\drone2.png"],[0.1],True,20,1,settings.accidents)
	if(re != "success"):
		return "end"

	while(True):
		re  = adb_controller.wait_to_match_and_click([r"template_images\drone3.png"],[0.1],True,20,1,settings.accidents)
		if(re != "success"):
			return "end"

		re  = adb_controller.wait_till_match_any([r"template_images\drone7.png"],[0.01],True,4,1)
		if(re != None):
			return "end"

		re  = adb_controller.wait_to_match_and_click([r"template_images\drone4.png"],[0.1],True,20,1,settings.accidents)
		if(re != "success"):
			return "end"

		re  = adb_controller.wait_to_match_and_click([r"template_images\drone6.png"],[0.1],True,20,1,settings.accidents)
		if(re != "success"):
			return "end"
	

	print("ArknightsController:Finished to Go Clue  ....")
	return "success"

def go_drone_inside():
	re = adb_controller.click([275,400])
	time.sleep(1)
	re = adb_controller.click([275,400])
	# re  = adb_controller.wait_to_match_and_click([r"template_images\drone1.png"],[0.1],True,20,1,settings.accidents)
	# if(re != "success"):
	# 	return "end"

	# re  = adb_controller.wait_to_match_and_click([r"template_images\drone2.png"],[0.1],True,20,1,settings.accidents)
	# if(re != "success"):
	# 	return "end"
	# time.sleep(5)
	# re = adb_controller.click([300,600])
	re  = adb_controller.wait_to_match_and_click([r"template_images\factory.png"],[0.1],True,10,1,settings.accidents)
	# if(re != "success"):
	# 	return "end"
	# time.sleep(3)

	re  = adb_controller.wait_to_match_and_click([r"template_images\yellow_drone_speed_up.png"],[0.1],True,5,1,settings.accidents)
	# if(re != "success"):
	# 	return "end"

	re  = adb_controller.wait_till_match_any([r"template_images\drone7.png"],[0.01],True,3,1)
	# if(re != None):
	# 	return "end"

	re  = adb_controller.wait_to_match_and_click([r"template_images\drone4.png"],[0.1],True,3,1,settings.accidents)
	# if(re != "success"):
	# 	return "end"
	if re=="success":

		re  = adb_controller.wait_to_match_and_click([r"template_images\drone6.png"],[0.1],True,3,1,settings.accidents)
		# if(re != "success"):
		# 	return "end"
		# time.sleep(5)
		re  = adb_controller.wait_to_match_and_click([r"template_images\recieve.png"],[0.1],True,5,1,settings.accidents)
		# if(re != "success"):
		# 	return "end"
		# time.sleep(10)
	else:
		print("Failed to boost, operator not in factory or already used all drones")

	re  = adb_controller.wait_to_match_and_click([r"template_images\back.png"],[0.1],True,3,1,settings.accidents)
	# if(re != "success"):
	# 	return "end"
	# time.sleep(2)
	re  = adb_controller.wait_to_match_and_click([r"template_images\back.png"],[0.1],True,3,1,settings.accidents)
	# if(re != "success"):
	# 	return "end"
	adb_controller.click((1,1))

	print("ArknightsController:Finished to speed up drones  ....")
	return "success"

	


########################  Main   ##########################
my_directory = os.path.basename(os.getcwd())


settings_path = r"E:\Code Base\Python Project\Arknight Autobot v2\settings.txt"
# settings_path = r"settings.txt"

add_string_vars = ["to_do_list","auto_t_level"]

string_vars = ["adb_path","device_address","main_address","chenrui_address","connor_address","sam_address","math_address","bill_address"]
######


######
int_vars = ["auto_ce_level"
				,"auto_ls_level"
				,"go_level_cycle"
				,"go_infrastructure_cycle"
				,"go_visit_friends_cycle"
				,"go_collect_quests_cycle"
				,"go_collect_mail_cycle"
				,"go_shop_cycle"
				,"go_hire_crew_cycle"
				,"go_hire_stop_options"
				,"go_clue_cycle"
				,"go_drone_cycle"
				,"recheck_time_when_no_work_to_do"]
				
print("#####################################################")
print("Start to read settings by {}".format(settings_path))
print("#####################################################")



for add_string_var in add_string_vars:
	exec("settings.{} = []".format(add_string_var),globals())
	# print("clear {}".format(add_string_var))
	# print(str(to_do_list))

# for line in open(settings_path,encoding = "gb18030",errors = "ignore"):
for line in open(settings_path,encoding = "UTF-8",errors = "ignore"):
	# Get rid of #
	if(len(re.findall("#",line)) > 0):
		line = re.findall("^(.*)#",line)[0]
	# print(line)

	# Set strings
	for string_var in string_vars:
		k = re.findall("^ *{} *= *\"(.+)\"".format(string_var),line)
		if(len(k)>0):
			temp_string = k[0]
			print("set {} : {}".format(string_var,temp_string))
			exec("settings.{} = temp_string".format(string_var),globals())
			continue

	# Set ints
	for int_var in int_vars:
		k = re.findall("^ *{} *= *(.+)".format(int_var),line)
		if(len(k)>0):
			temp_int = int(k[0])
			
			print("set {} : {}".format(int_var,str(temp_int)))
			exec("settings.{} = temp_int".format(int_var),globals())

	# Set add_string_vars
	for add_string_var in add_string_vars:
		k = re.findall("^ *{}\.append\(\"(.+)\"\) *".format(add_string_var),line)
		if(len(k)>0):
			temp_string = k[0]
			print("append {} : {}".format(add_string_var,str(temp_string)))
			exec("settings.{}.append(temp_string)".format(add_string_var))
#detecting if using multi conda

ctypes.windll.kernel32.SetConsoleTitleW(str(my_directory))
if my_directory in ["main","chenrui","connor","sam","math","bill"]:
	exec("settings.device_address = settings.{}_address".format(my_directory),globals())
	ctypes.windll.kernel32.SetConsoleTitleW(str(my_directory))

print(settings.device_address)
print("#####################################################")
print("Finished read settings by {}".format(settings_path))
print("#####################################################")


last_go_level_time = 0
last_go_infrastructure_time = 0
last_go_drone_time = 0
last_go_visit_friends_time = 0
last_go_collect_quests_time = 0
last_go_collect_mail_time = 0
last_go_shop_time = 0
last_go_hire_crew_time = 0
last_go_clue_time = 0
last_time = -1
work_cycle = -1

while(True):

	have_anything_to_do = False

	for a_work in settings.to_do_list:
		# time.sleep(3)
		exec("last_time = last_{}_time".format(a_work))
		exec("work_cycle = settings.{}_cycle".format(a_work))

		print("ArknightsController: Check Work : {} ,last_time = {} , current_time = {} ,work_cycle = {}"
			.format(a_work, last_time, time.time(),work_cycle))

		if(last_time == 0 or time.time() - last_time > work_cycle):

			have_anything_to_do = True

			print("#####################################################")
			print("ArknightsController: Choose to do " + a_work + " ....")
			print("#####################################################")

			#re = restart_app()
			# if re = adb_controller.wait_till_match_any([r"template_images\start0.png"],[0.3],True,60,2):
				# re = start_app()

			if(re == "restart"):
				continue

			exec("last_{}_time = time.time()".format(a_work))

			exec("re = {}()".format(a_work))

			if(re == "restart"):
				continue

			print("#####################################################")
			print("ArknightsController: Finished " + a_work + " !")
			print("#####################################################")
			
			#go back home page
			print("ArknightsController: Going back home page")
			re = adb_controller.wait_to_match_and_click([r"template_images\options.png"],[0.3],True,5,2)
			re = adb_controller.wait_to_match_and_click([r"template_images\home_option.png"],[0.3],True,5,2)
			# time.sleep(5)

			if have_anything_to_do == False:
				print("ArknightsController: Close the game")
				stop_app()

	if(have_anything_to_do == False):
		print("ArknightsController:No work to do yet.Sleep for "
			+ str(settings.recheck_time_when_no_work_to_do) +" seconds....")
		time.sleep(settings.recheck_time_when_no_work_to_do)
