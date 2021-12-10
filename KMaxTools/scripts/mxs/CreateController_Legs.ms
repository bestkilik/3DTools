IKInfoCA = attributes IKInfo
(
	parameters main
	(
		Length type:#float
		useSoftIK type:#boolean
	)
)

TransformInfoCA = attributes transInfo
(
	parameters main
	(
		Roll type:#float
		Pitch type:#float
		Yaw type:#float
	)
)

fn createSegmentsBones startPos endPos seg = (
	boneList = #()
	spacing = (endPos - startPos) / seg
	preBone = undefined
	for i = 1 to seg do (
		pos0 = startPos + (i - 1)*spacing
		pos1 = startPos + i*spacing

		oBone = BoneSys.createBone pos0 pos1 [0,1,0]
		oBone.parent = preBone
		preBone = oBone
		append boneList oBone
	)
	return boneList
)

HipNode = ctrlHip --boneSpine1

bgThighNode = getNodeByName "bg_Thigh"
bgCalfNode = getNodeByName "bg_Calf"
bgFootNode = getNodeByName "bg_Foot"
bgToeNode = getNodeByName "bg_Toe"
bgToeENode = getNodeByName "bg_ToeEff"
bgKneeNode = getNodeByName "bg_Knee" 

posThigh_R = bgThighNode.transform.pos
posCalf_R = bgCalfNode.transform.pos
posFoot_R = bgFootNode.transform.pos
posToe_R = bgToeNode.transform.pos
posToeE_R = bgToeENode.transform.pos

posThigh_L = [-posThigh_R.x, posThigh_R.y, posThigh_R.z]
posCalf_L = [-posCalf_R.x, posCalf_R.y, posCalf_R.z]
posFoot_L = [-posFoot_R.x, posFoot_R.y, posFoot_R.z]
posToe_L = [-posToe_R.x, posToe_R.y, posToe_R.z]
posToeE_L = [-posToeE_R.x, posToeE_R.y, posToeE_R.z]

DistT2C = distance bgThighNode.transform.pos bgCalfNode.transform.pos
DistC2F = distance bgCalfNode.transform.pos bgFootNode.transform.pos

nThighVec_R = normalize (bgCalfNode.transform.pos - bgThighNode.transform.pos)
nCalfVec_R = normalize (bgFootNode.transform.pos - bgCalfNode.transform.pos)
nLegVec_R = normalize (bgFootNode.transform.pos - bgThighNode.transform.pos)
LegSideVec = normalize (cross nCalfVec_R nThighVec_R)

nThighVec_L = [-nThighVec_R.x, nThighVec_R.y, nThighVec_R.z]
nCalfVec_L = [-nCalfVec_R.x, nCalfVec_R.y, nCalfVec_R.z]
nLegVec_L = [-nLegVec_R.x, nLegVec_R.y, nLegVec_R.z]

KneeRadius = bgKneeNode.radius * bgKneeNode.transform.scale.y

posKneeStart_R = (DistT2C - KneeRadius)*nThighVec_R + posThigh_R
posKneeEnd_R = KneeRadius*nCalfVec_R + posCalf_R
posKneeStart_L = [-posKneeStart_R.x, posKneeStart_R.y, posKneeStart_R.z]
posKneeEnd_L = [-posKneeEnd_R.x, posKneeEnd_R.y, posKneeEnd_R.z]

LegUpVec_R = normalize (cross LegSideVec nLegVec_R)
LegUpVec_L = [-LegUpVec_R.x, LegUpVec_R.y, LegUpVec_R.z]

TotalLegLength = (distance posThigh_R posKneeStart_R) + (distance posKneeStart_R posKneeEnd_R) + (distance posKneeEnd_R posFoot_R)

FootLength = (distance posFoot_R posToe_R) + (distance posToe_R posToeE_R)

----------------------------
LegRoot_R = point name:"LegRoot_R" pos:posThigh_R size:2 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
LegRoot_R.transform = getAimMatrix 1 [0,0,-1] 3 [0,1,0] posThigh_R
LegRoot_R.parent = HipNode
hideLayer.addNode LegRoot_R

LegRoot_L = point name:"LegRoot_L" pos:posThigh_L size:2 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
LegRoot_L.transform = getAimMatrix 1 [0,0,-1] 3 [0,1,0] posThigh_L
LegRoot_L.parent = HipNode
hideLayer.addNode LegRoot_L
---------------------
legBoneList_R = #()
boneThigh_R = BoneSys.createBone posThigh_R posKneeStart_R [0,1,0]
append legBoneList_R boneThigh_R
hideLayer.addNode boneThigh_R
boneThigh_R.transform = getAimMatrix 1 nThighVec_R 3 -LegUpVec_R posThigh_R
boneThigh_R.parent = LegRoot_R

CustAttributes.add boneThigh_R TransformInfoCA
boneThigh_R.Roll.controller = float_script()
boneThigh_R.Roll.controller.IScriptCtrl.AddNode "Parent" LegRoot_R
boneThigh_R.Roll.controller.IScriptCtrl.AddNode "self" boneThigh_R
boneThigh_R.Roll.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
														"RollEuler = quatToEuler (Quat locQuat.x 0 0 locQuat.w)\n" + \
														"return RollEuler.x")

boneThigh_R.Yaw.controller = float_script()
boneThigh_R.Yaw.controller.IScriptCtrl.AddNode "Parent" LegRoot_R
boneThigh_R.Yaw.controller.IScriptCtrl.AddNode "self" boneThigh_R
boneThigh_R.Yaw.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
														"YawEuler = quatToEuler (Quat 0 locQuat.y 0 locQuat.w)\n" + \
														"return YawEuler.y")

boneThigh_R.Pitch.controller = float_script()
boneThigh_R.Pitch.controller.IScriptCtrl.AddNode "Parent" LegRoot_R
boneThigh_R.Pitch.controller.IScriptCtrl.AddNode "self" boneThigh_R
boneThigh_R.Pitch.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
														"PitchEuler = quatToEuler (Quat 0 0 locQuat.z locQuat.w)\n" + \
														"return PitchEuler.z")


boneKnee_R = BoneSys.createBone posKneeStart_R posKneeEnd_R [0,1,0]
append legBoneList_R boneKnee_R
hideLayer.addNode boneKnee_R
boneKnee_R.transform = getAimMatrix 1 (posKneeEnd_R - posKneeStart_R) 3 -LegUpVec_R posKneeStart_R
boneKnee_R.parent = boneThigh_R

boneCalf_R = BoneSys.createBone posKneeEnd_R posFoot_R [0,1,0]
append legBoneList_R boneCalf_R
hideLayer.addNode boneCalf_R
boneCalf_R.transform = getAimMatrix 1 nCalfVec_R 3 -LegUpVec_R posKneeEnd_R
boneCalf_R.parent = boneKnee_R

boneLegEff_R = BoneSys.createBone posFoot_R posFoot_R [0,1,0]
append legBoneList_R boneLegEff_R
hideLayer.addNode boneLegEff_R
boneLegEff_R.parent = boneCalf_R
boneLegEff_R.rotation.controller.value = (quat 0 0 0 1)
boneLegEff_R.length = 2

for b in legBoneList_R do(
	b.wireColor = (color 5 17 33)
	b.width = 2
	b.height = 2
	b.Taper = 90
	b.sidefins = off
	b.sidefinssize = 2
	b.frontfin = off
	b.frontfinsize = 2
	b.backfin = off
	b.backfinsize = 2
)

legBoneList_L = #()
boneThigh_L = BoneSys.createBone posThigh_L posKneeStart_L [0,1,0]
append legBoneList_L boneThigh_L
hideLayer.addNode boneThigh_L
boneThigh_L.transform = getAimMatrix 1 nThighVec_L 3 -LegUpVec_L posThigh_L
boneThigh_L.parent = LegRoot_L

CustAttributes.add boneThigh_L TransformInfoCA
boneThigh_L.Roll.controller = float_script()
boneThigh_L.Roll.controller.IScriptCtrl.AddNode "Parent" LegRoot_L
boneThigh_L.Roll.controller.IScriptCtrl.AddNode "self" boneThigh_L
boneThigh_L.Roll.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
														"RollEuler = quatToEuler (Quat locQuat.x 0 0 locQuat.w)\n" + \
														"return RollEuler.x")
boneThigh_L.Yaw.controller = float_script()
boneThigh_L.Yaw.controller.IScriptCtrl.AddNode "Parent" LegRoot_L
boneThigh_L.Yaw.controller.IScriptCtrl.AddNode "self" boneThigh_L
boneThigh_L.Yaw.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
														"YawEuler = quatToEuler (Quat 0 locQuat.y 0 locQuat.w)\n" + \
														"return YawEuler.y")

boneThigh_L.Pitch.controller = float_script()
boneThigh_L.Pitch.controller.IScriptCtrl.AddNode "Parent" LegRoot_L
boneThigh_L.Pitch.controller.IScriptCtrl.AddNode "self" boneThigh_L
boneThigh_L.Pitch.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
														"PitchEuler = quatToEuler (Quat 0 0 locQuat.z locQuat.w)\n" + \
														"return PitchEuler.z")

boneKnee_L = BoneSys.createBone posKneeStart_L posKneeEnd_L [0,1,0]
append legBoneList_L boneKnee_L
hideLayer.addNode boneKnee_L
boneKnee_L.transform = getAimMatrix 1 (posKneeEnd_L - posKneeStart_L) 3 -LegUpVec_L posKneeStart_L
boneKnee_L.parent = boneThigh_L

boneCalf_L = BoneSys.createBone posKneeEnd_L posFoot_L [0,1,0]
append legBoneList_L boneCalf_L
hideLayer.addNode boneCalf_L
boneCalf_L.transform = getAimMatrix 1 nCalfVec_L 3 -LegUpVec_L posKneeEnd_L
boneCalf_L.parent = boneKnee_L

boneLegEff_L = BoneSys.createBone posFoot_L posFoot_L [0,1,0]
append legBoneList_L boneLegEff_L
hideLayer.addNode boneLegEff_L
boneLegEff_L.parent = boneCalf_L
boneLegEff_L.rotation.controller.value = (quat 0 0 0 1)
boneLegEff_L.length = 2

for b in legBoneList_L do(
	b.wireColor = (color 5 17 33)
	b.width = 2
	b.height = 2
	b.Taper = 90
	b.sidefins = off
	b.sidefinssize = 2
	b.frontfin = off
	b.frontfinsize = 2
	b.backfin = off
	b.backfinsize = 2
)
-------------------------------------
LegIKLoc_R = point name:"LegIKLoc_R" pos:posFoot_R size:2 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
CustAttributes.add LegIKLoc_R IKInfoCA
LegIKLoc_R.parent = CtrlRoot

LegIKLoc_R.length.controller = float_script()
LegIKLoc_R.length.controller.IScriptCtrl.AddNode "Node0" LegRoot_R
LegIKLoc_R.length.controller.IScriptCtrl.AddNode "Node1" LegIKLoc_R
scriptStr = "distance Node0.transform.pos Node1.transform.pos"
LegIKLoc_R.length.controller.IScriptCtrl.SetExpression scriptStr
LegIKLoc_R.Length.controller = float_limit()
LegIKLoc_R.Length.controller.upper_limit = TotalLegLength
LegIKLoc_R.Length.controller.upper_smoothing = TotalLegLength*0.01
LegIKLoc_R.useSoftIK.controller = On_Off()
LegIKLoc_R.useSoftIK = off

LegIKHold_R = IKSys.ikChain boneThigh_R boneLegEff_R "IKHISolver"

pyLegIK_R = point name:"pyLegIK_R" pos:posFoot_R size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
pyLegIK_R.parent = CtrlRoot
pyLegIK_R.pos.controller = position_script()
pyLegIK_R.pos.controller.IScriptCtrl.AddNode "Parent" CtrlRoot
pyLegIK_R.pos.controller.IScriptCtrl.AddNode "Node0" LegRoot_R
pyLegIK_R.pos.controller.IScriptCtrl.AddNode "Node1" LegIKLoc_R
pyLegIK_R.pos.controller.IScriptCtrl.AddTarget "Length" LegIKLoc_R.length.controller
pyLegIK_R.pos.controller.IScriptCtrl.AddTarget "sw" LegIKLoc_R.useSoftIK.controller
scriptStr = "vec = normalize (Node1.transform.pos - Node0.transform.pos)\n" + \
			"wPos = vec * Length + Node0.transform.pos\n" + \
			"if sw then return wPos * (inverse Parent.transform)\n" + \
			"else return Node1.transform.pos * (inverse Parent.transform)"
pyLegIK_R.pos.controller.IScriptCtrl.SetExpression scriptStr
LegIKHold_R.parent = pyLegIK_R
LegIKHold_R.pos.controller.value = [0,0,0]

hideLayer.addNode LegIKLoc_R
hideLayer.addNode LegIKHold_R
hideLayer.addNode pyLegIK_R
-------------
LegIKLoc_L = point name:"LegIKLoc_L" pos:posFoot_L size:2 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
CustAttributes.add LegIKLoc_L IKInfoCA
LegIKLoc_L.parent = CtrlRoot

LegIKLoc_L.length.controller = float_script()
LegIKLoc_L.length.controller.IScriptCtrl.AddNode "Node0" LegRoot_L
LegIKLoc_L.length.controller.IScriptCtrl.AddNode "Node1" LegIKLoc_L
scriptStr = "distance Node0.transform.pos Node1.transform.pos"
LegIKLoc_L.length.controller.IScriptCtrl.SetExpression scriptStr
LegIKLoc_L.Length.controller = float_limit()
LegIKLoc_L.Length.controller.upper_limit = TotalLegLength
LegIKLoc_L.Length.controller.upper_smoothing = TotalLegLength*0.01
LegIKLoc_L.useSoftIK.controller = On_Off()
LegIKLoc_L.useSoftIK = off

LegIKHold_L = IKSys.ikChain boneThigh_L boneLegEff_L "IKHISolver"

pyLegIK_L = point name:"pyLegIK_L" pos:posFoot_L size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
pyLegIK_L.parent = CtrlRoot
pyLegIK_L.pos.controller = position_script()
pyLegIK_L.pos.controller.IScriptCtrl.AddNode "Parent" CtrlRoot
pyLegIK_L.pos.controller.IScriptCtrl.AddNode "Node0" LegRoot_L
pyLegIK_L.pos.controller.IScriptCtrl.AddNode "Node1" LegIKLoc_L
pyLegIK_L.pos.controller.IScriptCtrl.AddTarget "Length" LegIKLoc_L.length.controller
pyLegIK_L.pos.controller.IScriptCtrl.AddTarget "sw" LegIKLoc_L.useSoftIK.controller
scriptStr = "vec = normalize (Node1.transform.pos - Node0.transform.pos)\n" + \
			"wPos = vec * Length + Node0.transform.pos\n" + \
			"if sw then return wPos * (inverse Parent.transform)\n" + \
			"else return Node1.transform.pos * (inverse Parent.transform)"
pyLegIK_L.pos.controller.IScriptCtrl.SetExpression scriptStr
LegIKHold_L.parent = pyLegIK_L
LegIKHold_L.pos.controller.value = [0,0,0]

hideLayer.addNode LegIKLoc_L
hideLayer.addNode LegIKHold_L
hideLayer.addNode pyLegIK_L

----------------------------
r = 3
WireSpherePointList = #(
	[0, 0, r*(cos 0)],
	[0, r*(sin 30), r*(cos 30)],
	[0, r*(sin 60), r*(cos 60)],
	[0, r*(sin 90), r*(cos 90)],
	[0, r*(sin 120), r*(cos 120)],
	[0, r*(sin 150), r*(cos 150)],
	[0, r*(sin 180), r*(cos 180)],
	[0, r*(sin 210), r*(cos 210)],
	[0, r*(sin 240), r*(cos 240)],
	[0, r*(sin 270), r*(cos 270)],
	[0, r*(sin 300), r*(cos 300)],
	[0, r*(sin 330), r*(cos 330)],
	[0, 0, r*(cos 0)],
	[r*(sin 30), 0, r*(cos 30)],
	[r*(sin 60), 0, r*(cos 60)],
	[r*(sin 90), 0, r*(cos 90)],
	[r*(sin 120), 0, r*(cos 120)],
	[r*(sin 150), 0, r*(cos 150)],
	[r*(sin 180), 0, r*(cos 180)],
	[r*(sin 210), 0, r*(cos 210)],
	[r*(sin 240), 0, r*(cos 240)],
	[r*(sin 270), 0, r*(cos 270)],
	[r*(sin 300), 0, r*(cos 300)],
	[r*(sin 330), 0, r*(cos 330)],
	[0, 0, r*(cos 0)],
	[r*(sin 30), 0, r*(cos 30)],
	[r*(sin 60), 0, r*(cos 60)],
	[r*(sin 90), 0, 0],
	[r*(sin 120), r*(cos 120), 0],
	[r*(sin 150), r*(cos 150), 0],
	[r*(sin 180), r*(cos 180), 0],
	[r*(sin 210), r*(cos 210), 0],
	[r*(sin 240), r*(cos 240), 0],
	[r*(sin 270), r*(cos 270), 0],
	[r*(sin 300), r*(cos 300), 0],
	[r*(sin 330), r*(cos 330), 0],
	[r*(sin 0), r*(cos 0), 0],
	[r*(sin 30), r*(cos 30), 0],
	[r*(sin 60), r*(cos 60), 0],
	[r*(sin 90), 0, 0]
)

ctrlLegUpV_R = createLineCtrl WireSpherePointList false
ctrlLegUpV_R.wireColor = (color 6 134 6)
ctrlLegUpV_R.name = "Ctrl_LegUpV_R"
ctrlLegUpV_R.pos = (posThigh_R + posFoot_R)*0.5 + LegUpVec_R*TotalLegLength*0.6
LegIKHold_R.transform.controller.VHTarget = ctrlLegUpV_R
ctrlLegUpV_R.parent = CtrlRoot
ctrlLegUpV_R.rotation.controller = SlaveRotation()
ctrlLegUpV_R.scale.controller = SlaveScale()
layer.addNode ctrlLegUpV_R

ctrlLegUpV_L = createLineCtrl WireSpherePointList false
ctrlLegUpV_L.wireColor = (color 28 28 177)
ctrlLegUpV_L.name = "Ctrl_LegUpV_L"
ctrlLegUpV_L.pos = (posThigh_L + posFoot_L)*0.5 + LegUpVec_L*TotalLegLength*0.6
LegIKHold_L.transform.controller.VHTarget = ctrlLegUpV_L
ctrlLegUpV_L.parent = CtrlRoot
ctrlLegUpV_L.rotation.controller = SlaveRotation()
ctrlLegUpV_L.scale.controller = SlaveScale()
layer.addNode ctrlLegUpV_L

---------------------------
LegTwistBoneList_R = createSegmentsBones posThigh_R posKneeStart_R 4

for i = 1 to LegTwistBoneList_R.count do (
	LegTwistBoneList_R[i].wireColor = (color 30 67 30)
	LegTwistBoneList_R[i].parent = boneThigh_R
	LegTwistBoneList_R[i].rotation.controller.value = (quat 0 0 0 1)
	LegTwistBoneList_R[i].width = 4
	LegTwistBoneList_R[i].height = 4
	LegTwistBoneList_R[i].Taper = 50
	LegTwistBoneList_R[i].sidefins = off
	LegTwistBoneList_R[i].sidefinssize = 2
	LegTwistBoneList_R[i].frontfin = off
	LegTwistBoneList_R[i].frontfinsize = 2
	LegTwistBoneList_R[i].backfin = off
	LegTwistBoneList_R[i].backfinsize = 2
	hideLayer.addNode LegTwistBoneList_R[i]

	LegTwistBoneList_R[i].rotation.controller.X_Rotation.controller = float_script()
	LegTwistBoneList_R[i].rotation.controller.X_Rotation.controller.IScriptCtrl.AddTarget "Roll" boneThigh_R.Roll.controller
	scriptStr = "-Roll * " + (((LegTwistBoneList_R.count - i as float)/(LegTwistBoneList_R.count - 1.0) * 0.01745329251994) as string)
	LegTwistBoneList_R[i].rotation.controller.X_Rotation.controller.IScriptCtrl.SetExpression scriptStr
)

---
LegTwistBoneList_L = createSegmentsBones posThigh_L posKneeStart_L 4

for i = 1 to LegTwistBoneList_L.count do (
	LegTwistBoneList_L[i].wireColor = (color 40 40 88)
	LegTwistBoneList_L[i].parent = boneThigh_L
	LegTwistBoneList_L[i].rotation.controller.value = (quat 0 0 0 1)
	LegTwistBoneList_L[i].width = 4
	LegTwistBoneList_L[i].height = 4
	LegTwistBoneList_L[i].Taper = 50
	LegTwistBoneList_L[i].sidefins = off
	LegTwistBoneList_L[i].sidefinssize = 2
	LegTwistBoneList_L[i].frontfin = off
	LegTwistBoneList_L[i].frontfinsize = 2
	LegTwistBoneList_L[i].backfin = off
	LegTwistBoneList_L[i].backfinsize = 2
	hideLayer.addNode LegTwistBoneList_L[i]

	LegTwistBoneList_L[i].rotation.controller.X_Rotation.controller = float_script()
	LegTwistBoneList_L[i].rotation.controller.X_Rotation.controller.IScriptCtrl.AddTarget "Roll" boneThigh_L.Roll.controller
	scriptStr = "-Roll * " + (((LegTwistBoneList_L.count - i as float)/(LegTwistBoneList_L.count - 1.0) * 0.01745329251994) as string)
	LegTwistBoneList_L[i].rotation.controller.X_Rotation.controller.IScriptCtrl.SetExpression scriptStr
)

----------Butt------
boneButt_R = BoneSys.createBone posThigh_R posThigh_R [0,1,0]
boneButt_R.transform = LegRoot_R.transform
boneButt_R.parent = LegRoot_R
boneButt_R.wireColor = (color 15 40 15)
boneButt_R.width = 5
boneButt_R.height = 5
boneButt_R.Taper = 5
boneButt_R.sidefins = off
boneButt_R.sidefinssize = 2
boneButt_R.frontfin = off
boneButt_R.frontfinsize = 2
boneButt_R.backfin = off
boneButt_R.backfinsize = 2
boneButt_R.length = 2.5

boneButt_R.rotation.controller = Orientation_Constraint()
boneButt_R.rotation.controller.appendtarget LegRoot_R 50
boneButt_R.rotation.controller.appendtarget LegTwistBoneList_R[1] 50

boneButt_R.scale.controller = scale_script()
boneButt_R.scale.controller.IScriptCtrl.AddTarget "Pitch" boneThigh_R.Pitch.controller
boneButt_R.scale.controller.IScriptCtrl.AddTarget "Yaw" boneThigh_R.Yaw.controller
boneButt_R.scale.controller.IScriptCtrl.SetExpression "[1, (abs Pitch)/180 + 1, (abs Yaw)/180 + 1]"

hideLayer.addNode boneButt_R
---
boneButt_L = BoneSys.createBone posThigh_L posThigh_L [0,1,0]
boneButt_L.transform = LegRoot_L.transform
boneButt_L.parent = LegRoot_L
boneButt_L.wireColor = (color 15 15 40)
boneButt_L.width = 5
boneButt_L.height = 5
boneButt_L.Taper = 5
boneButt_L.sidefins = off
boneButt_L.sidefinssize = 2
boneButt_L.frontfin = off
boneButt_L.frontfinsize = 2
boneButt_L.backfin = off
boneButt_L.backfinsize = 2
boneButt_L.length = 2.5

boneButt_L.rotation.controller = Orientation_Constraint()
boneButt_L.rotation.controller.appendtarget LegRoot_L 50
boneButt_L.rotation.controller.appendtarget LegTwistBoneList_L[1] 50

boneButt_L.scale.controller = scale_script()
boneButt_L.scale.controller.IScriptCtrl.AddTarget "Pitch" boneThigh_L.Pitch.controller
boneButt_L.scale.controller.IScriptCtrl.AddTarget "Yaw" boneThigh_L.Yaw.controller
boneButt_L.scale.controller.IScriptCtrl.SetExpression "[1, (abs Pitch)/180 + 1, (abs Yaw)/180 + 1]"

hideLayer.addNode boneButt_L
---------Foot------------
CtrlFootPointList = #(
	[-FootLength*0.4, FootLength*0.85, 0],
	[ FootLength*0.4, FootLength*0.85, 0],
	[ FootLength*0.4,-FootLength*0.85, 0],
	[-FootLength*0.4,-FootLength*0.85, 0]
)

innR = 18.0
outR = 20.0
etcD = 1.0
cenR = (innR + outR)*0.5

CtrlRotArrowPointList = #(
	[0, cenR*(cos  20), cenR*(sin  20)],
	[0, innR*(cos  15), innR*(sin  15)],
	[0, (innR - etcD)*(cos  10), (innR - etcD)*(sin  10)],
	[0, innR*(cos  10), innR*(sin  10)],
	[0, innR*(cos   5), innR*(sin   5)],
	[0, innR*(cos   0), innR*(sin   0)],
	[0, innR*(cos  -5), innR*(sin  -5)],
	[0, innR*(cos -10), innR*(sin -10)],
	[0, (innR - etcD)*(cos -10), (innR - etcD)*(sin -10)],
	[0, innR*(cos -15), innR*(sin -15)],
	[0, cenR*(cos -20), cenR*(sin -20)],
	[0, outR*(cos -15), outR*(sin -15)],
	[0, (outR + etcD)*(cos -10), (outR + etcD)*(sin -10)],
	[0, outR*(cos -10), outR*(sin -10)],
	[0, outR*(cos  -5), outR*(sin  -5)],
	[0, outR*(cos   0), outR*(sin   0)],
	[0, outR*(cos   5), outR*(sin   5)],
	[0, outR*(cos  10), outR*(sin  10)],
	[0, (outR + etcD)*(cos  10), (outR + etcD)*(sin  10)],
	[0, outR*(cos  15), outR*(sin  15)]
)
----
boneFootList_R = #()
boneFoot_R = BoneSys.createBone posFoot_R posToe_R [0,1,0]
boneFoot_R.parent = boneCalf_R
append boneFootList_R boneFoot_R
boneFoot_R.transform = getAimMatrix 1 (posToe_R - posFoot_R) 3 [0,0,-1] posFoot_R

boneToe_R = BoneSys.createBone posToe_R posToeE_R [0,1,0]
boneToe_R.parent = boneFoot_R
append boneFootList_R boneToe_R
boneToe_R.transform = getAimMatrix 1 (posToeE_R - posToe_R) 3 [0,0,-1] posToe_R

for b in boneFootList_R do (
	b.wireColor = (color 15 40 15)
	b.width = 2
	b.height = 2
	b.Taper = 90
	b.sidefins = off
	b.sidefinssize = 2
	b.frontfin = off
	b.frontfinsize = 2
	b.backfin = off
	b.backfinsize = 2

	hideLayer.addNode b
)

footCenter_R = (posToe_R + posFoot_R)*0.5
footCenter_R.z = 0

ctrlFoot_R = createLineCtrl CtrlFootPointList true
ctrlFoot_R.wireColor = (color 6 134 6)
ctrlFoot_R.name = "Ctrl_Foot_R"
ctrlFoot_R.transform = getAimMatrix 3 [0,0,1] 2 (posToe_R - posToeE_R) footCenter_R
ctrlFoot_R.parent = CtrlRoot
ctrlFoot_R.scale.controller = SlaveScale()
layer.addNode ctrlFoot_R

ctrlFootPad_R = createLineCtrl CtrlRotArrowPointList true
ctrlFootPad_R.wireColor = (color 6 134 6)
ctrlFootPad_R.name = "Ctrl_FootPad_R"
ctrlFootPad_R.transform = getAimMatrix 3 [0,0,1] 2 (posFoot_R - posToe_R) posToe_R
ctrlFootPad_R.parent = ctrlFoot_R
scriptStr = ctrlFootPad_R.pos.controller.value as string
ctrlFootPad_R.position.controller = position_script()
ctrlFootPad_R.position.controller.IScriptCtrl.SetExpression scriptStr
ctrlFootPad_R.scale.controller = SlaveScale()
LegIKLoc_R.parent = ctrlFootPad_R
layer.addNode ctrlFootPad_R

FootLocatorList_R = #()
locToeE_R = point name:"locToeE_R" pos:posToeE_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
locToeE_R.parent = ctrlFoot_R
append FootLocatorList_R locToeE_R
locToe_R = point name:"locToe_R" pos:posToe_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
locToe_R.parent = ctrlFoot_R
append FootLocatorList_R locToe_R

locFootPadUpV_R = point name:"locFootPadUpV_R" pos:((posFoot_R + posToe_R)*0.5 + boneFoot_R.transform.row3*FootLength*0.5) size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
locFootPadUpV_R.parent = ctrlFootPad_R
append FootLocatorList_R locFootPadUpV_R

locToeUpV_R = point name:"locToeUpV_R" pos:((posToeE_R + posToe_R)*0.5 + boneToe_R.transform.row3*FootLength*0.25) size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
locToeUpV_R.parent = ctrlFoot_R
append FootLocatorList_R locToeUpV_R

boneFoot_R.rotation.controller = LookAt_Constraint()
boneFoot_R.rotation.controller.appendtarget locToe_R 50
boneFoot_R.rotation.controller.lookat_vector_length = 0
boneFoot_R.rotation.controller.upnode_ctrl = 0
boneFoot_R.rotation.controller.upnode_world = off
boneFoot_R.rotation.controller.pickUpNode = locFootPadUpV_R
boneFoot_R.rotation.controller.StoUP_axis = 2
boneFoot_R.rotation.controller.StoUP_axisFlip = off

boneToe_R.rotation.controller = LookAt_Constraint()
boneToe_R.rotation.controller.appendtarget locToeE_R 50
boneToe_R.rotation.controller.lookat_vector_length = 0
boneToe_R.rotation.controller.upnode_ctrl = 0
boneToe_R.rotation.controller.upnode_world = off
boneToe_R.rotation.controller.pickUpNode = locToeUpV_R
boneToe_R.rotation.controller.StoUP_axis = 2
boneToe_R.rotation.controller.StoUP_axisFlip = off

for o in FootLocatorList_R do hideLayer.addNode o
------
boneFootList_L = #()
boneFoot_L = BoneSys.createBone posFoot_L posToe_L [0,1,0]
boneFoot_L.parent = boneCalf_L
append boneFootList_L boneFoot_L
boneFoot_L.transform = getAimMatrix 1 (posToe_L - posFoot_L) 3 [0,0,-1] posFoot_L

boneToe_L = BoneSys.createBone posToe_L posToeE_L [0,1,0]
boneToe_L.parent = boneFoot_L
append boneFootList_L boneToe_L
boneToe_L.transform = getAimMatrix 1 (posToeE_L - posToe_L) 3 [0,0,-1] posToe_L

for b in boneFootList_L do (
	b.wireColor = (color 40 40 88)
	b.width = 2
	b.height = 2
	b.Taper = 90
	b.sidefins = off
	b.sidefinssize = 2
	b.frontfin = off
	b.frontfinsize = 2
	b.backfin = off
	b.backfinsize = 2

	hideLayer.addNode b
)

footCenter_L = (posToe_L + posFoot_L)*0.5
footCenter_L.z = 0

ctrlFoot_L = createLineCtrl CtrlFootPointList true
ctrlFoot_L.wireColor = (color 28 28 177)
ctrlFoot_L.name = "Ctrl_Foot_L"
ctrlFoot_L.transform = getAimMatrix 3 [0,0,1] 2 (posToe_L - posToeE_L) footCenter_L
ctrlFoot_L.parent = CtrlRoot
ctrlFoot_L.scale.controller = SlaveScale()
layer.addNode ctrlFoot_L

ctrlFootPad_L = createLineCtrl CtrlRotArrowPointList true
ctrlFootPad_L.wireColor = (color 28 28 177)
ctrlFootPad_L.name = "Ctrl_FootPad_L"
ctrlFootPad_L.transform = getAimMatrix 3 [0,0,1] 2 (posFoot_L - posToe_L) posToe_L
ctrlFootPad_L.parent = ctrlFoot_L
scriptStr = ctrlFootPad_L.pos.controller.value as string
ctrlFootPad_L.position.controller = position_script()
ctrlFootPad_L.position.controller.IScriptCtrl.SetExpression scriptStr
ctrlFootPad_L.scale.controller = SlaveScale()
LegIKLoc_L.parent = ctrlFootPad_L
layer.addNode ctrlFootPad_L

FootLocatorList_L = #()
locToeE_L = point name:"locToeE_L" pos:posToeE_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
locToeE_L.parent = ctrlFoot_L
append FootLocatorList_L locToeE_L
locToe_L = point name:"locToe_L" pos:posToe_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
locToe_L.parent = ctrlFoot_L
append FootLocatorList_L locToe_L

locFootPadUpV_L = point name:"locFootPadUpV_L" pos:((posFoot_L + posToe_L)*0.5 + boneFoot_L.transform.row3*FootLength*0.5) size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
locFootPadUpV_L.parent = ctrlFootPad_L
append FootLocatorList_L locFootPadUpV_L

locToeUpV_L = point name:"locToeUpV_L" pos:((posToeE_L + posToe_L)*0.5 + boneToe_L.transform.row3*FootLength*0.25) size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
locToeUpV_L.parent = ctrlFoot_L
append FootLocatorList_L locToeUpV_L

boneFoot_L.rotation.controller = LookAt_Constraint()
boneFoot_L.rotation.controller.appendtarget locToe_L 50
boneFoot_L.rotation.controller.lookat_vector_length = 0
boneFoot_L.rotation.controller.upnode_ctrl = 0
boneFoot_L.rotation.controller.upnode_world = off
boneFoot_L.rotation.controller.pickUpNode = locFootPadUpV_L
boneFoot_L.rotation.controller.StoUP_axis = 2
boneFoot_L.rotation.controller.StoUP_axisFlip = off

boneToe_L.rotation.controller = LookAt_Constraint()
boneToe_L.rotation.controller.appendtarget locToeE_L 50
boneToe_L.rotation.controller.lookat_vector_length = 0
boneToe_L.rotation.controller.upnode_ctrl = 0
boneToe_L.rotation.controller.upnode_world = off
boneToe_L.rotation.controller.pickUpNode = locToeUpV_L
boneToe_L.rotation.controller.StoUP_axis = 2
boneToe_L.rotation.controller.StoUP_axisFlip = off

for o in FootLocatorList_L do hideLayer.addNode o

-----------
paramWire.connect CtrlRoot.BipedControl[#bSoftIK] LegIKLoc_R.IKInfo[#useSoftIK] "bSoftIK"
paramWire.connect CtrlRoot.BipedControl[#bSoftIK] LegIKLoc_L.IKInfo[#useSoftIK] "bSoftIK"