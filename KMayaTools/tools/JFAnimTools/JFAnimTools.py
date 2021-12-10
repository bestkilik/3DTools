import maya.cmds as cmds
import inspect
if int(cmds.about(version=True)) >= 2017:
	import PySide2.QtCore as QtCore
	import PySide2.QtWidgets as QtGui
	from shiboken2 import wrapInstance
else:
	import PySide.QtCore as QtCore
	import PySide.QtGui as QtGui
	from shiboken import wrapInstance

from collections import OrderedDict

import json
import math

import maya.OpenMayaUI as omui
import maya.mel as mel
import os
import os.path
import tempfile

pi = 3.14159265359

def radByAngle(angle):
	return angle / 180.0 * pi

def getVectorSize(Vec):
	return math.sqrt(Vec[0]*Vec[0]+Vec[1]*Vec[1]+Vec[2]*Vec[2])

def normalizeVec(Vec):
	size = getVectorSize(Vec)
	return [Vec[0]/size, Vec[1]/size,Vec[2]/size]

def getDistance(pointA, pointB):
	return getVectorSize([pointB[0]-pointA[0], pointB[1]-pointA[1],pointB[2]-pointA[2]])

def dot(v1, v2):
    return sum(x*y for x,y in zip(v1,v2))

def distance(A, B):
	sqX = (A[0] - B[0])*(A[0] - B[0])
	sqY = (A[1] - B[1])*(A[1] - B[1])
	sqZ = (A[2] - B[2])*(A[2] - B[2])
	return math.sqrt(sqX + sqY + sqZ)

def getVector(pointA, pointB):
	return normalizeVec([pointB[0]-pointA[0], pointB[1]-pointA[1],pointB[2]-pointA[2]])

def crossVec(Vec1, Vec2):
	outVec = [Vec1[1]*Vec2[2] - Vec1[2]*Vec2[1],
	          Vec1[2]*Vec2[0] - Vec1[0]*Vec2[2],
	          Vec1[0]*Vec2[1] - Vec1[1]*Vec2[0]]
	return normalizeVec(outVec)

def getTransMatrix(LookAxisIdx, LookVec, UpAxisIdx, UpVec, Pos):
	LookVec = normalizeVec(LookVec)
	UpVec = normalizeVec(UpVec)
	
	SideVec = crossVec(LookVec, UpVec)
	UpVec = crossVec(SideVec, LookVec)
	
	VecX = LookVec
	VecY = UpVec
	VecZ = SideVec
	
	if LookAxisIdx == 0 and UpAxisIdx == 2:
		VecZ = UpVec
		VecY = [-SideVec[0], -SideVec[1], -SideVec[2]]
	elif LookAxisIdx == 1 and UpAxisIdx == 0:
		VecX = UpVec
		VecY = LookVec
		VecZ = [-SideVec[0], -SideVec[1], -SideVec[2]]
	elif LookAxisIdx == 1 and UpAxisIdx == 2:
		VecZ = UpVec
		VecY = LookVec
		VecX = SideVec
	elif LookAxisIdx == 2 and UpAxisIdx == 0:
		VecX = UpVec
		VecZ = LookVec
		VecY = SideVec
	elif LookAxisIdx == 2 and UpAxisIdx == 1:
		VecY = UpVec
		VecZ = LookVec
		VecX = [-SideVec[0], -SideVec[1], -SideVec[2]]
		
	return [VecX[0],VecX[1],VecX[2],0,
	        VecY[0],VecY[1],VecY[2],0,
	        VecZ[0],VecZ[1],VecZ[2],0,
	        Pos[0],Pos[1],Pos[2],1]

def getFilePathInfo(fullPath):
	DiskPath, fullFileName = os.path.split(fullPath)
	FileName, FileType = os.path.splitext(fullFileName)
	
	# if len(DiskPath) == 0:
	# 	DiskPath = defaultDiskPath #os.path.abspath(os.sep)
		
	# if len(FileType) == 0:
	# 	FileType = defaultFileType
		
	return [DiskPath,FileName,FileType]

def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(long(main_window_ptr), QtGui.QWidget)

class JFAnmTools(QtGui.QDialog):
	exportPath_edit = QtGui.QLineEdit("D:/Anm.kaf")
	exportPosePath_edit = QtGui.QLineEdit("D:/Pose.kpf")
	fMirrorThreshold = 0.05
	
	def __init__(self, parent=maya_main_window()):
		self.closeExistingWindow()
		super(JFAnmTools, self).__init__(parent)
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
		# try:
		# 	TLW = QtGui.QApplication.instance().topLevelWidgets()
		# 	if TLW:
		# 		for qt in TLW:
		# 			try:
		# 				if qt.__class__.__name__ == self.__class__.__name__:
		# 					qt.close()
		# 					qt.deleteLater()
		# 			except:
		# 				pass
		# except:
		# 	print("Can't close Tool...")
		# 	pass
		pass
				
	def create(self):
		self.setWindowTitle("JF Anim Tools")
		self.setWindowFlags(QtCore.Qt.Tool)
		self.setMinimumSize(400,440)
		self.setMaximumSize(400,440)
		
		self.create_controls()
		self.create_layout()
		self.readConfig()
		self.create_connections()
		self.show()
		
	def readConfig(self):
		## Default Value ##
		mirrorThreshold = None
		kafPath = 'D:/Anm.kaf'
		kpfPath = 'D:/Pose.kpf'
		try:
			if not cmds.optionVar( exists='JF_KAnm_MirrorThreshold' ):
				cmds.optionVar(fv = ('JF_KAnm_MirrorThreshold', 0.05))
				mirrorThreshold = 0.05
			else:
				mirrorThreshold = cmds.optionVar(q='JF_KAnm_MirrorThreshold' )

			if not cmds.optionVar( exists='JF_KAnm_KafPath' ):
				cmds.optionVar(sv = ('JF_KAnm_KafPath', kafPath))
			else:
				kafPath = cmds.optionVar(q='JF_KAnm_KafPath')
			
			if not cmds.optionVar( exists='JF_KAnm_KpfPath' ):
				cmds.optionVar(sv = ('JF_KAnm_KpfPath', kpfPath))
			else:
				kpfPath = cmds.optionVar(q='JF_KAnm_KpfPath')
		except:
			pass

		self.mirrorLocThreshold_spb.setValue(mirrorThreshold)
		self.exportPath_edit.setText(kafPath)
		self.exportPosePath_edit.setText(kpfPath)	
	
	def create_controls(self):
		#Anim Utilities
		self.btnArmFK2IKPose_R = QtGui.QPushButton("FK > IK (R)")
		self.btnArmFK2IKPose_L = QtGui.QPushButton("FK > IK (L)")
		self.btnArmFK2IKPose_B = QtGui.QPushButton("FK > IK (Both)")
		self.btnArmIK2FKPose_R = QtGui.QPushButton("IK > FK (R)")
		self.btnArmIK2FKPose_L = QtGui.QPushButton("IK > FK (L)")
		self.btnArmIK2FKPose_B = QtGui.QPushButton("IK > FK (Both)")
		
		self.btnArmFK2IKAnm_R = QtGui.QPushButton("FK > IK (R)")
		self.btnArmFK2IKAnm_L = QtGui.QPushButton("FK > IK (L)")
		self.btnArmFK2IKAnm_B = QtGui.QPushButton("FK > IK (Both)")
		self.btnArmIK2FKAnm_R = QtGui.QPushButton("IK > FK (R)")
		self.btnArmIK2FKAnm_L = QtGui.QPushButton("IK > FK (L)")
		self.btnArmIK2FKAnm_B = QtGui.QPushButton("IK > FK (Both)")
		
		self.btnGotoSkinPoseAll = QtGui.QPushButton("Go Skin Pose (ALL Controller)")
		self.btnGotoSkinPoseSelect = QtGui.QPushButton("Go Skin Pose (Selected)")
		self.btnSelectAll = QtGui.QPushButton("Select All")
		self.btnKeySelect = QtGui.QPushButton("Key Selected")
		self.btnKeyAll = QtGui.QPushButton("Key All")
		self.btnDelAnmSelect = QtGui.QPushButton("Del Anim Selected")
		self.btnDelAnmAll = QtGui.QPushButton("Del Anim All")
		
		#Bake Anim
		self.addMirrorInfo_btn = QtGui.QPushButton("Add Mirror Info")
		self.addMirrorInfo_btn.setMinimumHeight(86)
		self.mirrorLocThreshold_spb = QtGui.QDoubleSpinBox()
		self.mirrorLocThreshold_spb.setRange(0.00,10.00)
		self.mirrorLocThreshold_spb.setValue(0.05)
		self.mirrorLocThreshold_spb.setSingleStep(0.01)
		self.autoSetMInfo_btn = QtGui.QPushButton("Auto Setting")
		self.removeMirrorInfo_btn = QtGui.QPushButton("Remove Mirror Info")
		self.expBrowse_btn = QtGui.QPushButton("Browse")
		self.expAnm_btn = QtGui.QPushButton("Export")
		self.expAnmMirror_btn = QtGui.QPushButton("Mirror Export")
		self.impAnm_btn = QtGui.QPushButton("Import")
		self.expPoseBrowse_btn = QtGui.QPushButton("Browse")
		self.expPose_btn = QtGui.QPushButton("Export")
		self.expPoseMirror_btn = QtGui.QPushButton("Mirror Export")
		self.impPose_btn = QtGui.QPushButton("Import")
		
		#Mocap
		self.btnImportAnmFromFBX = QtGui.QPushButton("Import Anim from FBX")
		self.btnImportAnmFromFBX.setMinimumHeight(100)
		pass
		
	def create_layout(self):
		#--------------------------
		main_layout = QtGui.QVBoxLayout()
		main_layout.setContentsMargins(6, 6, 6, 6)
		
		MainTab_Widget = QtGui.QTabWidget()
		main_layout.addWidget(MainTab_Widget)
		
		#-------------
		BakeAnim_tab = QtGui.QWidget()
		BakeAnim_Layout = QtGui.QVBoxLayout()
		BakeAnim_tab.setLayout(BakeAnim_Layout)
		
		#-------------
		AnimUtilities_tab = QtGui.QWidget()
		AnimUtilities_Layout = QtGui.QVBoxLayout()
		AnimUtilities_tab.setLayout(AnimUtilities_Layout)
		
		#-------------
		Mocap_tab = QtGui.QWidget()
		Mocap_Layout = QtGui.QVBoxLayout()
		Mocap_tab.setLayout(Mocap_Layout)
		
		MainTab_Widget.addTab(AnimUtilities_tab, "Anim Utilities")
		MainTab_Widget.addTab(BakeAnim_tab, "Bake Anim")
		MainTab_Widget.addTab(Mocap_tab, "Mocap")
		
		#==============
		FKIKPose_Group = QtGui.QGroupBox("FK/IK (Pose)")
		FKIKPose_Group.setMaximumHeight(80)
		FKIKAnim_Group = QtGui.QGroupBox("FK/IK (Anim)")
		FKIKAnim_Group.setMaximumHeight(80)
		AnimUtilities_Layout.addWidget(FKIKPose_Group)
		AnimUtilities_Layout.addWidget(FKIKAnim_Group)
		# AnimUtilities_Layout.setAlignment(FKIKPose_Group, QtCore.Qt.AlignTop)
		AnimUtilities_Layout.setAlignment(FKIKAnim_Group, QtCore.Qt.AlignTop)
		
		FKIKPose_HLayout0 = QtGui.QHBoxLayout()
		FKIKPose_HLayout0.addWidget(self.btnArmFK2IKPose_R)
		FKIKPose_HLayout0.addWidget(self.btnArmFK2IKPose_B)
		FKIKPose_HLayout0.addWidget(self.btnArmFK2IKPose_L)
		
		FKIKPose_HLayout1 = QtGui.QHBoxLayout()
		FKIKPose_HLayout1.addWidget(self.btnArmIK2FKPose_R)
		FKIKPose_HLayout1.addWidget(self.btnArmIK2FKPose_B)
		FKIKPose_HLayout1.addWidget(self.btnArmIK2FKPose_L)
		
		FKIKPose_VLayout0 = QtGui.QVBoxLayout()
		FKIKPose_VLayout0.addLayout(FKIKPose_HLayout0)
		FKIKPose_VLayout0.addLayout(FKIKPose_HLayout1)
		#--
		FKIKAnm_HLayout0 = QtGui.QHBoxLayout()
		FKIKAnm_HLayout0.addWidget(self.btnArmFK2IKAnm_R)
		FKIKAnm_HLayout0.addWidget(self.btnArmFK2IKAnm_B)
		FKIKAnm_HLayout0.addWidget(self.btnArmFK2IKAnm_L)
		
		FKIKAnm_HLayout1 = QtGui.QHBoxLayout()
		FKIKAnm_HLayout1.addWidget(self.btnArmIK2FKAnm_R)
		FKIKAnm_HLayout1.addWidget(self.btnArmIK2FKAnm_B)
		FKIKAnm_HLayout1.addWidget(self.btnArmIK2FKAnm_L)
		
		FKIKAnm_VLayout0 = QtGui.QVBoxLayout()
		FKIKAnm_VLayout0.addLayout(FKIKAnm_HLayout0)
		FKIKAnm_VLayout0.addLayout(FKIKAnm_HLayout1)
		
		FKIKPose_Group.setLayout(FKIKPose_VLayout0)
		FKIKAnim_Group.setLayout(FKIKAnm_VLayout0)
		
		#--
		AnmTools_VLayout0 = QtGui.QVBoxLayout()
		AnimUtilities_Layout.addLayout(AnmTools_VLayout0)
		AnimUtilities_Layout.setAlignment(QtCore.Qt.AlignTop)
		
		AnmTools_HLayout0 = QtGui.QHBoxLayout()
		AnmTools_HLayout0.addWidget(self.btnGotoSkinPoseAll)
		AnmTools_HLayout0.addWidget(self.btnGotoSkinPoseSelect)
		AnmTools_VLayout0.addLayout(AnmTools_HLayout0)
		
		AnmTools_HLayout1 = QtGui.QHBoxLayout()
		AnmTools_HLayout1.addWidget(self.btnSelectAll)
		AnmTools_VLayout0.addLayout(AnmTools_HLayout1)
		
		AnmTools_HLayout2 = QtGui.QHBoxLayout()
		AnmTools_HLayout2.addWidget(self.btnKeySelect)
		AnmTools_HLayout2.addWidget(self.btnKeyAll)
		AnmTools_VLayout0.addLayout(AnmTools_HLayout2)
		
		AnmTools_HLayout3 = QtGui.QHBoxLayout()
		AnmTools_HLayout3.addWidget(self.btnDelAnmSelect)
		AnmTools_HLayout3.addWidget(self.btnDelAnmAll)
		AnmTools_VLayout0.addLayout(AnmTools_HLayout3)
		
		#==============
		groupBox0 = QtGui.QGroupBox("Mirror Info")

		mInfo_main_layout = QtGui.QHBoxLayout()
		mInfo_main_layout.setContentsMargins(6,6,6,6)

		mInfo_layout001 = QtGui.QHBoxLayout()
		mInfo_layout001.addWidget(QtGui.QLabel("mirror threshold:"))
		mInfo_layout001.addWidget(self.mirrorLocThreshold_spb)

		mInfo_layout01 = QtGui.QVBoxLayout()
		mInfo_layout01.addLayout(mInfo_layout001)
		mInfo_layout01.addWidget(self.autoSetMInfo_btn)
		mInfo_layout01.addWidget(self.removeMirrorInfo_btn)

		mInfo_main_layout.addWidget(self.addMirrorInfo_btn)
		mInfo_main_layout.addLayout(mInfo_layout01)

		groupBox0.setLayout(mInfo_main_layout)
		#--------------------------
		groupBox1 = QtGui.QGroupBox("Animation")

		layout1 = QtGui.QVBoxLayout()
		layout1.setContentsMargins(6, 6, 6, 6)

		layout01 = QtGui.QHBoxLayout()
		layout01.setContentsMargins(2, 2, 2, 2)
		layout01.addWidget(self.exportPath_edit)
		layout01.addWidget(self.expBrowse_btn)

		layout001 = QtGui.QVBoxLayout()
		layout001.setContentsMargins(2, 2, 2, 2)
		layout001.addWidget(self.expAnm_btn)
		layout001.addWidget(self.expAnmMirror_btn)

		layout02 = QtGui.QHBoxLayout()
		layout02.setContentsMargins(2, 6, 6, 6)

		layout02.addLayout(layout001)
		layout02.addWidget(self.impAnm_btn)
		
		layout1.addLayout(layout01)
		layout1.addLayout(layout02)

		groupBox1.setLayout(layout1)
		#------------------------------------
		groupBox2 = QtGui.QGroupBox("Pose")

		playout1 = QtGui.QVBoxLayout()
		playout1.setContentsMargins(6, 6, 6, 6)

		playout01 = QtGui.QHBoxLayout()
		playout01.setContentsMargins(2, 2, 2, 2)
		playout01.addWidget(self.exportPosePath_edit)
		playout01.addWidget(self.expPoseBrowse_btn)

		playout001 = QtGui.QVBoxLayout()
		playout001.setContentsMargins(2, 2, 2, 2)
		playout001.addWidget(self.expPose_btn)
		playout001.addWidget(self.expPoseMirror_btn)

		playout02 = QtGui.QHBoxLayout()
		playout02.setContentsMargins(2, 6, 6, 6)

		playout02.addLayout(playout001)
		playout02.addWidget(self.impPose_btn)
		
		playout1.addLayout(playout01)
		playout1.addLayout(playout02)

		groupBox2.setLayout(playout1)
		#------------------------------------
		BakeAnim_Layout.addWidget(groupBox0)
		BakeAnim_Layout.addWidget(groupBox1)
		BakeAnim_Layout.addWidget(groupBox2)

		BakeAnim_Layout.addStretch()
		
		#==============
		Mocap_Layout.addWidget(self.btnImportAnmFromFBX)


		#-------------
		self.setLayout(main_layout)
	
	def create_connections(self):
		#--------------
		self.btnArmFK2IKPose_R.clicked.connect(JFAnmTools.onArmPoseIK2FKRightPressed)
		self.btnArmFK2IKPose_B.clicked.connect(JFAnmTools.onArmPoseIK2FKBothPressed)
		self.btnArmFK2IKPose_L.clicked.connect(JFAnmTools.onArmPoseIK2FKLeftPressed)
		
		self.btnArmIK2FKPose_R.clicked.connect(JFAnmTools.onArmPoseFK2IKRightPressed)
		self.btnArmIK2FKPose_B.clicked.connect(JFAnmTools.onArmPoseFK2IKBothPressed)
		self.btnArmIK2FKPose_L.clicked.connect(JFAnmTools.onArmPoseFK2IKLeftPressed)
		
		
		self.btnArmFK2IKAnm_R.clicked.connect(JFAnmTools.onArmAnmIK2FKRightPressed)
		self.btnArmFK2IKAnm_B.clicked.connect(JFAnmTools.onArmAnmIK2FKBothPressed)
		self.btnArmFK2IKAnm_L.clicked.connect(JFAnmTools.onArmAnmIK2FKLeftPressed)
		
		self.btnArmIK2FKAnm_R.clicked.connect(JFAnmTools.onArmAnmFK2IKRightPressed)
		self.btnArmIK2FKAnm_B.clicked.connect(JFAnmTools.onArmAnmFK2IKBothPressed)
		self.btnArmIK2FKAnm_L.clicked.connect(JFAnmTools.onArmAnmFK2IKLeftPressed)
		
		# self.btnGotoSkinPoseAll
		self.btnGotoSkinPoseAll.clicked.connect(JFAnmTools.onGoSkinPoseAllPressed)
		self.btnGotoSkinPoseSelect.clicked.connect(JFAnmTools.onGoSkinPoseSelectedPressed)
		self.btnSelectAll.clicked.connect(JFAnmTools.onSelectAllPressed)
		
		self.btnKeySelect.clicked.connect(JFAnmTools.onKeySelectedPressed)
		self.btnKeyAll.clicked.connect(JFAnmTools.onKeyAllPressed)
		self.btnDelAnmSelect.clicked.connect(JFAnmTools.onDelAnmSelectedPressed)
		self.btnDelAnmAll.clicked.connect(JFAnmTools.onDelAnmAllPressed)
		
		#---------------
		self.mirrorLocThreshold_spb.valueChanged.connect(JFAnmTools.onExportMirrorThresholdChanged)
		self.exportPath_edit.textChanged.connect(JFAnmTools.onExportAnmPathChanged)
		self.exportPosePath_edit.textChanged.connect(JFAnmTools.onExportPosePathChanged)
		self.addMirrorInfo_btn.clicked.connect(JFAnmTools.onAddMirrorInfoPressed)
		self.autoSetMInfo_btn.clicked.connect(JFAnmTools.setMirrorInfo)
		self.removeMirrorInfo_btn.clicked.connect(JFAnmTools.onRemoveMirrorInfoPressed)
		self.expBrowse_btn.clicked.connect(JFAnmTools.onExpBrowserPressed)
		self.expAnm_btn.clicked.connect(JFAnmTools.onExpAnimaPressed)
		self.expAnmMirror_btn.clicked.connect(JFAnmTools.onExpAnimaMirrorPressed)
		self.impAnm_btn.clicked.connect(JFAnmTools.onImpAnimaPressed)
		self.expPoseBrowse_btn.clicked.connect(JFAnmTools.onPoseBrowserPressed)
		self.expPose_btn.clicked.connect(JFAnmTools.onExpPosePressed)
		self.expPoseMirror_btn.clicked.connect(JFAnmTools.onExpPoseMirrorPressed)
		self.impPose_btn.clicked.connect(JFAnmTools.onImpPosePressed)
		#---------------
		self.btnImportAnmFromFBX.clicked.connect(JFAnmTools.doImportFBXAnim)
	
	def closeEvent(self, event):
		self.deleteLater()
	#----------------------------------------------
	# METHOD
	#----------------------------------------------
	@classmethod
	def getControllerList(self):
		nameSpaceFrefix = ""
		selObjs = cmds.ls(sl=True)
		if(len(selObjs) > 0):
			sOName = selObjs[0].split(':')[-1]
			nameSpaceFrefix = selObjs[0][0:-(len(sOName))]
		
		bContinue = False
		CtrlSet = "ControllerSet"
		
		
		if not cmds.objExists(CtrlSet):
			if cmds.objExists(nameSpaceFrefix+CtrlSet):
				CtrlSet = nameSpaceFrefix+CtrlSet
				bContinue = True
			else:
				setList = cmds.ls(type='objectSet')
				for s in setList:
					if s[-13:] == 'ControllerSet':
						return cmds.listConnections(s+'.dagSetMembers')
		else:
			bContinue = True
			
		return cmds.listConnections(CtrlSet+'.dagSetMembers')
	
	@classmethod
	def goSkinPose(self, obj):
		if mel.eval('attributeExists "SPTranMtx" ' + obj) == 1:
			cmds.xform(obj, ws=False, m=cmds.getAttr(obj+".SPTranMtx"))
			
	
	@classmethod
	def convertArmAnmIK2FK(self, bRightArm, bBoth=False):
		nameSpaceFrefix = ""
		selObjs = cmds.ls(sl=True)
		if(len(selObjs) > 0):
			sOName = selObjs[0].split(':')[-1]
			nameSpaceFrefix = selObjs[0][0:-(len(sOName))]
		
		# TarSuffix = "R"
		# if not bRightArm:
		# 	TarSuffix = "L"
			
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
		
		# mel.eval("paneLayout -e -manage false $gMainPane")
		
		for f in range(0,framesCount,1):
			cmds.currentTime(f + timePrefix)
			if bBoth or bRightArm:
				tarRUpperArmTransArray.append(cmds.xform(locUpperArmR,q=True,ws=True,m=True))
				tarRForeArmTransArray.append(cmds.xform(locForeArmR,q=True,ws=True,m=True))
				tarRHandTransArray.append(cmds.xform(locHandR,q=True,ws=True,m=True))
			if bBoth or (not bRightArm):
				tarLUpperArmTransArray.append(cmds.xform(locUpperArmL,q=True,ws=True,m=True))
				tarLForeArmTransArray.append(cmds.xform(locForeArmL,q=True,ws=True,m=True))
				tarLHandTransArray.append(cmds.xform(locHandL,q=True,ws=True,m=True))
			# tarUpperArmTransArray.append(cmds.xform(locUpperArm,q=True,ws=True,m=True))
			# tarForeArmTransArray.append(cmds.xform(locForeArm,q=True,ws=True,m=True))
			# tarHandTransArray.append(cmds.xform(locHand,q=True,ws=True,m=True))
			
		for f in range(0,framesCount,1):
			tF = f + timePrefix
			cmds.currentTime(tF)
			# cmds.setKeyframe(nameSpaceFrefix+"ControlRoot." + TarSuffix + "ArmFKIKBlend", time=tF, value=0)
			
			# cmds.xform(targetUpperArm, ws=True, m=tarUpperArmTransArray[f])
			# cmds.setKeyframe(targetUpperArm + ".rx", targetUpperArm + ".ry", targetUpperArm + ".rz")
			# cmds.xform(targetForeArm, ws=True, m=tarForeArmTransArray[f])
			# cmds.setKeyframe(targetForeArm + ".rx", targetForeArm + ".ry", targetForeArm + ".rz")
			# cmds.xform(targetHand, ws=True, m=tarHandTransArray[f])
			# cmds.setKeyframe(targetHand + ".rx", targetHand + ".ry", targetHand + ".rz")
			
			if bBoth or bRightArm:
				# cmds.setKeyframe(nameSpaceFrefix+"ControlRoot.RArmFKIKBlend", time=tF, value=0)
				if f==0 or f==(framesCount-1):
					cmds.setKeyframe(nameSpaceFrefix+"ControlRoot.RArmFKIKBlend", time=tF, value=0)
				else:
					cmds.cutKey(nameSpaceFrefix+"ControlRoot.RArmFKIKBlend",time=(tF,tF))

				cmds.xform(targetUpperArmR, ws=True, m=tarRUpperArmTransArray[f])
				cmds.setKeyframe(targetUpperArmR + ".rx", targetUpperArmR + ".ry", targetUpperArmR + ".rz")
				cmds.xform(targetForeArmR, ws=True, m=tarRForeArmTransArray[f])
				cmds.setKeyframe(targetForeArmR + ".rx", targetForeArmR + ".ry", targetForeArmR + ".rz")
				cmds.xform(targetHandR, ws=True, m=tarRHandTransArray[f])
				cmds.setKeyframe(targetHandR + ".rx", targetHandR + ".ry", targetHandR + ".rz")
			if bBoth or (not bRightArm):
				# cmds.setKeyframe(nameSpaceFrefix+"ControlRoot.LArmFKIKBlend", time=tF, value=0)
				if f==0 or f==(framesCount-1):
					cmds.setKeyframe(nameSpaceFrefix+"ControlRoot.LArmFKIKBlend", time=tF, value=0)
				else:
					cmds.cutKey(nameSpaceFrefix+"ControlRoot.LArmFKIKBlend",time=(tF,tF))
				
				cmds.xform(targetUpperArmL, ws=True, m=tarLUpperArmTransArray[f])
				cmds.setKeyframe(targetUpperArmL + ".rx", targetUpperArmL + ".ry", targetUpperArmL + ".rz")
				cmds.xform(targetForeArmL, ws=True, m=tarLForeArmTransArray[f])
				cmds.setKeyframe(targetForeArmL + ".rx", targetForeArmL + ".ry", targetForeArmL + ".rz")
				cmds.xform(targetHandL, ws=True, m=tarLHandTransArray[f])
				cmds.setKeyframe(targetHandL + ".rx", targetHandL + ".ry", targetHandL + ".rz")
		
		if bBoth or bRightArm:
			cmds.filterCurve(targetUpperArmR+".rotateX",targetUpperArmR+".rotateY",targetUpperArmR+".rotateZ")
			cmds.filterCurve(targetForeArmR+".rotateX",targetForeArmR+".rotateY",targetForeArmR+".rotateZ")
			cmds.filterCurve(targetHandR+".rotateX",targetHandR+".rotateY",targetHandR+".rotateZ")
		if bBoth or (not bRightArm):
			cmds.filterCurve(targetUpperArmL+".rotateX",targetUpperArmL+".rotateY",targetUpperArmL+".rotateZ")
			cmds.filterCurve(targetForeArmL+".rotateX",targetForeArmL+".rotateY",targetForeArmL+".rotateZ")
			cmds.filterCurve(targetHandL+".rotateX",targetHandL+".rotateY",targetHandL+".rotateZ")
			
		# cmds.filterCurve("FKUpperArm_R.rotateX","FKUpperArm_R.rotateY","FKUpperArm_R.rotateZ")
		cmds.currentTime(currentTime)
		# mel.eval("paneLayout -e -manage true $gMainPane")
		
	@classmethod
	def convertArmAnmFK2IK(self, bRightArm, bBoth=False):
		nameSpaceFrefix = ""
		selObjs = cmds.ls(sl=True)
		if(len(selObjs) > 0):
			sOName = selObjs[0].split(':')[-1]
			nameSpaceFrefix = selObjs[0][0:-(len(sOName))]
		
		# TarSuffix = "R"
		# if not bRightArm:
		# 	TarSuffix = "L"
			
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
		
		# mel.eval("paneLayout -e -manage false $gMainPane")
		
		for f in range(0,framesCount,1):
			cmds.currentTime(f + timePrefix)
			
			# tarUpVTransArray.append(cmds.xform(locArmUpV,q=True,ws=True,m=True))
			# tarArmIKTransArray.append(cmds.xform(locArmIK,q=True,ws=True,m=True))
			
			if bBoth or bRightArm:
				tarRUpVTransArray.append(cmds.xform(locRArmUpV,q=True,ws=True,m=True))
				tarRArmIKTransArray.append(cmds.xform(locRArmIK,q=True,ws=True,m=True))
			if bBoth or (not bRightArm):
				tarLUpVTransArray.append(cmds.xform(locLArmUpV,q=True,ws=True,m=True))
				tarLArmIKTransArray.append(cmds.xform(locLArmIK,q=True,ws=True,m=True))
			
		# cmds.setAttr(nameSpaceFrefix+"ControlRoot." + TarSuffix + "ArmFKIKBlend",1)
		for f in range(0,framesCount,1):
			tF = f + timePrefix
			cmds.currentTime(tF)
			# cmds.setKeyframe(nameSpaceFrefix+"ControlRoot." + TarSuffix + "ArmFKIKBlend", time=tF, value=1)
			
			# cmds.xform(TargetArmIK, ws=True, m=tarArmIKTransArray[f])
			# cmds.setKeyframe(TargetArmIK + ".tx", TargetArmIK + ".ty", TargetArmIK + ".tz")
			# cmds.setKeyframe(TargetArmIK + ".rx", TargetArmIK + ".ry", TargetArmIK + ".rz")
			
			# cmds.xform(TargetUpV, ws=True, m=tarUpVTransArray[f])
			# cmds.setKeyframe(TargetUpV + ".tx", TargetUpV + ".ty", TargetUpV + ".tz")
			
			if bBoth or bRightArm:
				# cmds.setKeyframe(nameSpaceFrefix+"ControlRoot.RArmFKIKBlend", time=tF, value=1)
				if f==0 or f==(framesCount-1):
					cmds.setKeyframe(nameSpaceFrefix+"ControlRoot.RArmFKIKBlend", time=tF, value=1)
				else:
					cmds.cutKey(nameSpaceFrefix+"ControlRoot.RArmFKIKBlend",time=(tF,tF))
				
				cmds.xform(TargetArmIKR, ws=True, m=tarRArmIKTransArray[f])
				cmds.setKeyframe(TargetArmIKR + ".tx", TargetArmIKR + ".ty", TargetArmIKR + ".tz")
				cmds.setKeyframe(TargetArmIKR + ".rx", TargetArmIKR + ".ry", TargetArmIKR + ".rz")
				
				cmds.xform(TargetUpVR, ws=True, m=tarRUpVTransArray[f])
				cmds.setKeyframe(TargetUpVR + ".tx", TargetUpVR + ".ty", TargetUpVR + ".tz")
			if bBoth or (not bRightArm):
				# cmds.setKeyframe(nameSpaceFrefix+"ControlRoot.LArmFKIKBlend", time=tF, value=1)
				if f==0 or f==(framesCount-1):
					cmds.setKeyframe(nameSpaceFrefix+"ControlRoot.LArmFKIKBlend", time=tF, value=1)
				else:
					cmds.cutKey(nameSpaceFrefix+"ControlRoot.LArmFKIKBlend",time=(tF,tF))
				
				cmds.xform(TargetArmIKL, ws=True, m=tarLArmIKTransArray[f])
				cmds.setKeyframe(TargetArmIKL + ".tx", TargetArmIKL + ".ty", TargetArmIKL + ".tz")
				cmds.setKeyframe(TargetArmIKL + ".rx", TargetArmIKL + ".ry", TargetArmIKL + ".rz")
				
				cmds.xform(TargetUpVL, ws=True, m=tarLUpVTransArray[f])
				cmds.setKeyframe(TargetUpVL + ".tx", TargetUpVL + ".ty", TargetUpVL + ".tz")
		
		if bBoth or bRightArm:
			cmds.filterCurve(TargetArmIKR+".rotateX",TargetArmIKR+".rotateY",TargetArmIKR+".rotateZ")
		if bBoth or (not bRightArm):
			cmds.filterCurve(TargetArmIKL+".rotateX",TargetArmIKL+".rotateY",TargetArmIKL+".rotateZ")
			
		cmds.currentTime(currentTime)
		# mel.eval("paneLayout -e -manage true $gMainPane")
	
	@classmethod
	def convertArmPoseFK2IK(self, bRightArm):
		nameSpaceFrefix = ""
		selObjs = cmds.ls(sl=True)
		if(len(selObjs) > 0):
			sOName = selObjs[0].split(':')[-1]
			nameSpaceFrefix = selObjs[0][0:-(len(sOName))]
		
		# SrcSuffix = "R"
		TarSuffix = "R"
		if not bRightArm:
			# SrcSuffix = "L"
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
	def delAnm(self, obj):
		# mel.eval('cutKey -cl -t ":" -f ":" -at "tx" -at "ty" -at "tz" -at "rx" -at "ry" -at "rz" -at "sx" -at "sy" -at "sz" ' + obj)
		cmds.cutKey(obj)
	#----------------------------------------------
	# UI EVENTS
	#----------------------------------------------
	@classmethod
	def onKeySelectedPressed(self):
		objList = cmds.ls(sl=True)
		for obj in objList:
			self.setAnmKey(obj)
	
	@classmethod
	def onKeyAllPressed(self):
		objList = self.getControllerList()
		for obj in objList:
			self.setAnmKey(obj)
		
	@classmethod
	def onDelAnmSelectedPressed(self):
		objList = cmds.ls(sl=True)
		for obj in objList:
			self.delAnm(obj)
		
	@classmethod
	def onDelAnmAllPressed(self):
		objList = self.getControllerList()
		for obj in objList:
			self.delAnm(obj)
	
	@classmethod
	def onSelectAllPressed(self):
		cmds.select(self.getControllerList())
		
		
	@classmethod
	def onGoSkinPoseSelectedPressed(self):
		objList = cmds.ls(sl=True)
		for obj in objList:
			self.goSkinPose(obj)
		
	@classmethod
	def onGoSkinPoseAllPressed(self):
		ctrlList = self.getControllerList()
		for obj in ctrlList:
			self.goSkinPose(obj)
	
	@classmethod
	def onArmAnmIK2FKRightPressed(self):
		self.convertArmAnmFK2IK(True)
	
	@classmethod
	def onArmAnmIK2FKLeftPressed(self):
		self.convertArmAnmFK2IK(False)
		
	@classmethod
	def onArmAnmIK2FKBothPressed(self):
		self.convertArmAnmFK2IK(True, True)
		# self.convertArmAnmFK2IK(False)
	
	@classmethod
	def onArmAnmFK2IKRightPressed(self):
		self.convertArmAnmIK2FK(True)
	
	@classmethod
	def onArmAnmFK2IKLeftPressed(self):
		self.convertArmAnmIK2FK(False)
		
	@classmethod
	def onArmAnmFK2IKBothPressed(self):
		self.convertArmAnmIK2FK(True, True)
		# self.convertArmAnmIK2FK(False)
	#-----------
	@classmethod
	def onArmPoseIK2FKRightPressed(self):
		self.convertArmPoseFK2IK(True)
	
	@classmethod
	def onArmPoseIK2FKLeftPressed(self):
		self.convertArmPoseFK2IK(False)
		
	@classmethod
	def onArmPoseIK2FKBothPressed(self):
		self.convertArmPoseFK2IK(True)
		self.convertArmPoseFK2IK(False)
	
	@classmethod
	def onArmPoseFK2IKRightPressed(self):
		self.convertArmPoseIK2FK(True)
	
	@classmethod
	def onArmPoseFK2IKLeftPressed(self):
		self.convertArmPoseIK2FK(False)
		
	@classmethod
	def onArmPoseFK2IKBothPressed(self):
		self.convertArmPoseIK2FK(True)
		self.convertArmPoseIK2FK(False)
	
	@classmethod
	def onExportMirrorThresholdChanged(self, value):
		self.fMirrorThreshold = value
		cmds.optionVar(fv = ('JF_KAnm_MirrorThreshold', value))

	@classmethod
	def onExportAnmPathChanged(self):
		# print(self.exportPath_edit.text())
		cmds.optionVar(sv = ('JF_KAnm_KafPath', self.exportPath_edit.text()))
		pass

	@classmethod
	def onExportPosePathChanged(self):
		#print(self.exportPath_edit.text())
		cmds.optionVar(sv = ('JF_KAnm_KpfPath', self.exportPosePath_edit.text()))
		pass

	@classmethod
	def onAddMirrorInfoPressed(self):
		selObjects = cmds.ls(sl=True)
		for o in selObjects:
			if mel.eval('attributeExists "MirrorNode" ' + o) == 0:
				mel.eval('addAttr -ln "MirrorNode" -dt "string" ' + o)

			if mel.eval('attributeExists "InvPosX" ' + o) == 0:
				mel.eval('addAttr -ln "InvPosX" -at "bool" ' + o)

			if mel.eval('attributeExists "InvPosY" ' + o) == 0:
				mel.eval('addAttr -ln "InvPosY" -at "bool" ' + o)

			if mel.eval('attributeExists "InvPosZ" ' + o) == 0:
				mel.eval('addAttr -ln "InvPosZ" -at "bool" ' + o)

			if mel.eval('attributeExists "InvRotX" ' + o) == 0:
				mel.eval('addAttr -ln "InvRotX" -at "bool" ' + o)

			if mel.eval('attributeExists "InvRotY" ' + o) == 0:
				mel.eval('addAttr -ln "InvRotY" -at "bool" ' + o)

			if mel.eval('attributeExists "InvRotZ" ' + o) == 0:
				mel.eval('addAttr -ln "InvRotZ" -at "bool" ' + o)
				
			if mel.eval('attributeExists "MirrorRotOffset" ' + o) == 0:
				# mel.eval('addAttr -ln "MirrorRotOffset" -at "double3" ' + o)
				cmds.addAttr(o, ln="MirrorRotOffset", at="double3", k=False)
				cmds.addAttr(o, ln="MirrorRotOffsetX", at="double", p="MirrorRotOffset", k=False)
				cmds.addAttr(o, ln="MirrorRotOffsetY", at="double", p="MirrorRotOffset", k=False)
				cmds.addAttr(o, ln="MirrorRotOffsetZ", at="double", p="MirrorRotOffset", k=False)
		
		self.setMirrorInfo();

	@classmethod
	def onExpBrowserPressed(self):
		#fPath = mel.eval('fileDialog2 -fileFilter ("Animation File (*.kaf)")')
		fPath = cmds.fileDialog2(fileFilter = "Animation File (*.kaf)")
		if fPath[0]:
			self.exportPath_edit.setText(fPath[0])

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
	def onRemoveMirrorInfoPressed(self):
		selObjects = cmds.ls(sl=True)
		for o in selObjects:
			if mel.eval('attributeExists "MirrorNode" ' + o) == 1:
				cmds.deleteAttr(o+".MirrorNode")

			if mel.eval('attributeExists "InvPosX" ' + o) == 1:
				cmds.deleteAttr(o+".InvPosX")

			if mel.eval('attributeExists "InvPosY" ' + o) == 1:
				cmds.deleteAttr(o+".InvPosY")

			if mel.eval('attributeExists "InvPosZ" ' + o) == 1:
				cmds.deleteAttr(o+".InvPosZ")

			if mel.eval('attributeExists "InvRotX" ' + o) == 1:
				cmds.deleteAttr(o+".InvRotX")

			if mel.eval('attributeExists "InvRotY" ' + o) == 1:
				cmds.deleteAttr(o+".InvRotY")

			if mel.eval('attributeExists "InvRotZ" ' + o) == 1:
				cmds.deleteAttr(o+".InvRotZ")

	@classmethod
	def onPoseBrowserPressed(self):
		fPath = cmds.fileDialog2(fileFilter = "Pose File (*.kpf)")
		if fPath[0]:
			self.exportPosePath_edit.setText(fPath[0])

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

	# ----------------------------------------------
	# functions
	# -----------------------------------------------
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
		
		text_file.close()		

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

			# Vx1 = [trans01[0],trans01[1],trans01[2]]
			# Vy1 = [trans01[4],trans01[5],trans01[6]]
			# Vz1 = [trans01[8],trans01[9],trans01[10]]

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
	#===================
	@classmethod
	def getBoneByHIkId(self, cha, id):
		HIK_Node = mel.eval('GetHIKNode("' + cha + '",' + str(id) + ');')
		if len(HIK_Node) > 0:
			tarBone = cmds.listConnections(HIK_Node[0], d=False, s=True)
			if tarBone:
				return tarBone[0]
			else:
				return None
		else:
			return None

	@classmethod
	def doImportFBXAnim(self):
		nameSpaceFrefix = ""
		selObjs = cmds.ls(sl=True)
		if(len(selObjs) > 0):
			sOName = selObjs[0].split(':')[-1]
			nameSpaceFrefix = selObjs[0][0:-(len(sOName))]

		fPath = cmds.fileDialog2(fileFilter = "FBX File (*.fbx)",fm=1)
		if fPath[0]:
			# cmds.file(fPath[0],i=True,type="FBX",iv=True,ra=True, mnc=False)
			mel.eval('FBXImportFillTimeline -v true;')
			mel.eval('FBXImportGenerateLog -v false;')
			mel.eval('FBXImportSkeletonDefinitionsAs -v "humanik";')
			mel.eval('FBXImportSkins -v false;')
			res = mel.eval('FBXImport -f "' + fPath[0] + '";')

			if res=="Success":
				oriTopList = cmds.ls(dag=True)
				oriAutoKeyState  = cmds.autoKeyframe(q=True,state=True)
				cmds.autoKeyframe(state=False)

				charList = cmds.ls(type="HIKCharacterNode")
				if len(charList) > 0:
					startTime = int(cmds.playbackOptions(q=True, min=True))
					endTime = int(cmds.playbackOptions(q=True, max=True))
					currentTime = int(cmds.currentTime(q=True))
					timePrefix = startTime
					framesCount = endTime - startTime + 1
					cmds.currentTime(startTime)
					cmds.waitCursor(state=True)
					#==========================================
					character = charList[0]
					mel.eval('hikCreateCharacterControlsDockableWindow;')
					mel.eval('hikSetCurrentCharacter "' + character + '";')
					bHasControlRig = mel.eval(' hikHasControlRig("' + character + '");')
					
					character = mel.eval("hikGetCurrentCharacter();")
					mel.eval('hikSelectLastTab( "' + character + '");')
					mel.eval('hikSetCurrentSourceFromCharacter("' + character + '");')
					mel.eval('hikUpdateSourceList();')
					mel.eval('hikDefinitionUpdateCharacterLists;')
					mel.eval('hikDefinitionUpdateBones;')

					mel.eval('hikSetCurrentSource("Stance");')
					mel.eval('hikEnableCharacter("' + character + '", 2 );')
					labelControlRig = mel.eval('uiRes("m_hikGlobalUtils.kControlRig")')
					labelStance = mel.eval('uiRes("m_hikGlobalUtils.kStance")')

					if bHasControlRig == 1:
						mel.eval('hikSetRigInput( "' + character + '");')
						mel.eval('hikSetLiveState("' + character + '", 1 );')
						mel.eval('hikSelectControlRigTab();')
					else:
						mel.eval('hikCreateControlRig();')

					# mel.eval('hikSetStanceInput("' + character + '");')

					mel.eval('hikUpdateLiveConnectionUI;')
					mel.eval('hikUpdateContextualUI();')

					cmds.currentTime(startTime+1)
					cmds.currentTime(startTime)

					#==================
					mcChestList = []
					for i in range(23,32):
						bJnt = self.getBoneByHIkId(character, i)
						if bJnt:
							mcChestList.append(bJnt)
						else:
							break

					mcRoot = self.getBoneByHIkId(character, 0)
					mcHip = self.getBoneByHIkId(character, 1)
					mcWaist = self.getBoneByHIkId(character, 8)
					mcChest = self.getBoneByHIkId(character, 23)
					mcChest1 = self.getBoneByHIkId(character, 24)
					mcNeck = self.getBoneByHIkId(character, 20)
					mcHead = self.getBoneByHIkId(character, 15)
					mcShoulderL = self.getBoneByHIkId(character, 18)
					mcShoulderR = self.getBoneByHIkId(character, 19)
					mcArmUpperL = self.getBoneByHIkId(character, 9)
					mcArmUpperR = self.getBoneByHIkId(character, 12)
					mcArmForeL = self.getBoneByHIkId(character, 10)
					mcArmForeR = self.getBoneByHIkId(character, 13)
					mcHandL = self.getBoneByHIkId(character, 11)
					mcHandR = self.getBoneByHIkId(character, 14)
					mcThighL = self.getBoneByHIkId(character, 2)
					mcThighR = self.getBoneByHIkId(character, 5)
					mcCalfL = self.getBoneByHIkId(character, 3)
					mcCalfR = self.getBoneByHIkId(character, 6)
					mcFootL = self.getBoneByHIkId(character, 4)
					mcFootR = self.getBoneByHIkId(character, 7)
					mcToeL = self.getBoneByHIkId(character, 16)
					mcToeR = self.getBoneByHIkId(character, 17)
					#--------------
					cmds.setAttr(nameSpaceFrefix+'ControlRoot.LArmFKIKBlend', 1)
					cmds.setAttr(nameSpaceFrefix+'ControlRoot.RArmFKIKBlend', 1)
					#--------------
					cmds.parentConstraint(mcHip, nameSpaceFrefix + "Hip", mo=True)
					cmds.orientConstraint(mcWaist, nameSpaceFrefix + "Waist", mo=True)
					# cmds.orientConstraint(mcChest, nameSpaceFrefix + "Chest", mo=True)
					ChestCount = len(mcChestList)
					strChestList = '"' + mcChestList[0] + '"'

					if ChestCount > 1:
						for i in range(1, ChestCount):
							strChestList = strChestList + ' "' + mcChestList[i] + '"'

					ChestRC = mel.eval('orientConstraint -mo ' + strChestList + ' ' + nameSpaceFrefix + 'Chest' )
					cmds.setAttr(ChestRC[0] + ".interpType", 2)

					cmds.orientConstraint(mcChestList[ChestCount - 1], nameSpaceFrefix + "ChestU", mo=True)
					# cmds.orientConstraint(mcChest1, nameSpaceFrefix + "ChestU", mo=True)
					cmds.orientConstraint(mcNeck, nameSpaceFrefix + "Neck", mo=True)
					cmds.orientConstraint(mcHead, nameSpaceFrefix + "Head", mo=True)
					cmds.orientConstraint(mcShoulderL, nameSpaceFrefix + "Shoulder_L", mo=True)
					cmds.orientConstraint(mcShoulderR, nameSpaceFrefix + "Shoulder_R", mo=True)

					#------------------------------LArmCenLoc,LArmStrUpVLoc,ArmUpVLockPointL
					LArmCenLoc = cmds.spaceLocator(name="LArmCenLoc")[0]
					LArmUpVLoc = cmds.spaceLocator(name="LArmUpVLoc")[0]
					UpArmPosL = cmds.xform(mcArmUpperL,q=True,ws=True,t=True)
					FoArmPosL = cmds.xform(mcArmForeL,q=True,ws=True,t=True)
					HandPosL = cmds.xform(mcHandL,q=True,ws=True,t=True)
					UpArmLengthL = getDistance(UpArmPosL, FoArmPosL)
					FoArmLengthL = getDistance(FoArmPosL, HandPosL)
					cmds.pointConstraint(mcArmUpperL, mcHandL, LArmCenLoc)
					cmds.aimConstraint(mcArmUpperL, LArmCenLoc, aim=[0,1,0], u=[1,0,0], wut="object", wuo=mcArmForeL)
					cmds.parent(LArmUpVLoc, LArmCenLoc)
					cmds.xform(LArmUpVLoc,ws=True, m=cmds.xform(LArmCenLoc,q=True,ws=True,m=True))
					cmds.setAttr(LArmUpVLoc+".tx", (UpArmLengthL + FoArmLengthL)*0.75)

					LUpArmUpVLoc = cmds.spaceLocator(name="LUpArmUpVLoc")[0]
					LFoArmUpVLoc = cmds.spaceLocator(name="LFoArmUpVLoc")[0]
					LArmStrUpVLoc = cmds.spaceLocator(name="LArmStrUpVLoc")[0]
					cmds.xform(LUpArmUpVLoc, ws=True, t=cmds.xform(LArmUpVLoc,q=True,ws=True,t=True))
					cmds.xform(LFoArmUpVLoc, ws=True, t=cmds.xform(LArmUpVLoc,q=True,ws=True,t=True))
					cmds.parent(LUpArmUpVLoc, mcArmUpperL)
					cmds.parent(LFoArmUpVLoc, mcArmForeL)
					cmds.pointConstraint(LUpArmUpVLoc,LFoArmUpVLoc,LArmStrUpVLoc)


					mcUpArmXAxisNodeL = cmds.shadingNode("vectorProduct",au=True)
					cmds.setAttr(mcUpArmXAxisNodeL+".operation",3)
					cmds.setAttr(mcUpArmXAxisNodeL+".input1",1,0,0,type="float3")
					cmds.connectAttr(mcArmUpperL + ".worldMatrix[0]", mcUpArmXAxisNodeL+".matrix",f=True)
					mcFoArmXAxisNodeL = cmds.shadingNode("vectorProduct",au=True)
					cmds.setAttr(mcFoArmXAxisNodeL+".operation",3)
					cmds.setAttr(mcFoArmXAxisNodeL+".input1",1,0,0,type="float3")
					cmds.connectAttr(mcArmForeL + ".worldMatrix[0]", mcFoArmXAxisNodeL+".matrix",f=True)
					
					dotArmAngleNodeL = cmds.shadingNode("vectorProduct",au=True)
					cmds.setAttr(dotArmAngleNodeL+".operation",1)
					cmds.connectAttr(mcUpArmXAxisNodeL + ".output", dotArmAngleNodeL+".input1",f=True)
					cmds.connectAttr(mcFoArmXAxisNodeL + ".output", dotArmAngleNodeL+".input2",f=True)

					cosMinus1NodeL = cmds.shadingNode("plusMinusAverage",au=True)
					cmds.setAttr(cosMinus1NodeL+".operation",2)
					cmds.connectAttr(dotArmAngleNodeL + ".outputX", cosMinus1NodeL+".input1D[0]",f=True)
					mel.eval('AEnewNonNumericMultiAddNewItem("' + cosMinus1NodeL + '","input1D")')
					cmds.setAttr(cosMinus1NodeL+'.input1D[1]', 1)

					cosScaleNodeL = cmds.shadingNode("multiplyDivide",au=True)
					cmds.setAttr(cosScaleNodeL+".operation",1)
					cmds.connectAttr(cosMinus1NodeL + ".output1D", cosScaleNodeL+".input1X",f=True)
					cmds.setAttr(cosScaleNodeL+".input2X", 65.823)

					cosAdd1NodeL = cmds.shadingNode("plusMinusAverage",au=True)
					cmds.setAttr(cosAdd1NodeL+".operation",1)
					cmds.connectAttr(cosScaleNodeL + ".outputX", cosAdd1NodeL+".input1D[0]",f=True)
					mel.eval('AEnewNonNumericMultiAddNewItem("' + cosAdd1NodeL + '","input1D")')
					cmds.setAttr(cosAdd1NodeL+'.input1D[1]', 2)


					dotClampL = cmds.shadingNode("clamp", au=True)
					cmds.connectAttr(cosAdd1NodeL + ".output1D", dotClampL+".inputR",f=True)
					cmds.setAttr(dotClampL+'.maxR', 1)

					dotClampOneMinusL = cmds.shadingNode("plusMinusAverage",au=True)
					cmds.setAttr(dotClampOneMinusL+".operation",2)
					mel.eval('AEnewNonNumericMultiAddNewItem("' + dotClampOneMinusL + '","input1D")')
					mel.eval('AEnewNonNumericMultiAddNewItem("' + dotClampOneMinusL + '","input1D")')
					cmds.connectAttr(dotClampL + ".outputR", dotClampOneMinusL+".input1D[1]",f=True)
					cmds.setAttr(dotClampOneMinusL+'.input1D[0]', 1)

					ArmUpVLockPointL = cmds.spaceLocator(name="ArmUpVLockPointL")[0]
					AUVPC = cmds.pointConstraint(LArmStrUpVLoc, LArmUpVLoc, ArmUpVLockPointL)
					cmds.connectAttr(dotClampL + ".outputR", AUVPC[0] + "." + LArmStrUpVLoc + "W0",f=True)
					cmds.connectAttr(dotClampOneMinusL + ".output1D", AUVPC[0] + "." + LArmUpVLoc + "W1",f=True)

					cmds.parentConstraint(mcHandL, nameSpaceFrefix + 'HandIK_L', mo=True)
					cmds.pointConstraint(ArmUpVLockPointL, nameSpaceFrefix + 'ArmUpV_L')
					
					#-----------Right---------------
					RArmCenLoc = cmds.spaceLocator(name="RArmCenLoc")[0]
					RArmUpVLoc = cmds.spaceLocator(name="RArmUpVLoc")[0]
					UpArmPosR = cmds.xform(mcArmUpperR,q=True,ws=True,t=True)
					FoArmPosR = cmds.xform(mcArmForeR,q=True,ws=True,t=True)
					HandPosR = cmds.xform(mcHandR,q=True,ws=True,t=True)
					UpArmLengthR = getDistance(UpArmPosR, FoArmPosR)
					FoArmLengthR = getDistance(FoArmPosR, HandPosR)
					cmds.pointConstraint(mcArmUpperR, mcHandR, RArmCenLoc)
					cmds.aimConstraint(mcArmUpperR, RArmCenLoc, aim=[0,1,0], u=[1,0,0], wut="object", wuo=mcArmForeR)
					cmds.parent(RArmUpVLoc, RArmCenLoc)
					cmds.xform(RArmUpVLoc,ws=True, m=cmds.xform(RArmCenLoc,q=True,ws=True,m=True))
					cmds.setAttr(RArmUpVLoc+".tx", (UpArmLengthR + FoArmLengthR)*0.75)

					RUpArmUpVLoc = cmds.spaceLocator(name="RUpArmUpVLoc")[0]
					RFoArmUpVLoc = cmds.spaceLocator(name="RFoArmUpVLoc")[0]
					RArmStrUpVLoc = cmds.spaceLocator(name="RArmStrUpVLoc")[0]
					cmds.xform(RUpArmUpVLoc, ws=True, t=cmds.xform(RArmUpVLoc,q=True,ws=True,t=True))
					cmds.xform(RFoArmUpVLoc, ws=True, t=cmds.xform(RArmUpVLoc,q=True,ws=True,t=True))
					cmds.parent(RUpArmUpVLoc, mcArmUpperR)
					cmds.parent(RFoArmUpVLoc, mcArmForeR)
					cmds.pointConstraint(RUpArmUpVLoc,RFoArmUpVLoc,RArmStrUpVLoc)


					mcUpArmXAxisNodeR = cmds.shadingNode("vectorProduct",au=True)
					cmds.setAttr(mcUpArmXAxisNodeR+".operation",3)
					cmds.setAttr(mcUpArmXAxisNodeR+".input1",1,0,0,type="float3")
					cmds.connectAttr(mcArmUpperR + ".worldMatrix[0]", mcUpArmXAxisNodeR+".matrix",f=True)
					mcFoArmXAxisNodeR = cmds.shadingNode("vectorProduct",au=True)
					cmds.setAttr(mcFoArmXAxisNodeR+".operation",3)
					cmds.setAttr(mcFoArmXAxisNodeR+".input1",1,0,0,type="float3")
					cmds.connectAttr(mcArmForeR + ".worldMatrix[0]", mcFoArmXAxisNodeR+".matrix",f=True)
					
					dotArmAngleNodeR = cmds.shadingNode("vectorProduct",au=True)
					cmds.setAttr(dotArmAngleNodeR+".operation",1)
					cmds.connectAttr(mcUpArmXAxisNodeR + ".output", dotArmAngleNodeR+".input1",f=True)
					cmds.connectAttr(mcFoArmXAxisNodeR + ".output", dotArmAngleNodeR+".input2",f=True)

					cosMinus1NodeR = cmds.shadingNode("plusMinusAverage",au=True)
					cmds.setAttr(cosMinus1NodeR+".operation",2)
					cmds.connectAttr(dotArmAngleNodeR + ".outputX", cosMinus1NodeR+".input1D[0]",f=True)
					mel.eval('AEnewNonNumericMultiAddNewItem("' + cosMinus1NodeR + '","input1D")')
					cmds.setAttr(cosMinus1NodeR+'.input1D[1]', 1)

					cosScaleNodeR = cmds.shadingNode("multiplyDivide",au=True)
					cmds.setAttr(cosScaleNodeR+".operation",1)
					cmds.connectAttr(cosMinus1NodeR + ".output1D", cosScaleNodeR+".input1X",f=True)
					cmds.setAttr(cosScaleNodeR+".input2X", 65.823)

					cosAdd1NodeR = cmds.shadingNode("plusMinusAverage",au=True)
					cmds.setAttr(cosAdd1NodeR+".operation",1)
					cmds.connectAttr(cosScaleNodeR + ".outputX", cosAdd1NodeR+".input1D[0]",f=True)
					mel.eval('AEnewNonNumericMultiAddNewItem("' + cosAdd1NodeR + '","input1D")')
					cmds.setAttr(cosAdd1NodeR+'.input1D[1]', 2)


					dotClampR = cmds.shadingNode("clamp", au=True)
					cmds.connectAttr(cosAdd1NodeR + ".output1D", dotClampR+".inputR",f=True)
					cmds.setAttr(dotClampR+'.maxR', 1)

					dotClampOneMinusR = cmds.shadingNode("plusMinusAverage",au=True)
					cmds.setAttr(dotClampOneMinusR+".operation",2)
					mel.eval('AEnewNonNumericMultiAddNewItem("' + dotClampOneMinusR + '","input1D")')
					mel.eval('AEnewNonNumericMultiAddNewItem("' + dotClampOneMinusR + '","input1D")')
					cmds.connectAttr(dotClampR + ".outputR", dotClampOneMinusR+".input1D[1]",f=True)
					cmds.setAttr(dotClampOneMinusR+'.input1D[0]', 1)

					ArmUpVLockPointR = cmds.spaceLocator(name="ArmUpVLockPointR")[0]
					AUVPC = cmds.pointConstraint(RArmStrUpVLoc, RArmUpVLoc, ArmUpVLockPointR)
					cmds.connectAttr(dotClampR + ".outputR", AUVPC[0] + "." + RArmStrUpVLoc + "W0",f=True)
					cmds.connectAttr(dotClampOneMinusR + ".output1D", AUVPC[0] + "." + RArmUpVLoc + "W1",f=True)

					cmds.parentConstraint(mcHandR, nameSpaceFrefix + 'HandIK_R', mo=True)
					cmds.pointConstraint(ArmUpVLockPointR, nameSpaceFrefix + 'ArmUpV_R')
					#------------------


					LLegCenLoc = cmds.spaceLocator(name="LLegCenLoc")[0]
					LLegUpVLoc = cmds.spaceLocator(name="LLegUpVLoc")[0]
					ThighPosL = cmds.xform(mcThighL,q=True,ws=True,t=True)
					CalfPosL = cmds.xform(mcCalfL,q=True,ws=True,t=True)
					FootPosL = cmds.xform(mcFootL,q=True,ws=True,t=True)
					ThighLengthL = getDistance(ThighPosL, CalfPosL)
					CalfLengthL = getDistance(CalfPosL, FootPosL)
					cmds.pointConstraint(mcThighL, mcFootL, LLegCenLoc)
					cmds.aimConstraint(mcThighL, LLegCenLoc, aim=[0,1,0], u=[1,0,0], wut="object", wuo=mcCalfL)
					cmds.parent(LLegUpVLoc, LLegCenLoc)
					cmds.xform(LLegUpVLoc,ws=True, m=cmds.xform(LLegCenLoc,q=True,ws=True,m=True))
					cmds.setAttr(LLegUpVLoc+".tx", (ThighLengthL + CalfLengthL)*0.75)

					cmds.parentConstraint(mcToeL, nameSpaceFrefix + "Foot_L", mo=True)
					cmds.orientConstraint(mcFootL, nameSpaceFrefix + "Footpad_L", mo=True)
					cmds.pointConstraint(LLegUpVLoc, nameSpaceFrefix + "LegUpV_L")
					#-------------------
					RLegCenLoc = cmds.spaceLocator(name="RLegCenLoc")[0]
					RLegUpVLoc = cmds.spaceLocator(name="RLegUpVLoc")[0]
					ThighPosR = cmds.xform(mcThighR,q=True,ws=True,t=True)
					CalfPosR = cmds.xform(mcCalfR,q=True,ws=True,t=True)
					FootPosR = cmds.xform(mcFootR,q=True,ws=True,t=True)
					ThighLengthR = getDistance(ThighPosR, CalfPosR)
					CalfLengthR = getDistance(CalfPosR, FootPosR)
					cmds.pointConstraint(mcThighR, mcFootR, RLegCenLoc)
					cmds.aimConstraint(mcThighR, RLegCenLoc, aim=[0,1,0], u=[1,0,0], wut="object", wuo=mcCalfR)
					cmds.parent(RLegUpVLoc, RLegCenLoc)
					cmds.xform(RLegUpVLoc,ws=True, m=cmds.xform(RLegCenLoc,q=True,ws=True,m=True))
					cmds.setAttr(RLegUpVLoc+".tx", (ThighLengthR + CalfLengthR)*0.75)

					cmds.parentConstraint(mcToeR, nameSpaceFrefix + "Foot_R", mo=True)
					cmds.orientConstraint(mcFootR, nameSpaceFrefix + "Footpad_R", mo=True)
					cmds.pointConstraint(RLegUpVLoc, nameSpaceFrefix + "LegUpV_R")
					#================================================
					

					cmds.cutKey(nameSpaceFrefix + "ControlRoot")
					# cmds.setAttr(nameSpaceFrefix + "ControlRoot.RArmFKIKBlend", 0)
					# cmds.setAttr(nameSpaceFrefix + "ControlRoot.LArmFKIKBlend", 0)
					cmds.setAttr(nameSpaceFrefix + "ControlRoot.RootMotionSideCtrl", 1)
					cmds.setAttr(nameSpaceFrefix + "ControlRoot.RootMotionSideCtrl", 1)

					
					mel.eval('hikEnableCharacter("' + character + '", 2 );')
					cmds.currentTime(startTime+1)
					cmds.currentTime(startTime)

					CtrlObjList = ["Hip","Waist","Chest","ChestU","Neck","Head","Shoulder_L","Shoulder_R",
									"HandIK_L","ArmUpV_L","HandIK_R","ArmUpV_R","Foot_L","Foot_R","Footpad_L","Footpad_R","LegUpV_L","LegUpV_R"]
					# -------------
					for o in CtrlObjList:
						self.setAnmKey(nameSpaceFrefix + o)
					cmds.setAttr(nameSpaceFrefix + "Hip.blendParent1", 1)
					cmds.setAttr(nameSpaceFrefix + "Waist.blendOrient1", 1)
					cmds.setAttr(nameSpaceFrefix + "Chest.blendOrient1", 1)
					cmds.setAttr(nameSpaceFrefix + "ChestU.blendOrient1", 1)
					cmds.setAttr(nameSpaceFrefix + "Neck.blendOrient1", 1)
					cmds.setAttr(nameSpaceFrefix + "Head.blendOrient1", 1)
					cmds.setAttr(nameSpaceFrefix + "Shoulder_L.blendOrient1", 1)
					cmds.setAttr(nameSpaceFrefix + "Shoulder_R.blendOrient1", 1)
					cmds.setAttr(nameSpaceFrefix + "HandIK_L.blendParent1", 1)
					cmds.setAttr(nameSpaceFrefix + "ArmUpV_L.blendPoint1", 1)
					cmds.setAttr(nameSpaceFrefix + "HandIK_R.blendParent1", 1)
					cmds.setAttr(nameSpaceFrefix + "ArmUpV_R.blendPoint1", 1)
					# cmds.setAttr(nameSpaceFrefix + "FKUpperArm_L.blendOrient1", 1)
					# cmds.setAttr(nameSpaceFrefix + "FKUpperArm_R.blendOrient1", 1)
					# cmds.setAttr(nameSpaceFrefix + "FKForeArm_L.blendOrient1", 1)
					# cmds.setAttr(nameSpaceFrefix + "FKForeArm_R.blendOrient1", 1)
					# cmds.setAttr(nameSpaceFrefix + "FKHand_L.blendOrient1", 1)
					# cmds.setAttr(nameSpaceFrefix + "FKHand_R.blendOrient1", 1)
					cmds.setAttr(nameSpaceFrefix + "Foot_L.blendParent1", 1)
					cmds.setAttr(nameSpaceFrefix + "Foot_R.blendParent1", 1)
					cmds.setAttr(nameSpaceFrefix + "Footpad_L.blendOrient1", 1)
					cmds.setAttr(nameSpaceFrefix + "Footpad_R.blendOrient1", 1)
					cmds.setAttr(nameSpaceFrefix + "LegUpV_L.blendPoint1", 1)
					cmds.setAttr(nameSpaceFrefix + "LegUpV_R.blendPoint1", 1)
					# -----------------
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

					tarRUpperArmRotArray = []
					tarRForeArmRotArray = []
					tarRHandRotArray = []
					tarLUpperArmRotArray = []
					tarLForeArmRotArray = []
					tarLHandRotArray = []

					for f in range(0,framesCount,1):
						cmds.currentTime(f + timePrefix)
						for o in CtrlObjList:
							self.setAnmKey(nameSpaceFrefix + o)

						# tarLUpperArmRotArray.append(cmds.xform(locUpperArmL,q=True,ws=True,ro=True))
						# tarLForeArmRotArray.append(cmds.xform(locForeArmL,q=True,ws=True,ro=True))
						# tarLHandRotArray.append(cmds.xform(locHandL,q=True,ws=True,ro=True))

						# tarRUpperArmRotArray.append(cmds.xform(locUpperArmR,q=True,ws=True,ro=True))
						# tarRForeArmRotArray.append(cmds.xform(locForeArmR,q=True,ws=True,ro=True))
						# tarRHandRotArray.append(cmds.xform(locHandR,q=True,ws=True,ro=True))
						cmds.xform(targetUpperArmL, ws=True, m=cmds.xform(locUpperArmL,q=True,ws=True,m=True))
						tarLUpperArmRotArray.append(cmds.getAttr(targetUpperArmL+".rotate")[0])
						# cmds.setKeyframe(targetUpperArmL + ".rx", targetUpperArmL + ".ry", targetUpperArmL + ".rz")
						cmds.xform(targetForeArmL, ws=True, m=cmds.xform(locForeArmL,q=True,ws=True,m=True))
						tarLForeArmRotArray.append(cmds.getAttr(targetForeArmL+".rotate")[0])
						# cmds.setKeyframe(targetForeArmL + ".rx", targetForeArmL + ".ry", targetForeArmL + ".rz")
						cmds.xform(targetHandL, ws=True, m=cmds.xform(locHandL,q=True,ws=True,m=True))
						tarLHandRotArray.append(cmds.getAttr(targetHandL+".rotate")[0])
						# cmds.setKeyframe(targetHandL + ".rx", targetHandL + ".ry", targetHandL + ".rz")

						cmds.xform(targetUpperArmR, ws=True, m=cmds.xform(locUpperArmR,q=True,ws=True,m=True))
						tarRUpperArmRotArray.append(cmds.getAttr(targetUpperArmR+".rotate")[0])
						# cmds.setKeyframe(targetUpperArmR + ".rx", targetUpperArmR + ".ry", targetUpperArmR + ".rz")
						cmds.xform(targetForeArmR, ws=True, m=cmds.xform(locForeArmR,q=True,ws=True,m=True))
						tarRForeArmRotArray.append(cmds.getAttr(targetForeArmR+".rotate")[0])
						# cmds.setKeyframe(targetForeArmR + ".rx", targetForeArmR + ".ry", targetForeArmR + ".rz")
						cmds.xform(targetHandR, ws=True, m=cmds.xform(locHandR,q=True,ws=True,m=True))
						tarRHandRotArray.append(cmds.getAttr(targetHandR+".rotate")[0])
						# cmds.setKeyframe(targetHandR + ".rx", targetHandR + ".ry", targetHandR + ".rz")

					# cmds.setKeyframe(nameSpaceFrefix + objList[i] + ".translateX", time=(startFrame+f), value=AnimData[tKey]['Position'][i][0])
					for f in range(0,framesCount,1):
						t = f + timePrefix
						cmds.setKeyframe(targetUpperArmL + ".rx", time=t, value=tarLUpperArmRotArray[f][0])
						cmds.setKeyframe(targetUpperArmL + ".ry", time=t, value=tarLUpperArmRotArray[f][1])
						cmds.setKeyframe(targetUpperArmL + ".rz", time=t, value=tarLUpperArmRotArray[f][2])
						cmds.setKeyframe(targetForeArmL + ".rx", time=t, value=tarLForeArmRotArray[f][0])
						cmds.setKeyframe(targetForeArmL + ".ry", time=t, value=tarLForeArmRotArray[f][1])
						cmds.setKeyframe(targetForeArmL + ".rz", time=t, value=tarLForeArmRotArray[f][2])
						cmds.setKeyframe(targetHandL + ".rx", time=t, value=tarLHandRotArray[f][0])
						cmds.setKeyframe(targetHandL + ".ry", time=t, value=tarLHandRotArray[f][1])
						cmds.setKeyframe(targetHandL + ".rz", time=t, value=tarLHandRotArray[f][2])
						cmds.setKeyframe(targetUpperArmR + ".rx", time=t, value=tarRUpperArmRotArray[f][0])
						cmds.setKeyframe(targetUpperArmR + ".ry", time=t, value=tarRUpperArmRotArray[f][1])
						cmds.setKeyframe(targetUpperArmR + ".rz", time=t, value=tarRUpperArmRotArray[f][2])
						cmds.setKeyframe(targetForeArmR + ".rx", time=t, value=tarRForeArmRotArray[f][0])
						cmds.setKeyframe(targetForeArmR + ".ry", time=t, value=tarRForeArmRotArray[f][1])
						cmds.setKeyframe(targetForeArmR + ".rz", time=t, value=tarRForeArmRotArray[f][2])
						cmds.setKeyframe(targetHandR + ".rx", time=t, value=tarRHandRotArray[f][0])
						cmds.setKeyframe(targetHandR + ".ry", time=t, value=tarRHandRotArray[f][1])
						cmds.setKeyframe(targetHandR + ".rz", time=t, value=tarRHandRotArray[f][2])

					cmds.delete(character, mcRoot, RLegCenLoc, LLegCenLoc, LArmCenLoc, LArmStrUpVLoc, ArmUpVLockPointL, RArmCenLoc, RArmStrUpVLoc, ArmUpVLockPointR)
					try:
						cmds.delete(character+'_Ctrl_Reference')
					except Exception, e:
						raise e

					newTopList = cmds.ls(dag=True)
					for r in newTopList:
						bGotSame = False
						for o in oriTopList:
							if r == o:
								bGotSame = True
								break
						if not bGotSame:
							cmds.delete(r)

					for o in CtrlObjList:
						cmds.filterCurve(nameSpaceFrefix+o+".rotateX",nameSpaceFrefix+o+".rotateY",nameSpaceFrefix+o+".rotateZ")

					cmds.filterCurve(targetUpperArmL+".rotateX",targetUpperArmL+".rotateY",targetUpperArmL+".rotateZ")
					cmds.filterCurve(targetForeArmL+".rotateX",targetForeArmL+".rotateY",targetForeArmL+".rotateZ")
					cmds.filterCurve(targetHandL+".rotateX",targetHandL+".rotateY",targetHandL+".rotateZ")
					cmds.filterCurve(targetUpperArmR+".rotateX",targetUpperArmR+".rotateY",targetUpperArmR+".rotateZ")
					cmds.filterCurve(targetForeArmR+".rotateX",targetForeArmR+".rotateY",targetForeArmR+".rotateZ")
					cmds.filterCurve(targetHandR+".rotateX",targetHandR+".rotateY",targetHandR+".rotateZ")

					cmds.setAttr(nameSpaceFrefix + "ControlRoot.RArmFKIKBlend", 0)
					cmds.setAttr(nameSpaceFrefix + "ControlRoot.LArmFKIKBlend", 0)

					cmds.currentTime(startTime)
					cmds.autoKeyframe(state=oriAutoKeyState)
					cmds.waitCursor(state=False)
		
#===================================================================
if __name__ == "__main__":
	jfAnim_ui = JFAnmTools()