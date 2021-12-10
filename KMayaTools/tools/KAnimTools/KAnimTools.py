# -*- coding: utf-8 -*-
import maya.cmds as cmds
import inspect

if int(cmds.about(version=True)) >= 2017:
	import PySide2.QtCore as QtCore
	import PySide2.QtWidgets as QtGui
	import PySide2.QtGui as QGui
	from shiboken2 import wrapInstance
else:
	import PySide.QtCore as QtCore
	import PySide.QtGui as QtGui
	import PySide.QtGui as QGui
	from shiboken import wrapInstance

from collections import OrderedDict

import json
import math

from Transform import *

import maya.OpenMayaUI as omui
import maya.mel as mel
import os

pi = 3.14159265359

def radByAngle(angle):
	return angle / 180.0 * pi

def distance(A, B):
	sqX = (A[0] - B[0])*(A[0] - B[0])
	sqY = (A[1] - B[1])*(A[1] - B[1])
	sqZ = (A[2] - B[2])*(A[2] - B[2])
	return math.sqrt(sqX + sqY + sqZ)

def getFilePathInfo(fullPath):
	DiskPath, fullFileName = os.path.split(fullPath)
	FileName, FileType = os.path.splitext(fullFileName)
	
	if DiskPath[-1] != '/':
		DiskPath += '/'

	return [DiskPath,FileName,FileType]

def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(long(main_window_ptr), QtGui.QWidget)

class KAnimTools(QtGui.QDialog):
	exportPath_edit = QtGui.QLineEdit("D:/Anm.kaf")
	exportPosePath_edit = QtGui.QLineEdit("D:/Pose.kpf")

	NameSpace = ''

	cbbNameSpace = QtGui.QComboBox()
	btnRefreshNameSpace = QtGui.QPushButton('')
	
	btnSel_Root = QtGui.QPushButton('Root')
	btnSel_Hip = QtGui.QPushButton('')
	btnSel_Waist = QtGui.QPushButton('')
	btnSel_Chest = QtGui.QPushButton('')
	btnSel_Chest1 = QtGui.QPushButton('')
	btnSel_Neck = QtGui.QPushButton('')
	btnSel_Head = QtGui.QPushButton('')
	btnSel_ShoulderL = QtGui.QPushButton('')
	btnSel_ShoulderR = QtGui.QPushButton('')
	btnSel_FKUpperArmL = QtGui.QPushButton('FK')
	btnSel_FKUpperArmR = QtGui.QPushButton('FK')
	btnSel_FKForeArmL = QtGui.QPushButton('FK')
	btnSel_FKForeArmR = QtGui.QPushButton('FK')
	btnSel_FKHandL = QtGui.QPushButton('FK')
	btnSel_FKHandR = QtGui.QPushButton('FK')
	btnSel_IKArmUpVL = QtGui.QPushButton('IK')
	btnSel_IKArmUpVR = QtGui.QPushButton('IK')
	btnSel_IKHandL = QtGui.QPushButton('IK')
	btnSel_IKHandR = QtGui.QPushButton('IK')
	btnSel_IKLegUpVL = QtGui.QPushButton('IK')
	btnSel_IKLegUpVR = QtGui.QPushButton('IK')
	btnSel_IKLegL = QtGui.QPushButton('IK')
	btnSel_IKLegR = QtGui.QPushButton('IK')
	btnSel_FootL = QtGui.QPushButton('')
	btnSel_FootR = QtGui.QPushButton('')
	
	btnSel_Finger00L = QtGui.QPushButton('')
	btnSel_Finger01L = QtGui.QPushButton('')
	btnSel_Finger02L = QtGui.QPushButton('')
	btnSel_Finger10L = QtGui.QPushButton('')
	btnSel_Finger11L = QtGui.QPushButton('')
	btnSel_Finger12L = QtGui.QPushButton('')
	btnSel_Finger20L = QtGui.QPushButton('')
	btnSel_Finger21L = QtGui.QPushButton('')
	btnSel_Finger22L = QtGui.QPushButton('')
	btnSel_Finger30L = QtGui.QPushButton('')
	btnSel_Finger31L = QtGui.QPushButton('')
	btnSel_Finger32L = QtGui.QPushButton('')
	btnSel_Finger40L = QtGui.QPushButton('')
	btnSel_Finger41L = QtGui.QPushButton('')
	btnSel_Finger42L = QtGui.QPushButton('')
	btnSel_Finger00R = QtGui.QPushButton('')
	btnSel_Finger01R = QtGui.QPushButton('')
	btnSel_Finger02R = QtGui.QPushButton('')
	btnSel_Finger10R = QtGui.QPushButton('')
	btnSel_Finger11R = QtGui.QPushButton('')
	btnSel_Finger12R = QtGui.QPushButton('')
	btnSel_Finger20R = QtGui.QPushButton('')
	btnSel_Finger21R = QtGui.QPushButton('')
	btnSel_Finger22R = QtGui.QPushButton('')
	btnSel_Finger30R = QtGui.QPushButton('')
	btnSel_Finger31R = QtGui.QPushButton('')
	btnSel_Finger32R = QtGui.QPushButton('')
	btnSel_Finger40R = QtGui.QPushButton('')
	btnSel_Finger41R = QtGui.QPushButton('')
	btnSel_Finger42R = QtGui.QPushButton('')

	btnSel_FingerX4L = QtGui.QPushButton('')
	btnSel_FingerX4R = QtGui.QPushButton('')
	btnSel_FingerS0L = QtGui.QPushButton('')
	btnSel_FingerS1L = QtGui.QPushButton('')
	btnSel_FingerS2L = QtGui.QPushButton('')
	btnSel_FingerS0R = QtGui.QPushButton('')
	btnSel_FingerS1R = QtGui.QPushButton('')
	btnSel_FingerS2R = QtGui.QPushButton('')
	btnSel_FingerSx2L = QtGui.QPushButton('')
	btnSel_FingerSx2R = QtGui.QPushButton('')

	btnSel_Finger0L = QtGui.QPushButton('')
	btnSel_Finger1L = QtGui.QPushButton('')
	btnSel_Finger2L = QtGui.QPushButton('')
	btnSel_Finger3L = QtGui.QPushButton('')
	btnSel_Finger4L = QtGui.QPushButton('')
	btnSel_Finger0R = QtGui.QPushButton('')
	btnSel_Finger1R = QtGui.QPushButton('')
	btnSel_Finger2R = QtGui.QPushButton('')
	btnSel_Finger3R = QtGui.QPushButton('')
	btnSel_Finger4R = QtGui.QPushButton('')

	btnSel_FingerAllL = QtGui.QPushButton('All Fingers')
	btnSel_FingerAllR = QtGui.QPushButton('All Fingers')

	btnSel_All = QtGui.QPushButton('All')

	def __init__(self, parent=maya_main_window()):
		self.closeExistingWindow()
		super(KAnimTools, self).__init__(parent)
		self.create()
		
	def __del__(self):
		pass
		
	def closeExistingWindow(self):
		try:
			for qt in maya_main_window().findChildren(QtGui.QDialog):
				if qt.__class__.__name__ == self.__class__.__name__:
					qt.close()
					qt.deleteLater()
		except:
			pass

	def create(self):
		self.setWindowTitle('K Anim Tools v1.0')
		self.setWindowFlags(QtCore.Qt.Tool)
		self.setMinimumSize(400,640)
		self.setMaximumSize(400,640)
		
		# palette1 = QtGui.QPalette()
		# palette1.setColor(self.backgroundRole(), QColor(192,253,123))
		# palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('../../../Document/images/17_big.jpg')))
		
		self.create_controls()
		self.create_layout()
		self.readConfig()
		self.create_connect()
		self.show()
		self.UpdateRigNS()
	
	def readConfig(self):
		## Default Value ##
		kafPath = 'D:/Anm.kaf'
		kpfPath = 'D:/Pose.kpf'
		try:
			if not cmds.optionVar( exists='KM_KAnm_KafPath' ):
				cmds.optionVar(sv = ('KM_KAnm_KafPath', kafPath))
			else:
				kafPath = cmds.optionVar(q='KM_KAnm_KafPath')
			
			if not cmds.optionVar( exists='KM_KAnm_KpfPath' ):
				cmds.optionVar(sv = ('KM_KAnm_KpfPath', kpfPath))
			else:
				kpfPath = cmds.optionVar(q='KM_KAnm_KpfPath')
		except:
			pass

		self.exportPath_edit.setText(kafPath)
		self.exportPosePath_edit.setText(kpfPath)

	def create_controls(self):
		# btnCreateJoint = QtGui.QPushButton('Create Bones')
		# btnCreateJoint.setToolTip
		# self.btnCreateJoint.move(100,200)
		# self.btnCreateJoint.setPalette(QtGui.QPalette(QtGui.QColor(0,253,123)))
		usd = cmds.internalVar(usd=True)
		usrFold = usd[:-8]
		usrPlugFold = usrFold+"plugins/"
		usrScrptFold = usrFold+"scripts/"
		usrImgFold = usrFold+"prefs/icons/"
		#--------------------------------------------------
		palette0 = QGui.QPalette(QGui.QColor(32,234,75))
		palette1 = QGui.QPalette(QGui.QColor(41,126,185))
		palette2 = QGui.QPalette(QGui.QColor(61,171,140))
		palette3 = QGui.QPalette(QGui.QColor(176,146,55))
		palette4L = QGui.QPalette(QGui.QColor(53,76,160))
		palette4R = QGui.QPalette(QGui.QColor(53,160,81))
		palette5L = QGui.QPalette(QGui.QColor(45,50,118))
		palette5R = QGui.QPalette(QGui.QColor(45,118,60))
		palette6L = QGui.QPalette(QGui.QColor(71,79,196))
		palette6R = QGui.QPalette(QGui.QColor(52,153,74))
		palette7 = QGui.QPalette(QGui.QColor(112,10,10))
		#---------------
		self.cbbNameSpace.setGeometry(6,6,150,22)
		self.btnRefreshNameSpace.setGeometry(160,5,22,22)
		self.btnRefreshNameSpace.setFlat(True)
		self.btnRefreshNameSpace.setIcon(QGui.QIcon(usrImgFold+'reload.png'))
		# self.btnRefreshNameSpace.setIconSize(QtCore.QSize(16,16))
		#---------------
		self.btnSel_Root.setGeometry(151,547,72,16)
		self.btnSel_Root.setPalette(palette0)
		self.btnSel_Hip.setGeometry(147,288,77,34)
		self.btnSel_Hip.setPalette(palette1)
		self.btnSel_Waist.setGeometry(162,260,46,25)
		self.btnSel_Waist.setPalette(palette1)
		self.btnSel_Chest.setGeometry(147,217,77,40)
		self.btnSel_Chest.setPalette(palette1)
		self.btnSel_Chest1.setGeometry(147,198,77,16)
		self.btnSel_Chest1.setPalette(palette1)
		self.btnSel_Neck.setGeometry(175,164,21,31)
		self.btnSel_Neck.setPalette(palette2)
		self.btnSel_Head.setGeometry(160,98,51,63)
		self.btnSel_Head.setPalette(palette3)
		self.btnSel_ShoulderL.setGeometry(200,175,44,20)
		self.btnSel_ShoulderL.setPalette(palette4L)
		self.btnSel_ShoulderR.setGeometry(127,175,44,20)
		self.btnSel_ShoulderR.setPalette(palette4R)
		self.btnSel_FKUpperArmL.setGeometry(247,175,22,89)
		self.btnSel_FKUpperArmL.setPalette(palette5L)
		self.btnSel_FKUpperArmR.setGeometry(102,175,22,89)
		self.btnSel_FKUpperArmR.setPalette(palette5R)
		self.btnSel_FKForeArmL.setGeometry(247,268,22,83)
		self.btnSel_FKForeArmL.setPalette(palette5L)
		self.btnSel_FKForeArmR.setGeometry(102,268,22,83)
		self.btnSel_FKForeArmR.setPalette(palette5R)
		self.btnSel_FKHandL.setGeometry(240,354,38,44)
		self.btnSel_FKHandL.setPalette(palette5L)
		self.btnSel_FKHandR.setGeometry(94,354,38,44)
		self.btnSel_FKHandR.setPalette(palette5R)
		self.btnSel_IKArmUpVL.setGeometry(272,255,22,22)
		self.btnSel_IKArmUpVL.setPalette(palette6L)
		self.btnSel_IKArmUpVR.setGeometry(77,255,22,22)
		self.btnSel_IKArmUpVR.setPalette(palette6R)
		self.btnSel_IKHandL.setGeometry(281,354,22,44)
		self.btnSel_IKHandL.setPalette(palette6L)
		self.btnSel_IKHandR.setGeometry(69,354,22,44)
		self.btnSel_IKHandR.setPalette(palette6R)
		self.btnSel_IKLegUpVL.setGeometry(200,400,24,24)
		self.btnSel_IKLegUpVL.setPalette(palette6L)
		self.btnSel_IKLegUpVR.setGeometry(147,400,24,24)
		self.btnSel_IKLegUpVR.setPalette(palette6R)
		self.btnSel_FootL.setGeometry(200,502,37,24)
		self.btnSel_FootL.setPalette(palette4L)
		self.btnSel_FootR.setGeometry(135,502,37,24)
		self.btnSel_FootR.setPalette(palette4R)
		self.btnSel_IKLegL.setGeometry(200,528,58,14)
		self.btnSel_IKLegL.setPalette(palette4L)
		self.btnSel_IKLegR.setGeometry(114,528,58,14)
		self.btnSel_IKLegR.setPalette(palette4R)
		
		self.btn_ThighL = QtGui.QPushButton('')
		self.btn_ThighL.setGeometry(200,325,24,72)
		self.btn_ThighL.setEnabled(False)
		
		self.btn_CalfL = QtGui.QPushButton('')
		self.btn_CalfL.setGeometry(200,427,24,72)
		self.btn_CalfL.setEnabled(False)
		
		self.btn_ThighR = QtGui.QPushButton('')
		self.btn_ThighR.setGeometry(147,325,24,72)
		self.btn_ThighR.setEnabled(False)
		
		self.btn_CalfR = QtGui.QPushButton('')
		self.btn_CalfR.setGeometry(147,427,24,72)
		self.btn_CalfR.setEnabled(False)
		
		#-------------------
		self.btn_RfHandL = QtGui.QPushButton('Left')
		self.btn_RfHandL.setGeometry(280,514,63,60)
		self.btn_RfHandL.setEnabled(False)
		self.btn_RfHandR = QtGui.QPushButton('Right')
		self.btn_RfHandR.setGeometry(28,514,63,60)
		self.btn_RfHandR.setEnabled(False)
		
		self.btnSel_FingerX4L.setGeometry(280,411, 63, 8)
		self.btnSel_FingerX4L.setPalette(palette7)
		self.btnSel_FingerX4R.setGeometry(28,411, 63, 8)
		self.btnSel_FingerX4R.setPalette(palette7)

		self.btnSel_FingerSx2L.setGeometry(258, 434, 8, 49)
		self.btnSel_FingerSx2L.setPalette(palette7)
		self.btnSel_FingerSx2R.setGeometry(105, 434, 8, 49)
		self.btnSel_FingerSx2R.setPalette(palette7)

		self.btnSel_FingerS0L.setGeometry(264,490,14,14)
		self.btnSel_FingerS0L.setFlat(True)
		self.btnSel_FingerS0L.setIcon(QGui.QIcon(usrImgFold+'TriArrow_R.png'))
		self.btnSel_FingerS1L.setGeometry(264,464,14,14)
		self.btnSel_FingerS1L.setFlat(True)
		self.btnSel_FingerS1L.setIcon(QGui.QIcon(usrImgFold+'TriArrow_R.png'))
		self.btnSel_FingerS2L.setGeometry(264,438,14,14)
		self.btnSel_FingerS2L.setFlat(True)
		self.btnSel_FingerS2L.setIcon(QGui.QIcon(usrImgFold+'TriArrow_R.png'))

		self.btnSel_FingerS0R.setGeometry(92,490,14,14)
		self.btnSel_FingerS0R.setFlat(True)
		self.btnSel_FingerS0R.setIcon(QGui.QIcon(usrImgFold+'TriArrow_L.png'))
		self.btnSel_FingerS1R.setGeometry(92,464,14,14)
		self.btnSel_FingerS1R.setFlat(True)
		self.btnSel_FingerS1R.setIcon(QGui.QIcon(usrImgFold+'TriArrow_L.png'))
		self.btnSel_FingerS2R.setGeometry(92,438,14,14)
		self.btnSel_FingerS2R.setFlat(True)
		self.btnSel_FingerS2R.setIcon(QGui.QIcon(usrImgFold+'TriArrow_L.png'))

		self.btnSel_Finger0L.setGeometry(347,460,14,14)
		self.btnSel_Finger0L.setFlat(True)
		self.btnSel_Finger0L.setIcon(QGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger1L.setGeometry(328,417,14,14)
		self.btnSel_Finger1L.setFlat(True)
		self.btnSel_Finger1L.setIcon(QGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger2L.setGeometry(312,417,14,14)
		self.btnSel_Finger2L.setFlat(True)
		self.btnSel_Finger2L.setIcon(QGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger3L.setGeometry(296,417,14,14)
		self.btnSel_Finger3L.setFlat(True)
		self.btnSel_Finger3L.setIcon(QGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger4L.setGeometry(280,417,14,14)
		self.btnSel_Finger4L.setFlat(True)
		self.btnSel_Finger4L.setIcon(QGui.QIcon(usrImgFold+'TriArrow_D.png'))

		self.btnSel_Finger0R.setGeometry(10,460,14,14)
		self.btnSel_Finger0R.setFlat(True)
		self.btnSel_Finger0R.setIcon(QGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger1R.setGeometry(28,417,14,14)
		self.btnSel_Finger1R.setFlat(True)
		self.btnSel_Finger1R.setIcon(QGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger2R.setGeometry(44,417,14,14)
		self.btnSel_Finger2R.setFlat(True)
		self.btnSel_Finger2R.setIcon(QGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger3R.setGeometry(60,417,14,14)
		self.btnSel_Finger3R.setFlat(True)
		self.btnSel_Finger3R.setIcon(QGui.QIcon(usrImgFold+'TriArrow_D.png'))
		self.btnSel_Finger4R.setGeometry(76,417,14,14)
		self.btnSel_Finger4R.setFlat(True)
		self.btnSel_Finger4R.setIcon(QGui.QIcon(usrImgFold+'TriArrow_D.png'))

		self.btnSel_Finger00L.setGeometry(347,530,14,22)
		self.btnSel_Finger00L.setPalette(palette6L)
		self.btnSel_Finger01L.setGeometry(347,504,14,22)
		self.btnSel_Finger01L.setPalette(palette6L)
		self.btnSel_Finger02L.setGeometry(347,478,14,22)
		self.btnSel_Finger02L.setPalette(palette6L)
		self.btnSel_Finger10L.setGeometry(328,486,14,22)
		self.btnSel_Finger10L.setPalette(palette6L)
		self.btnSel_Finger11L.setGeometry(328,460,14,22)
		self.btnSel_Finger11L.setPalette(palette6L)
		self.btnSel_Finger12L.setGeometry(328,434,14,22)
		self.btnSel_Finger12L.setPalette(palette6L)
		self.btnSel_Finger20L.setGeometry(312,486,14,22)
		self.btnSel_Finger20L.setPalette(palette6L)
		self.btnSel_Finger21L.setGeometry(312,460,14,22)
		self.btnSel_Finger21L.setPalette(palette6L)
		self.btnSel_Finger22L.setGeometry(312,434,14,22)
		self.btnSel_Finger22L.setPalette(palette6L)
		self.btnSel_Finger30L.setGeometry(296,486,14,22)
		self.btnSel_Finger30L.setPalette(palette6L)
		self.btnSel_Finger31L.setGeometry(296,460,14,22)
		self.btnSel_Finger31L.setPalette(palette6L)
		self.btnSel_Finger32L.setGeometry(296,434,14,22)
		self.btnSel_Finger32L.setPalette(palette6L)
		self.btnSel_Finger40L.setGeometry(280,486,14,22)
		self.btnSel_Finger40L.setPalette(palette6L)
		self.btnSel_Finger41L.setGeometry(280,460,14,22)
		self.btnSel_Finger41L.setPalette(palette6L)
		self.btnSel_Finger42L.setGeometry(280,434,14,22)
		self.btnSel_Finger42L.setPalette(palette6L)
		
		self.btnSel_Finger00R.setGeometry(10,530,14,22)
		self.btnSel_Finger00R.setPalette(palette6R)
		self.btnSel_Finger01R.setGeometry(10,504,14,22)
		self.btnSel_Finger01R.setPalette(palette6R)
		self.btnSel_Finger02R.setGeometry(10,478,14,22)
		self.btnSel_Finger02R.setPalette(palette6R)
		self.btnSel_Finger10R.setGeometry(28,486,14,22)
		self.btnSel_Finger10R.setPalette(palette6R)
		self.btnSel_Finger11R.setGeometry(28,460,14,22)
		self.btnSel_Finger11R.setPalette(palette6R)
		self.btnSel_Finger12R.setGeometry(28,434,14,22)
		self.btnSel_Finger12R.setPalette(palette6R)
		self.btnSel_Finger20R.setGeometry(44,486,14,22)
		self.btnSel_Finger20R.setPalette(palette6R)
		self.btnSel_Finger21R.setGeometry(44,460,14,22)
		self.btnSel_Finger21R.setPalette(palette6R)
		self.btnSel_Finger22R.setGeometry(44,434,14,22)
		self.btnSel_Finger22R.setPalette(palette6R)
		self.btnSel_Finger30R.setGeometry(60,486,14,22)
		self.btnSel_Finger30R.setPalette(palette6R)
		self.btnSel_Finger31R.setGeometry(60,460,14,22)
		self.btnSel_Finger31R.setPalette(palette6R)
		self.btnSel_Finger32R.setGeometry(60,434,14,22)
		self.btnSel_Finger32R.setPalette(palette6R)
		self.btnSel_Finger40R.setGeometry(76,486,14,22)
		self.btnSel_Finger40R.setPalette(palette6R)
		self.btnSel_Finger41R.setGeometry(76,460,14,22)
		self.btnSel_Finger41R.setPalette(palette6R)
		self.btnSel_Finger42R.setGeometry(76,434,14,22)
		self.btnSel_Finger42R.setPalette(palette6R)
		
		self.btnSel_FingerAllL.setGeometry(280, 576, 82, 12)
		self.btnSel_FingerAllL.setPalette(palette7)
		self.btnSel_FingerAllR.setGeometry(10, 576, 82, 12)
		self.btnSel_FingerAllR.setPalette(palette7)
		self.btnSel_All.setGeometry(108,567,159,23)
		self.btnSel_All.setPalette(palette7)

		self.btnAnmConvert2IK = QtGui.QPushButton('IK')
		self.btnAnmConvert2FK = QtGui.QPushButton('FK')
		self.btnPoseConvert2IK = QtGui.QPushButton('IK')
		self.btnPoseConvert2FK = QtGui.QPushButton('FK')

		self.btnGoBindPose = QtGui.QPushButton('')
		self.btnGoBindPose.setGeometry(300,125,60,60)
		self.btnGoBindPose.setIcon(QGui.QIcon(usrImgFold+'TPose.png'))
		self.btnGoBindPose.setIconSize(QtCore.QSize(60,60))
		self.btnGoBindPose.setFlat(True)

		self.btnKeyAll = QtGui.QPushButton('Key All')
		self.btnKeyAll.setGeometry(8,38,84,48)
		self.btnKeySel = QtGui.QPushButton('Key')
		self.btnKeySel.setGeometry(97,38,48,48)
		self.btnDelKeySel = QtGui.QPushButton('Del\nKey')
		self.btnDelKeySel.setGeometry(150,38,48,48)
		self.btnDelAllAnm = QtGui.QPushButton('Del All\nAnimation')
		self.btnDelAllAnm.setGeometry(8,92,84,30)
		self.btnDelAnm = QtGui.QPushButton('Del\nAnim')
		self.btnDelAnm.setGeometry(97,92,48,30)

		#================
		self.exportPath_edit.setGeometry(9,19,278,20)
		self.exportPosePath_edit.setGeometry(9,19,278,20)

		self.expBrowse_btn = QtGui.QPushButton("Browse")
		self.expBrowse_btn.setGeometry(291,19,56,20)
		self.expAnm_btn = QtGui.QPushButton("Export")
		self.expAnm_btn.setGeometry(9,48,160,23)
		self.expAnmMirror_btn = QtGui.QPushButton("Mirror Export")
		self.expAnmMirror_btn.setGeometry(9,76,160,23)
		self.impAnm_btn = QtGui.QPushButton("Import")
		self.impAnm_btn.setGeometry(180,48,167,51)
		self.expPoseBrowse_btn = QtGui.QPushButton("Browse")
		self.expPoseBrowse_btn.setGeometry(291,19,56,20)
		self.expPose_btn = QtGui.QPushButton("Export")
		self.expPose_btn.setGeometry(9,48,160,23)
		self.expPoseMirror_btn = QtGui.QPushButton("Mirror Export")
		self.expPoseMirror_btn.setGeometry(9,76,160,23)
		self.impPose_btn = QtGui.QPushButton("Import")
		self.impPose_btn.setGeometry(180,48,167,51)

	def create_layout(self):
		
		baseLayout = QtGui.QVBoxLayout(self)
		
		tabWidget = QtGui.QTabWidget()
		baseLayout.addWidget(tabWidget)
		
		#---------------
		select_tab = QtGui.QWidget()
		tabWidget.addTab(select_tab, "Control Select")
		
		grpIKFKConvert = QtGui.QGroupBox('Arm IK/FK Convert', select_tab)
		grpIKFKConvert.setGeometry(225,9,143,98)

		lbIFAnm = QtGui.QLabel('Animation', grpIKFKConvert)
		lbIFAnm.setGeometry(5,31,54,20)
		lbIFAnm.setAlignment(QtCore.Qt.AlignRight)

		lbIFPose = QtGui.QLabel('Pose', grpIKFKConvert)
		lbIFPose.setGeometry(5,68,54,20)
		lbIFPose.setAlignment(QtCore.Qt.AlignRight)

		self.btnAnmConvert2IK.setGeometry(67,23,32,32)
		self.btnAnmConvert2IK.setParent(grpIKFKConvert)
		self.btnAnmConvert2FK.setGeometry(104,23,32,32)
		self.btnAnmConvert2FK.setParent(grpIKFKConvert)

		self.btnPoseConvert2IK.setGeometry(67,60,32,32)
		self.btnPoseConvert2IK.setParent(grpIKFKConvert)
		self.btnPoseConvert2FK.setGeometry(104,60,32,32)
		self.btnPoseConvert2FK.setParent(grpIKFKConvert)
		#-----------------
		self.btnGoBindPose.setParent(select_tab)

		lbGoBindPose = QtGui.QLabel('Bind Pose', select_tab)
		lbGoBindPose.setGeometry(305,185,62,12)

		self.btnKeyAll.setParent(select_tab)
		self.btnKeySel.setParent(select_tab)
		self.btnDelKeySel.setParent(select_tab)
		self.btnDelAllAnm.setParent(select_tab)
		self.btnDelAnm.setParent(select_tab)
		#-----------------
		self.cbbNameSpace.setParent(select_tab)
		self.btnRefreshNameSpace.setParent(select_tab)
		
		self.btnSel_Root.setParent(select_tab)
		self.btnSel_Hip.setParent(select_tab)
		self.btnSel_Waist.setParent(select_tab)
		self.btnSel_Chest.setParent(select_tab)
		self.btnSel_Chest1.setParent(select_tab)
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
		#=================================================
		facial_tab = QtGui.QWidget()
		tabWidget.addTab(facial_tab, "Facial")
		#=================================================
		AnimRec_tab = QtGui.QWidget()
		tabWidget.addTab(AnimRec_tab, "Anim Rec.")

		gpAnimation = QtGui.QGroupBox('Animation Rec.', AnimRec_tab)
		gpAnimation.setGeometry(9,9,357,110)

		self.exportPath_edit.setParent(gpAnimation)
		self.expBrowse_btn.setParent(gpAnimation)
		self.expAnm_btn.setParent(gpAnimation)
		self.expAnmMirror_btn.setParent(gpAnimation)
		self.impAnm_btn.setParent(gpAnimation)

		gpPose = QtGui.QGroupBox('Pose Rec.', AnimRec_tab)
		gpPose.setGeometry(9,132,357,110)

		self.exportPosePath_edit.setParent(gpPose)
		self.expPoseBrowse_btn.setParent(gpPose)
		self.expPose_btn.setParent(gpPose)
		self.expPoseMirror_btn.setParent(gpPose)
		self.impPose_btn.setParent(gpPose)
	
	def create_connect(self):
		self.btnRefreshNameSpace.clicked.connect(KAnimTools.UpdateRigNS)
		self.cbbNameSpace.currentIndexChanged.connect(KAnimTools.onCcbNSChanged)

		self.btnSel_All.clicked.connect(self.onSelectAll)
		self.btnSel_Root.clicked.connect((lambda e="ControlRoot":self.SelectByName(e)))
		self.btnSel_Hip.clicked.connect((lambda e="Hip":self.SelectByName(e)))
		self.btnSel_Waist.clicked.connect((lambda e="Waist":self.SelectByName(e)))
		self.btnSel_Chest.clicked.connect((lambda e="Chest":self.SelectByName(e)))
		self.btnSel_Chest1.clicked.connect((lambda e="Chest1":self.SelectByName(e)))
		self.btnSel_Neck.clicked.connect((lambda e="Neck":self.SelectByName(e)))
		self.btnSel_Head.clicked.connect((lambda e="Head":self.SelectByName(e)))
		self.btnSel_ShoulderL.clicked.connect((lambda e="Shoulder_L":self.SelectByName(e)))
		self.btnSel_ShoulderR.clicked.connect((lambda e="Shoulder_R":self.SelectByName(e)))
		self.btnSel_FKUpperArmL.clicked.connect((lambda e="FKUpperArm_L":self.SelectByName(e)))
		self.btnSel_FKUpperArmR.clicked.connect((lambda e="FKUpperArm_R":self.SelectByName(e)))
		self.btnSel_FKForeArmL.clicked.connect((lambda e="FKForeArm_L":self.SelectByName(e)))
		self.btnSel_FKForeArmR.clicked.connect((lambda e="FKForeArm_R":self.SelectByName(e)))
		self.btnSel_FKHandL.clicked.connect((lambda e="FKHand_L":self.SelectByName(e)))
		self.btnSel_FKHandR.clicked.connect((lambda e="FKHand_R":self.SelectByName(e)))
		self.btnSel_IKHandL.clicked.connect((lambda e="HandIK_L":self.SelectByName(e)))
		self.btnSel_IKHandR.clicked.connect((lambda e="HandIK_R":self.SelectByName(e)))
		self.btnSel_IKArmUpVL.clicked.connect((lambda e="ArmUpV_L":self.SelectByName(e)))
		self.btnSel_IKArmUpVR.clicked.connect((lambda e="ArmUpV_R":self.SelectByName(e)))
		self.btnSel_IKLegL.clicked.connect((lambda e="Foot_L":self.SelectByName(e)))
		self.btnSel_IKLegR.clicked.connect((lambda e="Foot_R":self.SelectByName(e)))
		self.btnSel_IKLegUpVL.clicked.connect((lambda e="LegUpV_L":self.SelectByName(e)))
		self.btnSel_IKLegUpVR.clicked.connect((lambda e="LegUpV_R":self.SelectByName(e)))
		self.btnSel_FootL.clicked.connect((lambda e="Footpad_L":self.SelectByName(e)))
		self.btnSel_FootR.clicked.connect((lambda e="Footpad_R":self.SelectByName(e)))

		self.btnSel_Finger00L.clicked.connect((lambda e="Finger_00_L":self.SelectByName(e)))
		self.btnSel_Finger01L.clicked.connect((lambda e="Finger_01_L":self.SelectByName(e)))
		self.btnSel_Finger02L.clicked.connect((lambda e="Finger_02_L":self.SelectByName(e)))
		self.btnSel_Finger10L.clicked.connect((lambda e="Finger_10_L":self.SelectByName(e)))
		self.btnSel_Finger11L.clicked.connect((lambda e="Finger_11_L":self.SelectByName(e)))
		self.btnSel_Finger12L.clicked.connect((lambda e="Finger_12_L":self.SelectByName(e)))
		self.btnSel_Finger20L.clicked.connect((lambda e="Finger_20_L":self.SelectByName(e)))
		self.btnSel_Finger21L.clicked.connect((lambda e="Finger_21_L":self.SelectByName(e)))
		self.btnSel_Finger22L.clicked.connect((lambda e="Finger_22_L":self.SelectByName(e)))
		self.btnSel_Finger30L.clicked.connect((lambda e="Finger_30_L":self.SelectByName(e)))
		self.btnSel_Finger31L.clicked.connect((lambda e="Finger_31_L":self.SelectByName(e)))
		self.btnSel_Finger32L.clicked.connect((lambda e="Finger_32_L":self.SelectByName(e)))
		self.btnSel_Finger40L.clicked.connect((lambda e="Finger_40_L":self.SelectByName(e)))
		self.btnSel_Finger41L.clicked.connect((lambda e="Finger_41_L":self.SelectByName(e)))
		self.btnSel_Finger42L.clicked.connect((lambda e="Finger_42_L":self.SelectByName(e)))

		self.btnSel_Finger00R.clicked.connect((lambda e="Finger_00_R":self.SelectByName(e)))
		self.btnSel_Finger01R.clicked.connect((lambda e="Finger_01_R":self.SelectByName(e)))
		self.btnSel_Finger02R.clicked.connect((lambda e="Finger_02_R":self.SelectByName(e)))
		self.btnSel_Finger10R.clicked.connect((lambda e="Finger_10_R":self.SelectByName(e)))
		self.btnSel_Finger11R.clicked.connect((lambda e="Finger_11_R":self.SelectByName(e)))
		self.btnSel_Finger12R.clicked.connect((lambda e="Finger_12_R":self.SelectByName(e)))
		self.btnSel_Finger20R.clicked.connect((lambda e="Finger_20_R":self.SelectByName(e)))
		self.btnSel_Finger21R.clicked.connect((lambda e="Finger_21_R":self.SelectByName(e)))
		self.btnSel_Finger22R.clicked.connect((lambda e="Finger_22_R":self.SelectByName(e)))
		self.btnSel_Finger30R.clicked.connect((lambda e="Finger_30_R":self.SelectByName(e)))
		self.btnSel_Finger31R.clicked.connect((lambda e="Finger_31_R":self.SelectByName(e)))
		self.btnSel_Finger32R.clicked.connect((lambda e="Finger_32_R":self.SelectByName(e)))
		self.btnSel_Finger40R.clicked.connect((lambda e="Finger_40_R":self.SelectByName(e)))
		self.btnSel_Finger41R.clicked.connect((lambda e="Finger_41_R":self.SelectByName(e)))
		self.btnSel_Finger42R.clicked.connect((lambda e="Finger_42_R":self.SelectByName(e)))

		listFinger0L = ["Finger_00_L","Finger_01_L","Finger_02_L"]
		listFinger1L = ["Finger_10_L","Finger_11_L","Finger_12_L"]
		listFinger2L = ["Finger_20_L","Finger_21_L","Finger_22_L"]
		listFinger3L = ["Finger_30_L","Finger_31_L","Finger_32_L"]
		listFinger4L = ["Finger_40_L","Finger_41_L","Finger_42_L"]

		listFinger0R = ["Finger_00_R","Finger_01_R","Finger_02_R"]
		listFinger1R = ["Finger_10_R","Finger_11_R","Finger_12_R"]
		listFinger2R = ["Finger_20_R","Finger_21_R","Finger_22_R"]
		listFinger3R = ["Finger_30_R","Finger_31_R","Finger_32_R"]
		listFinger4R = ["Finger_40_R","Finger_41_R","Finger_42_R"]

		listFingerS0L = ["Finger_10_L","Finger_20_L","Finger_30_L","Finger_40_L"]
		listFingerS1L = ["Finger_11_L","Finger_21_L","Finger_31_L","Finger_41_L"]
		listFingerS2L = ["Finger_12_L","Finger_22_L","Finger_32_L","Finger_42_L"]

		listFingerS0R = ["Finger_10_R","Finger_20_R","Finger_30_R","Finger_40_R"]
		listFingerS1R = ["Finger_11_R","Finger_21_R","Finger_31_R","Finger_41_R"]
		listFingerS2R = ["Finger_12_R","Finger_22_R","Finger_32_R","Finger_42_R"]

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

		self.btnAnmConvert2FK.clicked.connect(self.convertArmAnmIK2FK)
		self.btnAnmConvert2IK.clicked.connect(self.convertArmAnmFK2IK)
		self.btnPoseConvert2FK.clicked.connect(self.onPoseConvert2FKPressed)
		self.btnPoseConvert2IK.clicked.connect(self.onPoseConvert2IKPressed)
		
		self.btnGoBindPose.clicked.connect(self.onGoSkinPoseAllPressed)
		self.btnKeyAll.clicked.connect(self.onKeyAll)
		self.btnKeySel.clicked.connect(self.onKeySelect)
		self.btnDelKeySel.clicked.connect(self.onDelKey)
		self.btnDelAllAnm.clicked.connect(self.onDelAllAnimation)
		self.btnDelAnm.clicked.connect(self.onDelSelAnimation)
		
		#=============================
		self.expBrowse_btn.clicked.connect(self.onExpBrowserPressed)
		self.expPoseBrowse_btn.clicked.connect(self.onPoseBrowserPressed)
		
		self.exportPath_edit.textChanged.connect(self.onExportAnmPathChanged)
		self.exportPosePath_edit.textChanged.connect(self.onExportPosePathChanged)
		
		self.expAnm_btn.clicked.connect(self.onExpAnimaPressed)
		self.expAnmMirror_btn.clicked.connect(self.onExpAnimaMirrorPressed)
		self.impAnm_btn.clicked.connect(self.onImpAnimaPressed)

		self.expPose_btn.clicked.connect(self.onExpPosePressed)
		self.expPoseMirror_btn.clicked.connect(self.onExpPoseMirrorPressed)
		self.impPose_btn.clicked.connect(self.onImpPosePressed)


	def closeEvent(self, event):
		self.deleteLater()
	
	#====================================
	# METHOD
	#====================================
	@classmethod
	def UpdateRigNS(self):
		self.cbbNameSpace.clear()

		if cmds.objExists('ControlRoot'):
			self.cbbNameSpace.insertItem(-1,'--')
			self.NameSpace = ''

		listNameSpace = cmds.namespaceInfo(lon=True, recurse=True)
		for ns in listNameSpace:
			if cmds.objExists(ns+':ControlRoot'):
				self.cbbNameSpace.insertItem(-1,ns+':')
				self.NameSpace = ns+':'
		
	@classmethod
	def onCcbNSChanged(self, i):
		# print(i)
		print(self.cbbNameSpace.itemText(i))
		if i == 0:
			self.NameSpace = ''
		else:
			self.NameSpace = self.cbbNameSpace.itemText(i)

	@classmethod
	def onKeyAll(self):
		objList = self.getControllerList()
		for obj in objList:
			self.setAnmKey(obj)

	@classmethod
	def onKeySelect(self):
		objList = cmds.ls(sl=True)
		for obj in objList:
			self.setAnmKey(obj)

	@classmethod
	def onDelKey(self):
		currentTime = int(cmds.currentTime(q=True))
		objList = cmds.ls(sl=True)
		for obj in objList:
			self.delKey(obj, currentTime, currentTime)

	@classmethod
	def onSelectAll(self):
		cmds.select(self.getControllerList())

	@classmethod
	def onDelAllAnimation(self):
		objList = self.getControllerList()
		for obj in objList:
			self.delAnm(obj)

	@classmethod
	def onDelSelAnimation(self):
		objList = cmds.ls(sl=True)
		for obj in objList:
			self.delAnm(obj)

	@classmethod
	def onGoSkinPoseAllPressed(self):
		ctrlList = self.getControllerList()
		for obj in ctrlList:
			self.goSkinPose(obj)

	@classmethod
	def onExpBrowserPressed(self):
		fPath = cmds.fileDialog2(fileFilter = "Animation File (*.kaf)")
		if fPath[0]:
			self.exportPath_edit.setText(fPath[0])

	@classmethod
	def onPoseBrowserPressed(self):
		fPath = cmds.fileDialog2(fileFilter = "Pose File (*.kpf)")
		if fPath[0]:
			self.exportPosePath_edit.setText(fPath[0])


	@classmethod
	def onExportAnmPathChanged(self):
		cmds.optionVar(sv = ('KM_KAnm_KafPath', self.exportPath_edit.text()))
		pass

	@classmethod
	def onExportPosePathChanged(self):
		cmds.optionVar(sv = ('KM_KAnm_KpfPath', self.exportPosePath_edit.text()))
		

	@classmethod
	def test(self):
		print("FUCK")
		pass
	#------Select-------
	@classmethod
	def SelectByName(self, *strName):
		# print(self.NameSpace)
		selList = []
		for mem in strName:
			if isinstance(mem,tuple) or isinstance(mem,list):
				for m in mem:
					if isinstance(m,unicode) or isinstance(m,str):
						selList.append(self.NameSpace + m)
			elif isinstance(mem,unicode) or isinstance(mem,str):
				selList.append(self.NameSpace + mem)

		mods = cmds.getModifiers()
		if mods == 0:
			cmds.select(selList)
		elif mods == 4 or mods == 1: #add
			cmds.select(selList, add=True)
		elif mods == 8:
			cmds.select(selList, d=True)

	#---
	@classmethod
	def getControllerList(self):
		
		CtrlSet = "ControllerSet"
		
		if not cmds.objExists(CtrlSet):
			if cmds.objExists(self.NameSpace+CtrlSet):
				CtrlSet = self.NameSpace+CtrlSet
			else:
				setList = cmds.ls(type='objectSet')
				for s in setList:
					if s[-13:] == 'ControllerSet':
						return cmds.listConnections(s+'.dagSetMembers')
			
		return cmds.listConnections(CtrlSet+'.dagSetMembers')

	@classmethod
	def goSkinPose(self, obj):
		if mel.eval('attributeExists "SPTranMtx" ' + obj) == 1:
			cmds.xform(obj, ws=False, m=cmds.getAttr(obj+".SPTranMtx"))

	@classmethod
	def convertArmAnmIK2FK(self):
		nameSpaceFrefix = self.NameSpace
		
		startTime = int(cmds.playbackOptions(q=True, min=True))
		endTime = int(cmds.playbackOptions(q=True, max=True))
		currentTime = int(cmds.currentTime(q=True))
		timePrefix = startTime
		framesCount = endTime - startTime + 1
		
		locUpperArmR = nameSpaceFrefix + "lpIK2FKUpArm_R"
		locForeArmR = nameSpaceFrefix + "lpIK2FKFoArm_R"
		locHandR = nameSpaceFrefix + "lpIK2FKHand_R"
		locUpperArmL = nameSpaceFrefix + "lpIK2FKUpArm_L"
		locForeArmL = nameSpaceFrefix + "lpIK2FKFoArm_L"
		locHandL = nameSpaceFrefix + "lpIK2FKHand_L"
		
		targetUpperArmR = nameSpaceFrefix + "FKUpperArm_R"
		targetForeArmR = nameSpaceFrefix + "FKForeArm_R"
		targetHandR = nameSpaceFrefix + "FKHand_R"
		targetUpperArmL = nameSpaceFrefix + "FKUpperArm_L"
		targetForeArmL = nameSpaceFrefix + "FKForeArm_L"
		targetHandL = nameSpaceFrefix + "FKHand_L"
		
		tarRUpperArmTransArray = []
		tarRForeArmTransArray = []
		tarRHandTransArray = []
		tarLUpperArmTransArray = []
		tarLForeArmTransArray = []
		tarLHandTransArray = []
		
		for f in range(0,framesCount,1):
			cmds.currentTime(f + timePrefix)
			# if bBoth or bRightArm:
			tarRUpperArmTransArray.append(cmds.xform(locUpperArmR,q=True,ws=True,m=True))
			tarRForeArmTransArray.append(cmds.xform(locForeArmR,q=True,ws=True,m=True))
			tarRHandTransArray.append(cmds.xform(locHandR,q=True,ws=True,m=True))
			# if bBoth or (not bRightArm):
			tarLUpperArmTransArray.append(cmds.xform(locUpperArmL,q=True,ws=True,m=True))
			tarLForeArmTransArray.append(cmds.xform(locForeArmL,q=True,ws=True,m=True))
			tarLHandTransArray.append(cmds.xform(locHandL,q=True,ws=True,m=True))
			
		for f in range(0,framesCount,1):
			tF = f + timePrefix
			cmds.currentTime(tF)
			
			
			if f==0 or f==(framesCount-1):
				cmds.setKeyframe(nameSpaceFrefix+"ControlRoot.RArmFKIKBlend", time=tF, value=0)
				cmds.setKeyframe(nameSpaceFrefix+"ControlRoot.LArmFKIKBlend", time=tF, value=0)
			else:
				cmds.cutKey(nameSpaceFrefix+"ControlRoot.RArmFKIKBlend",time=(tF,tF))
				cmds.cutKey(nameSpaceFrefix+"ControlRoot.LArmFKIKBlend",time=(tF,tF))

			cmds.xform(targetUpperArmR, ws=True, m=tarRUpperArmTransArray[f])
			cmds.setKeyframe(targetUpperArmR + ".rx", targetUpperArmR + ".ry", targetUpperArmR + ".rz")
			cmds.xform(targetForeArmR, ws=True, m=tarRForeArmTransArray[f])
			cmds.setKeyframe(targetForeArmR + ".rx", targetForeArmR + ".ry", targetForeArmR + ".rz")
			cmds.xform(targetHandR, ws=True, m=tarRHandTransArray[f])
			cmds.setKeyframe(targetHandR + ".rx", targetHandR + ".ry", targetHandR + ".rz")
		
			cmds.xform(targetUpperArmL, ws=True, m=tarLUpperArmTransArray[f])
			cmds.setKeyframe(targetUpperArmL + ".rx", targetUpperArmL + ".ry", targetUpperArmL + ".rz")
			cmds.xform(targetForeArmL, ws=True, m=tarLForeArmTransArray[f])
			cmds.setKeyframe(targetForeArmL + ".rx", targetForeArmL + ".ry", targetForeArmL + ".rz")
			cmds.xform(targetHandL, ws=True, m=tarLHandTransArray[f])
			cmds.setKeyframe(targetHandL + ".rx", targetHandL + ".ry", targetHandL + ".rz")
		
		
		cmds.filterCurve(targetUpperArmR+".rotateX",targetUpperArmR+".rotateY",targetUpperArmR+".rotateZ")
		cmds.filterCurve(targetForeArmR+".rotateX",targetForeArmR+".rotateY",targetForeArmR+".rotateZ")
		cmds.filterCurve(targetHandR+".rotateX",targetHandR+".rotateY",targetHandR+".rotateZ")
	
		cmds.filterCurve(targetUpperArmL+".rotateX",targetUpperArmL+".rotateY",targetUpperArmL+".rotateZ")
		cmds.filterCurve(targetForeArmL+".rotateX",targetForeArmL+".rotateY",targetForeArmL+".rotateZ")
		cmds.filterCurve(targetHandL+".rotateX",targetHandL+".rotateY",targetHandL+".rotateZ")
			
		cmds.currentTime(currentTime)
	
	@classmethod
	def convertArmAnmFK2IK(self):
		nameSpaceFrefix = self.NameSpace
			
		startTime = int(cmds.playbackOptions(q=True, min=True))
		endTime = int(cmds.playbackOptions(q=True, max=True))
		currentTime = int(cmds.currentTime(q=True))
		timePrefix = startTime
		framesCount = endTime - startTime + 1
		
		locRArmUpV = nameSpaceFrefix + "pyArmUpv_R"
		locRArmIK = nameSpaceFrefix + "lpFK2IK_R"
		locLArmUpV = nameSpaceFrefix + "pyArmUpv_L"
		locLArmIK = nameSpaceFrefix + "lpFK2IK_L"
		
		TargetUpVR = nameSpaceFrefix + "ArmUpV_R"
		TargetArmIKR = nameSpaceFrefix + "HandIK_R"
		TargetUpVL = nameSpaceFrefix + "ArmUpV_L"
		TargetArmIKL = nameSpaceFrefix + "HandIK_L"
		
		tarRUpVTransArray = []
		tarRArmIKTransArray = []
		tarLUpVTransArray = []
		tarLArmIKTransArray = []
		
				
		for f in range(0,framesCount,1):
			cmds.currentTime(f + timePrefix)
			
			tarRUpVTransArray.append(cmds.xform(locRArmUpV,q=True,ws=True,m=True))
			tarRArmIKTransArray.append(cmds.xform(locRArmIK,q=True,ws=True,m=True))
			tarLUpVTransArray.append(cmds.xform(locLArmUpV,q=True,ws=True,m=True))
			tarLArmIKTransArray.append(cmds.xform(locLArmIK,q=True,ws=True,m=True))
		
		for f in range(0,framesCount,1):
			tF = f + timePrefix
			cmds.currentTime(tF)

			# if bBoth or bRightArm:
			if f==0 or f==(framesCount-1):
				cmds.setKeyframe(nameSpaceFrefix+"ControlRoot.RArmFKIKBlend", time=tF, value=1)
				cmds.setKeyframe(nameSpaceFrefix+"ControlRoot.LArmFKIKBlend", time=tF, value=1)
			else:
				cmds.cutKey(nameSpaceFrefix+"ControlRoot.RArmFKIKBlend",time=(tF,tF))
				cmds.cutKey(nameSpaceFrefix+"ControlRoot.LArmFKIKBlend",time=(tF,tF))
			
			cmds.xform(TargetArmIKR, ws=True, m=tarRArmIKTransArray[f])
			cmds.setKeyframe(TargetArmIKR + ".tx", TargetArmIKR + ".ty", TargetArmIKR + ".tz")
			cmds.setKeyframe(TargetArmIKR + ".rx", TargetArmIKR + ".ry", TargetArmIKR + ".rz")
			cmds.xform(TargetUpVR, ws=True, m=tarRUpVTransArray[f])
			cmds.setKeyframe(TargetUpVR + ".tx", TargetUpVR + ".ty", TargetUpVR + ".tz")
			
			cmds.xform(TargetArmIKL, ws=True, m=tarLArmIKTransArray[f])
			cmds.setKeyframe(TargetArmIKL + ".tx", TargetArmIKL + ".ty", TargetArmIKL + ".tz")
			cmds.setKeyframe(TargetArmIKL + ".rx", TargetArmIKL + ".ry", TargetArmIKL + ".rz")
			cmds.xform(TargetUpVL, ws=True, m=tarLUpVTransArray[f])
			cmds.setKeyframe(TargetUpVL + ".tx", TargetUpVL + ".ty", TargetUpVL + ".tz")
		
		cmds.filterCurve(TargetArmIKR+".rotateX",TargetArmIKR+".rotateY",TargetArmIKR+".rotateZ")
		cmds.filterCurve(TargetArmIKL+".rotateX",TargetArmIKL+".rotateY",TargetArmIKL+".rotateZ")
			
		cmds.currentTime(currentTime)

	@classmethod
	def convertArmPoseFK2IK(self, bRightArm):
		nameSpaceFrefix = ""
		selObjs = cmds.ls(sl=True)
		if(len(selObjs) > 0):
			sOName = selObjs[0].split(':')[-1]
			nameSpaceFrefix = selObjs[0][0:-(len(sOName))]
		
		TarSuffix = "R"
		if not bRightArm:
			TarSuffix = "L"
		
		locArmUpV = nameSpaceFrefix + "pyArmUpv_" + TarSuffix
		locArmIK = nameSpaceFrefix + "lpFK2IK_" + TarSuffix
		
		TargetUpV = nameSpaceFrefix + "ArmUpV_" + TarSuffix
		TargetArmIK = nameSpaceFrefix + "HandIK_" + TarSuffix
		
		tarUpVTrans = cmds.xform(locArmUpV,q=True,ws=True,m=True)
		tarArmIKTrans = cmds.xform(locArmIK,q=True,ws=True,m=True)
		
		cmds.setAttr(nameSpaceFrefix+"ControlRoot." + TarSuffix + "ArmFKIKBlend",1)
		
		cmds.xform(TargetArmIK, ws=True, m=tarArmIKTrans)
		cmds.xform(TargetUpV, ws=True, m=tarUpVTrans)
	
	@classmethod
	def convertArmPoseIK2FK(self, bRightArm):
		nameSpaceFrefix = ""
		selObjs = cmds.ls(sl=True)
		if(len(selObjs) > 0):
			sOName = selObjs[0].split(':')[-1]
			nameSpaceFrefix = selObjs[0][0:-(len(sOName))]
		
		TarSuffix = "R"
		if not bRightArm:
			TarSuffix = "L"
			
		locUpperArm = nameSpaceFrefix + "lpIK2FKUpArm_" + TarSuffix
		locForeArm = nameSpaceFrefix + "lpIK2FKFoArm_" + TarSuffix
		locHand = nameSpaceFrefix + "lpIK2FKHand_" + TarSuffix
		
		targetUpperArm = nameSpaceFrefix + "FKUpperArm_" + TarSuffix
		targetForeArm = nameSpaceFrefix + "FKForeArm_" + TarSuffix
		targetHand = nameSpaceFrefix + "FKHand_" + TarSuffix
		
		tarUpperArmTrans = cmds.xform(locUpperArm,q=True,ws=True,m=True)
		tarForeArmTrans = cmds.xform(locForeArm,q=True,ws=True,m=True)
		tarHandTrans = cmds.xform(locHand,q=True,ws=True,m=True)
		
		cmds.setAttr(nameSpaceFrefix+"ControlRoot." + TarSuffix + "ArmFKIKBlend",0)
		
		cmds.xform(targetUpperArm, ws=True, m=tarUpperArmTrans)
		cmds.xform(targetForeArm, ws=True, m=tarForeArmTrans)
		cmds.xform(targetHand, ws=True, m=tarHandTrans)

	@classmethod
	def onPoseConvert2FKPressed(self):
		self.convertArmPoseIK2FK(True)
		self.convertArmPoseIK2FK(False)

	@classmethod
	def onPoseConvert2IKPressed(self):
		self.convertArmPoseFK2IK(True)
		self.convertArmPoseFK2IK(False)

	@classmethod
	def setAnmKey(self, obj):
		### Position ###
		if not cmds.getAttr(obj + ".translateX", l=True):
			cmds.setKeyframe(obj + ".translateX")
		if not cmds.getAttr(obj + ".translateY", l=True):
			cmds.setKeyframe(obj + ".translateY")
		if not cmds.getAttr(obj + ".translateZ", l=True):
			cmds.setKeyframe(obj + ".translateZ")

		### Rotation ###
		if not cmds.getAttr(obj + ".rotateX", l=True):
			cmds.setKeyframe(obj + ".rotateX")
		if not cmds.getAttr(obj + ".rotateY", l=True):
			cmds.setKeyframe(obj + ".rotateY")
		if not cmds.getAttr(obj + ".rotateZ", l=True):
			cmds.setKeyframe(obj + ".rotateZ")
			
		### Scale ###
		if not cmds.getAttr(obj + ".scaleX", l=True):
			cmds.setKeyframe(obj + ".scaleX")
		if not cmds.getAttr(obj + ".scaleY", l=True):
			cmds.setKeyframe(obj + ".scaleY")
		if not cmds.getAttr(obj + ".scaleZ", l=True):
			cmds.setKeyframe(obj + ".scaleZ")

	@classmethod
	def delKey(self,obj, startT, endT):
		cmds.cutKey(obj, t=(startT,endT))

	@classmethod
	def delAnm(self, obj):
		cmds.cutKey(obj)

	@classmethod
	def addMirrorInfo(self, obj):
		if cmds.objExists(obj):
			if mel.eval('attributeExists "MirrorNode" ' + obj) == 0:
				mel.eval('addAttr -ln "MirrorNode" -dt "string" ' + obj)

			if mel.eval('attributeExists "InvPosX" ' + obj) == 0:
				mel.eval('addAttr -ln "InvPosX" -at "bool" ' + obj)

			if mel.eval('attributeExists "InvPosY" ' + obj) == 0:
				mel.eval('addAttr -ln "InvPosY" -at "bool" ' + obj)

			if mel.eval('attributeExists "InvPosZ" ' + obj) == 0:
				mel.eval('addAttr -ln "InvPosZ" -at "bool" ' + obj)

			if mel.eval('attributeExists "InvRotX" ' + obj) == 0:
				mel.eval('addAttr -ln "InvRotX" -at "bool" ' + obj)

			if mel.eval('attributeExists "InvRotY" ' + obj) == 0:
				mel.eval('addAttr -ln "InvRotY" -at "bool" ' + obj)

			if mel.eval('attributeExists "InvRotZ" ' + obj) == 0:
				mel.eval('addAttr -ln "InvRotZ" -at "bool" ' + obj)
				
			if mel.eval('attributeExists "MirrorRotOffset" ' + obj) == 0:
				cmds.addAttr(obj, ln="MirrorRotOffset", at="double3", k=False)
				cmds.addAttr(obj, ln="MirrorRotOffsetX", at="double", p="MirrorRotOffset", k=False)
				cmds.addAttr(obj, ln="MirrorRotOffsetY", at="double", p="MirrorRotOffset", k=False)
				cmds.addAttr(obj, ln="MirrorRotOffsetZ", at="double", p="MirrorRotOffset", k=False)

	@classmethod
	def setMirrorInfo(self):
		selObjects = cmds.ls(sl=True)
		for obj in selObjects:
			objName = obj.split(':')[-1]
			strPrefix = obj[0:-(len(objName))]
			###### Try Find R/L name ######
			lastStr = objName[-1]
			mirStr = ""
			if lastStr=="M":
				cmds.setAttr(obj + ".MirrorNode", objName, type="string")
				continue
			elif lastStr=="R" or lastStr=="L" :
				if lastStr=="R":
					mirStr = "L"
				else:
					mirStr = "R"

				mirName = objName[:-1] + mirStr

				if (cmds.objExists(strPrefix+mirName)):
					cmds.setAttr(obj + ".MirrorNode", mirName, type="string")
					continue


			######  find mirror side node  ######
			checkBuff = False
			tarLoc = cmds.xform(obj, q=True, ws=True, t=True)
			mirLoc = [tarLoc[0], tarLoc[1], tarLoc[2]]
			mirLoc[0] *= -1

			for other in selObjects:
				if obj == other:
					continue
				else:
					cLoc = cmds.xform(other, q=True, ws=True, t=True)
					mOffsetDis = distance(mirLoc, cLoc)
					if mOffsetDis <= self.fMirrorThreshold:
						dcDis = distance(tarLoc, cLoc)
						if dcDis > self.fMirrorThreshold:
							cmds.setAttr(obj + ".MirrorNode", other.split(':')[-1], type="string")
							checkBuff = True
							break
			if checkBuff == False:
				cmds.setAttr(obj + ".MirrorNode", objName, type="string")

		####  Check flip axis  ####
		for obj in selObjects:
			objName = obj.split(':')[-1]
			strPrefix = obj[0:-(len(objName))]

			mirObj = strPrefix + cmds.getAttr(obj+".MirrorNode")
			trans01 = cmds.xform(obj, q=True, ws=True, m=True)
			trans02 = cmds.xform(mirObj, q=True, ws=True, m=True)

			mVx1 = [-trans01[0],trans01[1],trans01[2]]
			mVy1 = [-trans01[4],trans01[5],trans01[6]]
			mVz1 = [-trans01[8],trans01[9],trans01[10]]

			Vx2 = [trans02[0],trans02[1],trans02[2]]
			Vy2 = [trans02[4],trans02[5],trans02[6]]
			Vz2 = [trans02[8],trans02[9],trans02[10]]

			sX = dot(mVx1, Vx2)
			sY = dot(mVy1, Vy2)
			sZ = dot(mVz1, Vz2)

			invRot = [1,1,1]
			
			if sX > 0:
				cmds.setAttr(obj+".InvPosX", 0)
				cmds.setAttr(obj+".InvRotX", 1)
				invRot[0] = -1
			else:
				cmds.setAttr(obj+".InvPosX", 1)
				cmds.setAttr(obj+".InvRotX", 0)
				invRot[0] = 1

			if sY > 0:
				cmds.setAttr(obj+".InvPosY", 0)
				cmds.setAttr(obj+".InvRotY", 1)
				invRot[1] = -1
			else:
				cmds.setAttr(obj+".InvPosY", 1)
				cmds.setAttr(obj+".InvRotY", 0)
				invRot[1] = 1

			if sZ > 0:
				cmds.setAttr(obj+".InvPosZ", 0)
				cmds.setAttr(obj+".InvRotZ", 1)
				invRot[2] = -1
			else:
				cmds.setAttr(obj+".InvPosZ", 1)
				cmds.setAttr(obj+".InvRotZ", 0)
				invRot[2] = 1
				
			objRot = cmds.getAttr(obj+".rotate")[0]
			curMirrorRot = cmds.getAttr(mirObj+".rotate")[0]
			RotOffset = [curMirrorRot[0]-objRot[0]*invRot[0],
			             curMirrorRot[1]-objRot[1]*invRot[1],
			             curMirrorRot[2]-objRot[2]*invRot[2]]
			cmds.setAttr(obj + ".MirrorRotOffset", RotOffset[0],RotOffset[1],RotOffset[2], type="double3")

	@classmethod
	def exportAnima(self, filePath, isMirror):
		selObjects = cmds.ls(sl=True)
		objCount = len(selObjects)
		startTime = int(cmds.playbackOptions(q=True, min=True))
		endTime = int(cmds.playbackOptions(q=True, max=True))
		currentTime = int(cmds.currentTime(q=True))
		timePrefix = startTime
		framesCount = endTime - startTime + 1

		AnimData = OrderedDict()
		AnimData['count'] = objCount

		objList = []
		for o in selObjects:
			if isMirror and (mel.eval('attributeExists "MirrorNode" ' + o) == 1):
				objList.append(cmds.getAttr(o+".MirrorNode"))
			else:
				clrName = o.split(':')[-1]
				objList.append(clrName)
		AnimData['name'] = objList

		AnimData['timelength'] = framesCount

		frameAniData = OrderedDict()
		for f in range(0,framesCount,1):
			cmds.currentTime(f + timePrefix)
			posArray = []
			RotArray = []
			sclArray = []
			
			for o in selObjects:
				cLPos = list(cmds.getAttr(o+".translate")[0])
				cLRot = list(cmds.getAttr(o+".rotate")[0])
				cLScl = list(cmds.getAttr(o+".scale")[0])
				if isMirror:
					MRO = cmds.getAttr(o+".MirrorRotOffset")[0]
					if (cmds.getAttr(o+".InvPosX")):
						cLPos[0] *= -1
					if (cmds.getAttr(o+".InvPosY")):
						cLPos[1] *= -1
					if (cmds.getAttr(o+".InvPosZ")):
						cLPos[2] *= -1
					if (cmds.getAttr(o+".InvRotX")):
						cLRot[0] *= -1
					if (cmds.getAttr(o+".InvRotY")):
						cLRot[1] *= -1
					if (cmds.getAttr(o+".InvRotZ")):
						cLRot[2] *= -1
						
					cLRot[0] = cLRot[0] + MRO[0]
					cLRot[1] = cLRot[1] + MRO[1]
					cLRot[2] = cLRot[2] + MRO[2]

				posArray.append(cLPos)
				RotArray.append(cLRot)
				sclArray.append(cLScl)
			
			transformData = OrderedDict()
			transformData["Position"] = posArray
			transformData["Rotation"] = RotArray
			transformData["Scale"] = sclArray

			frameAniData[f] = transformData
		
		AnimData["Animation"] = frameAniData

		json_str = json.dumps(AnimData, sort_keys=False)

		#### Write to xaf file ###
		text_file = open(filePath, "w")
		text_file.write(json_str)
		text_file.close()

		cmds.currentTime(currentTime)

	@classmethod
	def importAnima(self, filePath):
		text_file = open(filePath, "r")
		
		nameSpaceFrefix = ""
		selObjs = cmds.ls(sl=True)
		if(len(selObjs) > 0):
			sOName = selObjs[0].split(':')[-1]
			nameSpaceFrefix = selObjs[0][0:-(len(sOName))]

		fString = text_file.read()
		kafData = json.loads(fString)

		objCount = kafData['count']
		objList = kafData['name']
		framesCount = kafData['timelength']
		AnimData = kafData['Animation']
		endTime = int(cmds.playbackOptions(q=True, max=True))
		startFrame = int(cmds.currentTime(q=True))
		for f in range(0,framesCount):
			tKey = str(f)
			for i in range(0,objCount):
				if (cmds.objExists(nameSpaceFrefix + objList[i])):
					
					### Position ###
					if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".translateX", l=True):
						cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".translateX", time=(startFrame+f), value=AnimData[tKey]['Position'][i][0])
					if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".translateY", l=True):
						cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".translateY", time=(startFrame+f), value=AnimData[tKey]['Position'][i][1])
					if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".translateZ", l=True):
						cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".translateZ", time=(startFrame+f), value=AnimData[tKey]['Position'][i][2])

					### Rotation ###
					if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".rotateX", l=True):
						cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".rotateX", time=(startFrame+f), value=AnimData[tKey]['Rotation'][i][0])
					if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".rotateY", l=True):
						cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".rotateY", time=(startFrame+f), value=AnimData[tKey]['Rotation'][i][1])
					if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".rotateZ", l=True):
						cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".rotateZ", time=(startFrame+f), value=AnimData[tKey]['Rotation'][i][2])

					### Scale ###
					if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".scaleX", l=True):
						cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".scaleX", time=(startFrame+f), value=AnimData[tKey]['Scale'][i][0])
					if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".scaleY", l=True):
						cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".scaleY", time=(startFrame+f), value=AnimData[tKey]['Scale'][i][1])
					if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".scaleZ", l=True):
						cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".scaleZ", time=(startFrame+f), value=AnimData[tKey]['Scale'][i][2])
		
		for i in range(0,objCount):
			if (cmds.objExists(nameSpaceFrefix + objList[i])):
				cmds.filterCurve(nameSpaceFrefix+objList[i]+".rotateX",nameSpaceFrefix+objList[i]+".rotateY",nameSpaceFrefix+objList[i]+".rotateZ")
		
		newEndFrame = startFrame + framesCount
		if newEndFrame > endTime:
			cmds.playbackOptions(max = newEndFrame - 1)

		text_file.close()

	@classmethod
	def exportPose(self, filePath, isMirror):
		selObjects = cmds.ls(sl=True)
		objCount = len(selObjects)
		currentTime = int(cmds.currentTime(q=True))

		PoseData = OrderedDict()
		PoseData['count'] = objCount

		objList = []
		for o in selObjects:
			if isMirror and (mel.eval('attributeExists "MirrorNode" ' + o) == 1):
				objList.append(cmds.getAttr(o+".MirrorNode"))
			else:
				clrName = o.split(':')[-1]
				objList.append(clrName)
		PoseData['name'] = objList

		

		posArray = []
		RotArray = []
		sclArray = []

		for o in selObjects:
			cLPos = list(cmds.getAttr(o+".translate")[0])
			cLRot = list(cmds.getAttr(o+".rotate")[0])
			cLScl = list(cmds.getAttr(o+".scale")[0])
			if isMirror:
				MRO = cmds.getAttr(o+".MirrorRotOffset")[0]
				if (cmds.getAttr(o+".InvPosX")):
					cLPos[0] *= -1
				if (cmds.getAttr(o+".InvPosY")):
					cLPos[1] *= -1
				if (cmds.getAttr(o+".InvPosZ")):
					cLPos[2] *= -1
				if (cmds.getAttr(o+".InvRotX")):
					cLRot[0] *= -1
				if (cmds.getAttr(o+".InvRotY")):
					cLRot[1] *= -1
				if (cmds.getAttr(o+".InvRotZ")):
					cLRot[2] *= -1
					
				cLRot[0] = cLRot[0] + MRO[0]
				cLRot[1] = cLRot[1] + MRO[1]
				cLRot[2] = cLRot[2] + MRO[2]

			posArray.append(cLPos)
			RotArray.append(cLRot)
			sclArray.append(cLScl)

		transformData = OrderedDict()
		transformData["Position"] = posArray
		transformData["Rotation"] = RotArray
		transformData["Scale"] = sclArray

		PoseData['Pose'] = transformData

		json_str = json.dumps(PoseData, sort_keys=False)
		
		
		
		#### Write to xaf file ###
		text_file = open(filePath, "w")
		text_file.write(json_str)
		text_file.close()

	@classmethod
	def importPose(self, filePath):
		text_file = open(filePath, "r")
		
		nameSpaceFrefix = ""
		selObjs = cmds.ls(sl=True)
		if(len(selObjs) > 0):
			sOName = selObjs[0].split(':')[-1]
			nameSpaceFrefix = selObjs[0][0:-(len(sOName))]

		fString = text_file.read()
		kpfData = json.loads(fString)

		objCount = kpfData['count']
		objList = kpfData['name']
		PoseData = kpfData['Pose']

		for i in range(0,objCount):
			if (cmds.objExists(nameSpaceFrefix + objList[i])):
				### Position ###
				if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".translateX", l=True):
					#cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".translateX", time=(startFrame+f), value=AnimData[tKey]['Position'][i][0])
					cmds.setAttr(nameSpaceFrefix + objList[i] + ".translateX", PoseData['Position'][i][0])
				if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".translateY", l=True):
					#cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".translateY", time=(startFrame+f), value=AnimData[tKey]['Position'][i][1])
					cmds.setAttr(nameSpaceFrefix + objList[i] + ".translateY", PoseData['Position'][i][1])
				if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".translateZ", l=True):
					#cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".translateZ", time=(startFrame+f), value=AnimData[tKey]['Position'][i][2])
					cmds.setAttr(nameSpaceFrefix + objList[i] + ".translateZ", PoseData['Position'][i][2])

				### Rotation ###
				if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".rotateX", l=True):
					#cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".rotateX", time=(startFrame+f), value=AnimData[tKey]['Rotation'][i][0])
					cmds.setAttr(nameSpaceFrefix + objList[i] + ".rotateX", PoseData['Rotation'][i][0])
				if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".rotateY", l=True):
					#cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".rotateY", time=(startFrame+f), value=AnimData[tKey]['Rotation'][i][1])
					cmds.setAttr(nameSpaceFrefix + objList[i] + ".rotateY", PoseData['Rotation'][i][1])
				if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".rotateZ", l=True):
					#cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".rotateZ", time=(startFrame+f), value=AnimData[tKey]['Rotation'][i][2])
					cmds.setAttr(nameSpaceFrefix + objList[i] + ".rotateZ", PoseData['Rotation'][i][2])

				### Scale ###
				if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".scaleX", l=True):
					#cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".scaleX", time=(startFrame+f), value=AnimData[tKey]['Scale'][i][0])
					cmds.setAttr(nameSpaceFrefix + objList[i] + ".scaleX", PoseData['Scale'][i][0])
				if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".scaleY", l=True):
					#cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".scaleY", time=(startFrame+f), value=AnimData[tKey]['Scale'][i][1])
					cmds.setAttr(nameSpaceFrefix + objList[i] + ".scaleY", PoseData['Scale'][i][1])
				if not cmds.getAttr(nameSpaceFrefix + objList[i] + ".scaleZ", l=True):
					#cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".scaleZ", time=(startFrame+f), value=AnimData[tKey]['Scale'][i][2])
					cmds.setAttr(nameSpaceFrefix + objList[i] + ".scaleZ", PoseData['Scale'][i][2])

	@classmethod
	def onExpAnimaPressed(self):
		fileInfo = getFilePathInfo(self.exportPath_edit.text())
		if len(fileInfo[0]) == 0:
			fileInfo[0] = "D:/"
		if len(fileInfo[1]) == 0:
			fileInfo[1] = "Anm"
		if fileInfo[2] != ".kaf":
			fileInfo[2] = ".kaf"
		newFilePath = fileInfo[0] + fileInfo[1] + fileInfo[2]
		newFilePath = newFilePath.encode('utf-8')
		self.exportPath_edit.setText(newFilePath)
		
		self.exportAnima(newFilePath, False)

	@classmethod
	def onExpAnimaMirrorPressed(self):
		fileInfo = getFilePathInfo(self.exportPath_edit.text())
		if len(fileInfo[0]) == 0:
			fileInfo[0] = "D:/"
		if len(fileInfo[1]) == 0:
			fileInfo[1] = "Anm"
		if fileInfo[2] != ".kaf":
			fileInfo[2] = ".kaf"
		newFilePath = fileInfo[0] + fileInfo[1] + fileInfo[2]
		newFilePath = newFilePath.encode('utf-8')
		self.exportPath_edit.setText(newFilePath)
		
		self.exportAnima(newFilePath, True)

	@classmethod
	def onImpAnimaPressed(self):
		fileInfo = getFilePathInfo(self.exportPath_edit.text())
		if len(fileInfo[0]) == 0:
			fileInfo[0] = "D:/"
		if len(fileInfo[1]) == 0:
			fileInfo[1] = "Anm"
		if fileInfo[2] != ".kaf":
			fileInfo[2] = ".kaf"
		newFilePath = fileInfo[0] + fileInfo[1] + fileInfo[2]
		newFilePath = newFilePath.encode('utf-8')
		self.exportPath_edit.setText(newFilePath)
		
		self.importAnima(newFilePath)

	@classmethod
	def onExpPosePressed(self):
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
		self.exportPose(newFilePath, False)

	@classmethod
	def onExpPoseMirrorPressed(self):
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
		self.exportPose(newFilePath, True)
		
	@classmethod
	def onImpPosePressed(self):
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
		self.importPose(newFilePath)
#-------------------------------------------------#
if __name__ == "__main__":
	kAnim_ui = KAnimTools() 