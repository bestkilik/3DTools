# -*- coding: utf-8 -*-
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
import pymel.core.datatypes as dt
import maya.mel as mel
import os

pi = 3.14159265359

Xn = 0.950456
Yn = 1.0
Zn = 1.088754

ConstNum1 = 7.787037037037 #((29.0/6.0)^2)/3.0
ConstNum2 = 0.137931034483 #16/116
ConstNum3 = 0.206896551724 #6/29
ConstNum4 = 0.128418549346 #((6.0/29.0)^2) * 3

def fn(t):
	if t > 0.008856451679:
		return math.pow(t, 0.333333333333)
	else:
		return ConstNum1*t + ConstNum2

def XYZ2Lab(XYZ):
	X = XYZ[0]
	Y = XYZ[1]
	Z = XYZ[2]
	
	fX = fn(X/Xn)
	fY = fn(Y/Yn)
	fZ = fn(Z/Zn)
	
	L = 116.0 * fY - 16.0
	a = 500.0*(fX - fY)
	b = 200.0*(fY - fZ)
	return [L, a, b]
	
def Lab2XYZ(Lab):
	L = Lab[0]
	a = Lab[1]
	b = Lab[2]
	
	fY = (L + 16.0)/116.0
	fX = fY + a/500.0
	fZ = fY - b/200.0
	
	if fY > ConstNum3:
		Y = Yn * fY * fY * fY
	else:
		Y = (fY - ConstNum2)*ConstNum4*Yn
	
	if fX > ConstNum3:
		X = Xn * fX * fX * fX
	else:
		X = (fX - ConstNum2)*ConstNum4*Xn
		
	if fZ > ConstNum3:
		Z = Zn * fZ * fZ * fZ
	else:
		Z = (fZ - ConstNum2)*ConstNum4*Zn
		
	return [X, Y, Z]

def RGB2XYZ(RGB):
	R = RGB[0]
	G = RGB[1]
	B = RGB[2]
	
	X = 0.412453 * R + 0.357580 * G + 0.180423 * B
	Y = 0.212671 * R + 0.715160 * G + 0.072169 * B
	Z = 0.019334 * R + 0.119193 * G + 0.950227 * B
	
	return [X, Y, Z]

def XYZ2RGB(XYZ):
	X = XYZ[0]
	Y = XYZ[1]
	Z = XYZ[2]
	
	R =  3.240479 * X - 1.537150 * Y - 0.498535 * Z
	G = -0.969256 * X + 1.875992 * Y + 0.041556 * Z
	B =  0.055648 * X - 0.204043 * Y + 1.057311 * Z
	
	if R < 0.0:
		R = 0.0
	elif R > 1.0:
		R = 1.0

	if G < 0.0:
		G = 0.0
	elif G > 1.0:
		G = 1.0

	if B < 0.0:
		B = 0.0
	elif B > 1.0:
		B = 1.0
	return [R, G, B]

def RGB2Lab(RGB):
	XYZ = RGB2XYZ(RGB)
	return XYZ2Lab(XYZ)
	
def Lab2RGB(Lab):
	XYZ = Lab2XYZ(Lab)
	return XYZ2RGB(XYZ)

def RGB2HSV(RGB):
	R = RGB[0]
	G = RGB[1]
	B = RGB[2]
	
	vMax = max(R, G, B)
	vMin = min(R, G, B)
	
	if vMax == vMin:
		H = 0.0
	elif vMax == R and G >= B:
		H = 60.0*(G-B)/(vMax-vMin)
	elif vMax == R and G < B:
		H = 60.0*(G-B)/(vMax-vMin) + 360.0
	elif vMax == G:
		H = 60.0*(B-R)/(vMax-vMin) + 120.0
	elif vMax == B:
		H = 60.0*(R-G)/(vMax-vMin) + 240.0
	else:
		H = 0.0
		
	if vMax == 0:
		S = 0.0
	else:
		S = 1.0 - vMin/vMax
		
	V = vMax
	
	return [H, S, V]
	
def HSV2RGB(HSV):
	H = HSV[0]
	S = HSV[1]
	V = HSV[2]
	
	if H < 0:
		H += 360.0

	hi = int(H/60)%6
	f = H/60-hi
	p = V*(1-S)
	q = V*(1-S*f)
	t = V*(1-S*(1-f))
	
	if hi == 1:
		return [q, V, p]
	elif hi == 2:
		return [p, V, t]
	elif hi == 3:
		return [p, q, V]
	elif hi == 4:
		return [t, p, V]
	elif hi == 5:
		return [V, p, q]
	else:
		return [V, t, p]

def RGB2HSL(RGB):
	R = RGB[0]
	G = RGB[1]
	B = RGB[2]
	
	vMax = max(R, G, B)
	vMin = min(R, G, B)
	
	if vMax == vMin:
		H = 0.0
	elif vMax == R and G >= B:
		H = 60.0*(G-B)/(vMax-vMin)
	elif vMax == R and G < B:
		H = 60.0*(G-B)/(vMax-vMin) + 360.0
	elif vMax == G:
		H = 60.0*(B-R)/(vMax-vMin) + 120.0
	elif vMax == B:
		H = 60.0*(R-G)/(vMax-vMin) + 240.0
	else:
		H = 0.0
		
	L = (vMax+vMin)*0.5
	
	if L == 0 or vMax==vMin:
		S = 0.0
	elif L > 0 and L <= 0.5:
		S = (vMax-vMin)/(vMax+vMin)
	else:
		S = (vMax-vMin)/(2.0-vMax-vMin)

	return [H, S, L]
	
def HSL2RGB(HSL):
	h = HSL[0]
	s = HSL[1]
	l = HSL[2]
	
	if s == 0:
		return [1.0,1.0,1.0]
	else:
		def tC (p, q, t):
			if t<0:
				t+=1
			if t>1:
				t-=1
			if t < (1.0/6.0):
				return p + (q - p) * 6.0 * t
			elif t < 0.5:
				return q
			elif t < (2.0/3.0):
				return p + (q - p) * (2.0/3.0 - t) * 6.0
			else:
				return p
			
		if h < 0:
			h += 360.0
			
		if l < 0.5:
			q = l*(1+s)
		else:
			q = l + s - (l*s)
		
		p = 2*l-q
		hk = h/360.0
		tR = hk + 0.333333333333333333
		tG = hk
		tB = hk - 0.333333333333333333
		
		R = tC(p, q, tR)
		G = tC(p, q, tG)
		B = tC(p, q, tB)
		
		if R < 0.0:
			R = 0.0
		elif R > 1.0:
			R = 1.0

		if G < 0.0:
			G = 0.0
		elif G > 1.0:
			G = 1.0

		if B < 0.0:
			B = 0.0
		elif B > 1.0:
			B = 1.0
		return [R, G, B]

def liRGB2sRGB(RGB):
	R = RGB[0]
	G = RGB[1]
	B = RGB[2]

	if R <= 0.0031308:
		r = 12.92 * R
	else:
		r = math.pow(R, 0.4166667)*1.055 - 0.055

	if G <= 0.0031308:
		g = 12.92 * G
	else:
		g = math.pow(G, 0.4166667)*1.055 - 0.055

	if B <= 0.0031308:
		b = 12.92 * B
	else:
		b = math.pow(B, 0.4166667)*1.055 - 0.055

	return [r, g, b]

def sRGB2liRGB(rgb):
	r = rgb[0]
	g = rgb[1]
	b = rgb[2]

	if r < 0.04045:
		R = r / 12.92
	else:
		R = math.pow((r+0.055)/1.055, 2.4)

	if g < 0.04045:
		G = g / 12.92
	else:
		G = math.pow((g+0.055)/1.055, 2.4)

	if b < 0.04045:
		B = b / 12.92
	else:
		B = math.pow((b+0.055)/1.055, 2.4)

	return [R, G, B]

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

def invertVec(Vec):
	return [-Vec[0], -Vec[1], -Vec[2]]

def scaleVec(Vec, scale):
	return [Vec[0]*scale,Vec[1]*scale,Vec[2]*scale]

def sumVec(*Vecs):
	sumV = [0,0,0]
	for v in Vecs:
		sumV[0] += v[0]
		sumV[1] += v[1]
		sumV[2] += v[2]
	return sumV

def multiVec(*Vecs):
	mulV = [1,1,1]
	for v in Vecs:
		mulV[0] *= v[0]
		mulV[1] *= v[1]
		mulV[2] *= v[2]
	return mulV

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

def getRowFromMatrix(Matrix, idx):
	if idx == 0:
		return [Matrix[0],Matrix[1],Matrix[2]]
	elif idx == 1:
		return [Matrix[4],Matrix[5],Matrix[6]]
	elif idx == 2:
		return [Matrix[8],Matrix[9],Matrix[10]]
	elif idx == 3:
		return [Matrix[12],Matrix[13],Matrix[14]]
	else:
		return None

def getPositionFromMatrix(Matrix):
	return getRowFromMatrix(Matrix, 3)

def getTrainNodes(obj,pa=False):
	if cmds.objExists(obj):
		List = [obj]
		children = cmds.listRelatives(obj, c=True,pa=pa)
		if children:
			for child in children:
				clist = getTrainNodes(child, pa)
				for c in clist:
					List.append(c)
			return List
		else:
			return List


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(long(main_window_ptr), QtGui.QWidget)
	
class RigTools(QtGui.QDialog):
	fCrossArrowSize = 10.0
	fCrossArrowBold = 0.5
	fCrossArcArrowRadius = 10.0
	fCrossArcArrowArcRange = 120.0
	rfWireColor = [0.04777575,0.585973,1]
	rfWireColor2 = [0.585973,0.04777575,1]
	btnColorPick = QtGui.QPushButton("")
	btnColor2Pick = QtGui.QPushButton("")
	SymmetryFlipAxis = 1
	bMatchPos = True
	bMatchRot = True
	bMatchScl = False
	bSquash = True

	def __init__(self, parent=maya_main_window()):
		self.closeExistingWindow()
		super(RigTools, self).__init__(parent)
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
		self.setWindowTitle("Rig Tools")
		self.setWindowFlags(QtCore.Qt.Tool)
		self.setMinimumSize(400,320)
		self.setMaximumSize(400,320)
		# print(type(self))
		RefSelf = self
		
		self.create_controls()
		self.create_layout2()
		self.create_connections()
		self.show()
		
	def create_controls(self):
		self.spFuxkNoUse = QtGui.QDoubleSpinBox()

		self.btnCreateBipedGuide = QtGui.QPushButton("Create Biped Guide")
		self.btnCreateBipedGuide.setMinimumHeight(64)
		
		self.btnSetBodyTorsoCenter = QtGui.QPushButton("Set Body Torso Center")
		self.btnSetBodyTorsoCenter.setMinimumWidth(160)
		
		self.btnMirrorRight2Left = QtGui.QPushButton("Mirror All R > L")
		self.btnMirrorLeft2Right = QtGui.QPushButton("Mirror All L > R")
		
		self.btnMirrorRight2Left_Arm = QtGui.QPushButton("Mirror Arm R > L")
		self.btnMirrorLeft2Right_Arm = QtGui.QPushButton("Mirror Arm L > R")
		
		self.btnMirrorRight2Left_Leg = QtGui.QPushButton("Mirror Leg R > L")
		self.btnMirrorLeft2Right_Leg = QtGui.QPushButton("Mirror Leg L > R")
		
		self.btnDeleteBipedGuide = QtGui.QPushButton("Delete Guide")
		#---------------------------
		self.btnCreateBipedControl = QtGui.QPushButton("Create Biped Control")
		self.btnCreateBipedControl.setMinimumHeight(64)
		
		#===========================
		self.btnCreateWireBox = QtGui.QPushButton("Box")
		self.btnCreateWireBox.setMinimumWidth(100)
		self.btnCreateWireBox.setMaximumWidth(100)

		self.btnCreateWireSphere = QtGui.QPushButton("Sphere")
		self.btnCreateWireSphere.setMinimumWidth(100)
		self.btnCreateWireSphere.setMaximumWidth(100)

		self.btnCreateWireRect = QtGui.QPushButton("Rect")
		self.btnCreateWireRect.setMinimumWidth(100)
		self.btnCreateWireRect.setMaximumWidth(100)

		self.btnCreateWireCrossArrow = QtGui.QPushButton("Cross Arrow")
		self.btnCreateWireCrossArrow.setMinimumWidth(100)
		self.btnCreateWireCrossArrow.setMaximumWidth(100)
		self.spCrossArrowSize = QtGui.QDoubleSpinBox()
		self.spCrossArrowSize.setRange(0.00,999.00)
		self.spCrossArrowSize.setValue(10.0)
		self.spCrossArrowSize.setSingleStep(0.01)
		self.spCrossArrowBold = QtGui.QDoubleSpinBox()
		self.spCrossArrowBold.setRange(0.00,1.00)
		self.spCrossArrowBold.setValue(0.5)
		self.spCrossArrowBold.setSingleStep(0.01)


		self.btnCreateWireArcCrossArrow = QtGui.QPushButton("Arc Cross Arrow")
		self.btnCreateWireArcCrossArrow.setMinimumWidth(100)
		self.btnCreateWireArcCrossArrow.setMaximumWidth(100)
		self.spCrossArcArrowRadius = QtGui.QDoubleSpinBox()
		self.spCrossArcArrowRadius.setRange(0.00,999.00)
		self.spCrossArcArrowRadius.setValue(10.0)
		self.spCrossArcArrowRadius.setSingleStep(0.01)
		self.spCrossArcArrowArcRange = QtGui.QDoubleSpinBox()
		self.spCrossArcArrowArcRange.setRange(0,180)
		self.spCrossArcArrowArcRange.setValue(120)
		self.spCrossArcArrowArcRange.setSingleStep(0.5)
		
		self.btnColorPick.setMinimumWidth(50)
		self.btnColorPick.setMaximumWidth(50)
		self.btnColorPick.setStyleSheet("background-color:rgb(64,200,255)")
		self.btnColor2Pick.setMinimumWidth(50)
		self.btnColor2Pick.setMaximumWidth(50)
		self.btnColor2Pick.setStyleSheet("background-color:rgb(200,64,255)")
		self.btnSetWireColor = QtGui.QPushButton("Set")
		self.btnSetGradientColor = QtGui.QPushButton("Gradient")

		self.btnSymmetryClone = QtGui.QPushButton("Symmetry Clone")
		self.btnSymmetryClone.setMaximumWidth(100)
		self.cbSymmetryFlixAxis = QtGui.QComboBox()
		self.cbSymmetryFlixAxis.setMaximumWidth(50)
		# self.cbSymmetryFlixAxis.addItem(["X","Y","Z"])
		self.cbSymmetryFlixAxis.addItem("X",0)
		self.cbSymmetryFlixAxis.addItem("Y",1)
		self.cbSymmetryFlixAxis.addItem("Z",2)
		self.cbSymmetryFlixAxis.addItem("All",3)
		self.cbSymmetryFlixAxis.setCurrentIndex(1)

		self.btnCreateJoint = QtGui.QPushButton("Create Bones")
		self.btnCreateIK = QtGui.QPushButton("Create 2Bones(IK)")
		self.btnSetStretchCtrl = QtGui.QPushButton("Stretch")
		self.swSquash = QtGui.QCheckBox("Squash")
		self.swSquash.setChecked(True)


		self.btnAlignTo = QtGui.QPushButton("Align")
		self.btnAlignTo.setMinimumHeight(40)
		self.btnAlignTo.setMaximumWidth(150)
		self.swMatchPos = QtGui.QCheckBox("Position")
		self.swMatchPos.setChecked(True)
		# self.swMatchPos.setCheckState(1)
		self.swMatchRot = QtGui.QCheckBox("Rotation")
		self.swMatchRot.setChecked(True)
		# self.swMatchRot.setCheckState(1)
		self.swMatchScl = QtGui.QCheckBox("Scale")

		self.btnCreateFixRoot = QtGui.QPushButton("Create Transform Fix Root")

	def create_layout(self):
		#--------------------------
		main_layout = QtGui.QVBoxLayout()
		main_layout.setContentsMargins(6, 6, 6, 6)
		
		MainTab_Widget = QtGui.QTabWidget()
		MainTab_Widget.currentChanged.connect(RigTools.onTabChanged)
		main_layout.addWidget(MainTab_Widget)
		#-------------
		self.Biped_tab = QtGui.QWidget()
		MainTab_Widget.addTab(self.Biped_tab, "Biped")
		
		RigUtility_Layout = QtGui.QVBoxLayout()
		self.Biped_tab.setLayout(RigUtility_Layout)
		
		BipedGuide_Group = QtGui.QGroupBox("Biped Guide")
		# BipedGuide_Group.setMinimumHeight(200)
		RigUtility_Layout.addWidget(BipedGuide_Group)
		# RigUtility_Layout.setAlignment(BipedGuide_Group, QtCore.Qt.AlignTop)
		BipedGuide_VLayout = QtGui.QVBoxLayout()
		
		BipedGuide_VLayout.addWidget(self.btnCreateBipedGuide)
		BipedGuide_VLayout.addWidget(self.btnSetBodyTorsoCenter)
		BipedGuide_VLayout.setAlignment(self.btnSetBodyTorsoCenter, QtCore.Qt.AlignCenter)
		BipedGuide_Group.setLayout(BipedGuide_VLayout)
		
		BipedGuide_HLayout0 = QtGui.QHBoxLayout()
		BipedGuide_HLayout0.addWidget(self.btnMirrorRight2Left)
		BipedGuide_HLayout0.addWidget(self.btnMirrorLeft2Right)
		
		BipedGuide_HLayout1 = QtGui.QHBoxLayout()
		BipedGuide_HLayout1.addWidget(self.btnMirrorRight2Left_Arm)
		BipedGuide_HLayout1.addWidget(self.btnMirrorLeft2Right_Arm)
		
		BipedGuide_HLayout2 = QtGui.QHBoxLayout()
		BipedGuide_HLayout2.addWidget(self.btnMirrorRight2Left_Leg)
		BipedGuide_HLayout2.addWidget(self.btnMirrorLeft2Right_Leg)
		
		BipedGuide_HLayout3 = QtGui.QHBoxLayout()
		BipedGuide_HLayout3.addWidget(self.btnDeleteBipedGuide)
		BipedGuide_HLayout3.setAlignment(self.btnDeleteBipedGuide, QtCore.Qt.AlignRight)
		
		BipedGuide_VLayout.addLayout(BipedGuide_HLayout0)
		BipedGuide_VLayout.addLayout(BipedGuide_HLayout1)
		BipedGuide_VLayout.addLayout(BipedGuide_HLayout2)
		BipedGuide_VLayout.addLayout(BipedGuide_HLayout3)
		
		BipedControl_Group = QtGui.QGroupBox("Biped Control")
		RigUtility_Layout.addWidget(BipedControl_Group)
		RigUtility_Layout.setAlignment(BipedControl_Group, QtCore.Qt.AlignTop)
		BipedControl_VLayout = QtGui.QVBoxLayout()
		
		BipedControl_VLayout.addWidget(self.btnCreateBipedControl)
		BipedControl_Group.setLayout(BipedControl_VLayout)
		
		
		#-------------
		self.RigUtility_tab = QtGui.QWidget()
		MainTab_Widget.addTab(self.RigUtility_tab, "Rig Utilities")
		
		OtherUtility_Layout = QtGui.QVBoxLayout()
		self.RigUtility_tab.setLayout(OtherUtility_Layout)
		#----
		OtherUtility_Layout.addWidget(self.btnCreateFixRoot)

		#-----
		WireObj_Group = QtGui.QGroupBox("Wire Object")
		OtherUtility_Layout.addWidget(WireObj_Group)
		# OtherUtility_Layout.setAlignment(WireObj_Group, QtCore.Qt.AlignTop)
		
		WireObj_VLayout = QtGui.QVBoxLayout()
		WireObj_Group.setLayout(WireObj_VLayout)

		WireObj_HLayout0 = QtGui.QHBoxLayout()
		WireObj_HLayout0.addWidget(self.btnCreateWireBox)
		WireObj_HLayout0.addWidget(self.btnCreateWireSphere)
		WireObj_HLayout0.addWidget(self.btnCreateWireRect)
		WireObj_VLayout.addLayout(WireObj_HLayout0)

		WireObj_HLayout1 = QtGui.QHBoxLayout()
		WireObj_HLayout1.setContentsMargins(00,10,00,00)
		WireObj_HLayout1.addWidget(self.btnCreateWireCrossArrow)
		WireObj_HLayout1.addWidget(QtGui.QLabel("  Size:"))
		WireObj_HLayout1.addWidget(self.spCrossArrowSize)
		WireObj_HLayout1.addWidget(QtGui.QLabel("  Bold Ratio:"))
		WireObj_HLayout1.addWidget(self.spCrossArrowBold)
		WireObj_VLayout.addLayout(WireObj_HLayout1)
		
		WireObj_HLayout2 = QtGui.QHBoxLayout()
		WireObj_HLayout2.setContentsMargins(00,10,00,00)
		WireObj_HLayout2.addWidget(self.btnCreateWireArcCrossArrow)
		WireObj_HLayout2.addWidget(QtGui.QLabel("  Radius:"))
		WireObj_HLayout2.addWidget(self.spCrossArcArrowRadius)
		WireObj_HLayout2.addWidget(QtGui.QLabel("  Arc Range:"))
		WireObj_HLayout2.addWidget(self.spCrossArcArrowArcRange)
		WireObj_VLayout.addLayout(WireObj_HLayout2)
		
		#-----
		WireColor_Group = QtGui.QGroupBox("Wire Color")
		OtherUtility_Layout.addWidget(WireColor_Group)
		# OtherUtility_Layout.setAlignment(WireColor_Group, QtCore.Qt.AlignTop)
		
		WireColor_VLayout = QtGui.QVBoxLayout()
		WireColor_Group.setLayout(WireColor_VLayout)

		WireColor_HLayout = QtGui.QHBoxLayout()
		WireColor_VLayout.addLayout(WireColor_HLayout)
		WireColor_HLayout.addWidget(self.btnColorPick)
		WireColor_HLayout.addWidget(self.btnColor2Pick)
		WireColor_HLayout.addWidget(self.btnSetWireColor)
		WireColor_HLayout.addWidget(self.btnSetGradientColor)
		#------------
		SymmetryClone_Group = QtGui.QGroupBox("Symmetry Clone")
		OtherUtility_Layout.addWidget(SymmetryClone_Group)
		OtherUtility_Layout.setAlignment(SymmetryClone_Group, QtCore.Qt.AlignTop)

		SymmetryClone_VLayout = QtGui.QVBoxLayout()
		SymmetryClone_Group.setLayout(SymmetryClone_VLayout)

		SymmetryClone_HLayout = QtGui.QHBoxLayout()
		SymmetryClone_VLayout.addLayout(SymmetryClone_HLayout)
		SymmetryClone_HLayout.addWidget(self.btnSymmetryClone)
		SymmetryClone_HLayout.addWidget(QtGui.QLabel("  Flip Axis:"))
		
		SymmetryClone_HLayout.addWidget(self.cbSymmetryFlixAxis)
		SymmetryClone_HLayout.setAlignment(QtCore.Qt.AlignHCenter)

		#----------------
		BoneJoint_Group = QtGui.QGroupBox("Bone Joint")
		OtherUtility_Layout.addWidget(BoneJoint_Group)
		OtherUtility_Layout.setAlignment(BoneJoint_Group, QtCore.Qt.AlignTop)

		BoneJoint_VLayout = QtGui.QVBoxLayout()
		BoneJoint_Group.setLayout(BoneJoint_VLayout)

		BoneJoint_HLayout = QtGui.QHBoxLayout()
		BoneJoint_VLayout.addLayout(BoneJoint_HLayout)
		BoneJoint_HLayout.addWidget(self.btnCreateJoint)
		BoneJoint_HLayout.addWidget(self.btnCreateIK)

		#-----------------
		AlignTool_Group = QtGui.QGroupBox("Align Tools")
		OtherUtility_Layout.addWidget(AlignTool_Group)
		OtherUtility_Layout.setAlignment(AlignTool_Group, QtCore.Qt.AlignTop)

		AlignTool_VLayout = QtGui.QVBoxLayout()
		AlignTool_Group.setLayout(AlignTool_VLayout)

		AlignTool_HLayout = QtGui.QHBoxLayout()
		AlignTool_VLayout.addLayout(AlignTool_HLayout)
		AlignTool_HLayout.addWidget(self.btnAlignTo)
		# AlignTool_HLayout.addWidget(self.swMatchPos)
		# AlignTool_HLayout.addWidget(self.swMatchRot)
		# AlignTool_HLayout.addWidget(self.swMatchScl)

		#----------------------------------
		StretchBone_Group = QtGui.QGroupBox("Stretch Bone")
		OtherUtility_Layout.addWidget(StretchBone_Group)
		OtherUtility_Layout.setAlignment(StretchBone_Group, QtCore.Qt.AlignTop)

		StretchBone_VLayout = QtGui.QVBoxLayout()
		StretchBone_Group.setLayout(StretchBone_VLayout)

		StretchBone_HLayout = QtGui.QHBoxLayout()
		StretchBone_VLayout.addLayout(StretchBone_HLayout)
		StretchBone_HLayout.addWidget(self.btnSetStretchCtrl)
		StretchBone_HLayout.addWidget(self.swSquash)

		#---------------------------
		OtherUtility_Layout.setAlignment(QtCore.Qt.AlignTop)
		#================================
		self.setLayout(main_layout)
	
	def create_layout2(self):
		#--------------------------
		main_layout = QtGui.QVBoxLayout()
		main_layout.setContentsMargins(6, 6, 6, 6)
		
		MainTab_Widget = QtGui.QTabWidget()
		MainTab_Widget.currentChanged.connect(RigTools.onTabChanged)
		main_layout.addWidget(MainTab_Widget)
		MainTab_Widget.currentChanged.connect(self.doChageTab)
		#-------------
		self.Biped_tab = QtGui.QWidget()
		MainTab_Widget.addTab(self.Biped_tab, "Biped")
		
		
		RigUtility_Layout = QtGui.QVBoxLayout()
		self.Biped_tab.setLayout(RigUtility_Layout)
		
		BipedGuide_Group = QtGui.QGroupBox("Biped Guide")
		BipedGuide_Group.setMaximumHeight(200)
		RigUtility_Layout.addWidget(BipedGuide_Group)
		# RigUtility_Layout.setAlignment(BipedGuide_Group, QtCore.Qt.AlignTop)
		BipedGuide_VLayout = QtGui.QVBoxLayout()
		
		BipedGuide_VLayout.addWidget(self.btnCreateBipedGuide)
		# BipedGuide_VLayout.addWidget(self.btnSetBodyTorsoCenter)
		BipedGuide_VLayout.setAlignment(self.btnSetBodyTorsoCenter, QtCore.Qt.AlignCenter)
		BipedGuide_Group.setLayout(BipedGuide_VLayout)
		
		# BipedGuide_HLayout0 = QtGui.QHBoxLayout()
		# BipedGuide_HLayout0.addWidget(self.btnMirrorRight2Left)
		# BipedGuide_HLayout0.addWidget(self.btnMirrorLeft2Right)
		
		# BipedGuide_HLayout1 = QtGui.QHBoxLayout()
		# BipedGuide_HLayout1.addWidget(self.btnMirrorRight2Left_Arm)
		# BipedGuide_HLayout1.addWidget(self.btnMirrorLeft2Right_Arm)
		
		# BipedGuide_HLayout2 = QtGui.QHBoxLayout()
		# BipedGuide_HLayout2.addWidget(self.btnMirrorRight2Left_Leg)
		# BipedGuide_HLayout2.addWidget(self.btnMirrorLeft2Right_Leg)
		
		BipedGuide_HLayout3 = QtGui.QHBoxLayout()
		BipedGuide_HLayout3.addWidget(self.btnDeleteBipedGuide)
		BipedGuide_HLayout3.setAlignment(self.btnDeleteBipedGuide, QtCore.Qt.AlignRight)
		
		# BipedGuide_VLayout.addLayout(BipedGuide_HLayout0)
		# BipedGuide_VLayout.addLayout(BipedGuide_HLayout1)
		# BipedGuide_VLayout.addLayout(BipedGuide_HLayout2)
		BipedGuide_VLayout.addLayout(BipedGuide_HLayout3)
		
		BipedControl_Group = QtGui.QGroupBox("Biped Control")
		RigUtility_Layout.addWidget(BipedControl_Group)
		RigUtility_Layout.setAlignment(BipedControl_Group, QtCore.Qt.AlignTop)
		BipedControl_VLayout = QtGui.QVBoxLayout()
		
		BipedControl_VLayout.addWidget(self.btnCreateBipedControl)
		BipedControl_Group.setLayout(BipedControl_VLayout)
		
		
		#-------------
		self.RigUtility_tab = QtGui.QWidget()
		MainTab_Widget.addTab(self.RigUtility_tab, "Rig Utilities")
		
		OtherUtility_Layout = QtGui.QVBoxLayout()
		self.RigUtility_tab.setLayout(OtherUtility_Layout)
		#----
		OtherUtility_Layout.addWidget(self.btnCreateFixRoot)

		#-----
		WireObj_Group = QtGui.QGroupBox("Wire Object")
		OtherUtility_Layout.addWidget(WireObj_Group)
		# OtherUtility_Layout.setAlignment(WireObj_Group, QtCore.Qt.AlignTop)
		
		WireObj_VLayout = QtGui.QVBoxLayout()
		WireObj_Group.setLayout(WireObj_VLayout)

		WireObj_HLayout0 = QtGui.QHBoxLayout()
		WireObj_HLayout0.addWidget(self.btnCreateWireBox)
		WireObj_HLayout0.addWidget(self.btnCreateWireSphere)
		WireObj_HLayout0.addWidget(self.btnCreateWireRect)
		WireObj_VLayout.addLayout(WireObj_HLayout0)

		WireObj_HLayout1 = QtGui.QHBoxLayout()
		WireObj_HLayout1.setContentsMargins(00,10,00,00)
		WireObj_HLayout1.addWidget(self.btnCreateWireCrossArrow)
		WireObj_HLayout1.addWidget(QtGui.QLabel("  Size:"))
		WireObj_HLayout1.addWidget(self.spCrossArrowSize)
		WireObj_HLayout1.addWidget(QtGui.QLabel("  Bold Ratio:"))
		WireObj_HLayout1.addWidget(self.spCrossArrowBold)
		WireObj_VLayout.addLayout(WireObj_HLayout1)
		
		WireObj_HLayout2 = QtGui.QHBoxLayout()
		WireObj_HLayout2.setContentsMargins(00,10,00,00)
		WireObj_HLayout2.addWidget(self.btnCreateWireArcCrossArrow)
		WireObj_HLayout2.addWidget(QtGui.QLabel("  Radius:"))
		WireObj_HLayout2.addWidget(self.spCrossArcArrowRadius)
		WireObj_HLayout2.addWidget(QtGui.QLabel("  Arc Range:"))
		WireObj_HLayout2.addWidget(self.spCrossArcArrowArcRange)
		WireObj_VLayout.addLayout(WireObj_HLayout2)
		
		#-----
		WireColor_Group = QtGui.QGroupBox("Wire Color")
		OtherUtility_Layout.addWidget(WireColor_Group)
		# OtherUtility_Layout.setAlignment(WireColor_Group, QtCore.Qt.AlignTop)
		
		WireColor_VLayout = QtGui.QVBoxLayout()
		WireColor_Group.setLayout(WireColor_VLayout)

		WireColor_HLayout = QtGui.QHBoxLayout()
		WireColor_VLayout.addLayout(WireColor_HLayout)
		WireColor_HLayout.addWidget(self.btnColorPick)
		WireColor_HLayout.addWidget(self.btnColor2Pick)
		WireColor_HLayout.addWidget(self.btnSetWireColor)
		WireColor_HLayout.addWidget(self.btnSetGradientColor)
		#------------
		SymmetryClone_Group = QtGui.QGroupBox("Symmetry Clone")
		OtherUtility_Layout.addWidget(SymmetryClone_Group)
		OtherUtility_Layout.setAlignment(SymmetryClone_Group, QtCore.Qt.AlignTop)

		SymmetryClone_VLayout = QtGui.QVBoxLayout()
		SymmetryClone_Group.setLayout(SymmetryClone_VLayout)

		SymmetryClone_HLayout = QtGui.QHBoxLayout()
		SymmetryClone_VLayout.addLayout(SymmetryClone_HLayout)
		SymmetryClone_HLayout.addWidget(self.btnSymmetryClone)
		SymmetryClone_HLayout.addWidget(QtGui.QLabel("  Flip Axis:"))
		
		SymmetryClone_HLayout.addWidget(self.cbSymmetryFlixAxis)
		SymmetryClone_HLayout.setAlignment(QtCore.Qt.AlignHCenter)

		#----------------
		BoneJoint_Group = QtGui.QGroupBox("Bone Joint")
		OtherUtility_Layout.addWidget(BoneJoint_Group)
		OtherUtility_Layout.setAlignment(BoneJoint_Group, QtCore.Qt.AlignTop)

		BoneJoint_VLayout = QtGui.QVBoxLayout()
		BoneJoint_Group.setLayout(BoneJoint_VLayout)

		BoneJoint_HLayout = QtGui.QHBoxLayout()
		BoneJoint_VLayout.addLayout(BoneJoint_HLayout)
		BoneJoint_HLayout.addWidget(self.btnCreateJoint)
		BoneJoint_HLayout.addWidget(self.btnCreateIK)

		#-----------------
		AlignTool_Group = QtGui.QGroupBox("Align Tools")
		OtherUtility_Layout.addWidget(AlignTool_Group)
		OtherUtility_Layout.setAlignment(AlignTool_Group, QtCore.Qt.AlignTop)

		AlignTool_VLayout = QtGui.QVBoxLayout()
		AlignTool_Group.setLayout(AlignTool_VLayout)

		AlignTool_HLayout = QtGui.QHBoxLayout()
		AlignTool_VLayout.addLayout(AlignTool_HLayout)
		AlignTool_HLayout.addWidget(self.btnAlignTo)
		# AlignTool_HLayout.addWidget(self.swMatchPos)
		# AlignTool_HLayout.addWidget(self.swMatchRot)
		# AlignTool_HLayout.addWidget(self.swMatchScl)

		#----------------------------------
		StretchBone_Group = QtGui.QGroupBox("Stretch Bone")
		OtherUtility_Layout.addWidget(StretchBone_Group)
		OtherUtility_Layout.setAlignment(StretchBone_Group, QtCore.Qt.AlignTop)

		StretchBone_VLayout = QtGui.QVBoxLayout()
		StretchBone_Group.setLayout(StretchBone_VLayout)

		StretchBone_HLayout = QtGui.QHBoxLayout()
		StretchBone_VLayout.addLayout(StretchBone_HLayout)
		StretchBone_HLayout.addWidget(self.btnSetStretchCtrl)
		StretchBone_HLayout.addWidget(self.swSquash)

		#---------------------------
		OtherUtility_Layout.setAlignment(QtCore.Qt.AlignTop)
		#================================
		self.setLayout(main_layout)

	def create_connections(self):
		self.btnCreateBipedGuide.clicked.connect(self.doCreateBipedGuide2)
		self.btnDeleteBipedGuide.clicked.connect(self.doDeleteGuide)
		self.btnSetBodyTorsoCenter.clicked.connect(self.doSetBodyTorsoCenter)
		self.btnMirrorLeft2Right_Leg.clicked.connect(self.doMirrorLegGuideL2R)
		self.btnMirrorRight2Left_Leg.clicked.connect(self.doMirrorLegGuideR2L)
		self.btnMirrorLeft2Right_Arm.clicked.connect(self.doMirrorArmGuideL2R)
		self.btnMirrorRight2Left_Arm.clicked.connect(self.doMirrorArmGuideR2L)
		self.btnMirrorLeft2Right.clicked.connect(self.doMirrorAllGuideL2R)
		self.btnMirrorRight2Left.clicked.connect(self.doMirrorAllGuideR2L)
		self.btnCreateBipedControl.clicked.connect(self.doCreateBipedControl4)
		#---------------------------------------
		self.spCrossArrowSize.valueChanged.connect(self.onWireCrossArrowSizeChanged)
		self.spCrossArrowBold.valueChanged.connect(self.onWireCrossArrowBoldRatioChanged)
		self.spCrossArcArrowRadius.valueChanged.connect(self.onWireArcCrossArrowRadiusChanged)
		self.spCrossArcArrowArcRange.valueChanged.connect(self.onWireArcCrossArrowArcRangeChanged)
		self.btnCreateWireBox.clicked.connect(self.doCreateWireBox)
		self.btnCreateWireSphere.clicked.connect(self.doCreateWireSphere)
		self.btnCreateWireRect.clicked.connect(self.doCreateWireRect)
		self.btnCreateWireCrossArrow.clicked.connect(self.doCreateWireCrossArrow)
		self.btnCreateWireArcCrossArrow.clicked.connect(self.doCreateWireArcCrossArrow)
		#------------
		self.btnColorPick.clicked.connect(self.doOpenColorPickerDialog)
		self.btnColor2Pick.clicked.connect(self.doOpenColorPickerDialog2)
		self.btnSetWireColor.clicked.connect(self.doSetWireColor)
		self.btnSetGradientColor.clicked.connect(self.doSetGradiantWireColor)
		#----------
		self.cbSymmetryFlixAxis.currentIndexChanged.connect(self.onSymmetryAxisSelectChanged)
		self.btnSymmetryClone.clicked.connect(self.doSymmetryClone)
		#-----
		self.btnCreateJoint.clicked.connect(self.doCreateBone)
		self.btnCreateIK.clicked.connect(self.doCreateIK)
		#---
		self.btnAlignTo.clicked.connect(self.doAlignTo)
		self.swMatchPos.stateChanged.connect(self.onSwMatchPosChanged)
		self.swMatchRot.stateChanged.connect(self.onSwMatchRotChanged)
		self.swMatchScl.stateChanged.connect(self.onSwMatchSclChanged)
		#---
		self.btnSetStretchCtrl.clicked.connect(self.doSetStretch)
		self.swSquash.stateChanged.connect(self.onSwSquash)
		#---
		self.btnCreateFixRoot.clicked.connect(self.doCreateTransFixRoot)
		
	def closeEvent(self, event):
		self.deleteLater()
	#----------------------------------------------
	# METHOD
	#----------------------------------------------
	def doChageTab(self, idx):
		if idx == 0:
			self.setMinimumWidth(400)
			self.setMaximumWidth(400)
			self.setMinimumHeight(320)
			self.setMaximumHeight(320)
		elif idx == 1:
			self.setMinimumWidth(400)
			self.setMaximumWidth(400)
			self.setMinimumHeight(650)
			self.setMaximumHeight(650)

	@classmethod
	def MirrorArmGuide(self, isR2L):
		wSrc = "R"
		wTgt = "L"
		if not isR2L:
			wSrc = "L"
			wTgt = "R"
		
		#BipedGuide:BG_Shoulder
		srcShoulderLocPosX = cmds.getAttr("BipedGuide:BG_Shoulder_" + wSrc + ".translateX")
		srcShoulderLocPosY = cmds.getAttr("BipedGuide:BG_Shoulder_" + wSrc + ".translateY")
		srcShoulderLocPosZ = cmds.getAttr("BipedGuide:BG_Shoulder_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Shoulder_" + wTgt + ".translateX", -srcShoulderLocPosX)
		cmds.setAttr("BipedGuide:BG_Shoulder_" + wTgt + ".translateY", srcShoulderLocPosY)
		cmds.setAttr("BipedGuide:BG_Shoulder_" + wTgt + ".translateZ", srcShoulderLocPosZ)
		
		#BipedGuide:BG_ArmUpper
		srcArmUpperLocPosX = cmds.getAttr("BipedGuide:BG_ArmUpper_" + wSrc + ".translateX")
		srcArmUpperLocPosY = cmds.getAttr("BipedGuide:BG_ArmUpper_" + wSrc + ".translateY")
		srcArmUpperLocPosZ = cmds.getAttr("BipedGuide:BG_ArmUpper_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_ArmUpper_" + wTgt + ".translateX", -srcArmUpperLocPosX)
		cmds.setAttr("BipedGuide:BG_ArmUpper_" + wTgt + ".translateY", srcArmUpperLocPosY)
		cmds.setAttr("BipedGuide:BG_ArmUpper_" + wTgt + ".translateZ", srcArmUpperLocPosZ)
		
		#BipedGuide:BG_ArmFore
		srcArmForeLocPosX = cmds.getAttr("BipedGuide:BG_ArmFore_" + wSrc + ".translateX")
		srcArmForeLocPosY = cmds.getAttr("BipedGuide:BG_ArmFore_" + wSrc + ".translateY")
		srcArmForeLocPosZ = cmds.getAttr("BipedGuide:BG_ArmFore_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_ArmFore_" + wTgt + ".translateX", -srcArmForeLocPosX)
		cmds.setAttr("BipedGuide:BG_ArmFore_" + wTgt + ".translateY", srcArmForeLocPosY)
		cmds.setAttr("BipedGuide:BG_ArmFore_" + wTgt + ".translateZ", srcArmForeLocPosZ)
		
		#BipedGuide:BG_Hand
		srcHandLocPosX = cmds.getAttr("BipedGuide:BG_Hand_" + wSrc + ".translateX")
		srcHandLocPosY = cmds.getAttr("BipedGuide:BG_Hand_" + wSrc + ".translateY")
		srcHandLocPosZ = cmds.getAttr("BipedGuide:BG_Hand_" + wSrc + ".translateZ")
		srcHandLocRotX = cmds.getAttr("BipedGuide:BG_Hand_" + wSrc + ".rotateX")
		srcHandLocRotY = cmds.getAttr("BipedGuide:BG_Hand_" + wSrc + ".rotateY")
		srcHandLocRotZ = cmds.getAttr("BipedGuide:BG_Hand_" + wSrc + ".rotateZ")
		cmds.setAttr("BipedGuide:BG_Hand_" + wTgt + ".translateX", -srcHandLocPosX)
		cmds.setAttr("BipedGuide:BG_Hand_" + wTgt + ".translateY", srcHandLocPosY)
		cmds.setAttr("BipedGuide:BG_Hand_" + wTgt + ".translateZ", srcHandLocPosZ)
		cmds.setAttr("BipedGuide:BG_Hand_" + wTgt + ".rotateX", srcHandLocRotX)
		cmds.setAttr("BipedGuide:BG_Hand_" + wTgt + ".rotateY", -srcHandLocRotY)
		cmds.setAttr("BipedGuide:BG_Hand_" + wTgt + ".rotateZ", -srcHandLocRotZ)
		
		#BipedGuide:BG_Finger0
		srcFinger0LocPosX = cmds.getAttr("BipedGuide:BG_Finger00_" + wSrc + ".translateX")
		srcFinger0LocPosY = cmds.getAttr("BipedGuide:BG_Finger00_" + wSrc + ".translateY")
		srcFinger0LocPosZ = cmds.getAttr("BipedGuide:BG_Finger00_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger00_" + wTgt + ".translateX", -srcFinger0LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger00_" + wTgt + ".translateY", srcFinger0LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger00_" + wTgt + ".translateZ", srcFinger0LocPosZ)
		srcFinger1LocPosX = cmds.getAttr("BipedGuide:BG_Finger01_" + wSrc + ".translateX")
		srcFinger1LocPosY = cmds.getAttr("BipedGuide:BG_Finger01_" + wSrc + ".translateY")
		srcFinger1LocPosZ = cmds.getAttr("BipedGuide:BG_Finger01_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger01_" + wTgt + ".translateX", -srcFinger1LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger01_" + wTgt + ".translateY", srcFinger1LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger01_" + wTgt + ".translateZ", srcFinger1LocPosZ)
		srcFinger2LocPosX = cmds.getAttr("BipedGuide:BG_Finger02_" + wSrc + ".translateX")
		srcFinger2LocPosY = cmds.getAttr("BipedGuide:BG_Finger02_" + wSrc + ".translateY")
		srcFinger2LocPosZ = cmds.getAttr("BipedGuide:BG_Finger02_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger02_" + wTgt + ".translateX", -srcFinger2LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger02_" + wTgt + ".translateY", srcFinger2LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger02_" + wTgt + ".translateZ", srcFinger2LocPosZ)
		srcFinger3LocPosX = cmds.getAttr("BipedGuide:BG_Finger03_" + wSrc + ".translateX")
		srcFinger3LocPosY = cmds.getAttr("BipedGuide:BG_Finger03_" + wSrc + ".translateY")
		srcFinger3LocPosZ = cmds.getAttr("BipedGuide:BG_Finger03_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger03_" + wTgt + ".translateX", -srcFinger3LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger03_" + wTgt + ".translateY", srcFinger3LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger03_" + wTgt + ".translateZ", srcFinger3LocPosZ)
		
		#BipedGuide:BG_Finger1
		srcFinger0LocPosX = cmds.getAttr("BipedGuide:BG_Finger10_" + wSrc + ".translateX")
		srcFinger0LocPosY = cmds.getAttr("BipedGuide:BG_Finger10_" + wSrc + ".translateY")
		srcFinger0LocPosZ = cmds.getAttr("BipedGuide:BG_Finger10_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger10_" + wTgt + ".translateX", -srcFinger0LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger10_" + wTgt + ".translateY", srcFinger0LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger10_" + wTgt + ".translateZ", srcFinger0LocPosZ)
		srcFinger1LocPosX = cmds.getAttr("BipedGuide:BG_Finger11_" + wSrc + ".translateX")
		srcFinger1LocPosY = cmds.getAttr("BipedGuide:BG_Finger11_" + wSrc + ".translateY")
		srcFinger1LocPosZ = cmds.getAttr("BipedGuide:BG_Finger11_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger11_" + wTgt + ".translateX", -srcFinger1LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger11_" + wTgt + ".translateY", srcFinger1LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger11_" + wTgt + ".translateZ", srcFinger1LocPosZ)
		srcFinger2LocPosX = cmds.getAttr("BipedGuide:BG_Finger12_" + wSrc + ".translateX")
		srcFinger2LocPosY = cmds.getAttr("BipedGuide:BG_Finger12_" + wSrc + ".translateY")
		srcFinger2LocPosZ = cmds.getAttr("BipedGuide:BG_Finger12_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger12_" + wTgt + ".translateX", -srcFinger2LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger12_" + wTgt + ".translateY", srcFinger2LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger12_" + wTgt + ".translateZ", srcFinger2LocPosZ)
		srcFinger3LocPosX = cmds.getAttr("BipedGuide:BG_Finger13_" + wSrc + ".translateX")
		srcFinger3LocPosY = cmds.getAttr("BipedGuide:BG_Finger13_" + wSrc + ".translateY")
		srcFinger3LocPosZ = cmds.getAttr("BipedGuide:BG_Finger13_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger13_" + wTgt + ".translateX", -srcFinger3LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger13_" + wTgt + ".translateY", srcFinger3LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger13_" + wTgt + ".translateZ", srcFinger3LocPosZ)
		
		#BipedGuide:BG_Finger2
		srcFinger0LocPosX = cmds.getAttr("BipedGuide:BG_Finger20_" + wSrc + ".translateX")
		srcFinger0LocPosY = cmds.getAttr("BipedGuide:BG_Finger20_" + wSrc + ".translateY")
		srcFinger0LocPosZ = cmds.getAttr("BipedGuide:BG_Finger20_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger20_" + wTgt + ".translateX", -srcFinger0LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger20_" + wTgt + ".translateY", srcFinger0LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger20_" + wTgt + ".translateZ", srcFinger0LocPosZ)
		srcFinger1LocPosX = cmds.getAttr("BipedGuide:BG_Finger21_" + wSrc + ".translateX")
		srcFinger1LocPosY = cmds.getAttr("BipedGuide:BG_Finger21_" + wSrc + ".translateY")
		srcFinger1LocPosZ = cmds.getAttr("BipedGuide:BG_Finger21_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger21_" + wTgt + ".translateX", -srcFinger1LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger21_" + wTgt + ".translateY", srcFinger1LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger21_" + wTgt + ".translateZ", srcFinger1LocPosZ)
		srcFinger2LocPosX = cmds.getAttr("BipedGuide:BG_Finger22_" + wSrc + ".translateX")
		srcFinger2LocPosY = cmds.getAttr("BipedGuide:BG_Finger22_" + wSrc + ".translateY")
		srcFinger2LocPosZ = cmds.getAttr("BipedGuide:BG_Finger22_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger22_" + wTgt + ".translateX", -srcFinger2LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger22_" + wTgt + ".translateY", srcFinger2LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger22_" + wTgt + ".translateZ", srcFinger2LocPosZ)
		srcFinger3LocPosX = cmds.getAttr("BipedGuide:BG_Finger23_" + wSrc + ".translateX")
		srcFinger3LocPosY = cmds.getAttr("BipedGuide:BG_Finger23_" + wSrc + ".translateY")
		srcFinger3LocPosZ = cmds.getAttr("BipedGuide:BG_Finger23_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger23_" + wTgt + ".translateX", -srcFinger3LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger23_" + wTgt + ".translateY", srcFinger3LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger23_" + wTgt + ".translateZ", srcFinger3LocPosZ)
		
		#BipedGuide:BG_Finger3
		srcFinger0LocPosX = cmds.getAttr("BipedGuide:BG_Finger30_" + wSrc + ".translateX")
		srcFinger0LocPosY = cmds.getAttr("BipedGuide:BG_Finger30_" + wSrc + ".translateY")
		srcFinger0LocPosZ = cmds.getAttr("BipedGuide:BG_Finger30_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger30_" + wTgt + ".translateX", -srcFinger0LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger30_" + wTgt + ".translateY", srcFinger0LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger30_" + wTgt + ".translateZ", srcFinger0LocPosZ)
		srcFinger1LocPosX = cmds.getAttr("BipedGuide:BG_Finger31_" + wSrc + ".translateX")
		srcFinger1LocPosY = cmds.getAttr("BipedGuide:BG_Finger31_" + wSrc + ".translateY")
		srcFinger1LocPosZ = cmds.getAttr("BipedGuide:BG_Finger31_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger31_" + wTgt + ".translateX", -srcFinger1LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger31_" + wTgt + ".translateY", srcFinger1LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger31_" + wTgt + ".translateZ", srcFinger1LocPosZ)
		srcFinger2LocPosX = cmds.getAttr("BipedGuide:BG_Finger32_" + wSrc + ".translateX")
		srcFinger2LocPosY = cmds.getAttr("BipedGuide:BG_Finger32_" + wSrc + ".translateY")
		srcFinger2LocPosZ = cmds.getAttr("BipedGuide:BG_Finger32_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger32_" + wTgt + ".translateX", -srcFinger2LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger32_" + wTgt + ".translateY", srcFinger2LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger32_" + wTgt + ".translateZ", srcFinger2LocPosZ)
		srcFinger3LocPosX = cmds.getAttr("BipedGuide:BG_Finger33_" + wSrc + ".translateX")
		srcFinger3LocPosY = cmds.getAttr("BipedGuide:BG_Finger33_" + wSrc + ".translateY")
		srcFinger3LocPosZ = cmds.getAttr("BipedGuide:BG_Finger33_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger33_" + wTgt + ".translateX", -srcFinger3LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger33_" + wTgt + ".translateY", srcFinger3LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger33_" + wTgt + ".translateZ", srcFinger3LocPosZ)
		
		#BipedGuide:BG_Finger4
		srcFinger0LocPosX = cmds.getAttr("BipedGuide:BG_Finger40_" + wSrc + ".translateX")
		srcFinger0LocPosY = cmds.getAttr("BipedGuide:BG_Finger40_" + wSrc + ".translateY")
		srcFinger0LocPosZ = cmds.getAttr("BipedGuide:BG_Finger40_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger40_" + wTgt + ".translateX", -srcFinger0LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger40_" + wTgt + ".translateY", srcFinger0LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger40_" + wTgt + ".translateZ", srcFinger0LocPosZ)
		srcFinger1LocPosX = cmds.getAttr("BipedGuide:BG_Finger41_" + wSrc + ".translateX")
		srcFinger1LocPosY = cmds.getAttr("BipedGuide:BG_Finger41_" + wSrc + ".translateY")
		srcFinger1LocPosZ = cmds.getAttr("BipedGuide:BG_Finger41_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger41_" + wTgt + ".translateX", -srcFinger1LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger41_" + wTgt + ".translateY", srcFinger1LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger41_" + wTgt + ".translateZ", srcFinger1LocPosZ)
		srcFinger2LocPosX = cmds.getAttr("BipedGuide:BG_Finger42_" + wSrc + ".translateX")
		srcFinger2LocPosY = cmds.getAttr("BipedGuide:BG_Finger42_" + wSrc + ".translateY")
		srcFinger2LocPosZ = cmds.getAttr("BipedGuide:BG_Finger42_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger42_" + wTgt + ".translateX", -srcFinger2LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger42_" + wTgt + ".translateY", srcFinger2LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger42_" + wTgt + ".translateZ", srcFinger2LocPosZ)
		srcFinger3LocPosX = cmds.getAttr("BipedGuide:BG_Finger43_" + wSrc + ".translateX")
		srcFinger3LocPosY = cmds.getAttr("BipedGuide:BG_Finger43_" + wSrc + ".translateY")
		srcFinger3LocPosZ = cmds.getAttr("BipedGuide:BG_Finger43_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Finger43_" + wTgt + ".translateX", -srcFinger3LocPosX)
		cmds.setAttr("BipedGuide:BG_Finger43_" + wTgt + ".translateY", srcFinger3LocPosY)
		cmds.setAttr("BipedGuide:BG_Finger43_" + wTgt + ".translateZ", srcFinger3LocPosZ)
	
	@classmethod
	def MirrorLegGuide(self, isR2L):
		wSrc = "R"
		wTgt = "L"
		if not isR2L:
			wSrc = "L"
			wTgt = "R"
		
		#BipedGuide:BG_Thigh
		srcThighLocPosX = cmds.getAttr("BipedGuide:BG_Thigh_" + wSrc + ".translateX")
		srcThighLocPosY = cmds.getAttr("BipedGuide:BG_Thigh_" + wSrc + ".translateY")
		srcThighLocPosZ = cmds.getAttr("BipedGuide:BG_Thigh_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Thigh_" + wTgt + ".translateX", -srcThighLocPosX)
		cmds.setAttr("BipedGuide:BG_Thigh_" + wTgt + ".translateY", srcThighLocPosY)
		cmds.setAttr("BipedGuide:BG_Thigh_" + wTgt + ".translateZ", srcThighLocPosZ)
		
		#BipedGuide:BG_Calf
		srcCalfLocPosX = cmds.getAttr("BipedGuide:BG_Calf_" + wSrc + ".translateX")
		srcCalfLocPosY = cmds.getAttr("BipedGuide:BG_Calf_" + wSrc + ".translateY")
		srcCalfLocPosZ = cmds.getAttr("BipedGuide:BG_Calf_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Calf_" + wTgt + ".translateX", -srcCalfLocPosX)
		cmds.setAttr("BipedGuide:BG_Calf_" + wTgt + ".translateY", srcCalfLocPosY)
		cmds.setAttr("BipedGuide:BG_Calf_" + wTgt + ".translateZ", srcCalfLocPosZ)
		
		#BipedGuide:BG_Foot
		srcFootLocPosX = cmds.getAttr("BipedGuide:BG_Foot_" + wSrc + ".translateX")
		srcFootLocPosY = cmds.getAttr("BipedGuide:BG_Foot_" + wSrc + ".translateY")
		srcFootLocPosZ = cmds.getAttr("BipedGuide:BG_Foot_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Foot_" + wTgt + ".translateX", -srcFootLocPosX)
		cmds.setAttr("BipedGuide:BG_Foot_" + wTgt + ".translateY", srcFootLocPosY)
		cmds.setAttr("BipedGuide:BG_Foot_" + wTgt + ".translateZ", srcFootLocPosZ)
		
		#BipedGuide:BG_Toe
		srcToeLocPosX = cmds.getAttr("BipedGuide:BG_Toe_" + wSrc + ".translateX")
		srcToeLocPosY = cmds.getAttr("BipedGuide:BG_Toe_" + wSrc + ".translateY")
		srcToeLocPosZ = cmds.getAttr("BipedGuide:BG_Toe_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_Toe_" + wTgt + ".translateX", -srcToeLocPosX)
		cmds.setAttr("BipedGuide:BG_Toe_" + wTgt + ".translateY", srcToeLocPosY)
		cmds.setAttr("BipedGuide:BG_Toe_" + wTgt + ".translateZ", srcToeLocPosZ)
		
		#BipedGuide:BG_ToeE
		srcToeLocPosX = cmds.getAttr("BipedGuide:BG_ToeE_" + wSrc + ".translateX")
		srcToeLocPosY = cmds.getAttr("BipedGuide:BG_ToeE_" + wSrc + ".translateY")
		srcToeLocPosZ = cmds.getAttr("BipedGuide:BG_ToeE_" + wSrc + ".translateZ")
		cmds.setAttr("BipedGuide:BG_ToeE_" + wTgt + ".translateX", -srcToeLocPosX)
		cmds.setAttr("BipedGuide:BG_ToeE_" + wTgt + ".translateY", srcToeLocPosY)
		cmds.setAttr("BipedGuide:BG_ToeE_" + wTgt + ".translateZ", srcToeLocPosZ)
	
	@classmethod
	def createWireCircle(self, name, radius, axisIdx, segment, offset=[0,0,0], color=[0,1,0], pos=[0,0,0], bDirector=False):
		
		listPt = []
		for i in range(segment+1):
			vA = 1
			if bDirector and (i==0 or i==segment):
				vA = 2
			
			if axisIdx == 2:
				arrP = (0, -math.cos(radByAngle(360.0/segment*i))*radius*vA, -math.sin(radByAngle(360.0/segment*i))*radius*vA)
			else:
				arrP = (0, math.sin(radByAngle(360.0/segment*i))*radius*vA, math.cos(radByAngle(360.0/segment*i))*radius*vA)

			listPt.append(arrP)
			
		listP = []
		if axisIdx == 1:
			for i in range(len(listPt)):
				lst = list(listPt[i])
				tmp = lst[0]
				lst[0] = lst[1]
				lst[1] = tmp
				listP.append(tuple(lst))
		elif axisIdx == 2:
			for i in range(len(listPt)):
				lst = list(listPt[i])
				tmp = lst[0]
				lst[0] = lst[2]
				lst[2] = tmp
				listP.append(tuple(lst))
		else:
			for i in range(len(listPt)):
				lst = list(listPt[i])
				listP.append(tuple(lst))
		
		listK = []
		for i in range(len(listP)):
			listK.append(i)
		obj = cmds.curve(name=name, p=listP, k=listK, d=1)
		
		shapes = cmds.listRelatives(obj,s=True)
		for i in range(len(shapes)):
			sh = cmds.rename(shapes[i], name+'Shape')
			cmds.setAttr((sh + ".overrideEnabled"), 1)
			cmds.setAttr((sh + ".overrideRGBColors"), 1)
			cmds.setAttr((sh + ".overrideColorR"), color[0])
			cmds.setAttr((sh + ".overrideColorG"), color[1])
			cmds.setAttr((sh + ".overrideColorB"), color[2])
		cmds.setAttr((obj + ".translateX"), pos[0])
		cmds.setAttr((obj + ".translateY"), pos[1])
		cmds.setAttr((obj + ".translateZ"), pos[2])
		return obj
	
	@classmethod
	def createWireSphere(self, name, radius, color=[0,1,0], pos=[0,0,0]):
		listP = [(0, 0, radius), 
		         (math.sin(pi/6)*radius, 0, math.cos(pi/6)*radius), 
		         (math.sin(pi/3)*radius, 0, math.cos(pi/3)*radius),
		         (radius, 0, 0),
		         (math.sin(pi/3)*radius, 0, math.cos(pi/3)*-radius), 
		         (math.sin(pi/6)*radius, 0, math.cos(pi/6)*-radius),
		         (0, 0, -radius),
		         (math.sin(pi/6)*-radius, 0, math.cos(pi/6)*-radius), 
		         (math.sin(pi/3)*-radius, 0, math.cos(pi/3)*-radius),
		         (-radius, 0, 0),
		         (math.sin(pi/3)*-radius, 0, math.cos(pi/3)*radius), 
		         (math.sin(pi/6)*-radius, 0, math.cos(pi/6)*radius),
		         (0, 0, radius),
		         (0, math.sin(pi/6)*radius, math.cos(pi/6)*radius),
		         (0, math.sin(pi/3)*radius, math.cos(pi/3)*radius),
		         (0, radius, 0),
		         (0, math.sin(pi/3)*radius, math.cos(pi/3)*-radius),
		         (0, math.sin(pi/6)*radius, math.cos(pi/6)*-radius),
		         (0, 0, -radius),
		         (0, math.sin(pi/6)*-radius, math.cos(pi/6)*-radius),
		         (0, math.sin(pi/3)*-radius, math.cos(pi/3)*-radius),
		         (0, -radius, 0),
		         (0, math.sin(pi/3)*-radius, math.cos(pi/3)*radius),
		         (0, math.sin(pi/6)*-radius, math.cos(pi/6)*radius),
		         (0, 0, radius),
		         (math.sin(pi/6)*radius, 0, math.cos(pi/6)*radius), 
		         (math.sin(pi/3)*radius, 0, math.cos(pi/3)*radius),
		         (radius, 0, 0),
		         (math.sin(pi/3)*radius, math.cos(pi/3)*radius, 0),
		         (math.sin(pi/6)*radius, math.cos(pi/6)*radius, 0),
		         (0, radius, 0),
		         (math.sin(pi/6)*-radius, math.cos(pi/6)*radius, 0),
		         (math.sin(pi/3)*-radius, math.cos(pi/3)*radius, 0),
		         (-radius, 0, 0),
		         (math.sin(pi/3)*-radius, math.cos(pi/3)*-radius, 0),
		         (math.sin(pi/6)*-radius, math.cos(pi/6)*-radius, 0),
		         (0, -radius, 0),
		         (math.sin(pi/6)*radius, math.cos(pi/6)*-radius, 0),
		         (math.sin(pi/3)*radius, math.cos(pi/3)*-radius, 0),
		         (radius, 0, 0)]
		
		listK = []
		for i in range(len(listP)):
			listK.append(i)
		obj = cmds.curve(name=name, p=listP, k=listK, d=1)
		
		shapes = cmds.listRelatives(obj,s=True)
		for i in range(len(shapes)):
			sh = cmds.rename(shapes[i], name+'Shape')
			cmds.setAttr((sh + ".overrideEnabled"), 1)
			cmds.setAttr((sh + ".overrideRGBColors"), 1)
			cmds.setAttr((sh + ".overrideColorR"), color[0])
			cmds.setAttr((sh + ".overrideColorG"), color[1])
			cmds.setAttr((sh + ".overrideColorB"), color[2])
		cmds.setAttr((obj + ".translateX"), pos[0])
		cmds.setAttr((obj + ".translateY"), pos[1])
		cmds.setAttr((obj + ".translateZ"), pos[2])
		return obj
	
	@classmethod
	def createWireRect2(self, name, width, length, offset=[0,0,0], color=[0,1,0], alignPlane = 'yz', pos=[0,0,0]):
		# bIsZUp = False
		# UpAxis = cmds.upAxis(q=True,ax=True)
		# if UpAxis=="z":
		# 	bIsZUp = True
		listPxy =  [(-0.5*width,-0.5*length),
					( 0.5*width,-0.5*length),
					( 0.5*width, 0.5*length),
					(-0.5*width, 0.5*length),
					(-0.5*width,-0.5*length)]

		# listPt = [(-0.5*width + offset[0], offset[1], -0.5*length + offset[2]),
		# 		  ( 0.5*width + offset[0], offset[1], -0.5*length + offset[2]),
		# 		  ( 0.5*width + offset[0], offset[1],  0.5*length + offset[2]),
		# 		  (-0.5*width + offset[0], offset[1],  0.5*length + offset[2]),
		# 		  (-0.5*width + offset[0], offset[1], -0.5*length + offset[2])]
		
		listP = []
		if alignPlane == 'xy':
			for i in range(5):
				listP.append( (listPxy[i][0]+offset[0],listPxy[i][1]+offset[1],offset[2]) )
		elif alignPlane == 'xz':
			for i in range(5):
				listP.append( (listPxy[i][0]+offset[0],offset[1],listPxy[i][1]+offset[2]) )
		else:
			for i in range(5):
				listP.append( (offset[0],listPxy[i][0]+offset[1],listPxy[i][1]+offset[2]) )

		# if not bIsZUp or not bFixAxis:
		# 	for i in range(len(listPt)):
		# 		lst = list(listPt[i])
		# 		listP.append(tuple(lst))
		# else:
		# 	for i in range(len(listPt)):
		# 		lst = list(listPt[i])
		# 		tmp = lst[1]
		# 		lst[1] = lst[2]
		# 		lst[2] = tmp
		# 		listP.append(tuple(lst))
		


		listK = []
		for i in range(len(listP)):
			listK.append(i)
		obj = cmds.curve(name=name, p=listP, k=listK, d=1)
		
		shapes = cmds.listRelatives(obj,s=True)
		for i in range(len(shapes)):
			sh = cmds.rename(shapes[i], name+'Shape')
			cmds.setAttr((sh + ".overrideEnabled"), 1)
			cmds.setAttr((sh + ".overrideRGBColors"), 1)
			cmds.setAttr((sh + ".overrideColorR"), color[0])
			cmds.setAttr((sh + ".overrideColorG"), color[1])
			cmds.setAttr((sh + ".overrideColorB"), color[2])
		cmds.setAttr((obj + ".translateX"), pos[0])
		cmds.setAttr((obj + ".translateY"), pos[1])
		cmds.setAttr((obj + ".translateZ"), pos[2])
		return obj

	@classmethod
	def createWireRect(self, name, width, length, offset=[0,0,0], color=[0,1,0], bFixAxis=True, pos=[0,0,0]):
		bIsZUp = False
		UpAxis = cmds.upAxis(q=True,ax=True)
		if UpAxis=="z":
			bIsZUp = True
		listPt = [(-0.5*width + offset[0], offset[1], -0.5*length + offset[2]),
				(0.5*width + offset[0], offset[1], -0.5*length + offset[2]),
				(0.5*width + offset[0], offset[1], 0.5*length + offset[2]),
				(-0.5*width + offset[0], offset[1], 0.5*length + offset[2]),
				(-0.5*width + offset[0], offset[1], -0.5*length + offset[2])]
		
		listP = []

		if not bIsZUp or not bFixAxis:
			for i in range(len(listPt)):
				lst = list(listPt[i])
				listP.append(tuple(lst))
		else:
			for i in range(len(listPt)):
				lst = list(listPt[i])
				tmp = lst[1]
				lst[1] = lst[2]
				lst[2] = tmp
				listP.append(tuple(lst))
			


		listK = []
		for i in range(len(listP)):
			listK.append(i)
		obj = cmds.curve(name=name, p=listP, k=listK, d=1)
		
		shapes = cmds.listRelatives(obj,s=True)
		for i in range(len(shapes)):
			sh = cmds.rename(shapes[i], name+'Shape')
			cmds.setAttr((sh + ".overrideEnabled"), 1)
			cmds.setAttr((sh + ".overrideRGBColors"), 1)
			cmds.setAttr((sh + ".overrideColorR"), color[0])
			cmds.setAttr((sh + ".overrideColorG"), color[1])
			cmds.setAttr((sh + ".overrideColorB"), color[2])
		cmds.setAttr((obj + ".translateX"), pos[0])
		cmds.setAttr((obj + ".translateY"), pos[1])
		cmds.setAttr((obj + ".translateZ"), pos[2])
		return obj
	
	@classmethod
	def createWireBox(self, name, width, length, hight, offset=[0,0,0], color=[0,1,0], pos=[0,0,0]):
		helfW = width * 0.5
		helfL = length * 0.5
		helfH = hight * 0.5
		bInv = 1
		UpAxis = cmds.upAxis(q=True,ax=True)
		if UpAxis=="z":
			helfL = hight * 0.5
			helfH = length * 0.5

		listP = [(helfW + offset[0], helfH + offset[1], helfL + offset[2]),
		         (-helfW + offset[0], helfH + offset[1], helfL + offset[2]),
		         (-helfW + offset[0], helfH + offset[1], -helfL + offset[2]),
		         (helfW + offset[0], helfH + offset[1], -helfL + offset[2]),
		         (helfW + offset[0], helfH + offset[1], helfL + offset[2]),
		         (helfW + offset[0], -helfH + offset[1], helfL + offset[2]),
		         (-helfW + offset[0], -helfH + offset[1], helfL + offset[2]),
		         (-helfW + offset[0], -helfH + offset[1], -helfL + offset[2]),
		         (helfW + offset[0], -helfH + offset[1], -helfL + offset[2]),
		         (helfW + offset[0], -helfH + offset[1], helfL + offset[2]),
		         (-helfW + offset[0], -helfH + offset[1], helfL + offset[2]),
		         (-helfW + offset[0], helfH + offset[1], helfL + offset[2]),
		         (-helfW + offset[0], helfH + offset[1], -helfL + offset[2]),
		         (-helfW + offset[0], -helfH + offset[1], -helfL + offset[2]),
		         (helfW + offset[0], -helfH + offset[1], -helfL + offset[2]),
		         (helfW + offset[0], helfH + offset[1], -helfL + offset[2])]
		
		listK = []
		for i in range(len(listP)):
			listK.append(i)
		obj = cmds.curve(name=name, p=listP, k=listK, d=1)
		
		shapes = cmds.listRelatives(obj,s=True)
		for i in range(len(shapes)):
			sh = cmds.rename(shapes[i], name+'Shape')
			cmds.setAttr((sh + ".overrideEnabled"), 1)
			cmds.setAttr((sh + ".overrideRGBColors"), 1)
			cmds.setAttr((sh + ".overrideColorR"), color[0])
			cmds.setAttr((sh + ".overrideColorG"), color[1])
			cmds.setAttr((sh + ".overrideColorB"), color[2])
		cmds.setAttr((obj + ".translateX"), pos[0])
		cmds.setAttr((obj + ".translateY"), pos[1])
		cmds.setAttr((obj + ".translateZ"), pos[2])
		return obj
	
	@classmethod
	def createWireCrossArrow(self, name, size, boldRatio, color=[0,1,0], pos=[0,0,0], axisIdx=1):
		innW = 0.5*size*boldRatio
		outW = innW + 0.125*size
		outL = size - outW
		listPt = [(0, 0, size),
				(-outW, 0, outL),
				(-innW, 0, outL),
				(-innW, 0, innW),
				(-outL, 0, innW),
				(-outL, 0, outW),
				(-size, 0, 0),
				(-outL, 0, -outW),
				(-outL, 0, -innW),
				(-innW, 0, -innW),
				(-innW, 0, -outL),
				(-outW, 0, -outL),
				(0, 0, -size),
				(outW, 0, -outL),
				(innW, 0, -outL),
				(innW, 0, -innW),
				(outL, 0, -innW),
				(outL, 0, -outW),
				(size, 0, 0),
				(outL, 0, outW),
				(outL, 0, innW),
				(innW, 0, innW),
				(innW, 0, outL),
				(outW, 0, outL),
				(0, 0, size)]
		
		listP = []

		if axisIdx == 0:
			for i in range(len(listPt)):
				lst = list(listPt[i])
				tmp = lst[0]
				lst[0] = lst[1]
				lst[1] = tmp
				listP.append(tuple(lst))
		elif axisIdx == 2:
			for i in range(len(listPt)):
				lst = list(listPt[i])
				tmp = lst[1]
				lst[1] = lst[2]
				lst[2] = tmp
				listP.append(tuple(lst))
		else:
			for i in range(len(listPt)):
				lst = list(listPt[i])
				listP.append(tuple(lst))

		listK = []
		for i in range(len(listP)):
			listK.append(i)
		obj = cmds.curve(name=name, p=listP, k=listK, d=1)
		
		shapes = cmds.listRelatives(obj,s=True)
		for i in range(len(shapes)):
			sh = cmds.rename(shapes[i], name+'Shape')
			cmds.setAttr((sh + ".overrideEnabled"), 1)
			cmds.setAttr((sh + ".overrideRGBColors"), 1)
			cmds.setAttr((sh + ".overrideColorR"), color[0])
			cmds.setAttr((sh + ".overrideColorG"), color[1])
			cmds.setAttr((sh + ".overrideColorB"), color[2])
		cmds.setAttr((obj + ".translateX"), pos[0])
		cmds.setAttr((obj + ".translateY"), pos[1])
		cmds.setAttr((obj + ".translateZ"), pos[2])
		return obj
		
	@classmethod
	def createWireSpherifyCrossArrow(self, name, radius, angleRange, axisIdx, bInvert, color=[0,1,0], offset=[0,0,0], pos=[0,0,0]):
		unitA = (angleRange * 0.5) / 8.0 
		p0 = [ math.cos(radByAngle(90.0 - unitA * 1))* radius, math.sin(radByAngle(90.0 - unitA * 1))* radius]
		p1 = [ math.cos(radByAngle(90.0 - unitA * 2))* radius, math.sin(radByAngle(90.0 - unitA * 2))* radius]
		p2 = [ math.cos(radByAngle(90.0 - unitA * 3))* radius, math.sin(radByAngle(90.0 - unitA * 3))* radius]
		p3 = [ math.cos(radByAngle(90.0 - unitA * 4))* radius, math.sin(radByAngle(90.0 - unitA * 4))* radius]
		p4 = [ math.cos(radByAngle(90.0 - unitA * 5))* radius, math.sin(radByAngle(90.0 - unitA * 5))* radius]
		p5 = [ math.cos(radByAngle(90.0 - unitA * 6))* radius, math.sin(radByAngle(90.0 - unitA * 6))* radius]
		p6 = [ math.cos(radByAngle(90.0 - unitA * 7))* radius, math.sin(radByAngle(90.0 - unitA * 7))* radius]
		p7 = [ math.cos(radByAngle(90.0 - unitA * 8))* radius, math.sin(radByAngle(90.0 - unitA * 8))* radius]
		
		inv = 1
		if bInvert:
			inv = -1
		
		listPt = [[p0[1], p0[0], -p0[0]],
		         [p1[1], p1[0], -p0[0]],
		         [p2[1], p2[0], -p0[0]],
		         [p3[1], p3[0], -p0[0]],
		         [p4[1], p4[0], -p0[0]],
		         [p5[1], p5[0], -p0[0]],
		         [p5[1], p5[0], -p0[0] * 1.7],
		         [p6[1], p6[0], -p0[0]],
		         [p7[1], p7[0], 0],
		         [p6[1], p6[0], p0[0]],
		         [p5[1], p5[0], p0[0] * 1.7],
		         [p5[1], p5[0], p0[0]],
		         [p4[1], p4[0], p0[0]],
		         [p3[1], p3[0], p0[0]],
		         [p2[1], p2[0], p0[0]],
		         [p1[1], p1[0], p0[0]],
		         [p0[1], p0[0], p0[0]],
		         [p1[1], p0[0], p1[0]],
		         [p2[1], p0[0], p2[0]],
		         [p3[1], p0[0], p3[0]],
		         [p4[1], p0[0], p4[0]],
		         [p5[1], p0[0], p5[0]],
		         [p5[1], p0[0] * 1.7, p5[0]],
		         [p6[1], p0[0], p6[0]],
		         [p7[1], 0, p7[0]],
		         [p6[1], -p0[0], p6[0]],
		         [p5[1], -p0[0] * 1.7, p5[0]],
		         [p5[1], -p0[0], p5[0]],
		         [p4[1], -p0[0], p4[0]],
		         [p3[1], -p0[0], p3[0]],
		         [p2[1], -p0[0], p2[0]],
		         [p1[1], -p0[0], p1[0]],
		         [p0[1], -p0[0], p0[0]],
		         [p1[1], -p1[0], p0[0]],
		         [p2[1], -p2[0], p0[0]],
		         [p3[1], -p3[0], p0[0]],
		         [p4[1], -p4[0], p0[0]],
		         [p5[1], -p5[0], p0[0]],
		         [p5[1], -p5[0], p0[0] * 1.7],
		         [p6[1], -p6[0], p0[0]],
		         [p7[1], -p7[0], 0],
		         [p6[1], -p6[0], -p0[0]],
		         [p5[1], -p5[0], -p0[0] * 1.7],
		         [p5[1], -p5[0], -p0[0]],
		         [p4[1], -p4[0], -p0[0]],
		         [p3[1], -p3[0], -p0[0]],
		         [p2[1], -p2[0], -p0[0]],
		         [p1[1], -p1[0], -p0[0]],
		         [p0[1], -p0[0], -p0[0]],
		         [p1[1], -p0[0], -p1[0]],
		         [p2[1], -p0[0], -p2[0]],
		         [p3[1], -p0[0], -p3[0]],
		         [p4[1], -p0[0], -p4[0]],
		         [p5[1], -p0[0], -p5[0]],
		         [p5[1], -p0[0] * 1.7, -p5[0]],
		         [p6[1], -p0[0], -p6[0]],
		         [p7[1], 0, -p7[0]],
		         [p6[1], p0[0], -p6[0]],
		         [p5[1], p0[0] * 1.7, -p5[0]],
		         [p5[1], p0[0], -p5[0]],
		         [p4[1], p0[0], -p4[0]],
		         [p3[1], p0[0], -p3[0]],
		         [p2[1], p0[0], -p2[0]],
		         [p1[1], p0[0], -p1[0]],
		         [p0[1], p0[0], -p0[0]]]
		
		listP = []
		
		if axisIdx == 1:
			for i in range(len(listPt)):
				lst = list(listPt[i])
				tmp = lst[0]
				lst[0] = lst[1]
				lst[1] = tmp * inv
				# listP.append(tuple(lst))
				listP.append(lst)
		elif axisIdx == 2:
			for i in range(len(listPt)):
				lst = list(listPt[i])
				tmp = lst[0]
				lst[0] = lst[2]
				lst[2] = tmp * inv
				# listP.append(tuple(lst))
				listP.append(lst)
		else:
			for i in range(len(listPt)):
				lst = list(listPt[i])
				lst[0] = lst[0] * inv
				# listP.append(tuple(lst))
				listP.append(lst)
			# listP = listPt
				# listP.append(tuple(listPt[i][0],listPt[i][1],listPt[i][2]))
		
		listK = []
		for i in range(len(listP)):
			listP[i][0] += offset[0]
			listP[i][1] += offset[1]
			listP[i][2] += offset[2]
			listK.append(i)
		obj = cmds.curve(name=name, p=listP, k=listK, d=1)
		
		shapes = cmds.listRelatives(obj,s=True)
		for i in range(len(shapes)):
			sh = cmds.rename(shapes[i], name+'Shape')
			cmds.setAttr((sh + ".overrideEnabled"), 1)
			cmds.setAttr((sh + ".overrideRGBColors"), 1)
			cmds.setAttr((sh + ".overrideColorR"), color[0])
			cmds.setAttr((sh + ".overrideColorG"), color[1])
			cmds.setAttr((sh + ".overrideColorB"), color[2])
		cmds.setAttr((obj + ".translateX"), pos[0])
		cmds.setAttr((obj + ".translateY"), pos[1])
		cmds.setAttr((obj + ".translateZ"), pos[2])
		return obj
	
	@classmethod
	def disableControl(self, objList, bLockPos, bLockRot, bLockScl):
		for obj in objList:
			if bLockPos:
				cmds.setAttr(obj+".tx", l=True)
				cmds.setAttr(obj+".ty", l=True)
				cmds.setAttr(obj+".tz", l=True)
				cmds.setAttr(obj+".tx", k=False)
				cmds.setAttr(obj+".ty", k=False)
				cmds.setAttr(obj+".tz", k=False)
			if bLockRot:
				cmds.setAttr(obj+".rx", l=True)
				cmds.setAttr(obj+".ry", l=True)
				cmds.setAttr(obj+".rz", l=True)
				cmds.setAttr(obj+".rx", k=False)
				cmds.setAttr(obj+".ry", k=False)
				cmds.setAttr(obj+".rz", k=False)
			if bLockScl:
				cmds.setAttr(obj+".sx", l=True)
				cmds.setAttr(obj+".sy", l=True)
				cmds.setAttr(obj+".sz", l=True)
				cmds.setAttr(obj+".sx", k=False)
				cmds.setAttr(obj+".sy", k=False)
				cmds.setAttr(obj+".sz", k=False)
			
	@classmethod
	def assignSkinPoseInfo(self, objList):
		for obj in objList:
			cmds.addAttr(obj, ln="SPTranMtx",at="matrix", k=False)
	
	@classmethod
	def storeSkinPose(self, objList):
		for obj in objList:
			if mel.eval('attributeExists "SPTranMtx" ' + obj) == 1:
				cmds.setAttr(obj+".SPTranMtx", cmds.xform(obj, q=True, ws=False,m=True), type="matrix")
				
	@classmethod
	def assignMirrorInfo(self, objList):
		for obj in objList:
			if mel.eval('attributeExists "MirrorNode" ' + obj) == 0:
				# mel.eval('addAttr -ln "InvRotX" -at "bool" ' + o)
				cmds.addAttr(obj, ln="MirrorNode", dt="string")
				cmds.addAttr(obj, ln="InvPosX", at="bool", k=False)
				cmds.addAttr(obj, ln="InvPosY", at="bool", k=False)
				cmds.addAttr(obj, ln="InvPosZ", at="bool", k=False)
				cmds.addAttr(obj, ln="InvRotX", at="bool", k=False)
				cmds.addAttr(obj, ln="InvRotY", at="bool", k=False)
				cmds.addAttr(obj, ln="InvRotZ", at="bool", k=False)
				# cmds.addAttr(obj, ln="MirrorRotOffset", at="double3", k=False)
				cmds.addAttr(obj, ln="MirrorRotOffset", at="double3", k=False)
				cmds.addAttr(obj, ln="MirrorRotOffsetX", at="double", p="MirrorRotOffset", k=False)
				cmds.addAttr(obj, ln="MirrorRotOffsetY", at="double", p="MirrorRotOffset", k=False)
				cmds.addAttr(obj, ln="MirrorRotOffsetZ", at="double", p="MirrorRotOffset", k=False)
	
	@classmethod
	def setMirrorInfo(self, objList):
		for obj in objList:
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
			
			MirrorObj = objName

			for other in objList:
				if obj == other:
					continue
				else:
					cLoc = cmds.xform(other, q=True, ws=True, t=True)
					mOffsetDis = distance(mirLoc, cLoc)
					if mOffsetDis <= 0.05:
						dcDis = distance(tarLoc, cLoc)
						if dcDis > 0.05:
							MirrorObj = other.split(':')[-1]
							cmds.setAttr(obj + ".MirrorNode", MirrorObj, type="string")
							checkBuff = True
							break
			if checkBuff == False:
				cmds.setAttr(obj + ".MirrorNode", MirrorObj, type="string")
			
		####  Check flip axis  ####
		for obj in objList:
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
	def getMatrixFliped(self, srcMatrix, flipAxis):
		if flipAxis == 0:
			return [srcMatrix[0],-srcMatrix[1],-srcMatrix[2],srcMatrix[3],-srcMatrix[4],srcMatrix[5],srcMatrix[6],srcMatrix[7],-srcMatrix[8],srcMatrix[9],srcMatrix[10],srcMatrix[11],-srcMatrix[12],srcMatrix[13],srcMatrix[14],srcMatrix[15]]
		elif flipAxis == 1:
			return [-srcMatrix[0],srcMatrix[1],srcMatrix[2],srcMatrix[3],srcMatrix[4],-srcMatrix[5],-srcMatrix[6],srcMatrix[7],-srcMatrix[8],srcMatrix[9],srcMatrix[10],srcMatrix[11],-srcMatrix[12],srcMatrix[13],srcMatrix[14],srcMatrix[15]]
		elif flipAxis == 2:
			return [-srcMatrix[0],srcMatrix[1],srcMatrix[2],srcMatrix[3],-srcMatrix[4],srcMatrix[5],srcMatrix[6],srcMatrix[7],srcMatrix[8],-srcMatrix[9],-srcMatrix[10],srcMatrix[11],-srcMatrix[12],srcMatrix[13],srcMatrix[14],srcMatrix[15]]
		elif flipAxis == 3:
			return [srcMatrix[0],-srcMatrix[1],-srcMatrix[2],srcMatrix[3],srcMatrix[4],-srcMatrix[5],-srcMatrix[6],srcMatrix[7],srcMatrix[8],-srcMatrix[9],-srcMatrix[10],srcMatrix[11],-srcMatrix[12],srcMatrix[13],srcMatrix[14],srcMatrix[15]]
		return None

	@classmethod
	def createTransFixRoot(self, obj):
		# obj = cmds.ls(sl=True)[0]
		pObj = cmds.listRelatives(obj, p=True)
		objRoot = cmds.group(em=True, name=(obj+'Root'))
		cmds.xform(objRoot,ws=True,m=cmds.xform(obj,q=True,ws=True,m=True))
		if pObj:
			cmds.parent(objRoot, pObj)

		cmds.parent(obj, objRoot)

	#--------------------------------------------------------------------------
	# UI EVENTS
	#--------------------------------------------------------------------------
	
	@classmethod
	def doSetBodyTorsoCenter(self):
		cmds.setAttr("BipedGuide:BG_Hip.translateX", 0)
		cmds.setAttr("BipedGuide:BG_Waist.translateX", 0)
		cmds.setAttr("BipedGuide:BG_Chest.translateX", 0)
		cmds.setAttr("BipedGuide:BG_Chest1.translateX", 0)
		cmds.setAttr("BipedGuide:BG_Neck.translateX", 0)
		cmds.setAttr("BipedGuide:BG_Head.translateX", 0)
		cmds.setAttr("BipedGuide:BG_HeadTop.translateX", 0)
	
	@classmethod
	def doMirrorLegGuideR2L(self):
		self.MirrorLegGuide(True)
		
	@classmethod
	def doMirrorLegGuideL2R(self):
		self.MirrorLegGuide(False)
	
	@classmethod
	def doMirrorArmGuideR2L(self):
		self.MirrorArmGuide(True)
		
	@classmethod
	def doMirrorArmGuideL2R(self):
		self.MirrorArmGuide(False)
	
	@classmethod
	def doMirrorAllGuideR2L(self):
		self.MirrorArmGuide(True)
		self.MirrorLegGuide(True)
	
	@classmethod
	def doMirrorAllGuideL2R(self):
		self.MirrorArmGuide(False)
		self.MirrorLegGuide(False)
	
	@classmethod
	def doDeleteGuide(self):
		if (cmds.objExists("BipedGuild")):
			cmds.delete("BipedGuild")
		
		if cmds.namespace(exists='BipedGuide'):
			cmds.namespace( rm='BipedGuide')
	
	@classmethod
	def doCreateBipedGuide(self):
		#cmds.group(em=True, name='BipedGuide')
		BG_N = ""
		if not cmds.namespace(exists='BipedGuide'):
			BG_N = cmds.namespace( add='BipedGuide') + ":"
		else:
			BG_N = "BipedGuide:"
		
		bIsZUp = False
		UpAxis = cmds.upAxis(q=True,ax=True)
		if UpAxis=="z":
			bIsZUp = True

		if not cmds.objExists(BG_N+"BG_Hip"):
			guideJointColor = [1.0,0.23,0]
			listBipedGuideLocator = []
			
			bLocHip	= self.createWireSphere(BG_N+"BG_Hip", 3.75, guideJointColor, [0, 105.6, 0.384])
			bLocWaist = self.createWireSphere(BG_N+"BG_Waist", 3.75, guideJointColor, [0, 114.72, 0.384])
			bLocChest = self.createWireSphere(BG_N+"BG_Chest", 3.75, guideJointColor, [0, 130.57, -0.192])
			bLocChest1 = self.createWireSphere(BG_N+"BG_Chest1", 3.75, guideJointColor, [0, 145.028, -4.313])
			bLocNeck = self.createWireSphere(BG_N+"BG_Neck", 3.0, guideJointColor, [0, 157.948, -4.945])
			bLocHead = self.createWireSphere(BG_N+"BG_Head", 3.0, guideJointColor, [0, 169.319, -1.527])
			bLocHeadTop = self.createWireSphere(BG_N+"BG_HeadTop", 3.0, guideJointColor, [0, 188.256, -1.527])
			#------------------------------
			bLocShoulderR = self.createWireSphere(BG_N+"BG_Shoulder_R", 3.0, guideJointColor, [-3.17, 153.836, -4.945])
			bLocArmUpperR = self.createWireSphere(BG_N+"BG_ArmUpper_R", 3.0, guideJointColor, [-17.648, 151.609, -6.271])
			bLocArmForeR = self.createWireSphere(BG_N+"BG_ArmFore_R", 3.0, guideJointColor, [-45.197, 151.609, -7.254])
			bLocHandR = self.createWireSphere(BG_N+"BG_Hand_R", 3.0, guideJointColor, [-73.291, 151.609, -7.254])
			bLocFinger00R = self.createWireSphere(BG_N+"BG_Finger00_R", 1, guideJointColor, [-74.9, 150.446, -3.947])
			bLocFinger01R = self.createWireSphere(BG_N+"BG_Finger01_R", 1, guideJointColor, [-78.218, 148.797, -0.865])
			bLocFinger02R = self.createWireSphere(BG_N+"BG_Finger02_R", 1, guideJointColor, [-80.929, 147.798, 1.2289])
			bLocFinger03R = self.createWireSphere(BG_N+"BG_Finger03_R", 1, guideJointColor, [-83.716, 146.73, 2.9])
			bLocFinger10R = self.createWireSphere(BG_N+"BG_Finger10_R", 1, guideJointColor, [-82.322, 151.075, -3.916])
			bLocFinger11R = self.createWireSphere(BG_N+"BG_Finger11_R", 1, guideJointColor, [-87.1981, 150.9926, -2.7721])
			bLocFinger12R = self.createWireSphere(BG_N+"BG_Finger12_R", 1, guideJointColor, [-89.891, 150.795, -2.183])
			bLocFinger13R = self.createWireSphere(BG_N+"BG_Finger13_R", 1, guideJointColor, [-92.1301, 150.5502, -1.6663])
			bLocFinger20R = self.createWireSphere(BG_N+"BG_Finger20_R", 1, guideJointColor, [-82.548, 151.241, -6.16])
			bLocFinger21R = self.createWireSphere(BG_N+"BG_Finger21_R", 1, guideJointColor, [-88.2657, 151.2580, -6.2734])
			bLocFinger22R = self.createWireSphere(BG_N+"BG_Finger22_R", 1, guideJointColor, [-91.332, 151.195, -6.349])
			bLocFinger23R = self.createWireSphere(BG_N+"BG_Finger23_R", 1, guideJointColor, [-93.8309, 150.9932, -6.3499])
			bLocFinger30R = self.createWireSphere(BG_N+"BG_Finger30_R", 1, guideJointColor, [-81.984, 151.075, -8.397])
			bLocFinger31R = self.createWireSphere(BG_N+"BG_Finger31_R", 1, guideJointColor, [-87.3043, 150.9275, -9.8530])
			bLocFinger32R = self.createWireSphere(BG_N+"BG_Finger32_R", 1, guideJointColor, [-89.594, 150.782, -10.488])
			bLocFinger33R = self.createWireSphere(BG_N+"BG_Finger33_R", 1, guideJointColor, [-91.8036, 150.4618, -11.0438])
			bLocFinger40R = self.createWireSphere(BG_N+"BG_Finger40_R", 1, guideJointColor, [-80.736, 150.481, -10.117])
			bLocFinger41R = self.createWireSphere(BG_N+"BG_Finger41_R", 1, guideJointColor, [-84.3475, 150.5688, -12.5258])
			bLocFinger42R = self.createWireSphere(BG_N+"BG_Finger42_R", 1, guideJointColor, [-85.895, 150.375, -13.544])
			bLocFinger43R = self.createWireSphere(BG_N+"BG_Finger43_R", 1, guideJointColor, [-87.0543, 150.0874, -14.2932])
			
			bLocThighR = self.createWireSphere(BG_N+"BG_Thigh_R", 3.75, guideJointColor, [-9.161, 101.04, 0.384])
			bLocCalfR = self.createWireSphere(BG_N+"BG_Calf_R", 3.75, guideJointColor, [-9.161, 54.878, 0.551])
			bLocFootR = self.createWireSphere(BG_N+"BG_Foot_R", 3.75, guideJointColor, [-9.161, 10.631, -4.196])
			bLocToeR = self.createWireSphere(BG_N+"BG_Toe_R", 3.75, guideJointColor, [-9.161, 2.459, 8.15])
			bLocToeER = self.createWireSphere(BG_N+"BG_ToeE_R", 3.75, guideJointColor, [-9.161, 2.459, 17.663])
			#--------------------------------------
			bLocShoulderL = self.createWireSphere(BG_N+"BG_Shoulder_L", 3.0, guideJointColor, [3.17, 153.836, -4.945])
			bLocArmUpperL = self.createWireSphere(BG_N+"BG_ArmUpper_L", 3.0, guideJointColor, [17.648, 151.609, -6.271])
			bLocArmForeL = self.createWireSphere(BG_N+"BG_ArmFore_L", 3.0, guideJointColor, [45.197, 151.609, -7.254])
			bLocHandL = self.createWireSphere(BG_N+"BG_Hand_L", 3.0, guideJointColor, [73.291, 151.609, -7.254])
			bLocFinger00L = self.createWireSphere(BG_N+"BG_Finger00_L", 1, guideJointColor, [74.9, 150.446, -3.947])
			bLocFinger01L = self.createWireSphere(BG_N+"BG_Finger01_L", 1, guideJointColor, [78.218, 148.797, -0.865])
			bLocFinger02L = self.createWireSphere(BG_N+"BG_Finger02_L", 1, guideJointColor, [80.929, 147.798, 1.2289])
			bLocFinger03L = self.createWireSphere(BG_N+"BG_Finger03_L", 1, guideJointColor, [83.716, 146.73, 2.9])
			bLocFinger10L = self.createWireSphere(BG_N+"BG_Finger10_L", 1, guideJointColor, [82.322, 151.075, -3.916])
			bLocFinger11L = self.createWireSphere(BG_N+"BG_Finger11_L", 1, guideJointColor, [87.1981, 150.9926, -2.7721])
			bLocFinger12L = self.createWireSphere(BG_N+"BG_Finger12_L", 1, guideJointColor, [89.891, 150.795, -2.183])
			bLocFinger13L = self.createWireSphere(BG_N+"BG_Finger13_L", 1, guideJointColor, [92.1301, 150.5502, -1.6663])
			bLocFinger20L = self.createWireSphere(BG_N+"BG_Finger20_L", 1, guideJointColor, [82.548, 151.241, -6.16])
			bLocFinger21L = self.createWireSphere(BG_N+"BG_Finger21_L", 1, guideJointColor, [88.2657, 151.2580, -6.2734])
			bLocFinger22L = self.createWireSphere(BG_N+"BG_Finger22_L", 1, guideJointColor, [91.332, 151.195, -6.349])
			bLocFinger23L = self.createWireSphere(BG_N+"BG_Finger23_L", 1, guideJointColor, [93.8309, 150.9932, -6.3499])
			bLocFinger30L = self.createWireSphere(BG_N+"BG_Finger30_L", 1, guideJointColor, [81.984, 151.075, -8.397])
			bLocFinger31L = self.createWireSphere(BG_N+"BG_Finger31_L", 1, guideJointColor, [87.3043, 150.9275, -9.8530])
			bLocFinger32L = self.createWireSphere(BG_N+"BG_Finger32_L", 1, guideJointColor, [89.594, 150.782, -10.488])
			bLocFinger33L = self.createWireSphere(BG_N+"BG_Finger33_L", 1, guideJointColor, [91.8036, 150.4618, -11.0438])
			bLocFinger40L = self.createWireSphere(BG_N+"BG_Finger40_L", 1, guideJointColor, [80.736, 150.481, -10.117])
			bLocFinger41L = self.createWireSphere(BG_N+"BG_Finger41_L", 1, guideJointColor, [84.3475, 150.5688, -12.5258])
			bLocFinger42L = self.createWireSphere(BG_N+"BG_Finger42_L", 1, guideJointColor, [85.895, 150.375, -13.544])
			bLocFinger43L = self.createWireSphere(BG_N+"BG_Finger43_L", 1, guideJointColor, [87.0543, 150.0874, -14.2932])
			
			bLocThighL = self.createWireSphere(BG_N+"BG_Thigh_L", 3.75, guideJointColor, [9.161, 101.04, 0.384])
			bLocCalfL = self.createWireSphere(BG_N+"BG_Calf_L", 3.75, guideJointColor, [9.161, 54.878, 0.551])
			bLocFootL = self.createWireSphere(BG_N+"BG_Foot_L", 3.75, guideJointColor, [9.161, 10.631, -4.196])
			bLocToeL = self.createWireSphere(BG_N+"BG_Toe_L", 3.75, guideJointColor, [9.161, 2.459, 8.15])
			bLocToeEL = self.createWireSphere(BG_N+"BG_ToeE_L", 3.75, guideJointColor, [9.161, 2.459, 17.663])
			#-------------------------------
			listBipedGuideLocator = [bLocHip,bLocWaist,bLocChest,bLocChest1,bLocNeck,bLocHead,bLocHeadTop,bLocShoulderR,bLocArmUpperR,bLocArmForeR,bLocHandR,bLocFinger00R,bLocFinger01R,bLocFinger02R,bLocFinger03R,bLocFinger10R,bLocFinger11R,bLocFinger12R,bLocFinger13R,bLocFinger20R,bLocFinger21R,bLocFinger22R,bLocFinger23R,bLocFinger30R,bLocFinger31R,bLocFinger32R,bLocFinger33R,bLocFinger40R,bLocFinger41R,bLocFinger42R,bLocFinger43R,bLocThighR,bLocCalfR,bLocFootR,bLocToeR,bLocToeER,bLocShoulderL,bLocArmUpperL,bLocArmForeL,bLocHandL,bLocFinger00L,bLocFinger01L,bLocFinger02L,bLocFinger03L,bLocFinger10L,bLocFinger11L,bLocFinger12L,bLocFinger13L,bLocFinger20L,bLocFinger21L,bLocFinger22L,bLocFinger23L,bLocFinger30L,bLocFinger31L,bLocFinger32L,bLocFinger33L,bLocFinger40L,bLocFinger41L,bLocFinger42L,bLocFinger43L,bLocThighL,bLocCalfL,bLocFootL,bLocToeL,bLocToeEL]
			
			BipedGuideRoot = cmds.group( em=True, name=(BG_N+"BipedGuild") )
			cmds.parent(listBipedGuideLocator,BipedGuideRoot)
			
			cmds.parent([bLocFinger00R, bLocFinger01R, bLocFinger02R, bLocFinger03R,
			             bLocFinger10R, bLocFinger11R, bLocFinger12R, bLocFinger13R,
			             bLocFinger20R, bLocFinger21R, bLocFinger22R, bLocFinger23R,
			             bLocFinger30R, bLocFinger31R, bLocFinger32R, bLocFinger33R,
			             bLocFinger40R, bLocFinger41R, bLocFinger42R, bLocFinger43R],bLocHandR)
			
			cmds.parent([bLocFinger00L, bLocFinger01L, bLocFinger02L, bLocFinger03L,
			             bLocFinger10L, bLocFinger11L, bLocFinger12L, bLocFinger13L,
			             bLocFinger20L, bLocFinger21L, bLocFinger22L, bLocFinger23L,
			             bLocFinger30L, bLocFinger31L, bLocFinger32L, bLocFinger33L,
			             bLocFinger40L, bLocFinger41L, bLocFinger42L, bLocFinger43L],bLocHandL)
			#-----------------------------------------
			cmds.select( d=True )
			bProxHip = cmds.joint(name=BG_N+"ProxHip",p=cmds.xform(bLocHip,q=True, ws=True, t=True), rad= 3)
			bProxWaist = cmds.joint(name=BG_N+"ProxWaist",p=cmds.xform(bLocWaist,q=True, ws=True, t=True), rad= 3)
			bProxChest = cmds.joint(name=BG_N+"ProxChest",p=cmds.xform(bLocChest,q=True, ws=True, t=True), rad= 3)
			bProxChest1 = cmds.joint(name=BG_N+"ProxChest1",p=cmds.xform(bLocChest1,q=True, ws=True, t=True), rad= 3)
			bProxNeck = cmds.joint(name=BG_N+"ProxNeck",p=cmds.xform(bLocNeck,q=True, ws=True, t=True), rad= 3)
			bProxHead = cmds.joint(name=BG_N+"ProxHead",p=cmds.xform(bLocHead,q=True, ws=True, t=True), rad= 3)
			bProxHeadTop = cmds.joint(name=BG_N+"ProxHeadTop",p=cmds.xform(bLocHeadTop,q=True, ws=True, t=True), rad= 3)
			cmds.select(bProxHip)
			bProxThighR = cmds.joint(name=BG_N+"ProxThighR",p=cmds.xform(bLocThighR,q=True, ws=True, t=True), rad= 3)
			bProxCalfR = cmds.joint(name=BG_N+"ProxCalfR",p=cmds.xform(bLocCalfR,q=True, ws=True, t=True), rad= 3)
			bProxFootR = cmds.joint(name=BG_N+"ProxFootR",p=cmds.xform(bLocFootR,q=True, ws=True, t=True), rad= 3)
			bProxToeR = cmds.joint(name=BG_N+"ProxToeR",p=cmds.xform(bLocToeR,q=True, ws=True, t=True), rad= 3)
			bProxToeER = cmds.joint(name=BG_N+"ProxToeER",p=cmds.xform(bLocToeER,q=True, ws=True, t=True), rad= 3)
			cmds.select(bProxHip)
			bProxThighL = cmds.joint(name=BG_N+"ProxThighL",p=cmds.xform(bLocThighL,q=True, ws=True, t=True), rad= 3)
			bProxCalfL = cmds.joint(name=BG_N+"ProxCalfL",p=cmds.xform(bLocCalfL,q=True, ws=True, t=True), rad= 3)
			bProxFootL = cmds.joint(name=BG_N+"ProxFootL",p=cmds.xform(bLocFootL,q=True, ws=True, t=True), rad= 3)
			bProxToeL = cmds.joint(name=BG_N+"ProxToeL",p=cmds.xform(bLocToeL,q=True, ws=True, t=True), rad= 3)
			bProxToeEL = cmds.joint(name=BG_N+"ProxToeEL",p=cmds.xform(bLocToeEL,q=True, ws=True, t=True), rad= 3)
			#------------------------------
			cmds.select(bProxChest1)
			bProxShoulderR = cmds.joint(name=BG_N+"ProxShoulderR",p=cmds.xform(bLocShoulderR,q=True, ws=True, t=True), rad= 3)
			bProxArmUpperR = cmds.joint(name=BG_N+"ProxArmUpperR",p=cmds.xform(bLocArmUpperR,q=True, ws=True, t=True), rad= 3)
			bProxArmForeR = cmds.joint(name=BG_N+"ProxArmForeR",p=cmds.xform(bLocArmForeR,q=True, ws=True, t=True), rad= 3)
			bProxHandR = cmds.joint(name=BG_N+"ProxHandR",p=cmds.xform(bLocHandR,q=True, ws=True, t=True), rad= 2)
			bProxFinger00R = cmds.joint(name=BG_N+"ProxFinger00R",p=cmds.xform(bLocFinger00R,q=True, ws=True, t=True), rad= 1)
			bProxFinger01R = cmds.joint(name=BG_N+"ProxFinger01R",p=cmds.xform(bLocFinger01R,q=True, ws=True, t=True), rad= 1)
			bProxFinger02R = cmds.joint(name=BG_N+"ProxFinger02R",p=cmds.xform(bLocFinger02R,q=True, ws=True, t=True), rad= 1)
			bProxFinger03R = cmds.joint(name=BG_N+"ProxFinger03R",p=cmds.xform(bLocFinger03R,q=True, ws=True, t=True), rad= 1)
			cmds.select(bProxHandR)
			bProxFinger10R = cmds.joint(name=BG_N+"ProxFinger10R",p=cmds.xform(bLocFinger10R,q=True, ws=True, t=True), rad= 1)
			bProxFinger11R = cmds.joint(name=BG_N+"ProxFinger11R",p=cmds.xform(bLocFinger11R,q=True, ws=True, t=True), rad= 1)
			bProxFinger12R = cmds.joint(name=BG_N+"ProxFinger12R",p=cmds.xform(bLocFinger12R,q=True, ws=True, t=True), rad= 1)
			bProxFinger13R = cmds.joint(name=BG_N+"ProxFinger13R",p=cmds.xform(bLocFinger13R,q=True, ws=True, t=True), rad= 1)
			cmds.select(bProxHandR)
			bProxFinger20R = cmds.joint(name=BG_N+"ProxFinger20R",p=cmds.xform(bLocFinger20R,q=True, ws=True, t=True), rad= 1)
			bProxFinger21R = cmds.joint(name=BG_N+"ProxFinger21R",p=cmds.xform(bLocFinger21R,q=True, ws=True, t=True), rad= 1)
			bProxFinger22R = cmds.joint(name=BG_N+"ProxFinger22R",p=cmds.xform(bLocFinger22R,q=True, ws=True, t=True), rad= 1)
			bProxFinger23R = cmds.joint(name=BG_N+"ProxFinger23R",p=cmds.xform(bLocFinger23R,q=True, ws=True, t=True), rad= 1)
			cmds.select(bProxHandR)
			bProxFinger30R = cmds.joint(name=BG_N+"ProxFinger30R",p=cmds.xform(bLocFinger30R,q=True, ws=True, t=True), rad= 1)
			bProxFinger31R = cmds.joint(name=BG_N+"ProxFinger31R",p=cmds.xform(bLocFinger31R,q=True, ws=True, t=True), rad= 1)
			bProxFinger32R = cmds.joint(name=BG_N+"ProxFinger32R",p=cmds.xform(bLocFinger32R,q=True, ws=True, t=True), rad= 1)
			bProxFinger33R = cmds.joint(name=BG_N+"ProxFinger33R",p=cmds.xform(bLocFinger33R,q=True, ws=True, t=True), rad= 1)
			cmds.select(bProxHandR)
			bProxFinger40R = cmds.joint(name=BG_N+"ProxFinger40R",p=cmds.xform(bLocFinger40R,q=True, ws=True, t=True), rad= 1)
			bProxFinger41R = cmds.joint(name=BG_N+"ProxFinger41R",p=cmds.xform(bLocFinger41R,q=True, ws=True, t=True), rad= 1)
			bProxFinger42R = cmds.joint(name=BG_N+"ProxFinger42R",p=cmds.xform(bLocFinger42R,q=True, ws=True, t=True), rad= 1)
			bProxFinger43R = cmds.joint(name=BG_N+"ProxFinger43R",p=cmds.xform(bLocFinger43R,q=True, ws=True, t=True), rad= 1)
			#------------------------------
			cmds.select(bProxChest1)
			bProxShoulderL = cmds.joint(name=BG_N+"ProxShoulderL",p=cmds.xform(bLocShoulderL,q=True, ws=True, t=True), rad= 3)
			bProxArmUpperL = cmds.joint(name=BG_N+"ProxArmUpperL",p=cmds.xform(bLocArmUpperL,q=True, ws=True, t=True), rad= 3)
			bProxArmForeL = cmds.joint(name=BG_N+"ProxArmForeL",p=cmds.xform(bLocArmForeL,q=True, ws=True, t=True), rad= 3)
			bProxHandL = cmds.joint(name=BG_N+"ProxHandL",p=cmds.xform(bLocHandL,q=True, ws=True, t=True), rad= 2)
			bProxFinger00L = cmds.joint(name=BG_N+"ProxFinger00L",p=cmds.xform(bLocFinger00L,q=True, ws=True, t=True), rad= 1)
			bProxFinger01L = cmds.joint(name=BG_N+"ProxFinger01L",p=cmds.xform(bLocFinger01L,q=True, ws=True, t=True), rad= 1)
			bProxFinger02L = cmds.joint(name=BG_N+"ProxFinger02L",p=cmds.xform(bLocFinger02L,q=True, ws=True, t=True), rad= 1)
			bProxFinger03L = cmds.joint(name=BG_N+"ProxFinger03L",p=cmds.xform(bLocFinger03L,q=True, ws=True, t=True), rad= 1)
			cmds.select(bProxHandL)
			bProxFinger10L = cmds.joint(name=BG_N+"ProxFinger10L",p=cmds.xform(bLocFinger10L,q=True, ws=True, t=True), rad= 1)
			bProxFinger11L = cmds.joint(name=BG_N+"ProxFinger11L",p=cmds.xform(bLocFinger11L,q=True, ws=True, t=True), rad= 1)
			bProxFinger12L = cmds.joint(name=BG_N+"ProxFinger12L",p=cmds.xform(bLocFinger12L,q=True, ws=True, t=True), rad= 1)
			bProxFinger13L = cmds.joint(name=BG_N+"ProxFinger13L",p=cmds.xform(bLocFinger13L,q=True, ws=True, t=True), rad= 1)
			cmds.select(bProxHandL)
			bProxFinger20L = cmds.joint(name=BG_N+"ProxFinger20L",p=cmds.xform(bLocFinger20L,q=True, ws=True, t=True), rad= 1)
			bProxFinger21L = cmds.joint(name=BG_N+"ProxFinger21L",p=cmds.xform(bLocFinger21L,q=True, ws=True, t=True), rad= 1)
			bProxFinger22L = cmds.joint(name=BG_N+"ProxFinger22L",p=cmds.xform(bLocFinger22L,q=True, ws=True, t=True), rad= 1)
			bProxFinger23L = cmds.joint(name=BG_N+"ProxFinger23L",p=cmds.xform(bLocFinger23L,q=True, ws=True, t=True), rad= 1)
			cmds.select(bProxHandL)
			bProxFinger30L = cmds.joint(name=BG_N+"ProxFinger30L",p=cmds.xform(bLocFinger30L,q=True, ws=True, t=True), rad= 1)
			bProxFinger31L = cmds.joint(name=BG_N+"ProxFinger31L",p=cmds.xform(bLocFinger31L,q=True, ws=True, t=True), rad= 1)
			bProxFinger32L = cmds.joint(name=BG_N+"ProxFinger32L",p=cmds.xform(bLocFinger32L,q=True, ws=True, t=True), rad= 1)
			bProxFinger33L = cmds.joint(name=BG_N+"ProxFinger33L",p=cmds.xform(bLocFinger33L,q=True, ws=True, t=True), rad= 1)
			cmds.select(bProxHandL)
			bProxFinger40L = cmds.joint(name=BG_N+"ProxFinger40L",p=cmds.xform(bLocFinger40L,q=True, ws=True, t=True), rad= 1)
			bProxFinger41L = cmds.joint(name=BG_N+"ProxFinger41L",p=cmds.xform(bLocFinger41L,q=True, ws=True, t=True), rad= 1)
			bProxFinger42L = cmds.joint(name=BG_N+"ProxFinger42L",p=cmds.xform(bLocFinger42L,q=True, ws=True, t=True), rad= 1)
			bProxFinger43L = cmds.joint(name=BG_N+"ProxFinger43L",p=cmds.xform(bLocFinger43L,q=True, ws=True, t=True), rad= 1)
			cmds.parent(bProxHip,BipedGuideRoot)
			
			cmds.setAttr((bProxHip + ".template"), 1)
			cmds.setAttr((bProxHip + ".overrideEnabled"), 1)
			cmds.setAttr((bProxHip + ".overrideRGBColors"), 1)
			cmds.setAttr((bProxHip + ".overrideColorR"), 1)
			cmds.setAttr((bProxHip + ".overrideColorG"), 0)
			cmds.setAttr((bProxHip + ".overrideColorB"), 0)
			
			#---------------------
			# Constraint
			#---------------------
			cmds.parentConstraint( bLocHip, bProxHip, mo=False )
			cmds.parentConstraint( bLocWaist, bProxWaist, mo=False )
			cmds.parentConstraint( bLocChest, bProxChest, mo=False )
			cmds.parentConstraint( bLocChest1, bProxChest1, mo=False )
			cmds.parentConstraint( bLocNeck, bProxNeck, mo=False )
			cmds.parentConstraint( bLocHead, bProxHead, mo=False )
			cmds.parentConstraint( bLocHeadTop, bProxHeadTop, mo=False )
			cmds.parentConstraint( bLocThighR, bProxThighR, mo=False )
			cmds.parentConstraint( bLocCalfR, bProxCalfR, mo=False )
			cmds.parentConstraint( bLocFootR, bProxFootR, mo=False )
			cmds.parentConstraint( bLocToeR, bProxToeR, mo=False )
			cmds.parentConstraint( bLocToeER, bProxToeER, mo=False )
			cmds.parentConstraint( bLocThighL, bProxThighL, mo=False )
			cmds.parentConstraint( bLocCalfL, bProxCalfL, mo=False )
			cmds.parentConstraint( bLocFootL, bProxFootL, mo=False )
			cmds.parentConstraint( bLocToeL, bProxToeL, mo=False )
			cmds.parentConstraint( bLocToeEL, bProxToeEL, mo=False )
			
			cmds.parentConstraint( bLocShoulderR, bProxShoulderR, mo=False )
			cmds.parentConstraint( bLocArmUpperR, bProxArmUpperR, mo=False )
			cmds.parentConstraint( bLocArmForeR, bProxArmForeR, mo=False )
			cmds.parentConstraint( bLocHandR, bProxHandR, mo=False )
			cmds.parentConstraint( bLocFinger00R, bProxFinger00R, mo=False )
			cmds.parentConstraint( bLocFinger01R, bProxFinger01R, mo=False )
			cmds.parentConstraint( bLocFinger02R, bProxFinger02R, mo=False )
			cmds.parentConstraint( bLocFinger03R, bProxFinger03R, mo=False )
			cmds.parentConstraint( bLocFinger10R, bProxFinger10R, mo=False )
			cmds.parentConstraint( bLocFinger11R, bProxFinger11R, mo=False )
			cmds.parentConstraint( bLocFinger12R, bProxFinger12R, mo=False )
			cmds.parentConstraint( bLocFinger13R, bProxFinger13R, mo=False )
			cmds.parentConstraint( bLocFinger20R, bProxFinger20R, mo=False )
			cmds.parentConstraint( bLocFinger21R, bProxFinger21R, mo=False )
			cmds.parentConstraint( bLocFinger22R, bProxFinger22R, mo=False )
			cmds.parentConstraint( bLocFinger23R, bProxFinger23R, mo=False )
			cmds.parentConstraint( bLocFinger30R, bProxFinger30R, mo=False )
			cmds.parentConstraint( bLocFinger31R, bProxFinger31R, mo=False )
			cmds.parentConstraint( bLocFinger32R, bProxFinger32R, mo=False )
			cmds.parentConstraint( bLocFinger33R, bProxFinger33R, mo=False )
			cmds.parentConstraint( bLocFinger40R, bProxFinger40R, mo=False )
			cmds.parentConstraint( bLocFinger41R, bProxFinger41R, mo=False )
			cmds.parentConstraint( bLocFinger42R, bProxFinger42R, mo=False )
			cmds.parentConstraint( bLocFinger43R, bProxFinger43R, mo=False )
			
			cmds.parentConstraint( bLocShoulderL, bProxShoulderL, mo=False )
			cmds.parentConstraint( bLocArmUpperL, bProxArmUpperL, mo=False )
			cmds.parentConstraint( bLocArmForeL, bProxArmForeL, mo=False )
			cmds.parentConstraint( bLocHandL, bProxHandL, mo=False )
			cmds.parentConstraint( bLocFinger00L, bProxFinger00L, mo=False )
			cmds.parentConstraint( bLocFinger01L, bProxFinger01L, mo=False )
			cmds.parentConstraint( bLocFinger02L, bProxFinger02L, mo=False )
			cmds.parentConstraint( bLocFinger03L, bProxFinger03L, mo=False )
			cmds.parentConstraint( bLocFinger10L, bProxFinger10L, mo=False )
			cmds.parentConstraint( bLocFinger11L, bProxFinger11L, mo=False )
			cmds.parentConstraint( bLocFinger12L, bProxFinger12L, mo=False )
			cmds.parentConstraint( bLocFinger13L, bProxFinger13L, mo=False )
			cmds.parentConstraint( bLocFinger20L, bProxFinger20L, mo=False )
			cmds.parentConstraint( bLocFinger21L, bProxFinger21L, mo=False )
			cmds.parentConstraint( bLocFinger22L, bProxFinger22L, mo=False )
			cmds.parentConstraint( bLocFinger23L, bProxFinger23L, mo=False )
			cmds.parentConstraint( bLocFinger30L, bProxFinger30L, mo=False )
			cmds.parentConstraint( bLocFinger31L, bProxFinger31L, mo=False )
			cmds.parentConstraint( bLocFinger32L, bProxFinger32L, mo=False )
			cmds.parentConstraint( bLocFinger33L, bProxFinger33L, mo=False )
			cmds.parentConstraint( bLocFinger40L, bProxFinger40L, mo=False )
			cmds.parentConstraint( bLocFinger41L, bProxFinger41L, mo=False )
			cmds.parentConstraint( bLocFinger42L, bProxFinger42L, mo=False )
			cmds.parentConstraint( bLocFinger43L, bProxFinger43L, mo=False )
		
			if bIsZUp:
				cmds.setAttr( BipedGuideRoot+".rx", 90)

		cmds.select(d=True)

	@classmethod
	def doCreateBipedGuide2(self):
		#cmds.group(em=True, name='BipedGuide')
		BG_N = ""
		# if not cmds.namespace(exists='BipedGuide'):
		# 	BG_N = cmds.namespace( add='BipedGuide') + ":"
		# else:
		# 	BG_N = "BipedGuide:"
		
		bIsZUp = False
		UpAxis = cmds.upAxis(q=True,ax=True)
		if UpAxis=="z":
			bIsZUp = True

		if not cmds.objExists(BG_N+"BG_Hip"):
			guideJointColor = [1.0,0.23,0]
			listBipedGuideLocator = []

			bLocHip	= [0, 105.6, 0.384]
			bLocWaist = [0, 114.72, 0.384]
			bLocChest = [0, 130.57, -0.192]
			bLocChest1 = [0, 145.028, -4.313]
			bLocNeck = [0, 157.948, -4.945]
			bLocHead = [0, 169.319, -1.527]
			bLocHeadTop = [0, 188.256, -1.527]
			#------------------------------
			bLocShoulderR = [-3.17, 153.836, -4.945]
			bLocArmUpperR = [-17.648, 151.609, -6.271]
			bLocArmForeR = [-45.197, 151.609, -7.254]
			bLocHandR = [-73.291, 151.609, -7.254]
			
			bLocFinger00R = [-74.9, 150.44599999999997, -3.947]
			bRotFinger00R = [-2.2380512244552864, -32.358031021725395, 20.583940707249962]
			bLocFinger01R = [-78.27913052446483, 148.991289161561, -0.8330065551667993]
			bRotFinger01R = [0.0, 6.281301303197348, 0.0]
			bLocFinger02R = [-80.98619692897162, 147.79799358240717, 1.1607263705926636]
			bRotFinger02R = [0.0, 4.617501971803037, 0.0]
			bLocFinger03R = [-83.70719692897161, 146.57999358240718, 2.8377263705926685]
			bRotFinger03R = [0.0, 0.0, 0.0]

			bLocFinger10R = [-82.322, 151.07499999999993, -3.915999999999992]
			bRotFinger10R = [77.77948854821013, -7.884028082136907, -3.892235270578649]
			bLocFinger11R = [-87.19802106639294, 150.99260133387938, -2.7721185172890475]
			bRotFinger11R = [0.0, 3.291376486449154, 0.0]
			bLocFinger12R = [-89.88407240687394, 150.78900605084098, -2.154208343781402]
			bRotFinger12R = [0.0, 2.1924467914422654, 0.0]
			bLocFinger13R = [-92.12396072720065, 150.5309292902841, -1.645755322812926]
			bRotFinger13R = [0.0, 0.0, 0.0]

			bLocFinger20R = [-82.548, 151.24099999999999, -6.1599999999999975]
			bRotFinger20R = [83.3728451104933, 6.172325210006943, -6.939809515268923]
			bLocFinger21R = [-88.2659919493199, 151.25800086803056, -6.273405790274565]
			bRotFinger21R = [0.0, 1.4319242390384543, 0.0]
			bLocFinger22R = [-91.33201665864458, 151.1904815092319, -6.332675111853519]
			bRotFinger22R = [0.0, 3.1375336178748596, 0.0]
			bLocFinger23R = [-93.83098822589947, 150.99824249234948, -6.3782262344096905]
			bRotFinger23R = [0.0, 0.0, 0.0]

			bLocFinger30R = [-81.98400000000001, 151.07499999999996, -8.396999999999995]
			bRotFinger30R = [85.8590739596086, 20.440027072408622, -7.170680056011666]
			bLocFinger31R = [-87.30400821536486, 150.9275080894374, -9.852920147655439]
			bRotFinger31R = [0.0, 1.9111388654749062, 0.0]
			bLocFinger32R = [-89.59808217344812, 150.7846463880092, -10.475679432266292]
			bRotFinger32R = [0.0, 4.662072267364468, 0.0]
			bLocFinger33R = [-91.79896339142071, 150.4608236759572, -11.06122394253291]
			bRotFinger33R = [0.0, 0.0, 0.0]

			bLocFinger40R = [-80.736, 150.48099999999997, -10.116999999999999]
			bRotFinger40R = [83.95046576174721, 38.195075157777445, -13.54379775875989]
			bLocFinger41R = [-84.34699999999998, 150.569, -12.525999999999993]
			bRotFinger41R = [0.0, 7.521256906965681, 0.0]
			bLocFinger42R = [-85.89854782938967, 150.3633525825103, -13.536765827247832]
			bRotFinger42R = [0.0, 5.373347773178957, 0.0]
			bLocFinger43R = [-87.06107227841822, 150.0776946183945, -14.281077971288799]
			bRotFinger43R = [0.0, 0.0, 0.0]
			
			bLocThighR = [-9.161, 101.04, 0.384]
			bLocCalfR = [-9.161, 54.878, 0.551]
			bLocFootR = [-9.161, 10.631, -4.196]
			bLocToeR = [-9.161, 2.459, 8.15]
			bLocToeER = [-9.161, 2.459, 17.663]

			#-----------------------------------------
			BipedGuideRoot = cmds.group( em=True, name=(BG_N+"BipedGuild") )

			cmds.select( d=True )
			bProxHip = cmds.joint(name=BG_N+"ProxHip",p=bLocHip, rad= 5)
			cmds.xform(bProxHip, ws=True, m=getTransMatrix(0, getVector(bLocHip, bLocWaist), 2, [0,0,1], bLocHip))
			cmds.setAttr(bProxHip + '.type', 2)
			cmds.setAttr(bProxHip + '.drawLabel', 1)
			bProxWaist = cmds.joint(name=BG_N+"ProxWaist",p=bLocWaist, rad= 5)
			cmds.xform(bProxWaist, ws=True, m=getTransMatrix(0, getVector(bLocHip, bLocChest), 2, [0,0,1], bLocWaist))
			cmds.setAttr(bProxWaist + '.type', 6)
			bProxChest = cmds.joint(name=BG_N+"ProxChest",p=bLocChest, rad= 5)
			cmds.xform(bProxChest, ws=True, m=getTransMatrix(0, getVector(bLocChest, bLocChest1), 2, [0,0,1], bLocChest))
			cmds.setAttr(bProxChest + '.type', 6)
			bProxChest1 = cmds.joint(name=BG_N+"ProxChest1",p=bLocChest1, rad= 5)
			cmds.xform(bProxChest1, ws=True, m=getTransMatrix(0, getVector(bLocChest1, bLocNeck), 2, [0,0,1], bLocChest1))
			cmds.setAttr(bProxChest1 + '.type', 6)
			bProxNeck = cmds.joint(name=BG_N+"ProxNeck",p=bLocNeck, rad= 3)
			cmds.xform(bProxNeck, ws=True, m=getTransMatrix(0, getVector(bLocNeck, bLocHead), 2, [0,0,1], bLocNeck))
			cmds.setAttr(bProxNeck + '.type', 7)
			bProxHead = cmds.joint(name=BG_N+"ProxHead",p=bLocHead, rad= 5)
			cmds.xform(bProxHead, ws=True, m=getTransMatrix(0, getVector(bLocHead, bLocHeadTop), 2, [0,0,1], bLocHead))
			cmds.setAttr(bProxHead + '.type', 8)
			cmds.setAttr(bProxHead + '.drawLabel', 1)
			bProxHeadTop = cmds.joint(name=BG_N+"ProxHeadTop",p=bLocHeadTop, rad= 3)
			
			cmds.select(bProxHip)
			bProxThighR = cmds.joint(name=BG_N+"ProxThigh",p=bLocThighR, rad= 5)
			cmds.xform(bProxThighR, ws=True, m=getTransMatrix(0, getVector(bLocThighR, bLocCalfR), 1, [1,0,0], bLocThighR))
			cmds.setAttr(bProxThighR + '.type', 18)
			cmds.setAttr(bProxThighR + '.otherType', 'Thigh', type='string')

			bProxCalfR = cmds.joint(name=BG_N+"ProxCalf",p=bLocCalfR, rad= 5)
			cmds.xform(bProxCalfR, ws=True, m=getTransMatrix(0, getVector(bLocCalfR, bLocFootR), 1, [1,0,0], bLocCalfR))
			cmds.setAttr(bProxCalfR + '.type', 18)
			cmds.setAttr(bProxCalfR + '.otherType', 'Calf', type='string')

			bProxFootR = cmds.joint(name=BG_N+"ProxFoot",p=bLocFootR, rad= 5)
			cmds.xform(bProxFootR, ws=True, m=getTransMatrix(0, getVector(bLocFootR, bLocToeR), 1, [1,0,0], bLocFootR))
			cmds.setAttr(bProxFootR + '.type', 4)

			bProxToeR = cmds.joint(name=BG_N+"ProxToe",p=bLocToeR, rad= 3)
			cmds.xform(bProxToeR, ws=True, m=getTransMatrix(0, getVector(bLocToeR, bLocToeER), 1, [1,0,0], bLocToeR))
			cmds.setAttr(bProxToeR + '.type', 5)

			bProxToeER = cmds.joint(name=BG_N+"ProxToeE",p=bLocToeER, rad= 3)
			# #------------------------------
			cmds.select(bProxChest1)
			bProxShoulderR = cmds.joint(name=BG_N+"ProxShoulder",p=bLocShoulderR, rad= 5)
			cmds.xform(bProxShoulderR, ws=True, m=getTransMatrix(0, getVector(bLocShoulderR, bLocArmUpperR), 2, [0,0,1], bLocShoulderR))
			cmds.setAttr(bProxShoulderR + '.type', 10)

			bProxArmUpperR = cmds.joint(name=BG_N+"ProxArmUpper",p=bLocArmUpperR, rad= 5)
			cmds.xform(bProxArmUpperR, ws=True, m=getTransMatrix(0, getVector(bLocArmUpperR, bLocArmForeR), 2, [0,0,1], bLocArmUpperR))
			cmds.setAttr(bProxArmUpperR + '.type', 18)
			cmds.setAttr(bProxArmUpperR + '.otherType', 'UpperArm', type='string')

			bProxArmForeR = cmds.joint(name=BG_N+"ProxArmFore",p=bLocArmForeR, rad= 5)
			cmds.xform(bProxArmForeR, ws=True, m=getTransMatrix(0, getVector(bLocArmForeR, bLocHandR), 2, [0,0,1], bLocArmForeR))
			cmds.setAttr(bProxArmForeR + '.type', 18)
			cmds.setAttr(bProxArmForeR + '.otherType', 'ForeArm', type='string')

			bProxHandR = cmds.joint(name=BG_N+"ProxHand",p=bLocHandR, rad= 5)
			cmds.setAttr(bProxHandR + '.type', 12)
			pFCenter = [(bLocFinger00R[0]+bLocFinger10R[0]+bLocFinger20R[0]+bLocFinger30R[0]+bLocFinger40R[0])*0.2,
						(bLocFinger00R[1]+bLocFinger10R[1]+bLocFinger20R[1]+bLocFinger30R[1]+bLocFinger40R[1])*0.2,
						(bLocFinger00R[2]+bLocFinger10R[2]+bLocFinger20R[2]+bLocFinger30R[2]+bLocFinger40R[2])*0.2]
			hSideVec = getVector(bLocFinger40R, bLocFinger10R)
			cmds.xform(bProxHandR, ws=True, m=getTransMatrix(0, getVector(bLocHandR, pFCenter), 2, hSideVec, bLocHandR))

			bProxFinger00R = cmds.joint(name=BG_N+"ProxFinger00",p=bLocFinger00R,o=bRotFinger00R, rad= 2)
			cmds.setAttr(bProxFinger00R + '.type', 13)
			bProxFinger01R = cmds.joint(name=BG_N+"ProxFinger01",p=bLocFinger01R,o=bRotFinger01R, rad= 2)
			cmds.setAttr(bProxFinger01R + '.type', 13)
			cmds.transformLimits(bProxFinger01R, rx=[0,0], erx=[1,1],rz=[0,0], erz=[1,1])
			bProxFinger02R = cmds.joint(name=BG_N+"ProxFinger02",p=bLocFinger02R,o=bRotFinger02R, rad= 2)
			cmds.setAttr(bProxFinger02R + '.type', 13)
			cmds.transformLimits(bProxFinger02R, rx=[0,0], erx=[1,1],rz=[0,0], erz=[1,1])
			bProxFinger03R = cmds.joint(name=BG_N+"ProxFinger03",p=bLocFinger03R,o=bRotFinger03R, rad= 2)
			cmds.select(bProxHandR)
			bProxFinger10R = cmds.joint(name=BG_N+"ProxFinger10",p=bLocFinger10R,o=bRotFinger10R, rad= 2)
			cmds.setAttr(bProxFinger10R + '.type', 13)
			bProxFinger11R = cmds.joint(name=BG_N+"ProxFinger11",p=bLocFinger11R,o=bRotFinger11R, rad= 2)
			cmds.setAttr(bProxFinger11R + '.type', 13)
			cmds.transformLimits(bProxFinger11R, rx=[0,0], erx=[1,1],rz=[0,0], erz=[1,1])
			bProxFinger12R = cmds.joint(name=BG_N+"ProxFinger12",p=bLocFinger12R,o=bRotFinger12R, rad= 2)
			cmds.setAttr(bProxFinger12R + '.type', 13)
			cmds.transformLimits(bProxFinger12R, rx=[0,0], erx=[1,1],rz=[0,0], erz=[1,1])
			bProxFinger13R = cmds.joint(name=BG_N+"ProxFinger13",p=bLocFinger13R,o=bRotFinger13R, rad= 2)
			cmds.select(bProxHandR)
			bProxFinger20R = cmds.joint(name=BG_N+"ProxFinger20",p=bLocFinger20R,o=bRotFinger20R, rad= 2)
			cmds.setAttr(bProxFinger20R + '.type', 13)
			bProxFinger21R = cmds.joint(name=BG_N+"ProxFinger21",p=bLocFinger21R,o=bRotFinger21R, rad= 2)
			cmds.setAttr(bProxFinger21R + '.type', 13)
			cmds.transformLimits(bProxFinger21R, rx=[0,0], erx=[1,1],rz=[0,0], erz=[1,1])
			bProxFinger22R = cmds.joint(name=BG_N+"ProxFinger22",p=bLocFinger22R,o=bRotFinger22R, rad= 2)
			cmds.setAttr(bProxFinger22R + '.type', 13)
			cmds.transformLimits(bProxFinger22R, rx=[0,0], erx=[1,1],rz=[0,0], erz=[1,1])
			bProxFinger23R = cmds.joint(name=BG_N+"ProxFinger23",p=bLocFinger23R,o=bRotFinger23R, rad= 2)
			cmds.select(bProxHandR)
			bProxFinger30R = cmds.joint(name=BG_N+"ProxFinger30",p=bLocFinger30R,o=bRotFinger30R, rad= 2)
			cmds.setAttr(bProxFinger30R + '.type', 13)
			bProxFinger31R = cmds.joint(name=BG_N+"ProxFinger31",p=bLocFinger31R,o=bRotFinger31R, rad= 2)
			cmds.setAttr(bProxFinger31R + '.type', 13)
			cmds.transformLimits(bProxFinger31R, rx=[0,0], erx=[1,1],rz=[0,0], erz=[1,1])
			bProxFinger32R = cmds.joint(name=BG_N+"ProxFinger32",p=bLocFinger32R,o=bRotFinger32R, rad= 2)
			cmds.setAttr(bProxFinger32R + '.type', 13)
			cmds.transformLimits(bProxFinger32R, rx=[0,0], erx=[1,1],rz=[0,0], erz=[1,1])
			bProxFinger33R = cmds.joint(name=BG_N+"ProxFinger33",p=bLocFinger33R,o=bRotFinger33R, rad= 2)
			cmds.select(bProxHandR)
			bProxFinger40R = cmds.joint(name=BG_N+"ProxFinger40",p=bLocFinger40R,o=bRotFinger40R, rad= 2)
			cmds.setAttr(bProxFinger40R + '.type', 13)
			bProxFinger41R = cmds.joint(name=BG_N+"ProxFinger41",p=bLocFinger41R,o=bRotFinger41R, rad= 2)
			cmds.setAttr(bProxFinger41R + '.type', 13)
			cmds.transformLimits(bProxFinger41R, rx=[0,0], erx=[1,1],rz=[0,0], erz=[1,1])
			bProxFinger42R = cmds.joint(name=BG_N+"ProxFinger42",p=bLocFinger42R,o=bRotFinger42R, rad= 2)
			cmds.setAttr(bProxFinger42R + '.type', 13)
			cmds.transformLimits(bProxFinger42R, rx=[0,0], erx=[1,1],rz=[0,0], erz=[1,1])
			bProxFinger43R = cmds.joint(name=BG_N+"ProxFinger43",p=bLocFinger43R,o=bRotFinger43R, rad= 2)
			# #------------------------------
			
			cmds.parent(bProxHip,BipedGuideRoot)
			
			cmds.setAttr((bProxHip + ".overrideEnabled"), 1)
			cmds.setAttr((bProxHip + ".overrideRGBColors"), 1)
			cmds.setAttr((bProxHip + ".overrideColorR"), 1)
			cmds.setAttr((bProxHip + ".overrideColorG"), 0.214)
			cmds.setAttr((bProxHip + ".overrideColorB"), 0)
			
		
			if bIsZUp:
				cmds.setAttr( BipedGuideRoot+".rx", 90)

		cmds.select(d=True)


	@classmethod
	def onWireCrossArrowSizeChanged(self, value):
		self.fCrossArrowSize = value

	@classmethod
	def onWireCrossArrowBoldRatioChanged(self, value):
		self.fCrossArrowBold = value

	@classmethod
	def onWireArcCrossArrowRadiusChanged(self, value):
		self.fCrossArcArrowRadius = value

	@classmethod
	def onWireArcCrossArrowArcRangeChanged(self, value):
		self.fCrossArcArrowArcRange = value

	@classmethod
	def onSymmetryAxisSelectChanged(self, value):
		self.SymmetryFlipAxis = value

	@classmethod
	def onSwMatchPosChanged(self, value):
		# self.bMatchPos = value
		# print(value)
		if value > 0:
			self.bMatchPos = True
		else:
			self.bMatchPos = False

	@classmethod
	def onSwMatchRotChanged(self, value):
		if value > 0:
			self.bMatchRot = True
		else:
			self.bMatchRot = False

	@classmethod
	def onSwMatchSclChanged(self, value):
		# self.bMatchScl = value
		if value > 0:
			self.bMatchScl = True
		else:
			self.bMatchScl = False

	@classmethod
	def onSwSquash(self, value):
		# self.bSquash = value
		if value > 0:
			self.bSquash = True
		else:
			self.bSquash = False

	@classmethod
	def doCreateWireBox(self):
		self.createWireBox("WireBox", 5,5,5)
		# res = cmds.createNode('renderBox')
		# cmds.setAttr(res+'.sizeX', 5)
		# cmds.setAttr(res+'.sizeY', 5)
		# cmds.setAttr(res+'.sizeZ', 5)
		# cmds.setAttr((res + ".overrideEnabled"), 1)
		# cmds.setAttr((res + ".overrideRGBColors"), 1)
		# cmds.setAttr((res + ".overrideColorR"), 0)
		# cmds.setAttr((res + ".overrideColorG"), 1)
		# cmds.setAttr((res + ".overrideColorB"), 0)
		# cmds.select(cmds.listRelatives(res,p=True)[0])

	@classmethod
	def doCreateWireSphere(self):
		self.createWireSphere("WireSphere", 5)
		# res = cmds.createNode('renderSphere')
		# cmds.setAttr(res+'.radius', 5)
		# cmds.setAttr((res + ".overrideEnabled"), 1)
		# cmds.setAttr((res + ".overrideRGBColors"), 1)
		# cmds.setAttr((res + ".overrideColorR"), 0)
		# cmds.setAttr((res + ".overrideColorG"), 1)
		# cmds.setAttr((res + ".overrideColorB"), 0)
		# cmds.select(cmds.listRelatives(res,p=True)[0])

	@classmethod
	def doCreateWireRect(self):
		self.createWireRect("WireRec", 15,15)

	@classmethod
	def doCreateWireCrossArrow(self):
		self.createWireCrossArrow("WireCrossArrow", self.fCrossArrowSize, self.fCrossArrowBold)

	@classmethod
	def doCreateWireArcCrossArrow(self):
		self.createWireSpherifyCrossArrow("WireArcCrossArrow", self.fCrossArcArrowRadius,self.fCrossArcArrowArcRange, 1, False)

	@classmethod
	def doOpenColorPickerDialog(self):
		mods = cmds.getModifiers()
		if mods == 4:
			selList = cmds.ls(sl=True)
			if len(selList) > 0:
				shapes = cmds.listRelatives(selList[0], s=True)
				if shapes:
					if cmds.getAttr(shapes[0]+'.overrideRGBColors'):
						R = cmds.getAttr(shapes[0]+'.overrideColorR')
						G = cmds.getAttr(shapes[0]+'.overrideColorG')
						B = cmds.getAttr(shapes[0]+'.overrideColorB')
					else:
						colorIdx = cmds.getAttr(shapes[0]+'.overrideColor')
						RGB = cmds.colorIndex(colorIdx, q=True)
						R = RGB[0]
						G = RGB[1]
						B = RGB[2]
				else:
					if cmds.getAttr(selList[0]+'.overrideRGBColors'):
						R = cmds.getAttr(selList[0]+'.overrideColorR')
						G = cmds.getAttr(selList[0]+'.overrideColorG')
						B = cmds.getAttr(selList[0]+'.overrideColorB')
					else:
						colorIdx = cmds.getAttr(selList[0]+'.overrideColor')
						RGB = cmds.colorIndex(colorIdx, q=True)
						R = RGB[0]
						G = RGB[1]
						B = RGB[2]
				if R < 0.0:
					R = 0.0
				elif R > 1.0:
					R = 1.0

				if G < 0.0:
					G = 0.0
				elif G > 1.0:
					G = 1.0

				if B < 0.0:
					B = 0.0
				elif B > 1.0:
					B = 1.0
				self.rfWireColor[0]= R
				self.rfWireColor[1]= G
				self.rfWireColor[2]= B
				rr = math.pow(R, 0.4545454545) * 255
				gg = math.pow(G, 0.4545454545) * 255
				bb = math.pow(B, 0.4545454545) * 255
				self.btnColorPick.setStyleSheet("background-color:rgb("+str(rr)+","+str(gg)+","+str(bb)+")")
		else:
			colorDialog = QtGui.QColorDialog.getColor()
			if colorDialog.isValid():

				color = colorDialog.getRgb()
			
				self.rfWireColor[0]= math.pow(color[0]*0.0039215686, 2.2)
				self.rfWireColor[1]= math.pow(color[1]*0.0039215686, 2.2)
				self.rfWireColor[2]= math.pow(color[2]*0.0039215686, 2.2)
				self.btnColorPick.setStyleSheet("background-color:rgb("+str(color[0])+","+str(color[1])+","+str(color[2])+")")

	@classmethod
	def doOpenColorPickerDialog2(self):
		mods = cmds.getModifiers()
		if mods == 4:
			selList = cmds.ls(sl=True)
			if len(selList) > 0:
				shapes = cmds.listRelatives(selList[0], s=True)
				if shapes:
					if cmds.getAttr(shapes[0]+'.overrideRGBColors'):
						R = cmds.getAttr(shapes[0]+'.overrideColorR')
						G = cmds.getAttr(shapes[0]+'.overrideColorG')
						B = cmds.getAttr(shapes[0]+'.overrideColorB')
					else:
						colorIdx = cmds.getAttr(shapes[0]+'.overrideColor')
						RGB = cmds.colorIndex(colorIdx, q=True)
						R = RGB[0]
						G = RGB[1]
						B = RGB[2]
				else:
					if cmds.getAttr(selList[0]+'.overrideRGBColors'):
						R = cmds.getAttr(selList[0]+'.overrideColorR')
						G = cmds.getAttr(selList[0]+'.overrideColorG')
						B = cmds.getAttr(selList[0]+'.overrideColorB')
					else:
						colorIdx = cmds.getAttr(selList[0]+'.overrideColor')
						RGB = cmds.colorIndex(colorIdx, q=True)
						R = RGB[0]
						G = RGB[1]
						B = RGB[2]
				if R < 0.0:
					R = 0.0
				elif R > 1.0:
					R = 1.0

				if G < 0.0:
					G = 0.0
				elif G > 1.0:
					G = 1.0

				if B < 0.0:
					B = 0.0
				elif B > 1.0:
					B = 1.0
				self.rfWireColor2[0]= R
				self.rfWireColor2[1]= G
				self.rfWireColor2[2]= B
				rr = math.pow(R, 0.4545454545) * 255
				gg = math.pow(G, 0.4545454545) * 255
				bb = math.pow(B, 0.4545454545) * 255
				self.btnColor2Pick.setStyleSheet("background-color:rgb("+str(rr)+","+str(gg)+","+str(bb)+")")
		else:
			colorDialog = QtGui.QColorDialog.getColor()
			if colorDialog.isValid():

				color = colorDialog.getRgb()
			
				self.rfWireColor2[0]= math.pow(color[0]*0.0039215686, 2.2)
				self.rfWireColor2[1]= math.pow(color[1]*0.0039215686, 2.2)
				self.rfWireColor2[2]= math.pow(color[2]*0.0039215686, 2.2)
				self.btnColor2Pick.setStyleSheet("background-color:rgb("+str(color[0])+","+str(color[1])+","+str(color[2])+")")

	@classmethod
	def doSetWireColor(self):
		for obj in (cmds.ls(sl=True)):
			shapes = cmds.listRelatives(obj, s=True, f=True)
			if shapes:
				for sh in shapes:
					cmds.setAttr((sh + ".overrideEnabled"), 1)
					cmds.setAttr((sh + ".overrideRGBColors"), 1)
					cmds.setAttr((sh + ".overrideColorR"), self.rfWireColor[0])
					cmds.setAttr((sh + ".overrideColorG"), self.rfWireColor[1])
					cmds.setAttr((sh + ".overrideColorB"), self.rfWireColor[2])
			else:
				cmds.setAttr((obj + ".overrideEnabled"), 1)
				cmds.setAttr((obj + ".overrideRGBColors"), 1)
				cmds.setAttr((obj + ".overrideColorR"), self.rfWireColor[0])
				cmds.setAttr((obj + ".overrideColorG"), self.rfWireColor[1])
				cmds.setAttr((obj + ".overrideColorB"), self.rfWireColor[2])

	@classmethod
	def doSetGradiantWireColor(self):
		selList = cmds.ls(sl=True)
		actObj = []
		if len(selList) > 0:
			actObj = []
			for o in selList:
				oTypes = cmds.nodeType(o, inherited=True)

				if 'shape' in oTypes:
					tempObj = cmds.listRelatives(o, p=True)[0]
				else:
					tempObj = o

				if not (o in actObj):
					actObj.append(tempObj)

			num = len(actObj)
			if num > 1:
				mods = cmds.getModifiers()
				if mods == 4:
					Lab1 = RGB2Lab(self.rfWireColor)
					Lab2 = RGB2Lab(self.rfWireColor2)

					dL = (Lab2[0] - Lab1[0])/(num - 1.0)
					da = (Lab2[1] - Lab1[1])/(num - 1.0)
					db = (Lab2[2] - Lab1[2])/(num - 1.0)

					for i in range(num):
						RGB = Lab2RGB([Lab1[0]+dL*i, Lab1[1]+da*i, Lab1[2]+db*i])
						
						shapes = cmds.listRelatives(actObj[i], s=True, f=True)
						if shapes:
							for sh in shapes:
								cmds.setAttr((sh + ".overrideEnabled"), 1)
								cmds.setAttr((sh + ".overrideRGBColors"), 1)
								cmds.setAttr((sh + ".overrideColorR"), RGB[0])
								cmds.setAttr((sh + ".overrideColorG"), RGB[1])
								cmds.setAttr((sh + ".overrideColorB"), RGB[2])
						else:
							cmds.setAttr((actObj[i] + ".overrideEnabled"), 1)
							cmds.setAttr((actObj[i] + ".overrideRGBColors"), 1)
							cmds.setAttr((actObj[i] + ".overrideColorR"), RGB[0])
							cmds.setAttr((actObj[i] + ".overrideColorG"), RGB[1])
							cmds.setAttr((actObj[i] + ".overrideColorB"), RGB[2])
				elif mods == 8:
					hsv1 = RGB2HSV(self.rfWireColor)
					hsv2 = RGB2HSV(self.rfWireColor2)

					Dh1 = hsv2[0] - hsv1[0]
					if Dh1 > 180:
						hsv2[0] -= 360.0
					elif Dh1 < -180:
						hsv2[0] += 360.0
					dh = (hsv2[0] - hsv1[0])/(num - 1.0)
					ds = (hsv2[1] - hsv1[1])/(num - 1.0)
					dv = (hsv2[2] - hsv1[2])/(num - 1.0)
					

					for i in range(num):
						RGB = HSV2RGB([hsv1[0]+dh*i, hsv1[1]+ds*i, hsv1[2]+dv*i])
						
						shapes = cmds.listRelatives(actObj[i], s=True, f=True)
						if shapes:
							for sh in shapes:
								cmds.setAttr((sh + ".overrideEnabled"), 1)
								cmds.setAttr((sh + ".overrideRGBColors"), 1)
								cmds.setAttr((sh + ".overrideColorR"), RGB[0])
								cmds.setAttr((sh + ".overrideColorG"), RGB[1])
								cmds.setAttr((sh + ".overrideColorB"), RGB[2])
						else:
							cmds.setAttr((actObj[i] + ".overrideEnabled"), 1)
							cmds.setAttr((actObj[i] + ".overrideRGBColors"), 1)
							cmds.setAttr((actObj[i] + ".overrideColorR"), RGB[0])
							cmds.setAttr((actObj[i] + ".overrideColorG"), RGB[1])
							cmds.setAttr((actObj[i] + ".overrideColorB"), RGB[2])
				elif mods == 1:
					hsl1 = RGB2HSL(self.rfWireColor)
					hsl2 = RGB2HSL(self.rfWireColor2)

					Dh1 = hsl2[0] - hsl1[0]
					if Dh1 > 180:
						hsl2[0] -= 360.0
					elif Dh1 < -180:
						hsl2[0] += 360.0
					dh = (hsl2[0] - hsl1[0])/(num - 1.0)
					ds = (hsl2[1] - hsl1[1])/(num - 1.0)
					dl = (hsl2[2] - hsl1[2])/(num - 1.0)
					
					for i in range(num):
						RGB = HSL2RGB([hsl1[0]+dh*i, hsl1[1]+ds*i, hsl1[2]+dl*i])
						
						shapes = cmds.listRelatives(actObj[i], s=True, f=True)
						if shapes:
							for sh in shapes:
								cmds.setAttr((sh + ".overrideEnabled"), 1)
								cmds.setAttr((sh + ".overrideRGBColors"), 1)
								cmds.setAttr((sh + ".overrideColorR"), RGB[0])
								cmds.setAttr((sh + ".overrideColorG"), RGB[1])
								cmds.setAttr((sh + ".overrideColorB"), RGB[2])
						else:
							cmds.setAttr((actObj[i] + ".overrideEnabled"), 1)
							cmds.setAttr((actObj[i] + ".overrideRGBColors"), 1)
							cmds.setAttr((actObj[i] + ".overrideColorR"), RGB[0])
							cmds.setAttr((actObj[i] + ".overrideColorG"), RGB[1])
							cmds.setAttr((actObj[i] + ".overrideColorB"), RGB[2])
				else: #add
					RGB1 = self.rfWireColor
					RGB2 = self.rfWireColor2

					dR = (RGB2[0] - RGB1[0])/(num - 1.0)
					dG = (RGB2[1] - RGB1[1])/(num - 1.0)
					dB = (RGB2[2] - RGB1[2])/(num - 1.0)

					for i in range(num):
						RGB = [RGB1[0]+dR*i, RGB1[1]+dG*i, RGB1[2]+dB*i]

						shapes = cmds.listRelatives(actObj[i], s=True, f=True)
						if shapes:
							for sh in shapes:
								cmds.setAttr((sh + ".overrideEnabled"), 1)
								cmds.setAttr((sh + ".overrideRGBColors"), 1)
								cmds.setAttr((sh + ".overrideColorR"), RGB[0])
								cmds.setAttr((sh + ".overrideColorG"), RGB[1])
								cmds.setAttr((sh + ".overrideColorB"), RGB[2])
						else:
							cmds.setAttr((actObj[i] + ".overrideEnabled"), 1)
							cmds.setAttr((actObj[i] + ".overrideRGBColors"), 1)
							cmds.setAttr((actObj[i] + ".overrideColorR"), RGB[0])
							cmds.setAttr((actObj[i] + ".overrideColorG"), RGB[1])
							cmds.setAttr((actObj[i] + ".overrideColorB"), RGB[2])

				
			elif num == 1:
				shapes = cmds.listRelatives(actObj[0], s=True, f=True)
				if shapes:
					for sh in shapes:
						cmds.setAttr((sh + ".overrideEnabled"), 1)
						cmds.setAttr((sh + ".overrideRGBColors"), 1)
						cmds.setAttr((sh + ".overrideColorR"), self.rfWireColor[0])
						cmds.setAttr((sh + ".overrideColorG"), self.rfWireColor[1])
						cmds.setAttr((sh + ".overrideColorB"), self.rfWireColor[2])
				else:
					cmds.setAttr((actObj[0] + ".overrideEnabled"), 1)
					cmds.setAttr((actObj[0] + ".overrideRGBColors"), 1)
					cmds.setAttr((actObj[0] + ".overrideColorR"), self.rfWireColor[0])
					cmds.setAttr((actObj[0] + ".overrideColorG"), self.rfWireColor[1])
					cmds.setAttr((actObj[0] + ".overrideColorB"), self.rfWireColor[2])

	@classmethod
	def doSymmetryClone(self):
		selList = cmds.ls(sl = True)

		dupList = cmds.duplicate(selList,rc=True,name="DupObj_1")
		newSel = cmds.ls(sl = True)

		for obj in dupList:
			bCheck = False
			for com in newSel:
				if com == obj:
					bCheck = True
					break

			if (not bCheck) and cmds.objExists(obj):
				cmds.delete(obj)


		pDupList = []
		sysMatrix = []
		for obj in newSel:
			sysMatrix.append(self.getMatrixFliped( cmds.xform(obj,q=True,ws=True,m=True), self.SymmetryFlipAxis ))

		for obj in newSel:
			papa = cmds.listRelatives(obj, p=True)
			pDupList.append(papa)
			if papa != None:
				cmds.parent(obj, w=True)

		for idx in range(len(newSel)):
			cmds.xform(dupList[idx], ws=True, m=sysMatrix[idx])

		for idx in range(len(newSel)):
			if pDupList[idx]:
				cmds.parent(newSel[idx], pDupList[idx])

	@classmethod
	def doCreateIK(self):
		locList = cmds.ls(sl=True)
		cmds.select(d=True)
		if len(locList) == 3:
			point1 = cmds.xform(locList[0],q=True,ws=True,t=True)
			point2 = cmds.xform(locList[1],q=True,ws=True,t=True)
			point3 = cmds.xform(locList[2],q=True,ws=True,t=True)
			xAxis1 = getVector(point1, point2)
			xAxis2 = getVector(point2, point3)
			dis1 = getDistance(point1, point2)
			dis2 = getDistance(point2, point3)

			BN = crossVec(getVector(point2, point1),getVector(point2, point3))
			UpVec = crossVec(BN, getVector(point1, point3))
			UpVPos = [	(point1[0]+point3[0])*0.5+UpVec[0]*(dis1+dis2)*0.75,
						(point1[1]+point3[1])*0.5+UpVec[1]*(dis1+dis2)*0.75,
						(point1[2]+point3[2])*0.5+UpVec[2]*(dis1+dis2)*0.75]
			IKUpV = cmds.spaceLocator(name="IKUpV")[0]
			cmds.xform(IKUpV,ws=True,t=UpVPos)

			cmds.select(d=True)
			Bone1 = cmds.joint(p=point1)
			cmds.xform(Bone1, ws=True, m=getTransMatrix(0, xAxis1, 1, BN, point1))
			Bone2 = cmds.joint(p=point2)
			cmds.xform(Bone2, ws=True, m=getTransMatrix(0, xAxis2, 1, BN, point2))
			BoneEff = cmds.joint(p=point3)
			cmds.xform(BoneEff, ro=[0,0,0])
			cmds.makeIdentity([Bone1,Bone2,BoneEff],apply=True, t=True, r=True,s=True,n=2,pn=True)

			IKHandle = cmds.ikHandle(name="IKHandle",sj=Bone1, ee=BoneEff, sol="ikRPsolver")
			cmds.poleVectorConstraint(IKUpV, IKHandle[0], w=1)

		else:
			cmds.confirmDialog(title="Error", message="You must select 3 ref objects to create IK", button="OK")

	@classmethod
	def doCreateBone(self):
		locList = cmds.ls(sl=True)
		cmds.select(d=True)
		if len(locList) >= 2:
			
			for i in range(len(locList) - 1):
				bPos = cmds.xform(locList[i],q=True, ws=True, t=True)
				xAxis = getVector(bPos, cmds.xform(locList[i+1],q=True, ws=True, t=True))

				curBone = cmds.joint(p=bPos)
				cmds.xform(curBone, ws=True, m=getTransMatrix(0, xAxis, 2, [0,0,1], bPos))
				cmds.makeIdentity(curBone,apply=True, t=True, r=True,s=True,n=2,pn=True)

			lastBone = cmds.joint(p=cmds.xform(locList[len(locList) - 1],q=True, ws=True, t=True))
			cmds.xform(lastBone, ro=[0,0,0])
			cmds.makeIdentity(lastBone,apply=True, t=True, r=True,s=True,n=2,pn=True)
		else:
			cmds.confirmDialog(title="Error", message="You must select more then 2 ref objects...", button="OK")

	@classmethod
	def doAlignTo(self):
		# selList = cmds.ls(sl=True)
		# LocNode = cmds.spaceLocator(name="LocNode")[0]
		
		# if len(selList)==2:
		# 	# movObj = selList[0]
		# 	cmds.parentConstraint(selList[1], LocNode, mo=False)
		# 	cmds.scaleConstraint(selList[1], LocNode, mo=False)
		# 	# bIsAutoKey = cmds.autoKeyframe(q=True, state=True)
		# 	if self.bMatchPos:
		# 		cmds.xform(selList[0], ws=True, t=cmds.xform(LocNode,q=True,ws=True,t=True))
		# 	if self.bMatchRot:
		# 		cmds.xform(selList[0], ws=True, ro=cmds.xform(LocNode,q=True,ws=True,ro=True))
		# 	if self.bMatchScl:
		# 		cmds.xform(selList[0], ws=True, s=cmds.xform(LocNode,q=True,ws=True,s=True))

		# 	cmds.delete(LocNode)
		#=============================
		selList = cmds.ls(sl=True)
		if len(selList)==2:
			

			pCon = cmds.parentConstraint(selList[1], selList[0], mo=False)
			
			# if self.bMatchScl:
			# 	sCon = cmds.scaleConstraint(selList[1], selList[0], mo=False)

			posValue = cmds.xform(selList[0],q=True,ws=True,t=True)
			rotValue = cmds.xform(selList[0],q=True,ws=True,ro=True)
			# sclValue = cmds.xform(selList[0],q=True,ws=True,s=True)

			cmds.delete(pCon)

			# if self.bMatchScl:
			# 	cmds.delete(sCon)


			# if self.bMatchPos:
			cmds.xform(selList[0], ws=True, t=posValue)
			# if self.bMatchRot:
			cmds.xform(selList[0], ws=True, ro=rotValue)
			# if self.bMatchScl:
			# 	cmds.xform(selList[0], ws=True, s=sclValue)

			cmds.select(selList[0])
		# print("pressed AlignTo")

	@classmethod
	def doSetStretch(self):
		selList = cmds.ls(sl=True)
		if len(selList) == 1:
			child = cmds.listRelatives(selList[0], c=True)
			if len(child) == 1 and cmds.objectType(child[0]) == "joint":
				cLocPos = cmds.xform(child[0],q=True,ws=False,t=True)
				length = getDistance([0,0,0], cLocPos)
				if cLocPos[1] < 0.001 and cLocPos[2] < 0.001:
					AimTarget = cmds.spaceLocator(name="AimTarget")[0]
					AimTargetShape = cmds.listRelatives(AimTarget,c =True)[0]
					cmds.xform(AimTarget, ws=True, t=cmds.xform(child[0],q=True,ws=True,t=True))
					cmds.aimConstraint(AimTarget, selList[0], aim=[1,0,0], u=[0,1,0], wut="none")

					# StretchBoneLoc = cmds.spaceLocator(name=(selList[0]+"Loc"))[0]
					# StretchBoneLocShape = cmds.listRelatives(StretchBoneLoc,c =True)[0]
					# cmds.xform(StretchBoneLoc, ws=True, m=cmds.xform(selList[0],q=True,ws=True,m=True))
					# cmds.parent(StretchBoneLoc, selList[0])
					# cmds.pointConstraint(AimTarget, child[0])
					StretchWsPosNode =  cmds.shadingNode("pointMatrixMult",au=True)
					cmds.connectAttr(selList[0] + ".translate", StretchWsPosNode+".inPoint",f=True)
					cmds.connectAttr(selList[0] + ".parentMatrix[0]", StretchWsPosNode+".inMatrix",f=True)


					cmds.addAttr(selList[0], ln="refLength",at="double", k=False)
					cmds.setAttr(selList[0]+".refLength",length)

					DistanceNode = cmds.shadingNode("distanceBetween",au=True)
					# cmds.connectAttr(selList[0] + ".translate", DistanceNode+".point1",f=True)
					# cmds.connectAttr(AimTarget + ".translate", DistanceNode+".point2",f=True)
					cmds.connectAttr(AimTargetShape + ".worldPosition[0]", DistanceNode+".point1",f=True)
					cmds.connectAttr(StretchWsPosNode + ".output", DistanceNode+".point2",f=True)

					DivideLengthNode = cmds.shadingNode("multiplyDivide",au=True)
					cmds.setAttr(DivideLengthNode+".operation", 2)
					cmds.connectAttr(DistanceNode + ".distance", DivideLengthNode+".input1X",f=True)
					cmds.connectAttr(selList[0]+".refLength", DivideLengthNode+".input2X",f=True)
					cmds.connectAttr(DivideLengthNode+".outputX", selList[0]+".sx",f=True)
					
					if self.bSquash:
						invScaleNode = cmds.shadingNode("multiplyDivide",au=True)
						cmds.setAttr(invScaleNode+".operation", 2)
						# cmds.connectAttr(DivideLengthNode+".outputX", invScaleNode+".input1X",f=True)
						cmds.connectAttr(DivideLengthNode+".outputX", invScaleNode+".input2X",f=True)
						# cmds.disconnectAttr(DivideLengthNode+".outputX", invScaleNode+".input1X")
						cmds.setAttr(invScaleNode+".input1X",1)

						sqrtNode = cmds.shadingNode("multiplyDivide",au=True)
						cmds.setAttr(sqrtNode+".operation", 3)
						cmds.connectAttr(invScaleNode+".outputX", sqrtNode+".input1X",f=True)
						cmds.setAttr(sqrtNode+".input2X",0.5)

						cmds.connectAttr(sqrtNode+".outputX", selList[0]+".sy",f=True)
						cmds.connectAttr(sqrtNode+".outputX", selList[0]+".sz",f=True)

	@classmethod
	def doCreateTransFixRoot(self):
		# obj = cmds.ls(sl=True)[0]
		# pObj = cmds.listRelatives(obj, p=True)
		# objRoot = cmds.group(em=True, name=(obj+'Root'))
		# cmds.xform(objRoot,ws=True,m=cmds.xform(obj,q=True,ws=True,m=True))
		# if pObj:
		# 	cmds.parent(objRoot, pObj)

		# cmds.parent(obj, objRoot)
		if len(cmds.ls(sl=True)) == 1:
			self.createTransFixRoot(cmds.ls(sl=True)[0])
		# print("pressed Create Transiform Fix Root")

	@classmethod
	def onTabChanged(self, value):
		pass
		# print(self.staticMetaObject)

	@classmethod
	def doCreateBipedControl4(self):

		bIsZUp = False
		SceneUp = 1
		UpAxis = cmds.upAxis(q=True,ax=True)
		if UpAxis=="z":
			bIsZUp = True
			SceneUp = 2

		if cmds.objExists("BipedGuild"):
			NSPrefix = ""

			#--------------
			SNList = []
			HiddenList = []
			CtrlList = []
			BoneList = []
			MidItemList = []
			BoneConstraintList = []

			ListNoScl = []
			ListOnlyRot = []
			ListOnlyPos = []

			BGMathDict = {
				'ProxHip' : 'B_Hip',
				'ProxWaist' : 'B_Waist',
				'ProxChest' : 'B_Chest',
				'ProxChest1' : 'B_Chest1',
				'ProxNeck' : 'B_Neck',
				'ProxNeck1' : 'B_Neck1',
				'ProxShoulder' : 'B_Shoulder',
				'ProxArmUpper' : 'B_ArmUpper',
				'ProxArmFore' : 'B_ArmFore',
				'ProxHand' : 'B_Hand',
				'ProxFinger00' : 'B_Finger00',
				'ProxFinger01' : 'B_Finger01',
				'ProxFinger02' : 'B_Finger02',
				'ProxFinger10' : 'B_Finger10',
				'ProxFinger11' : 'B_Finger11',
				'ProxFinger12' : 'B_Finger12',
				'ProxFinger20' : 'B_Finger20',
				'ProxFinger21' : 'B_Finger21',
				'ProxFinger22' : 'B_Finger22',
				'ProxFinger30' : 'B_Finger30',
				'ProxFinger31' : 'B_Finger31',
				'ProxFinger32' : 'B_Finger32',
				'ProxFinger40' : 'B_Finger40',
				'ProxFinger41' : 'B_Finger41',
				'ProxFinger42' : 'B_Finger42',
				'ProxThigh' : 'B_Thigh',
				'ProxCalf' : 'B_Calf',
				'ProxFoot' : 'B_Foot',
				'ProxToe' : 'B_Toe'
			}

			bGuideTrain = getTrainNodes("ProxHip", True)

			#--------------
			SpineBList = ['ProxHip','ProxWaist','ProxChest','ProxChest1','ProxNeck']
			swPosList = []
			scpList = []

			for b in SpineBList:
				_pos = cmds.xform(b,q=True,ws=True,t=True)
				swPosList.append(dt.Vector(_pos))

			for i in range(1, len(SpineBList)):
				scpList.append(swPosList[i])

			vec1 = swPosList[2] - swPosList[1]
			vec2 = swPosList[3] - swPosList[2]
			vec3 = swPosList[4] - swPosList[3]

			vec12 = swPosList[3] - swPosList[1]
			vec23 = swPosList[4] - swPosList[2]

			biVec12 = vec2.normal()^vec1.normal()
			biVec23 = vec3.normal()^vec2.normal()

			upV1 = biVec12^vec12
			upV2 = biVec23^vec23

			p1 = vec12.normal() * vec12.length() * 0.5 + swPosList[1]
			p2 = vec23.normal() * vec23.length() * 0.5 + swPosList[2]
			scpList[1] = p1 + upV1 * 0.75
			scpList[2] = p2 + upV2 * 0.75

			oCurve = cmds.curve(n='spineCurve', d=3,p=scpList)
			MidItemList.append(oCurve)
			oCurveShape = cmds.listRelatives(oCurve, s=True)[0]
			ListCurveCtrl = []
			for i in range(len(scpList)):
				ListCurveCtrl.append(cmds.cluster(oCurve + '.cv[' + str(i) + ']', rel=True)[1])

			#記錄曲線原始長度
			curveLen = cmds.arclen(oCurve)
			cmds.addAttr(oCurve, ln='oriLength', at='double', k=False)
			cmds.setAttr(oCurve+'.oriLength', curveLen)

			#SplineIK伸縮度
			cmds.addAttr(oCurve, ln="flexible",at="double", k=False)
			cmds.setAttr(oCurve+'.flexible', 0.2)

			##
			spSeg1Len = vec1.length()
			spSeg2Len = vec2.length()
			spSeg3Len = vec3.length()
			spineTotalLen = spSeg1Len + spSeg2Len + spSeg3Len

			listSegRatio = [
				(spSeg1Len / spineTotalLen),
				((spSeg1Len+spSeg2Len) / spineTotalLen),
				((spSeg1Len+spSeg2Len+spSeg3Len) / spineTotalLen)
			]
			#Spine Curve Info
			spCurveInfo = cmds.createNode('curveInfo',n=oCurve+'CurveInfo')
			SNList.append(spCurveInfo)
			cmds.connectAttr(oCurveShape+'.worldSpace', spCurveInfo+'.inputCurve', f=True)

			spDiffLengh = cmds.shadingNode('plusMinusAverage',name=oCurve+'DiffLength',au=True)
			SNList.append(spDiffLengh)
			cmds.setAttr(spDiffLengh+'.operation', 2)
			# mel.eval('AEnewNonNumericMultiAddNewItem("' + spDiffLengh + '","input1D");')
			# mel.eval('AEnewNonNumericMultiAddNewItem("' + spDiffLengh + '","input1D");')
			cmds.connectAttr(spCurveInfo+'.arcLength', spDiffLengh+'.input1D[0]',f=True)
			cmds.connectAttr(oCurve+'.oriLength', spDiffLengh+'.input1D[1]',f=True)

			spStretchDiff = cmds.shadingNode('multiplyDivide',name=oCurve+'StretchDiff',au=True)
			SNList.append(spStretchDiff)
			cmds.setAttr(spStretchDiff+'.operation',1)
			cmds.connectAttr(spDiffLengh+'.output1D', spStretchDiff+'.input1X', f=True)
			cmds.connectAttr(oCurve+'.flexible', spStretchDiff+'.input2X', f=True)

			spActLength = cmds.shadingNode('plusMinusAverage',name=oCurve+'ActLength',au=True)
			SNList.append(spActLength)
			cmds.setAttr(spActLength+'.operation', 1)
			# mel.eval('AEnewNonNumericMultiAddNewItem("' + spActLength + '","input1D");')
			# mel.eval('AEnewNonNumericMultiAddNewItem("' + spActLength + '","input1D");')
			cmds.connectAttr(oCurve+'.oriLength', spActLength+'.input1D[0]',f=True)
			cmds.connectAttr(spStretchDiff+'.outputX', spActLength+'.input1D[1]',f=True)

			listPocInfo = []
			spStartPocInfo = cmds.createNode('pointOnCurveInfo', n=oCurve+'SpPocInfo0')
			SNList.append(spStartPocInfo)
			listPocInfo.append(spStartPocInfo)
			cmds.setAttr(spStartPocInfo+'.turnOnPercentage', 1)
			cmds.connectAttr(oCurveShape+'.worldSpace', spStartPocInfo+'.inputCurve', f=True)

			for i in range(3):
				_spActBoneLen = cmds.shadingNode('multiplyDivide',name=oCurve+'ActBoneLen'+str(i+1),au=True)
				SNList.append(_spActBoneLen)
				cmds.setAttr(_spActBoneLen+'.operation',1)
				cmds.connectAttr(spActLength+'.output1D', _spActBoneLen+'.input1X', f=True)
				cmds.setAttr(_spActBoneLen+'.input2X', listSegRatio[i])

				_spActBoneRatio = cmds.shadingNode('multiplyDivide',name=oCurve+'ActBoneRatio'+str(i+1),au=True)
				SNList.append(_spActBoneRatio)
				cmds.setAttr(_spActBoneRatio+'.operation',2)
				cmds.connectAttr(_spActBoneLen+'.outputX', _spActBoneRatio+'.input1X', f=True)
				cmds.connectAttr(spCurveInfo+'.arcLength', _spActBoneRatio+'.input2X', f=True)

				_spPocInfo = cmds.createNode('pointOnCurveInfo', n=oCurve+'SpPocInfo'+str(i+1))
				SNList.append(_spPocInfo)
				listPocInfo.append(_spPocInfo)
				cmds.setAttr(_spPocInfo+'.turnOnPercentage', 1)
				cmds.connectAttr(oCurveShape+'.worldSpace', _spPocInfo+'.inputCurve', f=True)
				cmds.connectAttr(_spActBoneRatio+'.outputX', _spPocInfo+'.parameter', f=True)

			listSpLoc = []
			for i in range(len(listPocInfo)):
				_spLoc = cmds.spaceLocator(n=oCurve+'SpJntLoc'+str(i))[0]
				listSpLoc.append(_spLoc)

				_spTmpMtx = cmds.shadingNode('composeMatrix',n=oCurve+'SpTmpMtx'+str(i),au=True)
				SNList.append(_spTmpMtx)
				cmds.connectAttr(listPocInfo[i]+'.position', _spTmpMtx+'.inputTranslate',f=True)
				# multMatrix

				_spLocalMtx = cmds.shadingNode('multMatrix',n=oCurve+'SpLocalMtx'+str(i),au=True)
				SNList.append(_spLocalMtx)
				cmds.connectAttr(_spTmpMtx+'.outputMatrix', _spLocalMtx+'.matrixIn[0]',f=True)
				cmds.connectAttr(_spLoc+'.parentInverseMatrix[0]', _spLocalMtx+'.matrixIn[1]',f=True)

				_spDecomMtx = cmds.shadingNode('decomposeMatrix',n=oCurve+'SpDecomMtx'+str(i),au=True)
				SNList.append(_spDecomMtx)
				cmds.connectAttr(_spLocalMtx+'.matrixSum', _spDecomMtx+'.inputMatrix')

				##
				cmds.connectAttr(_spDecomMtx+'.outputTranslate', _spLoc+'.translate')

			#-----------------
			MidItemList += ListCurveCtrl
			MidItemList += listSpLoc
			#----------------

			HipBGLoc = dt.Vector(cmds.xform("ProxHip",q=True,ws=True,t=True))
			
			# WaistBGLoc = cmds.xform("ProxWaist",q=True,ws=True,t=True)
			# ChestBGLoc = cmds.xform("ProxChest",q=True,ws=True,t=True)
			# Chest1BGLoc = cmds.xform("ProxChest1",q=True,ws=True,t=True)
			WaistBGLoc = dt.Vector(cmds.xform(listSpLoc[0],q=True,ws=True,t=True))
			ChestBGLoc = dt.Vector(cmds.xform(listSpLoc[1],q=True,ws=True,t=True))
			Chest1BGLoc = dt.Vector(cmds.xform(listSpLoc[2],q=True,ws=True,t=True))

			NeckBGLoc = dt.Vector(cmds.xform("ProxNeck",q=True,ws=True,t=True))
			HeadBGLoc = dt.Vector(cmds.xform("ProxHead",q=True,ws=True,t=True))
			HeadTopBGLoc = dt.Vector(cmds.xform("ProxHeadTop",q=True,ws=True,t=True))

			ChestEndXAxis = (NeckBGLoc - Chest1BGLoc).normal()
			HeadNavXAxis = (HeadBGLoc - HeadTopBGLoc).normal()

			NeckLength = (HeadBGLoc - NeckBGLoc).length()

			#--Neck Spline--
			NeckKnot1Loc = NeckBGLoc + ChestEndXAxis*(NeckLength*0.2)
			NeckKnot2Loc = HeadBGLoc + HeadNavXAxis*NeckLength*0.5

			nspList = [NeckBGLoc, NeckKnot1Loc, NeckKnot2Loc, HeadBGLoc]
			neckCurve = cmds.curve(d=3,p=nspList)
			MidItemList.append(neckCurve)
			neckCurveShape = cmds.listRelatives(neckCurve, s=True)[0]
			ListNeckCurveCtrl = []
			for i in range(len(nspList)):
				ListNeckCurveCtrl.append(cmds.cluster(neckCurve + '.cv[' + str(i) + ']', rel=True)[1])
			MidItemList += ListNeckCurveCtrl
			
			midNeckPocInfo = cmds.createNode('pointOnCurveInfo', n=neckCurve+'midNeckPocInfo')
			SNList.append(midNeckPocInfo)
			cmds.setAttr(midNeckPocInfo+'.turnOnPercentage', 1)
			cmds.setAttr(midNeckPocInfo+'.parameter', 0.65)# '.parameter'
			cmds.connectAttr(neckCurveShape+'.worldSpace', midNeckPocInfo+'.inputCurve', f=True)

			midNeckWrdMtx = cmds.createNode('composeMatrix', n=neckCurve+'midNeckWrdMtx')
			SNList.append(midNeckWrdMtx)
			cmds.connectAttr(midNeckPocInfo+'.position', midNeckWrdMtx+'.inputTranslate', f=True)

			neck1SpLocator = cmds.spaceLocator(n='neck1SpLocator')[0]
			MidItemList.append(neck1SpLocator)

			midNeckLocMtx = cmds.createNode('multMatrix', n=neckCurve+'midNeckLocMtx')
			SNList.append(midNeckLocMtx)
			cmds.connectAttr(midNeckWrdMtx+'.outputMatrix', midNeckLocMtx+'.matrixIn[0]', f=True)
			cmds.connectAttr(neck1SpLocator+'.parentInverseMatrix[0]', midNeckLocMtx+'.matrixIn[1]', f=True)

			midNeckLocDecomMtx = cmds.createNode('decomposeMatrix', n=neckCurve+'midNeckLocDecomMtx')
			SNList.append(midNeckLocDecomMtx)
			cmds.connectAttr(midNeckLocMtx+'.matrixSum', midNeckLocDecomMtx+'.inputMatrix', f=True)


			cmds.connectAttr(midNeckLocDecomMtx+'.outputTranslate', neck1SpLocator + '.translate', f=True)

			Neck1BGLoc = dt.Vector(cmds.getAttr(midNeckPocInfo+'.position'))


			#--


			ShoulderList = []
			for obj in bGuideTrain:
				if cmds.getAttr(obj+".type") == 10:
					ShoulderList.append(obj)

			UpArmList = []
			for obj in bGuideTrain:
				if (cmds.getAttr(obj+".type") == 18) and (cmds.getAttr(obj+".otherType") == "UpperArm"):
					UpArmList.append(obj)

			ThighList = []
			for obj in bGuideTrain:
				if (cmds.getAttr(obj+".type") == 18) and (cmds.getAttr(obj+".otherType") == "Thigh"):
					ThighList.append(obj)

			TailList = []
			for obj in bGuideTrain:
				if (cmds.getAttr(obj+".type") == 18) and (cmds.getAttr(obj+".otherType") == "Tail0"):
					TailList.append(obj)

			
			#============Bone Joint===============
			
			if bIsZUp:
				wFrontVec = [0,-1,0]
			else:
				wFrontVec = [0,0,1]

			cmds.select( d=True )
			BRoot = cmds.joint(name="root",p=[0,0,0], rad= 3.5)
			BHip = cmds.joint(name="B_Hip",p=HipBGLoc, rad= 3.5)
			cmds.xform("B_Hip",ws=True,m=getTransMatrix(0, getVector(HipBGLoc, WaistBGLoc), 1, wFrontVec, HipBGLoc))
			BoneList.append(BHip)
			BWaist = cmds.joint(name="B_Waist",p=WaistBGLoc, rad= 3.5)
			cmds.xform("B_Waist",ws=True,m=getTransMatrix(0, getVector(WaistBGLoc, ChestBGLoc), 1, wFrontVec, WaistBGLoc))
			BoneList.append(BWaist)
			BChest = cmds.joint(name="B_Chest",p=ChestBGLoc, rad= 3.5)
			cmds.xform("B_Chest",ws=True,m=getTransMatrix(0, getVector(ChestBGLoc, Chest1BGLoc), 1, wFrontVec, ChestBGLoc))
			BoneList.append(BChest)
			BChest1 = cmds.joint(name="B_Chest1",p=Chest1BGLoc, rad= 3.5)
			cmds.xform("B_Chest1",ws=True,m=getTransMatrix(0, getVector(Chest1BGLoc, NeckBGLoc), 1, wFrontVec, Chest1BGLoc))
			BoneList.append(BChest1)
			BNeck = cmds.joint(name="B_Neck",p=NeckBGLoc, rad= 3.5)
			cmds.xform("B_Neck",ws=True,m=getTransMatrix(0, getVector(NeckBGLoc, Neck1BGLoc), 1, wFrontVec, NeckBGLoc))
			BoneList.append(BNeck)
			BNeck1 = cmds.joint(name="B_Neck1",p=Neck1BGLoc, rad= 3.5)
			cmds.xform("B_Neck1",ws=True,m=getTransMatrix(0, getVector(Neck1BGLoc, HeadBGLoc), 1, wFrontVec, Neck1BGLoc))
			BoneList.append(BNeck1)
			BHead = cmds.joint(name="B_Head",p=HeadBGLoc, rad= 3.5)
			cmds.xform("B_Head",ws=True,m=getTransMatrix(0, getVector(HeadBGLoc, HeadTopBGLoc), 1, wFrontVec, HeadBGLoc))
			BoneList.append(BHead)
			EndHead = cmds.joint(name="end_Head",p=HeadTopBGLoc, rad= 3.5)
			cmds.xform("end_Head",ro=[0,0,0])
			#-------------
			spLocRoot = cmds.spaceLocator(name='spLocRoot')[0]
			spLocWaist = cmds.spaceLocator(name='spLocWaist')[0]
			spLocChest = cmds.spaceLocator(name='spLocChest')[0]
			spLocChest1 = cmds.spaceLocator(name='spLocChest1')[0]
			spLocEnd = cmds.spaceLocator(name='spLocEnd')[0]
			cmds.parent(spLocWaist, spLocRoot)
			cmds.parent(spLocChest, spLocWaist)
			cmds.parent(spLocChest1, spLocChest)
			cmds.parent(spLocEnd, spLocChest1)
			HiddenList += [spLocRoot, spLocWaist, spLocChest, spLocChest1, spLocEnd]
			cmds.xform(spLocRoot,  ws=True,m=getTransMatrix(0, getVector(WaistBGLoc, ChestBGLoc),  1, [-1,0,0], WaistBGLoc))
			cmds.xform(spLocWaist, ws=True,m=getTransMatrix(0, getVector(WaistBGLoc, ChestBGLoc),  1, [-1,0,0], WaistBGLoc))
			cmds.xform(spLocChest, ws=True,m=getTransMatrix(0, getVector(ChestBGLoc, Chest1BGLoc), 1, [-1,0,0], ChestBGLoc))
			cmds.xform(spLocChest1,ws=True,m=getTransMatrix(0, getVector(Chest1BGLoc, NeckBGLoc),  1, [-1,0,0], Chest1BGLoc))
			cmds.xform(spLocEnd,   ws=True,m=getTransMatrix(0, getVector(NeckBGLoc, HeadBGLoc),    1, [-1,0,0], NeckBGLoc))
			# listSpLoc
			cmds.pointConstraint(listSpLoc[0], spLocWaist)
			cmds.pointConstraint(listSpLoc[1], spLocChest)
			cmds.pointConstraint(listSpLoc[2], spLocChest1)
			cmds.pointConstraint(listSpLoc[3], spLocEnd)
			cmds.aimConstraint(listSpLoc[1], spLocWaist,  aim=[1,0,0], u=[0,1,0], wut="none")
			cmds.aimConstraint(listSpLoc[2], spLocChest,  aim=[1,0,0], u=[0,1,0], wut="none")
			cmds.aimConstraint(listSpLoc[3], spLocChest1, aim=[1,0,0], u=[0,1,0], wut="none")


			cmds.select( d=True )
			spWaist = cmds.joint(name="spWaist",p=WaistBGLoc, rad= 0.5)
			cmds.xform(spWaist,ws=True,m=getTransMatrix(0, getVector(WaistBGLoc, ChestBGLoc),  1, [-1,0,0], WaistBGLoc))
			spChest = cmds.joint(name="spChest",p=ChestBGLoc, rad= 0.5)
			cmds.xform(spChest,ws=True,m=getTransMatrix(0, getVector(ChestBGLoc, Chest1BGLoc), 1, [-1,0,0], ChestBGLoc))
			spChest1 = cmds.joint(name="spChest1",p=Chest1BGLoc, rad= 0.5)
			cmds.xform(spChest1,ws=True,m=getTransMatrix(0, getVector(Chest1BGLoc, NeckBGLoc), 1, [-1,0,0], Chest1BGLoc))
			spEnd = cmds.joint(name="spEnd",p=NeckBGLoc, rad= 0.5)
			cmds.xform(spEnd,ws=True,m=getTransMatrix(0, getVector(NeckBGLoc, HeadBGLoc),      1, [-1,0,0], NeckBGLoc))
			HiddenList += [spWaist, spChest, spChest1, spEnd]


			# return

			Chest1Trans = cmds.xform(BChest1, q=True,ws=True,m=True)
			Chest1Fw = getRowFromMatrix(Chest1Trans,1)
			HipTrans = cmds.xform(BHip,q=True,ws=True,m=True)
			HipDownDir = invertVec(getRowFromMatrix(HipTrans, 0))
			HipFwDir = getRowFromMatrix(HipTrans, 1)

			CtrlRoot = self.createWireCrossArrow("ControlRoot", 90, 0.6, [0.1,1.0,0.1],[0,0,0],SceneUp)
			CtrlList.append(CtrlRoot)
			ListNoScl.append(CtrlRoot)
			CtrlHip = self.createWireRect("Hip", 80, 60, [0,0,0], [0,0.3,1])
			CtrlList.append(CtrlHip)
			ListNoScl.append(CtrlHip)
			if not bIsZUp:
				cmds.setAttr(CtrlHip+".rotateOrder", 1)
				cmds.xform(CtrlHip,ws=True,m=getTransMatrix(1, getVector(HipBGLoc, WaistBGLoc), 0, [1,0,0], HipBGLoc))
			else:
				cmds.setAttr(CtrlHip+".rotateOrder", 5)
				cmds.xform(CtrlHip,ws=True,m=getTransMatrix(2, getVector(HipBGLoc, WaistBGLoc), 0, [1,0,0], HipBGLoc))
			cmds.parent(CtrlHip, CtrlRoot)
			detCtrlHip = cmds.spaceLocator(n='detCtrlHip')[0]
			cmds.xform(detCtrlHip,ws=True,m=getTransMatrix(0, getVector(HipBGLoc, WaistBGLoc), 1, [-1,0,0], HipBGLoc))
			cmds.parent(detCtrlHip, CtrlHip)
			cmds.parent(spLocRoot, CtrlHip)
			cmds.parent(spWaist, CtrlHip)
			HiddenList.append(detCtrlHip)
			
			cmds.addAttr(CtrlRoot, ln="SoftIkArm", k=True,w=True,at="float", dv=0, hxv=True, hnv=True, max=1, min=0)
			cmds.addAttr(CtrlRoot, ln="SoftIkLeg", k=True,w=True,at="float", dv=0, hxv=True, hnv=True, max=1, min=0)


			locChest = cmds.createNode('transform',n='locChest')
			cmds.parent(locChest, CtrlRoot)
			cmds.pointConstraint(CtrlHip, locChest)

			CtrlChest = self.createWireRect("Chest", 80, 60, [0,0,0], [0,0.3,1])
			CtrlList.append(CtrlChest)
			ListNoScl.append(CtrlChest)
			CenChest = scaleVec(sumVec(ChestBGLoc, NeckBGLoc),0.5)
			
			if not bIsZUp:
				cmds.setAttr(CtrlChest+".rotateOrder", 1)
				cmds.xform(CtrlChest,ws=True,m=getTransMatrix(1, getVector(ChestBGLoc, NeckBGLoc), 0, [1,0,0], CenChest))
			else:
				cmds.setAttr(CtrlChest+".rotateOrder", 5)
				cmds.xform(CtrlChest,ws=True,m=getTransMatrix(2, getVector(ChestBGLoc, NeckBGLoc), 0, [1,0,0], CenChest))
			
			cmds.parent(CtrlChest, locChest)
			detCtrlChest = cmds.spaceLocator(n='detCtrlChest')[0]
			cmds.xform(detCtrlChest,ws=True,m=getTransMatrix(0, getVector(ChestBGLoc, NeckBGLoc), 1, [-1,0,0], CenChest))
			cmds.parent(detCtrlChest, CtrlChest)
			HiddenList.append(detCtrlChest)


			locChest1 = cmds.createNode('transform', n='Chest1')
			cmds.xform(locChest1,ws=True,m=cmds.xform(spChest1,q=True,ws=True,m=True))
			cmds.parent(locChest1, CtrlRoot)
			# MidItemList.append(locChest1)
			cmds.parentConstraint(spChest1, locChest1, mo=True)

			#--------------
			cmds.parentConstraint(CtrlHip,   ListCurveCtrl[0], mo=True)
			cmds.parentConstraint(CtrlChest, ListCurveCtrl[1], mo=True)
			cmds.parentConstraint(CtrlChest, ListCurveCtrl[2], mo=True)
			cmds.parentConstraint(CtrlChest, ListCurveCtrl[3], mo=True)
			#--------------
			hipBaseChestMtx = cmds.shadingNode('multMatrix',n='hipBaseChestMtx',au=True)
			SNList.append(hipBaseChestMtx)
			cmds.connectAttr(detCtrlChest+'.worldMatrix[0]', hipBaseChestMtx+'.matrixIn[0]',f=True)
			cmds.connectAttr(spLocChest1+'.worldInverseMatrix[0]', hipBaseChestMtx+'.matrixIn[1]',f=True)

			decompHipBaseChestMtx = cmds.shadingNode('decomposeMatrix',n='decompHipBaseChestMtx',au=True)
			SNList.append(decompHipBaseChestMtx)
			cmds.connectAttr(hipBaseChestMtx+'.matrixSum', decompHipBaseChestMtx+'.inputMatrix',f=True)

			dhbcm2Euler = cmds.shadingNode('quatToEuler',n='dhbcm2Euler',au=True)
			SNList.append(dhbcm2Euler)
			cmds.connectAttr(decompHipBaseChestMtx+'.outputQuatX', dhbcm2Euler+'.inputQuatX',f=True)
			cmds.connectAttr(decompHipBaseChestMtx+'.outputQuatW', dhbcm2Euler+'.inputQuatW',f=True)

			##
			#waist
			sclWaistRoll = cmds.shadingNode('multiplyDivide',name='sclWaistRoll',au=True)
			SNList.append(sclWaistRoll)
			cmds.connectAttr(dhbcm2Euler+'.outputRotate', sclWaistRoll+'.input1',f=True)
			cmds.setAttr(sclWaistRoll+'.input2', 0.4,0.4,0.4,type='double3')
			
			rollWaistMtx = cmds.shadingNode('composeMatrix',name='rollWaistMtx',au=True)
			SNList.append(rollWaistMtx)
			cmds.connectAttr(sclWaistRoll+'.output', rollWaistMtx+'.inputRotate',f=True)

			mixWaistWsMtx = cmds.shadingNode('multMatrix',n='mixWaistWsMtx',au=True)
			SNList.append(mixWaistWsMtx)
			cmds.connectAttr(rollWaistMtx+'.outputMatrix', mixWaistWsMtx+'.matrixIn[0]',f=True)
			cmds.connectAttr(spLocWaist+'.worldMatrix[0]', mixWaistWsMtx+'.matrixIn[1]',f=True)

			spWaistLsMtx = cmds.shadingNode('multMatrix',n='spWaistLsMtx',au=True)
			SNList.append(spWaistLsMtx)
			cmds.connectAttr(mixWaistWsMtx+'.matrixSum', spWaistLsMtx+'.matrixIn[0]',f=True)
			cmds.connectAttr(spWaist+'.parentInverseMatrix[0]', spWaistLsMtx+'.matrixIn[1]',f=True)

			spWaistTransInfo = cmds.shadingNode('decomposeMatrix',n='spWaistTransInfo',au=True)
			SNList.append(spWaistTransInfo)
			cmds.connectAttr(spWaistLsMtx+'.matrixSum', spWaistTransInfo+'.inputMatrix',f=True)
			cmds.connectAttr(spWaistTransInfo+'.outputTranslate', spWaist+'.translate', f=True)
			cmds.connectAttr(spWaistTransInfo+'.outputRotate', spWaist+'.rotate', f=True)

			#chest
			sclChestRoll = cmds.shadingNode('multiplyDivide',name='sclChestRoll',au=True)
			SNList.append(sclChestRoll)
			cmds.connectAttr(dhbcm2Euler+'.outputRotate', sclChestRoll+'.input1',f=True)
			cmds.setAttr(sclChestRoll+'.input2', 0.8,0.8,0.8,type='double3')
			
			rollChestMtx = cmds.shadingNode('composeMatrix',name='rollChestMtx',au=True)
			SNList.append(rollChestMtx)
			cmds.connectAttr(sclChestRoll+'.output', rollChestMtx+'.inputRotate',f=True)

			mixChestWsMtx = cmds.shadingNode('multMatrix',n='mixChestWsMtx',au=True)
			SNList.append(mixChestWsMtx)
			cmds.connectAttr(rollChestMtx+'.outputMatrix', mixChestWsMtx+'.matrixIn[0]',f=True)
			cmds.connectAttr(spLocChest+'.worldMatrix[0]', mixChestWsMtx+'.matrixIn[1]',f=True)

			spChestLsMtx = cmds.shadingNode('multMatrix',n='spChestLsMtx',au=True)
			SNList.append(spChestLsMtx)
			cmds.connectAttr(mixChestWsMtx+'.matrixSum', spChestLsMtx+'.matrixIn[0]',f=True)
			cmds.connectAttr(spChest+'.parentInverseMatrix[0]', spChestLsMtx+'.matrixIn[1]',f=True)

			spChestTransInfo = cmds.shadingNode('decomposeMatrix',n='spChestTransInfo',au=True)
			SNList.append(spChestTransInfo)
			cmds.connectAttr(spChestLsMtx+'.matrixSum', spChestTransInfo+'.inputMatrix',f=True)
			cmds.connectAttr(spChestTransInfo+'.outputTranslate', spChest+'.translate', f=True)
			cmds.connectAttr(spChestTransInfo+'.outputRotate', spChest+'.rotate', f=True)

			#chest1
			sclChest1Roll = cmds.shadingNode('multiplyDivide',name='sclChest1Roll',au=True)
			SNList.append(sclChest1Roll)
			cmds.connectAttr(dhbcm2Euler+'.outputRotate', sclChest1Roll+'.input1',f=True)
			cmds.setAttr(sclChest1Roll+'.input2', 1,1,1,type='double3')
			
			rollChest1Mtx = cmds.shadingNode('composeMatrix',name='rollChest1Mtx',au=True)
			SNList.append(rollChest1Mtx)
			cmds.connectAttr(sclChest1Roll+'.output', rollChest1Mtx+'.inputRotate',f=True)

			mixChest1WsMtx = cmds.shadingNode('multMatrix',n='mixChest1WsMtx',au=True)
			SNList.append(mixChest1WsMtx)
			cmds.connectAttr(rollChest1Mtx+'.outputMatrix', mixChest1WsMtx+'.matrixIn[0]',f=True)
			cmds.connectAttr(spLocChest1+'.worldMatrix[0]', mixChest1WsMtx+'.matrixIn[1]',f=True)

			spChest1LsMtx = cmds.shadingNode('multMatrix',n='spChest1LsMtx',au=True)
			SNList.append(spChest1LsMtx)
			cmds.connectAttr(mixChest1WsMtx+'.matrixSum', spChest1LsMtx+'.matrixIn[0]',f=True)
			cmds.connectAttr(spChest1+'.parentInverseMatrix[0]', spChest1LsMtx+'.matrixIn[1]',f=True)

			spChest1TransInfo = cmds.shadingNode('decomposeMatrix',n='spChest1TransInfo',au=True)
			SNList.append(spChest1TransInfo)
			cmds.connectAttr(spChest1LsMtx+'.matrixSum', spChest1TransInfo+'.inputMatrix',f=True)
			cmds.connectAttr(spChest1TransInfo+'.outputTranslate', spChest1+'.translate', f=True)
			cmds.connectAttr(spChest1TransInfo+'.outputRotate', spChest1+'.rotate', f=True)
			

			# lockChestPos = cmds.spaceLocator(name="lkChestPos")[0]
			# cmds.xform(lockChestPos, ws=True, t=ChestBGLoc)
			# cmds.parent(lockChestPos, CtrlWaist)
			# HiddenList.append(lockChestPos)

			# CHESTPC = cmds.pointConstraint(lockChestPos, CtrlChest)[0]
			# cmds.setAttr(CHESTPC+".nds", k=False, cb=False)
			# cmds.setAttr(CHESTPC+".ox", k=False, cb=False)
			# cmds.setAttr(CHESTPC+".oy", k=False, cb=False)
			# cmds.setAttr(CHESTPC+".oz", k=False, cb=False)
			# cmds.setAttr(CHESTPC+".w0", k=False, cb=False)

			# buffWaist = cmds.group(em=True, name="bufWaist")#cmds.spaceLocator(name="bufWaist")[0]
			# cmds.xform(buffWaist, ws=True, t=WaistBGLoc)
			# cmds.parent(buffWaist, CtrlHip)
			# RC_BUW = cmds.orientConstraint(CtrlHip, CtrlChest, buffWaist)
			# cmds.setAttr(RC_BUW[0] + ".interpType", 2)

			# cmds.parent(CtrlWaist, buffWaist)

			# if not bIsZUp:
			# 	CtrlChest1 = self.createWireSpherifyCrossArrow("Chest1", 25, 90, 2, True, [0,0.15,0.7])
			# 	cmds.setAttr(CtrlChest1+".rotateOrder", 1)
			# 	cmds.xform(CtrlChest1,ws=True,m=getTransMatrix(1, getVector(Chest1BGLoc, NeckBGLoc), 0, [1,0,0], Chest1BGLoc))
			# else:
			# 	CtrlChest1 = self.createWireSpherifyCrossArrow("Chest1", 25, 90, 1, False, [0,0.15,0.7])
			# 	cmds.setAttr(CtrlChest1+".rotateOrder", 5)
			# 	cmds.xform(CtrlChest1,ws=True,m=getTransMatrix(2, getVector(Chest1BGLoc, NeckBGLoc), 0, [1,0,0], Chest1BGLoc))
			# cmds.parent(CtrlChest1, CtrlChest)
			# CtrlList.append(CtrlChest1)
			# ListOnlyRot.append(CtrlChest1)

			# if not bIsZUp:
			# 	CtrlNeck = self.createWireSpherifyCrossArrow("Neck", getDistance(NeckBGLoc, HeadBGLoc) * 1.8, 60, 2, True, [0,0.8,0.5])
			# 	cmds.setAttr(CtrlNeck+".rotateOrder", 1)
			# 	cmds.xform(CtrlNeck,ws=True,m=getTransMatrix(1, getVector(NeckBGLoc, HeadBGLoc), 0, [1,0,0], NeckBGLoc))
			# else:
			# 	CtrlNeck = self.createWireSpherifyCrossArrow("Neck", getDistance(NeckBGLoc, HeadBGLoc) * 1.8, 60, 1, False, [0,0.8,0.5])
			# 	cmds.setAttr(CtrlNeck+".rotateOrder", 5)
			# 	cmds.xform(CtrlNeck,ws=True,m=getTransMatrix(2, getVector(NeckBGLoc, HeadBGLoc), 0, [1,0,0], NeckBGLoc))
			# cmds.parent(CtrlNeck, spChest1)
			# # cmds.parent(CtrlNeck, CtrlChest1)
			# CtrlList.append(CtrlNeck)
			# ListOnlyRot.append(CtrlNeck)

			refSize = getDistance(HeadBGLoc, HeadTopBGLoc)
			


			if not bIsZUp:
				CtrlHead = self.createWireBox("Head", refSize*1.2, refSize*1.2, refSize*1.4, [0, refSize*0.5,0], [1.0, 0.5, 0.2])
				cmds.setAttr(CtrlHead+".rotateOrder", 1)
				cmds.xform(CtrlHead,ws=True,m=getTransMatrix(1, getVector(HeadBGLoc, HeadTopBGLoc), 0, [1,0,0], HeadBGLoc))
			else:
				CtrlHead = self.createWireBox("Head", refSize*1.2, refSize*1.2, refSize*1.4, [0,0,refSize*0.5], [1.0, 0.5, 0.2])
				cmds.setAttr(CtrlHead+".rotateOrder", 5)
				cmds.xform(CtrlHead,ws=True,m=getTransMatrix(2, getVector(HeadBGLoc, HeadTopBGLoc), 0, [1,0,0], HeadBGLoc))
			HeadRoot = cmds.createNode('transform',n='HeadRoot')
			cmds.xform(HeadRoot,ws=True,m=(cmds.xform(CtrlHead,q=True,ws=True,m=True)))
			cmds.parent(HeadRoot, CtrlRoot)
			cmds.parent(CtrlHead, HeadRoot)
			CtrlList.append(CtrlHead)
			ListNoScl.append(CtrlHead)

			lockPointHead = cmds.spaceLocator(name="lpHead")[0]
			cmds.xform(lockPointHead,ws=True,t=HeadBGLoc)
			cmds.parent(lockPointHead, locChest1)
			# cmds.parent(lockPointHead, CtrlNeck)
			HiddenList.append(lockPointHead)

			# HEADPC = cmds.pointConstraint(lockPointHead, CtrlHead)[0]
			# cmds.setAttr(HEADPC+".nds", k=False, cb=False)
			# cmds.setAttr(HEADPC+".ox", k=False, cb=False)
			# cmds.setAttr(HEADPC+".oy", k=False, cb=False)
			# cmds.setAttr(HEADPC+".oz", k=False, cb=False)
			# cmds.setAttr(HEADPC+".w0", k=False, cb=False)
			cmds.pointConstraint(lockPointHead, HeadRoot)

			# return
			#------------
			# constrain bone joint
			proxyHip = cmds.spaceLocator(name="pyHip")[0]
			cmds.xform(proxyHip,ws=True,m=cmds.xform(BHip,q=True,ws=True,m=True))
			cmds.parent(proxyHip, CtrlHip)
			HiddenList.append(proxyHip)
			
			proxyWaist = cmds.spaceLocator(name="pyWaist")[0]
			cmds.xform(proxyWaist,ws=True,m=cmds.xform(BWaist,q=True,ws=True,m=True))
			cmds.parent(proxyWaist, spWaist)
			# cmds.parent(proxyWaist, CtrlWaist)
			HiddenList.append(proxyWaist)

			proxyChest = cmds.spaceLocator(name="pyChest")[0]
			cmds.xform(proxyChest,ws=True,m=cmds.xform(BChest,q=True,ws=True,m=True))
			cmds.parent(proxyChest, spChest)
			# cmds.parent(proxyChest, CtrlChest)
			HiddenList.append(proxyChest)

			proxyChest1 = cmds.spaceLocator(name="pyChest1")[0]
			cmds.xform(proxyChest1,ws=True,m=cmds.xform(BChest1,q=True,ws=True,m=True))
			cmds.parent(proxyChest1, spChest1)
			# cmds.parent(proxyChest1, CtrlChest1)
			HiddenList.append(proxyChest1)
			
			# proxyNeck = cmds.spaceLocator(name="pyNeck")[0]
			# cmds.xform(proxyNeck,ws=True,m=cmds.xform(BNeck,q=True,ws=True,m=True))
			# cmds.parent(proxyNeck, CtrlNeck)
			# HiddenList.append(proxyNeck)

			proxyHead = cmds.spaceLocator(name="pyHead")[0]
			cmds.xform(proxyHead,ws=True,m=cmds.xform(BHead,q=True,ws=True,m=True))
			cmds.parent(proxyHead, CtrlHead)
			HiddenList.append(proxyHead)

			BoneConstraintList.append(cmds.parentConstraint(proxyHip, BHip, mo=False)[0])
			BoneConstraintList.append(cmds.parentConstraint(proxyWaist, BWaist, mo=False)[0])
			BoneConstraintList.append(cmds.parentConstraint(proxyChest, BChest, mo=False)[0])
			BoneConstraintList.append(cmds.parentConstraint(proxyChest1, BChest1, mo=False)[0])
			# BoneConstraintList.append(cmds.parentConstraint(proxyNeck, BNeck, mo=False)[0])
			BoneConstraintList.append(cmds.parentConstraint(proxyHead, BHead, mo=False)[0])
			#------------
			cmds.select( d=True )
			sNeckRoot = cmds.createNode('transform',n='sNeckRoot')
			cmds.xform(sNeckRoot,ws=True,m=(cmds.xform(BNeck ,q=True,ws=True,m=True)))
			sNeck0 = cmds.joint(name="sNeck0",p=NeckBGLoc, rad= 1)
			cmds.xform(sNeck0,ws=True,m=(cmds.xform(BNeck ,q=True,ws=True,m=True)))
			sNeck1 = cmds.joint(name="sNeck1",p=Neck1BGLoc, rad= 1)
			cmds.xform(sNeck1,ws=True,m=(cmds.xform(BNeck1 ,q=True,ws=True,m=True)))
			sNeckEnd = cmds.joint(name="sNeckEnd",p=HeadBGLoc, rad= 1)
			cmds.xform(sNeckEnd,ws=True,ro=(cmds.xform(sNeck1 ,q=True,ws=True,ro=True)))

			HiddenList += [sNeckRoot, sNeck0, sNeck1, sNeckEnd]

			locNeck = cmds.spaceLocator(n='locNeck')[0]
			locNeck1 = cmds.spaceLocator(n='locNeck1')[0]
			HiddenList += [locNeck, locNeck1]
			cmds.xform(locNeck,ws=True,t=NeckBGLoc)
			cmds.parent(locNeck1, locNeck)
			cmds.parent(locNeck, sNeckRoot)

			cmds.parent(sNeckRoot, locChest1)

			cmds.aimConstraint(neck1SpLocator, locNeck, aim=[1,0,0], u=[0,0,1], wut="none")
			cmds.aimConstraint(CtrlHead, locNeck1, aim=[1,0,0], u=[0,0,1], wut="none")
			cmds.pointConstraint(neck1SpLocator, locNeck1, mo=False)

			cmds.parentConstraint(locChest1 , ListNeckCurveCtrl[0], mo=True)
			cmds.parentConstraint(locChest1 , ListNeckCurveCtrl[1], mo=True)
			cmds.parentConstraint(CtrlHead , ListNeckCurveCtrl[2], mo=True)
			cmds.parentConstraint(CtrlHead , ListNeckCurveCtrl[3], mo=True)
			#--
			neckBaseHeadMtx = cmds.shadingNode('multMatrix', n='neckBaseHeadMtx', au=True)
			SNList.append(neckBaseHeadMtx)
			cmds.connectAttr(proxyHead+'.worldMatrix[0]', neckBaseHeadMtx+'.matrixIn[0]', f=True)
			cmds.connectAttr(locNeck1+'.worldInverseMatrix[0]', neckBaseHeadMtx+'.matrixIn[1]', f=True)

			decompNeckBaseHeadMtx = cmds.shadingNode('decomposeMatrix',n='decompNeckBaseHeadMtx',au=True)
			SNList.append(decompNeckBaseHeadMtx)
			cmds.connectAttr(neckBaseHeadMtx+'.matrixSum', decompNeckBaseHeadMtx+'.inputMatrix',f=True)

			dnbhm2Euler = cmds.shadingNode('quatToEuler',n='dnbhm2Euler',au=True)
			SNList.append(dnbhm2Euler)
			cmds.connectAttr(decompNeckBaseHeadMtx+'.outputQuatX', dnbhm2Euler+'.inputQuatX',f=True)
			cmds.connectAttr(decompNeckBaseHeadMtx+'.outputQuatW', dnbhm2Euler+'.inputQuatW',f=True)

			#neck
			sclNeckRoll = cmds.shadingNode('multiplyDivide',name='sclNeckRoll',au=True)
			SNList.append(sclNeckRoll)
			cmds.connectAttr(dnbhm2Euler+'.outputRotate', sclNeckRoll+'.input1',f=True)
			cmds.setAttr(sclNeckRoll+'.input2', 0.33,0.33,0.33,type='double3')


			rollNeckMtx = cmds.shadingNode('composeMatrix',name='rollNeckMtx',au=True)
			SNList.append(rollNeckMtx)
			cmds.connectAttr(sclNeckRoll+'.output', rollNeckMtx+'.inputRotate',f=True)

			mixNeckWsMtx = cmds.shadingNode('multMatrix',n='mixNeckWsMtx',au=True)
			SNList.append(mixNeckWsMtx)
			cmds.connectAttr(rollNeckMtx+'.outputMatrix', mixNeckWsMtx+'.matrixIn[0]',f=True)
			cmds.connectAttr(locNeck+'.worldMatrix[0]', mixNeckWsMtx+'.matrixIn[1]',f=True)

			neckLsMtx = cmds.shadingNode('multMatrix',n='neckLsMtx',au=True)
			SNList.append(neckLsMtx)
			cmds.connectAttr(mixNeckWsMtx+'.matrixSum', neckLsMtx+'.matrixIn[0]',f=True)
			cmds.connectAttr(sNeck0+'.parentInverseMatrix[0]', neckLsMtx+'.matrixIn[1]',f=True)

			neckWsTransInfo = cmds.shadingNode('decomposeMatrix',n='neckWsTransInfo',au=True)
			SNList.append(neckWsTransInfo)
			cmds.connectAttr(neckLsMtx+'.matrixSum', neckWsTransInfo+'.inputMatrix',f=True)
			cmds.connectAttr(neckWsTransInfo+'.outputTranslate', sNeck0+'.translate', f=True)
			cmds.connectAttr(neckWsTransInfo+'.outputRotate', sNeck0+'.rotate', f=True)

			#neck1
			sclNeck1Roll = cmds.shadingNode('multiplyDivide',name='sclNeck1Roll',au=True)
			SNList.append(sclNeck1Roll)
			cmds.connectAttr(dnbhm2Euler+'.outputRotate', sclNeck1Roll+'.input1',f=True)
			cmds.setAttr(sclNeck1Roll+'.input2', 0.67,0.67,0.67,type='double3')


			rollNeck1Mtx = cmds.shadingNode('composeMatrix',name='rollNeck1Mtx',au=True)
			SNList.append(rollNeck1Mtx)
			cmds.connectAttr(sclNeck1Roll+'.output', rollNeck1Mtx+'.inputRotate',f=True)

			mixNeck1WsMtx = cmds.shadingNode('multMatrix',n='mixNeck1WsMtx',au=True)
			SNList.append(mixNeck1WsMtx)
			cmds.connectAttr(rollNeck1Mtx+'.outputMatrix', mixNeck1WsMtx+'.matrixIn[0]',f=True)
			cmds.connectAttr(locNeck1+'.worldMatrix[0]', mixNeck1WsMtx+'.matrixIn[1]',f=True)

			neck1LsMtx = cmds.shadingNode('multMatrix',n='neck1LsMtx',au=True)
			SNList.append(neck1LsMtx)
			cmds.connectAttr(mixNeck1WsMtx+'.matrixSum', neck1LsMtx+'.matrixIn[0]',f=True)
			cmds.connectAttr(sNeck1+'.parentInverseMatrix[0]', neck1LsMtx+'.matrixIn[1]',f=True)

			neck1WsTransInfo = cmds.shadingNode('decomposeMatrix',n='neck1WsTransInfo',au=True)
			SNList.append(neck1WsTransInfo)
			cmds.connectAttr(neck1LsMtx+'.matrixSum', neck1WsTransInfo+'.inputMatrix',f=True)
			cmds.connectAttr(neck1WsTransInfo+'.outputTranslate', sNeck1+'.translate', f=True)
			cmds.connectAttr(neck1WsTransInfo+'.outputRotate', sNeck1+'.rotate', f=True)

			BoneConstraintList.append(cmds.parentConstraint(sNeck0, BNeck, mo=False)[0])
			BoneConstraintList.append(cmds.parentConstraint(sNeck1, BNeck1, mo=False)[0])
			#---------------------------
			cenBody = cmds.spaceLocator(name="cenBody")[0]
			MidItemList.append(cenBody)
			# cmds.parent(cenBody, CtrlRoot)
			HiddenList.append(cenBody)
			cmds.pointConstraint(proxyHip, sNeckRoot, cenBody, mo=False)
			CBOC = cmds.orientConstraint(CtrlHip, CtrlChest, CtrlHead, cenBody, mo=False)
			cmds.setAttr(CBOC[0] + ".interpType", 2)

			SideTransPart = cmds.group(em=True, name='pSideTransPart')
			cmds.parent(SideTransPart, CtrlRoot)
			cmds.setAttr(SideTransPart + ".inheritsTransform", False)
			SideConstrain = cmds.pointConstraint(cenBody, SideTransPart, skip=["y","z"])[0]

			ForwardTransPart = cmds.group(em=True, name='pForwardTransPart')
			cmds.xform(ForwardTransPart,ws=True,t=cmds.xform(SideTransPart,q=True,ws=True,t=True))
			cmds.parent(ForwardTransPart, SideTransPart)
			if not bIsZUp:
				ForwardConstrain = cmds.pointConstraint(cenBody, ForwardTransPart, skip=["x","y"])[0]
			else:
				ForwardConstrain = cmds.pointConstraint(cenBody, ForwardTransPart, skip=["x","z"])[0]
			
			lockTrans = cmds.group(em=True, name='pLockTransPart')
			cmds.parent(lockTrans, ForwardTransPart)
			RCConstrain = cmds.parentConstraint(CtrlRoot, lockTrans, mo=False)[0]

			RootLocUpV = 1
			if bIsZUp:
				RootLocUpV = 2
			CtrlRootLocator = self.createWireCircle("RootLocator", 20, RootLocUpV, 16, [0,0,0], [0.2,0,0], [0,0,0],True)
			ListNoScl.append(CtrlRootLocator)
			cmds.xform(CtrlRootLocator,ws=True,t=cmds.xform(lockTrans,q=True,ws=True,t=True))
			cmds.parent(CtrlRootLocator, lockTrans)
			
			proxyRoot = cmds.spaceLocator(name="pyRoot")[0]
			cmds.xform(proxyRoot,ws=True,m=cmds.xform(BRoot,q=True,ws=True,m=True))
			cmds.parent(proxyRoot, CtrlRootLocator)
			HiddenList.append(proxyRoot)

			BoneConstraintList.append(cmds.parentConstraint(proxyRoot, BRoot, mo=False)[0])

			cmds.addAttr(CtrlRoot, ln="SpineFlexible", k=True,w=True,at="float", dv=0.2, hxv=True, hnv=True, max=1, min=0)

			cmds.addAttr(CtrlRoot, ln="RootMotionSideCtrl", k=False,w=True,at="bool", dv=False)
			cmds.setAttr(CtrlRoot + ".RootMotionSideCtrl", cb=True)
			
			cmds.addAttr(CtrlRoot, ln="RootMotionForwardCtrl", k=False,w=True,at="bool", dv=True)
			cmds.setAttr(CtrlRoot + ".RootMotionForwardCtrl", cb=True)
			
			cmds.addAttr(CtrlRoot, ln="RArmFKIKBlend", k=True,w=True,at="float", dv=1, hxv=True, hnv=True, max=1, min=0)
			cmds.addAttr(CtrlRoot, ln="LArmFKIKBlend", k=True,w=True,at="float", dv=1, hxv=True, hnv=True, max=1, min=0)


			# oCurve
			cmds.connectAttr(CtrlRoot + ".SpineFlexible", oCurve + '.flexible', f=True)
			cmds.connectAttr(CtrlRoot + ".RootMotionSideCtrl", SideConstrain+"."+cenBody+"W0",f=True)
			cmds.connectAttr(CtrlRoot + ".RootMotionForwardCtrl", ForwardConstrain+"."+cenBody+"W0",f=True)

			oneMinus1 = cmds.shadingNode("plusMinusAverage",au=True)
			oneMinus2 = cmds.shadingNode("plusMinusAverage",au=True)
			multiNode1 = cmds.shadingNode("multiplyDivide",au=True)
			SNList.append(oneMinus1)
			SNList.append(oneMinus2)
			SNList.append(multiNode1)
			cmds.setAttr(oneMinus1+".operation", 2)
			cmds.setAttr(oneMinus2+".operation", 2)

			cmds.connectAttr(CtrlRoot + ".RootMotionSideCtrl", oneMinus1+".input1D[0]",f=True)
			cmds.connectAttr(CtrlRoot + ".RootMotionSideCtrl", oneMinus1+".input1D[1]",f=True)
			cmds.connectAttr(CtrlRoot + ".RootMotionForwardCtrl", oneMinus2+".input1D[0]",f=True)
			cmds.connectAttr(CtrlRoot + ".RootMotionForwardCtrl", oneMinus2+".input1D[1]",f=True)
			cmds.disconnectAttr(CtrlRoot + ".RootMotionSideCtrl", oneMinus1+".input1D[0]")
			cmds.disconnectAttr(CtrlRoot + ".RootMotionForwardCtrl", oneMinus2+".input1D[0]")
			cmds.setAttr(oneMinus1+".input1D[0]", 1)
			cmds.setAttr(oneMinus2+".input1D[0]", 1)
			cmds.connectAttr(oneMinus1 + ".output1D", multiNode1+".input1X",f=True)
			cmds.connectAttr(oneMinus2 + ".output1D", multiNode1+".input2X",f=True)
			cmds.connectAttr(multiNode1 + ".outputX", RCConstrain+"."+CtrlRoot+"W0",f=True)
			#----------Color Define----------
			Color_Ctrl1_R = [0.008,0.666,0.197]
			Color_Ctrl1_L = [0.012,0.058,0.984]
			Color_Ctrl2_R = [0.0003,0.074,0.004]
			Color_Ctrl2_L = [0.014,0.0399,0.142]
			Color_Ctrl3_R = [0,0.6,0]
			Color_Ctrl3_L = [0,0.0143,0.5054]
			Color_Ctrl4_R = [0.008,0.666,0.397]
			Color_Ctrl4_L = [0.012,0.258,0.984]

			HelperColor1 = [0.05,0.2,0.2]

			FingerCtrlSize = 1.6
			FingerCtrlSeg = 16
			FingerCtrlRColor = [0.177,0.3112,0.03]
			FingerCtrlLColor = [0.037,0.28,0.3889]
			#-------Shoulder-------------
			# for o in ShoulderList:
			for i in range(0, len(ShoulderList)):
				SN = ''
				if len(ShoulderList) > 1:
					SN = str(i)
				BShoulderR = 'B_Shoulder'+SN+'_R'
				BShoulderL = 'B_Shoulder'+SN+'_L'

				BShoulderR_parent = 'B_'+cmds.listRelatives(ShoulderList[i], p=True,pa=True)[0].split(':')[-1][4:]
				BShoulderL_parent = BShoulderR_parent

				cmds.select(BShoulderR_parent)
				shulderLocR = cmds.xform(ShoulderList[i],q=True,ws=True,t=True)
				endLocR = cmds.xform(cmds.listRelatives(ShoulderList[i], c=True,pa=True)[0],q=True,ws=True,t=True)
				BShoulderR = cmds.joint(name=BShoulderR,p=shulderLocR, rad= 3.5)
				BoneList.append(BShoulderR)
				cmds.xform(BShoulderR,ws=True,m=getTransMatrix(0, getVector(shulderLocR, endLocR), 1, Chest1Fw, shulderLocR))
				
				cmds.select(BShoulderL_parent)
				shulderLocL = multiVec(shulderLocR, [-1,1,1])
				endLocL = multiVec(endLocR, [-1,1,1])
				BShoulderL = cmds.joint(name=BShoulderL,p=shulderLocL, rad= 3.5)
				BoneList.append(BShoulderL)
				# cmds.xform(BShoulderL,ws=True,m=getTransMatrix(0, getVector(shulderLocL, endLocL), 2, Chest1Fw, shulderLocL))
				cmds.xform(BShoulderL,ws=True,m=self.getMatrixFliped(cmds.xform(BShoulderR, q=True, ws=True, m=True), 3))


				refSize = getDistance(shulderLocR, endLocR)

				# (self, name, width, length, offset=[0,0,0], color=[0,1,0], alignPlane = 'yz', pos=[0,0,0]):
				# CtrlShoulderR = self.createWireRect('Shoulder'+SN+'_R', refSize * 1.2, refSize*1.5, [refSize*0.6,-refSize*0.5,0], [0,0.4,0.017], False)
				CtrlShoulderR = self.createWireRect2('Shoulder'+SN+'_R', refSize * 1.2, refSize*1.5, [refSize*0.5,0,refSize*0.6], [0,0.4,0.017], 'xy')
				CtrlList.append(CtrlShoulderR)
				ListOnlyRot.append(CtrlShoulderR)
				
				# cmds.xform(CtrlShoulderR,ws=True,m=getTransMatrix(0, getVector(shulderLocR, endLocR), 2, Chest1Fw, shulderLocR))
				cmds.xform(CtrlShoulderR,ws=True,m=cmds.xform(BShoulderR, q=True, ws=True, m=True))
				cmds.parent(CtrlShoulderR, BShoulderR_parent[2:])
				self.createTransFixRoot(CtrlShoulderR)

				proxyShoulderR = cmds.spaceLocator(name='pyShoulder'+SN+'_R')[0]
				cmds.xform(proxyShoulderR ,ws=True,m=cmds.xform(BShoulderR,q=True,ws=True,m=True))
				cmds.parent(proxyShoulderR, CtrlShoulderR)
				HiddenList.append(proxyShoulderR)

				# CtrlShoulderL = self.createWireRect('Shoulder'+SN+'_L', refSize * 1.2, refSize*1.5, [refSize*0.6,refSize*0.5,0], [0,0.007,0.619],False)
				# CtrlShoulderL = self.createWireRect('Shoulder'+SN+'_L', refSize * 1.2, refSize*1.5, [-refSize*0.6,refSize*0.5,0], [0,0.007,0.619],False)
				CtrlShoulderL = self.createWireRect2('Shoulder'+SN+'_L', refSize * 1.2, refSize*1.5, [-refSize*0.5,0,-refSize*0.6], [0,0.007,0.619], 'xy')
				CtrlList.append(CtrlShoulderL)
				ListOnlyRot.append(CtrlShoulderL)
				
				# cmds.xform(CtrlShoulderL,ws=True,m=getTransMatrix(0, getVector(shulderLocL, endLocL), 2, Chest1Fw, shulderLocL))
				cmds.xform(CtrlShoulderL,ws=True,m=cmds.xform(BShoulderL, q=True, ws=True, m=True))
				cmds.parent(CtrlShoulderL, BShoulderL_parent[2:])
				self.createTransFixRoot(CtrlShoulderL)

				proxyShoulderL = cmds.spaceLocator(name='pyShoulder'+SN+'_L')[0]
				cmds.xform(proxyShoulderL ,ws=True,m=cmds.xform(BShoulderL,q=True,ws=True,m=True))
				cmds.parent(proxyShoulderL, CtrlShoulderL)
				HiddenList.append(proxyShoulderL)
				
				BoneConstraintList.append(cmds.parentConstraint(proxyShoulderR, BShoulderR, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyShoulderL, BShoulderL, mo=False)[0])

			for i in range(0, len(UpArmList)):
				SN = ''
				if len(UpArmList) > 1:
					SN = str(i)
				CheckDone = False
				UpArmR_parent = cmds.listRelatives(UpArmList[i], p=True,pa=True)[0]
				UpArmL_parent = ''
				for p in range(0, len(ShoulderList)):
					pSN = ''
					if len(ShoulderList) > 1:
						pSN = str(p)
					if ShoulderList[p] == UpArmR_parent:
						CheckDone = True
						UpArmR_parent = 'B_Shoulder'+pSN+'_R'
						UpArmL_parent = 'B_Shoulder'+pSN+'_L'
				if not CheckDone:
					UpArmR_parent = 'B_'+UpArmR_parent.split(':')[-1][4:]
					UpArmL_parent = UpArmR_parent

				if cmds.objExists(UpArmR_parent):
					CtrlUpArmR_parent = UpArmR_parent[2:]
					CtrlUpArmL_parent = UpArmL_parent[2:]

					bgUpArmR = UpArmList[i]
					bgForeArmR = cmds.listRelatives(bgUpArmR, c=True,pa=True)[0]
					bgHandR = cmds.listRelatives(bgForeArmR, c=True,pa=True)[0]
					bgFingerRootList = cmds.listRelatives(bgHandR, c=True,pa=True)


					UpArmLocR = cmds.xform(bgUpArmR,q=True,ws=True,t=True)
					ForeArmLocR = cmds.xform(bgForeArmR,q=True,ws=True,t=True)
					HandLocR = cmds.xform(bgHandR,q=True,ws=True,t=True)
					CenFingerLocR = cmds.xform(bgFingerRootList[2],q=True,ws=True,t=True)
					PointFingerLocR = cmds.xform(bgFingerRootList[1],q=True,ws=True,t=True)
					LastFingerLocR = cmds.xform(bgFingerRootList[-1],q=True,ws=True,t=True)

					uArmLength = getDistance(UpArmLocR, ForeArmLocR)
					fArmLength = getDistance(ForeArmLocR, HandLocR)
					armLength = uArmLength + fArmLength
					refSizeHand = getDistance(HandLocR, CenFingerLocR)

					RArmBN = crossVec(getVector(UpArmLocR, ForeArmLocR), getVector(ForeArmLocR, HandLocR))
					RArmUpV = crossVec(RArmBN, getVector(UpArmLocR,HandLocR))
					RHandBN = crossVec(getVector(HandLocR,CenFingerLocR),getVector(LastFingerLocR,PointFingerLocR))
					RHandUpV = crossVec(RHandBN,getVector(HandLocR,CenFingerLocR))
					RArmUpVPos = [
									0.5*(UpArmLocR[0]+HandLocR[0]) - RArmUpV[0]*armLength*0.8,
									0.5*(UpArmLocR[1]+HandLocR[1]) - RArmUpV[1]*armLength*0.8,
									0.5*(UpArmLocR[2]+HandLocR[2]) - RArmUpV[2]*armLength*0.8
								 ]

					UpArmLocL = multiVec(UpArmLocR, [-1,1,1])
					ForeArmLocL = multiVec(ForeArmLocR, [-1,1,1])
					HandLocL = multiVec(HandLocR, [-1,1,1])
					CenFingerLocL = multiVec(CenFingerLocR, [-1,1,1])
					PointFingerLocL = multiVec(PointFingerLocR, [-1,1,1])
					LastFingerLocL = multiVec(LastFingerLocR, [-1,1,1])

					LArmBN = multiVec(RArmBN, [-1,1,1])
					LArmUpV = multiVec(RArmUpV, [-1,1,1])
					LHandBN = multiVec(RHandBN, [-1,1,1])
					LHandUpV = multiVec(RHandUpV, [-1,1,1])
					LArmUpVPos = multiVec(RArmUpVPos, [-1,1,1])

					cmds.select(UpArmR_parent)
					BArmUpperR = cmds.joint(name='B_ArmUpper'+SN+'_R',p=UpArmLocR, rad= 3.5)
					BoneList.append(BArmUpperR)
					cmds.xform(BArmUpperR,ws=True,m=getTransMatrix(0, getVector(UpArmLocR, ForeArmLocR), 1, RArmUpV, UpArmLocR))
					BArmForeR = cmds.joint(name='B_ArmFore'+SN+'_R',p=ForeArmLocR, rad= 3.5)
					BoneList.append(BArmForeR)
					cmds.xform(BArmForeR,ws=True,m=getTransMatrix(0, getVector(ForeArmLocR, HandLocR), 1, RArmUpV, ForeArmLocR))
					BHandR = cmds.joint(name='B_Hand'+SN+'_R',p=HandLocR, rad= 3.5)
					BoneList.append(BHandR)
					cmds.xform(BHandR,ws=True,m=getTransMatrix(0, getVector(HandLocR, CenFingerLocR), 1, RHandUpV, HandLocR))

					cmds.select(UpArmL_parent)
					BArmUpperL = cmds.joint(name='B_ArmUpper'+SN+'_L',p=UpArmLocL, rad= 3.5)
					BoneList.append(BArmUpperL)
					# cmds.xform(BArmUpperL,ws=True,m=getTransMatrix(0, getVector(UpArmLocL, ForeArmLocL), 2, LArmUpV, UpArmLocL))
					cmds.xform(BArmUpperL,ws=True,m=self.getMatrixFliped(cmds.xform(BArmUpperR,q=True,ws=True,m=True), 3))
					BArmForeL = cmds.joint(name='B_ArmFore'+SN+'_L',p=ForeArmLocL, rad= 3.5)
					BoneList.append(BArmForeL)
					# cmds.xform(BArmForeL,ws=True,m=getTransMatrix(0, getVector(ForeArmLocL, HandLocL), 2, LArmUpV, ForeArmLocL))
					cmds.xform(BArmForeL,ws=True,m=self.getMatrixFliped(cmds.xform(BArmForeR,q=True,ws=True,m=True), 3))
					BHandL = cmds.joint(name='B_Hand'+SN+'_L',p=HandLocL, rad= 3.5)
					BoneList.append(BHandL)
					# cmds.xform(BHandL,ws=True,m=getTransMatrix(0, getVector(HandLocL, CenFingerLocL), 2, LHandUpV, HandLocL))
					cmds.xform(BHandL,ws=True,m=self.getMatrixFliped(cmds.xform(BHandR,q=True,ws=True,m=True), 3))

					
					#----
					cmds.select(UpArmR_parent)
					BArmUpperBuffR = cmds.joint(name='B_ArmUpper'+SN+'Buff_R',p=[0,0,0], rad= 4)
					BoneList.append(BArmUpperBuffR)
					cmds.select(BArmUpperR)
					BArmUpperTwist1R = cmds.joint(name='B_ArmUpper'+SN+'Tw1_R',p=[0,0,0], rad= 3)
					BoneList.append(BArmUpperTwist1R)
					cmds.select(BArmUpperR)
					BArmUpperTwist2R = cmds.joint(name='B_ArmUpper'+SN+'Tw2_R',p=[0,0,0], rad= 3)
					BoneList.append(BArmUpperTwist2R)
					cmds.select(BArmForeR)
					BElbowBuffR = cmds.joint(name='B_Elbow'+SN+'Buff_R',p=[0,0,0], rad= 3)
					BoneList.append(BElbowBuffR)
					cmds.select(BArmForeR)
					BArmForeTwist1R = cmds.joint(name='B_ArmFore'+SN+'Tw1_R',p=[0,0,0], rad= 3)
					BoneList.append(BArmForeTwist1R)
					cmds.select(BArmForeR)
					BArmForeTwist2R = cmds.joint(name='B_ArmFore'+SN+'Tw2_R',p=[0,0,0], rad= 3)
					BoneList.append(BArmForeTwist2R)

					cmds.select(UpArmL_parent)
					BArmUpperBuffL = cmds.joint(name='B_ArmUpper'+SN+'Buff_L',p=[0,0,0], rad= 4)
					BoneList.append(BArmUpperBuffL)
					cmds.select(BArmUpperL)
					BArmUpperTwist1L = cmds.joint(name='B_ArmUpper'+SN+'Tw1_L',p=[0,0,0], rad= 3)
					BoneList.append(BArmUpperTwist1L)
					cmds.select(BArmUpperL)
					BArmUpperTwist2L = cmds.joint(name='B_ArmUpper'+SN+'Tw2_L',p=[0,0,0], rad= 3)
					BoneList.append(BArmUpperTwist2L)
					cmds.select(BArmForeL)
					BElbowBuffL = cmds.joint(name='B_Elbow'+SN+'Buff_L',p=[0,0,0], rad= 3)
					BoneList.append(BElbowBuffL)
					cmds.select(BArmForeL)
					BArmForeTwist1L = cmds.joint(name='B_ArmFore'+SN+'Tw1_L',p=[0,0,0], rad= 3)
					BoneList.append(BArmForeTwist1L)
					cmds.select(BArmForeL)
					BArmForeTwist2L = cmds.joint(name='B_ArmFore'+SN+'Tw2_L',p=[0,0,0], rad= 3)
					BoneList.append(BArmForeTwist2L)
					
					#----
					cmds.select( d=True )
					proxyUpperArmJntR = cmds.joint(name='pyUpArmJnt'+SN+'_R',p=UpArmLocR, rad= 6)
					# cmds.xform(proxyUpperArmJntR,ws=True,m=getTransMatrix(0, getVector(UpArmLocR, ForeArmLocR), 2, RArmUpV, UpArmLocR))
					cmds.xform(proxyUpperArmJntR,ws=True,m=cmds.xform(BArmUpperR,q=True,ws=True,m=True))
					HiddenList.append(proxyUpperArmJntR)
					proxyForeArmJntR = cmds.joint(name='pyForeArmJnt'+SN+'_R',p=ForeArmLocR, rad= 6)
					# cmds.xform(proxyForeArmJntR,ws=True,m=getTransMatrix(0, getVector(ForeArmLocR, HandLocR), 2, RArmUpV, ForeArmLocR))
					cmds.xform(proxyForeArmJntR,ws=True,m=cmds.xform(BArmForeR,q=True,ws=True,m=True))
					HiddenList.append(proxyForeArmJntR)
					proxyEndArmJntR = cmds.joint(name='pyEndArmJnt'+SN+'_R',p=HandLocR, rad= 2)
					# cmds.xform(proxyEndArmJntR,ws=True,m=getTransMatrix(0, getVector(HandLocR, CenFingerLocR), 2, RHandUpV, HandLocR))
					cmds.xform(proxyEndArmJntR,ws=True,m=cmds.xform(BHandR,q=True,ws=True,m=True))
					HiddenList.append(proxyEndArmJntR)

					cmds.makeIdentity([proxyUpperArmJntR,proxyForeArmJntR,proxyEndArmJntR],apply=True, t=True, r=True,s=True,n=2,pn=True)
					
					ArmIKHandleR = cmds.ikHandle(name='pyArmIKHandle'+SN+'R',sj=proxyUpperArmJntR, ee=proxyEndArmJntR, sol='ikRPsolver')
					HiddenList.append(ArmIKHandleR[0])

					proxyArmUpvR = cmds.spaceLocator(name='pyArmUpv'+SN+'_R')[0]
					cmds.xform(proxyArmUpvR ,ws=True, t=RArmUpVPos)
					MidItemList.append(proxyArmUpvR)
					# cmds.parent(proxyArmUpvR, CtrlRoot)
					cmds.poleVectorConstraint(proxyArmUpvR, ArmIKHandleR[0], w=1)
					HiddenList.append(proxyArmUpvR)

					refForeArmR = cmds.spaceLocator(name='rfForeArm'+SN+'_R')[0]
					cmds.xform(refForeArmR, ws=True, m=cmds.xform(BArmForeR,q=True,ws=True,m=True))
					cmds.parent(refForeArmR, proxyForeArmJntR)
					HiddenList.append(refForeArmR)

					refHandR = cmds.spaceLocator(name='rfHand'+SN+'_R')[0]
					cmds.xform(refHandR, ws=True, m=cmds.xform(BHandR,q=True,ws=True,m=True))
					cmds.parent(refHandR, proxyEndArmJntR)
					HiddenList.append(refHandR)

					cmds.parent(proxyUpperArmJntR, CtrlUpArmR_parent)
					# cmds.parent(ArmIKHandleR[0], CtrlRoot)
					cmds.setAttr((ArmIKHandleR[0] + ".template"), 1)
					MidItemList.append(ArmIKHandleR[0])

					proxyArmIKR = self.createWireSphere('pyArmIK'+SN+'_R', 2.5, [0,0.2,0.4])
					# cmds.parent(proxyArmIKR, CtrlRoot)
					MidItemList.append(proxyArmIKR)
					cmds.xform(proxyArmIKR ,ws=True,m=cmds.xform(proxyEndArmJntR,q=True,ws=True,m=True))
					cmds.parentConstraint(proxyArmIKR, ArmIKHandleR[0], mo=True)
					HiddenList.append(proxyArmIKR)

					proxyUArmLocR = cmds.spaceLocator(name='pyUArmLoc'+SN+'_R')[0]
					cmds.parent(proxyUArmLocR, CtrlUpArmR_parent)
					HiddenList.append(proxyUArmLocR)
					xVec = getVector(UpArmLocR, cmds.xform(UpArmR_parent,q=True,ws=True,t=True))
					uArmJntPos = sumVec(UpArmLocR, scaleVec(xVec, uArmLength * 0.005))
					locUArmR = cmds.spaceLocator(name='locUArm'+SN+'_R')[0]
					HiddenList.append(locUArmR)
					cmds.xform(locUArmR ,ws=True,m=getTransMatrix(0, xVec, 1, RArmUpV, UpArmLocR))
					cmds.parent(locUArmR, proxyUpperArmJntR)
					cmds.xform(proxyUArmLocR ,ws=True,m=getTransMatrix(0, xVec, 1, RArmUpV, UpArmLocR))
					cmds.pointConstraint(locUArmR, proxyUArmLocR)
					cmds.aimConstraint(proxyForeArmJntR, proxyUArmLocR, aim=[1,0,0], u=[0,1,0], wut="none")

					refUArmR = cmds.spaceLocator(name='refUArm'+SN+'_R')[0]
					cmds.xform(refUArmR ,ws=True,m=cmds.xform(BArmUpperR,q=True,ws=True,m=True))
					cmds.parent(refUArmR, proxyUpperArmJntR)
					HiddenList.append(refUArmR)

					buffUArmR = self.createWireSphere('buffUArm'+SN+'_R', 3.5355, [0.05,0.4,0.4], uArmJntPos)
					cmds.parent(buffUArmR, CtrlUpArmR_parent)
					HiddenList.append(buffUArmR)
					RC_BUAR = cmds.orientConstraint(CtrlUpArmR_parent, proxyUArmLocR, buffUArmR)
					cmds.setAttr(RC_BUAR[0] + ".interpType", 2)

					proxyUArmTwis1LocR = self.createWireBox('pyUArmTwis1Loc'+SN+'_R', 4,4,4,[0,0,0],[0.05,0.2,0.2])
					cmds.parent(proxyUArmTwis1LocR, proxyUpperArmJntR)
					HiddenList.append(proxyUArmTwis1LocR)
					PC_UAT1_R = cmds.pointConstraint(proxyUArmLocR, refForeArmR, proxyUArmTwis1LocR)
					cmds.setAttr(PC_UAT1_R[0] + "." + proxyUArmLocR + "W0", 2)
					cmds.setAttr(PC_UAT1_R[0] + "." + refForeArmR + "W1", 1)
					RC_UAT1_R = cmds.orientConstraint(proxyUArmLocR, refUArmR, proxyUArmTwis1LocR, mo=False)
					cmds.setAttr(RC_UAT1_R[0] + ".interpType", 2)

					proxyUArmTwis2LocR = self.createWireBox('pyUArmTwis2Loc'+SN+'_R', 4,4,4,[0,0,0],[0.05,0.2,0.2])
					cmds.parent(proxyUArmTwis2LocR, proxyUpperArmJntR)
					HiddenList.append(proxyUArmTwis2LocR)
					PC_UAT2_R = cmds.pointConstraint(proxyUArmLocR, refForeArmR, proxyUArmTwis2LocR)
					cmds.setAttr(PC_UAT2_R[0] + "." + proxyUArmLocR + "W0", 1)
					cmds.setAttr(PC_UAT2_R[0] + "." + refForeArmR + "W1", 2)

					RC_UAT2_R = cmds.orientConstraint(proxyUArmLocR, refUArmR, proxyUArmTwis2LocR, mo=False)
					cmds.setAttr(RC_UAT2_R[0] + "." + proxyUArmLocR + "W0", 1)
					cmds.setAttr(RC_UAT2_R[0] + "." + refUArmR + "W1", 3)
					cmds.setAttr(RC_UAT2_R[0] + ".interpType", 2)

					refHandRollDummyR = cmds.spaceLocator(name='refHandRoll'+SN+'_R')[0]
					cmds.xform(refHandRollDummyR ,ws=True,m=cmds.xform(refHandR,q=True,ws=True,m=True))
					cmds.parent(refHandRollDummyR, refForeArmR)
					HiddenList.append(refHandRollDummyR)
					cmds.aimConstraint(refForeArmR, refHandRollDummyR, aim=[-1,0,0], u=[0,0,1], wut="objectrotation", wuo=refHandR, wu=[0,0,1])

					proxyFArmTwis1LocR = self.createWireBox('pyFArmTwis1Loc'+SN+'_R', 4,4,4,[0,0,0],[0.05,0.2,0.2])
					cmds.parent(proxyFArmTwis1LocR, refForeArmR)
					HiddenList.append(proxyFArmTwis1LocR)
					PC_FAT1_R = cmds.pointConstraint(refForeArmR, refHandR, proxyFArmTwis1LocR)
					cmds.setAttr(PC_FAT1_R[0] + "." + refForeArmR + "W0", 2)
					cmds.setAttr(PC_FAT1_R[0] + "." + refHandR + "W1", 1)
					RC_FAT1_R = cmds.orientConstraint(refForeArmR, refHandRollDummyR, proxyFArmTwis1LocR, mo=False)
					cmds.setAttr(RC_FAT1_R[0] + "." + refForeArmR + "W0", 2)
					cmds.setAttr(RC_FAT1_R[0] + "." + refHandRollDummyR + "W1", 1)
					cmds.setAttr(RC_FAT1_R[0] + ".interpType", 2)

					proxyFArmTwis2LocR = self.createWireBox('pyFArmTwis2Loc'+SN+'_R', 4,4,4,[0,0,0],[0.05,0.2,0.2])
					cmds.parent(proxyFArmTwis2LocR, refForeArmR)
					HiddenList.append(proxyFArmTwis2LocR)
					PC_FAT2_R = cmds.pointConstraint(refForeArmR, refHandR, proxyFArmTwis2LocR)
					cmds.setAttr(PC_FAT2_R[0] + "." + refForeArmR + "W0", 1)
					cmds.setAttr(PC_FAT2_R[0] + "." + refHandR + "W1", 2)
					RC_FAT2_R = cmds.orientConstraint(refForeArmR, refHandRollDummyR, proxyFArmTwis2LocR, mo=False)
					cmds.setAttr(RC_FAT2_R[0] + "." + refForeArmR + "W0", 1)
					cmds.setAttr(RC_FAT2_R[0] + "." + refHandRollDummyR + "W1", 2)
					cmds.setAttr(RC_FAT2_R[0] + ".interpType", 2)

					lockPointFKArmR = cmds.spaceLocator(name='lpFKArm'+SN+'_R')[0]
					cmds.xform(lockPointFKArmR, ws=True, t=UpArmLocR)
					cmds.parent(lockPointFKArmR, CtrlUpArmR_parent)
					HiddenList.append(lockPointFKArmR)

					gpFKArmR = cmds.group(em=True, name='gpFKArm'+SN+'_R')
					xV = [0,-1,0]
					yV = [0,0,1]
					if bIsZUp:
						xV = [0,0,-1]
						yV = [0,-1,0]
					# cmds.xform(gpFKArmR, ws=True, t=UpArmLocR)
					cmds.xform(gpFKArmR, ws=True, m=getTransMatrix(0, xV, 1, yV, UpArmLocR))
					cmds.parent(gpFKArmR, CtrlRoot)
					cmds.pointConstraint(lockPointFKArmR, gpFKArmR)

					ctrlUpperArmFK_R = self.createWireBox('FKUpperArm'+SN+'_R', uArmLength,12,12, [uArmLength*0.5,0,0],Color_Ctrl2_R)
					CtrlList.append(ctrlUpperArmFK_R)
					ListOnlyRot.append(ctrlUpperArmFK_R)
					# if bIsZUp:
					# 	cmds.setAttr(ctrlUpperArmFK_R+".rotateOrder", 3)
					cmds.xform(ctrlUpperArmFK_R, ws=True, m=cmds.xform(BArmUpperR,q=True,ws=True,m=True))
					cmds.parent(ctrlUpperArmFK_R, gpFKArmR)

					ctrlForeArmFK_R = self.createWireBox('FKForeArm'+SN+'_R', fArmLength,12,12, [fArmLength*0.5,0,0],Color_Ctrl2_R)
					CtrlList.append(ctrlForeArmFK_R)
					ListOnlyRot.append(ctrlForeArmFK_R)
					# if bIsZUp:
					# 	cmds.setAttr(ctrlForeArmFK_R+".rotateOrder", 3)
					cmds.xform(ctrlForeArmFK_R, ws=True, m=cmds.xform(BArmForeR,q=True,ws=True,m=True))
					cmds.parent(ctrlForeArmFK_R, ctrlUpperArmFK_R)
					cmds.setAttr(ctrlForeArmFK_R+".rotateOrder", 3)

					FKHandSizeR = [refSizeHand,refSizeHand,refSizeHand*0.75]
					# if bIsZUp:
					# 	FKHandSizeR = [refSizeHand,refSizeHand*0.75,refSizeHand]
					ctrlHandFK_R = self.createWireBox('FKHand'+SN+'_R', FKHandSizeR[0],FKHandSizeR[1],FKHandSizeR[2], [refSizeHand*0.5,0,0],Color_Ctrl2_R)
					CtrlList.append(ctrlHandFK_R)
					ListOnlyRot.append(ctrlHandFK_R)
					cmds.xform(ctrlHandFK_R, ws=True, m=cmds.xform(BHandR,q=True,ws=True,m=True))
					cmds.parent(ctrlHandFK_R, ctrlForeArmFK_R)

					endArmFKR = cmds.spaceLocator(name='endFKArm'+SN+'_R')[0]
					cmds.xform(endArmFKR, ws=True, t=HandLocR)
					cmds.parent(endArmFKR, ctrlForeArmFK_R)
					HiddenList.append(endArmFKR)
					cmds.setAttr(endArmFKR+".translateZ", 0.01)

					refFKArmCentR = cmds.spaceLocator(name='rfFKArmCent'+SN+'_R')[0]
					cmds.pointConstraint(ctrlUpperArmFK_R, endArmFKR, refFKArmCentR)
					cmds.aimConstraint(endArmFKR, refFKArmCentR, aim=[1,0,0], u=[0,1,0], wut="object", wuo=ctrlForeArmFK_R)
					# cmds.parent(refFKArmCentR, CtrlRoot)
					MidItemList.append(refFKArmCentR)
					HiddenList.append(refFKArmCentR)
					proxyFKArmUppR = cmds.spaceLocator(name='pyFKArmUpp'+SN+'_R')[0]
					cmds.xform(proxyFKArmUppR, ws=True, t=RArmUpVPos)
					cmds.parent(proxyFKArmUppR, refFKArmCentR)
					HiddenList.append(proxyFKArmUppR)

					#----
					cmds.select( d=True )
					proxyUpperArmJntL = cmds.joint(name='pyUpArmJnt'+SN+'_L',p=UpArmLocL, rad= 6)
					# cmds.xform(proxyUpperArmJntL,ws=True,m=getTransMatrix(0, getVector(UpArmLocL, ForeArmLocL), 2, LArmUpV, UpArmLocL))
					cmds.xform(proxyUpperArmJntL,ws=True,m=cmds.xform(BArmUpperL,q=True,ws=True,m=True))
					HiddenList.append(proxyUpperArmJntL)
					proxyForeArmJntL = cmds.joint(name='pyForeArmJnt'+SN+'_L',p=ForeArmLocL, rad= 6)
					# cmds.xform(proxyForeArmJntL,ws=True,m=getTransMatrix(0, getVector(ForeArmLocL, HandLocL), 2, LArmUpV, ForeArmLocL))
					cmds.xform(proxyForeArmJntL,ws=True,m=cmds.xform(BArmForeL,q=True,ws=True,m=True))
					HiddenList.append(proxyForeArmJntL)
					proxyEndArmJntL = cmds.joint(name='pyEndArmJnt'+SN+'_L',p=HandLocL, rad= 2)
					# cmds.xform(proxyEndArmJntL,ws=True,m=getTransMatrix(0, getVector(HandLocL, CenFingerLocL), 2, LHandUpV, HandLocL))
					cmds.xform(proxyEndArmJntL,ws=True,m=cmds.xform(BHandL,q=True,ws=True,m=True))
					HiddenList.append(proxyEndArmJntL)

					cmds.makeIdentity([proxyUpperArmJntL,proxyForeArmJntL,proxyEndArmJntL],apply=True, t=True, r=True,s=True,n=2,pn=True)
					
					ArmIKHandleL = cmds.ikHandle(name='pyArmIKHandle'+SN+'L',sj=proxyUpperArmJntL, ee=proxyEndArmJntL, sol='ikRPsolver')
					HiddenList.append(ArmIKHandleL[0])

					proxyArmUpvL = cmds.spaceLocator(name='pyArmUpv'+SN+'_L')[0]
					cmds.xform(proxyArmUpvL ,ws=True, t=LArmUpVPos)
					MidItemList.append(proxyArmUpvL)
					# cmds.parent(proxyArmUpvL, CtrlRoot)
					HiddenList.append(proxyArmUpvL)
					cmds.poleVectorConstraint(proxyArmUpvL, ArmIKHandleL[0], w=1)

					refForeArmL = cmds.spaceLocator(name='rfForeArm'+SN+'_L')[0]
					cmds.xform(refForeArmL, ws=True, m=cmds.xform(BArmForeL,q=True,ws=True,m=True))
					cmds.parent(refForeArmL, proxyForeArmJntL)
					HiddenList.append(refForeArmL)

					refHandL = cmds.spaceLocator(name='rfHand'+SN+'_L')[0]
					cmds.xform(refHandL, ws=True, m=cmds.xform(BHandL,q=True,ws=True,m=True))
					cmds.parent(refHandL, proxyEndArmJntL)
					HiddenList.append(refHandL)

					cmds.parent(proxyUpperArmJntL, CtrlUpArmL_parent)
					# cmds.parent(ArmIKHandleL[0], CtrlRoot)
					cmds.setAttr((ArmIKHandleL[0] + ".template"), 1)
					MidItemList.append(ArmIKHandleL[0])

					proxyArmIKL = self.createWireSphere('pyArmIK'+SN+'_L', 2.5, [0,0.2,0.4])
					# cmds.parent(proxyArmIKL, CtrlRoot)
					MidItemList.append(proxyArmIKL)
					HiddenList.append(proxyArmIKL)
					cmds.xform(proxyArmIKL ,ws=True,m=cmds.xform(proxyEndArmJntL,q=True,ws=True,m=True))
					cmds.parentConstraint(proxyArmIKL, ArmIKHandleL[0], mo=True)

					proxyUArmLocL = cmds.spaceLocator(name='pyUArmLoc'+SN+'_L')[0]
					cmds.parent(proxyUArmLocL, CtrlUpArmL_parent)
					HiddenList.append(proxyUArmLocL)
					xVec = getVector(UpArmLocL, cmds.xform(UpArmL_parent,q=True,ws=True,t=True))
					uArmJntPos = sumVec(UpArmLocL, scaleVec(xVec, uArmLength * 0.005))
					locUArmL = cmds.spaceLocator(name='locUArm'+SN+'_L')[0]
					HiddenList.append(locUArmL)
					cmds.xform(locUArmL ,ws=True,m=getTransMatrix(0, xVec, 1, LArmUpV, UpArmLocL))
					cmds.parent(locUArmL, proxyUpperArmJntL)
					cmds.xform(proxyUArmLocL ,ws=True,m=getTransMatrix(0, xVec, 1, LArmUpV, UpArmLocL))
					cmds.pointConstraint(locUArmL, proxyUArmLocL)
					cmds.aimConstraint(proxyForeArmJntL, proxyUArmLocL, aim=[-1,0,0], u=[0,1,0], wut="none")

					refUArmL = cmds.spaceLocator(name='refUArm'+SN+'_L')[0]
					cmds.xform(refUArmL ,ws=True,m=cmds.xform(BArmUpperL,q=True,ws=True,m=True))
					cmds.parent(refUArmL, proxyUpperArmJntL)
					HiddenList.append(refUArmL)

					buffUArmL = self.createWireSphere('buffUArm'+SN+'_L', 3.5355, [0.05,0.4,0.4], uArmJntPos)
					cmds.parent(buffUArmL, CtrlUpArmL_parent)
					HiddenList.append(buffUArmL)
					RC_BUAL = cmds.orientConstraint(CtrlUpArmL_parent, proxyUArmLocL, buffUArmL)
					cmds.setAttr(RC_BUAL[0] + ".interpType", 2)

					proxyUArmTwis1LocL = self.createWireBox('pyUArmTwis1Loc'+SN+'_L', 4,4,4,[0,0,0],[0.05,0.2,0.2])
					cmds.parent(proxyUArmTwis1LocL, proxyUpperArmJntL)
					HiddenList.append(proxyUArmTwis1LocL)
					PC_UAT1_L = cmds.pointConstraint(proxyUArmLocL, refForeArmL, proxyUArmTwis1LocL)
					cmds.setAttr(PC_UAT1_L[0] + "." + proxyUArmLocL + "W0", 2)
					cmds.setAttr(PC_UAT1_L[0] + "." + refForeArmL + "W1", 1)
					RC_UAT1_L = cmds.orientConstraint(proxyUArmLocL, refUArmL, proxyUArmTwis1LocL, mo=False)
					cmds.setAttr(RC_UAT1_L[0] + ".interpType", 2)

					proxyUArmTwis2LocL = self.createWireBox('pyUArmTwis2Loc'+SN+'_L', 4,4,4,[0,0,0],[0.05,0.2,0.2])
					cmds.parent(proxyUArmTwis2LocL, proxyUpperArmJntL)
					HiddenList.append(proxyUArmTwis2LocL)
					PC_UAT2_L = cmds.pointConstraint(proxyUArmLocL, refForeArmL, proxyUArmTwis2LocL)
					cmds.setAttr(PC_UAT2_L[0] + "." + proxyUArmLocL + "W0", 1)
					cmds.setAttr(PC_UAT2_L[0] + "." + refForeArmL + "W1", 2)

					RC_UAT2_L = cmds.orientConstraint(proxyUArmLocL, refUArmL, proxyUArmTwis2LocL, mo=False)
					cmds.setAttr(RC_UAT2_L[0] + "." + proxyUArmLocL + "W0", 1)
					cmds.setAttr(RC_UAT2_L[0] + "." + refUArmL + "W1", 3)
					cmds.setAttr(RC_UAT2_L[0] + ".interpType", 2)

					refHandRollDummyL = cmds.spaceLocator(name='refHandRoll'+SN+'_L')[0]
					cmds.xform(refHandRollDummyL ,ws=True,m=cmds.xform(refHandL,q=True,ws=True,m=True))
					cmds.parent(refHandRollDummyL, refForeArmL)
					HiddenList.append(refHandRollDummyL)
					cmds.aimConstraint(refForeArmL, refHandRollDummyL, aim=[-1,0,0], u=[0,0,1], wut="objectrotation", wuo=refHandL, wu=[0,0,1])

					proxyFArmTwis1LocL = self.createWireBox('pyFArmTwis1Loc'+SN+'_L', 4,4,4,[0,0,0],[0.05,0.2,0.2])
					cmds.parent(proxyFArmTwis1LocL, refForeArmL)
					HiddenList.append(proxyFArmTwis1LocL)
					PC_FAT1_L = cmds.pointConstraint(refForeArmL, refHandL, proxyFArmTwis1LocL)
					cmds.setAttr(PC_FAT1_L[0] + "." + refForeArmL + "W0", 2)
					cmds.setAttr(PC_FAT1_L[0] + "." + refHandL + "W1", 1)
					RC_FAT1_L = cmds.orientConstraint(refForeArmL, refHandRollDummyL, proxyFArmTwis1LocL, mo=False)
					cmds.setAttr(RC_FAT1_L[0] + "." + refForeArmL + "W0", 2)
					cmds.setAttr(RC_FAT1_L[0] + "." + refHandRollDummyL + "W1", 1)
					cmds.setAttr(RC_FAT1_L[0] + ".interpType", 2)

					proxyFArmTwis2LocL = self.createWireBox('pyFArmTwis2Loc'+SN+'_L', 4,4,4,[0,0,0],[0.05,0.2,0.2])
					cmds.parent(proxyFArmTwis2LocL, refForeArmL)
					HiddenList.append(proxyFArmTwis2LocL)
					PC_FAT2_L = cmds.pointConstraint(refForeArmL, refHandL, proxyFArmTwis2LocL)
					cmds.setAttr(PC_FAT2_L[0] + "." + refForeArmL + "W0", 1)
					cmds.setAttr(PC_FAT2_L[0] + "." + refHandL + "W1", 2)
					RC_FAT2_L = cmds.orientConstraint(refForeArmL, refHandRollDummyL, proxyFArmTwis2LocL, mo=False)
					cmds.setAttr(RC_FAT2_L[0] + "." + refForeArmL + "W0", 1)
					cmds.setAttr(RC_FAT2_L[0] + "." + refHandRollDummyL + "W1", 2)
					cmds.setAttr(RC_FAT2_L[0] + ".interpType", 2)

					lockPointFKArmL = cmds.spaceLocator(name='lpFKArm'+SN+'_L')[0]
					cmds.xform(lockPointFKArmL, ws=True, t=UpArmLocL)
					cmds.parent(lockPointFKArmL, CtrlUpArmL_parent)
					HiddenList.append(lockPointFKArmL)

					gpFKArmL = cmds.group(em=True, name='gpFKArm'+SN+'_L')
					xV = [0,1,0]
					yV = [0,0,-1]
					if bIsZUp:
						xV = [0,0,1]
						yV = [0,1,0]
					# cmds.xform(gpFKArmL, ws=True, t=UpArmLocL)
					cmds.xform(gpFKArmL, ws=True, m=getTransMatrix(0, xV, 1, yV, UpArmLocL))
					cmds.parent(gpFKArmL, CtrlRoot)
					cmds.pointConstraint(lockPointFKArmL, gpFKArmL)

					ctrlUpperArmFK_L = self.createWireBox('FKUpperArm'+SN+'_L', uArmLength,12,12, [uArmLength*0.5,0,0],Color_Ctrl2_L)
					tmpShapes = cmds.listRelatives(ctrlUpperArmFK_L, s=True)
					for sh in tmpShapes:
						cmds.xform(sh+'.cv[0:999]', s=[-1,-1,-1])
					CtrlList.append(ctrlUpperArmFK_L)
					ListOnlyRot.append(ctrlUpperArmFK_L)
					# if bIsZUp:
					# 	cmds.setAttr(ctrlUpperArmFK_L+".rotateOrder", 3)
					cmds.xform(ctrlUpperArmFK_L, ws=True, m=cmds.xform(BArmUpperL,q=True,ws=True,m=True))
					cmds.parent(ctrlUpperArmFK_L, gpFKArmL)

					ctrlForeArmFK_L = self.createWireBox('FKForeArm'+SN+'_L', fArmLength,12,12, [fArmLength*0.5,0,0],Color_Ctrl2_L)
					tmpShapes = cmds.listRelatives(ctrlForeArmFK_L, s=True)
					for sh in tmpShapes:
						cmds.xform(sh+'.cv[0:999]', s=[-1,-1,-1])
					CtrlList.append(ctrlForeArmFK_L)
					ListOnlyRot.append(ctrlForeArmFK_L)
					# if bIsZUp:
					# 	cmds.setAttr(ctrlForeArmFK_L+".rotateOrder", 3)
					cmds.xform(ctrlForeArmFK_L, ws=True, m=cmds.xform(BArmForeL,q=True,ws=True,m=True))
					cmds.parent(ctrlForeArmFK_L, ctrlUpperArmFK_L)
					cmds.setAttr(ctrlForeArmFK_L+".rotateOrder", 3)

					FKHandSizeL = [refSizeHand,refSizeHand,refSizeHand*0.75]
					# if bIsZUp:
					# 	FKHandSizeL = [refSizeHand,refSizeHand*0.75,refSizeHand]
					ctrlHandFK_L = self.createWireBox('FKHand'+SN+'_L', FKHandSizeL[0],FKHandSizeL[1],FKHandSizeL[2], [refSizeHand*0.5,0,0],Color_Ctrl2_L)
					tmpShapes = cmds.listRelatives(ctrlHandFK_L, s=True)
					for sh in tmpShapes:
						cmds.xform(sh+'.cv[0:999]', s=[-1,-1,-1])
					CtrlList.append(ctrlHandFK_L)
					ListOnlyRot.append(ctrlHandFK_L)
					cmds.xform(ctrlHandFK_L, ws=True, m=cmds.xform(BHandL,q=True,ws=True,m=True))
					cmds.parent(ctrlHandFK_L, ctrlForeArmFK_L)

					endArmFKL = cmds.spaceLocator(name='endFKArm'+SN+'_L')[0]
					cmds.xform(endArmFKL, ws=True, t=HandLocL)
					cmds.parent(endArmFKL, ctrlForeArmFK_L)
					cmds.setAttr(endArmFKL+".translateZ", 0.01)
					HiddenList.append(endArmFKL)

					refFKArmCentL = cmds.spaceLocator(name='rfFKArmCent'+SN+'_L')[0]
					cmds.pointConstraint(ctrlUpperArmFK_L, endArmFKL, refFKArmCentL)
					cmds.aimConstraint(endArmFKL, refFKArmCentL, aim=[1,0,0], u=[0,1,0], wut="object", wuo=ctrlForeArmFK_L)
					# cmds.parent(refFKArmCentL, CtrlRoot)
					MidItemList.append(refFKArmCentL)
					HiddenList.append(refFKArmCentL)
					proxyFKArmUppL = cmds.spaceLocator(name='pyFKArmUpp'+SN+'_L')[0]
					cmds.xform(proxyFKArmUppL, ws=True, t=LArmUpVPos)
					cmds.parent(proxyFKArmUppL, refFKArmCentL)
					HiddenList.append(proxyFKArmUppL)

					#----
					CtrlHandIKR = self.createWireSpherifyCrossArrow('HandIK'+SN+'_R', refSizeHand*1.2, 90, 0, True, Color_Ctrl1_R, [0,-refSizeHand*0.25,0])
					tmpShapes = cmds.listRelatives(CtrlHandIKR, s=True)
					for sh in tmpShapes:
						cmds.xform(sh+'.cv[0:999]', s=[1,1.5,1.5])
					CtrlList.append(CtrlHandIKR)
					ListNoScl.append(CtrlHandIKR)
					cmds.setAttr(CtrlHandIKR+".rotateOrder", 1)
					cmds.xform(CtrlHandIKR,ws=True,m=getTransMatrix(1, getVector(CenFingerLocR, HandLocR), 2, RHandUpV, HandLocR))
					cmds.parent(CtrlHandIKR, CtrlRoot)
					CtrlHandIKL = self.createWireSpherifyCrossArrow('HandIK'+SN+'_L', refSizeHand*1.2, 90, 0, False, Color_Ctrl1_L, [0,-refSizeHand*0.25,0])
					tmpShapes = cmds.listRelatives(CtrlHandIKL, s=True)
					for sh in tmpShapes:
						cmds.xform(sh+'.cv[0:999]', s=[1,1.5,1.5])
					CtrlList.append(CtrlHandIKL)
					ListNoScl.append(CtrlHandIKL)
					cmds.setAttr(CtrlHandIKL+".rotateOrder", 1)
					cmds.xform(CtrlHandIKL,ws=True,m=getTransMatrix(1, getVector(CenFingerLocL, HandLocL), 2, LHandUpV, HandLocL))
					cmds.parent(CtrlHandIKL, CtrlRoot)

					proxyHandIKR = cmds.spaceLocator(name='pyHandIK'+SN+'_R')[0]
					cmds.xform(proxyHandIKR, ws=True, m=cmds.xform(BHandR,q=True,ws=True,m=True))
					cmds.parent(proxyHandIKR, CtrlHandIKR)
					HiddenList.append(proxyHandIKR)
					proxyHandIKL = cmds.spaceLocator(name='pyHandIK'+SN+'_L')[0]
					cmds.xform(proxyHandIKL, ws=True, m=cmds.xform(BHandL,q=True,ws=True,m=True))
					cmds.parent(proxyHandIKL, CtrlHandIKL)
					HiddenList.append(proxyHandIKL)

					CtrlArmUpV_R = self.createWireSphere('ArmUpV'+SN+'_R', 4, Color_Ctrl1_R, RArmUpVPos)
					CtrlList.append(CtrlArmUpV_R)
					ListOnlyPos.append(CtrlArmUpV_R)
					cmds.parent(CtrlArmUpV_R, CtrlRoot)
					CtrlArmUpV_L = self.createWireSphere('ArmUpV'+SN+'_L', 4, Color_Ctrl1_L, LArmUpVPos)
					CtrlList.append(CtrlArmUpV_L)
					ListOnlyPos.append(CtrlArmUpV_L)
					cmds.parent(CtrlArmUpV_L, CtrlRoot)
					#-----Arm Soft IK 
					# armLength
					# ArmEndLength = 0.95 * armLength
					# ArmLefLength = armLength - ArmEndLength
					
					armSoftRange = cmds.shadingNode('multiplyDivide', n='armSoftRange'+SN, au=True)
					SNList.append(armSoftRange)
					cmds.connectAttr(CtrlRoot+'.SoftIkArm', armSoftRange+'.input1X', f=True)
					cmds.setAttr(armSoftRange+'.input2X', 0.02)

					ArmTmpLefLen = cmds.shadingNode('multiplyDivide', n='ArmTmpLefLen'+SN, au=True)
					SNList.append(ArmTmpLefLen)
					cmds.connectAttr(armSoftRange+'.outputX', ArmTmpLefLen+'.input1X', f=True)
					cmds.setAttr(ArmTmpLefLen+'.input2X', armLength)

					ArmLefLength = cmds.shadingNode('clamp', n='ArmLefLength'+SN, au=True)
					SNList.append(ArmLefLength)
					cmds.setAttr(ArmLefLength+'.min', 0.0001,0.0001,0.0001,type='float3')
					cmds.setAttr(ArmLefLength+'.max', armLength,armLength,armLength,type='float3')
					cmds.connectAttr(ArmTmpLefLen+'.outputX', ArmLefLength+'.inputR', f=True)

					ArmEndLength = cmds.shadingNode('plusMinusAverage', n='ArmEndLength'+SN, au=True)
					SNList.append(ArmEndLength)
					cmds.setAttr(ArmEndLength+'.operation', 2)
					# mel.eval('AEnewNonNumericMultiAddNewItem("' + ArmEndLength + '","input1D");')
					# mel.eval('AEnewNonNumericMultiAddNewItem("' + ArmEndLength + '","input1D");')
					cmds.connectAttr(ArmLefLength+'.outputR', ArmEndLength+'.input1D[0]', f=True)
					cmds.connectAttr(ArmLefLength+'.outputR', ArmEndLength+'.input1D[1]', f=True)
					cmds.disconnectAttr(ArmLefLength+'.outputR', ArmEndLength+'.input1D[0]')
					cmds.setAttr(ArmEndLength+'.input1D[0]', armLength)

					#Right arm
					ArmAimer_R = cmds.spaceLocator(n='ArmAimer'+SN+'_R')[0]
					HiddenList.append(ArmAimer_R)
					cmds.parent(ArmAimer_R, CtrlUpArmR_parent)
					cmds.xform(ArmAimer_R, ws=True, t=UpArmLocR)
					cmds.aimConstraint(CtrlHandIKR, ArmAimer_R, aim=[1,0,0], u=[0,1,0], wut="none")

					mtxArmIKCtrl_R = cmds.shadingNode('decomposeMatrix', n='mtxArmIKCtrl' + SN + '_R', au=True)
					SNList.append(mtxArmIKCtrl_R)
					cmds.connectAttr(CtrlHandIKR+'.worldMatrix[0]', mtxArmIKCtrl_R+'.inputMatrix', f=True)

					distArmIKCtrl_R = cmds.shadingNode('distanceBetween', n='distArmIKCtrl' + SN + '_R', au=True)
					SNList.append(distArmIKCtrl_R)
					cmds.connectAttr(cmds.listRelatives(ArmAimer_R, s=True)[0]+'.worldPosition[0]', distArmIKCtrl_R+'.point1', f=True)
					cmds.connectAttr(mtxArmIKCtrl_R+'.outputTranslate', distArmIKCtrl_R+'.point2', f=True)

					extraArmIKCtrl_R = cmds.shadingNode('plusMinusAverage', n='extraArmIKCtrl'+SN+'_R', au=True)
					SNList.append(extraArmIKCtrl_R)
					cmds.setAttr(extraArmIKCtrl_R+'.operation', 2)
					# mel.eval('AEnewNonNumericMultiAddNewItem("' + extraArmIKCtrl_R + '","input1D");')
					# mel.eval('AEnewNonNumericMultiAddNewItem("' + extraArmIKCtrl_R + '","input1D");')
					cmds.connectAttr(distArmIKCtrl_R+'.distance', extraArmIKCtrl_R+'.input1D[0]', f=True)
					cmds.connectAttr(ArmEndLength+'.output1D', extraArmIKCtrl_R+'.input1D[1]', f=True)

					mappingExtAIKCtrl_R = cmds.shadingNode('multiplyDivide', n='mappingExtAIKCtrl'+SN+'_R', au=True)
					SNList.append(mappingExtAIKCtrl_R)
					cmds.setAttr(mappingExtAIKCtrl_R+'.operation', 2)
					cmds.connectAttr(extraArmIKCtrl_R+'.output1D', mappingExtAIKCtrl_R+'.input1X', f=True)
					cmds.connectAttr(ArmLefLength+'.outputR', mappingExtAIKCtrl_R+'.input2X', f=True)

					invExtraArmIK_R = cmds.shadingNode('multiplyDivide', n='invExtraArmIK'+SN+'_R', au=True)
					SNList.append(invExtraArmIK_R)
					cmds.connectAttr(mappingExtAIKCtrl_R+'.outputX', invExtraArmIK_R+'.input1X', f=True)
					cmds.setAttr(invExtraArmIK_R+'.input2X', -1)

					expExtraArmIK_R = cmds.shadingNode('multiplyDivide', n='expExtraArmIK'+SN+'_R', au=True)
					SNList.append(expExtraArmIK_R)
					cmds.setAttr(expExtraArmIK_R+'.operation', 3)
					cmds.setAttr(expExtraArmIK_R+'.input1X', 2.71828182846)
					cmds.connectAttr(invExtraArmIK_R+'.outputX', expExtraArmIK_R+'.input2X', f=True)

					oneMinusExpArmIK_R = cmds.shadingNode('plusMinusAverage', n='oneMinusExpArmIK'+SN+'_R', au=True)
					SNList.append(oneMinusExpArmIK_R)
					cmds.setAttr(oneMinusExpArmIK_R+'.operation', 2)
					# mel.eval('AEnewNonNumericMultiAddNewItem("' + oneMinusExpArmIK_R + '","input1D");')
					# mel.eval('AEnewNonNumericMultiAddNewItem("' + oneMinusExpArmIK_R + '","input1D");')
					cmds.connectAttr(expExtraArmIK_R+'.outputX', oneMinusExpArmIK_R+'.input1D[0]', f=True)
					cmds.connectAttr(expExtraArmIK_R+'.outputX', oneMinusExpArmIK_R+'.input1D[1]', f=True)
					cmds.disconnectAttr(expExtraArmIK_R+'.outputX', oneMinusExpArmIK_R+'.input1D[0]')
					cmds.setAttr(oneMinusExpArmIK_R+'.input1D[0]', 1)

					clampOmExpArmIK_R = cmds.shadingNode('clamp', n='expExtraArmIK'+SN+'_R', au=True)
					SNList.append(clampOmExpArmIK_R)
					cmds.setAttr(clampOmExpArmIK_R+'.max', 1,1,1,type='float3')
					cmds.connectAttr(oneMinusExpArmIK_R+'.output1D', clampOmExpArmIK_R+'.inputR', f=True)

					softExtraDArmIK_R = cmds.shadingNode('multiplyDivide', n='softExtraDArmIK'+SN+'_R', au=True)
					SNList.append(softExtraDArmIK_R)
					cmds.setAttr(softExtraDArmIK_R+'.operation', 1)
					cmds.connectAttr(clampOmExpArmIK_R+'.outputR', softExtraDArmIK_R+'.input1X', f=True)
					cmds.connectAttr(ArmLefLength+'.outputR', softExtraDArmIK_R+'.input2X', f=True)

					finalSoftArmIKDis_R = cmds.shadingNode('plusMinusAverage', n='finalSoftArmIKDis'+SN+'_R', au=True)
					SNList.append(finalSoftArmIKDis_R)
					cmds.connectAttr(softExtraDArmIK_R+'.outputX', finalSoftArmIKDis_R+'.input1D[0]', f=True)
					cmds.connectAttr(ArmEndLength+'.output1D', finalSoftArmIKDis_R+'.input1D[1]', f=True)

					condiArmSoftIK_R = cmds.shadingNode('condition', n='condiArmSoftIK'+SN+'_R', au=True)
					SNList.append(condiArmSoftIK_R)
					cmds.connectAttr(distArmIKCtrl_R+'.distance', condiArmSoftIK_R+'.firstTerm')
					cmds.connectAttr(ArmEndLength+'.output1D', condiArmSoftIK_R+'.secondTerm', f=True)
					cmds.setAttr(condiArmSoftIK_R+'.operation', 2)
					cmds.connectAttr(finalSoftArmIKDis_R+'.output1D', condiArmSoftIK_R+'.colorIfTrueR', f=True)
					cmds.connectAttr(distArmIKCtrl_R+'.distance', condiArmSoftIK_R+'.colorIfFalseR', f=True)

					ArmSoftIK_R = cmds.spaceLocator(n='ArmSoftIK'+SN+'_R')[0]
					HiddenList.append(ArmSoftIK_R)
					cmds.parent(ArmSoftIK_R, ArmAimer_R)
					cmds.setAttr(ArmSoftIK_R+'.translate',0,0,0,type='double3')
					cmds.setAttr(ArmSoftIK_R+'.rotate',0,0,0,type='double3')
					cmds.connectAttr(condiArmSoftIK_R+'.outColorR',ArmSoftIK_R+'.tx', f=True)

					#Left arm
					ArmAimer_L = cmds.spaceLocator(n='ArmAimer'+SN+'_L')[0]
					HiddenList.append(ArmAimer_L)
					cmds.parent(ArmAimer_L, CtrlUpArmL_parent)
					cmds.xform(ArmAimer_L, ws=True, t=UpArmLocL)
					cmds.aimConstraint(CtrlHandIKL, ArmAimer_L, aim=[1,0,0], u=[0,1,0], wut="none")

					mtxArmIKCtrl_L = cmds.shadingNode('decomposeMatrix', n='mtxArmIKCtrl' + SN + '_L', au=True)
					SNList.append(mtxArmIKCtrl_L)
					cmds.connectAttr(CtrlHandIKL+'.worldMatrix[0]', mtxArmIKCtrl_L+'.inputMatrix', f=True)

					distArmIKCtrl_L = cmds.shadingNode('distanceBetween', n='distArmIKCtrl' + SN + '_L', au=True)
					SNList.append(distArmIKCtrl_L)
					cmds.connectAttr(cmds.listRelatives(ArmAimer_L, s=True)[0]+'.worldPosition[0]', distArmIKCtrl_L+'.point1', f=True)
					cmds.connectAttr(mtxArmIKCtrl_L+'.outputTranslate', distArmIKCtrl_L+'.point2', f=True)

					extraArmIKCtrl_L = cmds.shadingNode('plusMinusAverage', n='extraArmIKCtrl'+SN+'_L', au=True)
					SNList.append(extraArmIKCtrl_L)
					cmds.setAttr(extraArmIKCtrl_L+'.operation', 2)
					# mel.eval('AEnewNonNumericMultiAddNewItem("' + extraArmIKCtrl_L + '","input1D");')
					# mel.eval('AEnewNonNumericMultiAddNewItem("' + extraArmIKCtrl_L + '","input1D");')
					cmds.connectAttr(distArmIKCtrl_L+'.distance', extraArmIKCtrl_L+'.input1D[0]', f=True)
					cmds.connectAttr(ArmEndLength+'.output1D', extraArmIKCtrl_L+'.input1D[1]', f=True)

					mappingExtAIKCtrl_L = cmds.shadingNode('multiplyDivide', n='mappingExtAIKCtrl'+SN+'_L', au=True)
					SNList.append(mappingExtAIKCtrl_L)
					cmds.setAttr(mappingExtAIKCtrl_L+'.operation', 2)
					cmds.connectAttr(extraArmIKCtrl_L+'.output1D', mappingExtAIKCtrl_L+'.input1X', f=True)
					cmds.connectAttr(ArmLefLength+'.outputR', mappingExtAIKCtrl_L+'.input2X', f=True)

					invExtraArmIK_L = cmds.shadingNode('multiplyDivide', n='invExtraArmIK'+SN+'_L', au=True)
					SNList.append(invExtraArmIK_L)
					cmds.connectAttr(mappingExtAIKCtrl_L+'.outputX', invExtraArmIK_L+'.input1X', f=True)
					cmds.setAttr(invExtraArmIK_L+'.input2X', -1)

					expExtraArmIK_L = cmds.shadingNode('multiplyDivide', n='expExtraArmIK'+SN+'_L', au=True)
					SNList.append(expExtraArmIK_L)
					cmds.setAttr(expExtraArmIK_L+'.operation', 3)
					cmds.setAttr(expExtraArmIK_L+'.input1X', 2.71828182846)
					cmds.connectAttr(invExtraArmIK_L+'.outputX', expExtraArmIK_L+'.input2X', f=True)

					oneMinusExpArmIK_L = cmds.shadingNode('plusMinusAverage', n='oneMinusExpArmIK'+SN+'_L', au=True)
					SNList.append(oneMinusExpArmIK_L)
					cmds.setAttr(oneMinusExpArmIK_L+'.operation', 2)
					# mel.eval('AEnewNonNumericMultiAddNewItem("' + oneMinusExpArmIK_L + '","input1D");')
					# mel.eval('AEnewNonNumericMultiAddNewItem("' + oneMinusExpArmIK_L + '","input1D");')
					cmds.connectAttr(expExtraArmIK_L+'.outputX', oneMinusExpArmIK_L+'.input1D[0]', f=True)
					cmds.connectAttr(expExtraArmIK_L+'.outputX', oneMinusExpArmIK_L+'.input1D[1]', f=True)
					cmds.disconnectAttr(expExtraArmIK_L+'.outputX', oneMinusExpArmIK_L+'.input1D[0]')
					cmds.setAttr(oneMinusExpArmIK_L+'.input1D[0]', 1)

					clampOmExpArmIK_L = cmds.shadingNode('clamp', n='expExtraArmIK'+SN+'_L', au=True)
					SNList.append(clampOmExpArmIK_L)
					cmds.setAttr(clampOmExpArmIK_L+'.max', 1,1,1,type='float3')
					cmds.connectAttr(oneMinusExpArmIK_L+'.output1D', clampOmExpArmIK_L+'.inputR', f=True)

					softExtraDArmIK_L = cmds.shadingNode('multiplyDivide', n='softExtraDArmIK'+SN+'_L', au=True)
					SNList.append(softExtraDArmIK_L)
					cmds.setAttr(softExtraDArmIK_L+'.operation', 1)
					cmds.connectAttr(clampOmExpArmIK_L+'.outputR', softExtraDArmIK_L+'.input1X', f=True)
					cmds.connectAttr(ArmLefLength+'.outputR', softExtraDArmIK_L+'.input2X', f=True)

					finalSoftArmIKDis_L = cmds.shadingNode('plusMinusAverage', n='finalSoftArmIKDis'+SN+'_L', au=True)
					SNList.append(finalSoftArmIKDis_L)
					cmds.connectAttr(softExtraDArmIK_L+'.outputX', finalSoftArmIKDis_L+'.input1D[0]', f=True)
					cmds.connectAttr(ArmEndLength+'.output1D', finalSoftArmIKDis_L+'.input1D[1]', f=True)

					condiArmSoftIK_L = cmds.shadingNode('condition', n='condiArmSoftIK'+SN+'_L', au=True)
					SNList.append(condiArmSoftIK_L)
					cmds.connectAttr(distArmIKCtrl_L+'.distance', condiArmSoftIK_L+'.firstTerm')
					cmds.connectAttr(ArmEndLength+'.output1D', condiArmSoftIK_L+'.secondTerm', f=True)
					cmds.setAttr(condiArmSoftIK_L+'.operation', 2)
					cmds.connectAttr(finalSoftArmIKDis_L+'.output1D', condiArmSoftIK_L+'.colorIfTrueR', f=True)
					cmds.connectAttr(distArmIKCtrl_L+'.distance', condiArmSoftIK_L+'.colorIfFalseR', f=True)

					ArmSoftIK_L = cmds.spaceLocator(n='ArmSoftIK'+SN+'_L')[0]
					HiddenList.append(ArmSoftIK_L)
					cmds.parent(ArmSoftIK_L, ArmAimer_L)
					cmds.setAttr(ArmSoftIK_L+'.translate',0,0,0,type='double3')
					cmds.setAttr(ArmSoftIK_L+'.rotate',0,0,0,type='double3')
					cmds.connectAttr(condiArmSoftIK_L+'.outColorR',ArmSoftIK_L+'.tx', f=True)
					# return
					#-------
					PC_PAIK_R = cmds.pointConstraint(ArmSoftIK_R, ctrlHandFK_R, proxyArmIKR)
					cmds.setAttr(PC_PAIK_R[0] + "." + ArmSoftIK_R + "W0", 0)
					cmds.setAttr(PC_PAIK_R[0] + "." + ctrlHandFK_R + "W1", 1)
					
					PC_PAUP_R = cmds.pointConstraint(CtrlArmUpV_R, proxyFKArmUppR, proxyArmUpvR)
					cmds.setAttr(PC_PAUP_R[0] + "." + CtrlArmUpV_R + "W0", 0)
					cmds.setAttr(PC_PAUP_R[0] + "." + proxyFKArmUppR + "W1", 1)
					
					RC_PH_R = cmds.orientConstraint(proxyHandIKR, ctrlHandFK_R, proxyEndArmJntR, mo=True)
					cmds.setAttr(RC_PH_R[0] + "." + proxyHandIKR + "W0", 0)
					cmds.setAttr(RC_PH_R[0] + "." + ctrlHandFK_R + "W1", 1)
					cmds.setAttr(RC_PH_R[0] + ".interpType", 2)

					PC_PAIK_L = cmds.pointConstraint(ArmSoftIK_L, ctrlHandFK_L, proxyArmIKL)
					cmds.setAttr(PC_PAIK_L[0] + "." + ArmSoftIK_L + "W0", 0)
					cmds.setAttr(PC_PAIK_L[0] + "." + ctrlHandFK_L + "W1", 1)
					
					PC_PAUP_L = cmds.pointConstraint(CtrlArmUpV_L, proxyFKArmUppL, proxyArmUpvL)
					cmds.setAttr(PC_PAUP_L[0] + "." + CtrlArmUpV_L + "W0", 0)
					cmds.setAttr(PC_PAUP_L[0] + "." + proxyFKArmUppL + "W1", 1)
					
					RC_PH_L = cmds.orientConstraint(proxyHandIKL, ctrlHandFK_L, proxyEndArmJntL, mo=True)
					cmds.setAttr(RC_PH_L[0] + "." + proxyHandIKL + "W0", 0)
					cmds.setAttr(RC_PH_L[0] + "." + ctrlHandFK_L + "W1", 1)
					cmds.setAttr(RC_PH_L[0] + ".interpType", 2)
					#---------------
					oneMinusFKIK_R = cmds.shadingNode("plusMinusAverage",au=True)
					SNList.append(oneMinusFKIK_R)
					cmds.setAttr(oneMinusFKIK_R+".operation", 2)
					cmds.connectAttr(CtrlRoot + ".RArmFKIKBlend", oneMinusFKIK_R+".input1D[0]",f=True)
					cmds.connectAttr(CtrlRoot + ".RArmFKIKBlend", oneMinusFKIK_R+".input1D[1]",f=True)
					cmds.disconnectAttr(CtrlRoot + ".RArmFKIKBlend", oneMinusFKIK_R+".input1D[0]")
					cmds.setAttr(oneMinusFKIK_R+".input1D[0]", 1)
					
					cmds.connectAttr(CtrlRoot + ".RArmFKIKBlend", PC_PAIK_R[0] + "." + ArmSoftIK_R + "W0",f=True)
					cmds.connectAttr(CtrlRoot + ".RArmFKIKBlend", PC_PAUP_R[0] + "." + CtrlArmUpV_R + "W0",f=True)
					cmds.connectAttr(CtrlRoot + ".RArmFKIKBlend", RC_PH_R[0] + "." + proxyHandIKR + "W0",f=True)
					
					cmds.connectAttr(oneMinusFKIK_R + ".output1D", PC_PAIK_R[0] + "." + ctrlHandFK_R + "W1",f=True)
					cmds.connectAttr(oneMinusFKIK_R + ".output1D", PC_PAUP_R[0] + "." + proxyFKArmUppR + "W1",f=True)
					cmds.connectAttr(oneMinusFKIK_R + ".output1D", RC_PH_R[0] + "." + ctrlHandFK_R + "W1",f=True)

					oneMinusFKIK_L = cmds.shadingNode("plusMinusAverage",au=True)
					SNList.append(oneMinusFKIK_L)
					cmds.setAttr(oneMinusFKIK_L+".operation", 2)
					cmds.connectAttr(CtrlRoot + ".LArmFKIKBlend", oneMinusFKIK_L+".input1D[0]",f=True)
					cmds.connectAttr(CtrlRoot + ".LArmFKIKBlend", oneMinusFKIK_L+".input1D[1]",f=True)
					cmds.disconnectAttr(CtrlRoot + ".LArmFKIKBlend", oneMinusFKIK_L+".input1D[0]")
					cmds.setAttr(oneMinusFKIK_L+".input1D[0]", 1)
					
					cmds.connectAttr(CtrlRoot + ".LArmFKIKBlend", PC_PAIK_L[0] + "." + ArmSoftIK_L + "W0",f=True)
					cmds.connectAttr(CtrlRoot + ".LArmFKIKBlend", PC_PAUP_L[0] + "." + CtrlArmUpV_L + "W0",f=True)
					cmds.connectAttr(CtrlRoot + ".LArmFKIKBlend", RC_PH_L[0] + "." + proxyHandIKL + "W0",f=True)
					
					cmds.connectAttr(oneMinusFKIK_L + ".output1D", PC_PAIK_L[0] + "." + ctrlHandFK_L + "W1",f=True)
					cmds.connectAttr(oneMinusFKIK_L + ".output1D", PC_PAUP_L[0] + "." + proxyFKArmUppL + "W1",f=True)
					cmds.connectAttr(oneMinusFKIK_L + ".output1D", RC_PH_L[0] + "." + ctrlHandFK_L + "W1",f=True)
					#-----------------
					Multi100FKIK_R = cmds.shadingNode("multiplyDivide",au=True)
					SNList.append(Multi100FKIK_R)
					cmds.setAttr(Multi100FKIK_R+".input1X", 100)
					cmds.connectAttr(CtrlRoot + ".RArmFKIKBlend", Multi100FKIK_R+".input2X",f=True)
					
					invMulti100FKIK_R = cmds.shadingNode("plusMinusAverage",au=True)
					SNList.append(invMulti100FKIK_R)
					cmds.setAttr(invMulti100FKIK_R+".operation", 2)
					cmds.connectAttr(Multi100FKIK_R + ".outputX", invMulti100FKIK_R+".input1D[0]",f=True)
					cmds.connectAttr(Multi100FKIK_R + ".outputX", invMulti100FKIK_R+".input1D[1]",f=True)
					cmds.disconnectAttr(Multi100FKIK_R + ".outputX", invMulti100FKIK_R+".input1D[0]")
					cmds.setAttr(invMulti100FKIK_R+".input1D[0]", 100)
					
					cmds.connectAttr(Multi100FKIK_R + ".outputX", CtrlHandIKR + ".visibility",f=True)
					cmds.connectAttr(Multi100FKIK_R + ".outputX", CtrlArmUpV_R + ".visibility",f=True)
					cmds.connectAttr(invMulti100FKIK_R + ".output1D", ctrlUpperArmFK_R + ".visibility",f=True)
					cmds.connectAttr(invMulti100FKIK_R + ".output1D", ctrlForeArmFK_R + ".visibility",f=True)
					cmds.connectAttr(invMulti100FKIK_R + ".output1D", ctrlHandFK_R + ".visibility",f=True)
					
					Multi100FKIK_L = cmds.shadingNode("multiplyDivide",au=True)
					SNList.append(Multi100FKIK_L)
					cmds.setAttr(Multi100FKIK_L+".input1X", 100)
					cmds.connectAttr(CtrlRoot + ".LArmFKIKBlend", Multi100FKIK_L+".input2X",f=True)
					
					invMulti100FKIK_L = cmds.shadingNode("plusMinusAverage",au=True)
					SNList.append(invMulti100FKIK_L)
					cmds.setAttr(invMulti100FKIK_L+".operation", 2)
					cmds.connectAttr(Multi100FKIK_L + ".outputX", invMulti100FKIK_L+".input1D[0]",f=True)
					cmds.connectAttr(Multi100FKIK_L + ".outputX", invMulti100FKIK_L+".input1D[1]",f=True)
					cmds.disconnectAttr(Multi100FKIK_L + ".outputX", invMulti100FKIK_L+".input1D[0]")
					cmds.setAttr(invMulti100FKIK_L+".input1D[0]", 100)
					
					cmds.connectAttr(Multi100FKIK_L + ".outputX", CtrlHandIKL + ".visibility",f=True)
					cmds.connectAttr(Multi100FKIK_L + ".outputX", CtrlArmUpV_L + ".visibility",f=True)
					cmds.connectAttr(invMulti100FKIK_L + ".output1D", ctrlUpperArmFK_L + ".visibility",f=True)
					cmds.connectAttr(invMulti100FKIK_L + ".output1D", ctrlForeArmFK_L + ".visibility",f=True)
					cmds.connectAttr(invMulti100FKIK_L + ".output1D", ctrlHandFK_L + ".visibility",f=True)
					#----------
					ProxyElbowBuffR = self.createWireBox('pyElbowBuff'+SN+'_R', 2, 5, 5,[0,0,0])
					HiddenList.append(ProxyElbowBuffR)
					cmds.parent(ProxyElbowBuffR, proxyForeArmJntR)
					cmds.xform(ProxyElbowBuffR,ws=False, t=[-0.1,0,0])
					PEBROC = cmds.orientConstraint(proxyUpperArmJntR,proxyForeArmJntR,ProxyElbowBuffR,mo=False)
					cmds.setAttr(PEBROC[0] + ".interpType", 2)

					ArmAngleD180_R = cmds.shadingNode("multiplyDivide",au=True)
					SNList.append(ArmAngleD180_R)
					cmds.setAttr(ArmAngleD180_R+".operation",2)
					cmds.connectAttr(proxyForeArmJntR + ".ry", ArmAngleD180_R+".input1X",f=True)
					cmds.setAttr(ArmAngleD180_R+".input2X",180)

					ArmAngleP2_R = cmds.shadingNode("multiplyDivide",au=True)
					SNList.append(ArmAngleP2_R)
					cmds.connectAttr(ArmAngleD180_R + ".outputX", ArmAngleP2_R+".input1X",f=True)
					cmds.connectAttr(ArmAngleD180_R + ".outputX", ArmAngleP2_R+".input2X",f=True)
					
					ArmAngleXV_R = cmds.shadingNode("multiplyDivide",au=True)
					SNList.append(ArmAngleXV_R)
					cmds.connectAttr(ArmAngleP2_R + ".outputX", ArmAngleXV_R+".input1X",f=True)
					cmds.setAttr(ArmAngleXV_R+".input2X",1.7)
					
					ArmAngleP1_R = cmds.shadingNode("plusMinusAverage",au=True)
					SNList.append(ArmAngleP1_R)
					cmds.connectAttr(ArmAngleXV_R + ".outputX", ArmAngleP1_R+".input1D[0]",f=True)
					cmds.connectAttr(ArmAngleXV_R + ".outputX", ArmAngleP1_R+".input1D[1]",f=True)
					cmds.disconnectAttr(ArmAngleXV_R + ".outputX", ArmAngleP1_R+".input1D[0]")
					cmds.setAttr(ArmAngleP1_R+".input1D[0]",1)
					
					cmds.connectAttr(ArmAngleP1_R + ".output1D", ProxyElbowBuffR+".sz",f=True)

					ProxyElbowBuffL = self.createWireBox('pyElbowBuff'+SN+'_L', 2, 5, 5,[0,0,0])
					HiddenList.append(ProxyElbowBuffL)
					cmds.parent(ProxyElbowBuffL, proxyForeArmJntL)
					cmds.xform(ProxyElbowBuffL,ws=False, t=[-0.1,0,0])
					PEBLOC = cmds.orientConstraint(proxyUpperArmJntL,proxyForeArmJntL,ProxyElbowBuffL,mo=False)
					cmds.setAttr(PEBLOC[0] + ".interpType", 2)
					
					ArmAngleD180_L = cmds.shadingNode("multiplyDivide",au=True)
					SNList.append(ArmAngleD180_L)
					cmds.setAttr(ArmAngleD180_L+".operation",2)
					cmds.connectAttr(proxyForeArmJntL + ".ry", ArmAngleD180_L+".input1X",f=True)
					cmds.setAttr(ArmAngleD180_L+".input2X",180)
					
					ArmAngleP2_L = cmds.shadingNode("multiplyDivide",au=True)
					SNList.append(ArmAngleP2_L)
					cmds.connectAttr(ArmAngleD180_L + ".outputX", ArmAngleP2_L+".input1X",f=True)
					cmds.connectAttr(ArmAngleD180_L + ".outputX", ArmAngleP2_L+".input2X",f=True)
					
					ArmAngleXV_L = cmds.shadingNode("multiplyDivide",au=True)
					SNList.append(ArmAngleXV_L)
					cmds.connectAttr(ArmAngleP2_L + ".outputX", ArmAngleXV_L+".input1X",f=True)
					cmds.setAttr(ArmAngleXV_L+".input2X",1.7)
					
					ArmAngleP1_L = cmds.shadingNode("plusMinusAverage",au=True)
					SNList.append(ArmAngleP1_L)
					cmds.connectAttr(ArmAngleXV_L + ".outputX", ArmAngleP1_L+".input1D[0]",f=True)
					cmds.connectAttr(ArmAngleXV_L + ".outputX", ArmAngleP1_L+".input1D[1]",f=True)
					cmds.disconnectAttr(ArmAngleXV_L + ".outputX", ArmAngleP1_L+".input1D[0]")
					cmds.setAttr(ArmAngleP1_L+".input1D[0]",1)
					
					cmds.connectAttr(ArmAngleP1_L + ".output1D", ProxyElbowBuffL+".sz",f=True)
					#----------
					locPointFK2HandIK_R = cmds.spaceLocator(name='lpFK2IK'+SN+'_R')[0]
					HiddenList.append(locPointFK2HandIK_R)
					cmds.xform(locPointFK2HandIK_R,ws=True,m=cmds.xform(CtrlHandIKR,q=True,ws=True,m=True))
					cmds.parent(locPointFK2HandIK_R, proxyEndArmJntR)
					
					locPointFK2HandIK_L = cmds.spaceLocator(name='lpFK2IK'+SN+'_L')[0]
					HiddenList.append(locPointFK2HandIK_L)
					cmds.xform(locPointFK2HandIK_L,ws=True,m=cmds.xform(CtrlHandIKL,q=True,ws=True,m=True))
					cmds.parent(locPointFK2HandIK_L, proxyEndArmJntL)
					
					locPointIK2FKUpArm_R = cmds.spaceLocator(name='lpIK2FKUpArm'+SN+'_R')[0]
					HiddenList.append(locPointIK2FKUpArm_R)
					cmds.xform(locPointIK2FKUpArm_R,ws=True,m=cmds.xform(ctrlUpperArmFK_R,q=True,ws=True,m=True))
					cmds.parent(locPointIK2FKUpArm_R, proxyUpperArmJntR)
					
					locPointIK2FKFoArm_R = cmds.spaceLocator(name='lpIK2FKFoArm'+SN+'_R')[0]
					HiddenList.append(locPointIK2FKFoArm_R)
					cmds.xform(locPointIK2FKFoArm_R,ws=True,m=cmds.xform(ctrlForeArmFK_R,q=True,ws=True,m=True))
					cmds.parent(locPointIK2FKFoArm_R, proxyForeArmJntR)
					
					locPointIK2FKHand_R = cmds.spaceLocator(name='lpIK2FKHand'+SN+'_R')[0]
					HiddenList.append(locPointIK2FKHand_R)
					cmds.xform(locPointIK2FKHand_R,ws=True,m=cmds.xform(ctrlHandFK_R,q=True,ws=True,m=True))
					cmds.parent(locPointIK2FKHand_R, proxyEndArmJntR)
					
					locPointIK2FKUpArm_L = cmds.spaceLocator(name='lpIK2FKUpArm'+SN+'_L')[0]
					HiddenList.append(locPointIK2FKUpArm_L)
					cmds.xform(locPointIK2FKUpArm_L,ws=True,m=cmds.xform(ctrlUpperArmFK_L,q=True,ws=True,m=True))
					cmds.parent(locPointIK2FKUpArm_L, proxyUpperArmJntL)
					
					locPointIK2FKFoArm_L = cmds.spaceLocator(name='lpIK2FKFoArm'+SN+'_L')[0]
					HiddenList.append(locPointIK2FKFoArm_L)
					cmds.xform(locPointIK2FKFoArm_L,ws=True,m=cmds.xform(ctrlForeArmFK_L,q=True,ws=True,m=True))
					cmds.parent(locPointIK2FKFoArm_L, proxyForeArmJntL)
					
					locPointIK2FKHand_L = cmds.spaceLocator(name='lpIK2FKHand'+SN+'_L')[0]
					HiddenList.append(locPointIK2FKHand_L)
					cmds.xform(locPointIK2FKHand_L,ws=True,m=cmds.xform(ctrlHandFK_L,q=True,ws=True,m=True))
					cmds.parent(locPointIK2FKHand_L, proxyEndArmJntL)

					#----------
					cmds.setAttr(CtrlHandIKR+".visibility", k=False)
					cmds.setAttr(CtrlArmUpV_R+".visibility", k=False)
					cmds.setAttr(ctrlUpperArmFK_R+".visibility", k=False)
					cmds.setAttr(ctrlForeArmFK_R+".visibility", k=False)
					cmds.setAttr(ctrlHandFK_R+".visibility", k=False)
					
					cmds.setAttr(CtrlHandIKL+".visibility", k=False)
					cmds.setAttr(CtrlArmUpV_L+".visibility", k=False)
					cmds.setAttr(ctrlUpperArmFK_L+".visibility", k=False)
					cmds.setAttr(ctrlForeArmFK_L+".visibility", k=False)
					cmds.setAttr(ctrlHandFK_L+".visibility", k=False)

					#--------------
					BoneConstraintList.append(cmds.parentConstraint(proxyUArmLocR, BArmUpperR, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(proxyUArmLocL, BArmUpperL, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(refForeArmR, BArmForeR, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(refForeArmL, BArmForeL, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(refHandR, BHandR, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(refHandL, BHandL, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(buffUArmR, BArmUpperBuffR, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(buffUArmL, BArmUpperBuffL, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(proxyUArmTwis1LocR, BArmUpperTwist1R, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(proxyUArmTwis2LocR, BArmUpperTwist2R, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(proxyUArmTwis1LocL, BArmUpperTwist1L, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(proxyUArmTwis2LocL, BArmUpperTwist2L, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(ProxyElbowBuffR, BElbowBuffR, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(ProxyElbowBuffL, BElbowBuffL, mo=False)[0])
					BoneConstraintList.append(cmds.scaleConstraint(ProxyElbowBuffR, BElbowBuffR, mo=False)[0])
					BoneConstraintList.append(cmds.scaleConstraint(ProxyElbowBuffL, BElbowBuffL, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(proxyFArmTwis1LocR, BArmForeTwist1R, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(proxyFArmTwis2LocR, BArmForeTwist2R, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(proxyFArmTwis1LocL, BArmForeTwist1L, mo=False)[0])
					BoneConstraintList.append(cmds.parentConstraint(proxyFArmTwis2LocL, BArmForeTwist2L, mo=False)[0])

					#-------------------------------------------------------------------
					gpFingerR = cmds.group(em=True, name='rootFinger'+SN+'_R')
					cmds.xform(gpFingerR,ws=True,m=cmds.xform(proxyEndArmJntR,q=True,ws=True,m=True))
					cmds.parent(gpFingerR,CtrlRoot)
					cmds.parentConstraint(proxyEndArmJntR, gpFingerR, mo=False)
					gpFingerL = cmds.group(em=True, name='rootFinger'+SN+'_L')
					cmds.xform(gpFingerL,ws=True,m=cmds.xform(proxyEndArmJntL,q=True,ws=True,m=True))
					cmds.parent(gpFingerL,CtrlRoot)
					cmds.parentConstraint(proxyEndArmJntL, gpFingerL, mo=False)

					for f in range(0, len(bgFingerRootList)):
						fSN = ''
						if len(bgFingerRootList) > 1:
							fSN = '_'+str(f)
						RFingerBN = getRowFromMatrix(cmds.xform(bgFingerRootList[f],q=True,ws=True,m=True), 1)
						RFingerUpV = getRowFromMatrix(cmds.xform(bgFingerRootList[f],q=True,ws=True,m=True), 2)
						LFingerBN = multiVec(RFingerBN, [-1,1,1])
						LFingerUpV = multiVec(RFingerUpV, [-1,1,1])

						FingerSegList = getTrainNodes(bgFingerRootList[f], True)
						
						gpFinger0R = cmds.group(em=True, name='rootFinger'+SN+fSN+'_R')
						cmds.parent(gpFinger0R, gpFingerR)
						tmpParent = gpFinger0R
						cmds.select(BHandR)
						for fs in range(0, len(FingerSegList)-1):
							fsSN = str(fs)

							fPosR = cmds.xform(FingerSegList[fs],q=True,ws=True,t=True)
							endPosR = cmds.xform(FingerSegList[fs+1],q=True,ws=True,t=True)
							
							BFingerR = cmds.joint(name='B_Finger'+SN+fSN+fsSN+'_R',p=fPosR, rad= 1.5)
							BoneList.append(BFingerR)
							cmds.xform(BFingerR,ws=True,m=getTransMatrix(0, getVector(fPosR, endPosR), 2, RFingerUpV, fPosR))

							if fs == 0:
								cmds.xform(gpFinger0R,ws=True,m=cmds.xform(BFingerR,q=True,ws=True,m=True))
								CtrlFinger00R = self.createWireCircle('Finger'+SN+fSN+fsSN+'_R', FingerCtrlSize, 0, FingerCtrlSeg, [0,0,0], FingerCtrlRColor)
								CtrlList.append(CtrlFinger00R)
								ListOnlyRot.append(CtrlFinger00R)
								cmds.xform(CtrlFinger00R,ws=True,m=cmds.xform(BFingerR,q=True,ws=True,m=True))
								cmds.parent(CtrlFinger00R, tmpParent)
								BoneConstraintList.append(cmds.parentConstraint(CtrlFinger00R, BFingerR, mo=False)[0])
								tmpParent = CtrlFinger00R
							else:
								CtrlFingerR = self.createWireCircle('Finger'+SN+fSN+fsSN+'_R', FingerCtrlSize, 0, FingerCtrlSeg, [0,0,0], FingerCtrlRColor)
								CtrlList.append(CtrlFingerR)
								ListOnlyRot.append(CtrlFingerR)
								cmds.xform(CtrlFingerR,ws=True,m=cmds.xform(BFingerR,q=True,ws=True,m=True))
								cmds.parent(CtrlFingerR, tmpParent)
								BoneConstraintList.append(cmds.parentConstraint(CtrlFingerR, BFingerR, mo=False)[0])
								tmpParent = CtrlFingerR

							cmds.select(BFingerR)

						EndFingerR = cmds.joint(name='end_Finger'+SN+fSN+'_R',p=cmds.xform(FingerSegList[-1],q=True,ws=True,t=True), rad= 1.5)
						cmds.xform(EndFingerR,ro=[0,0,0])

						gpFinger0L = cmds.group(em=True, name='rootFinger'+SN+fSN+'_L')
						cmds.parent(gpFinger0L, gpFingerL)
						tmpParent = gpFinger0L
						cmds.select(BHandL)
						for fs in range(0, len(FingerSegList)-1):
							fsSN = str(fs)

							fPosR = cmds.xform(FingerSegList[fs],q=True,ws=True,t=True)
							endPosR = cmds.xform(FingerSegList[fs+1],q=True,ws=True,t=True)
							fPosL = multiVec(fPosR, [-1,1,1])
							endPosL = multiVec(endPosR, [-1,1,1])

							BFingerL = cmds.joint(name='B_Finger'+SN+fSN+fsSN+'_L',p=fPosL, rad= 1.5)
							BoneList.append(BFingerL)
							cmds.xform(BFingerL,ws=True,m=getTransMatrix(0, getVector(fPosL, endPosL), 2, LFingerUpV, fPosL))

							if fs == 0:
								cmds.xform(gpFinger0L,ws=True,m=cmds.xform(BFingerL,q=True,ws=True,m=True))
								CtrlFinger00L = self.createWireCircle('Finger'+SN+fSN+fsSN+'_L', FingerCtrlSize, 0, FingerCtrlSeg, [0,0,0], FingerCtrlLColor)
								CtrlList.append(CtrlFinger00L)
								ListOnlyRot.append(CtrlFinger00L)
								cmds.xform(CtrlFinger00L,ws=True,m=cmds.xform(BFingerL,q=True,ws=True,m=True))
								cmds.parent(CtrlFinger00L, tmpParent)
								BoneConstraintList.append(cmds.parentConstraint(CtrlFinger00L, BFingerL, mo=False)[0])
								tmpParent = CtrlFinger00L
							else:
								CtrlFingerL = self.createWireCircle('Finger'+SN+fSN+fsSN+'_L', FingerCtrlSize, 0, FingerCtrlSeg, [0,0,0], FingerCtrlLColor)
								CtrlList.append(CtrlFingerL)
								ListOnlyRot.append(CtrlFingerL)
								cmds.xform(CtrlFingerL,ws=True,m=cmds.xform(BFingerL,q=True,ws=True,m=True))
								cmds.parent(CtrlFingerL, tmpParent)
								BoneConstraintList.append(cmds.parentConstraint(CtrlFingerL, BFingerL, mo=False)[0])
								tmpParent = CtrlFingerL

							cmds.select(BFingerL)

						endFinLoc_L = multiVec(cmds.xform(FingerSegList[-1],q=True,ws=True,t=True), [-1,1,1])
						EndFingerL = cmds.joint(name='end_Finger'+SN+fSN+'_L',p=endFinLoc_L, rad= 1.5)
						cmds.xform(EndFingerL,ro=[0,0,0])

			for i in range(0, len(ThighList)):
				SN = ''
				if len(ThighList) > 1:
					SN = str(i)

				bgThigh_parent = cmds.listRelatives(ThighList[i], p=True,pa=True)[0]
				bgCalf = cmds.listRelatives(ThighList[i], c=True,pa=True)[0]
				bgFoot = cmds.listRelatives(bgCalf, c=True,pa=True)[0]
				bgToe = cmds.listRelatives(bgFoot, c=True,pa=True)[0]
				bgToeE = cmds.listRelatives(bgToe, c=True,pa=True)[0]

				Thigh_Parent = 'B_'+bgThigh_parent.split(':')[-1][4:]
				CtrlThigh_Parent = Thigh_Parent[2:]

				ThighLocR = cmds.xform(ThighList[i],q=True,ws=True,t=True)
				CalfLocR = cmds.xform(bgCalf,q=True,ws=True,t=True)
				FootLocR = cmds.xform(bgFoot,q=True,ws=True,t=True)
				ToeLocR = cmds.xform(bgToe,q=True,ws=True,t=True)
				ToeELocR = cmds.xform(bgToeE,q=True,ws=True,t=True)
				RLegSideV = crossVec(getVector(ThighLocR, CalfLocR), getVector(CalfLocR, FootLocR))
				RLegUpV = crossVec(getVector(ThighLocR, FootLocR), RLegSideV)

				LegLength = getDistance(ThighLocR, CalfLocR) + getDistance(CalfLocR, FootLocR)
				FootLength = getDistance(FootLocR, ToeLocR) + getDistance(ToeLocR, ToeELocR)

				ThighLocL = multiVec(ThighLocR, [-1,1,1])
				CalfLocL = multiVec(CalfLocR, [-1,1,1])
				FootLocL = multiVec(FootLocR, [-1,1,1])
				ToeLocL = multiVec(ToeLocR, [-1,1,1])
				ToeELocL = multiVec(ToeELocR, [-1,1,1])
				LLegSideV = crossVec(getVector(ThighLocL, CalfLocL), getVector(CalfLocL, FootLocL))
				LLegUpV = multiVec(RLegUpV, [-1,1,1])

				LegUpVPosR = sumVec(scaleVec(sumVec(ThighLocR, FootLocR), 0.5), scaleVec(RLegUpV, 0.75*LegLength))
				LegUpVPosL = multiVec(LegUpVPosR, [-1,1,1])

				

				cmds.select( Thigh_Parent )
				BThighR = cmds.joint(name='B_Thigh'+SN+'_R',p=ThighLocR, rad= 3.5)
				BoneList.append(BThighR)
				cmds.xform(BThighR,ws=True,m=getTransMatrix(0, getVector(ThighLocR, CalfLocR), 1, RLegSideV, ThighLocR))
				BCalfR = cmds.joint(name='B_Calf'+SN+'_R',p=CalfLocR, rad= 3.5)
				BoneList.append(BCalfR)
				cmds.xform(BCalfR,ws=True,m=getTransMatrix(0, getVector(CalfLocR, FootLocR), 1, RLegSideV, CalfLocR))
				BFootR = cmds.joint(name='B_Foot'+SN+'_R',p=FootLocR, rad= 3.5)
				BoneList.append(BFootR)
				cmds.xform(BFootR,ws=True,m=getTransMatrix(0, getVector(FootLocR, ToeLocR), 1, RLegSideV, FootLocR))
				BToeR = cmds.joint(name='B_Toe'+SN+'_R',p=ToeLocR, rad= 3.5)
				BoneList.append(BToeR)
				cmds.xform(BToeR,ws=True,m=getTransMatrix(0, getVector(ToeLocR, ToeELocR), 1, RLegSideV, ToeLocR))
				EndToeR = cmds.joint(name='end_Toe'+SN+'_R',p=ToeELocR, rad= 3.5)
				cmds.xform(EndToeR,ro=[0,0,0])

				cmds.select( Thigh_Parent )
				BThighL = cmds.joint(name='B_Thigh'+SN+'_L',p=ThighLocL, rad= 3.5)
				BoneList.append(BThighL)
				cmds.xform(BThighL,ws=True,m=getTransMatrix(0, getVector(ThighLocL, CalfLocL), 1, LLegSideV, ThighLocL))
				BCalfL = cmds.joint(name='B_Calf'+SN+'_L',p=CalfLocL, rad= 3.5)
				BoneList.append(BCalfL)
				cmds.xform(BCalfL,ws=True,m=getTransMatrix(0, getVector(CalfLocL, FootLocL), 1, LLegSideV, CalfLocL))
				BFootL = cmds.joint(name='B_Foot'+SN+'_L',p=FootLocL, rad= 3.5)
				BoneList.append(BFootL)
				cmds.xform(BFootL,ws=True,m=getTransMatrix(0, getVector(FootLocL, ToeLocL), 1, LLegSideV, FootLocL))
				BToeL = cmds.joint(name='B_Toe'+SN+'_L',p=ToeLocL, rad= 3.5)
				BoneList.append(BToeL)
				cmds.xform(BToeL,ws=True,m=getTransMatrix(0, getVector(ToeLocL, ToeELocL), 1, LLegSideV, ToeLocL))
				EndToeL = cmds.joint(name='end_Toe'+SN+'_L',p=ToeELocL, rad= 3.5)
				cmds.xform(EndToeL,ro=[0,0,0])

				#---
				cmds.select(BThighR)
				BButtBuffR = cmds.joint(name='B_ButtBuff'+SN+'_R',p=[0,0,0], rad= 4)
				BoneList.append(BButtBuffR)
				cmds.select(BThighR)
				BThighTwist1R = cmds.joint(name='B_Thigh'+SN+'Tw1_R',p=[0,0,0], rad= 4)
				BoneList.append(BThighTwist1R)
				cmds.select(BThighR)
				BThighTwist2R = cmds.joint(name='B_Thigh'+SN+'Tw2_R',p=[0,0,0], rad= 4)
				BoneList.append(BThighTwist2R)
				cmds.select(BCalfR)
				BKneeBuffR = cmds.joint(name='B_KneeBuff'+SN+'_R',p=[0,0,0], rad= 4)
				BoneList.append(BKneeBuffR)

				cmds.select(BThighL)
				BButtBuffL = cmds.joint(name='B_ButtBuff'+SN+'_L',p=[0,0,0], rad= 4)
				BoneList.append(BButtBuffL)
				cmds.select(BThighL)
				BThighTwist1L = cmds.joint(name='B_Thigh'+SN+'Tw1_L',p=[0,0,0], rad= 4)
				BoneList.append(BThighTwist1L)
				cmds.select(BThighL)
				BThighTwist2L = cmds.joint(name='B_Thigh'+SN+'Tw2_L',p=[0,0,0], rad= 4)
				BoneList.append(BThighTwist2L)
				cmds.select(BCalfL)
				BKneeBuffL = cmds.joint(name='B_KneeBuff'+SN+'_L',p=[0,0,0], rad= 4)
				BoneList.append(BKneeBuffL)

				#-----------------
				cmds.select( d=True )
				proxyThighJntR = cmds.joint(name='pyThighJnt'+SN+'_R',p=ThighLocR, rad= 6)
				HiddenList.append(proxyThighJntR)
				cmds.xform(proxyThighJntR,ws=True,m=getTransMatrix(0, getVector(ThighLocR, CalfLocR), 2, RLegUpV, ThighLocR))
				proxyCalfJntR = cmds.joint(name='pyCalfJnt'+SN+'_R',p=CalfLocR, rad= 6)
				HiddenList.append(proxyCalfJntR)
				cmds.xform(proxyCalfJntR,ws=True,m=getTransMatrix(0, getVector(CalfLocR, FootLocR), 2, RLegUpV, CalfLocR))
				proxyEndLegJntR = cmds.joint(name='pyEndLegJnt'+SN+'_R',p=FootLocR, rad= 6)
				HiddenList.append(proxyEndLegJntR)
				cmds.xform(proxyEndLegJntR, ro=[0,0,0])
				cmds.parent(proxyThighJntR, CtrlHip)
				proxyLegUpvR = cmds.spaceLocator(name='pyLegUpv'+SN+'_R')[0]
				HiddenList.append(proxyLegUpvR)
				cmds.xform(proxyLegUpvR ,ws=True, t=LegUpVPosR)
				cmds.parent(proxyLegUpvR, CtrlRoot)

				cmds.makeIdentity([proxyThighJntR,proxyCalfJntR,proxyEndLegJntR],apply=True, t=True, r=True,s=True,n=2,pn=True)

				LegIKHandleR = cmds.ikHandle(name='pyLegIKHandle'+SN+'R',sj=proxyThighJntR, ee=proxyEndLegJntR, sol="ikRPsolver")
				HiddenList.append(LegIKHandleR[0])
				cmds.poleVectorConstraint(proxyLegUpvR, LegIKHandleR[0], w=1)
				#--
				cmds.select( d=True )
				proxyThighJntL = cmds.joint(name='pyThighJnt'+SN+'_L',p=ThighLocL, rad= 6)
				HiddenList.append(proxyThighJntL)
				cmds.xform(proxyThighJntL,ws=True,m=getTransMatrix(0, getVector(ThighLocL, CalfLocL), 2, LLegUpV, ThighLocL))
				proxyCalfJntL = cmds.joint(name='pyCalfJnt'+SN+'_L',p=CalfLocL, rad= 6)
				HiddenList.append(proxyCalfJntL)
				cmds.xform(proxyCalfJntL,ws=True,m=getTransMatrix(0, getVector(CalfLocL, FootLocL), 2, LLegUpV, CalfLocL))
				proxyEndLegJntL = cmds.joint(name='pyEndLegJnt'+SN+'_L',p=FootLocL, rad= 6)
				HiddenList.append(proxyEndLegJntL)
				cmds.xform(proxyEndLegJntL, ro=[0,0,0])
				cmds.parent(proxyThighJntL, CtrlHip)
				proxyLegUpvL = cmds.spaceLocator(name='pyLegUpv'+SN+'_L')[0]
				HiddenList.append(proxyLegUpvL)
				cmds.xform(proxyLegUpvL ,ws=True, t=LegUpVPosL)
				cmds.parent(proxyLegUpvL, CtrlRoot)

				cmds.makeIdentity([proxyThighJntL,proxyCalfJntL,proxyEndLegJntL],apply=True, t=True, r=True,s=True,n=2,pn=True)

				LegIKHandleL = cmds.ikHandle(name='pyLegIKHandle'+SN+'L',sj=proxyThighJntL, ee=proxyEndLegJntL, sol="ikRPsolver")
				HiddenList.append(LegIKHandleL[0])
				cmds.poleVectorConstraint(proxyLegUpvL, LegIKHandleL[0], w=1)
				#---
				proxyThighRootR = cmds.spaceLocator(name='pyThighRoot'+SN+'_R')[0]
				HiddenList.append(proxyThighRootR)
				cmds.xform(proxyThighRootR,ws=True,m=getTransMatrix(0, HipDownDir, 2, HipFwDir, ThighLocR))
				cmds.parent(proxyThighRootR, CtrlThigh_Parent)
				proxyThighR = cmds.spaceLocator(name='pyThigh'+SN+'_R')[0]
				HiddenList.append(proxyThighR)
				cmds.xform(proxyThighR,ws=True,m=cmds.xform(BThighR,q=True,ws=True,m=True))
				cmds.parent(proxyThighR, proxyThighJntR)
				proxyCalfR = self.createWireBox('pyCalf'+SN+'_R', 6, 6, 6, [0,0,0], HelperColor1)
				HiddenList.append(proxyCalfR)
				cmds.xform(proxyCalfR,ws=True,m=cmds.xform(BCalfR,q=True,ws=True,m=True))
				cmds.parent(proxyCalfR, proxyCalfJntR)
				
				proxyThighTwis1R = self.createWireBox('pyThigh'+SN+'Twis1_R', 6, 6, 6, [0,0,0], HelperColor1)
				HiddenList.append(proxyThighTwis1R)
				cmds.xform(proxyThighTwis1R,ws=True,m=getTransMatrix(0, getVector(ThighLocR, CalfLocR), 2, HipFwDir, ThighLocR))
				cmds.parent(proxyThighTwis1R, proxyThighRootR)
				cmds.aimConstraint(proxyCalfJntR, proxyThighTwis1R, aim=[1,0,0], u=[0,0,1], wut="none")

				proxyThighTwis2R = self.createWireBox('pyThigh'+SN+'Twis2_R', 6, 6, 6, [0,0,0], HelperColor1)
				HiddenList.append(proxyThighTwis2R)
				cmds.parent(proxyThighTwis2R, proxyThighJntR)
				PC_TT2_R = cmds.pointConstraint(proxyThighTwis1R, proxyCalfJntR, proxyThighTwis2R)
				cmds.setAttr(PC_TT2_R[0] + "." + proxyThighTwis1R + "W0", 2)
				cmds.setAttr(PC_TT2_R[0] + "." + proxyCalfJntR + "W1", 1)
				RC_TT2_R = cmds.orientConstraint(proxyThighTwis1R, proxyThighR, proxyThighTwis2R, mo=False)
				cmds.setAttr(RC_TT2_R[0] + "." + proxyThighTwis1R + "W0", 1)
				cmds.setAttr(RC_TT2_R[0] + "." + proxyThighR + "W1", 1)
				cmds.setAttr(RC_TT2_R[0] + ".interpType", 2)

				proxyThighTwis3R = self.createWireBox('pyThigh'+SN+'Twis3_R', 6, 6, 6, [0,0,0], HelperColor1)
				HiddenList.append(proxyThighTwis3R)
				cmds.parent(proxyThighTwis3R, proxyThighJntR)
				PC_TT3_R = cmds.pointConstraint(proxyThighTwis1R, proxyCalfJntR, proxyThighTwis3R)
				cmds.setAttr(PC_TT3_R[0] + "." + proxyThighTwis1R + "W0", 1)
				cmds.setAttr(PC_TT3_R[0] + "." + proxyCalfJntR + "W1", 2)
				RC_TT3_R = cmds.orientConstraint(proxyThighR, proxyThighTwis3R, mo=False)
				#--
				proxyThighRootL = cmds.spaceLocator(name='pyThighRoot'+SN+'_L')[0]
				HiddenList.append(proxyThighRootL)
				cmds.xform(proxyThighRootL,ws=True,m=getTransMatrix(0, HipDownDir, 2, HipFwDir, ThighLocL))
				cmds.parent(proxyThighRootL, CtrlThigh_Parent)
				proxyThighL = cmds.spaceLocator(name='pyThigh'+SN+'_L')[0]
				HiddenList.append(proxyThighL)
				cmds.xform(proxyThighL,ws=True,m=cmds.xform(BThighL,q=True,ws=True,m=True))
				cmds.parent(proxyThighL, proxyThighJntL)
				proxyCalfL = self.createWireBox('pyCalf'+SN+'_L', 6, 6, 6, [0,0,0], HelperColor1)
				HiddenList.append(proxyCalfL)
				cmds.xform(proxyCalfL,ws=True,m=cmds.xform(BCalfL,q=True,ws=True,m=True))
				cmds.parent(proxyCalfL, proxyCalfJntL)
				
				proxyThighTwis1L = self.createWireBox('pyThigh'+SN+'Twis1_L', 6, 6, 6, [0,0,0], HelperColor1)
				HiddenList.append(proxyThighTwis1L)
				cmds.xform(proxyThighTwis1L,ws=True,m=getTransMatrix(0, getVector(ThighLocL, CalfLocL), 2, HipFwDir, ThighLocL))
				cmds.parent(proxyThighTwis1L, proxyThighRootL)
				cmds.aimConstraint(proxyCalfJntL, proxyThighTwis1L, aim=[1,0,0], u=[0,0,1], wut="none")

				proxyThighTwis2L = self.createWireBox('pyThigh'+SN+'Twis2_L', 6, 6, 6, [0,0,0], HelperColor1)
				HiddenList.append(proxyThighTwis2L)
				cmds.parent(proxyThighTwis2L, proxyThighJntL)
				PC_TT2_L = cmds.pointConstraint(proxyThighTwis1L, proxyCalfJntL, proxyThighTwis2L)
				cmds.setAttr(PC_TT2_L[0] + "." + proxyThighTwis1L + "W0", 2)
				cmds.setAttr(PC_TT2_L[0] + "." + proxyCalfJntL + "W1", 1)
				RC_TT2_L = cmds.orientConstraint(proxyThighTwis1L, proxyThighL, proxyThighTwis2L, mo=False)
				cmds.setAttr(RC_TT2_L[0] + "." + proxyThighTwis1L + "W0", 1)
				cmds.setAttr(RC_TT2_L[0] + "." + proxyThighL + "W1", 1)
				cmds.setAttr(RC_TT2_L[0] + ".interpType", 2)

				proxyThighTwis3L = self.createWireBox('pyThigh'+SN+'Twis3_L', 6, 6, 6, [0,0,0], HelperColor1)
				HiddenList.append(proxyThighTwis3L)
				cmds.parent(proxyThighTwis3L, proxyThighJntL)
				PC_TT3_L = cmds.pointConstraint(proxyThighTwis1L, proxyCalfJntL, proxyThighTwis3L)
				cmds.setAttr(PC_TT3_L[0] + "." + proxyThighTwis1L + "W0", 1)
				cmds.setAttr(PC_TT3_L[0] + "." + proxyCalfJntL + "W1", 2)
				RC_TT3_L = cmds.orientConstraint(proxyThighL, proxyThighTwis3L, mo=False)
				#---
				FootCtrlPosR = multiVec(sumVec(FootLocR,ToeELocR),[0.5,0,0.5])
				if bIsZUp:
					FootCtrlPosR = multiVec(sumVec(FootLocR,ToeELocR),[0.5,0.5,0])

				FootFwDirR = getVector(FootLocR, ToeELocR)
				if not bIsZUp:
					FootFwDirR = normalizeVec([FootFwDirR[0],0,FootFwDirR[2]])
				else:
					FootFwDirR = normalizeVec([FootFwDirR[0],FootFwDirR[1],0])

				FootTransR = cmds.xform(BFootR,q=True,ws=True,m=True)
				FootPadUpDirR = getRowFromMatrix(FootTransR, 2)
				ToeTransR = cmds.xform(BToeR,q=True,ws=True,m=True)
				ToeUpDirR = getRowFromMatrix(ToeTransR, 2)

				FootCtrlPosL = multiVec(FootCtrlPosR, [-1,1,1])
				FootFwDirL = multiVec(FootFwDirR, [-1,1,1])
				FootPadUpDirL = multiVec(FootPadUpDirR, [-1,1,1])
				ToeUpDirL = multiVec(ToeUpDirR, [-1,1,1])

				FOffset = [0,FootLength*0.07,0]
				if bIsZUp:
					FOffset = [0,0,FootLength*0.07]

				#---Leg Soft IK
				legSoftRange = cmds.shadingNode('multiplyDivide', n='legSoftRange'+SN, au=True)
				SNList.append(legSoftRange)
				cmds.connectAttr(CtrlRoot+'.SoftIkLeg', legSoftRange+'.input1X', f=True)
				cmds.setAttr(legSoftRange+'.input2X', 0.016)

				LegTmpLefLen = cmds.shadingNode('multiplyDivide', n='LegTmpLefLen'+SN, au=True)
				SNList.append(LegTmpLefLen)
				cmds.connectAttr(legSoftRange+'.outputX', LegTmpLefLen+'.input1X', f=True)
				cmds.setAttr(LegTmpLefLen+'.input2X', LegLength)

				LegLefLength = cmds.shadingNode('clamp', n='LegLefLength'+SN, au=True)
				SNList.append(LegLefLength)
				cmds.setAttr(LegLefLength+'.min', 0.0001,0.0001,0.0001,type='float3')
				cmds.setAttr(LegLefLength+'.max', LegLength,LegLength,LegLength,type='float3')
				cmds.connectAttr(LegTmpLefLen+'.outputX', LegLefLength+'.inputR', f=True)

				LegEndLength = cmds.shadingNode('plusMinusAverage', n='LegEndLength'+SN, au=True)
				SNList.append(LegEndLength)
				cmds.setAttr(LegEndLength+'.operation', 2)
				# mel.eval('AEnewNonNumericMultiAddNewItem("' + LegEndLength + '","input1D");')
				# mel.eval('AEnewNonNumericMultiAddNewItem("' + LegEndLength + '","input1D");')
				cmds.connectAttr(LegLefLength+'.outputR', LegEndLength+'.input1D[0]', f=True)
				cmds.connectAttr(LegLefLength+'.outputR', LegEndLength+'.input1D[1]', f=True)
				cmds.disconnectAttr(LegLefLength+'.outputR', LegEndLength+'.input1D[0]')
				cmds.setAttr(LegEndLength+'.input1D[0]', LegLength)

				#Right Leg
				CtrlLegIK_R = cmds.spaceLocator(n='CtrlLegIK'+SN+'_R')[0]
				HiddenList.append(CtrlLegIK_R)
				cmds.xform(CtrlLegIK_R,ws=True, t=FootLocR)

				LegAimer_R = cmds.spaceLocator(n='LegAimer'+SN+'_R')[0]
				HiddenList.append(LegAimer_R)
				cmds.parent(LegAimer_R, CtrlHip)
				cmds.xform(LegAimer_R, ws=True, t=ThighLocR)
				cmds.aimConstraint(CtrlLegIK_R, LegAimer_R, aim=[1,0,0], u=[0,1,0], wut="none")

				distLegIKCtrl_R = cmds.shadingNode('distanceBetween', n='distLegIKCtrl' + SN + '_R', au=True)
				SNList.append(distLegIKCtrl_R)
				cmds.connectAttr(cmds.listRelatives(LegAimer_R, s=True)[0]+'.worldPosition[0]', distLegIKCtrl_R+'.point1', f=True)
				cmds.connectAttr(cmds.listRelatives(CtrlLegIK_R, s=True)[0]+'.worldPosition[0]', distLegIKCtrl_R+'.point2', f=True)

				extraLegIKCtrl_R = cmds.shadingNode('plusMinusAverage', n='extraLegIKCtrl'+SN+'_R', au=True)
				SNList.append(extraLegIKCtrl_R)
				cmds.setAttr(extraLegIKCtrl_R+'.operation', 2)
				# mel.eval('AEnewNonNumericMultiAddNewItem("' + extraLegIKCtrl_R + '","input1D");')
				# mel.eval('AEnewNonNumericMultiAddNewItem("' + extraLegIKCtrl_R + '","input1D");')
				cmds.connectAttr(distLegIKCtrl_R+'.distance', extraLegIKCtrl_R+'.input1D[0]', f=True)
				cmds.connectAttr(LegEndLength+'.output1D', extraLegIKCtrl_R+'.input1D[1]', f=True)

				mappingExtLIKCtrl_R = cmds.shadingNode('multiplyDivide', n='mappingExtLIKCtrl'+SN+'_R', au=True)
				SNList.append(mappingExtLIKCtrl_R)
				cmds.setAttr(mappingExtLIKCtrl_R+'.operation', 2)
				cmds.connectAttr(extraLegIKCtrl_R+'.output1D', mappingExtLIKCtrl_R+'.input1X', f=True)
				cmds.connectAttr(LegLefLength+'.outputR', mappingExtLIKCtrl_R+'.input2X', f=True)

				invExtraLegIK_R = cmds.shadingNode('multiplyDivide', n='invExtraLegIK'+SN+'_R', au=True)
				SNList.append(invExtraLegIK_R)
				cmds.connectAttr(mappingExtLIKCtrl_R+'.outputX', invExtraLegIK_R+'.input1X', f=True)
				cmds.setAttr(invExtraLegIK_R+'.input2X', -1)

				expExtraLegIK_R = cmds.shadingNode('multiplyDivide', n='expExtraLegIK'+SN+'_R', au=True)
				SNList.append(expExtraLegIK_R)
				cmds.setAttr(expExtraLegIK_R+'.operation', 3)
				cmds.setAttr(expExtraLegIK_R+'.input1X', 2.71828182846)
				cmds.connectAttr(invExtraLegIK_R+'.outputX', expExtraLegIK_R+'.input2X', f=True)

				oneMinusExpLegIK_R = cmds.shadingNode('plusMinusAverage', n='oneMinusExpLegIK'+SN+'_R', au=True)
				SNList.append(oneMinusExpLegIK_R)
				cmds.setAttr(oneMinusExpLegIK_R+'.operation', 2)
				# mel.eval('AEnewNonNumericMultiAddNewItem("' + oneMinusExpLegIK_R + '","input1D");')
				# mel.eval('AEnewNonNumericMultiAddNewItem("' + oneMinusExpLegIK_R + '","input1D");')
				cmds.connectAttr(expExtraLegIK_R+'.outputX', oneMinusExpLegIK_R+'.input1D[0]', f=True)
				cmds.connectAttr(expExtraLegIK_R+'.outputX', oneMinusExpLegIK_R+'.input1D[1]', f=True)
				cmds.disconnectAttr(expExtraLegIK_R+'.outputX', oneMinusExpLegIK_R+'.input1D[0]')
				cmds.setAttr(oneMinusExpLegIK_R+'.input1D[0]', 1)

				clampOmExpLegIK_R = cmds.shadingNode('clamp', n='expExtraLegIK'+SN+'_R', au=True)
				SNList.append(clampOmExpLegIK_R)
				cmds.setAttr(clampOmExpLegIK_R+'.max', 1,1,1,type='float3')
				cmds.connectAttr(oneMinusExpLegIK_R+'.output1D', clampOmExpLegIK_R+'.inputR', f=True)

				softExtraDLegIK_R = cmds.shadingNode('multiplyDivide', n='softExtraDLegIK'+SN+'_R', au=True)
				SNList.append(softExtraDLegIK_R)
				cmds.setAttr(softExtraDLegIK_R+'.operation', 1)
				cmds.connectAttr(clampOmExpLegIK_R+'.outputR', softExtraDLegIK_R+'.input1X', f=True)
				cmds.connectAttr(LegLefLength+'.outputR', softExtraDLegIK_R+'.input2X', f=True)

				finalSoftLegIKDis_R = cmds.shadingNode('plusMinusAverage', n='finalSoftLegIKDis'+SN+'_R', au=True)
				SNList.append(finalSoftLegIKDis_R)
				cmds.connectAttr(softExtraDLegIK_R+'.outputX', finalSoftLegIKDis_R+'.input1D[0]', f=True)
				cmds.connectAttr(LegEndLength+'.output1D', finalSoftLegIKDis_R+'.input1D[1]', f=True)

				condiLegSoftIK_R = cmds.shadingNode('condition', n='condiLegSoftIK'+SN+'_R', au=True)
				SNList.append(condiLegSoftIK_R)
				cmds.connectAttr(distLegIKCtrl_R+'.distance', condiLegSoftIK_R+'.firstTerm')
				cmds.connectAttr(LegEndLength+'.output1D', condiLegSoftIK_R+'.secondTerm', f=True)
				cmds.setAttr(condiLegSoftIK_R+'.operation', 2)
				cmds.connectAttr(finalSoftLegIKDis_R+'.output1D', condiLegSoftIK_R+'.colorIfTrueR', f=True)
				cmds.connectAttr(distLegIKCtrl_R+'.distance', condiLegSoftIK_R+'.colorIfFalseR', f=True)

				LegSoftIK_R = cmds.spaceLocator(n='LegSoftIK'+SN+'_R')[0]
				HiddenList.append(LegSoftIK_R)
				cmds.parent(LegSoftIK_R, LegAimer_R)
				cmds.setAttr(LegSoftIK_R+'.translate',0,0,0,type='double3')
				cmds.setAttr(LegSoftIK_R+'.rotate',0,0,0,type='double3')
				cmds.connectAttr(condiLegSoftIK_R+'.outColorR',LegSoftIK_R+'.tx', f=True)

				#Left Leg
				CtrlLegIK_L = cmds.spaceLocator(n='CtrlLegIK'+SN+'_L')[0]
				HiddenList.append(CtrlLegIK_L)
				cmds.xform(CtrlLegIK_L,ws=True, t=FootLocL)

				LegAimer_L = cmds.spaceLocator(n='LegAimer'+SN+'_L')[0]
				HiddenList.append(LegAimer_L)
				cmds.parent(LegAimer_L, CtrlHip)
				cmds.xform(LegAimer_L, ws=True, t=ThighLocL)
				cmds.aimConstraint(CtrlLegIK_L, LegAimer_L, aim=[1,0,0], u=[0,1,0], wut="none")

				distLegIKCtrl_L = cmds.shadingNode('distanceBetween', n='distLegIKCtrl' + SN + '_L', au=True)
				SNList.append(distLegIKCtrl_L)
				cmds.connectAttr(cmds.listRelatives(LegAimer_L, s=True)[0]+'.worldPosition[0]', distLegIKCtrl_L+'.point1', f=True)
				cmds.connectAttr(cmds.listRelatives(CtrlLegIK_L, s=True)[0]+'.worldPosition[0]', distLegIKCtrl_L+'.point2', f=True)

				extraLegIKCtrl_L = cmds.shadingNode('plusMinusAverage', n='extraLegIKCtrl'+SN+'_L', au=True)
				SNList.append(extraLegIKCtrl_L)
				cmds.setAttr(extraLegIKCtrl_L+'.operation', 2)
				# mel.eval('AEnewNonNumericMultiAddNewItem("' + extraLegIKCtrl_L + '","input1D");')
				# mel.eval('AEnewNonNumericMultiAddNewItem("' + extraLegIKCtrl_L + '","input1D");')
				cmds.connectAttr(distLegIKCtrl_L+'.distance', extraLegIKCtrl_L+'.input1D[0]', f=True)
				cmds.connectAttr(LegEndLength+'.output1D', extraLegIKCtrl_L+'.input1D[1]', f=True)

				mappingExtLIKCtrl_L = cmds.shadingNode('multiplyDivide', n='mappingExtLIKCtrl'+SN+'_L', au=True)
				SNList.append(mappingExtLIKCtrl_L)
				cmds.setAttr(mappingExtLIKCtrl_L+'.operation', 2)
				cmds.connectAttr(extraLegIKCtrl_L+'.output1D', mappingExtLIKCtrl_L+'.input1X', f=True)
				cmds.connectAttr(LegLefLength+'.outputR', mappingExtLIKCtrl_L+'.input2X', f=True)

				invExtraLegIK_L = cmds.shadingNode('multiplyDivide', n='invExtraLegIK'+SN+'_L', au=True)
				SNList.append(invExtraLegIK_L)
				cmds.connectAttr(mappingExtLIKCtrl_L+'.outputX', invExtraLegIK_L+'.input1X', f=True)
				cmds.setAttr(invExtraLegIK_L+'.input2X', -1)

				expExtraLegIK_L = cmds.shadingNode('multiplyDivide', n='expExtraLegIK'+SN+'_L', au=True)
				SNList.append(expExtraLegIK_L)
				cmds.setAttr(expExtraLegIK_L+'.operation', 3)
				cmds.setAttr(expExtraLegIK_L+'.input1X', 2.71828182846)
				cmds.connectAttr(invExtraLegIK_L+'.outputX', expExtraLegIK_L+'.input2X', f=True)

				oneMinusExpLegIK_L = cmds.shadingNode('plusMinusAverage', n='oneMinusExpLegIK'+SN+'_L', au=True)
				SNList.append(oneMinusExpLegIK_L)
				cmds.setAttr(oneMinusExpLegIK_L+'.operation', 2)
				# mel.eval('AEnewNonNumericMultiAddNewItem("' + oneMinusExpLegIK_L + '","input1D");')
				# mel.eval('AEnewNonNumericMultiAddNewItem("' + oneMinusExpLegIK_L + '","input1D");')
				cmds.connectAttr(expExtraLegIK_L+'.outputX', oneMinusExpLegIK_L+'.input1D[0]', f=True)
				cmds.connectAttr(expExtraLegIK_L+'.outputX', oneMinusExpLegIK_L+'.input1D[1]', f=True)
				cmds.disconnectAttr(expExtraLegIK_L+'.outputX', oneMinusExpLegIK_L+'.input1D[0]')
				cmds.setAttr(oneMinusExpLegIK_L+'.input1D[0]', 1)

				clampOmExpLegIK_L = cmds.shadingNode('clamp', n='expExtraLegIK'+SN+'_L', au=True)
				SNList.append(clampOmExpLegIK_L)
				cmds.setAttr(clampOmExpLegIK_L+'.max', 1,1,1,type='float3')
				cmds.connectAttr(oneMinusExpLegIK_L+'.output1D', clampOmExpLegIK_L+'.inputR', f=True)

				softExtraDLegIK_L = cmds.shadingNode('multiplyDivide', n='softExtraDLegIK'+SN+'_L', au=True)
				SNList.append(softExtraDLegIK_L)
				cmds.setAttr(softExtraDLegIK_L+'.operation', 1)
				cmds.connectAttr(clampOmExpLegIK_L+'.outputR', softExtraDLegIK_L+'.input1X', f=True)
				cmds.connectAttr(LegLefLength+'.outputR', softExtraDLegIK_L+'.input2X', f=True)

				finalSoftLegIKDis_L = cmds.shadingNode('plusMinusAverage', n='finalSoftLegIKDis'+SN+'_L', au=True)
				SNList.append(finalSoftLegIKDis_L)
				cmds.connectAttr(softExtraDLegIK_L+'.outputX', finalSoftLegIKDis_L+'.input1D[0]', f=True)
				cmds.connectAttr(LegEndLength+'.output1D', finalSoftLegIKDis_L+'.input1D[1]', f=True)

				condiLegSoftIK_L = cmds.shadingNode('condition', n='condiLegSoftIK'+SN+'_L', au=True)
				SNList.append(condiLegSoftIK_L)
				cmds.connectAttr(distLegIKCtrl_L+'.distance', condiLegSoftIK_L+'.firstTerm')
				cmds.connectAttr(LegEndLength+'.output1D', condiLegSoftIK_L+'.secondTerm', f=True)
				cmds.setAttr(condiLegSoftIK_L+'.operation', 2)
				cmds.connectAttr(finalSoftLegIKDis_L+'.output1D', condiLegSoftIK_L+'.colorIfTrueR', f=True)
				cmds.connectAttr(distLegIKCtrl_L+'.distance', condiLegSoftIK_L+'.colorIfFalseR', f=True)

				LegSoftIK_L = cmds.spaceLocator(n='LegSoftIK'+SN+'_L')[0]
				HiddenList.append(LegSoftIK_L)
				cmds.parent(LegSoftIK_L, LegAimer_L)
				cmds.setAttr(LegSoftIK_L+'.translate',0,0,0,type='double3')
				cmds.setAttr(LegSoftIK_L+'.rotate',0,0,0,type='double3')
				cmds.connectAttr(condiLegSoftIK_L+'.outColorR',LegSoftIK_L+'.tx', f=True)
				# return
				#---
				CtrlFootR = self.createWireBox('Foot'+SN+'_R', FootLength*0.7, FootLength*1.4, FootLength*0.14, FOffset, Color_Ctrl3_R)
				CtrlList.append(CtrlFootR)
				ListNoScl.append(CtrlFootR)
				if not bIsZUp:
					cmds.xform(CtrlFootR,ws=True,m=getTransMatrix(2, FootFwDirR, 1, [0,1,0], FootCtrlPosR))
				else:
					cmds.xform(CtrlFootR,ws=True,m=getTransMatrix(1, invertVec(FootFwDirR), 2, [0,0,1], FootCtrlPosR))
				cmds.parent(CtrlFootR, CtrlRoot)

				if not bIsZUp:
					CtrlFootpadR = self.createWireSpherifyCrossArrow('Footpad'+SN+'_R', FootLength * 1.1, 60, 2, True, Color_Ctrl3_R)
					cmds.xform(CtrlFootpadR,ws=True,m=getTransMatrix(2, FootFwDirR, 1, FootPadUpDirR, ToeLocR))
				else:
					CtrlFootpadR = self.createWireSpherifyCrossArrow('Footpad'+SN+'_R', FootLength * 1.1, 60, 1, False, Color_Ctrl3_R)
					cmds.xform(CtrlFootpadR,ws=True,m=getTransMatrix(1, invertVec(FootFwDirR), 2, FootPadUpDirR, ToeLocR))
				CtrlList.append(CtrlFootpadR)
				ListOnlyRot.append(CtrlFootpadR)
				cmds.parent(CtrlFootpadR, CtrlFootR)

				lockPointFoot0R = cmds.spaceLocator(name='lpFoot'+SN+'0_R')[0]
				lockPointFoot1R = cmds.spaceLocator(name='lpFoot'+SN+'1_R')[0]
				lockPointFoot2R = cmds.spaceLocator(name='lpFoot'+SN+'2_R')[0]
				lockPointFoot3R = cmds.spaceLocator(name='lpFoot'+SN+'3_R')[0]
				lockPointFoot4R = cmds.spaceLocator(name='lpFoot'+SN+'4_R')[0]
				HiddenList.append(lockPointFoot0R)
				HiddenList.append(lockPointFoot1R)
				HiddenList.append(lockPointFoot2R)
				HiddenList.append(lockPointFoot3R)
				HiddenList.append(lockPointFoot4R)
				cmds.xform(lockPointFoot0R,ws=True,t=FootLocR)
				cmds.xform(lockPointFoot1R,ws=True,t=ToeLocR)
				cmds.xform(lockPointFoot2R,ws=True,t=ToeELocR)
				cmds.xform(lockPointFoot3R,ws=True,t=sumVec(FootLocR, invertVec(scaleVec(FootPadUpDirR, FootLength*0.4))))
				cmds.xform(lockPointFoot4R,ws=True,t=sumVec(ToeLocR, invertVec(scaleVec(ToeUpDirR, FootLength*0.4))))
				cmds.parent(lockPointFoot0R, CtrlFootpadR)
				cmds.parent(lockPointFoot3R, CtrlFootpadR)
				cmds.parent([lockPointFoot1R,lockPointFoot2R,lockPointFoot4R], CtrlFootR)
				# cmds.parent(LegIKHandleR[0], CtrlFootpadR)
				cmds.parent(CtrlLegIK_R, CtrlFootpadR)
				cmds.parent(LegIKHandleR[0], LegSoftIK_R)

				# proxyLegDirector_R = cmds.spaceLocator(name='pyLegDirector'+SN+'_R')[0]
				# HiddenList.append(proxyLegDirector_R)
				# cmds.xform(proxyLegDirector_R,ws=True,m=getTransMatrix(0, getVector(ThighLocR, FootLocR), 2, HipFwDir, ThighLocR))
				# cmds.parent(proxyLegDirector_R, proxyThighRootR)
				# cmds.aimConstraint(lockPointFoot0R, proxyLegDirector_R, aim=[1,0,0], u=[0,1,0], wut="objectrotation", wuo=CtrlFootR, wu=[1,0,0])

				# lockPointLegUpvR = cmds.spaceLocator(name='lpLegUpv'+SN+'_R')[0]
				# HiddenList.append(lockPointLegUpvR)
				# cmds.xform(lockPointLegUpvR,ws=True,t=LegUpVPosR)
				# cmds.parent(lockPointLegUpvR, proxyLegDirector_R)

				cmds.select(proxyEndLegJntR)
				proxyFootJntR = cmds.joint(name='pyFootJnt'+SN+'_R',p=FootLocR, rad= 4.5)
				HiddenList.append(proxyFootJntR)
				cmds.xform(proxyFootJntR,ws=True,m=cmds.xform(BFootR,q=True,ws=True,m=True))
				proxyToeJntR = cmds.joint(name='pyToeJnt'+SN+'_R',p=ToeLocR, rad= 4.5)
				HiddenList.append(proxyToeJntR)
				cmds.xform(proxyToeJntR,ws=True,m=cmds.xform(BToeR,q=True,ws=True,m=True))
				proxyToeEJntR = cmds.joint(name='pyToeEJnt'+SN+'_R',p=ToeELocR, rad= 4.5)
				HiddenList.append(proxyToeEJntR)
				cmds.xform(proxyToeEJntR,ws=True,m=cmds.xform(EndToeR,q=True,ws=True,m=True))

				cmds.aimConstraint(lockPointFoot1R, proxyFootJntR, aim=[1,0,0], u=[0,0,-1], wut="object", wuo=lockPointFoot3R)
				cmds.aimConstraint(lockPointFoot2R, proxyToeJntR, aim=[1,0,0], u=[0,0,-1], wut="object", wuo=lockPointFoot4R)

				# rootLegUpvR = cmds.group(em=True, name='rootLegUpv'+SN+'_R')
				# cmds.parent(rootLegUpvR, CtrlRoot)
				# cmds.pointConstraint(lockPointLegUpvR, rootLegUpvR)
				CtrlLegUpvR = self.createWireSphere('LegUpV'+SN+'_R', 5, Color_Ctrl4_R, LegUpVPosR)
				CtrlList.append(CtrlLegUpvR)
				ListOnlyPos.append(CtrlLegUpvR)
				# cmds.parent(CtrlLegUpvR, rootLegUpvR)
				cmds.parent(CtrlLegUpvR, CtrlRoot)
				cmds.parent(proxyLegUpvR, CtrlLegUpvR)
				#---
				CtrlFootL = self.createWireBox('Foot'+SN+'_L', FootLength*0.7, FootLength*1.4, FootLength*0.14, FOffset, Color_Ctrl3_L)
				CtrlList.append(CtrlFootL)
				ListNoScl.append(CtrlFootL)
				if not bIsZUp:
					cmds.xform(CtrlFootL,ws=True,m=getTransMatrix(2, FootFwDirL, 1, [0,1,0], FootCtrlPosL))
				else:
					cmds.xform(CtrlFootL,ws=True,m=getTransMatrix(1, invertVec(FootFwDirL), 2, [0,0,1], FootCtrlPosL))
				cmds.parent(CtrlFootL, CtrlRoot)

				if not bIsZUp:
					CtrlFootpadL = self.createWireSpherifyCrossArrow('Footpad'+SN+'_L', FootLength * 1.1, 60, 2, True, Color_Ctrl3_L)
					cmds.xform(CtrlFootpadL,ws=True,m=getTransMatrix(2, FootFwDirL, 1, FootPadUpDirL, ToeLocL))
				else:
					CtrlFootpadL = self.createWireSpherifyCrossArrow('Footpad'+SN+'_L', FootLength * 1.1, 60, 1, False, Color_Ctrl3_L)
					cmds.xform(CtrlFootpadL,ws=True,m=getTransMatrix(1, invertVec(FootFwDirL), 2, FootPadUpDirL, ToeLocL))
				CtrlList.append(CtrlFootpadL)
				ListOnlyRot.append(CtrlFootpadL)
				cmds.parent(CtrlFootpadL, CtrlFootL)

				lockPointFoot0L = cmds.spaceLocator(name='lpFoot'+SN+'0_L')[0]
				lockPointFoot1L = cmds.spaceLocator(name='lpFoot'+SN+'1_L')[0]
				lockPointFoot2L = cmds.spaceLocator(name='lpFoot'+SN+'2_L')[0]
				lockPointFoot3L = cmds.spaceLocator(name='lpFoot'+SN+'3_L')[0]
				lockPointFoot4L = cmds.spaceLocator(name='lpFoot'+SN+'4_L')[0]
				HiddenList.append(lockPointFoot0L)
				HiddenList.append(lockPointFoot1L)
				HiddenList.append(lockPointFoot2L)
				HiddenList.append(lockPointFoot3L)
				HiddenList.append(lockPointFoot4L)
				cmds.xform(lockPointFoot0L,ws=True,t=FootLocL)
				cmds.xform(lockPointFoot1L,ws=True,t=ToeLocL)
				cmds.xform(lockPointFoot2L,ws=True,t=ToeELocL)
				cmds.xform(lockPointFoot3L,ws=True,t=sumVec(FootLocL, invertVec(scaleVec(FootPadUpDirL, FootLength*0.4))))
				cmds.xform(lockPointFoot4L,ws=True,t=sumVec(ToeLocL, invertVec(scaleVec(ToeUpDirL, FootLength*0.4))))
				cmds.parent(lockPointFoot0L, CtrlFootpadL)
				cmds.parent(lockPointFoot3L, CtrlFootpadL)
				cmds.parent([lockPointFoot1L,lockPointFoot2L,lockPointFoot4L], CtrlFootL)
				# cmds.parent(LegIKHandleL[0], CtrlFootpadL)
				cmds.parent(CtrlLegIK_L, CtrlFootpadL)
				cmds.parent(LegIKHandleL[0], LegSoftIK_L)

				# proxyLegDirector_L = cmds.spaceLocator(name='pyLegDirector'+SN+'_L')[0]
				# HiddenList.append(proxyLegDirector_L)
				# cmds.xform(proxyLegDirector_L,ws=True,m=getTransMatrix(0, getVector(ThighLocL, FootLocL), 2, HipFwDir, ThighLocL))
				# cmds.parent(proxyLegDirector_L, proxyThighRootL)
				# cmds.aimConstraint(lockPointFoot0L, proxyLegDirector_L, aim=[1,0,0], u=[0,1,0], wut="objectrotation", wuo=CtrlFootL, wu=[1,0,0])

				# lockPointLegUpvL = cmds.spaceLocator(name='lpLegUpv'+SN+'_L')[0]
				# HiddenList.append(lockPointLegUpvL)
				# cmds.xform(lockPointLegUpvL,ws=True,t=LegUpVPosL)
				# cmds.parent(lockPointLegUpvL, proxyLegDirector_L)

				cmds.select(proxyEndLegJntL)
				proxyFootJntL = cmds.joint(name='pyFootJnt'+SN+'_L',p=FootLocL, rad= 4.5)
				HiddenList.append(proxyFootJntL)
				cmds.xform(proxyFootJntL,ws=True,m=cmds.xform(BFootL,q=True,ws=True,m=True))
				proxyToeJntL = cmds.joint(name='pyToeJnt'+SN+'_L',p=ToeLocL, rad= 4.5)
				HiddenList.append(proxyToeJntL)
				cmds.xform(proxyToeJntL,ws=True,m=cmds.xform(BToeL,q=True,ws=True,m=True))
				proxyToeEJntL = cmds.joint(name='pyToeEJnt'+SN+'_L',p=ToeELocL, rad= 4.5)
				HiddenList.append(proxyToeEJntL)
				cmds.xform(proxyToeEJntL,ws=True,m=cmds.xform(EndToeL,q=True,ws=True,m=True))

				cmds.aimConstraint(lockPointFoot1L, proxyFootJntL, aim=[1,0,0], u=[0,0,-1], wut="object", wuo=lockPointFoot3L)
				cmds.aimConstraint(lockPointFoot2L, proxyToeJntL, aim=[1,0,0], u=[0,0,-1], wut="object", wuo=lockPointFoot4L)

				# rootLegUpvL = cmds.group(em=True, name='rootLegUpv'+SN+'_L')
				# cmds.parent(rootLegUpvL, CtrlRoot)
				# cmds.pointConstraint(lockPointLegUpvL, rootLegUpvL)
				CtrlLegUpvL = self.createWireSphere('LegUpV'+SN+'_L', 5, Color_Ctrl4_L, LegUpVPosL)
				CtrlList.append(CtrlLegUpvL)
				ListOnlyPos.append(CtrlLegUpvL)
				# cmds.parent(CtrlLegUpvL, rootLegUpvL)
				cmds.parent(CtrlLegUpvL, CtrlRoot)
				cmds.parent(proxyLegUpvL, CtrlLegUpvL)
				#----------------------
				ProxyKneeBuffR = self.createWireBox('pyKneeBuff'+SN+'_R', 2, 5, 5,[0,0,0])
				HiddenList.append(ProxyKneeBuffR)
				cmds.parent(ProxyKneeBuffR, proxyCalfJntR)
				cmds.xform(ProxyKneeBuffR,ws=False, t=[-0.1,0,0])
				PKBROC = cmds.orientConstraint(proxyThighJntR,proxyCalfJntR,ProxyKneeBuffR,mo=False)
				cmds.setAttr(PKBROC[0] + ".interpType", 2)

				LegAngleD180_R = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(LegAngleD180_R)
				cmds.setAttr(LegAngleD180_R+".operation",2)
				cmds.connectAttr(proxyCalfJntR + ".ry", LegAngleD180_R+".input1X",f=True)
				cmds.setAttr(LegAngleD180_R+".input2X",180)

				LegAngleP2_R = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(LegAngleP2_R)
				cmds.connectAttr(LegAngleD180_R + ".outputX", LegAngleP2_R+".input1X",f=True)
				cmds.connectAttr(LegAngleD180_R + ".outputX", LegAngleP2_R+".input2X",f=True)

				LegAngleXV_R = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(LegAngleXV_R)
				cmds.connectAttr(LegAngleP2_R + ".outputX", LegAngleXV_R+".input1X",f=True)
				cmds.setAttr(LegAngleXV_R+".input2X",1.7)
				
				LegAngleP1_R = cmds.shadingNode("plusMinusAverage",au=True)
				SNList.append(LegAngleP1_R)
				cmds.connectAttr(LegAngleXV_R + ".outputX", LegAngleP1_R+".input1D[0]",f=True)
				cmds.connectAttr(LegAngleXV_R + ".outputX", LegAngleP1_R+".input1D[1]",f=True)
				cmds.disconnectAttr(LegAngleXV_R + ".outputX", LegAngleP1_R+".input1D[0]")
				cmds.setAttr(LegAngleP1_R+".input1D[0]",1)
				
				cmds.connectAttr(LegAngleP1_R + ".output1D", ProxyKneeBuffR+".sz",f=True)
				#---
				ProxyKneeBuffL = self.createWireBox('pyKneeBuff'+SN+'_L', 2, 5, 5,[0,0,0])
				HiddenList.append(ProxyKneeBuffL)
				cmds.parent(ProxyKneeBuffL, proxyCalfJntL)
				cmds.xform(ProxyKneeBuffL,ws=False, t=[-0.1,0,0])
				PKBROC = cmds.orientConstraint(proxyThighJntL,proxyCalfJntL,ProxyKneeBuffL,mo=False)
				cmds.setAttr(PKBROC[0] + ".interpType", 2)

				LegAngleD180_L = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(LegAngleD180_L)
				cmds.setAttr(LegAngleD180_L+".operation",2)
				cmds.connectAttr(proxyCalfJntL + ".ry", LegAngleD180_L+".input1X",f=True)
				cmds.setAttr(LegAngleD180_L+".input2X",180)

				LegAngleP2_L = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(LegAngleP2_L)
				cmds.connectAttr(LegAngleD180_L + ".outputX", LegAngleP2_L+".input1X",f=True)
				cmds.connectAttr(LegAngleD180_L + ".outputX", LegAngleP2_L+".input2X",f=True)

				LegAngleXV_L = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(LegAngleXV_L)
				cmds.connectAttr(LegAngleP2_L + ".outputX", LegAngleXV_L+".input1X",f=True)
				cmds.setAttr(LegAngleXV_L+".input2X",1.7)
				
				LegAngleP1_L = cmds.shadingNode("plusMinusAverage",au=True)
				SNList.append(LegAngleP1_L)
				cmds.connectAttr(LegAngleXV_L + ".outputX", LegAngleP1_L+".input1D[0]",f=True)
				cmds.connectAttr(LegAngleXV_L + ".outputX", LegAngleP1_L+".input1D[1]",f=True)
				cmds.disconnectAttr(LegAngleXV_L + ".outputX", LegAngleP1_L+".input1D[0]")
				cmds.setAttr(LegAngleP1_L+".input1D[0]",1)
				
				cmds.connectAttr(LegAngleP1_L + ".output1D", ProxyKneeBuffL+".sz",f=True)
				#-----------
				proxyButtBuffR = self.createWireBox('pyButtBuff'+SN+'_R', 4, 8, 8,[0,0,0])
				HiddenList.append(proxyButtBuffR)
				cmds.parent(proxyButtBuffR, proxyThighTwis1R)
				cmds.xform(proxyButtBuffR,ws=False, t=[-0.1,0,0])
				PBBROC = cmds.orientConstraint(proxyThighRootR,proxyThighTwis1R,proxyButtBuffR,mo=False)
				cmds.setAttr(PBBROC[0] + ".interpType", 2)

				ThighXAxis_R = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(ThighXAxis_R)
				cmds.setAttr(ThighXAxis_R+".operation",3)
				cmds.setAttr(ThighXAxis_R+".input1",1,0,0,type="float3")
				cmds.connectAttr(proxyThighTwis1R + ".worldMatrix[0]", ThighXAxis_R+".matrix",f=True)
				
				HipXAxis_R = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(HipXAxis_R)
				cmds.setAttr(HipXAxis_R+".operation",3)
				cmds.setAttr(HipXAxis_R+".input1",1,0,0,type="float3")
				cmds.connectAttr(proxyThighRootR + ".worldMatrix[0]", HipXAxis_R+".matrix",f=True)
				
				HipYAxis_R = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(HipYAxis_R)
				cmds.setAttr(HipYAxis_R+".operation",3)
				cmds.setAttr(HipYAxis_R+".input1",0,1,0,type="float3")
				cmds.connectAttr(proxyThighRootR + ".worldMatrix[0]", HipYAxis_R+".matrix",f=True)
				
				HipZAxis_R = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(HipZAxis_R)
				cmds.setAttr(HipZAxis_R+".operation",3)
				cmds.setAttr(HipZAxis_R+".input1",0,0,1,type="float3")
				cmds.connectAttr(proxyThighRootR + ".worldMatrix[0]", HipZAxis_R+".matrix",f=True)
				
				ThighXXDot_R = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(ThighXXDot_R)
				cmds.setAttr(ThighXXDot_R+".operation",1)
				cmds.connectAttr(ThighXAxis_R + ".output", ThighXXDot_R+".input1",f=True)
				cmds.connectAttr(HipXAxis_R + ".output", ThighXXDot_R+".input2",f=True)
				
				ThighXYDot_R = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(ThighXYDot_R)
				cmds.setAttr(ThighXXDot_R+".operation",1)
				cmds.connectAttr(ThighXAxis_R + ".output", ThighXYDot_R+".input1",f=True)
				cmds.connectAttr(HipYAxis_R + ".output", ThighXYDot_R+".input2",f=True)
				
				ThighXZDot_R = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(ThighXZDot_R)
				cmds.setAttr(ThighXXDot_R+".operation",1)
				cmds.connectAttr(ThighXAxis_R + ".output", ThighXZDot_R+".input1",f=True)
				cmds.connectAttr(HipZAxis_R + ".output", ThighXZDot_R+".input2",f=True)
				
				ThighXYZDotP2_R = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(ThighXYZDotP2_R)
				cmds.connectAttr(ThighXYDot_R + ".outputX", ThighXYZDotP2_R+".input1X",f=True)
				cmds.connectAttr(ThighXYDot_R + ".outputX", ThighXYZDotP2_R+".input2X",f=True)
				cmds.connectAttr(ThighXZDot_R + ".outputX", ThighXYZDotP2_R+".input1Y",f=True)
				cmds.connectAttr(ThighXZDot_R + ".outputX", ThighXYZDotP2_R+".input2Y",f=True)
				
				ThighXYZDotSqrt_R = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(ThighXYZDotSqrt_R)
				cmds.setAttr(ThighXXDot_R+".operation",3)
				cmds.connectAttr(ThighXYZDotP2_R + ".outputX", ThighXYZDotSqrt_R+".input1X",f=True)
				cmds.connectAttr(ThighXYZDotP2_R + ".outputY", ThighXYZDotSqrt_R+".input1Y",f=True)
				cmds.setAttr(ThighXYZDotSqrt_R+".input2",0.5,0.5,1,type="float3")
				
				ScaleThighDot_R = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(ScaleThighDot_R)
				cmds.connectAttr(ThighXXDot_R + ".outputX", ScaleThighDot_R+".input1X",f=True)
				cmds.setAttr(ScaleThighDot_R+".input2X",-0.5)
				
				OffsetThighDot_R = cmds.shadingNode("plusMinusAverage",au=True)
				SNList.append(OffsetThighDot_R)
				cmds.connectAttr(ScaleThighDot_R + ".outputX", OffsetThighDot_R+".input1D[0]",f=True)
				cmds.connectAttr(ScaleThighDot_R + ".outputX", OffsetThighDot_R+".input1D[1]",f=True)
				cmds.disconnectAttr(ScaleThighDot_R + ".outputX", OffsetThighDot_R+".input1D[0]")
				cmds.setAttr(OffsetThighDot_R+".input1D[0]",0.7)
				
				ScaleButt_R = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(ScaleButt_R)
				cmds.connectAttr(OffsetThighDot_R + ".output1D", ScaleButt_R+".input1X",f=True)
				cmds.connectAttr(ThighXYZDotSqrt_R + ".outputX", ScaleButt_R+".input2X",f=True)
				cmds.connectAttr(OffsetThighDot_R + ".output1D", ScaleButt_R+".input1Y",f=True)
				cmds.connectAttr(ThighXYZDotSqrt_R + ".outputY", ScaleButt_R+".input2Y",f=True)
				
				OffsetScaleButt_R = cmds.shadingNode("plusMinusAverage",au=True)
				SNList.append(OffsetScaleButt_R)
				cmds.connectAttr(ScaleButt_R + ".outputX", OffsetScaleButt_R+".input2D[0].input2Dx",f=True)
				cmds.connectAttr(ScaleButt_R + ".outputX", OffsetScaleButt_R+".input2D[1].input2Dx",f=True)
				cmds.disconnectAttr(ScaleButt_R + ".outputX", OffsetScaleButt_R+".input2D[0].input2Dx")
				cmds.connectAttr(ScaleButt_R + ".outputY", OffsetScaleButt_R+".input2D[1].input2Dy",f=True)
				cmds.setAttr(OffsetScaleButt_R+".input2D[0].input2Dx",1)
				cmds.setAttr(OffsetScaleButt_R+".input2D[0].input2Dy",1)
				
				cmds.connectAttr(OffsetScaleButt_R + ".output2Dx", proxyButtBuffR+".sy",f=True)
				cmds.connectAttr(OffsetScaleButt_R + ".output2Dy", proxyButtBuffR+".sz",f=True)
				#---
				proxyButtBuffL = self.createWireBox('pyButtBuff'+SN+'_L', 4, 8, 8,[0,0,0])
				HiddenList.append(proxyButtBuffL)
				cmds.parent(proxyButtBuffL, proxyThighTwis1L)
				cmds.xform(proxyButtBuffL,ws=False, t=[-0.1,0,0])
				PBBLOC = cmds.orientConstraint(proxyThighRootL,proxyThighTwis1L,proxyButtBuffL,mo=False)
				cmds.setAttr(PBBLOC[0] + ".interpType", 2)

				ThighXAxis_L = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(ThighXAxis_L)
				cmds.setAttr(ThighXAxis_L+".operation",3)
				cmds.setAttr(ThighXAxis_L+".input1",1,0,0,type="float3")
				cmds.connectAttr(proxyThighTwis1L + ".worldMatrix[0]", ThighXAxis_L+".matrix",f=True)
				
				HipXAxis_L = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(HipXAxis_L)
				cmds.setAttr(HipXAxis_L+".operation",3)
				cmds.setAttr(HipXAxis_L+".input1",1,0,0,type="float3")
				cmds.connectAttr(proxyThighRootL + ".worldMatrix[0]", HipXAxis_L+".matrix",f=True)
				
				HipYAxis_L = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(HipYAxis_L)
				cmds.setAttr(HipYAxis_L+".operation",3)
				cmds.setAttr(HipYAxis_L+".input1",0,1,0,type="float3")
				cmds.connectAttr(proxyThighRootL + ".worldMatrix[0]", HipYAxis_L+".matrix",f=True)
				
				HipZAxis_L = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(HipZAxis_L)
				cmds.setAttr(HipZAxis_L+".operation",3)
				cmds.setAttr(HipZAxis_L+".input1",0,0,1,type="float3")
				cmds.connectAttr(proxyThighRootL + ".worldMatrix[0]", HipZAxis_L+".matrix",f=True)
				
				ThighXXDot_L = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(ThighXXDot_L)
				cmds.setAttr(ThighXXDot_L+".operation",1)
				cmds.connectAttr(ThighXAxis_L + ".output", ThighXXDot_L+".input1",f=True)
				cmds.connectAttr(HipXAxis_L + ".output", ThighXXDot_L+".input2",f=True)
				
				ThighXYDot_L = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(ThighXYDot_L)
				cmds.setAttr(ThighXXDot_L+".operation",1)
				cmds.connectAttr(ThighXAxis_L + ".output", ThighXYDot_L+".input1",f=True)
				cmds.connectAttr(HipYAxis_L + ".output", ThighXYDot_L+".input2",f=True)
				
				ThighXZDot_L = cmds.shadingNode("vectorProduct",au=True)
				SNList.append(ThighXZDot_L)
				cmds.setAttr(ThighXXDot_L+".operation",1)
				cmds.connectAttr(ThighXAxis_L + ".output", ThighXZDot_L+".input1",f=True)
				cmds.connectAttr(HipZAxis_L + ".output", ThighXZDot_L+".input2",f=True)
				
				ThighXYZDotP2_L = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(ThighXYZDotP2_L)
				cmds.connectAttr(ThighXYDot_L + ".outputX", ThighXYZDotP2_L+".input1X",f=True)
				cmds.connectAttr(ThighXYDot_L + ".outputX", ThighXYZDotP2_L+".input2X",f=True)
				cmds.connectAttr(ThighXZDot_L + ".outputX", ThighXYZDotP2_L+".input1Y",f=True)
				cmds.connectAttr(ThighXZDot_L + ".outputX", ThighXYZDotP2_L+".input2Y",f=True)
				
				ThighXYZDotSqrt_L = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(ThighXYZDotSqrt_L)
				cmds.setAttr(ThighXXDot_L+".operation",3)
				cmds.connectAttr(ThighXYZDotP2_L + ".outputX", ThighXYZDotSqrt_L+".input1X",f=True)
				cmds.connectAttr(ThighXYZDotP2_L + ".outputY", ThighXYZDotSqrt_L+".input1Y",f=True)
				cmds.setAttr(ThighXYZDotSqrt_L+".input2",0.5,0.5,1,type="float3")
				
				ScaleThighDot_L = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(ScaleThighDot_L)
				cmds.connectAttr(ThighXXDot_L + ".outputX", ScaleThighDot_L+".input1X",f=True)
				cmds.setAttr(ScaleThighDot_L+".input2X",-0.5)
				
				OffsetThighDot_L = cmds.shadingNode("plusMinusAverage",au=True)
				SNList.append(OffsetThighDot_L)
				cmds.connectAttr(ScaleThighDot_L + ".outputX", OffsetThighDot_L+".input1D[0]",f=True)
				cmds.connectAttr(ScaleThighDot_L + ".outputX", OffsetThighDot_L+".input1D[1]",f=True)
				cmds.disconnectAttr(ScaleThighDot_L + ".outputX", OffsetThighDot_L+".input1D[0]")
				cmds.setAttr(OffsetThighDot_L+".input1D[0]",0.7)
				
				ScaleButt_L = cmds.shadingNode("multiplyDivide",au=True)
				SNList.append(ScaleButt_L)
				cmds.connectAttr(OffsetThighDot_L + ".output1D", ScaleButt_L+".input1X",f=True)
				cmds.connectAttr(ThighXYZDotSqrt_L + ".outputX", ScaleButt_L+".input2X",f=True)
				cmds.connectAttr(OffsetThighDot_L + ".output1D", ScaleButt_L+".input1Y",f=True)
				cmds.connectAttr(ThighXYZDotSqrt_L + ".outputY", ScaleButt_L+".input2Y",f=True)
				
				OffsetScaleButt_L = cmds.shadingNode("plusMinusAverage",au=True)
				SNList.append(OffsetScaleButt_L)
				cmds.connectAttr(ScaleButt_L + ".outputX", OffsetScaleButt_L+".input2D[0].input2Dx",f=True)
				cmds.connectAttr(ScaleButt_L + ".outputX", OffsetScaleButt_L+".input2D[1].input2Dx",f=True)
				cmds.disconnectAttr(ScaleButt_L + ".outputX", OffsetScaleButt_L+".input2D[0].input2Dx")
				cmds.connectAttr(ScaleButt_L + ".outputY", OffsetScaleButt_L+".input2D[1].input2Dy",f=True)
				cmds.setAttr(OffsetScaleButt_L+".input2D[0].input2Dx",1)
				cmds.setAttr(OffsetScaleButt_L+".input2D[0].input2Dy",1)
				
				cmds.connectAttr(OffsetScaleButt_L + ".output2Dx", proxyButtBuffL+".sy",f=True)
				cmds.connectAttr(OffsetScaleButt_L + ".output2Dy", proxyButtBuffL+".sz",f=True)

				#----------Constrain to Bone joint-----
				BoneConstraintList.append(cmds.parentConstraint(proxyThighTwis1R, BThighR, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyThighTwis1L, BThighL, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyCalfR, BCalfR, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyCalfL, BCalfL, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyFootJntR, BFootR, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyFootJntL, BFootL, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyToeJntR, BToeR, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyToeJntL, BToeL, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyButtBuffR, BButtBuffR, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyButtBuffL, BButtBuffL, mo=False)[0])
				BoneConstraintList.append(cmds.scaleConstraint(proxyButtBuffR, BButtBuffR, mo=False)[0])
				BoneConstraintList.append(cmds.scaleConstraint(proxyButtBuffL, BButtBuffL, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyThighTwis2R, BThighTwist1R, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyThighTwis3R, BThighTwist2R, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyThighTwis2L, BThighTwist1L, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(proxyThighTwis3L, BThighTwist2L, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(ProxyKneeBuffR, BKneeBuffR, mo=False)[0])
				BoneConstraintList.append(cmds.parentConstraint(ProxyKneeBuffL, BKneeBuffL, mo=False)[0])
				BoneConstraintList.append(cmds.scaleConstraint(ProxyKneeBuffR, BKneeBuffR, mo=False)[0])
				BoneConstraintList.append(cmds.scaleConstraint(ProxyKneeBuffL, BKneeBuffL, mo=False)[0])

			# return
			#======


			ConstSys = cmds.createNode('transform',n='ConstraintSys')
			cmds.parent(ConstSys, CtrlRoot)
			cmds.parent(BoneConstraintList, ConstSys)
			# return
			#====== Create Select Set =======
			cmds.select( d=True )

			CtrlItemsGroup = cmds.createNode('transform',n='CtrlItems')
			cmds.parent(CtrlItemsGroup, CtrlRoot)
			cmds.parent(MidItemList, CtrlItemsGroup)
			# return
			HiddenSet = cmds.sets(HiddenList, n="HiddenSet")
			SNSet = cmds.sets(SNList, n="SNSet")
			HiddenLayer = cmds.createDisplayLayer(name="Hidden")
			cmds.editDisplayLayerMembers( HiddenLayer, HiddenList)
			cmds.setAttr(HiddenLayer + ".visibility", 0)
			cmds.setAttr(HiddenLayer + ".hideOnPlayback", 1)

			cmds.select( d=True )
			ControlLayer = cmds.createDisplayLayer(name="Controller")
			cmds.editDisplayLayerMembers( ControlLayer, CtrlList, noRecurse=True)

			BoneSet = cmds.sets(BoneList, n="SkinBoneSet")
			CtrlSet = cmds.sets(CtrlList, n="ControllerSet")

			#Sets all sets
			cmds.sets([HiddenSet, SNSet, BoneSet, CtrlSet], n='Sets')
			# return
			#================================
			self.disableControl(ListNoScl,0,0,1)
			self.disableControl(ListOnlyRot,1,0,1)
			self.disableControl(ListOnlyPos,0,1,1)
			#================================
			self.assignSkinPoseInfo(CtrlList)
			self.storeSkinPose(CtrlList)
			
			#set mirror info
			self.assignMirrorInfo(CtrlList)
			self.setMirrorInfo(CtrlList)
			# if bIsZUp:
			# 	cmds.setAttr(ctrlUpperArmFK_R+".InvPosX", 0)
			# 	cmds.setAttr(ctrlUpperArmFK_R+".InvPosY", 0)
			# 	cmds.setAttr(ctrlUpperArmFK_R+".InvPosZ", 1)
			# 	cmds.setAttr(ctrlUpperArmFK_R+".InvRotX", 1)
			# 	cmds.setAttr(ctrlUpperArmFK_R+".InvRotY", 1)
			# 	cmds.setAttr(ctrlUpperArmFK_R+".InvRotZ", 0)
			# 	cmds.setAttr(ctrlUpperArmFK_L+".InvPosX", 0)
			# 	cmds.setAttr(ctrlUpperArmFK_L+".InvPosY", 0)
			# 	cmds.setAttr(ctrlUpperArmFK_L+".InvPosZ", 1)
			# 	cmds.setAttr(ctrlUpperArmFK_L+".InvRotX", 1)
			# 	cmds.setAttr(ctrlUpperArmFK_L+".InvRotY", 1)
			# 	cmds.setAttr(ctrlUpperArmFK_L+".InvRotZ", 0)

			cmds.parent('BipedGuild', CtrlRoot)
			cmds.setAttr('BipedGuild.visibility', False)
			#==========----End----===========#
			cmds.select( d=True )


#-------------------------------------------------#
if __name__ == "__main__":
	rig_ui = RigTools() 
	