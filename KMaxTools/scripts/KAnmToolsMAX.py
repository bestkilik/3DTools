import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui
import json
import pymxs
import MaxPlus
from pymxs import runtime as rt
from pymxs import attime as at
from collections import OrderedDict

import os
import sys
# from PySide2 import shiboken2 as wrapInstance
# from ctypes import pythonapi, c_void_p, py_object

def getFlipMatrix(m, flipIdx):
	if flipIdx == 1: # flip X
		return rt.matrix3(rt.point3( m[0][0],-m[0][1],-m[0][2]), 
						  rt.point3(-m[1][0], m[1][1], m[1][2]), 
						  rt.point3(-m[2][0], m[2][1], m[2][2]), 
						  rt.point3(-m[3][0], m[3][1], m[3][2]))
	elif flipIdx == 2: # flip Y
		return rt.matrix3(rt.point3(-m[0][0], m[0][1], m[0][2]), 
						  rt.point3( m[1][0],-m[1][1],-m[1][2]), 
						  rt.point3(-m[2][0], m[2][1], m[2][2]), 
						  rt.point3(-m[3][0], m[3][1], m[3][2]))
	elif flipIdx == 3: # flip Z
		return rt.matrix3(rt.point3(-m[0][0], m[0][1], m[0][2]), 
						  rt.point3(-m[1][0], m[1][1], m[1][2]), 
						  rt.point3( m[2][0],-m[2][1],-m[2][2]), 
						  rt.point3(-m[3][0], m[3][1], m[3][2]))
	else:	# flip All
		return rt.matrix3(rt.point3(-m[0][0],-m[0][1],-m[0][2]), 
						  rt.point3(-m[1][0],-m[1][1],-m[1][2]), 
						  rt.point3(-m[2][0],-m[2][1],-m[2][2]), 
						  rt.point3(-m[3][0], m[3][1], m[3][2]))

def exportPose(filePath, isMirror):
	selObjects = rt.selection

	if selObjects.count > 0:
		PoseData = OrderedDict()

		PoseData['type'] = "Matrix"
		PoseData['count'] = selObjects.count

		objList = []
		for o in selObjects:
			if isMirror and rt.isProperty(o,'MirrorInfo'):
				objList.append(o.SymmetryNode)
			else:
				objList.append(o.name)
		PoseData['name'] = objList

		mtxArray = []
		for o in selObjects:
			
			if isMirror and rt.isProperty(o,'MirrorInfo'):
				po = o.parent
				if po != None:
					if rt.isProperty(po,'MirrorInfo'):
						pfIdx = po.FlipAxis
					else:
						pfIdx = 2
					pMtx = getFlipMatrix(po.transform, pfIdx)
				else:
					pMtx = rt.matrix3(1)
				wMtx = getFlipMatrix(o.transform, o.FlipAxis)
			else:
				wMtx = o.transform
				if o.parent != None:
					pMtx = o.parent.transform
				else:
					pMtx = rt.matrix3(1)

			locMtx = wMtx * rt.Inverse(pMtx)
			mtxArray.append([[locMtx[0][0], locMtx[0][1], locMtx[0][2]],
							 [locMtx[1][0], locMtx[1][1], locMtx[1][2]],
							 [locMtx[2][0], locMtx[2][1], locMtx[2][2]],
							 [locMtx[3][0], locMtx[3][1], locMtx[3][2]]])

		transformData = OrderedDict()
		transformData["LocalMatrix"] = mtxArray

		PoseData['Pose'] = transformData
		json_str = json.dumps(PoseData, sort_keys=False)

		#### Write to xpf file ###
		text_file = open(filePath, "w")
		text_file.write(json_str)
		text_file.close()

def importPose(filePath):
	text_file = open(filePath, "r")

	fString = text_file.read()
	kpfData = json.loads(fString)

	objCount = kpfData['count']
	objList = kpfData['name']
	PoseData = kpfData['Pose']

	for i in range(objCount):
		obj = rt.getNodeByName(objList[i])
		if obj != None:
			m = PoseData['LocalMatrix'][i]
			locMtx = rt.matrix3(rt.point3( m[0][0], m[0][1], m[0][2]), 
								rt.point3( m[1][0], m[1][1], m[1][2]), 
								rt.point3( m[2][0], m[2][1], m[2][2]), 
								rt.point3( m[3][0], m[3][1], m[3][2]))
			if obj.parent != None:
				pMtx = obj.parent.transform
			else:
				pMtx = rt.matrix3(1)

			wMtx = locMtx * pMtx
			obj.transform = wMtx

	rt.redrawViews()

def exportAnima(filePath, isMirror):
	selObjects = rt.selection

	if selObjects.count > 0:
		startTime = int(rt.animationRange.start)
		endTime = int(rt.animationRange.end)
		currentTime = int(rt.currentTime)
		timePrefix = startTime
		framesCount = endTime - startTime + 1

		AnimData = OrderedDict()
		AnimData['type'] = "Matrix"
		AnimData['count'] = selObjects.count

		objList = []

		for o in selObjects:
			if isMirror and rt.isProperty(o,'MirrorInfo'):
				objList.append(o.SymmetryNode)
			else:
				objList.append(o.name)

		AnimData['name'] = objList
		AnimData['timelength'] = framesCount
		frameAniData = OrderedDict()

		rt.disableSceneRedraw()

		for f in range(framesCount):
			rt.sliderTime = f + timePrefix
			mtxArray = []

			for o in selObjects:
				if isMirror and rt.isProperty(o,'MirrorInfo'):
					po = o.parent
					if po != None:
						if rt.isProperty(po,'MirrorInfo'):
							pfIdx = po.FlipAxis
						else:
							pfIdx = 2
						pMtx = getFlipMatrix(po.transform, pfIdx)
					else:
						pMtx = rt.matrix3(1)
					wMtx = getFlipMatrix(o.transform, o.FlipAxis)
				
				else:
					wMtx = o.transform
					if o.parent != None:
						pMtx = o.parent.transform
					else:
						pMtx = rt.matrix3(1)

				locMtx = wMtx * rt.Inverse(pMtx)
				mtxArray.append([[locMtx[0][0], locMtx[0][1], locMtx[0][2]],
								 [locMtx[1][0], locMtx[1][1], locMtx[1][2]],
								 [locMtx[2][0], locMtx[2][1], locMtx[2][2]],
								 [locMtx[3][0], locMtx[3][1], locMtx[3][2]]])

			transformData = OrderedDict()
			transformData["LocalMatrix"] = mtxArray

			frameAniData[f] = transformData

		AnimData["Animation"] = frameAniData
		json_str = json.dumps(AnimData, sort_keys=False)
		
		#### Write to xaf file ###
		text_file = open(filePath, "w")
		text_file.write(json_str)
		text_file.close()

		rt.sliderTime = currentTime
		rt.enableSceneRedraw()
		rt.messageBox(filePath + "\n儲存完成")
		# print('Kaf儲存完成')

def importAnima(filePath):
	text_file = open(filePath, "r")

	fString = text_file.read()
	kafData = json.loads(fString)

	anmType = kafData['type']
	if anmType == 'Matrix':
		objCount = kafData['count']
		objList = kafData['name']
		framesCount = kafData['timelength']
		AnimData = kafData['Animation']

		endTime = int(rt.animationRange.end)
		startFrame = int(rt.currentTime)
		rt.disableSceneRedraw()
		for f in range(framesCount):
			tKey = str(f)
			for i in range(objCount):
				obj = rt.getNodeByName(objList[i])
				if obj != None:
					m = AnimData[tKey]['LocalMatrix'][i]
					locMtx = rt.matrix3(rt.point3( m[0][0], m[0][1], m[0][2]), 
										rt.point3( m[1][0], m[1][1], m[1][2]), 
										rt.point3( m[2][0], m[2][1], m[2][2]), 
										rt.point3( m[3][0], m[3][1], m[3][2]))
					if obj.parent != None:
						pMtx = obj.parent.transform
					else:
						pMtx = rt.matrix3(1)

					wMtx = locMtx * pMtx
					with pymxs.animate(True):
						with at(startFrame+f):
							obj.transform = wMtx

		####
		for n in objList:
			obj = rt.getNodeByName(n)
			if obj != None:
				rt.setPropertyController(obj.controller, "rotation", rt.tcb_rotation())
				rt.setPropertyController(obj.controller, "rotation", rt.euler_XYZ())
		
		####
		newEndFrame = startFrame + framesCount
		if newEndFrame > endTime:
			# rt.animationRange.end = newEndFrame - 1
			rt.animationRange = rt.interval(rt.animationRange.start, newEndFrame - 1)

		text_file.close()
		rt.enableSceneRedraw()
		rt.messageBox(filePath+"\n動作輸入完成")
		# print('動作輸入完成')

def getFilePathInfo(fullPath):
	DiskPath, fullFileName = os.path.split(fullPath)
	FileName, FileType = os.path.splitext(fullFileName)
	
	if DiskPath[-1] != '\\':
		DiskPath += '\\'

	return [DiskPath,FileName,FileType]

# def max_main_window():
# 	main_window_ptr = MaxPlus.GetQMaxMainWindow()
# 	return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class KAnimTools(QtWidgets.QDialog):
	RootPath = ''

	exportAnimPath_edit = QtWidgets.QLineEdit("D:\\Anm.kaf")
	exportPosePath_edit = QtWidgets.QLineEdit("D:\\Pose.kpf")

	uiScale = rt.Point2(1,1)

	def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
		super(KAnimTools, self).__init__(parent)
		# self.closeExistingWindow()
		self.RootPath = os.path.dirname(sys.argv[0]) + '\\'
		self.uiScale = rt.sysInfo.DesktopSizeUnscaled / rt.sysInfo.DesktopSize

		self.create()
	
	def __del__(self):
		pass

	def closeExistingWindow(self):
		try:
			for qt in MaxPlus.GetQMaxMainWindow().findChildren(QtWidgets.QDialog):
				if qt.__class__.__name__ == self.__class__.__name__:
					qt.close()
					# qt.deleteLater()
			pass
		except:
			pass

	def closeEvent(self, event):
		self.deleteLater()
		pass

	def create(self):
		self.setWindowTitle('K Anim Tools v1.0')
		self.setWindowFlags(QtCore.Qt.Tool)
		self.setMinimumSize(400 * self.uiScale.x,640 * self.uiScale.y)
		self.setMaximumSize(400 * self.uiScale.x,640 * self.uiScale.y)

		self.create_controls()
		self.create_layout()
		self.create_connection()
		self.readConfig()
		self.show()

	def readConfig(self):
		## Default Value ##
		kafPath = 'D:\\Anm.kaf'
		kpfPath = 'D:\\Pose.kpf'
		maxIni = rt.getMAXIniFile()

		if rt.hasINISetting(maxIni, 'Directories', 'kafPath'):
			kafPath = rt.getINISetting(maxIni, 'Directories', 'kafPath')
		else:
			rt.setINISetting(maxIni, 'Directories', 'kafPath', kafPath)

		if rt.hasINISetting(maxIni, 'Directories', 'kpfPath'):
			kpfPath = rt.getINISetting(maxIni, 'Directories', 'kpfPath')
		else:
			rt.setINISetting(maxIni, 'Directories', 'kpfPath', kpfPath)

		self.exportAnimPath_edit.setText(kafPath)
		self.exportPosePath_edit.setText(kpfPath)
	
	def create_controls(self):
		usrImgFold = self.RootPath + 'icons\\'

		#--------------------------------------------------
		palette0 = QtGui.QPalette(QtGui.QColor(32,234,75))
		palette1 = QtGui.QPalette(QtGui.QColor(41,126,185))
		palette2 = QtGui.QPalette(QtGui.QColor(61,171,140))
		palette3 = QtGui.QPalette(QtGui.QColor(176,146,55))
		palette4L = QtGui.QPalette(QtGui.QColor(53,76,160))
		palette4R = QtGui.QPalette(QtGui.QColor(53,160,81))
		palette5L = QtGui.QPalette(QtGui.QColor(45,50,118))
		palette5R = QtGui.QPalette(QtGui.QColor(45,118,60))
		palette6L = QtGui.QPalette(QtGui.QColor(71,79,196))
		palette6R = QtGui.QPalette(QtGui.QColor(52,153,74))
		palette7 = QtGui.QPalette(QtGui.QColor(112,10,10))
		#---------------------------------------------------------
		self.btnSel_Root = QtWidgets.QPushButton('Root')
		self.btnSel_Hip = QtWidgets.QPushButton('')
		self.btnSel_Waist = QtWidgets.QPushButton('')
		self.btnSel_Chest = QtWidgets.QPushButton('')
		self.btnSel_Chest1 = QtWidgets.QPushButton('')
		self.btnSel_Neck = QtWidgets.QPushButton('')
		self.btnSel_Head = QtWidgets.QPushButton('')
		self.btnSel_ShoulderL = QtWidgets.QPushButton('')
		self.btnSel_ShoulderR = QtWidgets.QPushButton('')
		self.btnSel_FKUpperArmL = QtWidgets.QPushButton('FK')
		self.btnSel_FKUpperArmR = QtWidgets.QPushButton('FK')
		self.btnSel_FKForeArmL = QtWidgets.QPushButton('FK')
		self.btnSel_FKForeArmR = QtWidgets.QPushButton('FK')
		self.btnSel_FKHandL = QtWidgets.QPushButton('FK')
		self.btnSel_FKHandR = QtWidgets.QPushButton('FK')
		self.btnSel_IKArmUpVL = QtWidgets.QPushButton('IK')
		self.btnSel_IKArmUpVR = QtWidgets.QPushButton('IK')
		self.btnSel_IKHandL = QtWidgets.QPushButton('IK')
		self.btnSel_IKHandR = QtWidgets.QPushButton('IK')
		self.btnSel_IKLegUpVL = QtWidgets.QPushButton('IK')
		self.btnSel_IKLegUpVR = QtWidgets.QPushButton('IK')
		self.btnSel_IKLegL = QtWidgets.QPushButton('IK')
		self.btnSel_IKLegR = QtWidgets.QPushButton('IK')
		self.btnSel_FootL = QtWidgets.QPushButton('')
		self.btnSel_FootR = QtWidgets.QPushButton('')
		
		self.btnSel_Finger00L = QtWidgets.QPushButton('')
		self.btnSel_Finger01L = QtWidgets.QPushButton('')
		self.btnSel_Finger02L = QtWidgets.QPushButton('')
		self.btnSel_Finger10L = QtWidgets.QPushButton('')
		self.btnSel_Finger11L = QtWidgets.QPushButton('')
		self.btnSel_Finger12L = QtWidgets.QPushButton('')
		self.btnSel_Finger20L = QtWidgets.QPushButton('')
		self.btnSel_Finger21L = QtWidgets.QPushButton('')
		self.btnSel_Finger22L = QtWidgets.QPushButton('')
		self.btnSel_Finger30L = QtWidgets.QPushButton('')
		self.btnSel_Finger31L = QtWidgets.QPushButton('')
		self.btnSel_Finger32L = QtWidgets.QPushButton('')
		self.btnSel_Finger40L = QtWidgets.QPushButton('')
		self.btnSel_Finger41L = QtWidgets.QPushButton('')
		self.btnSel_Finger42L = QtWidgets.QPushButton('')
		self.btnSel_Finger00R = QtWidgets.QPushButton('')
		self.btnSel_Finger01R = QtWidgets.QPushButton('')
		self.btnSel_Finger02R = QtWidgets.QPushButton('')
		self.btnSel_Finger10R = QtWidgets.QPushButton('')
		self.btnSel_Finger11R = QtWidgets.QPushButton('')
		self.btnSel_Finger12R = QtWidgets.QPushButton('')
		self.btnSel_Finger20R = QtWidgets.QPushButton('')
		self.btnSel_Finger21R = QtWidgets.QPushButton('')
		self.btnSel_Finger22R = QtWidgets.QPushButton('')
		self.btnSel_Finger30R = QtWidgets.QPushButton('')
		self.btnSel_Finger31R = QtWidgets.QPushButton('')
		self.btnSel_Finger32R = QtWidgets.QPushButton('')
		self.btnSel_Finger40R = QtWidgets.QPushButton('')
		self.btnSel_Finger41R = QtWidgets.QPushButton('')
		self.btnSel_Finger42R = QtWidgets.QPushButton('')

		self.btnSel_FingerX4L = QtWidgets.QPushButton('')
		self.btnSel_FingerX4R = QtWidgets.QPushButton('')
		self.btnSel_FingerS0L = QtWidgets.QPushButton('')
		self.btnSel_FingerS1L = QtWidgets.QPushButton('')
		self.btnSel_FingerS2L = QtWidgets.QPushButton('')
		self.btnSel_FingerS0R = QtWidgets.QPushButton('')
		self.btnSel_FingerS1R = QtWidgets.QPushButton('')
		self.btnSel_FingerS2R = QtWidgets.QPushButton('')
		self.btnSel_FingerSx2L = QtWidgets.QPushButton('')
		self.btnSel_FingerSx2R = QtWidgets.QPushButton('')

		self.btnSel_Finger0L = QtWidgets.QPushButton('')
		self.btnSel_Finger1L = QtWidgets.QPushButton('')
		self.btnSel_Finger2L = QtWidgets.QPushButton('')
		self.btnSel_Finger3L = QtWidgets.QPushButton('')
		self.btnSel_Finger4L = QtWidgets.QPushButton('')
		self.btnSel_Finger0R = QtWidgets.QPushButton('')
		self.btnSel_Finger1R = QtWidgets.QPushButton('')
		self.btnSel_Finger2R = QtWidgets.QPushButton('')
		self.btnSel_Finger3R = QtWidgets.QPushButton('')
		self.btnSel_Finger4R = QtWidgets.QPushButton('')

		self.btnSel_FingerAllL = QtWidgets.QPushButton('All Fingers')
		self.btnSel_FingerAllR = QtWidgets.QPushButton('All Fingers')

		self.btnSel_All = QtWidgets.QPushButton('All')

		self.btnSel_Root.setGeometry(151 * self.uiScale.x,547 * self.uiScale.y,72 * self.uiScale.x,16 * self.uiScale.y)
		self.btnSel_Root.setPalette(palette0)
		self.btnSel_Hip.setGeometry(147 * self.uiScale.x,288 * self.uiScale.y,77 * self.uiScale.x,34 * self.uiScale.y)
		self.btnSel_Hip.setPalette(palette1)
		self.btnSel_Waist.setGeometry(162 * self.uiScale.x,256 * self.uiScale.y,46 * self.uiScale.x,30 * self.uiScale.y)
		self.btnSel_Waist.setPalette(palette1)
		# self.btnSel_Waist.setEnabled(False)
		self.btnSel_Chest.setGeometry(147 * self.uiScale.x,198 * self.uiScale.y,77 * self.uiScale.x,56 * self.uiScale.y)
		self.btnSel_Chest.setPalette(palette1)
		# self.btnSel_Chest1.setGeometry(147,198,77,16)
		# self.btnSel_Chest1.setPalette(palette1)
		self.btnSel_Neck.setGeometry(175 * self.uiScale.x,164 * self.uiScale.y,21 * self.uiScale.x,31 * self.uiScale.y)
		# self.btnSel_Neck.setPalette(palette2)
		self.btnSel_Neck.setEnabled(False)
		self.btnSel_Head.setGeometry(160 * self.uiScale.x,98 * self.uiScale.y,51 * self.uiScale.x,63 * self.uiScale.y)
		self.btnSel_Head.setPalette(palette3)
		self.btnSel_ShoulderL.setGeometry(200 * self.uiScale.x,175 * self.uiScale.y,44 * self.uiScale.x,20 * self.uiScale.y)
		self.btnSel_ShoulderL.setPalette(palette4L)
		self.btnSel_ShoulderR.setGeometry(127 * self.uiScale.x,175 * self.uiScale.y,44 * self.uiScale.x,20 * self.uiScale.y)
		self.btnSel_ShoulderR.setPalette(palette4R)
		self.btnSel_FKUpperArmL.setGeometry(247 * self.uiScale.x,175 * self.uiScale.y,22 * self.uiScale.x,89 * self.uiScale.y)
		self.btnSel_FKUpperArmL.setPalette(palette5L)
		self.btnSel_FKUpperArmR.setGeometry(102 * self.uiScale.x,175 * self.uiScale.y,22 * self.uiScale.x,89 * self.uiScale.y)
		self.btnSel_FKUpperArmR.setPalette(palette5R)
		self.btnSel_FKForeArmL.setGeometry(247 * self.uiScale.x,268 * self.uiScale.y,22 * self.uiScale.x,83 * self.uiScale.y)
		self.btnSel_FKForeArmL.setPalette(palette5L)
		self.btnSel_FKForeArmR.setGeometry(102 * self.uiScale.x,268 * self.uiScale.y,22 * self.uiScale.x,83 * self.uiScale.y)
		self.btnSel_FKForeArmR.setPalette(palette5R)
		self.btnSel_FKHandL.setGeometry(240 * self.uiScale.x,354 * self.uiScale.y,38 * self.uiScale.x,44 * self.uiScale.y)
		self.btnSel_FKHandL.setPalette(palette5L)
		self.btnSel_FKHandR.setGeometry(94 * self.uiScale.x,354 * self.uiScale.y,38 * self.uiScale.x,44 * self.uiScale.y)
		self.btnSel_FKHandR.setPalette(palette5R)
		self.btnSel_IKArmUpVL.setGeometry(272 * self.uiScale.x,255 * self.uiScale.y,22 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_IKArmUpVL.setPalette(palette6L)
		self.btnSel_IKArmUpVR.setGeometry(77 * self.uiScale.x,255 * self.uiScale.y,22 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_IKArmUpVR.setPalette(palette6R)
		self.btnSel_IKHandL.setGeometry(281 * self.uiScale.x,354 * self.uiScale.y,22 * self.uiScale.x,44 * self.uiScale.y)
		self.btnSel_IKHandL.setPalette(palette6L)
		self.btnSel_IKHandR.setGeometry(69 * self.uiScale.x,354 * self.uiScale.y,22 * self.uiScale.x,44 * self.uiScale.y)
		self.btnSel_IKHandR.setPalette(palette6R)
		self.btnSel_IKLegUpVL.setGeometry(200 * self.uiScale.x,400 * self.uiScale.y,24 * self.uiScale.x,24 * self.uiScale.y)
		self.btnSel_IKLegUpVL.setPalette(palette6L)
		self.btnSel_IKLegUpVR.setGeometry(147 * self.uiScale.x,400 * self.uiScale.y,24 * self.uiScale.x,24 * self.uiScale.y)
		self.btnSel_IKLegUpVR.setPalette(palette6R)
		self.btnSel_FootL.setGeometry(200 * self.uiScale.x,502 * self.uiScale.y,37 * self.uiScale.x,24 * self.uiScale.y)
		self.btnSel_FootL.setPalette(palette4L)
		self.btnSel_FootR.setGeometry(135 * self.uiScale.x,502 * self.uiScale.y,37 * self.uiScale.x,24 * self.uiScale.y)
		self.btnSel_FootR.setPalette(palette4R)
		self.btnSel_IKLegL.setGeometry(200 * self.uiScale.x,528 * self.uiScale.y,58 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_IKLegL.setPalette(palette4L)
		self.btnSel_IKLegR.setGeometry(114 * self.uiScale.x,528 * self.uiScale.y,58 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_IKLegR.setPalette(palette4R)

		self.btn_ThighL = QtWidgets.QPushButton('')
		self.btn_ThighL.setGeometry(200 * self.uiScale.x,325 * self.uiScale.y,24 * self.uiScale.x,72 * self.uiScale.y)
		self.btn_ThighL.setEnabled(False)
		
		self.btn_CalfL = QtWidgets.QPushButton('')
		self.btn_CalfL.setGeometry(200 * self.uiScale.x,427 * self.uiScale.y,24 * self.uiScale.x,72 * self.uiScale.y)
		self.btn_CalfL.setEnabled(False)
		
		self.btn_ThighR = QtWidgets.QPushButton('')
		self.btn_ThighR.setGeometry(147 * self.uiScale.x,325 * self.uiScale.y,24 * self.uiScale.x,72 * self.uiScale.y)
		self.btn_ThighR.setEnabled(False)
		
		self.btn_CalfR = QtWidgets.QPushButton('')
		self.btn_CalfR.setGeometry(147 * self.uiScale.x,427 * self.uiScale.y,24 * self.uiScale.x,72 * self.uiScale.y)
		self.btn_CalfR.setEnabled(False)

		self.btn_RfHandL = QtWidgets.QPushButton('Left')
		self.btn_RfHandL.setGeometry(280 * self.uiScale.x,514 * self.uiScale.y,63 * self.uiScale.x,60 * self.uiScale.y)
		self.btn_RfHandL.setEnabled(False)
		self.btn_RfHandR = QtWidgets.QPushButton('Right')
		self.btn_RfHandR.setGeometry(28 * self.uiScale.x,514 * self.uiScale.y,63 * self.uiScale.x,60 * self.uiScale.y)
		self.btn_RfHandR.setEnabled(False)
		
		self.btnSel_FingerX4L.setGeometry(280 * self.uiScale.x,411 * self.uiScale.y, 63 * self.uiScale.x, 8 * self.uiScale.y)
		self.btnSel_FingerX4L.setPalette(palette7)
		self.btnSel_FingerX4R.setGeometry(28 * self.uiScale.x,411 * self.uiScale.y, 63 * self.uiScale.x, 8 * self.uiScale.y)
		self.btnSel_FingerX4R.setPalette(palette7)

		self.btnSel_FingerSx2L.setGeometry(258 * self.uiScale.x, 434 * self.uiScale.y, 8 * self.uiScale.x, 49 * self.uiScale.y)
		self.btnSel_FingerSx2L.setPalette(palette7)
		self.btnSel_FingerSx2R.setGeometry(105 * self.uiScale.x, 434 * self.uiScale.y, 8 * self.uiScale.x, 49 * self.uiScale.y)
		self.btnSel_FingerSx2R.setPalette(palette7)

		self.btnSel_FingerS0L.setGeometry(264 * self.uiScale.x,490 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_FingerS0L.setFlat(True)
		self.btnSel_FingerS0L.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_R.png'))
		self.btnSel_FingerS1L.setGeometry(264 * self.uiScale.x,464 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_FingerS1L.setFlat(True)
		self.btnSel_FingerS1L.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_R.png'))
		self.btnSel_FingerS2L.setGeometry(264 * self.uiScale.x,438 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_FingerS2L.setFlat(True)
		self.btnSel_FingerS2L.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_R.png'))

		self.btnSel_FingerS0R.setGeometry(92 * self.uiScale.x,490 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_FingerS0R.setFlat(True)
		self.btnSel_FingerS0R.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_L.png'))
		self.btnSel_FingerS1R.setGeometry(92 * self.uiScale.x,464 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_FingerS1R.setFlat(True)
		self.btnSel_FingerS1R.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_L.png'))
		self.btnSel_FingerS2R.setGeometry(92 * self.uiScale.x,438 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_FingerS2R.setFlat(True)
		self.btnSel_FingerS2R.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_L.png'))

		self.btnSel_Finger0L.setGeometry(347 * self.uiScale.x,460 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_Finger0L.setFlat(True)
		self.btnSel_Finger0L.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger1L.setGeometry(328 * self.uiScale.x,417 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_Finger1L.setFlat(True)
		self.btnSel_Finger1L.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger2L.setGeometry(312 * self.uiScale.x,417 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_Finger2L.setFlat(True)
		self.btnSel_Finger2L.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger3L.setGeometry(296 * self.uiScale.x,417 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_Finger3L.setFlat(True)
		self.btnSel_Finger3L.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger4L.setGeometry(280 * self.uiScale.x,417 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_Finger4L.setFlat(True)
		self.btnSel_Finger4L.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_D.png'))

		self.btnSel_Finger0R.setGeometry(10 * self.uiScale.x,460 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_Finger0R.setFlat(True)
		self.btnSel_Finger0R.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger1R.setGeometry(28 * self.uiScale.x,417 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_Finger1R.setFlat(True)
		self.btnSel_Finger1R.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger2R.setGeometry(44 * self.uiScale.x,417 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_Finger2R.setFlat(True)
		self.btnSel_Finger2R.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger3R.setGeometry(60 * self.uiScale.x,417 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_Finger3R.setFlat(True)
		self.btnSel_Finger3R.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger4R.setGeometry(76 * self.uiScale.x,417 * self.uiScale.y,14 * self.uiScale.x,14 * self.uiScale.y)
		self.btnSel_Finger4R.setFlat(True)
		self.btnSel_Finger4R.setIcon(QtGui.QIcon(usrImgFold+'TriArrow_D.png'))

		self.btnSel_Finger00L.setGeometry(347 * self.uiScale.x,530 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger00L.setPalette(palette6L)
		self.btnSel_Finger01L.setGeometry(347 * self.uiScale.x,504 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger01L.setPalette(palette6L)
		self.btnSel_Finger02L.setGeometry(347 * self.uiScale.x,478 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger02L.setPalette(palette6L)
		self.btnSel_Finger10L.setGeometry(328 * self.uiScale.x,486 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger10L.setPalette(palette6L)
		self.btnSel_Finger11L.setGeometry(328 * self.uiScale.x,460 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger11L.setPalette(palette6L)
		self.btnSel_Finger12L.setGeometry(328 * self.uiScale.x,434 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger12L.setPalette(palette6L)
		self.btnSel_Finger20L.setGeometry(312 * self.uiScale.x,486 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger20L.setPalette(palette6L)
		self.btnSel_Finger21L.setGeometry(312 * self.uiScale.x,460 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger21L.setPalette(palette6L)
		self.btnSel_Finger22L.setGeometry(312 * self.uiScale.x,434 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger22L.setPalette(palette6L)
		self.btnSel_Finger30L.setGeometry(296 * self.uiScale.x,486 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger30L.setPalette(palette6L)
		self.btnSel_Finger31L.setGeometry(296 * self.uiScale.x,460 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger31L.setPalette(palette6L)
		self.btnSel_Finger32L.setGeometry(296 * self.uiScale.x,434 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger32L.setPalette(palette6L)
		self.btnSel_Finger40L.setGeometry(280 * self.uiScale.x,486 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger40L.setPalette(palette6L)
		self.btnSel_Finger41L.setGeometry(280 * self.uiScale.x,460 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger41L.setPalette(palette6L)
		self.btnSel_Finger42L.setGeometry(280 * self.uiScale.x,434 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger42L.setPalette(palette6L)
		
		self.btnSel_Finger00R.setGeometry(10 * self.uiScale.x,530 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger00R.setPalette(palette6R)
		self.btnSel_Finger01R.setGeometry(10 * self.uiScale.x,504 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger01R.setPalette(palette6R)
		self.btnSel_Finger02R.setGeometry(10 * self.uiScale.x,478 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger02R.setPalette(palette6R)
		self.btnSel_Finger10R.setGeometry(28 * self.uiScale.x,486 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger10R.setPalette(palette6R)
		self.btnSel_Finger11R.setGeometry(28 * self.uiScale.x,460 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger11R.setPalette(palette6R)
		self.btnSel_Finger12R.setGeometry(28 * self.uiScale.x,434 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger12R.setPalette(palette6R)
		self.btnSel_Finger20R.setGeometry(44 * self.uiScale.x,486 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger20R.setPalette(palette6R)
		self.btnSel_Finger21R.setGeometry(44 * self.uiScale.x,460 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger21R.setPalette(palette6R)
		self.btnSel_Finger22R.setGeometry(44 * self.uiScale.x,434 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger22R.setPalette(palette6R)
		self.btnSel_Finger30R.setGeometry(60 * self.uiScale.x,486 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger30R.setPalette(palette6R)
		self.btnSel_Finger31R.setGeometry(60 * self.uiScale.x,460 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger31R.setPalette(palette6R)
		self.btnSel_Finger32R.setGeometry(60 * self.uiScale.x,434 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger32R.setPalette(palette6R)
		self.btnSel_Finger40R.setGeometry(76 * self.uiScale.x,486 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger40R.setPalette(palette6R)
		self.btnSel_Finger41R.setGeometry(76 * self.uiScale.x,460 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger41R.setPalette(palette6R)
		self.btnSel_Finger42R.setGeometry(76 * self.uiScale.x,434 * self.uiScale.y,14 * self.uiScale.x,22 * self.uiScale.y)
		self.btnSel_Finger42R.setPalette(palette6R)
		
		self.btnSel_FingerAllL.setGeometry(280 * self.uiScale.x, 576 * self.uiScale.y, 82 * self.uiScale.x, 12 * self.uiScale.y)
		self.btnSel_FingerAllL.setPalette(palette7)
		self.btnSel_FingerAllR.setGeometry(10 * self.uiScale.x, 576 * self.uiScale.y, 82 * self.uiScale.x, 12 * self.uiScale.y)
		self.btnSel_FingerAllR.setPalette(palette7)
		self.btnSel_All.setGeometry(108 * self.uiScale.x,567 * self.uiScale.y,159 * self.uiScale.x,23 * self.uiScale.y)
		self.btnSel_All.setPalette(palette7)

		self.btnAnmConvert2IK = QtWidgets.QPushButton('IK')
		self.btnAnmConvert2IK.setGeometry(67 * self.uiScale.x,23 * self.uiScale.y,32 * self.uiScale.x,32 * self.uiScale.y)
		self.btnAnmConvert2FK = QtWidgets.QPushButton('FK')
		self.btnAnmConvert2FK.setGeometry(104 * self.uiScale.x,23 * self.uiScale.y,32 * self.uiScale.x,32 * self.uiScale.y)
		self.btnPoseConvert2IK = QtWidgets.QPushButton('IK')
		self.btnPoseConvert2IK.setGeometry(67 * self.uiScale.x,60 * self.uiScale.y,32 * self.uiScale.x,32 * self.uiScale.y)
		self.btnPoseConvert2FK = QtWidgets.QPushButton('FK')
		self.btnPoseConvert2FK.setGeometry(104 * self.uiScale.x,60 * self.uiScale.y,32 * self.uiScale.x,32 * self.uiScale.y)

		self.btnGoBindPose = QtWidgets.QPushButton('')
		self.btnGoBindPose.setGeometry(300 * self.uiScale.x,125 * self.uiScale.y,60 * self.uiScale.x,60 * self.uiScale.y)
		self.btnGoBindPose.setIcon(QtGui.QIcon(usrImgFold+'TPose.png'))
		self.btnGoBindPose.setIconSize(QtCore.QSize(60 * self.uiScale.x,60))
		self.btnGoBindPose.setFlat(True)

		self.btnKeyAll = QtWidgets.QPushButton('Key All')
		self.btnKeyAll.setGeometry(8 * self.uiScale.x,38 * self.uiScale.y,84 * self.uiScale.x,48 * self.uiScale.y)
		self.btnKeySel = QtWidgets.QPushButton('Key')
		self.btnKeySel.setGeometry(97 * self.uiScale.x,38 * self.uiScale.y,48 * self.uiScale.x,48 * self.uiScale.y)
		self.btnDelKeySel = QtWidgets.QPushButton('Del\nKey')
		self.btnDelKeySel.setGeometry(150 * self.uiScale.x,38 * self.uiScale.y,48 * self.uiScale.x,48 * self.uiScale.y)
		self.btnDelAllAnm = QtWidgets.QPushButton('Del All\nAnimation')
		self.btnDelAllAnm.setGeometry(8 * self.uiScale.x,92 * self.uiScale.y,84 * self.uiScale.x,30 * self.uiScale.y)
		self.btnDelAnm = QtWidgets.QPushButton('Del\nAnim')
		self.btnDelAnm.setGeometry(97 * self.uiScale.x,92 * self.uiScale.y,48 * self.uiScale.x,30 * self.uiScale.y)

		#-------------------------------------------------------------
		self.btnExpAnmBrowse = QtWidgets.QPushButton("...")
		self.btnExpAnm = QtWidgets.QPushButton("Export")
		self.btnExpAnmMirror = QtWidgets.QPushButton("Mirror Export")
		self.btnImpAnm = QtWidgets.QPushButton("Import")


		self.btnExpPoseBrowse = QtWidgets.QPushButton("...")
		self.btnExpPose = QtWidgets.QPushButton("Export")
		self.btnExpPoseMirror = QtWidgets.QPushButton("Mirror Export")
		self.btnImpPose = QtWidgets.QPushButton("Import")

	def create_layout(self):
		baseLayout = QtWidgets.QVBoxLayout(self)
		tabWidget = QtWidgets.QTabWidget()
		baseLayout.addWidget(tabWidget)
		#-----------------------------
		select_tab = QtWidgets.QWidget()
		tabWidget.addTab(select_tab, "選擇工具")
		tabWidget.currentChanged.connect(self.doChageTab)

		grpIKFKConvert = QtWidgets.QGroupBox('Arm IK/FK Convert', select_tab)
		grpIKFKConvert.setGeometry(225 * self.uiScale.x,9 * self.uiScale.y,143 * self.uiScale.x,98 * self.uiScale.y)

		lbIFAnm = QtWidgets.QLabel('Animation', grpIKFKConvert)
		lbIFAnm.setGeometry(5 * self.uiScale.x,31 * self.uiScale.y,54 * self.uiScale.x,20 * self.uiScale.y)
		lbIFAnm.setAlignment(QtCore.Qt.AlignRight)

		lbIFPose = QtWidgets.QLabel('Pose', grpIKFKConvert)
		lbIFPose.setGeometry(5 * self.uiScale.x,68 * self.uiScale.y,54 * self.uiScale.x,20 * self.uiScale.y)
		lbIFPose.setAlignment(QtCore.Qt.AlignRight)

		lbGoBindPose = QtWidgets.QLabel('Bind Pose', select_tab)
		lbGoBindPose.setGeometry(305 * self.uiScale.x,185 * self.uiScale.y,62 * self.uiScale.x,12 * self.uiScale.y)

		self.btnAnmConvert2IK.setParent(grpIKFKConvert)
		self.btnAnmConvert2FK.setParent(grpIKFKConvert)
		self.btnPoseConvert2IK.setParent(grpIKFKConvert)
		self.btnPoseConvert2FK.setParent(grpIKFKConvert)

		self.btnGoBindPose.setParent(select_tab)
		self.btnKeyAll.setParent(select_tab)
		self.btnKeySel.setParent(select_tab)
		self.btnDelKeySel.setParent(select_tab)
		self.btnDelAllAnm.setParent(select_tab)
		self.btnDelAnm.setParent(select_tab)

		# self.cbbNameSpace.setParent(select_tab)
		# self.btnRefreshNameSpace.setParent(select_tab)
		
		self.btnSel_Root.setParent(select_tab)
		self.btnSel_Hip.setParent(select_tab)
		self.btnSel_Waist.setParent(select_tab)
		self.btnSel_Chest.setParent(select_tab)
		# self.btnSel_Chest1.setParent(select_tab)
		self.btnSel_Neck.setParent(select_tab)
		self.btnSel_Head.setParent(select_tab)
		self.btnSel_ShoulderL.setParent(select_tab)
		self.btnSel_ShoulderR.setParent(select_tab)
		self.btnSel_FKUpperArmL.setParent(select_tab)
		self.btnSel_FKUpperArmR.setParent(select_tab)
		self.btnSel_FKForeArmL.setParent(select_tab)
		self.btnSel_FKForeArmR.setParent(select_tab)
		self.btnSel_FKHandL.setParent(select_tab)
		self.btnSel_FKHandR.setParent(select_tab)
		self.btnSel_IKArmUpVL.setParent(select_tab)
		self.btnSel_IKArmUpVR.setParent(select_tab)
		self.btnSel_IKHandL.setParent(select_tab)
		self.btnSel_IKHandR.setParent(select_tab)
		self.btnSel_IKLegUpVL.setParent(select_tab)
		self.btnSel_IKLegUpVR.setParent(select_tab)
		self.btnSel_FootL.setParent(select_tab)
		self.btnSel_FootR.setParent(select_tab)
		self.btnSel_IKLegL.setParent(select_tab)
		self.btnSel_IKLegR.setParent(select_tab)
		
		self.btn_ThighL.setParent(select_tab)
		self.btn_CalfL.setParent(select_tab)
		self.btn_ThighR.setParent(select_tab)
		self.btn_CalfR.setParent(select_tab)
		#---
		self.btn_RfHandL.setParent(select_tab)
		self.btn_RfHandR.setParent(select_tab)
		
		self.btnSel_FingerX4L.setParent(select_tab)
		self.btnSel_FingerX4R.setParent(select_tab)

		self.btnSel_FingerSx2L.setParent(select_tab)
		self.btnSel_FingerSx2R.setParent(select_tab)

		self.btnSel_FingerS0L.setParent(select_tab)
		self.btnSel_FingerS1L.setParent(select_tab)
		self.btnSel_FingerS2L.setParent(select_tab)

		self.btnSel_FingerS0R.setParent(select_tab)
		self.btnSel_FingerS1R.setParent(select_tab)
		self.btnSel_FingerS2R.setParent(select_tab)

		self.btnSel_FingerAllL.setParent(select_tab)
		self.btnSel_FingerAllR.setParent(select_tab)

		self.btnSel_Finger0L.setParent(select_tab)
		self.btnSel_Finger1L.setParent(select_tab)
		self.btnSel_Finger2L.setParent(select_tab)
		self.btnSel_Finger3L.setParent(select_tab)
		self.btnSel_Finger4L.setParent(select_tab)
		self.btnSel_Finger0R.setParent(select_tab)
		self.btnSel_Finger1R.setParent(select_tab)
		self.btnSel_Finger2R.setParent(select_tab)
		self.btnSel_Finger3R.setParent(select_tab)
		self.btnSel_Finger4R.setParent(select_tab)

		self.btnSel_Finger00L.setParent(select_tab)
		self.btnSel_Finger01L.setParent(select_tab)
		self.btnSel_Finger02L.setParent(select_tab)
		self.btnSel_Finger10L.setParent(select_tab)
		self.btnSel_Finger11L.setParent(select_tab)
		self.btnSel_Finger12L.setParent(select_tab)
		self.btnSel_Finger20L.setParent(select_tab)
		self.btnSel_Finger21L.setParent(select_tab)
		self.btnSel_Finger22L.setParent(select_tab)
		self.btnSel_Finger30L.setParent(select_tab)
		self.btnSel_Finger31L.setParent(select_tab)
		self.btnSel_Finger32L.setParent(select_tab)
		self.btnSel_Finger40L.setParent(select_tab)
		self.btnSel_Finger41L.setParent(select_tab)
		self.btnSel_Finger42L.setParent(select_tab)
		
		self.btnSel_Finger00R.setParent(select_tab)
		self.btnSel_Finger01R.setParent(select_tab)
		self.btnSel_Finger02R.setParent(select_tab)
		self.btnSel_Finger10R.setParent(select_tab)
		self.btnSel_Finger11R.setParent(select_tab)
		self.btnSel_Finger12R.setParent(select_tab)
		self.btnSel_Finger20R.setParent(select_tab)
		self.btnSel_Finger21R.setParent(select_tab)
		self.btnSel_Finger22R.setParent(select_tab)
		self.btnSel_Finger30R.setParent(select_tab)
		self.btnSel_Finger31R.setParent(select_tab)
		self.btnSel_Finger32R.setParent(select_tab)
		self.btnSel_Finger40R.setParent(select_tab)
		self.btnSel_Finger41R.setParent(select_tab)
		self.btnSel_Finger42R.setParent(select_tab)

		self.btnSel_All.setParent(select_tab)
		# btnTest = QtWidgets.QPushButton('測試')
		# btnTest.setParent(select_tab)
		# btnTest.move(20,20)
		# btnTest.clicked.connect(self.doTest)

		#------------------------------
		save_tab = QtWidgets.QWidget()
		tabWidget.addTab(save_tab, "動作記錄")

		gpAnimation = QtWidgets.QGroupBox('Animation Rec.', save_tab)
		gpAnimation.setGeometry(9 * self.uiScale.x,9 * self.uiScale.y,278 * self.uiScale.x,110 * self.uiScale.y)

		self.exportAnimPath_edit.setParent(gpAnimation)
		self.exportAnimPath_edit.setGeometry(9 * self.uiScale.x,19 * self.uiScale.y,240 * self.uiScale.x,20 * self.uiScale.y)
		
		self.btnExpAnmBrowse.setParent(gpAnimation)
		self.btnExpAnmBrowse.setGeometry(253 * self.uiScale.x,19 * self.uiScale.y,20 * self.uiScale.x,20 * self.uiScale.y)

		self.btnExpAnm.setParent(gpAnimation)
		self.btnExpAnm.setGeometry(9 * self.uiScale.x,48 * self.uiScale.y,130 * self.uiScale.x,23 * self.uiScale.y)

		self.btnExpAnmMirror.setParent(gpAnimation)
		self.btnExpAnmMirror.setGeometry(9 * self.uiScale.x,76 * self.uiScale.y,130 * self.uiScale.x,23 * self.uiScale.y)

		self.btnImpAnm.setParent(gpAnimation)
		self.btnImpAnm.setGeometry(144 * self.uiScale.x,48 * self.uiScale.y,126 * self.uiScale.x,51 * self.uiScale.y)

		gpPose = QtWidgets.QGroupBox('Pose Rec.', save_tab)
		gpPose.setGeometry(9 * self.uiScale.x,132 * self.uiScale.y,278 * self.uiScale.x,110 * self.uiScale.y)

		self.exportPosePath_edit.setParent(gpPose)
		self.exportPosePath_edit.setGeometry(9 * self.uiScale.x,19 * self.uiScale.y,240 * self.uiScale.x,20 * self.uiScale.y)
		
		self.btnExpPoseBrowse.setParent(gpPose)
		self.btnExpPoseBrowse.setGeometry(253 * self.uiScale.x,19 * self.uiScale.y,20 * self.uiScale.x,20 * self.uiScale.y)

		self.btnExpPose.setParent(gpPose)
		self.btnExpPose.setGeometry(9 * self.uiScale.x,48 * self.uiScale.y,130 * self.uiScale.x,23 * self.uiScale.y)

		self.btnExpPoseMirror.setParent(gpPose)
		self.btnExpPoseMirror.setGeometry(9 * self.uiScale.x,76 * self.uiScale.y,130 * self.uiScale.x,23 * self.uiScale.y)

		self.btnImpPose.setParent(gpPose)
		self.btnImpPose.setGeometry(144 * self.uiScale.x,48 * self.uiScale.y,126 * self.uiScale.x,51 * self.uiScale.y)

	def create_connection(self):
		self.btnSel_All.clicked.connect(self.onSelectAll)
		self.btnSel_Root.clicked.connect((lambda e="ControlRoot":self.SelectByName(e)))
		self.btnSel_Hip.clicked.connect((lambda e="Ctrl_Hip":self.SelectByName(e)))
		self.btnSel_Waist.clicked.connect((lambda e="Ctrl_Waist":self.SelectByName(e)))
		self.btnSel_Chest.clicked.connect((lambda e="Ctrl_Chest":self.SelectByName(e)))
		self.btnSel_Head.clicked.connect((lambda e="Ctrl_Head":self.SelectByName(e)))
		self.btnSel_ShoulderL.clicked.connect((lambda e="Ctrl_Shoulder_L":self.SelectByName(e)))
		self.btnSel_ShoulderR.clicked.connect((lambda e="Ctrl_Shoulder_R":self.SelectByName(e)))
		self.btnSel_FKUpperArmL.clicked.connect((lambda e="Ctrl_UpperArmFK_L":self.SelectByName(e)))
		self.btnSel_FKUpperArmR.clicked.connect((lambda e="Ctrl_UpperArmFK_R":self.SelectByName(e)))
		self.btnSel_FKForeArmL.clicked.connect((lambda e="Ctrl_ForeArmFK_L":self.SelectByName(e)))
		self.btnSel_FKForeArmR.clicked.connect((lambda e="Ctrl_ForeArmFK_R":self.SelectByName(e)))
		self.btnSel_FKHandL.clicked.connect((lambda e="Ctrl_HandFK_L":self.SelectByName(e)))
		self.btnSel_FKHandR.clicked.connect((lambda e="Ctrl_HandFK_R":self.SelectByName(e)))
		self.btnSel_IKHandL.clicked.connect((lambda e="Ctrl_HandIK_L":self.SelectByName(e)))
		self.btnSel_IKHandR.clicked.connect((lambda e="Ctrl_HandIK_R":self.SelectByName(e)))
		self.btnSel_IKArmUpVL.clicked.connect((lambda e="Ctrl_ArmUpV_L":self.SelectByName(e)))
		self.btnSel_IKArmUpVR.clicked.connect((lambda e="Ctrl_ArmUpV_R":self.SelectByName(e)))
		self.btnSel_IKLegL.clicked.connect((lambda e="Ctrl_Foot_L":self.SelectByName(e)))
		self.btnSel_IKLegR.clicked.connect((lambda e="Ctrl_Foot_R":self.SelectByName(e)))
		self.btnSel_IKLegUpVL.clicked.connect((lambda e="Ctrl_LegUpV_L":self.SelectByName(e)))
		self.btnSel_IKLegUpVR.clicked.connect((lambda e="Ctrl_LegUpV_R":self.SelectByName(e)))
		self.btnSel_FootL.clicked.connect((lambda e="Ctrl_FootPad_L":self.SelectByName(e)))
		self.btnSel_FootR.clicked.connect((lambda e="Ctrl_FootPad_R":self.SelectByName(e)))

		self.btnSel_Finger00L.clicked.connect((lambda e="Ctrl_Finger00_L":self.SelectByName(e)))
		self.btnSel_Finger01L.clicked.connect((lambda e="Ctrl_Finger01_L":self.SelectByName(e)))
		self.btnSel_Finger02L.clicked.connect((lambda e="Ctrl_Finger02_L":self.SelectByName(e)))
		self.btnSel_Finger10L.clicked.connect((lambda e="Ctrl_Finger10_L":self.SelectByName(e)))
		self.btnSel_Finger11L.clicked.connect((lambda e="Ctrl_Finger11_L":self.SelectByName(e)))
		self.btnSel_Finger12L.clicked.connect((lambda e="Ctrl_Finger12_L":self.SelectByName(e)))
		self.btnSel_Finger20L.clicked.connect((lambda e="Ctrl_Finger20_L":self.SelectByName(e)))
		self.btnSel_Finger21L.clicked.connect((lambda e="Ctrl_Finger21_L":self.SelectByName(e)))
		self.btnSel_Finger22L.clicked.connect((lambda e="Ctrl_Finger22_L":self.SelectByName(e)))
		self.btnSel_Finger30L.clicked.connect((lambda e="Ctrl_Finger30_L":self.SelectByName(e)))
		self.btnSel_Finger31L.clicked.connect((lambda e="Ctrl_Finger31_L":self.SelectByName(e)))
		self.btnSel_Finger32L.clicked.connect((lambda e="Ctrl_Finger32_L":self.SelectByName(e)))
		self.btnSel_Finger40L.clicked.connect((lambda e="Ctrl_Finger40_L":self.SelectByName(e)))
		self.btnSel_Finger41L.clicked.connect((lambda e="Ctrl_Finger41_L":self.SelectByName(e)))
		self.btnSel_Finger42L.clicked.connect((lambda e="Ctrl_Finger42_L":self.SelectByName(e)))

		self.btnSel_Finger00R.clicked.connect((lambda e="Ctrl_Finger00_R":self.SelectByName(e)))
		self.btnSel_Finger01R.clicked.connect((lambda e="Ctrl_Finger01_R":self.SelectByName(e)))
		self.btnSel_Finger02R.clicked.connect((lambda e="Ctrl_Finger02_R":self.SelectByName(e)))
		self.btnSel_Finger10R.clicked.connect((lambda e="Ctrl_Finger10_R":self.SelectByName(e)))
		self.btnSel_Finger11R.clicked.connect((lambda e="Ctrl_Finger11_R":self.SelectByName(e)))
		self.btnSel_Finger12R.clicked.connect((lambda e="Ctrl_Finger12_R":self.SelectByName(e)))
		self.btnSel_Finger20R.clicked.connect((lambda e="Ctrl_Finger20_R":self.SelectByName(e)))
		self.btnSel_Finger21R.clicked.connect((lambda e="Ctrl_Finger21_R":self.SelectByName(e)))
		self.btnSel_Finger22R.clicked.connect((lambda e="Ctrl_Finger22_R":self.SelectByName(e)))
		self.btnSel_Finger30R.clicked.connect((lambda e="Ctrl_Finger30_R":self.SelectByName(e)))
		self.btnSel_Finger31R.clicked.connect((lambda e="Ctrl_Finger31_R":self.SelectByName(e)))
		self.btnSel_Finger32R.clicked.connect((lambda e="Ctrl_Finger32_R":self.SelectByName(e)))
		self.btnSel_Finger40R.clicked.connect((lambda e="Ctrl_Finger40_R":self.SelectByName(e)))
		self.btnSel_Finger41R.clicked.connect((lambda e="Ctrl_Finger41_R":self.SelectByName(e)))
		self.btnSel_Finger42R.clicked.connect((lambda e="Ctrl_Finger42_R":self.SelectByName(e)))

		listFinger0L = ["Ctrl_Finger00_L","Ctrl_Finger01_L","Ctrl_Finger02_L"]
		listFinger1L = ["Ctrl_Finger10_L","Ctrl_Finger11_L","Ctrl_Finger12_L"]
		listFinger2L = ["Ctrl_Finger20_L","Ctrl_Finger21_L","Ctrl_Finger22_L"]
		listFinger3L = ["Ctrl_Finger30_L","Ctrl_Finger31_L","Ctrl_Finger32_L"]
		listFinger4L = ["Ctrl_Finger40_L","Ctrl_Finger41_L","Ctrl_Finger42_L"]

		listFinger0R = ["Ctrl_Finger00_R","Ctrl_Finger01_R","Ctrl_Finger02_R"]
		listFinger1R = ["Ctrl_Finger10_R","Ctrl_Finger11_R","Ctrl_Finger12_R"]
		listFinger2R = ["Ctrl_Finger20_R","Ctrl_Finger21_R","Ctrl_Finger22_R"]
		listFinger3R = ["Ctrl_Finger30_R","Ctrl_Finger31_R","Ctrl_Finger32_R"]
		listFinger4R = ["Ctrl_Finger40_R","Ctrl_Finger41_R","Ctrl_Finger42_R"]

		listFingerS0L = ["Ctrl_Finger10_L","Ctrl_Finger20_L","Ctrl_Finger30_L","Ctrl_Finger40_L"]
		listFingerS1L = ["Ctrl_Finger11_L","Ctrl_Finger21_L","Ctrl_Finger31_L","Ctrl_Finger41_L"]
		listFingerS2L = ["Ctrl_Finger12_L","Ctrl_Finger22_L","Ctrl_Finger32_L","Ctrl_Finger42_L"]

		listFingerS0R = ["Ctrl_Finger10_R","Ctrl_Finger20_R","Ctrl_Finger30_R","Ctrl_Finger40_R"]
		listFingerS1R = ["Ctrl_Finger11_R","Ctrl_Finger21_R","Ctrl_Finger31_R","Ctrl_Finger41_R"]
		listFingerS2R = ["Ctrl_Finger12_R","Ctrl_Finger22_R","Ctrl_Finger32_R","Ctrl_Finger42_R"]

		self.btnSel_Finger0L.clicked.connect((lambda e=listFinger0L:self.SelectByName(e)))
		self.btnSel_Finger1L.clicked.connect((lambda e=listFinger1L:self.SelectByName(e)))
		self.btnSel_Finger2L.clicked.connect((lambda e=listFinger2L:self.SelectByName(e)))
		self.btnSel_Finger3L.clicked.connect((lambda e=listFinger3L:self.SelectByName(e)))
		self.btnSel_Finger4L.clicked.connect((lambda e=listFinger4L:self.SelectByName(e)))
		self.btnSel_FingerS0L.clicked.connect((lambda e=listFingerS0L:self.SelectByName(e)))
		self.btnSel_FingerS1L.clicked.connect((lambda e=listFingerS1L:self.SelectByName(e)))
		self.btnSel_FingerS2L.clicked.connect((lambda e=listFingerS2L:self.SelectByName(e)))
		self.btnSel_FingerX4L.clicked.connect((lambda e=(listFinger1L+listFinger2L+listFinger3L+listFinger4L):self.SelectByName(e)))
		self.btnSel_FingerAllL.clicked.connect((lambda e=(listFinger0L+listFinger1L+listFinger2L+listFinger3L+listFinger4L):self.SelectByName(e)))
		self.btnSel_FingerSx2L.clicked.connect((lambda e=(listFingerS1L+listFingerS2L):self.SelectByName(e)))


		self.btnSel_Finger0R.clicked.connect((lambda e=listFinger0R:self.SelectByName(e)))
		self.btnSel_Finger1R.clicked.connect((lambda e=listFinger1R:self.SelectByName(e)))
		self.btnSel_Finger2R.clicked.connect((lambda e=listFinger2R:self.SelectByName(e)))
		self.btnSel_Finger3R.clicked.connect((lambda e=listFinger3R:self.SelectByName(e)))
		self.btnSel_Finger4R.clicked.connect((lambda e=listFinger4R:self.SelectByName(e)))
		self.btnSel_FingerS0R.clicked.connect((lambda e=listFingerS0R:self.SelectByName(e)))
		self.btnSel_FingerS1R.clicked.connect((lambda e=listFingerS1R:self.SelectByName(e)))
		self.btnSel_FingerS2R.clicked.connect((lambda e=listFingerS2R:self.SelectByName(e)))
		self.btnSel_FingerX4R.clicked.connect((lambda e=(listFinger1R+listFinger2R+listFinger3R+listFinger4R):self.SelectByName(e)))
		self.btnSel_FingerAllR.clicked.connect((lambda e=(listFinger0R+listFinger1R+listFinger2R+listFinger3R+listFinger4R):self.SelectByName(e)))
		self.btnSel_FingerSx2R.clicked.connect((lambda e=(listFingerS1R+listFingerS2R):self.SelectByName(e)))
		##------
		self.btnKeyAll.clicked.connect(self.onKeyAll)
		self.btnKeySel.clicked.connect(self.onKeySelect)
		self.btnDelKeySel.clicked.connect(self.onDelKey)
		self.btnDelAllAnm.clicked.connect(self.onDelAllAnimation)
		self.btnDelAnm.clicked.connect(self.onDelSelAnimation)
		self.btnGoBindPose.clicked.connect(self.doSkinPose)
		##########################
		self.exportAnimPath_edit.textChanged.connect(self.onExportAnmPathChanged)
		self.btnExpAnmBrowse.clicked.connect(self.onAnmExpBrowserPressed)
		self.btnExpAnm.clicked.connect(self.doBtnExpAnmPressed)
		self.btnExpAnmMirror.clicked.connect(self.doBtnExpAnmMirrorPressed)
		self.btnImpAnm.clicked.connect(self.doBtnImpAnmPressed)

		self.exportPosePath_edit.textChanged.connect(self.onExportPosePathChanged)
		self.btnExpPoseBrowse.clicked.connect(self.onPoseExpBrowserPressed)
		self.btnExpPose.clicked.connect(self.onBtnExpPosePressed)
		self.btnExpPoseMirror.clicked.connect(self.onBtnExpPoseMirrorPressed)
		self.btnImpPose.clicked.connect(self.onBtnImpPosePressed)

	def doTest(self):
		# select = MaxPlus.SelectionManager.Nodes
		# selList = []

		# for o in select:
		# 	selList.append(o)
		# print(selList)
		# xx = rt.getnodebyname('Sphere001')
		# rt.select(xx)

		# exportAnima("D:/test.kaf", False)
		# for o in select:
		# 	print(o.Transform)
		print(self.RootPath)
		pass

	def doChageTab(self, idx):
		if idx == 0:
			self.setMinimumWidth(400 * self.uiScale.x)
			self.setMaximumWidth(400 * self.uiScale.x)
			self.setMinimumHeight(640 * self.uiScale.y)
			self.setMaximumHeight(640 * self.uiScale.y)
		elif idx == 1:
			self.setMinimumWidth(320 * self.uiScale.x)
			self.setMaximumWidth(320 * self.uiScale.x)
			self.setMinimumHeight(300 * self.uiScale.y)
			self.setMaximumHeight(300 * self.uiScale.y)

	def onExportAnmPathChanged(self, str):
		maxIni = rt.getMAXIniFile()
		rt.setINISetting(maxIni, 'Directories', 'kafPath', str)

	def onExportPosePathChanged(self, str):
		maxIni = rt.getMAXIniFile()
		rt.setINISetting(maxIni, 'Directories', 'kpfPath', str)

	def doBtnExpAnmPressed(self):
		fileInfo = getFilePathInfo(self.exportAnimPath_edit.text())
		if len(fileInfo[0]) == 0:
			fileInfo[0] = "D:/"
		if len(fileInfo[1]) == 0:
			fileInfo[1] = "Anm"
		if fileInfo[2] != ".kaf":
			fileInfo[2] = ".kaf"
		newFilePath = fileInfo[0] + fileInfo[1] + fileInfo[2]
		newFilePath = newFilePath.encode('utf-8')
		self.exportAnimPath_edit.setText(newFilePath)
		exportAnima(newFilePath, False)

	def doBtnExpAnmMirrorPressed(self):
		fileInfo = getFilePathInfo(self.exportAnimPath_edit.text())
		if len(fileInfo[0]) == 0:
			fileInfo[0] = "D:/"
		if len(fileInfo[1]) == 0:
			fileInfo[1] = "Anm"
		if fileInfo[2] != ".kaf":
			fileInfo[2] = ".kaf"
		newFilePath = fileInfo[0] + fileInfo[1] + fileInfo[2]
		newFilePath = newFilePath.encode('utf-8')
		self.exportAnimPath_edit.setText(newFilePath)
		exportAnima(newFilePath, True)

	def doBtnImpAnmPressed(self):
		fileInfo = getFilePathInfo(self.exportAnimPath_edit.text())
		if len(fileInfo[0]) == 0:
			fileInfo[0] = "D:/"
		if len(fileInfo[1]) == 0:
			fileInfo[1] = "Anm"
		if fileInfo[2] != ".kaf":
			fileInfo[2] = ".kaf"
		newFilePath = fileInfo[0] + fileInfo[1] + fileInfo[2]
		newFilePath = newFilePath.encode('utf-8')
		self.exportAnimPath_edit.setText(newFilePath)
		importAnima(newFilePath)

	def onAnmExpBrowserPressed(self):
		fPath = rt.getSaveFileName(caption="Save kaf...", types="kaf file(*.kaf)|*.kaf|")
		if fPath:
			self.exportAnimPath_edit.setText(fPath)

	def onPoseExpBrowserPressed(self):
		fPath = rt.getSaveFileName(caption="Save kpf...", types="kpf file(*.kpf)|*.kpf|")
		if fPath:
			self.exportPosePath_edit.setText(fPath)

	def onBtnExpPosePressed(self):
		fileInfo = getFilePathInfo(self.exportPosePath_edit.text())
		if len(fileInfo[0]) == 0:
			fileInfo[0] = "D:/"
		if len(fileInfo[1]) == 0:
			fileInfo[1] = "Pose"
		if fileInfo[2] != ".kpf":
			fileInfo[2] = ".kpf"
		newFilePath = fileInfo[0] + fileInfo[1] + fileInfo[2]
		newFilePath = newFilePath.encode('utf-8')
		self.exportPosePath_edit.setText(newFilePath)
		exportPose(newFilePath, False)
		pass

	def onBtnExpPoseMirrorPressed(self):
		fileInfo = getFilePathInfo(self.exportPosePath_edit.text())
		if len(fileInfo[0]) == 0:
			fileInfo[0] = "D:/"
		if len(fileInfo[1]) == 0:
			fileInfo[1] = "Pose"
		if fileInfo[2] != ".kpf":
			fileInfo[2] = ".kpf"
		newFilePath = fileInfo[0] + fileInfo[1] + fileInfo[2]
		newFilePath = newFilePath.encode('utf-8')
		self.exportPosePath_edit.setText(newFilePath)
		exportPose(newFilePath, True)
		pass

	def onBtnImpPosePressed(self):
		fileInfo = getFilePathInfo(self.exportPosePath_edit.text())
		if len(fileInfo[0]) == 0:
			fileInfo[0] = "D:/"
		if len(fileInfo[1]) == 0:
			fileInfo[1] = "Pose"
		if fileInfo[2] != ".kpf":
			fileInfo[2] = ".kpf"
		newFilePath = fileInfo[0] + fileInfo[1] + fileInfo[2]
		newFilePath = newFilePath.encode('utf-8')
		self.exportPosePath_edit.setText(newFilePath)
		importPose(newFilePath)
		pass

	def onKeyAll(self):
		count = MaxPlus.LayerManager.GetNumLayers ()

		vLayer = None
		bKeepGo = False
		for i in range(count):
			# print(MaxPlus.LayerManager.GetLayer(i).GetName())
			if MaxPlus.LayerManager.GetLayer(i).GetName() == 'Controller':
				vLayer = MaxPlus.LayerManager.GetLayer(i)
				# print(vLayer.Name)
				# print(vLayer.GetName())
				bKeepGo = True
				break

		if bKeepGo:
			for i in range(vLayer.GetNodes().GetCount()):
				obj = rt.getNodeByName(vLayer.GetNodes().GetItem(i).GetName())
				if obj != None:
					posCtrl = rt.getPropertyController(obj.controller, "position")
					rotCtrl = rt.getPropertyController(obj.controller, "rotation")
					rt.addNewKey(posCtrl, rt.currentTime)
					rt.addNewKey(rotCtrl, rt.currentTime)


			# addNewKey 	

	def onKeySelect(self):
		selList = rt.selection
		for o in selList:
			posCtrl = rt.getPropertyController(o.controller, "position")
			rotCtrl = rt.getPropertyController(o.controller, "rotation")
			rt.addNewKey(posCtrl, rt.currentTime)
			rt.addNewKey(rotCtrl, rt.currentTime)

	def onDelKey(self):
		# selectKeys $.rotation.controller currentTime currentTime
		# deleteKeys <controller> [#allKeys | #selection
		selList = rt.selection
		for o in selList:
			posCtrl = rt.getPropertyController(o.controller, "position")
			rotCtrl = rt.getPropertyController(o.controller, "rotation")
			rt.selectKeys(posCtrl,  rt.currentTime ,rt.currentTime)
			MaxPlus.Core.EvalMAXScript('deleteKeys $'+ o.name +'.position.controller #selection')
			rt.selectKeys(rotCtrl,  rt.currentTime ,rt.currentTime)
			MaxPlus.Core.EvalMAXScript('deleteKeys $'+ o.name +'.rotation.controller #selection')

	def onDelSelAnimation(self):
		selList = rt.selection
		for o in selList:
			posCtrl = rt.getPropertyController(o.controller, "position")
			rotCtrl = rt.getPropertyController(o.controller, "rotation")
			# rt.selectKeys(posCtrl,  rt.currentTime ,rt.currentTime)
			MaxPlus.Core.EvalMAXScript('deleteKeys $'+ o.name +'.position.controller #allKeys')
			# rt.selectKeys(rotCtrl,  rt.currentTime ,rt.currentTime)
			MaxPlus.Core.EvalMAXScript('deleteKeys $'+ o.name +'.rotation.controller #allKeys')

	def onDelAllAnimation(self):
		# allKeys 
		count = MaxPlus.LayerManager.GetNumLayers ()

		vLayer = None
		bKeepGo = False
		for i in range(count):
			if MaxPlus.LayerManager.GetLayer(i).GetName() == 'Controller':
				vLayer = MaxPlus.LayerManager.GetLayer(i)
				bKeepGo = True
				break

		if bKeepGo:
			for i in range(vLayer.GetNodes().GetCount()):
				obj = rt.getNodeByName(vLayer.GetNodes().GetItem(i).GetName())
				if obj != None:
					posCtrl = rt.getPropertyController(obj.controller, "position")
					rotCtrl = rt.getPropertyController(obj.controller, "rotation")
					# rt.selectKeys(posCtrl,  rt.currentTime ,rt.currentTime)
					MaxPlus.Core.EvalMAXScript('deleteKeys $'+ obj.name +'.position.controller #allKeys')
					# rt.selectKeys(rotCtrl,  rt.currentTime ,rt.currentTime)
					MaxPlus.Core.EvalMAXScript('deleteKeys $'+ obj.name +'.rotation.controller #allKeys')

	def doSkinPose(self):
		count = MaxPlus.LayerManager.GetNumLayers ()

		vLayer = None
		bKeepGo = False
		for i in range(count):
			if MaxPlus.LayerManager.GetLayer(i).GetName() == 'Controller':
				vLayer = MaxPlus.LayerManager.GetLayer(i)
				bKeepGo = True
				break

		if bKeepGo:
			for i in range(vLayer.GetNodes().GetCount()):
				obj = rt.getNodeByName(vLayer.GetNodes().GetItem(i).GetName())
				if obj != None:
					obj.assumeSkinPose()
			rt.redrawViews()


	def onSelectAll(self):
		layer = rt.LayerManager.getLayerFromName('Controller')
		layer.select(True)
		rt.redrawViews()

	def SelectByName(self, name):
		if type(name)==str:
			obj = rt.getNodeByName(name)

			if rt.keyboard.controlPressed:
				rt.selectMore(obj)
			elif rt.keyboard.shiftPressed:
				rt.deselect(obj)
			else:
				rt.select(obj)
		elif type(name)==list:
			objs = []
			for n in name:
				obj = rt.getNodeByName(n)
				if obj != None:
					objs.append(obj)
			if rt.keyboard.controlPressed:
				rt.selectMore(objs)
			elif rt.keyboard.shiftPressed:
				rt.deselect(objs)
			else:
				rt.select(objs)
			pass

		rt.redrawViews()

if __name__ == "__main__":
	kAnim_ui = KAnimTools()