fn getAimMatrix aimAxisID vecAim upAxisID vecUp pos = (
	xAxis = [1,0,0]
	yAxis = [0,1,0]
	zAxis = [0,0,1]
	
	aimV = normalize vecAim
	sideV = normalize (cross vecUp aimV)
	upV = normalize (cross vecAim sideV)
	
	if aimAxisID == 1 and upAxisID == 3 then (
		xAxis = aimV
		yAxis = sideV
		zAxis = upV
	)
	else if  aimAxisID == 1 and upAxisID == 2 then (
		xAxis = aimV
		yAxis = upV
		zAxis = -sideV
	)
	else if  aimAxisID == 2 and upAxisID == 1 then (
		xAxis = upV
		yAxis = aimV
		zAxis = sideV
	)
	else if  aimAxisID == 2 and upAxisID == 3 then (
		xAxis = -sideV
		yAxis = aimV
		zAxis = upV
	)
	else if  aimAxisID == 3 and upAxisID == 1 then (
		xAxis = upV
		yAxis = -sideV
		zAxis = aimV
	)
	else if  aimAxisID == 3 and upAxisID == 2 then (
		xAxis = sideV
		yAxis = upV
		zAxis = aimV
	)
	else ( 
		print "I should not be here"
		return undefined
	)
	
	return matrix3 xAxis yAxis zAxis pos	
)

fn fixRotation obj = (
	obj.rotation.controller = tcb_rotation ()
	obj.rotation.controller = Euler_XYZ ()
)

fn createBipedGuide = (
-- 	BGLayer = LayerManager.newLayer()
-- 	BGLayer.setname "BipedGuide"

	BGLayer = LayerManager.getLayerFromName "BipedGuide"
	if BGLayer == undefined then (
	    BGLayer = LayerManager.newLayer()
	    BGLayer.setname "BipedGuide"
	)

	bgRoot = dummy name:"bg_Root" boxsize:[20,20,2]
	BGLayer.addNode bgRoot

	nset = NURBSSet ()
	pointList = #()
-- 	append pointList [0,-5.50414,101.401]
-- 	append pointList [0,-8.74318,113.731]
-- 	append pointList [0,-0.618217,124.584]
	append pointList [0,-6.20173,109.037]
	append pointList [0,-6.38082,117.935]
	append pointList [0,-0.141972,126.45]

	append pointList [0, 1.853, 145.704]
	append pointList [0,-0.585692,154.592]
	append pointList [0,-0.585692,170.768]

	c = NURBSCVCurve name:"CV Curve" order:4 numCVs:4 numKnots:8
	for k in 1 to 4 do ( setKnot c k 0; setKnot c (k+4) 1 )
	cv = NURBSControlVertex pointList[1]
	setCV c 1 cv
	cv.pos = pointList[2]
	setCV c 2 cv
	cv.pos = pointList[3]
	setCV c 3 cv
	cv.pos = pointList[4]
	setCV c 4 cv
	appendObject nset c
	-- create the NURBS object from the NURBSSet
	bgSpineLine = NURBSNode nset name:"bg_SpineLine" pos:[0,0,0]
	bgSpineLine.wireColor = (color 254 7 1)--(color 255 109 51)
	bgSpineLine.parent = bgRoot
	BGLayer.addNode bgSpineLine

	spIKCtrlModify = Spline_IK_Control()
	addModifier bgSpineLine spIKCtrlModify
	spIKCtrlModify.helper_size = 12
	spIKCtrlModify.createHelper 4
	bgSIKPointList = spIKCtrlModify.helper_list
	for i = 1 to (bgSIKPointList.count) do
	(
		bgSIKPointList[i].wireColor = (color 255 109 51)
		bgSIKPointList[i].name = "bg_SpineLineCtrl_" + (i as string)
		bgSIKPointList[i].parent = bgRoot
		if i == 1 then (
			bgSIKPointList[i].isHidden = True
		)
		BGLayer.addNode bgSIKPointList[i]
	)

	bgSpineSeg0 = Sphere name:"bg_SpineSeg0" radius:0.75 wireColor:(color 60 60 60) isFrozen:true
	bgSpineSeg1 = Sphere name:"bg_SpineSeg1" radius:2 wireColor:(color 255 109 51)
	bgSpineSeg2 = Sphere name:"bg_SpineSeg2" radius:2 wireColor:(color 255 109 51)
-- 	bgSpineSeg3 = Sphere name:"bg_SpineSeg3" radius:2 wireColor:(color 255 109 51)
	bgSpineSegE = Sphere name:"bg_SpineSegE" radius:0.75 wireColor:(color 60 60 60) isFrozen:true
	bgSpineSeg0.pos.controller = Path_Constraint percent:0 follow:false path:bgSpineLine loop:off
	bgSpineSeg1.pos.controller = Path_Constraint percent:30 follow:false path:bgSpineLine loop:off
	bgSpineSeg2.pos.controller = Path_Constraint percent:60 follow:false path:bgSpineLine loop:off
-- 	bgSpineSeg3.pos.controller = Path_Constraint percent:70 follow:false path:bgSpineLine loop:off
	bgSpineSegE.pos.controller = Path_Constraint percent:100 follow:false path:bgSpineLine loop:off
	deleteKeys bgSpineSeg0 #AllKeys
	deleteKeys bgSpineSeg1 #AllKeys
	deleteKeys bgSpineSeg2 #AllKeys
-- 	deleteKeys bgSpineSeg3 #AllKeys
	deleteKeys bgSpineSegE #AllKeys
	bgSpineSeg0.parent = bgRoot
	bgSpineSeg1.parent = bgRoot
	bgSpineSeg2.parent = bgRoot
-- 	bgSpineSeg3.parent = bgRoot
	bgSpineSegE.parent = bgRoot
	BGLayer.addNode bgSpineSeg0
	BGLayer.addNode bgSpineSeg1
	BGLayer.addNode bgSpineSeg2
-- 	BGLayer.addNode bgSpineSeg3
	BGLayer.addNode bgSpineSegE
	
	
	rfSpineList = #()
	bgRfSpine1 = BoneSys.createBone bgSpineSeg0.transform.pos bgSpineSeg1.transform.pos [0,1,0]
	bgRfSpine2 = BoneSys.createBone bgSpineSeg1.transform.pos bgSpineSeg2.transform.pos [0,1,0]
	bgRfSpine3 = BoneSys.createBone bgSpineSeg2.transform.pos bgSpineSegE.transform.pos [0,1,0]
-- 	bgRfSpine4 = BoneSys.createBone bgSpineSeg3.transform.pos bgSpineSegE.transform.pos [0,1,0]
	bgRfSpineE = BoneSys.createBone bgSpineSegE.transform.pos bgSpineSegE.transform.pos [0,1,0]
	append rfSpineList bgRfSpine1
	append rfSpineList bgRfSpine2
	append rfSpineList bgRfSpine3
-- 	append rfSpineList bgRfSpine4
	append rfSpineList bgRfSpineE
	
	for sp in rfSpineList do
	(
		-- name:"bgRfSpine1" wireColor:(color 254 7 1) showFrozenInGray:false isFrozen:true
		sp.wireColor = (color 254 7 1)
		sp.width = 4
		sp.height = 4
		sp.Taper = 90
		sp.sidefins = off
		sp.sidefinssize = 2
		sp.frontfin = off
		sp.frontfinsize = 2
		sp.backfin = off
		sp.backfinsize = 2
		sp.showFrozenInGray = false
		sp.isFrozen = true
		BGLayer.addNode sp
	)

	bgRfSpine1.parent = bgRoot
	bgRfSpine2.parent = bgRfSpine1
	bgRfSpine3.parent = bgRfSpine2
-- 	bgRfSpine4.parent = bgRfSpine3
	bgRfSpineE.parent = bgRfSpine3
	bgRfSpineE.rotation.controller.value = (quat 0 0 0 1)
	bgRfSpineE.width = 2
	bgRfSpineE.height = 2
	bgRfSpineE.length = 2

	bgRfSpine1.rotation.controller = LookAt_Constraint ()
	bgRfSpine1.rotation.controller.appendtarget bgSpineSeg1 50
	bgRfSpine1.rotation.controller.lookat_vector_length = 0
	bgRfSpine2.rotation.controller = LookAt_Constraint ()
	bgRfSpine2.rotation.controller.appendtarget bgSpineSeg2 50
	bgRfSpine2.rotation.controller.lookat_vector_length = 0
	bgRfSpine3.rotation.controller = LookAt_Constraint ()
	bgRfSpine3.rotation.controller.appendtarget bgSpineSegE 50
	bgRfSpine3.rotation.controller.lookat_vector_length = 0
-- 	bgRfSpine4.rotation.controller = LookAt_Constraint ()
-- 	bgRfSpine4.rotation.controller.appendtarget bgSpineSegE 50
-- 	bgRfSpine4.rotation.controller.lookat_vector_length = 0

	bgRfSpine1.pos.controller = Position_Constraint ()
	bgRfSpine1.pos.controller.appendtarget bgSpineSeg0 50
	bgRfSpine2.pos.controller = Position_Constraint ()
	bgRfSpine2.pos.controller.appendtarget bgSpineSeg1 50
	bgRfSpine3.pos.controller = Position_Constraint ()
	bgRfSpine3.pos.controller.appendtarget bgSpineSeg2 50
-- 	bgRfSpine4.pos.controller = Position_Constraint ()
-- 	bgRfSpine4.pos.controller.appendtarget bgSpineSeg3 50
	bgRfSpineE.pos.controller = Position_Constraint ()
	bgRfSpineE.pos.controller.appendtarget bgSpineSegE 50

	bgHip = BoneSys.createBone [0,-5.50414,101.401] pointList[1] [0,1,0]
	bgHip.name = "bg_Hip"
	bgHip.wireColor = (color 255 109 51)
	bgHip.width = 4
	bgHip.height = 4
	bgHip.Taper = 0
	bgHip.sidefins = off
	bgHip.sidefinssize = 2
	bgHip.frontfin = off
	bgHip.frontfinsize = 2
	bgHip.backfin = off
	bgHip.backfinsize = 2
	bgHip.backfinstarttaper = 10
	bgHip.parent = bgRoot
	BGLayer.addNode bgHip
	bgSIKPointList[1].parent = bgHip

	------------------------------------------------------
	bgNeck = BoneSys.createBone pointList[4] pointList[5] [0,1,0]
	bgNeck.name = "bg_Neck"
	bgNeck.wireColor = (color 255 109 51)
	bgNeck.width = 4
	bgNeck.height = 4
	bgNeck.Taper = 0
	bgNeck.sidefins = off
	bgNeck.sidefinssize = 2
	bgNeck.frontfin = off
	bgNeck.frontfinsize = 2
	bgNeck.backfin = off
	bgNeck.backfinsize = 2
	bgNeck.backfinstarttaper = 10
	bgNeck.parent = bgRoot
	bgNeck.transform = (getAimMatrix 1 (pointList[5] - pointList[4]) 2 [0,1,0] pointList[4])
	fixRotation bgNeck

	bgHead = BoneSys.createBone pointList[5] pointList[6] [0,1,0]
	bgHead.name = "bg_Head"
	bgHead.wireColor = (color 255 109 51)
	bgHead.width = 4
	bgHead.height = 4
	bgHead.Taper = 15
	bgHead.sidefins = on
	bgHead.sidefinssize = 4.5
	bgHead.frontfin = on
	bgHead.frontfinsize = 5
	bgHead.backfin = on
	bgHead.backfinsize = 7.8
	bgHead.backfinstarttaper = -56
	bgHead.parent = bgNeck
	bgHead.transform = (getAimMatrix 1 (pointList[6] - pointList[5]) 2 [0,1,0] pointList[5])
	fixRotation bgHead


	bgHeadEff = BoneSys.createBone pointList[6] ( pointList[6] + 2 * ( normalize (pointList[6] - pointList[5]) ) ) [0,1,0]
	bgHeadEff.name = "bg_HeadEff"
	bgHeadEff.wireColor = (color 255 109 51)
	bgHeadEff.width = 2
	bgHeadEff.height = 2
	bgHeadEff.Taper = 90
	bgHeadEff.sidefins = off
	bgHeadEff.sidefinssize = 2
	bgHeadEff.frontfin = off
	bgHeadEff.frontfinsize = 2
	bgHeadEff.backfin = off
	bgHeadEff.backfinsize = 2
	bgHeadEff.backfinstarttaper = 10
	bgHeadEff.parent = bgHead
	bgHeadEff.transform = (getAimMatrix 1 (pointList[6] - pointList[5]) 2 [0,1,0] pointList[6] )
	fixRotation bgHeadEff

	BGLayer.addNode bgNeck
	BGLayer.addNode bgHead
	BGLayer.addNode bgHeadEff

	bgNeck.pos.controller = Position_Constraint ()
	bgNeck.pos.controller.appendtarget bgSIKPointList[bgSIKPointList.count] 50
	-------------------------------------------------------------------------------------------------
	posThigh = [-8.82323,-5.25398,99.8303]
	posCalf = [-8.50866,-4.20878,54.0757]
	posFoot = [-8.18885,-0.598426,7.61584]
	posToe = [-8.18885,-11.3747,1.39321]
	posToeEff = [-8.18885,-17.2756,1.39321]

	bgLegSideVec = normalize ( cross (posFoot - posCalf) (posCalf - posThigh) )

	bgThigh = BoneSys.createBone posThigh posCalf [0,1,0]
	bgThigh.name = "bg_Thigh"
	bgThigh.wireColor = (color 255 109 51)
	bgThigh.width = 14
	bgThigh.height = 14
	bgThigh.Taper = 55
	bgThigh.sidefins = off
	bgThigh.sidefinssize = 2
	bgThigh.frontfin = off
	bgThigh.frontfinsize = 2
	bgThigh.backfin = off
	bgThigh.backfinsize = 2
	bgThigh.backfinstarttaper = 10
	bgThigh.transform = (getAimMatrix 1 (posCalf - posThigh) 2 bgLegSideVec posThigh)
	bgThigh.parent = bgRoot
	fixRotation bgThigh

	bgCalf = BoneSys.createBone posCalf posFoot [0,1,0]
	bgCalf.name = "bg_Calf"
	bgCalf.wireColor = (color 255 109 51)
	bgCalf.width = 7
	bgCalf.height = 7
	bgCalf.Taper = 52
	bgCalf.sidefins = off
	bgCalf.sidefinssize = 2
	bgCalf.frontfin = off
	bgCalf.frontfinsize = 2
	bgCalf.backfin = off
	bgCalf.backfinsize = 2
	bgCalf.backfinstarttaper = 10
	bgCalf.transform = (getAimMatrix 1 (posFoot - posCalf) 2 bgLegSideVec posCalf)
	bgCalf.parent = bgThigh
	fixRotation bgCalf

	bgFoot = BoneSys.createBone posFoot posToe [0,1,0]
	bgFoot.name = "bg_Foot"
	bgFoot.wireColor = (color 255 109 51)
	bgFoot.width = 4
	bgFoot.height = 4
	bgFoot.Taper = 90
	bgFoot.sidefins = off
	bgFoot.sidefinssize = 2
	bgFoot.frontfin = off
	bgFoot.frontfinsize = 2
	bgFoot.backfin = off
	bgFoot.backfinsize = 2
	bgFoot.backfinstarttaper = 10
	bgFoot.transform = (getAimMatrix 1 (posToe - posFoot) 3 [0,0,-1] posFoot )
	bgFoot.parent = bgCalf
	fixRotation bgFoot

	bgToe = BoneSys.createBone posToe posToeEff [0,1,0]
	bgToe.name = "bg_Toe"
	bgToe.wireColor = (color 255 109 51)
	bgToe.width = 4
	bgToe.height = 4
	bgToe.Taper = 90
	bgToe.sidefins = off
	bgToe.sidefinssize = 2
	bgToe.frontfin = off
	bgToe.frontfinsize = 2
	bgToe.backfin = off
	bgToe.backfinsize = 2
	bgToe.backfinstarttaper = 10
	bgToe.transform = (getAimMatrix 1 (posToeEff - posToe) 3 [0,0,-1] posToe )
	bgToe.parent = bgFoot
	fixRotation bgToe

	bgToeEff = BoneSys.createBone posToeEff ( posToeEff + 2 * ( normalize (posToeEff - posToe) ) ) [0,1,0]
	bgToeEff.name = "bg_ToeEff"
	bgToeEff.wireColor = (color 255 109 51)
	bgToeEff.width = 2
	bgToeEff.height = 2
	bgToeEff.Taper = 90
	bgToeEff.sidefins = off
	bgToeEff.sidefinssize = 2
	bgToeEff.frontfin = off
	bgToeEff.frontfinsize = 2
	bgToeEff.backfin = off
	bgToeEff.backfinsize = 2
	bgToeEff.backfinstarttaper = 10
	bgToeEff.transform = (getAimMatrix 1 (posToeEff - posToe) 3 [0,0,-1] posToeEff )
	bgToeEff.parent = bgToe
	fixRotation bgToeEff

	bgKnee = Sphere name:"bg_Knee" radius:1.75 wireColor:(color 255 109 51)
	bgKnee.transform = bgCalf.transform
	bgKnee.parent = bgCalf

	BGLayer.addNode bgThigh
	BGLayer.addNode bgCalf
	BGLayer.addNode bgFoot
	BGLayer.addNode bgToe
	BGLayer.addNode bgToeEff
	BGLayer.addNode bgKnee
	-------------------------------------------------------
	posShoulder = [-1.21646,-0.47384,142.406]
	posUpperArm = [-10.5603,-0.1169,142.062]
	posForeArm = [-36.6245,0.240055,142.181]
	posHand = [-59.1366,-1.10794,142.288]
	posHandEff = [-67.6821,-1.03918,142.152]

	armSideVec = normalize (cross (posHand - posForeArm) (posForeArm - posUpperArm) )
	armUpVec = normalize (cross armSideVec (posHand - posUpperArm) )

	bgShoulder = BoneSys.createBone posShoulder posUpperArm [0,1,0]
	bgShoulder.name = "bg_Shoulder"
	bgShoulder.transform = (getAimMatrix 1 (posUpperArm - posShoulder) 3 [0,1,0] posShoulder )
	bgShoulder.wireColor = (color 255 109 51)
	bgShoulder.width = 8
	bgShoulder.height = 3.5
	bgShoulder.Taper = 30
	bgShoulder.sidefins = off
	bgShoulder.sidefinssize = 2
	bgShoulder.frontfin = off
	bgShoulder.frontfinsize = 2
	bgShoulder.backfin = off
	bgShoulder.backfinsize = 2
	bgShoulder.backfinstarttaper = 10
	bgShoulder.parent = bgRoot
	fixRotation bgShoulder

	bgUpperArm = BoneSys.createBone posUpperArm posForeArm [0,1,0]
	bgUpperArm.name = "bg_UpperArm"
	bgUpperArm.transform = (getAimMatrix 1 (posForeArm - posUpperArm) 3 armUpVec posUpperArm )
	bgUpperArm.wireColor = (color 255 109 51)
	bgUpperArm.width = 6
	bgUpperArm.height = 6
	bgUpperArm.Taper = 90
	bgUpperArm.sidefins = off
	bgUpperArm.sidefinssize = 2
	bgUpperArm.frontfin = off
	bgUpperArm.frontfinsize = 2
	bgUpperArm.backfin = off
	bgUpperArm.backfinsize = 2
	bgUpperArm.backfinstarttaper = 10
	bgUpperArm.parent = bgShoulder
	fixRotation bgUpperArm

	bgForeArm = BoneSys.createBone posForeArm posHand [0,1,0]
	bgForeArm.name = "bg_ForeArm"
	bgForeArm.transform = (getAimMatrix 1 (posHand - posForeArm) 3 armUpVec posForeArm )
	bgForeArm.wireColor = (color 255 109 51)
	bgForeArm.width = 5
	bgForeArm.height = 5
	bgForeArm.Taper = 90
	bgForeArm.sidefins = off
	bgForeArm.sidefinssize = 2
	bgForeArm.frontfin = off
	bgForeArm.frontfinsize = 2
	bgForeArm.backfin = off
	bgForeArm.backfinsize = 2
	bgForeArm.backfinstarttaper = 10
	bgForeArm.parent = bgUpperArm
	fixRotation bgForeArm

	bgHand = BoneSys.createBone posHand posHandEff [0,1,0]
	bgHand.name = "bg_Hand"
	bgHand.transform = (getAimMatrix 1 (posHandEff - posHand) 3 [0,1,0] posHand )
	bgHand.wireColor = (color 255 109 51)
	bgHand.width = 6
	bgHand.height = 3
	bgHand.Taper = 27
	bgHand.sidefins = off
	bgHand.sidefinssize = 2
	bgHand.frontfin = off
	bgHand.frontfinsize = 2
	bgHand.backfin = off
	bgHand.backfinsize = 2
	bgHand.backfinstarttaper = 10
	bgHand.parent = bgForeArm
	fixRotation bgHand

	bgElbow = Sphere name:"bg_Elbow" radius:0.5 wireColor:(color 255 109 51)
	bgElbow.transform = bgForeArm.transform
	bgElbow.parent = bgForeArm

	BGLayer.addNode bgShoulder
	BGLayer.addNode bgUpperArm
	BGLayer.addNode bgForeArm
	BGLayer.addNode bgHand
	BGLayer.addNode bgElbow
	-------------------------------------
	posFin00 = [-62.0023,-3.30127,141.258]
	rotFin00 = (quat -0.18139 0.0415884 0.930945 0.314181)
	posFin01 = [-65.1764,-5.88638,139.915]
	rotFin01 = (quat 0 0 -0.00445889 0.99999)
	posFin02 = [-66.7136,-7.16201,139.264]
	rotFin02 = (quat 0 0 0.047337 0.998879)
	posFin0Eff = [-68.2847,-8.22437,138.608]

	posFin10 = [-68.2139,-3.15899,142.29]
	rotFin10 = (quat -0.0633261 0.667968 0.738228 0.0694898)
	posFin11 = [-71.7969,-3.84282,142.287]
	rotFin11 = (quat 0 0 0 1)
	posFin12 = [-73.8597,-4.23594,142.286]
	rotFin12 = (quat 0 0 0 1)
	posFin1Eff = [-75.8244,-4.61031,142.285]

	posFin20 = [-68.4013,-1.38404,142.478]
	rotFin20 = (quat -0.00142285 0.707105 0.707105 0.00142285)
	posFin21 = [-72.6512,-1.40116,142.478]
	rotFin21 = (quat 0 0 0 1)
	posFin22 = [-74.9512,-1.4104,142.478]
	rotFin22 = (quat 0 0 0 1)
	posFin2Eff = [-77.0512,-1.41883,142.478]
-- 				
	posFin30 = [-68.1535,0.194751,142.026]
	rotFin30 = (quat 0.0947588 0.718234 0.68502 -0.0768669)
	posFin31 = [-71.9854,1.14827,142.102]
	rotFin31 = (quat 0 0 0.00261799 0.999997)
	posFin32 = [-74.4123,1.75151,142.138]
	rotFin32 = (quat 0 0 0 1)
	posFin3Eff = [-76.1373,2.18026,142.163]

	posFin40 = [-67.588,1.59379,141.681]
	rotFin40 = (quat 0.166978 0.732653 0.63759 -0.169756)
	posFin41 = [-70.5081,3.11262,141.563]
	rotFin41 = (quat 0 0 0.00261799 0.999997)
	posFin42 = [-72.403,4.09657,141.475]
	rotFin42 = (quat 0 0 0.00436331 0.99999)
	posFin4Eff = [-73.8027,4.82133,141.397]

	bgFinger00 = BoneSys.createBone posFin00 posFin01 [0,1,0]
	bgFinger00.name = "bg_Finger00"
	bgFinger00.rotation.controller.value = rotFin00
	bgFinger00.wireColor = (color 255 109 51)
	bgFinger00.width = 1
	bgFinger00.height = 1
	bgFinger00.Taper = 90
	bgFinger00.sidefins = off
	bgFinger00.sidefinssize = 2
	bgFinger00.frontfin = off
	bgFinger00.frontfinsize = 2
	bgFinger00.backfin = off
	bgFinger00.backfinsize = 2
	bgFinger00.backfinstarttaper = 10
	fixRotation bgFinger00

	bgFinger01 = BoneSys.createBone posFin01 posFin02 [0,1,0]
	bgFinger01.name = "bg_Finger01"
	bgFinger01.wireColor = (color 255 109 51)
	bgFinger01.width = 1
	bgFinger01.height = 1
	bgFinger01.Taper = 90
	bgFinger01.sidefins = off
	bgFinger01.sidefinssize = 2
	bgFinger01.frontfin = off
	bgFinger01.frontfinsize = 2
	bgFinger01.backfin = off
	bgFinger01.backfinsize = 2
	bgFinger01.backfinstarttaper = 10
	bgFinger01.parent = bgFinger00
	bgFinger01.rotation.controller.value = rotFin01
	fixRotation bgFinger01

	bgFinger02 = BoneSys.createBone posFin02 posFin0Eff [0,1,0]
	bgFinger02.name = "bg_Finger02"
	bgFinger02.wireColor = (color 255 109 51)
	bgFinger02.width = 1
	bgFinger02.height = 1
	bgFinger02.Taper = 90
	bgFinger02.sidefins = off
	bgFinger02.sidefinssize = 2
	bgFinger02.frontfin = off
	bgFinger02.frontfinsize = 2
	bgFinger02.backfin = off
	bgFinger02.backfinsize = 2
	bgFinger02.backfinstarttaper = 10
	bgFinger02.parent = bgFinger01
	bgFinger02.rotation.controller.value = rotFin02
	fixRotation bgFinger02

	bgFinger0E = BoneSys.createBone posFin0Eff ( posFin0Eff + 0.5*(normalize (posFin0Eff - posFin02) ) ) [0,1,0]
	bgFinger0E.name = "bg_Finger0E"
	bgFinger0E.wireColor = (color 255 109 51)
	bgFinger0E.width = 0.5
	bgFinger0E.height = 0.5
	bgFinger0E.Taper = 90
	bgFinger0E.sidefins = off
	bgFinger0E.sidefinssize = 2
	bgFinger0E.frontfin = off
	bgFinger0E.frontfinsize = 2
	bgFinger0E.backfin = off
	bgFinger0E.backfinsize = 2
	bgFinger0E.backfinstarttaper = 10
	bgFinger0E.parent = bgFinger02
	bgFinger0E.rotation.controller.value = (quat 1)
	fixRotation bgFinger0E
	----
	bgFinger10 = BoneSys.createBone posFin10 posFin11 [0,1,0]
	bgFinger10.name = "bg_Finger10"
	bgFinger10.rotation.controller.value = rotFin10
	bgFinger10.wireColor = (color 255 109 51)
	bgFinger10.width = 1
	bgFinger10.height = 1
	bgFinger10.Taper = 90
	bgFinger10.sidefins = off
	bgFinger10.sidefinssize = 2
	bgFinger10.frontfin = off
	bgFinger10.frontfinsize = 2
	bgFinger10.backfin = off
	bgFinger10.backfinsize = 2
	bgFinger10.backfinstarttaper = 10
	fixRotation bgFinger10

	bgFinger11 = BoneSys.createBone posFin11 posFin12 [0,1,0]
	bgFinger11.name = "bg_Finger11"
	bgFinger11.wireColor = (color 255 109 51)
	bgFinger11.width = 1
	bgFinger11.height = 1
	bgFinger11.Taper = 90
	bgFinger11.sidefins = off
	bgFinger11.sidefinssize = 2
	bgFinger11.frontfin = off
	bgFinger11.frontfinsize = 2
	bgFinger11.backfin = off
	bgFinger11.backfinsize = 2
	bgFinger11.backfinstarttaper = 10
	bgFinger11.parent = bgFinger10
	bgFinger11.rotation.controller.value = rotFin11
	fixRotation bgFinger11

	bgFinger12 = BoneSys.createBone posFin12 posFin1Eff [0,1,0]
	bgFinger12.name = "bg_Finger12"
	bgFinger12.wireColor = (color 255 109 51)
	bgFinger12.width = 1
	bgFinger12.height = 1
	bgFinger12.Taper = 90
	bgFinger12.sidefins = off
	bgFinger12.sidefinssize = 2
	bgFinger12.frontfin = off
	bgFinger12.frontfinsize = 2
	bgFinger12.backfin = off
	bgFinger12.backfinsize = 2
	bgFinger12.backfinstarttaper = 10
	bgFinger12.parent = bgFinger11
	bgFinger12.rotation.controller.value = rotFin12
	fixRotation bgFinger12

	bgFinger1E = BoneSys.createBone posFin1Eff ( posFin1Eff + 0.5*(normalize (posFin1Eff - posFin12) ) ) [0,1,0]
	bgFinger1E.name = "bg_Finger1E"
	bgFinger1E.wireColor = (color 255 109 51)
	bgFinger1E.width = 0.5
	bgFinger1E.height = 0.5
	bgFinger1E.Taper = 90
	bgFinger1E.sidefins = off
	bgFinger1E.sidefinssize = 2
	bgFinger1E.frontfin = off
	bgFinger1E.frontfinsize = 2
	bgFinger1E.backfin = off
	bgFinger1E.backfinsize = 2
	bgFinger1E.backfinstarttaper = 10
	bgFinger1E.parent = bgFinger12
	bgFinger1E.rotation.controller.value = (quat 1)
	fixRotation bgFinger1E
	----
	bgFinger20 = BoneSys.createBone posFin20 posFin21 [0,1,0]
	bgFinger20.name = "bg_Finger20"
	bgFinger20.rotation.controller.value = rotFin20
	bgFinger20.wireColor = (color 255 109 51)
	bgFinger20.width = 1
	bgFinger20.height = 1
	bgFinger20.Taper = 90
	bgFinger20.sidefins = off
	bgFinger20.sidefinssize = 2
	bgFinger20.frontfin = off
	bgFinger20.frontfinsize = 2
	bgFinger20.backfin = off
	bgFinger20.backfinsize = 2
	bgFinger20.backfinstarttaper = 10
	fixRotation bgFinger20

	bgFinger21 = BoneSys.createBone posFin21 posFin22 [0,1,0]
	bgFinger21.name = "bg_Finger21"
	bgFinger21.wireColor = (color 255 109 51)
	bgFinger21.width = 1
	bgFinger21.height = 1
	bgFinger21.Taper = 90
	bgFinger21.sidefins = off
	bgFinger21.sidefinssize = 2
	bgFinger21.frontfin = off
	bgFinger21.frontfinsize = 2
	bgFinger21.backfin = off
	bgFinger21.backfinsize = 2
	bgFinger21.backfinstarttaper = 10
	bgFinger21.parent = bgFinger20
	bgFinger21.rotation.controller.value = rotFin21
	fixRotation bgFinger21

	bgFinger22 = BoneSys.createBone posFin22 posFin2Eff [0,1,0]
	bgFinger22.name = "bg_Finger22"
	bgFinger22.wireColor = (color 255 109 51)
	bgFinger22.width = 1
	bgFinger22.height = 1
	bgFinger22.Taper = 90
	bgFinger22.sidefins = off
	bgFinger22.sidefinssize = 2
	bgFinger22.frontfin = off
	bgFinger22.frontfinsize = 2
	bgFinger22.backfin = off
	bgFinger22.backfinsize = 2
	bgFinger22.backfinstarttaper = 10
	bgFinger22.parent = bgFinger21
	bgFinger22.rotation.controller.value = rotFin22
	fixRotation bgFinger22

	bgFinger2E = BoneSys.createBone posFin2Eff ( posFin2Eff + 0.5*(normalize (posFin2Eff - posFin22) ) ) [0,1,0]
	bgFinger2E.name = "bg_Finger2E"
	bgFinger2E.wireColor = (color 255 109 51)
	bgFinger2E.width = 0.5
	bgFinger2E.height = 0.5
	bgFinger2E.Taper = 90
	bgFinger2E.sidefins = off
	bgFinger2E.sidefinssize = 2
	bgFinger2E.frontfin = off
	bgFinger2E.frontfinsize = 2
	bgFinger2E.backfin = off
	bgFinger2E.backfinsize = 2
	bgFinger2E.backfinstarttaper = 10
	bgFinger2E.parent = bgFinger22
	bgFinger2E.rotation.controller.value = (quat 1)
	fixRotation bgFinger2E
	----
	bgFinger30 = BoneSys.createBone posFin30 posFin31 [0,1,0]
	bgFinger30.name = "bg_Finger30"
	bgFinger30.rotation.controller.value = rotFin30
	bgFinger30.wireColor = (color 255 109 51)
	bgFinger30.width = 1
	bgFinger30.height = 1
	bgFinger30.Taper = 90
	bgFinger30.sidefins = off
	bgFinger30.sidefinssize = 2
	bgFinger30.frontfin = off
	bgFinger30.frontfinsize = 2
	bgFinger30.backfin = off
	bgFinger30.backfinsize = 2
	bgFinger30.backfinstarttaper = 10
	fixRotation bgFinger30

	bgFinger31 = BoneSys.createBone posFin31 posFin32 [0,1,0]
	bgFinger31.name = "bg_Finger31"
	bgFinger31.wireColor = (color 255 109 51)
	bgFinger31.width = 1
	bgFinger31.height = 1
	bgFinger31.Taper = 90
	bgFinger31.sidefins = off
	bgFinger31.sidefinssize = 2
	bgFinger31.frontfin = off
	bgFinger31.frontfinsize = 2
	bgFinger31.backfin = off
	bgFinger31.backfinsize = 2
	bgFinger31.backfinstarttaper = 10
	bgFinger31.parent = bgFinger30
	bgFinger31.rotation.controller.value = rotFin31
	fixRotation bgFinger31

	bgFinger32 = BoneSys.createBone posFin32 posFin3Eff [0,1,0]
	bgFinger32.name = "bg_Finger32"
	bgFinger32.wireColor = (color 255 109 51)
	bgFinger32.width = 1
	bgFinger32.height = 1
	bgFinger32.Taper = 90
	bgFinger32.sidefins = off
	bgFinger32.sidefinssize = 2
	bgFinger32.frontfin = off
	bgFinger32.frontfinsize = 2
	bgFinger32.backfin = off
	bgFinger32.backfinsize = 2
	bgFinger32.backfinstarttaper = 10
	bgFinger32.parent = bgFinger31
	bgFinger32.rotation.controller.value = rotFin32
	fixRotation bgFinger32

	bgFinger3E = BoneSys.createBone posFin3Eff ( posFin3Eff + 0.5*(normalize (posFin3Eff - posFin32) ) ) [0,1,0]
	bgFinger3E.name = "bg_Finger3E"
	bgFinger3E.wireColor = (color 255 109 51)
	bgFinger3E.width = 0.5
	bgFinger3E.height = 0.5
	bgFinger3E.Taper = 90
	bgFinger3E.sidefins = off
	bgFinger3E.sidefinssize = 2
	bgFinger3E.frontfin = off
	bgFinger3E.frontfinsize = 2
	bgFinger3E.backfin = off
	bgFinger3E.backfinsize = 2
	bgFinger3E.backfinstarttaper = 10
	bgFinger3E.parent = bgFinger32
	bgFinger3E.rotation.controller.value = (quat 1)
	fixRotation bgFinger3E
	----
	bgFinger40 = BoneSys.createBone posFin40 posFin41 [0,1,0]
	bgFinger40.name = "bg_Finger40"
	bgFinger40.rotation.controller.value = rotFin40
	bgFinger40.wireColor = (color 255 109 51)
	bgFinger40.width = 1
	bgFinger40.height = 1
	bgFinger40.Taper = 90
	bgFinger40.sidefins = off
	bgFinger40.sidefinssize = 2
	bgFinger40.frontfin = off
	bgFinger40.frontfinsize = 2
	bgFinger40.backfin = off
	bgFinger40.backfinsize = 2
	bgFinger40.backfinstarttaper = 10
	fixRotation bgFinger40

	bgFinger41 = BoneSys.createBone posFin41 posFin42 [0,1,0]
	bgFinger41.name = "bg_Finger41"
	bgFinger41.wireColor = (color 255 109 51)
	bgFinger41.width = 1
	bgFinger41.height = 1
	bgFinger41.Taper = 90
	bgFinger41.sidefins = off
	bgFinger41.sidefinssize = 2
	bgFinger41.frontfin = off
	bgFinger41.frontfinsize = 2
	bgFinger41.backfin = off
	bgFinger41.backfinsize = 2
	bgFinger41.backfinstarttaper = 10
	bgFinger41.parent = bgFinger40
	bgFinger41.rotation.controller.value = rotFin41
	fixRotation bgFinger41

	bgFinger42 = BoneSys.createBone posFin42 posFin4Eff [0,1,0]
	bgFinger42.name = "bg_Finger42"
	bgFinger42.wireColor = (color 255 109 51)
	bgFinger42.width = 1
	bgFinger42.height = 1
	bgFinger42.Taper = 90
	bgFinger42.sidefins = off
	bgFinger42.sidefinssize = 2
	bgFinger42.frontfin = off
	bgFinger42.frontfinsize = 2
	bgFinger42.backfin = off
	bgFinger42.backfinsize = 2
	bgFinger42.backfinstarttaper = 10
	bgFinger42.parent = bgFinger41
	bgFinger42.rotation.controller.value = rotFin42
	fixRotation bgFinger42

	bgFinger4E = BoneSys.createBone posFin4Eff ( posFin4Eff + 0.5*(normalize (posFin4Eff - posFin42) ) ) [0,1,0]
	bgFinger4E.name = "bg_Finger4E"
	bgFinger4E.wireColor = (color 255 109 51)
	bgFinger4E.width = 0.5
	bgFinger4E.height = 0.5
	bgFinger4E.Taper = 90
	bgFinger4E.sidefins = off
	bgFinger4E.sidefinssize = 2
	bgFinger4E.frontfin = off
	bgFinger4E.frontfinsize = 2
	bgFinger4E.backfin = off
	bgFinger4E.backfinsize = 2
	bgFinger4E.backfinstarttaper = 10
	bgFinger4E.parent = bgFinger42
	bgFinger4E.rotation.controller.value = (quat 1)
	fixRotation bgFinger4E
	----
	bgFinger00.parent = bgHand
	bgFinger10.parent = bgHand
	bgFinger20.parent = bgHand
	bgFinger30.parent = bgHand
	bgFinger40.parent = bgHand

	BGLayer.addNode bgFinger00
	BGLayer.addNode bgFinger01
	BGLayer.addNode bgFinger02
	BGLayer.addNode bgFinger0E
	BGLayer.addNode bgFinger10
	BGLayer.addNode bgFinger11
	BGLayer.addNode bgFinger12
	BGLayer.addNode bgFinger1E
	BGLayer.addNode bgFinger20
	BGLayer.addNode bgFinger21
	BGLayer.addNode bgFinger22
	BGLayer.addNode bgFinger2E
	BGLayer.addNode bgFinger30
	BGLayer.addNode bgFinger31
	BGLayer.addNode bgFinger32
	BGLayer.addNode bgFinger3E
	BGLayer.addNode bgFinger40
	BGLayer.addNode bgFinger41
	BGLayer.addNode bgFinger42
	BGLayer.addNode bgFinger4E

	-------------------------------------------------
	lineTeresMajor = splineShape ()
	addNewSpline lineTeresMajor
	addKnot lineTeresMajor 1 #corner #line [-8.56163,2.15393,133.849]
	addKnot lineTeresMajor 1 #corner #line [-14.3548,2.7063,140.739]
	updateshape lineTeresMajor
	lineTeresMajor.wireColor = (color 254 7 1)
	lineTeresMajor.isFrozen = true
	lineTeresMajor.showFrozenInGray = false
	lineTeresMajor.parent = bgRoot

	tmIKCtrl = Spline_IK_Control()
	addModifier lineTeresMajor tmIKCtrl
	tmIKCtrl.helper_size = 2
	tmIKCtrl.createHelper 2
	tmSIKPointList = tmIKCtrl.helper_list

	tmSIKPointList[1].wireColor = (color 255 247 15)
	tmSIKPointList[2].wireColor = (color 255 247 15)
	tmSIKPointList[1].name = "bg_TeresMajor1"
	tmSIKPointList[2].name = "bg_TeresMajor2"
	tmSIKPointList[1].parent = bgRoot
	tmSIKPointList[2].parent = bgRoot

	BGLayer.addNode lineTeresMajor
	BGLayer.addNode tmSIKPointList[1]
	BGLayer.addNode tmSIKPointList[2]
	----------------------------------------------------
	--Stern
	lineStern = splineShape ()
	addNewSpline lineStern
	addKnot lineStern 1 #corner #line [-1.03037,-4.54383,143.196]
	addKnot lineStern 1 #corner #line [-2.6866,-2.65107,151.632]
	updateshape lineStern
	lineStern.wireColor = (color 254 7 1)
	lineStern.isFrozen = true
	lineStern.showFrozenInGray = false
	lineStern.parent = bgRoot

	stIKCtrl = Spline_IK_Control()
	addModifier lineStern stIKCtrl
	stIKCtrl.helper_size = 2
	stIKCtrl.createHelper 2
	stSIKPointList = stIKCtrl.helper_list

	stSIKPointList[1].wireColor = (color 255 247 15)
	stSIKPointList[2].wireColor = (color 255 247 15)
	stSIKPointList[1].name = "bg_Stem1"
	stSIKPointList[2].name = "bg_Stem2"
	stSIKPointList[1].parent = bgRoot
	stSIKPointList[2].parent = bgRoot

	BGLayer.addNode lineStern
	BGLayer.addNode stSIKPointList[1]
	BGLayer.addNode stSIKPointList[2]
	-----------------------------------------------------
	nset2 = NURBSSet ()
	c = NURBSCVCurve name:"CV Curve" order:3 numCVs:3 numKnots:6
	for k in 1 to 3 do ( setKnot c k 0; setKnot c (k+3) 1 )
	cv = NURBSControlVertex [0.0773101,-11.4487,131.018]
	setCV c 1 cv
	cv.pos = [-8.02592,-11.4577,131.004]
	setCV c 2 cv
	cv.pos = [-9.85713,-4.63212,140.011]
	setCV c 3 cv
	appendObject nset2 c
	-- create the NURBS object from the NURBSSet
	refBustCurve = NURBSNode nset2 name:"rf_BustLine" pos:[0,0,0]
	refBustCurve.wireColor = (color 254 7 1)--(color 255 109 51)
	refBustCurve.parent = bgRoot
	BGLayer.addNode refBustCurve

	blIKCtrlModify = Spline_IK_Control()
	addModifier refBustCurve blIKCtrlModify
	blIKCtrlModify.helper_size = 2
	blIKCtrlModify.createHelper 3
	blSIKPointList = blIKCtrlModify.helper_list
	for i = 1 to (blSIKPointList.count) do
	(
		blSIKPointList[i].wireColor = (color 255 247 15)
		blSIKPointList[i].name = "bg_BustRootPos_" + (i as string)
		blSIKPointList[i].parent = bgRoot
		BGLayer.addNode blSIKPointList[i]
	)

	BustPosList = #()
	append BustPosList [-4.81341,-10.6231,132.106]
	append BustPosList [-6.39851,-16.4595,133.6]
	append BustPosList [-5.80024,-14.2552,133.006]

	bgBust0 = BoneSys.createBone BustPosList[1] BustPosList[2] [0,0,1]
	bgBust0.name = "bg_Bust0"
	bgBust0.wireColor = (color 255 109 51)
	bgBust0.width = 4
	bgBust0.height = 4
	bgBust0.Taper = 90
	bgBust0.sidefins = off
	bgBust0.sidefinssize = 2
	bgBust0.frontfin = off
	bgBust0.frontfinsize = 2
	bgBust0.backfin = off
	bgBust0.backfinsize = 2
	bgBust0.parent = bgRoot

	bgBust1 = BoneSys.createBone BustPosList[2] BustPosList[3] [0,0,1]
	bgBust1.name = "bg_Bust1"
	bgBust1.wireColor = (color 255 109 51)
	bgBust1.width = 2
	bgBust1.height = 2
	bgBust1.Taper = 90
	bgBust1.sidefins = off
	bgBust1.sidefinssize = 2
	bgBust1.frontfin = off
	bgBust1.frontfinsize = 2
	bgBust1.backfin = off
	bgBust1.backfinsize = 2
	bgBust1.parent = bgBust0

	bgBustE = BoneSys.createBone BustPosList[3] BustPosList[3] [0,0,1]
	bgBustE.name = "bg_BustEff"
	bgBustE.wireColor = (color 255 109 51)
	bgBustE.width = 1
	bgBustE.height = 1
	bgBustE.Taper = 90
	bgBustE.sidefins = off
	bgBustE.sidefinssize = 2
	bgBustE.frontfin = off
	bgBustE.frontfinsize = 2
	bgBustE.backfin = off
	bgBustE.backfinsize = 2
	bgBustE.parent = bgBust1
	bgBustE.rotation.controller.value = (quat 1)
	bgBustE.length = 1

	bgBust0.pos.controller = Path_Constraint percent:31 follow:false path:refBustCurve loop:off
	deleteKeys bgBust0 #AllKeys

	BGLayer.addNode bgBust0
	BGLayer.addNode bgBust1
	BGLayer.addNode bgBustE
)

createBipedGuide()