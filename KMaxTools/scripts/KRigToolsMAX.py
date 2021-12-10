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


def getChainObj(obj, bOnlyFirst):
	listChain = []
	listChain.append(obj)
	if len(obj.children) > 0:
		if bOnlyFirst:
			listChain += getChainObj(obj.children[0], bOnlyFirst)
		else:
			for c in obj.children:
				listChain += getChainObj(c, bOnlyFirst)
	return listChain

def getConnectChain(objA, objB):
	listChain = [objB]
	serchNode = objB
	
	bCheck = True
	bNeed2nd = False
	while bCheck:
		tmpParent = serchNode.parent
		if tmpParent == None:
			bCheck = False
			bNeed2nd = True
		elif tmpParent == objA:
			listChain.append(objA)
			bCheck = False
		else:
			listChain.append(tmpParent)
			serchNode = tmpParent
	if bNeed2nd:
		listChain = [objA]
		serchNode = objA
		bCheck = True
		while bCheck:
			tmpParent = serchNode.parent
			if tmpParent == None:
				bCheck = False
			elif tmpParent == objB:
				listChain.append(objB)
				bCheck = False
			else:
				listChain.append(tmpParent)
				serchNode = tmpParent
	listChain.reverse()
	return listChain

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
		return rt.matrix3(rt.point3( m[0][0],-m[0][1],-m[0][2]), 
						  rt.point3( m[1][0],-m[1][1],-m[1][2]), 
						  rt.point3( m[2][0],-m[2][1],-m[2][2]), 
						  rt.point3(-m[3][0], m[3][1], m[3][2]))

def getFilePathInfo(fullPath):
	DiskPath, fullFileName = os.path.split(fullPath)
	FileName, FileType = os.path.splitext(fullFileName)
	
	if DiskPath[-1] != '\\':
		DiskPath += '\\'

	return [DiskPath,FileName,FileType]

def flipSlash(str):
	pass
# def max_main_window():
# 	main_window_ptr = MaxPlus.GetQMaxMainWindow()
# 	return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class KRigTools(QtWidgets.QDialog):
	RootPath = ''
	uiScale = rt.Point2(1,1)

	width = 300
	height = 200

	spnSPIKSegNum = QtWidgets.QSpinBox()
	spnSPIKCtrlSize = QtWidgets.QDoubleSpinBox()
	spnBoneWidth = QtWidgets.QDoubleSpinBox()
	spnBoneHeight = QtWidgets.QDoubleSpinBox()
	spnBoneTaper = QtWidgets.QDoubleSpinBox()

	cbUseSoftIK = QtWidgets.QCheckBox('Soft IK')

	def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
		super(KRigTools, self).__init__(parent)
		# self.closeExistingWindow()
		self.RootPath = os.path.dirname(sys.argv[0]) + '\\'
		self.uiScale = rt.sysInfo.DesktopSizeUnscaled / rt.sysInfo.DesktopSize

		self.width *= self.uiScale.x
		self.height *= self.uiScale.y
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
		self.setWindowTitle('K Rig Tools v2.0')
		self.setWindowFlags(QtCore.Qt.Tool)
		self.setMinimumSize(self.width, self.height)
		self.setMaximumSize(self.width, self.height)

		self.create_controls()
		self.create_layout()
		self.create_connection()
		self.readConfig()
		self.show()

	def readConfig(self):
		pass
	
	def create_controls(self):
		usrImgFold = self.RootPath + 'icons\\'

		self.btnCreateBipedGuide = QtWidgets.QPushButton('建立Biped Guide')
		self.btnCreateBipedControl = QtWidgets.QPushButton('生成Biped Control')

		self.btnAssignMirrorInfo = QtWidgets.QPushButton('套用\nMirror Info.')
		self.btnRemoveMirrorInfo = QtWidgets.QPushButton('移除\nMirror Info.')

		self.btnCreateBones = QtWidgets.QPushButton('Create Bones')
		self.btnCreateBones.setToolTip('根據選擇的物件(兩個以上)的位置，來創建骨架。')
		self.btnAlignChain = QtWidgets.QPushButton('Align\nChain')
		self.btnAlignChain.setToolTip('轉正骨架串\n*Ctrl+按鈕：\n  轉正選擇Bone以下所有子串的Bone\n*選擇單一Bone+按鈕：\n  轉正擇擇Bone以下第一串的Bone\n*選擇兩個Bone+按鈕：\n  轉正選擇的兩個bone間所有的bone\n')
		self.btnAlignForIK = QtWidgets.QPushButton('Align\nFor IK')
		self.btnAlignForIK.setToolTip('將所選骨架跟下一根骨架轉正，以Z軸為唯一轉軸。')

		self.btnCreateXSplineIK = QtWidgets.QPushButton('Create\nX-Spline IK')
		self.btnCreateXSplineIK.setToolTip('根據選擇的Line，來產生X-Spline IK')

		self.spnSPIKSegNum.setRange(2,100)
		self.spnSPIKSegNum.setValue(4)

		self.spnSPIKCtrlSize.setRange(0.0,9999.0)
		self.spnSPIKCtrlSize.setValue(40.0)

		self.btnCreate2JntIKBone = QtWidgets.QPushButton('2-Joint IK')
		self.btnCreate3JntIKBone = QtWidgets.QPushButton('3-Joint IK')

		self.btnAssignBoneSetting = QtWidgets.QPushButton('Assign')

		self.spnBoneWidth.setRange(0.1,999.0)
		self.spnBoneWidth.setValue(5.0)
		self.spnBoneHeight.setRange(0.1,999.0)
		self.spnBoneHeight.setValue(5.0)
		self.spnBoneTaper.setRange(-1000.0,100.0)
		self.spnBoneTaper.setValue(90.0)

	def create_layout(self):
		baseLayout = QtWidgets.QVBoxLayout(self)
		tabWidget = QtWidgets.QTabWidget()
		baseLayout.addWidget(tabWidget)
		#================================
		biped_tab = QtWidgets.QWidget()
		tabWidget.addTab(biped_tab, "Biped Rig")
		tabWidget.currentChanged.connect(self.doChageTab)

		gpBipedGuide = QtWidgets.QGroupBox('Biped Guide', biped_tab)
		gpBipedGuide.setGeometry(9 * self.uiScale.x,9 * self.uiScale.x,self.width - 42 * self.uiScale.x,60 * self.uiScale.x)

		self.btnCreateBipedGuide.setParent(gpBipedGuide)
		self.btnCreateBipedGuide.setGeometry(20 * self.uiScale.x,20 * self.uiScale.x,gpBipedGuide.width() - 40 * self.uiScale.x,28 * self.uiScale.x)
		#---------------------
		# print(gpBipedGuide.pos().x())
		gpBipedControl = QtWidgets.QGroupBox('Biped Control', biped_tab)
		gpBipedControl.setGeometry(	9 * self.uiScale.x,
									gpBipedGuide.pos().y() + gpBipedGuide.height() + 9 * self.uiScale.x,
									self.width - 42 * self.uiScale.x,
									60 * self.uiScale.x)

		self.btnCreateBipedControl.setParent(gpBipedControl)
		self.btnCreateBipedControl.setGeometry(20 * self.uiScale.x,20 * self.uiScale.x,gpBipedControl.width() - 40 * self.uiScale.x,28 * self.uiScale.x)
		#=====================================
		bone_tab = QtWidgets.QWidget()
 		tabWidget.addTab(bone_tab, "Bone Rig")

 		self.btnCreateBones.setParent(bone_tab)
 		self.btnCreateBones.setGeometry(10 * self.uiScale.x,10 * self.uiScale.x,self.width/2-15 * self.uiScale.x, 40 * self.uiScale.x)

 		self.btnAlignChain.setParent(bone_tab)
 		self.btnAlignChain.setGeometry(self.btnCreateBones.pos().x()+self.btnCreateBones.width()+5 * self.uiScale.x,
 									   10 * self.uiScale.x,
 									   self.width/4-20 * self.uiScale.x,
 									   40 * self.uiScale.x)

 		self.btnAlignForIK.setParent(bone_tab)
 		self.btnAlignForIK.setGeometry(self.btnAlignChain.pos().x()+self.btnAlignChain.width()+5 * self.uiScale.x,
 									   10 * self.uiScale.x,
 									   self.width/4-20 * self.uiScale.x,
 									   40 * self.uiScale.x)

 		gpSplineIK = QtWidgets.QGroupBox('X-Spline IK', bone_tab)
		gpSplineIK.setGeometry(8 * self.uiScale.x,60 * self.uiScale.x,self.width - 40 * self.uiScale.x,80 * self.uiScale.x)

		self.btnCreateXSplineIK.setParent(gpSplineIK)
		self.btnCreateXSplineIK.setGeometry(9 * self.uiScale.x,20 * self.uiScale.x,100 * self.uiScale.x, gpSplineIK.height()-28 * self.uiScale.x)


		lbSPIKSegNum = QtWidgets.QLabel('骨架節數：', gpSplineIK)
		lbSPIKSegNum.move(gpSplineIK.width()-125 * self.uiScale.x , 26 * self.uiScale.x)

		lbSPIKCtrlSize = QtWidgets.QLabel('控制器大小：', gpSplineIK)
		lbSPIKCtrlSize.move(gpSplineIK.width()-136 * self.uiScale.x , 54 * self.uiScale.x)

		self.spnSPIKSegNum.setParent(gpSplineIK)
		self.spnSPIKSegNum.setGeometry(gpSplineIK.width()-70 * self.uiScale.x, 20 * self.uiScale.x, 60 * self.uiScale.x, 24 * self.uiScale.x)

		self.spnSPIKCtrlSize.setParent(gpSplineIK)
		self.spnSPIKCtrlSize.setGeometry(gpSplineIK.width()-70 * self.uiScale.x, 48 * self.uiScale.x, 60 * self.uiScale.x, 24 * self.uiScale.x)

		gpIKChain = QtWidgets.QGroupBox('IK Chain', bone_tab)
		gpIKChain.setGeometry(8 * self.uiScale.x,145 * self.uiScale.x,self.width - 40 * self.uiScale.x,60 * self.uiScale.x)

		self.btnCreate2JntIKBone.setParent(gpIKChain)
		self.btnCreate2JntIKBone.setGeometry(9 * self.uiScale.x, 20 * self.uiScale.x, 80 * self.uiScale.x, 32 * self.uiScale.x)

		self.btnCreate3JntIKBone.setParent(gpIKChain)
		self.btnCreate3JntIKBone.setGeometry(95 * self.uiScale.x, 20 * self.uiScale.x, 80 * self.uiScale.x, 32 * self.uiScale.x)

		self.cbUseSoftIK.setParent(gpIKChain)
		self.cbUseSoftIK.move(195 * self.uiScale.x, 37 * self.uiScale.x)

		gpBoneSetting = QtWidgets.QGroupBox('Bone Setting', bone_tab)
		gpBoneSetting.setGeometry(8 * self.uiScale.x,215 * self.uiScale.x,self.width - 40 * self.uiScale.x,85 * self.uiScale.x)

		self.btnAssignBoneSetting.setParent(gpBoneSetting)
		self.btnAssignBoneSetting.setGeometry(9 * self.uiScale.x,20 * self.uiScale.x, 90 * self.uiScale.x, 57 * self.uiScale.x)

		self.spnBoneWidth.setParent(gpBoneSetting)
		self.spnBoneWidth.setGeometry(160 * self.uiScale.x, 20 * self.uiScale.x, 90 * self.uiScale.x, 16 * self.uiScale.x)

		self.spnBoneHeight.setParent(gpBoneSetting)
		self.spnBoneHeight.setGeometry(160 * self.uiScale.x, 40 * self.uiScale.x, 90 * self.uiScale.x, 16 * self.uiScale.x)

		self.spnBoneTaper.setParent(gpBoneSetting)
		self.spnBoneTaper.setGeometry(160 * self.uiScale.x, 60 * self.uiScale.x, 90 * self.uiScale.x, 16 * self.uiScale.x)

		lbBoneWidth = QtWidgets.QLabel('Width :',gpBoneSetting)
		lbBoneWidth.move(113 * self.uiScale.x, 21 * self.uiScale.x)

		lbBoneHeight = QtWidgets.QLabel('Height :',gpBoneSetting)
		lbBoneHeight.move(110 * self.uiScale.x, 41 * self.uiScale.x)

		lbBoneTaper = QtWidgets.QLabel('Taper :',gpBoneSetting)
		lbBoneTaper.move(113 * self.uiScale.x, 61 * self.uiScale.x)

		#==================================
		mirror_tab = QtWidgets.QWidget()
 		tabWidget.addTab(mirror_tab, "鏡射設定")

 		self.btnAssignMirrorInfo.setParent(mirror_tab)
 		self.btnAssignMirrorInfo.setGeometry(15 * self.uiScale.x,15 * self.uiScale.x,100 * self.uiScale.x,60 * self.uiScale.x)

 		self.btnRemoveMirrorInfo.setParent(mirror_tab)
 		self.btnRemoveMirrorInfo.setGeometry(15 * self.uiScale.x,85 * self.uiScale.x,100 * self.uiScale.x,60 * self.uiScale.x)



	def create_connection(self):
		self.btnCreateBipedGuide.clicked.connect(self.doBtnCreateBipedGuidePressed)
		self.btnCreateBipedControl.clicked.connect(self.doBtnCreateBipedControlPressed)
		#---------------
		self.btnCreateBones.clicked.connect(self.doCreateBonePressed)
		self.btnAlignChain.clicked.connect(self.doAlignChainPressed)
		self.btnAlignForIK.clicked.connect(self.doAlignForIKPressed)

		self.btnCreateXSplineIK.clicked.connect(self.doCreateXSplineIK)
		self.btnCreate2JntIKBone.clicked.connect(self.doCreate2JointIK)
		self.btnCreate3JntIKBone.clicked.connect(self.doCreate3JointIK)

		self.btnAssignBoneSetting.clicked.connect(self.doAssignBoneSetting)
		#--------------
		self.btnAssignMirrorInfo.clicked.connect(self.doBtnAssianMirrorInfo)
		self.btnRemoveMirrorInfo.clicked.connect(self.doBtnRemoveMirrorInfo)
		

	############################################################################
	##
	############################################################################
	def doTest(self):
		print(self.RootPath)
		pass

	def doChageTab(self, idx):
		if idx == 0:
			self.width = 300 * self.uiScale.x
			self.height = 200 * self.uiScale.x
		elif idx == 1:
			self.width = 300 * self.uiScale.x
			self.height = 350 * self.uiScale.x
		elif idx == 2:
			self.width = 300 * self.uiScale.x
			self.height = 200 * self.uiScale.x

		self.setMinimumWidth(self.width)
		self.setMaximumWidth(self.width)
		self.setMinimumHeight(self.height)
		self.setMaximumHeight(self.height)

	def doBtnCreateBipedGuidePressed(self):
		scriptPath = self.RootPath.replace('\\','/') + 'mxs/'
		MaxPlus.Core.EvalMAXScript('fileIn "' + scriptPath + 'BipedGuide.ms"')

	def doBtnCreateBipedControlPressed(self):
		scriptPath = self.RootPath.replace('\\','/') + 'mxs/'

		MaxPlus.Core.EvalMAXScript('fileIn "' + scriptPath + 'CreateController_Spine.ms"')
		MaxPlus.Core.EvalMAXScript('fileIn "' + scriptPath + 'CreateController_Head.ms"')
		MaxPlus.Core.EvalMAXScript('fileIn "' + scriptPath + 'CreateController_Legs.ms"')
		MaxPlus.Core.EvalMAXScript('fileIn "' + scriptPath + 'CreateController_Arm.ms"')
		MaxPlus.Core.EvalMAXScript('fileIn "' + scriptPath + 'CreateController_Other.ms"')
		MaxPlus.Core.EvalMAXScript('fileIn "' + scriptPath + 'CreateSkeleton.ms"')
		MaxPlus.Core.EvalMAXScript('fileIn "' + scriptPath + 'CreateController_MirrorSetting.ms"')

		ctrlRoot = rt.getNodeByName("ControlRoot")
		ctrlRoot.ScriptPath = scriptPath
	
	def doCreateBonePressed(self):
		selList = rt.selection

		if len(selList) >= 2:
			with pymxs.undo(True):
				listNewBone = []
				oriAutoKeyState = rt.animButtonState
				rt.animButtonState = False
				CtrlSize = (self.spnBoneWidth.value()+self.spnBoneHeight.value())
				for i in range(1, len(selList)):
					newBone = rt.BoneSys.createBone(selList[i-1].transform.pos, selList[i].transform.pos, rt.point3(0,1,0))
					newBone.width = self.spnBoneWidth.value()
					newBone.height = self.spnBoneHeight.value()
					newBone.taper = self.spnBoneTaper.value()
					listNewBone.append(newBone)
				endBone = rt.BoneSys.createBone(selList[-1].transform.pos, selList[-1].transform.pos+listNewBone[-1].transform[0]*CtrlSize*0.25, rt.point3(0,1,0))
				endBone.width = self.spnBoneWidth.value()*0.5
				endBone.height = self.spnBoneHeight.value()*0.5
				endBone.taper = self.spnBoneTaper.value()
				listNewBone.append(endBone)
				for i in range(1, len(listNewBone)):
					listNewBone[i].parent = listNewBone[i-1]

				rt.animButtonState = oriAutoKeyState
				rt.select(listNewBone)
				rt.redrawViews()

	def doAlignChainPressed(self):
		selList = rt.selection
		selCount = len(selList)
		listChian = []
		if selCount == 1:
			if rt.keyboard.controlPressed:
				listChian = getChainObj(selList[0], False)
			else:
				listChian = getChainObj(selList[0], True)
			
		elif selCount == 2:
			listChian = getConnectChain(selList[0], selList[1])
			
		if len(listChian) > 2:
			with pymxs.undo(True):
				for i in range(1, len(listChian)):
					listChildren = []
					for c in listChian[i].children:
						listChildren.append(c)
					for c in listChildren:
						c.parent = None

					pMtx_w = listChian[i].parent.transform#listChian[i-1].transform
					cMtx_w = listChian[i].transform
					cMtx_l = cMtx_w * (rt.Inverse(pMtx_w))
					cQuat_l = cMtx_l.rotation
					cEuler_l = rt.quatToEuler(cQuat_l, order=7)
					cEuler_l.x = -cEuler_l.z
					fixQuat = rt.eulerToQuat(cEuler_l, order=7)
					rotCtrl = rt.getPropertyController(listChian[i].controller, "rotation")
					rotCtrl.value = fixQuat
					
					for c in listChildren:
						c.parent = listChian[i]
				# rt.select(listChian)
				rt.redrawViews()

	def doAlignForIKPressed(self):
		firstBone = rt.selection[0]
		if str(rt.classOf(rt.selection[0])) == 'BoneGeometry':
			if len(rt.selection[0].children) > 0:
				firstChild = rt.selection[0].children[0]
				if str(rt.classOf(firstChild)) == 'BoneGeometry':
					with pymxs.undo(True):
						bone1AxisX = rt.normalize(firstChild.transform.pos - firstBone.transform.pos)
						bone2AxisX = firstChild.transform[0]
						bone1Children = []
						for c in firstBone.children:
							bone1Children.append(c)
							c.parent = None
						bone2Children = []
						for c in firstChild.children:
							bone2Children.append(c)
							c.parent = None
						if rt.abs(rt.dot(bone1AxisX, bone2AxisX))<1:
							crossVec = rt.normalize(rt.cross(bone2AxisX, bone1AxisX))
							bone1AxisY = rt.normalize(rt.cross(crossVec, bone1AxisX))
							bone2AxisY = rt.normalize(rt.cross(crossVec, bone2AxisX))
							firstBone.transform = rt.matrix3(bone1AxisX, bone1AxisY, crossVec, firstBone.transform.pos)
							firstChild.transform = rt.matrix3(bone2AxisX, bone2AxisY, crossVec, firstChild.transform.pos)
						else:
							bone2AxisY = rt.normalize(rt.cross(firstBone.transform[2], bone2AxisX))
							firstChild.transform = rt.matrix3(bone2AxisX, bone2AxisY, firstBone.transform[2], firstChild.transform.pos)
						
						for c in bone1Children:
							c.parent = firstBone
						for c in bone2Children:
							c.parent = firstChild
						rt.redrawViews()
		pass

	def doCreateXSplineIK(self):
		scriptPath = self.RootPath.replace('\\','/') + 'mxs/'

		selList = rt.selection
		lineObj = selList[0]
		if len(selList)==1 and str(rt.superClassOf(lineObj))=='shape':
			with pymxs.undo(True):
				oriAutoKeyState = rt.animButtonState
				rt.animButtonState = False
				scriptStr  = 'fileIn "' + scriptPath + 'RigFunction.ms"\n'
				scriptStr += 'GenXSplineIK $' + lineObj.name + ' ' + str(self.spnSPIKSegNum.value()) + ' ' + str(self.spnSPIKCtrlSize.value()) + ' ' + str(self.spnBoneWidth.value()) + ' ' + str(self.spnBoneHeight.value()) + ' ' + str(self.spnBoneTaper.value())
				# print(scriptStr)
				MaxPlus.Core.EvalMAXScript(scriptStr)
				rt.animButtonState = oriAutoKeyState
				rt.redrawViews()
		pass

	def doCreate2JointIK(self):
		selList = rt.selection
		if len(selList) == 3:
			with pymxs.undo(True):
				oriAutoKeyState = rt.animButtonState
				rt.animButtonState = False

				CtrlSize = (self.spnBoneWidth.value()+self.spnBoneHeight.value())

				refPos0 = selList[0].transform.pos
				refPos1 = selList[1].transform.pos
				refPos2 = selList[2].transform.pos
				cen02Pos = (refPos0 + refPos2)*0.5

				lenBone1 = rt.distance(refPos0, refPos1)
				lenBone2 = rt.distance(refPos1, refPos2)

				lenSE = rt.distance(refPos0, refPos2)
				
				vecSE = rt.normalize(refPos2 - refPos0)
				
				bone1XAxis = rt.normalize(refPos1 - refPos0)
				bone2XAxis = rt.normalize(refPos2 - refPos1)
				sideVec = rt.normalize(rt.cross(bone2XAxis, bone1XAxis))
				bone1YAxis = rt.normalize(rt.cross(sideVec,bone1XAxis))
				bone2YAxis = rt.normalize(rt.cross(sideVec,bone2XAxis))

				upVec = rt.normalize(rt.cross(sideVec, vecSE))
				upNodePos = cen02Pos + upVec*(lenBone1+lenBone2)*0.75

				bone1 = rt.BoneSys.createBone(refPos0, refPos1, rt.point3(0,1,0))
				bone2 = rt.BoneSys.createBone(refPos1, refPos2, rt.point3(0,1,0))
				boneE = rt.BoneSys.createBone(refPos2, refPos2+bone2XAxis*CtrlSize*0.5, rt.point3(0,1,0))
				listBone = [bone1, bone2, boneE]
				for b in listBone:
					b.width = self.spnBoneWidth.value()
					b.height = self.spnBoneHeight.value()
					b.Taper = self.spnBoneTaper.value()
					b.sidefins = False
					b.sidefinssize = 2
					b.frontfin = False
					b.frontfinsize = 2
					b.backfin = False
					b.backfinsize = 2


				bone1.transform = rt.matrix3(bone1XAxis, bone1YAxis, sideVec, refPos0)
				bone2.transform = rt.matrix3(bone2XAxis, bone2YAxis, sideVec, refPos1)
				boneE.transform = rt.matrix3(bone2XAxis, bone2YAxis, sideVec, refPos2)

				bone2.parent = bone1
				boneE.parent = bone2

				UpVec = rt.point(name='UpVec', 
								 wirecolor=rt.color(255,128,10),
								 centermarker=False, 
								 axistripod=False,
								 cross=False,
								 box=True,
								 size=CtrlSize*1.5,
								 constantscreensize=False,
								 drawontop=False)
				UpVec.pos = upNodePos

				IKHolder = rt.IKSys.ikChain(bone1, boneE, 'IKLimb')
				IKHolder.controller.VHTarget = UpVec
				IKHolder.controller.dispGoal = True

				if self.cbUseSoftIK.isChecked():
					IKHolder.controller.dispGoal = False
					boneRoot = rt.point(name=rt.uniquename('boneRoot'), 
										wirecolor=rt.color(255,255,10),
										centermarker=False, 
										axistripod=False,
										cross=False,
										box=True,
										size=CtrlSize*1.5,
										constantscreensize=False,
										drawontop=False)
					boneRoot.pos = refPos0
					bone1.parent = boneRoot
					IKHolder.parent = boneRoot

					CtrlIK = rt.point(name='CtrlIK', 
									  wirecolor=rt.color(255,255,10),
									  centermarker=False, 
									  axistripod=False,
									  cross=False,
									  box=True,
									  size=CtrlSize*2.0,
									  constantscreensize=False,
									  drawontop=False)

					CtrlIK.pos = refPos2
					rt.custAttributes.add(CtrlIK, rt.DummyRelationDef)
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.vec.controller = Point3_Script()')
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller = Float_Script()')

					vecAttrCtrl = rt.getPropertyController(CtrlIK.baseObject, "vec")
					distAttrCtrl = rt.getPropertyController(CtrlIK.baseObject, "dist")


					vecAttrCtrl.IScriptCtrl.AddNode('ref', boneRoot)
					vecAttrCtrl.IScriptCtrl.AddNode('self', CtrlIK)
					scriptStr  = 'rlMtx = self.transform * (Inverse ref.transform)\n'
					scriptStr += 'normalize rlMtx[4]'
					vecAttrCtrl.IScriptCtrl.SetExpression(scriptStr)

					distAttrCtrl.IScriptCtrl.AddNode('ref', boneRoot)
					distAttrCtrl.IScriptCtrl.AddNode('self', CtrlIK)
					distAttrCtrl.IScriptCtrl.SetExpression('distance self.transform.pos ref.transform.pos')

					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller = float_limit()')
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_limit.controller = float_script ()')
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_limit.controller.IScriptCtrl.AddNode "Bone1" $' + bone1.name)
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_limit.controller.IScriptCtrl.AddNode "Bone2" $' + bone2.name)
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_limit.controller.IScriptCtrl.SetExpression "(Bone1.length + Bone2.length)"')

					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_smoothing.controller = float_script ()')
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_smoothing.controller.IScriptCtrl.AddNode "Bone1" $' + bone1.name)
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_smoothing.controller.IScriptCtrl.AddNode "Bone2" $' + bone2.name)
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_smoothing.controller.IScriptCtrl.SetExpression "(Bone1.length + Bone2.length)*0.02"')

					#$.transform.controller.IKGoal.controller = transform_script()
					MaxPlus.Core.EvalMAXScript('$\''+IKHolder.name + '\'.transform.controller.IKGoal.controller = transform_script()')
					IKGoalCtrl = rt.getPropertyController(IKHolder.controller, 'IKGoal')
					IKGoalCtrl.IScriptCtrl.AddNode('boneRoot', boneRoot)
					IKGoalCtrl.IScriptCtrl.AddNode('IKCtrl', CtrlIK)
					scriptStr  = 'wPos = IKCtrl.vec*IKCtrl.dist\n'
					scriptStr += 'matrix3 [1,0,0] [0,1,0] [0,0,1] wPos'
					IKGoalCtrl.IScriptCtrl.SetExpression(scriptStr)
					rt.select(CtrlIK)
				rt.animButtonState = oriAutoKeyState
				rt.redrawViews()

	def doCreate3JointIK(self):
		selList = rt.selection
		if len(selList) == 4:
			with pymxs.undo(True):
				oriAutoKeyState = rt.animButtonState
				rt.animButtonState = False

				CtrlSize = (self.spnBoneWidth.value()+self.spnBoneHeight.value())

				refPos0 = selList[0].transform.pos
				refPos1 = selList[1].transform.pos
				refPos2 = selList[2].transform.pos
				refPos3 = selList[3].transform.pos
				cen12Pos = (refPos1 + refPos2)*0.5
				cen03Pos = (refPos0 + refPos3)*0.5

				lenBone1 = rt.distance(refPos0, refPos1)
				lenBone2 = rt.distance(refPos1, refPos2)
				lenBone3 = rt.distance(refPos2, refPos3)
				lenRef1 = rt.distance(refPos0, cen12Pos)
				lenRef2 = rt.distance(refPos3, cen12Pos)

				lenSE = rt.distance(refPos0, refPos3)
				
				vecSE = rt.normalize(refPos3 - refPos0)
				vecSM = rt.normalize(cen12Pos - refPos0)
				
				refSEPos = lenRef1/(lenRef1+lenRef2)*lenSE*vecSE + refPos0
				bone2FaceVec = rt.normalize(cen12Pos - refSEPos)
				sideVec = rt.normalize(rt.cross(bone2FaceVec, vecSE))
				upVec = rt.normalize(rt.cross(vecSE, sideVec))

				ref1Vec = rt.normalize(rt.cross(bone2FaceVec, sideVec))

				upNodePos = cen03Pos + upVec*(lenBone1+lenBone3)*0.75
				realPos1 = ref1Vec*lenBone2*0.5 + cen12Pos 
				realPos2 = cen12Pos - ref1Vec*lenBone2*0.5

				bone1XAxis = rt.normalize(realPos1 - refPos0)
				bone1YAxis = rt.normalize(rt.cross(bone1XAxis, sideVec))
				bone2XAxis = rt.normalize(realPos2 - realPos1)
				bone2YAxis = rt.normalize(rt.cross(bone2XAxis, sideVec))
				bone3XAxis = rt.normalize(refPos3 - realPos2)
				bone3YAxis = rt.normalize(rt.cross(bone3XAxis, sideVec))

				bone1 = rt.BoneSys.createBone(refPos0, realPos1, rt.point3(0,1,0))
				bone2 = rt.BoneSys.createBone(realPos1, realPos2, rt.point3(0,1,0))
				bone3 = rt.BoneSys.createBone(realPos2, refPos3, rt.point3(0,1,0))
				boneE = rt.BoneSys.createBone(refPos3, refPos3+bone3XAxis*CtrlSize*0.5, rt.point3(0,1,0))
				listBone = [bone1, bone2, bone3, boneE]
				for b in listBone:
					b.width = self.spnBoneWidth.value()
					b.height = self.spnBoneHeight.value()
					b.Taper = self.spnBoneTaper.value()
					b.sidefins = False
					b.sidefinssize = 2
					b.frontfin = False
					b.frontfinsize = 2
					b.backfin = False
					b.backfinsize = 2


				bone1.transform = rt.matrix3(bone1XAxis, bone1YAxis, -sideVec, refPos0)
				bone2.transform = rt.matrix3(bone2XAxis, bone2YAxis, -sideVec, realPos1)
				bone3.transform = rt.matrix3(bone3XAxis, bone3YAxis, -sideVec, realPos2)
				boneE.transform = rt.matrix3(bone3XAxis, bone3YAxis, -sideVec, refPos3)

				bone2.parent = bone1
				bone3.parent = bone2
				boneE.parent = bone3

				UpVec = rt.point(name='UpVec', 
								 wirecolor=rt.color(255,128,10),
								 centermarker=False, 
								 axistripod=False,
								 cross=False,
								 box=True,
								 size=CtrlSize*1.5,
								 constantscreensize=False,
								 drawontop=False)
				UpVec.pos = upNodePos

				IKHolder = rt.IKSys.ikChain(bone1, boneE, 'IKHISolver')
				IKHolder.controller.VHTarget = UpVec
				IKHolder.controller.dispGoal = True

				if self.cbUseSoftIK.isChecked():
					IKHolder.controller.dispGoal = False
					boneRoot = rt.point(name=rt.uniquename('boneRoot'), 
										wirecolor=rt.color(255,255,10),
										centermarker=False, 
										axistripod=False,
										cross=False,
										box=True,
										size=CtrlSize*1.5,
										constantscreensize=False,
										drawontop=False)
					boneRoot.pos = refPos0
					bone1.parent = boneRoot
					IKHolder.parent = boneRoot

					CtrlIK = rt.point(name='CtrlIK', 
									  wirecolor=rt.color(255,255,10),
									  centermarker=False, 
									  axistripod=False,
									  cross=False,
									  box=True,
									  size=CtrlSize*2.0,
									  constantscreensize=False,
									  drawontop=False)

					CtrlIK.pos = refPos3
					rt.custAttributes.add(CtrlIK, rt.DummyRelationDef)
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.vec.controller = Point3_Script()')
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller = Float_Script()')

					vecAttrCtrl = rt.getPropertyController(CtrlIK.baseObject, "vec")
					distAttrCtrl = rt.getPropertyController(CtrlIK.baseObject, "dist")


					vecAttrCtrl.IScriptCtrl.AddNode('ref', boneRoot)
					vecAttrCtrl.IScriptCtrl.AddNode('self', CtrlIK)
					scriptStr  = 'rlMtx = self.transform * (Inverse ref.transform)\n'
					scriptStr += 'normalize rlMtx[4]'
					vecAttrCtrl.IScriptCtrl.SetExpression(scriptStr)

					distAttrCtrl.IScriptCtrl.AddNode('ref', boneRoot)
					distAttrCtrl.IScriptCtrl.AddNode('self', CtrlIK)
					distAttrCtrl.IScriptCtrl.SetExpression('distance self.transform.pos ref.transform.pos')

					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller = float_limit()')
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_limit.controller = float_script ()')
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_limit.controller.IScriptCtrl.AddNode "Bone1" $' + bone1.name)
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_limit.controller.IScriptCtrl.AddNode "Bone2" $' + bone2.name)
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_limit.controller.IScriptCtrl.AddNode "Bone3" $' + bone3.name)
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_limit.controller.IScriptCtrl.SetExpression "(Bone1.length + Bone2.length + Bone3.length)"')

					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_smoothing.controller = float_script ()')
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_smoothing.controller.IScriptCtrl.AddNode "Bone1" $' + bone1.name)
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_smoothing.controller.IScriptCtrl.AddNode "Bone2" $' + bone2.name)
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_smoothing.controller.IScriptCtrl.AddNode "Bone3" $' + bone3.name)
					MaxPlus.Core.EvalMAXScript('$'+CtrlIK.name + '.dist.controller.upper_smoothing.controller.IScriptCtrl.SetExpression "(Bone1.length + Bone2.length + Bone3.length)*0.02"')

					#$.transform.controller.IKGoal.controller = transform_script()
					MaxPlus.Core.EvalMAXScript('$\''+IKHolder.name + '\'.transform.controller.IKGoal.controller = transform_script()')
					IKGoalCtrl = rt.getPropertyController(IKHolder.controller, 'IKGoal')
					IKGoalCtrl.IScriptCtrl.AddNode('boneRoot', boneRoot)
					IKGoalCtrl.IScriptCtrl.AddNode('IKCtrl', CtrlIK)
					scriptStr  = 'wPos = IKCtrl.vec*IKCtrl.dist\n'
					scriptStr += 'matrix3 [1,0,0] [0,1,0] [0,0,1] wPos'
					IKGoalCtrl.IScriptCtrl.SetExpression(scriptStr)
					rt.select(CtrlIK)
				rt.animButtonState = oriAutoKeyState
				rt.redrawViews()

	def doAssignBoneSetting(self):
		pass
	##-------------
	def doBtnAssianMirrorInfo(self):
		selList = rt.selection

		for o in selList:
			mirrorInfoCA = rt.custAttributes.get(o, rt.CAMirrorInfo)
			if mirrorInfoCA == None:
				rt.custAttributes.add(o, rt.CAMirrorInfo)

	def doBtnRemoveMirrorInfo(self):
		selList = rt.selection

		for o in selList:
			mirrorInfoCA = rt.custAttributes.get(o, rt.CAMirrorInfo)
			if mirrorInfoCA != None:
				rt.custAttributes.delete(o, rt.CAMirrorInfo)

if __name__ == "__main__":
	kAnim_ui = KRigTools()