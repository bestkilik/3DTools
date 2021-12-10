fn createWireSpherifyCrossArrow radius angleRange axisIdx bInvert =(
	unitA = (angleRange * 0.5) / 8.0
	p1 = #((cos (90.0 - unitA * 1)) * radius, (sin (90.0 - unitA * 1)) * radius )
	p2 = #((cos (90.0 - unitA * 2)) * radius, (sin (90.0 - unitA * 2)) * radius )
	p3 = #((cos (90.0 - unitA * 3)) * radius, (sin (90.0 - unitA * 3)) * radius )
	p4 = #((cos (90.0 - unitA * 4)) * radius, (sin (90.0 - unitA * 4)) * radius )
	p5 = #((cos (90.0 - unitA * 5)) * radius, (sin (90.0 - unitA * 5)) * radius )
	p6 = #((cos (90.0 - unitA * 6)) * radius, (sin (90.0 - unitA * 6)) * radius )
	p7 = #((cos (90.0 - unitA * 7)) * radius, (sin (90.0 - unitA * 7)) * radius )
	p8 = #((cos (90.0 - unitA * 8)) * radius, (sin (90.0 - unitA * 8)) * radius )

	inv = 1
	if bInvert do inv = -1

	listPt = #(
		[p1[2],  p1[1], -p1[1]],
		[p2[2],  p2[1], -p1[1]],
		[p3[2],  p3[1], -p1[1]],
		[p4[2],  p4[1], -p1[1]],
		[p5[2],  p5[1], -p1[1]],
		[p6[2],  p6[1], -p1[1]],
		[p6[2],  p6[1], -p1[1]*1.7],
		[p7[2],  p7[1], -p1[1]],
		[p8[2],  p8[1],      0],
		[p7[2],  p7[1],  p1[1]],
		[p6[2],  p6[1],  p1[1]*1.7],
		[p6[2],  p6[1],  p1[1]],
		[p5[2],  p5[1],  p1[1]],
		[p4[2],  p4[1],  p1[1]],
		[p3[2],  p3[1],  p1[1]],
		[p2[2],  p2[1],  p1[1]],
		[p1[2],  p1[1],  p1[1]],
		[p2[2],  p1[1],  p2[1]],
		[p3[2],  p1[1],  p3[1]],
		[p4[2],  p1[1],  p4[1]],
		[p5[2],  p1[1],  p5[1]],
		[p6[2],  p1[1],  p6[1]],
		[p6[2],  p1[1]*1.7,  p6[1]],
		[p7[2],  p1[1],  p7[1]],
		[p8[2],      0,  p8[1]],
		[p7[2], -p1[1],  p7[1]],
		[p6[2], -p1[1]*1.7,  p6[1]],
		[p6[2], -p1[1],  p6[1]],
		[p5[2], -p1[1],  p5[1]],
		[p4[2], -p1[1],  p4[1]],
		[p3[2], -p1[1],  p3[1]],
		[p2[2], -p1[1],  p2[1]],
		[p1[2], -p1[1],  p1[1]],
		[p2[2], -p2[1],  p1[1]],
		[p3[2], -p3[1],  p1[1]],
		[p4[2], -p4[1],  p1[1]],
		[p5[2], -p5[1],  p1[1]],
		[p6[2], -p6[1],  p1[1]],
		[p6[2], -p6[1],  p1[1]*1.7],
		[p7[2], -p7[1],  p1[1]],
		[p8[2], -p8[1],      0],
		[p7[2], -p7[1], -p1[1]],
		[p6[2], -p6[1], -p1[1]*1.7],
		[p6[2], -p6[1], -p1[1]],
		[p5[2], -p5[1], -p1[1]],
		[p4[2], -p4[1], -p1[1]],
		[p3[2], -p3[1], -p1[1]],
		[p2[2], -p2[1], -p1[1]],
		[p1[2], -p1[1], -p1[1]],
		[p2[2], -p1[1], -p2[1]],
		[p3[2], -p1[1], -p3[1]],
		[p4[2], -p1[1], -p4[1]],
		[p5[2], -p1[1], -p5[1]],
		[p6[2], -p1[1], -p6[1]],
		[p6[2], -p1[1]*1.7, -p6[1]],
		[p7[2], -p1[1], -p7[1]],
		[p8[2],      0, -p8[1]],
		[p7[2],  p1[1], -p7[1]],
		[p6[2],  p1[1]*1.7, -p6[1]],
		[p6[2],  p1[1], -p6[1]],
		[p5[2],  p1[1], -p5[1]],
		[p4[2],  p1[1], -p4[1]],
		[p3[2],  p1[1], -p3[1]],
		[p2[2],  p1[1], -p2[1]],
		[p1[2],  p1[1], -p1[1]]
	)

	listP = #()

	if axisIdx == 2 then (
		for i = 1 to listPt.count do (
			item = copy listPt[i]
			tmp = item.x
			item.x = item.y
			item.y = tmp * inv
			append listP item
		)
	)
	else if axisIdx == 3 then (
		for i = 1 to listPt.count do (
			item = copy listPt[i]
			tmp = item.x
			item.x = item.z
			item.z = tmp * inv
			append listP item
		)
	)
	else (
		for i = 1 to listPt.count do (
			item = copy listPt[i]
			item.x = item.x * inv
			append listP item
		)
	)

	obj = createLineCtrl listP false
	return obj
)

BaseInfoCA = attributes baseInfo
(
	parameters main
	(
		visible type:#boolean
	)
)

ChestNode = pySpine3--boneSpine3

ChestFixNode = point name:"ChestFixNode" pos:ChestNode.transform.pos size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
ChestFixNode.parent = ChestNode
ChestFixNode.transform = ChestNode.transform
ChestFixNode.scale.controller = scale_script()
ChestFixNode.scale.controller.IScriptCtrl.AddNode "ref" boneSpine3
scriptStr = "ref.stretchTM.scale"
ChestFixNode.scale.controller.IScriptCtrl.SetExpression scriptStr
hideLayer.addNode ChestFixNode

bgShoulder = getNodeByName "bg_Shoulder"
bgUpperArm = getNodeByName "bg_UpperArm"
bgElbow = getNodeByName "bg_Elbow"
bgForeArm = getNodeByName "bg_ForeArm"
bgHand = getNodeByName "bg_Hand"

bgFinger00 = getNodeByName "bg_Finger00"
bgFinger01 = getNodeByName "bg_Finger01"
bgFinger02 = getNodeByName "bg_Finger02"
bgFinger0E = getNodeByName "bg_Finger0E"
bgFinger10 = getNodeByName "bg_Finger10"
bgFinger11 = getNodeByName "bg_Finger11"
bgFinger12 = getNodeByName "bg_Finger12"
bgFinger1E = getNodeByName "bg_Finger1E"
bgFinger20 = getNodeByName "bg_Finger20"
bgFinger21 = getNodeByName "bg_Finger21"
bgFinger22 = getNodeByName "bg_Finger22"
bgFinger2E = getNodeByName "bg_Finger2E"
bgFinger30 = getNodeByName "bg_Finger30"
bgFinger31 = getNodeByName "bg_Finger31"
bgFinger32 = getNodeByName "bg_Finger32"
bgFinger3E = getNodeByName "bg_Finger3E"
bgFinger40 = getNodeByName "bg_Finger40"
bgFinger41 = getNodeByName "bg_Finger41"
bgFinger42 = getNodeByName "bg_Finger42"
bgFinger4E = getNodeByName "bg_Finger4E"
-----R Finger
	posFinger00_R = bgFinger00.transform.pos
	posFinger01_R = bgFinger01.transform.pos
	posFinger02_R = bgFinger02.transform.pos
	posFinger0E_R = bgFinger0E.transform.pos
	posFinger10_R = bgFinger10.transform.pos
	posFinger11_R = bgFinger11.transform.pos
	posFinger12_R = bgFinger12.transform.pos
	posFinger1E_R = bgFinger1E.transform.pos
	posFinger20_R = bgFinger20.transform.pos
	posFinger21_R = bgFinger21.transform.pos
	posFinger22_R = bgFinger22.transform.pos
	posFinger2E_R = bgFinger2E.transform.pos
	posFinger30_R = bgFinger30.transform.pos
	posFinger31_R = bgFinger31.transform.pos
	posFinger32_R = bgFinger32.transform.pos
	posFinger3E_R = bgFinger3E.transform.pos
	posFinger40_R = bgFinger40.transform.pos
	posFinger41_R = bgFinger41.transform.pos
	posFinger42_R = bgFinger42.transform.pos
	posFinger4E_R = bgFinger4E.transform.pos
	
	xVecFinger00_R = bgFinger00.transform.row1
	xVecFinger01_R = bgFinger01.transform.row1
	xVecFinger02_R = bgFinger02.transform.row1
	xVecFinger0E_R = bgFinger0E.transform.row1
	xVecFinger10_R = bgFinger10.transform.row1
	xVecFinger11_R = bgFinger11.transform.row1
	xVecFinger12_R = bgFinger12.transform.row1
	xVecFinger1E_R = bgFinger1E.transform.row1
	xVecFinger20_R = bgFinger20.transform.row1
	xVecFinger21_R = bgFinger21.transform.row1
	xVecFinger22_R = bgFinger22.transform.row1
	xVecFinger2E_R = bgFinger2E.transform.row1
	xVecFinger30_R = bgFinger30.transform.row1
	xVecFinger31_R = bgFinger31.transform.row1
	xVecFinger32_R = bgFinger32.transform.row1
	xVecFinger3E_R = bgFinger3E.transform.row1
	xVecFinger40_R = bgFinger40.transform.row1
	xVecFinger41_R = bgFinger41.transform.row1
	xVecFinger42_R = bgFinger42.transform.row1
	xVecFinger4E_R = bgFinger4E.transform.row1
	
	zVecFinger00_R = bgFinger00.transform.row3
	zVecFinger01_R = bgFinger01.transform.row3
	zVecFinger02_R = bgFinger02.transform.row3
	zVecFinger0E_R = bgFinger0E.transform.row3
	zVecFinger10_R = bgFinger10.transform.row3
	zVecFinger11_R = bgFinger11.transform.row3
	zVecFinger12_R = bgFinger12.transform.row3
	zVecFinger1E_R = bgFinger1E.transform.row3
	zVecFinger20_R = bgFinger20.transform.row3
	zVecFinger21_R = bgFinger21.transform.row3
	zVecFinger22_R = bgFinger22.transform.row3
	zVecFinger2E_R = bgFinger2E.transform.row3
	zVecFinger30_R = bgFinger30.transform.row3
	zVecFinger31_R = bgFinger31.transform.row3
	zVecFinger32_R = bgFinger32.transform.row3
	zVecFinger3E_R = bgFinger3E.transform.row3
	zVecFinger40_R = bgFinger40.transform.row3
	zVecFinger41_R = bgFinger41.transform.row3
	zVecFinger42_R = bgFinger42.transform.row3
	zVecFinger4E_R = bgFinger4E.transform.row3
-----L Finger
	posFinger00_L = [-posFinger00_R.x, posFinger00_R.y, posFinger00_R.z]
	posFinger01_L = [-posFinger01_R.x, posFinger01_R.y, posFinger01_R.z]
	posFinger02_L = [-posFinger02_R.x, posFinger02_R.y, posFinger02_R.z]
	posFinger0E_L = [-posFinger0E_R.x, posFinger0E_R.y, posFinger0E_R.z]
	posFinger10_L = [-posFinger10_R.x, posFinger10_R.y, posFinger10_R.z]
	posFinger11_L = [-posFinger11_R.x, posFinger11_R.y, posFinger11_R.z]
	posFinger12_L = [-posFinger12_R.x, posFinger12_R.y, posFinger12_R.z]
	posFinger1E_L = [-posFinger1E_R.x, posFinger1E_R.y, posFinger1E_R.z]
	posFinger20_L = [-posFinger20_R.x, posFinger20_R.y, posFinger20_R.z]
	posFinger21_L = [-posFinger21_R.x, posFinger21_R.y, posFinger21_R.z]
	posFinger22_L = [-posFinger22_R.x, posFinger22_R.y, posFinger22_R.z]
	posFinger2E_L = [-posFinger2E_R.x, posFinger2E_R.y, posFinger2E_R.z]
	posFinger30_L = [-posFinger30_R.x, posFinger30_R.y, posFinger30_R.z]
	posFinger31_L = [-posFinger31_R.x, posFinger31_R.y, posFinger31_R.z]
	posFinger32_L = [-posFinger32_R.x, posFinger32_R.y, posFinger32_R.z]
	posFinger3E_L = [-posFinger3E_R.x, posFinger3E_R.y, posFinger3E_R.z]
	posFinger40_L = [-posFinger40_R.x, posFinger40_R.y, posFinger40_R.z]
	posFinger41_L = [-posFinger41_R.x, posFinger41_R.y, posFinger41_R.z]
	posFinger42_L = [-posFinger42_R.x, posFinger42_R.y, posFinger42_R.z]
	posFinger4E_L = [-posFinger4E_R.x, posFinger4E_R.y, posFinger4E_R.z]
	
	xVecFinger00_L = [-xVecFinger00_R.x, xVecFinger00_R.y, xVecFinger00_R.z]
	xVecFinger01_L = [-xVecFinger01_R.x, xVecFinger01_R.y, xVecFinger01_R.z]
	xVecFinger02_L = [-xVecFinger02_R.x, xVecFinger02_R.y, xVecFinger02_R.z]
	xVecFinger0E_L = [-xVecFinger0E_R.x, xVecFinger0E_R.y, xVecFinger0E_R.z]
	xVecFinger10_L = [-xVecFinger10_R.x, xVecFinger10_R.y, xVecFinger10_R.z]
	xVecFinger11_L = [-xVecFinger11_R.x, xVecFinger11_R.y, xVecFinger11_R.z]
	xVecFinger12_L = [-xVecFinger12_R.x, xVecFinger12_R.y, xVecFinger12_R.z]
	xVecFinger1E_L = [-xVecFinger1E_R.x, xVecFinger1E_R.y, xVecFinger1E_R.z]
	xVecFinger20_L = [-xVecFinger20_R.x, xVecFinger20_R.y, xVecFinger20_R.z]
	xVecFinger21_L = [-xVecFinger21_R.x, xVecFinger21_R.y, xVecFinger21_R.z]
	xVecFinger22_L = [-xVecFinger22_R.x, xVecFinger22_R.y, xVecFinger22_R.z]
	xVecFinger2E_L = [-xVecFinger2E_R.x, xVecFinger2E_R.y, xVecFinger2E_R.z]
	xVecFinger30_L = [-xVecFinger30_R.x, xVecFinger30_R.y, xVecFinger30_R.z]
	xVecFinger31_L = [-xVecFinger31_R.x, xVecFinger31_R.y, xVecFinger31_R.z]
	xVecFinger32_L = [-xVecFinger32_R.x, xVecFinger32_R.y, xVecFinger32_R.z]
	xVecFinger3E_L = [-xVecFinger3E_R.x, xVecFinger3E_R.y, xVecFinger3E_R.z]
	xVecFinger40_L = [-xVecFinger40_R.x, xVecFinger40_R.y, xVecFinger40_R.z]
	xVecFinger41_L = [-xVecFinger41_R.x, xVecFinger41_R.y, xVecFinger41_R.z]
	xVecFinger42_L = [-xVecFinger42_R.x, xVecFinger42_R.y, xVecFinger42_R.z]
	xVecFinger4E_L = [-xVecFinger4E_R.x, xVecFinger4E_R.y, xVecFinger4E_R.z]
	
	zVecFinger00_L = [-zVecFinger00_R.x, zVecFinger00_R.y, zVecFinger00_R.z]
	zVecFinger01_L = [-zVecFinger01_R.x, zVecFinger01_R.y, zVecFinger01_R.z]
	zVecFinger02_L = [-zVecFinger02_R.x, zVecFinger02_R.y, zVecFinger02_R.z]
	zVecFinger0E_L = [-zVecFinger0E_R.x, zVecFinger0E_R.y, zVecFinger0E_R.z]
	zVecFinger10_L = [-zVecFinger10_R.x, zVecFinger10_R.y, zVecFinger10_R.z]
	zVecFinger11_L = [-zVecFinger11_R.x, zVecFinger11_R.y, zVecFinger11_R.z]
	zVecFinger12_L = [-zVecFinger12_R.x, zVecFinger12_R.y, zVecFinger12_R.z]
	zVecFinger1E_L = [-zVecFinger1E_R.x, zVecFinger1E_R.y, zVecFinger1E_R.z]
	zVecFinger20_L = [-zVecFinger20_R.x, zVecFinger20_R.y, zVecFinger20_R.z]
	zVecFinger21_L = [-zVecFinger21_R.x, zVecFinger21_R.y, zVecFinger21_R.z]
	zVecFinger22_L = [-zVecFinger22_R.x, zVecFinger22_R.y, zVecFinger22_R.z]
	zVecFinger2E_L = [-zVecFinger2E_R.x, zVecFinger2E_R.y, zVecFinger2E_R.z]
	zVecFinger30_L = [-zVecFinger30_R.x, zVecFinger30_R.y, zVecFinger30_R.z]
	zVecFinger31_L = [-zVecFinger31_R.x, zVecFinger31_R.y, zVecFinger31_R.z]
	zVecFinger32_L = [-zVecFinger32_R.x, zVecFinger32_R.y, zVecFinger32_R.z]
	zVecFinger3E_L = [-zVecFinger3E_R.x, zVecFinger3E_R.y, zVecFinger3E_R.z]
	zVecFinger40_L = [-zVecFinger40_R.x, zVecFinger40_R.y, zVecFinger40_R.z]
	zVecFinger41_L = [-zVecFinger41_R.x, zVecFinger41_R.y, zVecFinger41_R.z]
	zVecFinger42_L = [-zVecFinger42_R.x, zVecFinger42_R.y, zVecFinger42_R.z]
	zVecFinger4E_L = [-zVecFinger4E_R.x, zVecFinger4E_R.y, zVecFinger4E_R.z]

posShoulder_R = bgShoulder.transform.pos
posUpperArm_R = bgUpperArm.transform.pos
posForeArm_R = bgForeArm.transform.pos
posHand_R = bgHand.transform.pos
posHandEff_R = bgHand.transform.pos + bgHand.transform.row1*bgHand.length*bgHand.transform.scale.x

posShoulder_L = [-posShoulder_R.x, posShoulder_R.y, posShoulder_R.z]
posUpperArm_L = [-posUpperArm_R.x, posUpperArm_R.y, posUpperArm_R.z]
posForeArm_L = [-posForeArm_R.x, posForeArm_R.y, posForeArm_R.z]
posHand_L = [-posHand_R.x, posHand_R.y, posHand_R.z]
posHandEff_L = [-posHandEff_R.x, posHandEff_R.y, posHandEff_R.z]

DistU2F = distance posUpperArm_R posForeArm_R
DistF2H = distance posForeArm_R posHand_R

nUpperArmVec_R = normalize (posForeArm_R - posUpperArm_R)
nForeArmVec_R = normalize (posHand_R - posForeArm_R)
nArmVec_R = normalize (posHand_R - posUpperArm_R)
nArmSideVec = normalize (cross nForeArmVec_R nUpperArmVec_R)

nUpperArmVec_L = [-nUpperArmVec_R.x, nUpperArmVec_R.y, nUpperArmVec_R.z]
nForeArmVec_L = [-nForeArmVec_R.x, nForeArmVec_R.y, nForeArmVec_R.z]
nArmVec_L = [-nArmVec_R.x, nArmVec_R.y, nArmVec_R.z]

ElbowRadius = bgElbow.radius * bgElbow.transform.scale.y

posElbowStart_R = (DistU2F - ElbowRadius)*nUpperArmVec_R + posUpperArm_R
posElbowEnd_R = ElbowRadius*nForeArmVec_R + posForeArm_R
posElbowStart_L = [-posElbowStart_R.x, posElbowStart_R.y, posElbowStart_R.z]
posElbowEnd_L = [-posElbowEnd_R.x, posElbowEnd_R.y, posElbowEnd_R.z]

ArmUpVec_R = normalize (cross nArmSideVec nArmVec_R)
ArmUpVec_L = [-ArmUpVec_R.x, ArmUpVec_R.y, ArmUpVec_R.z]

TotalArmLength = (distance posUpperArm_R posElbowStart_R) + (distance posElbowStart_R posElbowEnd_R) + (distance posElbowEnd_R posHand_R)

posArmUpV_R = (posUpperArm_R + posHand_R)*0.5 + ArmUpVec_R*TotalArmLength*0.6
posArmUpV_L = [-posArmUpV_R.x, posArmUpV_R.y, posArmUpV_R.z]

nShoulderXVec_R = bgShoulder.transform.row1
nShoulderZVec_R = bgShoulder.transform.row3
nShoulderXVec_L = [-nShoulderXVec_R.x, nShoulderXVec_R.y, nShoulderXVec_R.z]
nShoulderZVec_L = [-nShoulderZVec_R.x, nShoulderZVec_R.y, nShoulderZVec_R.z]

refSizeHand = bgHand.length * bgHand.transform.scale.x

nHandXVec_R = bgHand.transform.row1
nHandYVec_R = bgHand.transform.row2
nHandZVec_R = bgHand.transform.row3
nHandXVec_L = [-nHandXVec_R.x, nHandXVec_R.y, nHandXVec_R.z]
nHandYVec_L = [-nHandYVec_R.x, nHandYVec_R.y, nHandYVec_R.z]
nHandZVec_L = [-nHandZVec_R.x, nHandZVec_R.y, nHandZVec_R.z]

------Color setting------
	CtrlColor1_R = (color 6 134 6)
	CtrlColor1_L = (color 68 68 236)
	CtrlColor2_R = (color 30 180 30)
	CtrlColor2_L = (color 120 120 255)
	CtrlColor3_R = (color 141 176 18)
	CtrlColor3_L = (color 42 165 236)
	refColor1_R = (color 30 67 30)
	refColor1_L = (color 40 40 88)
------Point List-----
	ShoulderLength = bgShoulder.length * bgShoulder.transform.scale.x
	ShoulderWidth = bgShoulder.width * bgShoulder.transform.scale.y
	xStep = (0.5 * ShoulderLength)/12.0
	xInterval6 = ShoulderLength/6.0

	r = ShoulderWidth * 1
	ctrlShoulderPointList_R = #(
		--[((cos  120) + 1.5) * 2.5 * xInterval6, r*(cos  120),  r*(sin  120)],
		--[((cos  110) + 1.5) * 2.5 * xInterval6, r*(cos  110),  r*(sin  110)],
		--[((cos  100) + 1.5) * 2.5 * xInterval6, r*(cos  100),  r*(sin  100)],
		[((cos   90) + 1.5) * 2.5 * xInterval6, r*(cos   90),  r*(sin   90)],
		[((cos   80) + 1.5) * 2.5 * xInterval6, r*(cos   80),  r*(sin   80)],
		[((cos   70) + 1.5) * 2.5 * xInterval6, r*(cos   70),  r*(sin   70)],
		[((cos   60) + 1.5) * 2.5 * xInterval6, r*(cos   60),  r*(sin   60)],
		[((cos   50) + 1.5) * 2.5 * xInterval6, r*(cos   50),  r*(sin   50)],
		[((cos   40) + 1.5) * 2.5 * xInterval6, r*(cos   40),  r*(sin   40)],
		[((cos   30) + 1.5) * 2.5 * xInterval6, r*(cos   30),  r*(sin   30)],
		[((cos   20) + 1.5) * 2.5 * xInterval6, r*(cos   20),  r*(sin   20)],
		[((cos   10) + 1.5) * 2.5 * xInterval6, r*(cos   10),  r*(sin   10)],
		[((cos    0) + 1.5) * 2.5 * xInterval6, r*(cos    0),  r*(sin    0)],
		[((cos  -10) + 1.5) * 2.5 * xInterval6, r*(cos  -10),  r*(sin  -10)],
		[((cos  -20) + 1.5) * 2.5 * xInterval6, r*(cos  -20),  r*(sin  -20)],
		[((cos  -30) + 1.5) * 2.5 * xInterval6, r*(cos  -30),  r*(sin  -30)],
		[((cos  -40) + 1.5) * 2.5 * xInterval6, r*(cos  -40),  r*(sin  -40)],
		[((cos  -50) + 1.5) * 2.5 * xInterval6, r*(cos  -50),  r*(sin  -50)],
		[((cos  -60) + 1.5) * 2.5 * xInterval6, r*(cos  -60),  r*(sin  -60)],
		[((cos  -70) + 1.5) * 2.5 * xInterval6, r*(cos  -70),  r*(sin  -70)],
		[((cos  -80) + 1.5) * 2.5 * xInterval6, r*(cos  -80),  r*(sin  -80)],
		[((cos  -90) + 1.5) * 2.5 * xInterval6, r*(cos  -90),  r*(sin  -90)],
		--[((cos -100) + 1.5) * 2.5 * xInterval6, r*(cos -100),  r*(sin -100)],
		--[((cos -110) + 1.5) * 2.5 * xInterval6, r*(cos -110),  r*(sin -110)],
		--[((cos -120) + 1.5) * 2.5 * xInterval6, r*(cos -120),  r*(sin -120)],
		--[((cos -120) + 2.5) * 2.5 * xInterval6, r*(cos -120),  r*(sin -120)],
		--[((cos -110) + 2.5) * 2.5 * xInterval6, r*(cos -110),  r*(sin -110)],
		--[((cos -100) + 2.5) * 2.5 * xInterval6, r*(cos -100),  r*(sin -100)],
		[((cos  -90) + 2.5) * 2.5 * xInterval6, r*(cos  -90),  r*(sin  -90)],
		[((cos  -80) + 2.5) * 2.5 * xInterval6, r*(cos  -80),  r*(sin  -80)],
		[((cos  -70) + 2.5) * 2.5 * xInterval6, r*(cos  -70),  r*(sin  -70)],
		[((cos  -60) + 2.5) * 2.5 * xInterval6, r*(cos  -60),  r*(sin  -60)],
		[((cos  -50) + 2.5) * 2.5 * xInterval6, r*(cos  -50),  r*(sin  -50)],
		[((cos  -40) + 2.5) * 2.5 * xInterval6, r*(cos  -40),  r*(sin  -40)],
		[((cos  -30) + 2.5) * 2.5 * xInterval6, r*(cos  -30),  r*(sin  -30)],
		[((cos  -20) + 2.5) * 2.5 * xInterval6, r*(cos  -20),  r*(sin  -20)],
		[((cos  -10) + 2.5) * 2.5 * xInterval6, r*(cos  -10),  r*(sin  -10)],
		[((cos    0) + 2.5) * 2.5 * xInterval6, r*(cos    0),  r*(sin    0)],
		[((cos   10) + 2.5) * 2.5 * xInterval6, r*(cos   10),  r*(sin   10)],
		[((cos   20) + 2.5) * 2.5 * xInterval6, r*(cos   20),  r*(sin   20)],
		[((cos   30) + 2.5) * 2.5 * xInterval6, r*(cos   30),  r*(sin   30)],
		[((cos   40) + 2.5) * 2.5 * xInterval6, r*(cos   40),  r*(sin   40)],
		[((cos   50) + 2.5) * 2.5 * xInterval6, r*(cos   50),  r*(sin   50)],
		[((cos   60) + 2.5) * 2.5 * xInterval6, r*(cos   60),  r*(sin   60)],
		[((cos   70) + 2.5) * 2.5 * xInterval6, r*(cos   70),  r*(sin   70)],
		[((cos   80) + 2.5) * 2.5 * xInterval6, r*(cos   80),  r*(sin   80)],
		[((cos   90) + 2.5) * 2.5 * xInterval6, r*(cos   90),  r*(sin   90)]--,
		--[((cos  100) + 2.5) * 2.5 * xInterval6, r*(cos  100),  r*(sin  100)],
		--[((cos  110) + 2.5) * 2.5 * xInterval6, r*(cos  110),  r*(sin  110)],
		--[((cos  120) + 2.5) * 2.5 * xInterval6, r*(cos  120),  r*(sin  120)]
	)

	ctrlShoulderPointList_L = #()
	for i in ctrlShoulderPointList_R do (
		append ctrlShoulderPointList_L [i.x, -i.y, i.z]
	)

	r = 1.5
	CtrlFingerPointList = #(
		[0, r*(sin 0), r*(cos 0)],
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
		[0, r*(sin 330), r*(cos 330)]
	)

	r = 2.2
	CtrlFinger0PointList = #(
		[0, r*(sin 0), r*(cos 0)],
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
		[0, r*(sin 330), r*(cos 330)]
	)

	r = 8
	CtrlArmFKPointList = #(
		[0, r*(sin 0), r*(cos 0)],
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
		[0, r*(sin 330), r*(cos 330)]
	)

	r = 6
	CtrlHandFKPointList = #(
		[0, r*(sin 0), r*(cos 0)],
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
		[0, r*(sin 330), r*(cos 330)]
	)

	CtrlSubFingerPointList = #(
		[ 0.000000, 2.569870, 0.000000],
		[-0.841330, 2.536820, 0.257254],
		[-1.111470, 2.511760, 0.787313],
		[-1.307650, 2.343010, 3.428440],
		[-1.328330, 1.767110, 4.619120],
		[-1.347200, 0.612108, 5.252680],
		[-1.350600,-0.617018, 5.252680],
		[-1.338020,-1.772020, 4.619130],
		[-1.323470,-2.348150, 3.428440],
		[-1.134020,-2.518450, 0.782361],
		[-0.895811,-2.539270, 0.257258],
		[ 0.000000,-2.570000, 0.000000],
		[ 0.895811,-2.539270, 0.257258],
		[ 1.134020,-2.518450, 0.782360],
		[ 1.323470,-2.348150, 3.428440],
		[ 1.338020,-1.772020, 4.619130],
		[ 1.350600,-0.617018, 5.252680],
		[ 1.347200, 0.612108, 5.252680],
		[ 1.328330, 1.767110, 4.619120],
		[ 1.307650, 2.343010, 3.428440],
		[ 1.111470, 2.511760, 0.787313],
		[ 0.841330, 2.536820, 0.257254]
	)
------------------ Shoulder R ------------------
	locShoulder_R = point name:"locShoulder_R" pos:posShoulder_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	locShoulder_R.parent = ChestFixNode
	hideLayer.addNode locShoulder_R

	ShoulderRoot_R = point name:"ShoulderRoot_R" pos:posShoulder_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	ShoulderRoot_R.transform = getAimMatrix 1 nShoulderXVec_R 3 nShoulderZVec_R posShoulder_R
	ShoulderRoot_R.parent = ChestNode
	ShoulderRoot_R.pos.controller = Position_Constraint()
	ShoulderRoot_R.pos.controller.appendtarget locShoulder_R 50
	hideLayer.addNode ShoulderRoot_R

	ctrlShoulder_R = createLineCtrl ctrlShoulderPointList_R true
	ctrlShoulder_R.name = "Ctrl_Shoulder_R"
	ctrlShoulder_R.transform = getAimMatrix 1 nShoulderXVec_R 3 nShoulderZVec_R posShoulder_R
	ctrlShoulder_R.wireColor = CtrlColor1_R
	ctrlShoulder_R.parent = ShoulderRoot_R
	ctrlShoulder_R.position.controller = SlavePos()
	ctrlShoulder_R.scale.controller = SlaveScale()
	layer.addNode ctrlShoulder_R
------------------ Shoulder L ------------------
	locShoulder_L = point name:"locShoulder_L" pos:posShoulder_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	locShoulder_L.parent = ChestFixNode
	hideLayer.addNode locShoulder_L

	ShoulderRoot_L = point name:"ShoulderRoot_L" pos:posShoulder_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	ShoulderRoot_L.transform = getAimMatrix 1 nShoulderXVec_L 3 nShoulderZVec_L posShoulder_L
	ShoulderRoot_L.parent = ChestNode
	ShoulderRoot_L.pos.controller = Position_Constraint()
	ShoulderRoot_L.pos.controller.appendtarget locShoulder_L 50
	hideLayer.addNode ShoulderRoot_L

	--ctrlShoulder_L = createLineCtrl ctrlShoulderPointList_L true
	ctrlShoulder_L = GenSymObject ctrlShoulder_R "all"
	ctrlShoulder_L.name = "Ctrl_Shoulder_L"
	--ctrlShoulder_L.transform = getAimMatrix 1 nShoulderXVec_L 3 nShoulderZVec_L posShoulder_L
	ctrlShoulder_L.wireColor = CtrlColor1_L
	ctrlShoulder_L.parent = ShoulderRoot_L
	ctrlShoulder_L.position.controller = SlavePos()
	ctrlShoulder_L.scale.controller = SlaveScale()
	layer.addNode ctrlShoulder_L
------------------ Arm R ------------------
	ArmRoot_R = point name:"ArmRoot_R" pos:posUpperArm_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	ArmRoot_R.parent = ctrlShoulder_R
	ArmRoot_R.rotation.controller.value = (quat 0 0 0 1)
	hideLayer.addNode ArmRoot_R

	ArmBoneList_R = #()
	boneUpperArm_R = BoneSys.createBone posUpperArm_R posElbowStart_R [0,1,0]
	append ArmBoneList_R boneUpperArm_R
	hideLayer.addNode boneUpperArm_R
	boneUpperArm_R.transform = getAimMatrix 1 nUpperArmVec_R 3 ArmUpVec_R posUpperArm_R
	boneUpperArm_R.parent = ArmRoot_R

	CustAttributes.add boneUpperArm_R TransformInfoCA
	boneUpperArm_R.Roll.controller = float_script()
	boneUpperArm_R.Roll.controller.IScriptCtrl.AddNode "Parent" ArmRoot_R
	boneUpperArm_R.Roll.controller.IScriptCtrl.AddNode "self" boneUpperArm_R
	boneUpperArm_R.Roll.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
															"RollEuler = quatToEuler (Quat locQuat.x 0 0 locQuat.w)\n" + \
															"return RollEuler.x")

	boneUpperArm_R.Yaw.controller = float_script()
	boneUpperArm_R.Yaw.controller.IScriptCtrl.AddNode "Parent" ArmRoot_R
	boneUpperArm_R.Yaw.controller.IScriptCtrl.AddNode "self" boneUpperArm_R
	boneUpperArm_R.Yaw.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
															"YawEuler = quatToEuler (Quat 0 locQuat.y 0 locQuat.w)\n" + \
															"return YawEuler.y")

	boneUpperArm_R.Pitch.controller = float_script()
	boneUpperArm_R.Pitch.controller.IScriptCtrl.AddNode "Parent" ArmRoot_R
	boneUpperArm_R.Pitch.controller.IScriptCtrl.AddNode "self" boneUpperArm_R
	boneUpperArm_R.Pitch.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
															"PitchEuler = quatToEuler (Quat 0 0 locQuat.z locQuat.w)\n" + \
															"return PitchEuler.z")

	boneElbow_R = BoneSys.createBone posElbowStart_R posElbowEnd_R [0,1,0]
	append ArmBoneList_R boneElbow_R
	hideLayer.addNode boneElbow_R
	boneElbow_R.transform = getAimMatrix 1 (posElbowEnd_R - posElbowStart_R) 3 ArmUpVec_R posElbowStart_R
	boneElbow_R.parent = boneUpperArm_R

	boneForeArm_R  = BoneSys.createBone posElbowEnd_R posHand_R [0,1,0]
	append ArmBoneList_R boneForeArm_R
	hideLayer.addNode boneForeArm_R
	boneForeArm_R.transform = getAimMatrix 1 nForeArmVec_R 3 ArmUpVec_R posElbowEnd_R
	boneForeArm_R.parent = boneElbow_R

	boneHand_R = BoneSys.createBone posHand_R posHand_R [0,1,0]
	append ArmBoneList_R boneHand_R
	hideLayer.addNode boneHand_R
	boneHand_R.parent = boneForeArm_R
	boneHand_R.transform = getAimMatrix 1 nHandXVec_R 3 nHandZVec_R posHand_R
	boneHand_R.length = bgHand.length*bgHand.transform.scale.x
	fixRotation boneHand_R

	CustAttributes.add boneHand_R TransformInfoCA
	boneHand_R.Roll.controller = float_script()
	boneHand_R.Roll.controller.IScriptCtrl.AddNode "Parent" boneForeArm_R
	boneHand_R.Roll.controller.IScriptCtrl.AddNode "self" boneHand_R
	boneHand_R.Roll.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
															"RollEuler = quatToEuler (Quat locQuat.x 0 0 locQuat.w)\n" + \
															"return RollEuler.x")

	for b in ArmBoneList_R do(
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
	boneElbow_R.width = ElbowRadius * 2
	boneElbow_R.height = ElbowRadius * 2

	ArmIKLoc_R = point name:"ArmIKLoc_R" pos:posHand_R size:2 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	CustAttributes.add ArmIKLoc_R IKInfoCA
	ArmIKLoc_R.parent = CtrlRoot

	ArmIKLoc_R.length.controller = float_script()
	ArmIKLoc_R.length.controller.IScriptCtrl.AddNode "Node0" ArmRoot_R
	ArmIKLoc_R.length.controller.IScriptCtrl.AddNode "Node1" ArmIKLoc_R
	scriptStr = "distance Node0.transform.pos Node1.transform.pos"
	ArmIKLoc_R.length.controller.IScriptCtrl.SetExpression scriptStr
	ArmIKLoc_R.Length.controller = float_limit()
	ArmIKLoc_R.Length.controller.upper_limit = TotalArmLength
	ArmIKLoc_R.Length.controller.upper_smoothing = TotalArmLength*0.01
	ArmIKLoc_R.useSoftIK.controller = On_Off()
	ArmIKLoc_R.useSoftIK = off

	ArmIKHold_R = IKSys.ikChain boneUpperArm_R boneHand_R "IKHISolver"

	pyArmIK_R = point name:"pyArmIK_R" pos:posFoot_R size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	pyArmIK_R.parent = CtrlRoot
	pyArmIK_R.pos.controller = position_script()
	pyArmIK_R.pos.controller.IScriptCtrl.AddNode "Parent" CtrlRoot
	pyArmIK_R.pos.controller.IScriptCtrl.AddNode "Node0" ArmRoot_R
	pyArmIK_R.pos.controller.IScriptCtrl.AddNode "Node1" ArmIKLoc_R
	pyArmIK_R.pos.controller.IScriptCtrl.AddTarget "Length" ArmIKLoc_R.length.controller
	pyArmIK_R.pos.controller.IScriptCtrl.AddTarget "sw" ArmIKLoc_R.useSoftIK.controller
	scriptStr = "vec = normalize (Node1.transform.pos - Node0.transform.pos)\n" + \
				"wPos = vec * Length + Node0.transform.pos\n" + \
				"if sw then return wPos * (inverse Parent.transform)\n" + \
				"else return Node1.transform.pos * (inverse Parent.transform)"
	pyArmIK_R.pos.controller.IScriptCtrl.SetExpression scriptStr
	ArmIKHold_R.parent = pyArmIK_R
	ArmIKHold_R.pos.controller.value = [0,0,0]

	pyArmUpV_R = point name:"pyArmUpV_R" pos:posArmUpV_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	ArmIKHold_R.transform.controller.VHTarget = pyArmUpV_R
	pyArmUpV_R.parent = CtrlRoot

	hideLayer.addNode ArmIKLoc_R
	hideLayer.addNode ArmIKHold_R
	hideLayer.addNode pyArmIK_R
	hideLayer.addNode pyArmUpV_R
------------------ Arm L ------------------
	ArmRoot_L = point name:"ArmRoot_L" pos:posUpperArm_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	ArmRoot_L.parent = ctrlShoulder_L
	--ArmRoot_L.rotation.controller.value = (quat 0 0 0 1)
	ArmRoot_L.transform = getAimMatrix 1 nShoulderXVec_L 3 nShoulderZVec_L posUpperArm_L
	hideLayer.addNode ArmRoot_L

	ArmBoneList_L = #()
	boneUpperArm_L = BoneSys.createBone posUpperArm_L posElbowStart_L [0,1,0]
	append ArmBoneList_L boneUpperArm_L
	hideLayer.addNode boneUpperArm_L
	boneUpperArm_L.transform = getAimMatrix 1 nUpperArmVec_L 3 ArmUpVec_L posUpperArm_L
	boneUpperArm_L.parent = ArmRoot_L

	CustAttributes.add boneUpperArm_L TransformInfoCA
	boneUpperArm_L.Roll.controller = float_script()
	boneUpperArm_L.Roll.controller.IScriptCtrl.AddNode "Parent" ArmRoot_L
	boneUpperArm_L.Roll.controller.IScriptCtrl.AddNode "self" boneUpperArm_L
	boneUpperArm_L.Roll.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
															"RollEuler = quatToEuler (Quat locQuat.x 0 0 locQuat.w)\n" + \
															"return RollEuler.x")

	boneUpperArm_L.Yaw.controller = float_script()
	boneUpperArm_L.Yaw.controller.IScriptCtrl.AddNode "Parent" ArmRoot_L
	boneUpperArm_L.Yaw.controller.IScriptCtrl.AddNode "self" boneUpperArm_L
	boneUpperArm_L.Yaw.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
															"YawEuler = quatToEuler (Quat 0 locQuat.y 0 locQuat.w)\n" + \
															"return YawEuler.y")

	boneUpperArm_L.Pitch.controller = float_script()
	boneUpperArm_L.Pitch.controller.IScriptCtrl.AddNode "Parent" ArmRoot_L
	boneUpperArm_L.Pitch.controller.IScriptCtrl.AddNode "self" boneUpperArm_L
	boneUpperArm_L.Pitch.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
															"PitchEuler = quatToEuler (Quat 0 0 locQuat.z locQuat.w)\n" + \
															"return PitchEuler.z")

	boneElbow_L = BoneSys.createBone posElbowStart_L posElbowEnd_L [0,1,0]
	append ArmBoneList_L boneElbow_L
	hideLayer.addNode boneElbow_L
	boneElbow_L.transform = getAimMatrix 1 (posElbowEnd_L - posElbowStart_L) 3 ArmUpVec_L posElbowStart_L
	boneElbow_L.parent = boneUpperArm_L

	boneForeArm_L  = BoneSys.createBone posElbowEnd_L posHand_L [0,1,0]
	append ArmBoneList_L boneForeArm_L
	hideLayer.addNode boneForeArm_L
	boneForeArm_L.transform = getAimMatrix 1 nForeArmVec_L 3 ArmUpVec_L posElbowEnd_L
	boneForeArm_L.parent = boneElbow_L

	boneHand_L = BoneSys.createBone posHand_L posHand_L [0,1,0]
	append ArmBoneList_L boneHand_L
	hideLayer.addNode boneHand_L
	boneHand_L.parent = boneForeArm_L
	boneHand_L.transform = getAimMatrix 1 nHandXVec_L 3 nHandZVec_L posHand_L
	boneHand_L.length = bgHand.length*bgHand.transform.scale.x
	fixRotation boneHand_L

	CustAttributes.add boneHand_L TransformInfoCA
	boneHand_L.Roll.controller = float_script()
	boneHand_L.Roll.controller.IScriptCtrl.AddNode "Parent" boneForeArm_L
	boneHand_L.Roll.controller.IScriptCtrl.AddNode "self" boneHand_L
	boneHand_L.Roll.controller.IScriptCtrl.SetExpression ("locQuat = (self.transform * (inverse Parent.transform)).rotation\n" + \
															"RollEuler = quatToEuler (Quat locQuat.x 0 0 locQuat.w)\n" + \
															"return RollEuler.x")

	for b in ArmBoneList_L do(
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
	boneElbow_L.width = ElbowRadius * 2
	boneElbow_L.height = ElbowRadius * 2

	ArmIKLoc_L = point name:"ArmIKLoc_L" pos:posHand_L size:2 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	CustAttributes.add ArmIKLoc_L IKInfoCA
	ArmIKLoc_L.parent = CtrlRoot

	ArmIKLoc_L.length.controller = float_script()
	ArmIKLoc_L.length.controller.IScriptCtrl.AddNode "Node0" ArmRoot_L
	ArmIKLoc_L.length.controller.IScriptCtrl.AddNode "Node1" ArmIKLoc_L
	scriptStr = "distance Node0.transform.pos Node1.transform.pos"
	ArmIKLoc_L.length.controller.IScriptCtrl.SetExpression scriptStr
	ArmIKLoc_L.Length.controller = float_limit()
	ArmIKLoc_L.Length.controller.upper_limit = TotalArmLength
	ArmIKLoc_L.Length.controller.upper_smoothing = TotalArmLength*0.01
	ArmIKLoc_L.useSoftIK.controller = On_Off()
	ArmIKLoc_L.useSoftIK = off

	ArmIKHold_L = IKSys.ikChain boneUpperArm_L boneHand_L "IKHISolver"

	pyArmIK_L = point name:"pyArmIK_L" pos:posFoot_L size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	pyArmIK_L.parent = CtrlRoot
	pyArmIK_L.pos.controller = position_script()
	pyArmIK_L.pos.controller.IScriptCtrl.AddNode "Parent" CtrlRoot
	pyArmIK_L.pos.controller.IScriptCtrl.AddNode "Node0" ArmRoot_L
	pyArmIK_L.pos.controller.IScriptCtrl.AddNode "Node1" ArmIKLoc_L
	pyArmIK_L.pos.controller.IScriptCtrl.AddTarget "Length" ArmIKLoc_L.length.controller
	pyArmIK_L.pos.controller.IScriptCtrl.AddTarget "sw" ArmIKLoc_L.useSoftIK.controller
	scriptStr = "vec = normalize (Node1.transform.pos - Node0.transform.pos)\n" + \
				"wPos = vec * Length + Node0.transform.pos\n" + \
				"if sw then return wPos * (inverse Parent.transform)\n" + \
				"else return Node1.transform.pos * (inverse Parent.transform)"
	pyArmIK_L.pos.controller.IScriptCtrl.SetExpression scriptStr
	ArmIKHold_L.parent = pyArmIK_L
	ArmIKHold_L.pos.controller.value = [0,0,0]

	pyArmUpV_L = point name:"pyArmUpV_L" pos:posArmUpV_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	ArmIKHold_L.transform.controller.VHTarget = pyArmUpV_L
	pyArmUpV_L.parent = CtrlRoot

	hideLayer.addNode ArmIKLoc_L
	hideLayer.addNode ArmIKHold_L
	hideLayer.addNode pyArmIK_L
	hideLayer.addNode pyArmUpV_L
------------------ Arm Twist Bone R ----------------
	UpperArmTwistBoneList_R = createSegmentsBones posUpperArm_R posElbowStart_R 4

	for i = 1 to UpperArmTwistBoneList_R.count do (
		UpperArmTwistBoneList_R[i].wireColor = refColor1_R
		UpperArmTwistBoneList_R[i].parent = boneUpperArm_R
		UpperArmTwistBoneList_R[i].rotation.controller.value = (quat 0 0 0 1)
		UpperArmTwistBoneList_R[i].width = 4
		UpperArmTwistBoneList_R[i].height = 4
		UpperArmTwistBoneList_R[i].Taper = 50
		UpperArmTwistBoneList_R[i].sidefins = off
		UpperArmTwistBoneList_R[i].sidefinssize = 2
		UpperArmTwistBoneList_R[i].frontfin = off
		UpperArmTwistBoneList_R[i].frontfinsize = 2
		UpperArmTwistBoneList_R[i].backfin = off
		UpperArmTwistBoneList_R[i].backfinsize = 2
		UpperArmTwistBoneList_R[i].boneEnable = false
		hideLayer.addNode UpperArmTwistBoneList_R[i]

		UpperArmTwistBoneList_R[i].rotation.controller.X_Rotation.controller = float_script()
		UpperArmTwistBoneList_R[i].rotation.controller.X_Rotation.controller.IScriptCtrl.AddTarget "Roll" boneUpperArm_R.Roll.controller
		scriptStr = "-Roll * " + (((UpperArmTwistBoneList_R.count - i as float)/(UpperArmTwistBoneList_R.count - 1.0) * 0.01745329251994) as string)
		UpperArmTwistBoneList_R[i].rotation.controller.X_Rotation.controller.IScriptCtrl.SetExpression scriptStr
	)

	ForeArmTwistBoneList_R = createSegmentsBones posElbowEnd_R posHand_R 4

	for i = 1 to ForeArmTwistBoneList_R.count do (
		ForeArmTwistBoneList_R[i].wireColor = refColor1_R
		ForeArmTwistBoneList_R[i].parent = boneForeArm_R
		ForeArmTwistBoneList_R[i].rotation.controller.value = (quat 0 0 0 1)
		ForeArmTwistBoneList_R[i].width = 4
		ForeArmTwistBoneList_R[i].height = 4
		ForeArmTwistBoneList_R[i].Taper = 50
		ForeArmTwistBoneList_R[i].sidefins = off
		ForeArmTwistBoneList_R[i].sidefinssize = 2
		ForeArmTwistBoneList_R[i].frontfin = off
		ForeArmTwistBoneList_R[i].frontfinsize = 2
		ForeArmTwistBoneList_R[i].backfin = off
		ForeArmTwistBoneList_R[i].backfinsize = 2
		hideLayer.addNode ForeArmTwistBoneList_R[i]

		ForeArmTwistBoneList_R[i].rotation.controller.X_Rotation.controller = float_script()
		ForeArmTwistBoneList_R[i].rotation.controller.X_Rotation.controller.IScriptCtrl.AddTarget "Roll" boneHand_R.Roll.controller
		scriptStr = "Roll * " + ((((i - 1) as float)/(ForeArmTwistBoneList_R.count - 1.0) * 0.01745329251994) as string)
		ForeArmTwistBoneList_R[i].rotation.controller.X_Rotation.controller.IScriptCtrl.SetExpression scriptStr
	)
------------------ Arm Twist Bone L ----------------
	UpperArmTwistBoneList_L = createSegmentsBones posUpperArm_L posElbowStart_L 4

	for i = 1 to UpperArmTwistBoneList_L.count do (
		UpperArmTwistBoneList_L[i].wireColor = refColor1_L
		UpperArmTwistBoneList_L[i].parent = boneUpperArm_L
		UpperArmTwistBoneList_L[i].rotation.controller.value = (quat 0 0 0 1)
		UpperArmTwistBoneList_L[i].width = 4
		UpperArmTwistBoneList_L[i].height = 4
		UpperArmTwistBoneList_L[i].Taper = 50
		UpperArmTwistBoneList_L[i].sidefins = off
		UpperArmTwistBoneList_L[i].sidefinssize = 2
		UpperArmTwistBoneList_L[i].frontfin = off
		UpperArmTwistBoneList_L[i].frontfinsize = 2
		UpperArmTwistBoneList_L[i].backfin = off
		UpperArmTwistBoneList_L[i].backfinsize = 2
		hideLayer.addNode UpperArmTwistBoneList_L[i]

		UpperArmTwistBoneList_L[i].rotation.controller.X_Rotation.controller = float_script()
		UpperArmTwistBoneList_L[i].rotation.controller.X_Rotation.controller.IScriptCtrl.AddTarget "Roll" boneUpperArm_L.Roll.controller
		scriptStr = "-Roll * " + (((UpperArmTwistBoneList_L.count - i as float)/(UpperArmTwistBoneList_L.count - 1.0) * 0.01745329251994) as string)
		UpperArmTwistBoneList_L[i].rotation.controller.X_Rotation.controller.IScriptCtrl.SetExpression scriptStr
	)

	ForeArmTwistBoneList_L = createSegmentsBones posElbowEnd_L posHand_L 4

	for i = 1 to ForeArmTwistBoneList_L.count do (
		ForeArmTwistBoneList_L[i].wireColor = refColor1_L
		ForeArmTwistBoneList_L[i].parent = boneForeArm_L
		ForeArmTwistBoneList_L[i].rotation.controller.value = (quat 0 0 0 1)
		ForeArmTwistBoneList_L[i].width = 4
		ForeArmTwistBoneList_L[i].height = 4
		ForeArmTwistBoneList_L[i].Taper = 50
		ForeArmTwistBoneList_L[i].sidefins = off
		ForeArmTwistBoneList_L[i].sidefinssize = 2
		ForeArmTwistBoneList_L[i].frontfin = off
		ForeArmTwistBoneList_L[i].frontfinsize = 2
		ForeArmTwistBoneList_L[i].backfin = off
		ForeArmTwistBoneList_L[i].backfinsize = 2
		hideLayer.addNode ForeArmTwistBoneList_L[i]

		ForeArmTwistBoneList_L[i].rotation.controller.X_Rotation.controller = float_script()
		ForeArmTwistBoneList_L[i].rotation.controller.X_Rotation.controller.IScriptCtrl.AddTarget "Roll" boneHand_L.Roll.controller
		scriptStr = "Roll * " + ((((i - 1) as float)/(ForeArmTwistBoneList_L.count - 1.0) * 0.01745329251994) as string)
		ForeArmTwistBoneList_L[i].rotation.controller.X_Rotation.controller.IScriptCtrl.SetExpression scriptStr
	)
------------------ Fingers R ----------------------
	posSubFinger_R = posHand_R * 0.33 + posFinger20_R * 0.67
	xVecSubFinger_R = normalize (posFinger20_R - posHand_R)
	zVecSubFinger_R = boneHand_R.transform.row3
	subFingerRoot_R = point name:"subFingerRoot_R" pos:posSubFinger_R size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	subFingerRoot_R.transform = getAimMatrix 1 xVecSubFinger_R 3 zVecSubFinger_R posSubFinger_R
	subFingerRoot_R.parent = boneHand_R
	fixRotation subFingerRoot_R
	hideLayer.addNode subFingerRoot_R

	CtrlSubFinger_R = createLineCtrl CtrlSubFingerPointList true
	CtrlSubFinger_R.name = "Ctrl_SubFingers_R"
	CtrlSubFinger_R.wireColor = CtrlColor1_R
	CtrlSubFinger_R.transform = subFingerRoot_R.transform
	CtrlSubFinger_R.parent = boneHand_R
	fixRotation CtrlSubFinger_R
	layer.addNode CtrlSubFinger_R
	subFingerRoot_R.rotation.controller =  Orientation_Constraint()
	subFingerRoot_R.rotation.controller.appendtarget CtrlSubFinger_R 50
	locPos = CtrlSubFinger_R.pos.controller.value
	locRot = CtrlSubFinger_R.rotation.controller.value
	CtrlSubFinger_R.pos.controller = position_script()
	CtrlSubFinger_R.pos.controller.IScriptCtrl.SetExpression (locPos as string)
	CtrlSubFinger_R.scale.controller = SlaveScale()

	lpFinger3_R = point name:"lpFinger3_R" pos:posFinger30_R size:0.5 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	lpFinger4_R = point name:"lpFinger4_R" pos:posFinger40_R size:0.5 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	lpFinger3_R.parent = subFingerRoot_R
	lpFinger4_R.parent = subFingerRoot_R
	hideLayer.addNode lpFinger3_R
	hideLayer.addNode lpFinger4_R

	Finger0Root_R = point name:"Finger0Root_R" pos:posFinger00_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	Finger1Root_R = point name:"Finger1Root_R" pos:posFinger10_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	Finger2Root_R = point name:"Finger2Root_R" pos:posFinger20_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	Finger3Root_R = point name:"Finger3Root_R" pos:posFinger30_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	Finger4Root_R = point name:"Finger4Root_R" pos:posFinger40_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	Finger0Root_R.transform = getAimMatrix 1 xVecFinger00_R 3 zVecFinger00_R posFinger00_R
	Finger1Root_R.transform = getAimMatrix 1 xVecFinger10_R 3 zVecFinger10_R posFinger10_R
	Finger2Root_R.transform = getAimMatrix 1 xVecFinger20_R 3 zVecFinger20_R posFinger20_R
	Finger3Root_R.transform = getAimMatrix 1 xVecFinger30_R 3 zVecFinger30_R posFinger30_R
	Finger4Root_R.transform = getAimMatrix 1 xVecFinger40_R 3 zVecFinger40_R posFinger40_R
	Finger0Root_R.parent = boneHand_R
	Finger1Root_R.parent = boneHand_R
	Finger2Root_R.parent = boneHand_R
	Finger3Root_R.parent = boneHand_R
	Finger4Root_R.parent = boneHand_R
	hideLayer.addNode Finger0Root_R
	hideLayer.addNode Finger1Root_R
	hideLayer.addNode Finger2Root_R
	hideLayer.addNode Finger3Root_R
	hideLayer.addNode Finger4Root_R

	Finger3Root_R.pos.controller = Position_Constraint()
	Finger3Root_R.pos.controller.appendtarget lpFinger3_R 50
	Finger4Root_R.pos.controller = Position_Constraint()
	Finger4Root_R.pos.controller.appendtarget lpFinger4_R 50

	CtrlFinger00_R = createLineCtrl CtrlFinger0PointList true
	CtrlFinger00_R.name = "Ctrl_Finger00_R"
	CtrlFinger00_R.wireColor = CtrlColor2_R
	CtrlFinger00_R.transform = getAimMatrix 1 xVecFinger00_R 3 zVecFinger00_R posFinger00_R
	CtrlFinger00_R.parent = Finger0Root_R
	fixRotation CtrlFinger00_R
	layer.addNode CtrlFinger00_R

	CtrlFinger10_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger10_R.name = "Ctrl_Finger10_R"
	CtrlFinger10_R.wireColor = CtrlColor2_R
	CtrlFinger10_R.transform = getAimMatrix 1 xVecFinger10_R 3 zVecFinger10_R posFinger10_R
	CtrlFinger10_R.parent = Finger1Root_R
	fixRotation CtrlFinger10_R
	layer.addNode CtrlFinger10_R

	CtrlFinger20_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger20_R.name = "Ctrl_Finger20_R"
	CtrlFinger20_R.wireColor = CtrlColor2_R
	CtrlFinger20_R.transform = getAimMatrix 1 xVecFinger20_R 3 zVecFinger20_R posFinger20_R
	CtrlFinger20_R.parent = Finger2Root_R
	fixRotation CtrlFinger20_R
	layer.addNode CtrlFinger20_R

	CtrlFinger30_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger30_R.name = "Ctrl_Finger30_R"
	CtrlFinger30_R.wireColor = CtrlColor2_R
	CtrlFinger30_R.transform = getAimMatrix 1 xVecFinger30_R 3 zVecFinger30_R posFinger30_R
	CtrlFinger30_R.parent = Finger3Root_R
	fixRotation CtrlFinger30_R
	layer.addNode CtrlFinger30_R

	CtrlFinger40_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger40_R.name = "Ctrl_Finger40_R"
	CtrlFinger40_R.wireColor = CtrlColor2_R
	CtrlFinger40_R.transform = getAimMatrix 1 xVecFinger40_R 3 zVecFinger40_R posFinger40_R
	CtrlFinger40_R.parent = Finger4Root_R
	fixRotation CtrlFinger40_R
	layer.addNode CtrlFinger40_R

	CtrlFinger01_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger02_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger11_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger12_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger21_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger22_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger31_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger32_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger41_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger42_R = createLineCtrl CtrlFingerPointList true
	CtrlFinger01_R.name = "Ctrl_Finger01_R"
	CtrlFinger02_R.name = "Ctrl_Finger02_R"
	CtrlFinger11_R.name = "Ctrl_Finger11_R"
	CtrlFinger12_R.name = "Ctrl_Finger12_R"
	CtrlFinger21_R.name = "Ctrl_Finger21_R"
	CtrlFinger22_R.name = "Ctrl_Finger22_R"
	CtrlFinger31_R.name = "Ctrl_Finger31_R"
	CtrlFinger32_R.name = "Ctrl_Finger32_R"
	CtrlFinger41_R.name = "Ctrl_Finger41_R"
	CtrlFinger42_R.name = "Ctrl_Finger42_R"
	CtrlFinger01_R.wireColor = CtrlColor2_R
	CtrlFinger02_R.wireColor = CtrlColor2_R
	CtrlFinger11_R.wireColor = CtrlColor2_R
	CtrlFinger12_R.wireColor = CtrlColor2_R
	CtrlFinger21_R.wireColor = CtrlColor2_R
	CtrlFinger22_R.wireColor = CtrlColor2_R
	CtrlFinger31_R.wireColor = CtrlColor2_R
	CtrlFinger32_R.wireColor = CtrlColor2_R
	CtrlFinger41_R.wireColor = CtrlColor2_R
	CtrlFinger42_R.wireColor = CtrlColor2_R
	CtrlFinger01_R.transform = getAimMatrix 1 xVecFinger01_R 3 zVecFinger01_R posFinger01_R
	CtrlFinger02_R.transform = getAimMatrix 1 xVecFinger02_R 3 zVecFinger02_R posFinger02_R
	CtrlFinger11_R.transform = getAimMatrix 1 xVecFinger11_R 3 zVecFinger11_R posFinger11_R
	CtrlFinger12_R.transform = getAimMatrix 1 xVecFinger12_R 3 zVecFinger12_R posFinger12_R
	CtrlFinger21_R.transform = getAimMatrix 1 xVecFinger21_R 3 zVecFinger21_R posFinger21_R
	CtrlFinger22_R.transform = getAimMatrix 1 xVecFinger22_R 3 zVecFinger22_R posFinger22_R
	CtrlFinger31_R.transform = getAimMatrix 1 xVecFinger31_R 3 zVecFinger31_R posFinger31_R
	CtrlFinger32_R.transform = getAimMatrix 1 xVecFinger32_R 3 zVecFinger32_R posFinger32_R
	CtrlFinger41_R.transform = getAimMatrix 1 xVecFinger41_R 3 zVecFinger41_R posFinger41_R
	CtrlFinger42_R.transform = getAimMatrix 1 xVecFinger42_R 3 zVecFinger42_R posFinger42_R
	fixRotation CtrlFinger01_R
	fixRotation CtrlFinger02_R
	fixRotation CtrlFinger11_R
	fixRotation CtrlFinger12_R
	fixRotation CtrlFinger21_R
	fixRotation CtrlFinger22_R
	fixRotation CtrlFinger31_R
	fixRotation CtrlFinger32_R
	fixRotation CtrlFinger41_R
	fixRotation CtrlFinger42_R
	layer.addNode CtrlFinger01_R
	layer.addNode CtrlFinger02_R
	layer.addNode CtrlFinger11_R
	layer.addNode CtrlFinger12_R
	layer.addNode CtrlFinger21_R
	layer.addNode CtrlFinger22_R
	layer.addNode CtrlFinger31_R
	layer.addNode CtrlFinger32_R
	layer.addNode CtrlFinger41_R
	layer.addNode CtrlFinger42_R
	CtrlFinger01_R.parent = CtrlFinger00_R
	CtrlFinger02_R.parent = CtrlFinger01_R
	CtrlFinger11_R.parent = CtrlFinger10_R
	CtrlFinger12_R.parent = CtrlFinger11_R
	CtrlFinger21_R.parent = CtrlFinger20_R
	CtrlFinger22_R.parent = CtrlFinger21_R
	CtrlFinger31_R.parent = CtrlFinger30_R
	CtrlFinger32_R.parent = CtrlFinger31_R
	CtrlFinger41_R.parent = CtrlFinger40_R
	CtrlFinger42_R.parent = CtrlFinger41_R
	locFingerPos00_R = CtrlFinger00_R.pos.controller.value
	locFingerPos01_R = CtrlFinger01_R.pos.controller.value
	locFingerPos02_R = CtrlFinger02_R.pos.controller.value
	locFingerPos10_R = CtrlFinger10_R.pos.controller.value
	locFingerPos11_R = CtrlFinger11_R.pos.controller.value
	locFingerPos12_R = CtrlFinger12_R.pos.controller.value
	locFingerPos20_R = CtrlFinger20_R.pos.controller.value
	locFingerPos21_R = CtrlFinger21_R.pos.controller.value
	locFingerPos22_R = CtrlFinger22_R.pos.controller.value
	locFingerPos30_R = CtrlFinger30_R.pos.controller.value
	locFingerPos31_R = CtrlFinger31_R.pos.controller.value
	locFingerPos32_R = CtrlFinger32_R.pos.controller.value
	locFingerPos40_R = CtrlFinger40_R.pos.controller.value
	locFingerPos41_R = CtrlFinger41_R.pos.controller.value
	locFingerPos42_R = CtrlFinger42_R.pos.controller.value
	CtrlFinger00_R.pos.controller = position_script()
	CtrlFinger01_R.pos.controller = position_script()
	CtrlFinger02_R.pos.controller = position_script()
	CtrlFinger10_R.pos.controller = position_script()
	CtrlFinger11_R.pos.controller = position_script()
	CtrlFinger12_R.pos.controller = position_script()
	CtrlFinger20_R.pos.controller = position_script()
	CtrlFinger21_R.pos.controller = position_script()
	CtrlFinger22_R.pos.controller = position_script()
	CtrlFinger30_R.pos.controller = position_script()
	CtrlFinger31_R.pos.controller = position_script()
	CtrlFinger32_R.pos.controller = position_script()
	CtrlFinger40_R.pos.controller = position_script()
	CtrlFinger41_R.pos.controller = position_script()
	CtrlFinger42_R.pos.controller = position_script()
	CtrlFinger00_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos00_R as string)
	CtrlFinger01_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos01_R as string)
	CtrlFinger02_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos02_R as string)
	CtrlFinger10_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos10_R as string)
	CtrlFinger11_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos11_R as string)
	CtrlFinger12_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos12_R as string)
	CtrlFinger20_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos20_R as string)
	CtrlFinger21_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos21_R as string)
	CtrlFinger22_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos22_R as string)
	CtrlFinger30_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos30_R as string)
	CtrlFinger31_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos31_R as string)
	CtrlFinger32_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos32_R as string)
	CtrlFinger40_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos40_R as string)
	CtrlFinger41_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos41_R as string)
	CtrlFinger42_R.pos.controller.IScriptCtrl.SetExpression (locFingerPos42_R as string)
	CtrlFinger00_R.scale.controller = SlaveScale()
	CtrlFinger01_R.scale.controller = SlaveScale()
	CtrlFinger02_R.scale.controller = SlaveScale()
	CtrlFinger10_R.scale.controller = SlaveScale()
	CtrlFinger11_R.scale.controller = SlaveScale()
	CtrlFinger12_R.scale.controller = SlaveScale()
	CtrlFinger20_R.scale.controller = SlaveScale()
	CtrlFinger21_R.scale.controller = SlaveScale()
	CtrlFinger22_R.scale.controller = SlaveScale()
	CtrlFinger30_R.scale.controller = SlaveScale()
	CtrlFinger31_R.scale.controller = SlaveScale()
	CtrlFinger32_R.scale.controller = SlaveScale()
	CtrlFinger40_R.scale.controller = SlaveScale()
	CtrlFinger41_R.scale.controller = SlaveScale()
	CtrlFinger42_R.scale.controller = SlaveScale()
------------------ Fingers L ----------------------
	posSubFinger_L = posHand_L * 0.33 + posFinger20_L * 0.67
	xVecSubFinger_L = normalize (posFinger20_L - posHand_L)
	zVecSubFinger_L = boneHand_L.transform.row3
	subFingerRoot_L = point name:"subFingerRoot_L" pos:posSubFinger_L size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	subFingerRoot_L.transform = getAimMatrix 1 xVecSubFinger_L 3 zVecSubFinger_L posSubFinger_L
	subFingerRoot_L.parent = boneHand_L
	fixRotation subFingerRoot_L
	hideLayer.addNode subFingerRoot_L

	CtrlSubFinger_L = createLineCtrl CtrlSubFingerPointList true
	CtrlSubFinger_L.name = "Ctrl_SubFingers_L"
	CtrlSubFinger_L.wireColor = CtrlColor1_L
	CtrlSubFinger_L.transform = subFingerRoot_L.transform
	CtrlSubFinger_L.parent = boneHand_L
	fixRotation CtrlSubFinger_L
	layer.addNode CtrlSubFinger_L
	subFingerRoot_L.rotation.controller =  Orientation_Constraint()
	subFingerRoot_L.rotation.controller.appendtarget CtrlSubFinger_L 50
	locPos = CtrlSubFinger_L.pos.controller.value
	locRot = CtrlSubFinger_L.rotation.controller.value
	CtrlSubFinger_L.pos.controller = position_script()
	CtrlSubFinger_L.pos.controller.IScriptCtrl.SetExpression (locPos as string)
	CtrlSubFinger_L.scale.controller = SlaveScale()

	lpFinger3_L = point name:"lpFinger3_L" pos:posFinger30_L size:0.5 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	lpFinger4_L = point name:"lpFinger4_L" pos:posFinger40_L size:0.5 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	lpFinger3_L.parent = subFingerRoot_L
	lpFinger4_L.parent = subFingerRoot_L
	hideLayer.addNode lpFinger3_L
	hideLayer.addNode lpFinger4_L

	Finger0Root_L = point name:"Finger0Root_L" pos:posFinger00_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	Finger1Root_L = point name:"Finger1Root_L" pos:posFinger10_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	Finger2Root_L = point name:"Finger2Root_L" pos:posFinger20_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	Finger3Root_L = point name:"Finger3Root_L" pos:posFinger30_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	Finger4Root_L = point name:"Finger4Root_L" pos:posFinger40_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	Finger0Root_L.transform = getAimMatrix 1 xVecFinger00_L 3 zVecFinger00_L posFinger00_L
	Finger1Root_L.transform = getAimMatrix 1 xVecFinger10_L 3 zVecFinger10_L posFinger10_L
	Finger2Root_L.transform = getAimMatrix 1 xVecFinger20_L 3 zVecFinger20_L posFinger20_L
	Finger3Root_L.transform = getAimMatrix 1 xVecFinger30_L 3 zVecFinger30_L posFinger30_L
	Finger4Root_L.transform = getAimMatrix 1 xVecFinger40_L 3 zVecFinger40_L posFinger40_L
	Finger0Root_L.parent = boneHand_L
	Finger1Root_L.parent = boneHand_L
	Finger2Root_L.parent = boneHand_L
	Finger3Root_L.parent = boneHand_L
	Finger4Root_L.parent = boneHand_L
	hideLayer.addNode Finger0Root_L
	hideLayer.addNode Finger1Root_L
	hideLayer.addNode Finger2Root_L
	hideLayer.addNode Finger3Root_L
	hideLayer.addNode Finger4Root_L

	Finger3Root_L.pos.controller = Position_Constraint()
	Finger3Root_L.pos.controller.appendtarget lpFinger3_L 50
	Finger4Root_L.pos.controller = Position_Constraint()
	Finger4Root_L.pos.controller.appendtarget lpFinger4_L 50

	CtrlFinger00_L = createLineCtrl CtrlFinger0PointList true
	CtrlFinger00_L.name = "Ctrl_Finger00_L"
	CtrlFinger00_L.wireColor = CtrlColor2_L
	CtrlFinger00_L.transform = getAimMatrix 1 xVecFinger00_L 3 zVecFinger00_L posFinger00_L
	CtrlFinger00_L.parent = Finger0Root_L
	fixRotation CtrlFinger00_L
	layer.addNode CtrlFinger00_L

	CtrlFinger10_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger10_L.name = "Ctrl_Finger10_L"
	CtrlFinger10_L.wireColor = CtrlColor2_L
	CtrlFinger10_L.transform = getAimMatrix 1 xVecFinger10_L 3 zVecFinger10_L posFinger10_L
	CtrlFinger10_L.parent = Finger1Root_L
	fixRotation CtrlFinger10_L
	layer.addNode CtrlFinger10_L

	CtrlFinger20_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger20_L.name = "Ctrl_Finger20_L"
	CtrlFinger20_L.wireColor = CtrlColor2_L
	CtrlFinger20_L.transform = getAimMatrix 1 xVecFinger20_L 3 zVecFinger20_L posFinger20_L
	CtrlFinger20_L.parent = Finger2Root_L
	fixRotation CtrlFinger20_L
	layer.addNode CtrlFinger20_L

	CtrlFinger30_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger30_L.name = "Ctrl_Finger30_L"
	CtrlFinger30_L.wireColor = CtrlColor2_L
	CtrlFinger30_L.transform = getAimMatrix 1 xVecFinger30_L 3 zVecFinger30_L posFinger30_L
	CtrlFinger30_L.parent = Finger3Root_L
	fixRotation CtrlFinger30_L
	layer.addNode CtrlFinger30_L

	CtrlFinger40_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger40_L.name = "Ctrl_Finger40_L"
	CtrlFinger40_L.wireColor = CtrlColor2_L
	CtrlFinger40_L.transform = getAimMatrix 1 xVecFinger40_L 3 zVecFinger40_L posFinger40_L
	CtrlFinger40_L.parent = Finger4Root_L
	fixRotation CtrlFinger40_L
	layer.addNode CtrlFinger40_L

	CtrlFinger01_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger02_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger11_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger12_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger21_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger22_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger31_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger32_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger41_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger42_L = createLineCtrl CtrlFingerPointList true
	CtrlFinger01_L.name = "Ctrl_Finger01_L"
	CtrlFinger02_L.name = "Ctrl_Finger02_L"
	CtrlFinger11_L.name = "Ctrl_Finger11_L"
	CtrlFinger12_L.name = "Ctrl_Finger12_L"
	CtrlFinger21_L.name = "Ctrl_Finger21_L"
	CtrlFinger22_L.name = "Ctrl_Finger22_L"
	CtrlFinger31_L.name = "Ctrl_Finger31_L"
	CtrlFinger32_L.name = "Ctrl_Finger32_L"
	CtrlFinger41_L.name = "Ctrl_Finger41_L"
	CtrlFinger42_L.name = "Ctrl_Finger42_L"
	CtrlFinger01_L.wireColor = CtrlColor2_L
	CtrlFinger02_L.wireColor = CtrlColor2_L
	CtrlFinger11_L.wireColor = CtrlColor2_L
	CtrlFinger12_L.wireColor = CtrlColor2_L
	CtrlFinger21_L.wireColor = CtrlColor2_L
	CtrlFinger22_L.wireColor = CtrlColor2_L
	CtrlFinger31_L.wireColor = CtrlColor2_L
	CtrlFinger32_L.wireColor = CtrlColor2_L
	CtrlFinger41_L.wireColor = CtrlColor2_L
	CtrlFinger42_L.wireColor = CtrlColor2_L
	CtrlFinger01_L.transform = getAimMatrix 1 xVecFinger01_L 3 zVecFinger01_L posFinger01_L
	CtrlFinger02_L.transform = getAimMatrix 1 xVecFinger02_L 3 zVecFinger02_L posFinger02_L
	CtrlFinger11_L.transform = getAimMatrix 1 xVecFinger11_L 3 zVecFinger11_L posFinger11_L
	CtrlFinger12_L.transform = getAimMatrix 1 xVecFinger12_L 3 zVecFinger12_L posFinger12_L
	CtrlFinger21_L.transform = getAimMatrix 1 xVecFinger21_L 3 zVecFinger21_L posFinger21_L
	CtrlFinger22_L.transform = getAimMatrix 1 xVecFinger22_L 3 zVecFinger22_L posFinger22_L
	CtrlFinger31_L.transform = getAimMatrix 1 xVecFinger31_L 3 zVecFinger31_L posFinger31_L
	CtrlFinger32_L.transform = getAimMatrix 1 xVecFinger32_L 3 zVecFinger32_L posFinger32_L
	CtrlFinger41_L.transform = getAimMatrix 1 xVecFinger41_L 3 zVecFinger41_L posFinger41_L
	CtrlFinger42_L.transform = getAimMatrix 1 xVecFinger42_L 3 zVecFinger42_L posFinger42_L
	fixRotation CtrlFinger01_L
	fixRotation CtrlFinger02_L
	fixRotation CtrlFinger11_L
	fixRotation CtrlFinger12_L
	fixRotation CtrlFinger21_L
	fixRotation CtrlFinger22_L
	fixRotation CtrlFinger31_L
	fixRotation CtrlFinger32_L
	fixRotation CtrlFinger41_L
	fixRotation CtrlFinger42_L
	layer.addNode CtrlFinger01_L
	layer.addNode CtrlFinger02_L
	layer.addNode CtrlFinger11_L
	layer.addNode CtrlFinger12_L
	layer.addNode CtrlFinger21_L
	layer.addNode CtrlFinger22_L
	layer.addNode CtrlFinger31_L
	layer.addNode CtrlFinger32_L
	layer.addNode CtrlFinger41_L
	layer.addNode CtrlFinger42_L
	CtrlFinger01_L.parent = CtrlFinger00_L
	CtrlFinger02_L.parent = CtrlFinger01_L
	CtrlFinger11_L.parent = CtrlFinger10_L
	CtrlFinger12_L.parent = CtrlFinger11_L
	CtrlFinger21_L.parent = CtrlFinger20_L
	CtrlFinger22_L.parent = CtrlFinger21_L
	CtrlFinger31_L.parent = CtrlFinger30_L
	CtrlFinger32_L.parent = CtrlFinger31_L
	CtrlFinger41_L.parent = CtrlFinger40_L
	CtrlFinger42_L.parent = CtrlFinger41_L
	locFingerPos00_L = CtrlFinger00_L.pos.controller.value
	locFingerPos01_L = CtrlFinger01_L.pos.controller.value
	locFingerPos02_L = CtrlFinger02_L.pos.controller.value
	locFingerPos10_L = CtrlFinger10_L.pos.controller.value
	locFingerPos11_L = CtrlFinger11_L.pos.controller.value
	locFingerPos12_L = CtrlFinger12_L.pos.controller.value
	locFingerPos20_L = CtrlFinger20_L.pos.controller.value
	locFingerPos21_L = CtrlFinger21_L.pos.controller.value
	locFingerPos22_L = CtrlFinger22_L.pos.controller.value
	locFingerPos30_L = CtrlFinger30_L.pos.controller.value
	locFingerPos31_L = CtrlFinger31_L.pos.controller.value
	locFingerPos32_L = CtrlFinger32_L.pos.controller.value
	locFingerPos40_L = CtrlFinger40_L.pos.controller.value
	locFingerPos41_L = CtrlFinger41_L.pos.controller.value
	locFingerPos42_L = CtrlFinger42_L.pos.controller.value
	CtrlFinger00_L.pos.controller = position_script()
	CtrlFinger01_L.pos.controller = position_script()
	CtrlFinger02_L.pos.controller = position_script()
	CtrlFinger10_L.pos.controller = position_script()
	CtrlFinger11_L.pos.controller = position_script()
	CtrlFinger12_L.pos.controller = position_script()
	CtrlFinger20_L.pos.controller = position_script()
	CtrlFinger21_L.pos.controller = position_script()
	CtrlFinger22_L.pos.controller = position_script()
	CtrlFinger30_L.pos.controller = position_script()
	CtrlFinger31_L.pos.controller = position_script()
	CtrlFinger32_L.pos.controller = position_script()
	CtrlFinger40_L.pos.controller = position_script()
	CtrlFinger41_L.pos.controller = position_script()
	CtrlFinger42_L.pos.controller = position_script()
	CtrlFinger00_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos00_L as string)
	CtrlFinger01_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos01_L as string)
	CtrlFinger02_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos02_L as string)
	CtrlFinger10_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos10_L as string)
	CtrlFinger11_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos11_L as string)
	CtrlFinger12_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos12_L as string)
	CtrlFinger20_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos20_L as string)
	CtrlFinger21_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos21_L as string)
	CtrlFinger22_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos22_L as string)
	CtrlFinger30_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos30_L as string)
	CtrlFinger31_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos31_L as string)
	CtrlFinger32_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos32_L as string)
	CtrlFinger40_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos40_L as string)
	CtrlFinger41_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos41_L as string)
	CtrlFinger42_L.pos.controller.IScriptCtrl.SetExpression (locFingerPos42_L as string)
	CtrlFinger00_L.scale.controller = SlaveScale()
	CtrlFinger01_L.scale.controller = SlaveScale()
	CtrlFinger02_L.scale.controller = SlaveScale()
	CtrlFinger10_L.scale.controller = SlaveScale()
	CtrlFinger11_L.scale.controller = SlaveScale()
	CtrlFinger12_L.scale.controller = SlaveScale()
	CtrlFinger20_L.scale.controller = SlaveScale()
	CtrlFinger21_L.scale.controller = SlaveScale()
	CtrlFinger22_L.scale.controller = SlaveScale()
	CtrlFinger30_L.scale.controller = SlaveScale()
	CtrlFinger31_L.scale.controller = SlaveScale()
	CtrlFinger32_L.scale.controller = SlaveScale()
	CtrlFinger40_L.scale.controller = SlaveScale()
	CtrlFinger41_L.scale.controller = SlaveScale()
	CtrlFinger42_L.scale.controller = SlaveScale()
------------------ Arm Joint R ----------------
	jntAcrom_R = point name:"jntAcrom_R" pos:posUpperArm_R size:4 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	jntAcrom_R.wireColor = refColor1_R
	jntAcrom_R.parent = ArmRoot_R
	jntAcrom_R.rotation.controller = Orientation_Constraint()
	jntAcrom_R.rotation.controller.appendtarget ArmRoot_R 50
	jntAcrom_R.rotation.controller.appendtarget UpperArmTwistBoneList_R[1] 50
	hideLayer.addNode jntAcrom_R

	jntElbow_R = point name:"jntElbow_R" pos:posElbowStart_R size:4 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	jntElbow_R.wireColor = refColor1_R
	jntElbow_R.parent = boneElbow_R
	jntElbow_R.rotation.controller.value = (quat 0 0 0 1)
	jntElbow_R.scale.controller = scale_script()
	jntElbow_R.scale.controller.IScriptCtrl.AddNode "Node0" boneUpperArm_R
	jntElbow_R.scale.controller.IScriptCtrl.AddNode "Node1" boneForeArm_R
	scriptStr = "Ang = acos (dot Node0.transform.row1 Node1.transform.row1)\n" + \
				"[1,1,1+Ang*0.004602373]"
	jntElbow_R.scale.controller.IScriptCtrl.SetExpression scriptStr
	hideLayer.addNode jntElbow_R

	jntWrist_R = point name:"jntWrist_R" pos:posHand_R size:4 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	jntWrist_R.wireColor = refColor1_R*0.5
	jntWrist_R.parent = ForeArmTwistBoneList_R[ForeArmTwistBoneList_R.count]
	jntWrist_R.rotation.controller = Orientation_Constraint()
	jntWrist_R.rotation.controller.appendtarget ForeArmTwistBoneList_R[ForeArmTwistBoneList_R.count] 50
	jntWrist_R.rotation.controller.appendtarget boneHand_R 50
	hideLayer.addNode jntWrist_R
------------------ Arm Joint L ----------------
	jntAcrom_L = point name:"jntAcrom_L" pos:posUpperArm_L size:4 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	jntAcrom_L.wireColor = refColor1_L
	jntAcrom_L.parent = ArmRoot_L
	jntAcrom_L.rotation.controller = Orientation_Constraint()
	jntAcrom_L.rotation.controller.appendtarget ArmRoot_L 50
	jntAcrom_L.rotation.controller.appendtarget UpperArmTwistBoneList_L[1] 50
	hideLayer.addNode jntAcrom_L

	jntElbow_L = point name:"jntElbow_L" pos:posElbowStart_L size:4 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	jntElbow_L.wireColor = refColor1_L
	jntElbow_L.parent = boneElbow_L
	jntElbow_L.rotation.controller.value = (quat 0 0 0 1)
	jntElbow_L.scale.controller = scale_script()
	jntElbow_L.scale.controller.IScriptCtrl.AddNode "Node0" boneUpperArm_L
	jntElbow_L.scale.controller.IScriptCtrl.AddNode "Node1" boneForeArm_L
	scriptStr = "Ang = acos (dot Node0.transform.row1 Node1.transform.row1)\n" + \
				"[1,1,1+Ang*0.004602373]"
	jntElbow_L.scale.controller.IScriptCtrl.SetExpression scriptStr
	hideLayer.addNode jntElbow_L

	jntWrist_L = point name:"jntWrist_L" pos:posHand_L size:4 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
	jntWrist_L.wireColor = refColor1_L*0.5
	jntWrist_L.parent = ForeArmTwistBoneList_L[ForeArmTwistBoneList_L.count]
	jntWrist_L.rotation.controller = Orientation_Constraint()
	jntWrist_L.rotation.controller.appendtarget ForeArmTwistBoneList_L[ForeArmTwistBoneList_L.count] 50
	jntWrist_L.rotation.controller.appendtarget boneHand_L 50
	hideLayer.addNode jntWrist_L
------------------ Arm IK R ----------------
	CtrlHandIK_R = createWireSpherifyCrossArrow refSizeHand 90 2 false
	CtrlHandIK_R.name = "Ctrl_HandIK_R"
	CtrlHandIK_R.wireColor = CtrlColor1_R
	CtrlHandIK_R.parent = rotYUpFix
	CtrlHandIK_R.transform = getAimMatrix 2 nHandYVec_R 3 -nHandZVec_R posHand_R
	CtrlHandIK_R.scale.controller = SlaveScale()
	layer.addNode CtrlHandIK_R
	CustAttributes.add CtrlHandIK_R BaseInfoCA

	CtrlArmUpV_R = createLineCtrl WireSpherePointList false
	CtrlArmUpV_R.wireColor = CtrlColor1_R
	CtrlArmUpV_R.name = "Ctrl_ArmUpV_R"
	CtrlArmUpV_R.pos = posArmUpV_R
	CtrlArmUpV_R.parent = CtrlRoot
	CtrlArmUpV_R.rotation.controller = SlaveRotation()
	CtrlArmUpV_R.scale.controller = SlaveScale()
	layer.addNode CtrlArmUpV_R
	CustAttributes.add CtrlArmUpV_R BaseInfoCA

	lpArmIKHand_R = point name:"lpArmIKHand_R" pos:posHand_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	lpArmIKHand_R.transform = boneHand_R.transform
	lpArmIKHand_R.parent = CtrlHandIK_R
	hideLayer.addNode lpArmIKHand_R
------------------ Arm IK L ----------------
	CtrlHandIK_L = createWireSpherifyCrossArrow refSizeHand 90 2 false
	--CtrlHandIK_L = GenSymObject CtrlHandIK_R "all"
	CtrlHandIK_L.name = "Ctrl_HandIK_L"
	CtrlHandIK_L.wireColor = CtrlColor1_L
	CtrlHandIK_L.parent = rotYUpFix
	CtrlHandIK_L.transform = getAimMatrix 2 nHandYVec_L 3 -nHandZVec_L posHand_L
	CtrlHandIK_L.scale.controller = SlaveScale()
	layer.addNode CtrlHandIK_L
	CustAttributes.add CtrlHandIK_L BaseInfoCA

	CtrlArmUpV_L = createLineCtrl WireSpherePointList false
	CtrlArmUpV_L.wireColor = CtrlColor1_L
	CtrlArmUpV_L.name = "Ctrl_ArmUpV_L"
	CtrlArmUpV_L.pos = posArmUpV_L
	CtrlArmUpV_L.parent = CtrlRoot
	CtrlArmUpV_L.rotation.controller = SlaveRotation()
	CtrlArmUpV_L.scale.controller = SlaveScale()
	layer.addNode CtrlArmUpV_L
	CustAttributes.add CtrlArmUpV_L BaseInfoCA

	lpArmIKHand_L = point name:"lpArmIKHand_L" pos:posHand_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	lpArmIKHand_L.transform = boneHand_L.transform
	lpArmIKHand_L.parent = CtrlHandIK_L
	hideLayer.addNode lpArmIKHand_L
------------------ Arm FK R --------------------------
	lpUpperArmFK_R = point name:"lpUpperArmFK_R" pos:posUpperArm_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	lpUpperArmFK_R.parent = ctrlShoulder_R
	hideLayer.addNode lpUpperArmFK_R

	CtrlUpperArmFK_R = createLineCtrl CtrlArmFKPointList true
	CtrlUpperArmFK_R.name = "Ctrl_UpperArmFK_R"
	CtrlUpperArmFK_R.wireColor = CtrlColor3_R
	CtrlUpperArmFK_R.transform = getAimMatrix 1 nUpperArmVec_R 3 ArmUpVec_R posUpperArm_R
	layer.addNode CtrlUpperArmFK_R
	CustAttributes.add CtrlUpperArmFK_R BaseInfoCA

	CtrlForeArmFK_R = createLineCtrl CtrlArmFKPointList true
	CtrlForeArmFK_R.name = "Ctrl_ForeArmFK_R"
	CtrlForeArmFK_R.wireColor = CtrlColor3_R
	CtrlForeArmFK_R.transform = getAimMatrix 1 nForeArmVec_R 3 ArmUpVec_R posForeArm_R
	layer.addNode CtrlForeArmFK_R
	CustAttributes.add CtrlForeArmFK_R BaseInfoCA

	CtrlHandFK_R = createLineCtrl CtrlHandFKPointList true
	CtrlHandFK_R.name = "Ctrl_HandFK_R"
	CtrlHandFK_R.wireColor = CtrlColor3_R
	CtrlHandFK_R.transform = getAimMatrix 1 nHandXVec_R 3 nHandZVec_R posHand_R
	layer.addNode CtrlHandFK_R
	CustAttributes.add CtrlHandFK_R BaseInfoCA

	CtrlUpperArmFK_R.parent = CtrlRoot
	CtrlForeArmFK_R.parent = CtrlUpperArmFK_R
	CtrlHandFK_R.parent = CtrlForeArmFK_R

	CtrlUpperArmFK_R.pos.controller = Position_Constraint()
	CtrlUpperArmFK_R.pos.controller.appendtarget lpUpperArmFK_R 50
	CtrlUpperArmFK_R.pos.controller.weight[1].controller = Float_Expression()
	CtrlUpperArmFK_R.pos.controller.weight[1].controller.SetExpression "50"
	CtrlUpperArmFK_R.scale.controller = SlaveScale()

	locPos = CtrlForeArmFK_R.pos.controller.value
	CtrlForeArmFK_R.pos.controller = Position_Expression()
	CtrlForeArmFK_R.pos.controller.SetExpression (locPos as string)
	CtrlForeArmFK_R.scale.controller = SlaveScale()

	locPos = CtrlHandFK_R.pos.controller.value
	CtrlHandFK_R.pos.controller = Position_Expression()
	CtrlHandFK_R.pos.controller.SetExpression (locPos as string)
	CtrlHandFK_R.scale.controller = SlaveScale()

	pyArmCenter_R = point name:"pyArmCenter_R" pos:posUpperArm_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	pyArmCenter_R.parent = CtrlRoot
	pyArmCenter_R.pos.controller = Position_Constraint()
	pyArmCenter_R.pos.controller.appendtarget CtrlUpperArmFK_R 50
	pyArmCenter_R.pos.controller.appendtarget CtrlHandFK_R 50
	pyArmCenter_R.rotation.controller = LookAt_Constraint()
	pyArmCenter_R.rotation.controller.appendtarget CtrlHandFK_R 50
	pyArmCenter_R.rotation.controller.lookat_vector_length = 0
	pyArmCenter_R.rotation.controller.upnode_ctrl = 0
	pyArmCenter_R.rotation.controller.upnode_world = off
	pyArmCenter_R.rotation.controller.pickUpNode = CtrlForeArmFK_R
	pyArmCenter_R.rotation.controller.StoUP_axis = 2
	pyArmCenter_R.rotation.controller.StoUP_axisFlip = off
	hideLayer.addNode pyArmCenter_R

	pyArmFKUpV_R = point name:"pyArmCenter_R" pos:posArmUpV_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	pyArmFKUpV_R.parent = pyArmCenter_R
	hideLayer.addNode pyArmFKUpV_R
------------------ Arm FK L --------------------------
	lpUpperArmFK_L = point name:"lpUpperArmFK_L" pos:posUpperArm_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	lpUpperArmFK_L.parent = ctrlShoulder_L
	hideLayer.addNode lpUpperArmFK_L

	CtrlUpperArmFK_L = createLineCtrl CtrlArmFKPointList true
	--CtrlUpperArmFK_L = GenSymObject CtrlUpperArmFK_R "all"
	CtrlUpperArmFK_L.name = "Ctrl_UpperArmFK_L"
	CtrlUpperArmFK_L.wireColor = CtrlColor3_L
	CtrlUpperArmFK_L.transform = getAimMatrix 1 nUpperArmVec_L 3 ArmUpVec_L posUpperArm_L
	layer.addNode CtrlUpperArmFK_L
	CustAttributes.add CtrlUpperArmFK_L BaseInfoCA

	CtrlForeArmFK_L = createLineCtrl CtrlArmFKPointList true
	--CtrlForeArmFK_L = GenSymObject CtrlForeArmFK_R "all"
	CtrlForeArmFK_L.name = "Ctrl_ForeArmFK_L"
	CtrlForeArmFK_L.wireColor = CtrlColor3_L
	CtrlForeArmFK_L.transform = getAimMatrix 1 nForeArmVec_L 3 ArmUpVec_L posForeArm_L
	layer.addNode CtrlForeArmFK_L
	CustAttributes.add CtrlForeArmFK_L BaseInfoCA

	CtrlHandFK_L = createLineCtrl CtrlHandFKPointList true
	--CtrlHandFK_L = GenSymObject CtrlHandFK_R "all"
	CtrlHandFK_L.name = "Ctrl_HandFK_L"
	CtrlHandFK_L.wireColor = CtrlColor3_L
	CtrlHandFK_L.transform = getAimMatrix 1 nHandXVec_L 3 nHandZVec_L posHand_L
	layer.addNode CtrlHandFK_L
	CustAttributes.add CtrlHandFK_L BaseInfoCA

	CtrlUpperArmFK_L.parent = CtrlRoot
	CtrlForeArmFK_L.parent = CtrlUpperArmFK_L
	CtrlHandFK_L.parent = CtrlForeArmFK_L

	CtrlUpperArmFK_L.pos.controller = Position_Constraint()
	CtrlUpperArmFK_L.pos.controller.appendtarget lpUpperArmFK_L 50
	CtrlUpperArmFK_L.pos.controller.weight[1].controller = Float_Expression()
	CtrlUpperArmFK_L.pos.controller.weight[1].controller.SetExpression "50"
	CtrlUpperArmFK_L.scale.controller = SlaveScale()

	locPos = CtrlForeArmFK_L.pos.controller.value
	CtrlForeArmFK_L.pos.controller = Position_Expression()
	CtrlForeArmFK_L.pos.controller.SetExpression (locPos as string)
	CtrlForeArmFK_L.scale.controller = SlaveScale()

	locPos = CtrlHandFK_L.pos.controller.value
	CtrlHandFK_L.pos.controller = Position_Expression()
	CtrlHandFK_L.pos.controller.SetExpression (locPos as string)
	CtrlHandFK_L.scale.controller = SlaveScale()

	pyArmCenter_L = point name:"pyArmCenter_L" pos:posUpperArm_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	pyArmCenter_L.parent = CtrlRoot
	pyArmCenter_L.pos.controller = Position_Constraint()
	pyArmCenter_L.pos.controller.appendtarget CtrlUpperArmFK_L 50
	pyArmCenter_L.pos.controller.appendtarget CtrlHandFK_L 50
	pyArmCenter_L.rotation.controller = LookAt_Constraint()
	pyArmCenter_L.rotation.controller.appendtarget CtrlHandFK_L 50
	pyArmCenter_L.rotation.controller.lookat_vector_length = 0
	pyArmCenter_L.rotation.controller.upnode_ctrl = 0
	pyArmCenter_L.rotation.controller.upnode_world = off
	pyArmCenter_L.rotation.controller.pickUpNode = CtrlForeArmFK_L
	pyArmCenter_L.rotation.controller.StoUP_axis = 2
	pyArmCenter_L.rotation.controller.StoUP_axisFlip = off
	hideLayer.addNode pyArmCenter_L

	pyArmFKUpV_L = point name:"pyArmCenter_L" pos:posArmUpV_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
	pyArmFKUpV_L.parent = pyArmCenter_L
	hideLayer.addNode pyArmFKUpV_L

------------------IK / FK-----------------------
	---R-------
		ArmIKLoc_R.pos.controller = Position_Constraint()
		pyArmUpV_R.pos.controller = Position_Constraint()
		boneHand_R.rotation.controller = Orientation_Constraint()
		
		ArmIKLoc_R.pos.controller.appendtarget CtrlHandIK_R 50
		pyArmUpV_R.pos.controller.appendtarget CtrlArmUpV_R 50
		boneHand_R.rotation.controller.appendtarget lpArmIKHand_R 50

		ArmIKLoc_R.pos.controller.appendtarget CtrlHandFK_R 50
		pyArmUpV_R.pos.controller.appendtarget pyArmFKUpV_R 50
		boneHand_R.rotation.controller.appendtarget CtrlHandFK_R 50
	---L-------
		ArmIKLoc_L.pos.controller = Position_Constraint()
		pyArmUpV_L.pos.controller = Position_Constraint()
		boneHand_L.rotation.controller = Orientation_Constraint()
		
		ArmIKLoc_L.pos.controller.appendtarget CtrlHandIK_L 50
		pyArmUpV_L.pos.controller.appendtarget CtrlArmUpV_L 50
		boneHand_L.rotation.controller.appendtarget lpArmIKHand_L 50

		ArmIKLoc_L.pos.controller.appendtarget CtrlHandFK_L 50
		pyArmUpV_L.pos.controller.appendtarget pyArmFKUpV_L 50
		boneHand_L.rotation.controller.appendtarget CtrlHandFK_L 50

	scWeight_IK_R = float_script()
	scWeight_FK_R = float_script()

	scWeight_IK_R.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_R.controller
	scWeight_FK_R.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_R.controller

	scWeight_IK_R.IScriptCtrl.SetExpression "Ratio * 50"
	scWeight_FK_R.IScriptCtrl.SetExpression "(1 - Ratio) * 50"

	ArmIKLoc_R.pos.controller.weight[1].controller = scWeight_IK_R
	pyArmUpV_R.pos.controller.weight[1].controller = scWeight_IK_R
	boneHand_R.rotation.controller.weight[1].controller = scWeight_IK_R

	ArmIKLoc_R.pos.controller.weight[2].controller = scWeight_FK_R
	pyArmUpV_R.pos.controller.weight[2].controller = scWeight_FK_R
	boneHand_R.rotation.controller.weight[2].controller = scWeight_FK_R

	scWeight_IK_L = float_script()
	scWeight_FK_L = float_script()

	scWeight_IK_L.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_L.controller
	scWeight_FK_L.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_L.controller

	scWeight_IK_L.IScriptCtrl.SetExpression "Ratio * 50"
	scWeight_FK_L.IScriptCtrl.SetExpression "(1 - Ratio) * 50"

	ArmIKLoc_L.pos.controller.weight[1].controller = scWeight_IK_L
	pyArmUpV_L.pos.controller.weight[1].controller = scWeight_IK_L
	boneHand_L.rotation.controller.weight[1].controller = scWeight_IK_L

	ArmIKLoc_L.pos.controller.weight[2].controller = scWeight_FK_L
	pyArmUpV_L.pos.controller.weight[2].controller = scWeight_FK_L
	boneHand_L.rotation.controller.weight[2].controller = scWeight_FK_L
	----------
	IKscriptStr = ("if Ratio > 0 then (\n" + \
				"	return 1\n" + \
				")\n" + \
				"else (\n" + \
				"	return 0 )")
	FKscriptStr = ("if Ratio < 1 then (\n" + \
				"	return 1\n" + \
				")\n" + \
				"else (\n" + \
				"	return 0 )")
	---
	CtrlHandIK_R.visible.controller = float_script()
	CtrlHandIK_R.visible.controller.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_R.controller
	CtrlHandIK_R.visible.controller.IScriptCtrl.SetExpression IKscriptStr

	CtrlArmUpV_R.visible.controller = float_script()
	CtrlArmUpV_R.visible.controller.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_R.controller
	CtrlArmUpV_R.visible.controller.IScriptCtrl.SetExpression IKscriptStr

	CtrlUpperArmFK_R.visible.controller = float_script()
	CtrlUpperArmFK_R.visible.controller.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_R.controller
	CtrlUpperArmFK_R.visible.controller.IScriptCtrl.SetExpression FKscriptStr

	CtrlForeArmFK_R.visible.controller = float_script()
	CtrlForeArmFK_R.visible.controller.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_R.controller
	CtrlForeArmFK_R.visible.controller.IScriptCtrl.SetExpression FKscriptStr

	CtrlHandFK_R.visible.controller = float_script()
	CtrlHandFK_R.visible.controller.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_R.controller
	CtrlHandFK_R.visible.controller.IScriptCtrl.SetExpression FKscriptStr
	---
	CtrlHandIK_L.visible.controller = float_script()
	CtrlHandIK_L.visible.controller.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_L.controller
	CtrlHandIK_L.visible.controller.IScriptCtrl.SetExpression IKscriptStr

	CtrlArmUpV_L.visible.controller = float_script()
	CtrlArmUpV_L.visible.controller.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_L.controller
	CtrlArmUpV_L.visible.controller.IScriptCtrl.SetExpression IKscriptStr

	CtrlUpperArmFK_L.visible.controller = float_script()
	CtrlUpperArmFK_L.visible.controller.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_L.controller
	CtrlUpperArmFK_L.visible.controller.IScriptCtrl.SetExpression FKscriptStr

	CtrlForeArmFK_L.visible.controller = float_script()
	CtrlForeArmFK_L.visible.controller.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_L.controller
	CtrlForeArmFK_L.visible.controller.IScriptCtrl.SetExpression FKscriptStr

	CtrlHandFK_L.visible.controller = float_script()
	CtrlHandFK_L.visible.controller.IScriptCtrl.AddTarget "Ratio" CtrlRoot.fIKFK_L.controller
	CtrlHandFK_L.visible.controller.IScriptCtrl.SetExpression FKscriptStr
	---------------
	CtrlHandIK_R.scale.controller = scale_script()
	CtrlArmUpV_R.scale.controller = scale_script()
	CtrlUpperArmFK_R.scale.controller = scale_script()
	CtrlForeArmFK_R.scale.controller = scale_script()
	CtrlHandFK_R.scale.controller = scale_script()

	CtrlHandIK_R.scale.controller.IScriptCtrl.AddTarget "visible" CtrlHandIK_R.visible.controller
	CtrlArmUpV_R.scale.controller.IScriptCtrl.AddTarget "visible" CtrlArmUpV_R.visible.controller
	CtrlUpperArmFK_R.scale.controller.IScriptCtrl.AddTarget "visible" CtrlUpperArmFK_R.visible.controller
	CtrlForeArmFK_R.scale.controller.IScriptCtrl.AddTarget "visible" CtrlForeArmFK_R.visible.controller
	CtrlHandFK_R.scale.controller.IScriptCtrl.AddTarget "visible" CtrlHandFK_R.visible.controller

	CtrlHandIK_R.scale.controller.IScriptCtrl.SetExpression "if visible then [1,1,1] else [0,0,0]"
	CtrlArmUpV_R.scale.controller.IScriptCtrl.SetExpression "if visible then [1,1,1] else [0,0,0]"
	CtrlUpperArmFK_R.scale.controller.IScriptCtrl.SetExpression "if visible then [1,1,1] else [0,0,0]"
	CtrlForeArmFK_R.scale.controller.IScriptCtrl.SetExpression "if visible then [1,1,1] else [0,0,0]"
	CtrlHandFK_R.scale.controller.IScriptCtrl.SetExpression "if visible then [1,1,1] else [0,0,0]"
	------
	CtrlHandIK_L.scale.controller = scale_script()
	CtrlArmUpV_L.scale.controller = scale_script()
	CtrlUpperArmFK_L.scale.controller = scale_script()
	CtrlForeArmFK_L.scale.controller = scale_script()
	CtrlHandFK_L.scale.controller = scale_script()

	CtrlHandIK_L.scale.controller.IScriptCtrl.AddTarget "visible" CtrlHandIK_L.visible.controller
	CtrlArmUpV_L.scale.controller.IScriptCtrl.AddTarget "visible" CtrlArmUpV_L.visible.controller
	CtrlUpperArmFK_L.scale.controller.IScriptCtrl.AddTarget "visible" CtrlUpperArmFK_L.visible.controller
	CtrlForeArmFK_L.scale.controller.IScriptCtrl.AddTarget "visible" CtrlForeArmFK_L.visible.controller
	CtrlHandFK_L.scale.controller.IScriptCtrl.AddTarget "visible" CtrlHandFK_L.visible.controller

	CtrlHandIK_L.scale.controller.IScriptCtrl.SetExpression "if visible then [1,1,1] else [0,0,0]"
	CtrlArmUpV_L.scale.controller.IScriptCtrl.SetExpression "if visible then [1,1,1] else [0,0,0]"
	CtrlUpperArmFK_L.scale.controller.IScriptCtrl.SetExpression "if visible then [1,1,1] else [0,0,0]"
	CtrlForeArmFK_L.scale.controller.IScriptCtrl.SetExpression "if visible then [1,1,1] else [0,0,0]"
	CtrlHandFK_L.scale.controller.IScriptCtrl.SetExpression "if visible then [1,1,1] else [0,0,0]"

-------------------------------
	paramWire.connect CtrlRoot.BipedControl[#bSoftIK] ArmIKLoc_R.IKInfo[#useSoftIK] "bSoftIK"
	paramWire.connect CtrlRoot.BipedControl[#bSoftIK] ArmIKLoc_L.IKInfo[#useSoftIK] "bSoftIK"