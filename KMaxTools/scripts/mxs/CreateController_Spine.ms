max modify mode

spineInfoCA = attributes spineInfo
(
	parameters main
	(
		XAngle type:#float
		ChestRoll type:#float
	)
)

curveInfoCA = attributes curveInfo
(
	parameters main
	(
		Length type:#float
		OriginLength type:#float
		StretchRatio type:#float
		StretchLength type:#float
	)
)

controlInfoCA = attributes "BipedControl"
attribID:#(0x263bcbd3, 0x4f732a71)
(
	parameters main rollout:BipedControl
	(
		bSoftIK type:#boolean ui:cbSoftIK default:false
		fIKFK_R type:#float ui:sdIKFK_R default:1.0
		fIKFK_L type:#float ui:sdIKFK_L default:1.0
		bRootFw type:#boolean ui:cbRootForward default:true
		bRootSd type:#boolean ui:cbRootSide default:false
		bRootYR type:#boolean ui:cbRootYawRot default:false
		ScriptPath type:#string default:""
	)
	rollout BipedControl "Biped Control"
	(
		group "IK / FK" (
			checkBox cbSoftIK "Enable Soft-IK"
			-----
			label lbRightArm "Right Arm :" align:#left offset:[0,8]
			label lbFK_R "FK" across:3 align:#left offset:[0,14]
			slider sdIKFK_R "" align:#center width:110 range:[0,1,1] tick:5 offset:[8,0]
			label lbIK_R "IK" align:#right offset:[0,14]
			-----
			label lbLeftArm "Left Arm :" align:#left offset:[0,8]
			label lbFK_L "FK" across:3 align:#left offset:[0,14]
			slider sdIKFK_L "" align:#center width:110 range:[0,1,1] tick:5 offset:[8,0]
			label lbIK_L "IK" align:#right offset:[0,14]
		)
		group "Root" (
		    checkBox cbRootForward "Root Motion Forward"
		    checkBox cbRootSide "Root Motion Side"
		    checkBox cbRootYawRot "Root Motion Yaw Rotate" offset:[0,20]
		)
		button btnAnmTool "Open Anm Tools" 

		on btnAnmTool pressed do (
			--filein "E:/CloudDrive/Dropbox/tools/KMaxTools/scripts/KBipedAnmTools.ms"
			python.executeFile (ScriptPath+"KAnmToolsMAX.py")
		)
	)
)

fn createLineCtrl pointList bClose = (
	lineStern = splineShape ()
	addNewSpline lineStern
	for i = 1 to pointList.count do (
		addKnot lineStern 1 #corner #line pointList[i]
	)
	if bClose then (
		addKnot lineStern 1 #corner #line pointList[1]
	)
	updateshape lineStern
	return lineStern
)

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

fn ResetTransformController obj = (
	obj.position.controller = Position_XYZ()
	obj.rotation.controller = Euler_XYZ()
	obj.scale.controller = bezier_scale()
)

fn getSymMtx mtx flipAxis = (
	case flipAxis of (
		"x":(
			return (matrix3 [ mtx[1].x,-mtx[1].y,-mtx[1].z] [-mtx[2].x, mtx[2].y, mtx[2].z] [-mtx[3].x, mtx[3].y, mtx[3].z] [-mtx[4].x, mtx[4].y, mtx[4].z])
		)
		"y":(
			return (matrix3 [-mtx[1].x, mtx[1].y, mtx[1].z] [ mtx[2].x,-mtx[2].y,-mtx[2].z] [-mtx[3].x, mtx[3].y, mtx[3].z] [-mtx[4].x, mtx[4].y, mtx[4].z])
		)
		"z":(
			return (matrix3 [-mtx[1].x, mtx[1].y, mtx[1].z] [-mtx[2].x, mtx[2].y, mtx[2].z] [ mtx[3].x,-mtx[3].y,-mtx[3].z] [-mtx[4].x, mtx[4].y, mtx[4].z])
		)
		"all":(
			return (matrix3 [ mtx[1].x,-mtx[1].y,-mtx[1].z] [ mtx[2].x,-mtx[2].y,-mtx[2].z] [ mtx[3].x,-mtx[3].y,-mtx[3].z] [-mtx[4].x, mtx[4].y, mtx[4].z])
		)
	)
	return undefined
)

fn GenSymObject obj flipAxis = (
	maxOps.cloneNodes obj cloneType:#copy newNodes:&cloneObj
	cloneObj = cloneObj[1]
	ResetTransformController cloneObj
	cloneObj.transform = getSymMtx obj.transform flipAxis
	
	mScl = [1,1,1]
	case flipAxis of (
		"x":( mScl = [-1,1,1])
		"y":( mScl = [1,-1,1])
		"z": (mScl = [1,1,-1])
		"all": (mScl = [-1,-1,-1])
	)
	
	modifyXform = XForm()
	addModifier cloneObj modifyXform
	modifyXform.gizmo.scale = mScl
	maxOps.CollapseNode cloneObj off
	return cloneObj
)



fn fixRotation obj = (
	obj.rotation.controller = tcb_rotation ()
	obj.rotation.controller = Euler_XYZ ()
)

bgLayer = LayerManager.getLayerFromName "BipedGuide"
if bgLayer != undefined then (
    bgLayer.ishidden = True
)

layer = LayerManager.getLayerFromName "Controller"
if layer == undefined then (
    layer = LayerManager.newLayer()
    layer.setname "Controller"
)

hideLayer = LayerManager.getLayerFromName "x.Hidden"
if hideLayer == undefined do (
    hideLayer = LayerManager.newLayer()
    hideLayer.setname "x.Hidden"
)

CtrlRoot = getNodeByName "ControlRoot"
if CtrlRoot == undefined then (
    CtrlRoot = Dummy name:"ControlRoot" pos:[0,0,0] boxsize:[75,75,1]
    CtrlRoot.scale.controller = SlaveScale()
)



layer.addNode CtrlRoot
CustAttributes.add CtrlRoot controlInfoCA
CtrlRoot.bSoftIK.controller = bezier_float()
CtrlRoot.fIKFK_R.controller = bezier_float()
CtrlRoot.fIKFK_L.controller = bezier_float()
CtrlRoot.bRootFw.controller = bezier_float()
CtrlRoot.bRootSd.controller = bezier_float()
CtrlRoot.bRootYR.controller = bezier_float()

rotXUpFix = getNodeByName "rotXUpFix"
if rotXUpFix == undefined do (
    rotXUpFix = point name:"rotXUpFix" pos:[0,0,0] size:1
)
rotXUpFix.transform = matrix3 [0,0,1] [0,1,0] [-1,0,0] CtrlRoot.transform.pos
rotXUpFix.parent = CtrlRoot
hideLayer.addNode rotXUpFix

rotYUpFix = getNodeByName "rotYUpFix"
if rotYUpFix == undefined do (
    rotYUpFix = point name:"rotYUpFix" pos:[0,0,0] size:1
)
rotYUpFix.transform = matrix3 [1,0,0] [0,0,1] [0,-1,0] CtrlRoot.transform.pos
rotYUpFix.parent = CtrlRoot
hideLayer.addNode rotYUpFix

-- oriSpineCurve = getNodeByName "bg_SpineLine"
hipNode = getNodeByName "bg_Hip"
spNode1 = getNodeByName "bg_SpineLineCtrl_1"
spNode2 = getNodeByName "bg_SpineLineCtrl_2"
spNode3 = getNodeByName "bg_SpineLineCtrl_3"
spNode4 = getNodeByName "bg_SpineLineCtrl_4"

posHip = hipNode.transform.pos
posSpNode1 = spNode1.transform.pos
posSpNode2 = spNode2.transform.pos
posSpNode3 = spNode3.transform.pos
posSpNode4 = spNode4.transform.pos

spSeg1 = getNodeByName "bg_SpineSeg1"
spSeg2 = getNodeByName "bg_SpineSeg2"
-- spSeg3 = getNodeByName "bg_SpineSeg3"

persSeg1 = spSeg1.pos.controller.percent
persSeg2 = spSeg2.pos.controller.percent
-- persSeg3 = spSeg3.pos.controller.percent

posSpSeg1 = spSeg1.transform.pos
posSpSeg2 = spSeg2.transform.pos
-- posSpSeg3 = spSeg3.transform.pos

bustNode = getNodeByName "bg_Bust0"
posBust = bustNode.transform.pos
posBustX0 = [0, posBust.y, posBust.z]

CtrlSpinePointList = #(
	[0, 20, 25],
	[0, 20,-25],
	[0,-20,-25],
	[0,-20, 25]
)

r = 16
-- CtrlWaistPointList = #(
-- 	[0, r*(sin 0), r*(cos 0)],
-- 	[0, r*(sin 30), r*(cos 30)],
-- 	[0, r*(sin 60), r*(cos 60)],
-- 	[0, r*(sin 90), r*(cos 90)],
-- 	[0, r*(sin 120), r*(cos 120)],
-- 	[0, r*(sin 150), r*(cos 150)],
-- 	[0, r*(sin 180), r*(cos 180)],
-- 	[0, r*(sin 210), r*(cos 210)],
-- 	[0, r*(sin 240), r*(cos 240)],
-- 	[0, r*(sin 270), r*(cos 270)],
-- 	[0, r*(sin 300), r*(cos 300)],
-- 	[0, r*(sin 330), r*(cos 330)]
-- )
CtrlWaistPointList = #()
for i = 0 to 48 do (
	ang = i / 48.0 * 360.0
	append CtrlWaistPointList [0, r*(sin ang), r*(cos ang)]
)

HipXAxis = normalize(posSpNode1 - posHip)
Spine0XAxis = normalize( ( normalize (posSpSeg2 - posSpNode1) ) + ( normalize (posSpNode2 - posSpNode1) ) )
ChestXAxis = posSpNode4 - posSpNode3
ChestCtrlPos = (posBustX0 + posSpSeg2)*0.5

ctrlHip = createLineCtrl CtrlSpinePointList true
ctrlHip.name = "Ctrl_Hip"
ctrlHip.wireColor = (color 10 144 177)
ctrlHip.transform = getAimMatrix 1 HipXAxis 3 [-1,0,0] posHip
ctrlHip.parent = rotXUpFix
ctrlHip.scale.controller = SlaveScale()

-- conSpineRoot = createLineCtrl CtrlSpinePointList true
conSpineRoot = point name:"conSpineRoot" size:1.5 axistripod:off centermarker:off drawontop:off constantscreensize:off
-- conSpineRoot.name = "conSpineRoot"
conSpineRoot.wireColor = (color 10 144 177)
conSpineRoot.transform = getAimMatrix 1 Spine0XAxis 3 [-1,0,0] posSpNode1
conSpineRoot.parent = ctrlHip
conSpineRoot.scale.controller = SlaveScale()
hideLayer.addNode conSpineRoot

ctrlChest = createLineCtrl CtrlSpinePointList true
ctrlChest.name = "Ctrl_Chest"
ctrlChest.wireColor = (color 10 144 177)
ctrlChest.transform = getAimMatrix 1 ChestXAxis 3 [-1,0,0] ChestCtrlPos
ctrlChest.parent = rotXUpFix
ctrlChest.scale.controller = SlaveScale()
CustAttributes.add ctrlChest spineInfoCA

rootPointWaist = point name:"rpWaist" size:1 axistripod:off centermarker:off drawontop:off constantscreensize:off
rootPointWaist.parent = rotXUpFix
rootPointWaist.position.controller = position_script()
rootPointWaist.position.controller.IScriptCtrl.AddNode "self" rootPointWaist
rootPointWaist.position.controller.IScriptCtrl.AddNode "Node0" conSpineRoot
rootPointWaist.position.controller.IScriptCtrl.AddNode "Node1" ctrlChest
rootPointWaistPosScriptStr = "invPMtx = inverse self.parent.transform\n"+ \
						"cen = (Node0.transform.pos + Node1.transform.pos)*0.5\n"+ \
						"tVec = Node1.transform.pos - Node0.transform.pos\n"+ \
						"bin = cross Node0.transform.row1 Node1.transform.row1\n"+ \
						"tan = (cross tVec bin)*0.4\n"+ \
						"pos = tan + cen\n"+ \
						"return pos * invPMtx\n"
rootPointWaist.position.controller.IScriptCtrl.SetExpression rootPointWaistPosScriptStr
rootPointWaist.rotation.controller = Orientation_Constraint ()
rootPointWaist.rotation.controller.appendtarget conSpineRoot 50
rootPointWaist.rotation.controller.appendtarget ctrlChest 50
hideLayer.addNode rootPointWaist

ctrlWaist = createLineCtrl CtrlWaistPointList true
ctrlWaist.name = "Ctrl_Waist"
ctrlWaist.wireColor = (color 10 144 177)
ctrlWaist.parent = rootPointWaist
ctrlWaist.transform = rootPointWaist.transform
ctrlWaist.scale.controller = SlaveScale()
ctrlWaist.rotation.controller = SlaveRotation()

-- layer.addNode conSpineRoot
layer.addNode ctrlWaist
layer.addNode ctrlChest
layer.addNode ctrlHip

ctrlChest.XAngle.controller = float_script()
ctrlChest.XAngle.controller.IScriptCtrl.AddNode "Node0" conSpineRoot
ctrlChest.XAngle.controller.IScriptCtrl.AddNode "Node1" ctrlChest
ctrlChestXAngleScriptStr = ("XdX = dot Node0.transform.row1 Node1.transform.row1\n"+ \
						"XdX *= XdX\n"+ \
						"return XdX")
ctrlChest.XAngle.controller.IScriptCtrl.SetExpression ctrlChestXAngleScriptStr

-- chestRollScript = float_script()
-- chestRollScript.IScriptCtrl.AddNode "Node0" conSpineRoot
-- chestRollScript.IScriptCtrl.AddNode "Node1" ctrlChest
-- scriptStr = "locQuat = (Node1.transform * (inverse Node0.transform)).rotation\n" + \
-- 			"RollEuler = quatToEuler (Quat locQuat.x 0 0 locQuat.w)\n" + \
-- 			"return RollEuler.x"
-- chestRollScript.IScriptCtrl.SetExpression scriptStr
-- ctrlChest.ChestRoll.controller = chestRollScript

---------------------
nset = NURBSSet ()
c = NURBSCVCurve name:"CV Curve" order:4 numCVs:4 numKnots:8
for k in 1 to 4 do ( setKnot c k 0; setKnot c (k+4) 1 )
cv = NURBSControlVertex posSpNode1
setCV c 1 cv
cv.pos = posSpNode2
setCV c 2 cv
cv.pos = posSpNode3
setCV c 3 cv
cv.pos = posSpNode4
setCV c 4 cv
appendObject nset c
-- create the NURBS object from the NURBSSet
rfSpineLine = NURBSNode nset name:"rf_SpineLine" pos:[0,0,0]
rfSpineLine.wireColor = (color 0 0 0)--(color 255 109 51)
rfSpineLine.parent = CtrlRoot
hideLayer.addNode rfSpineLine

rfIKConModifier = Spline_IK_Control()
addModifier rfSpineLine rfIKConModifier
rfIKConModifier.helper_size = 2
rfIKConModifier.createHelper 4
bgSIKPointList = rfIKConModifier.helper_list
for i = 1 to (bgSIKPointList.count) do
(
	bgSIKPointList[i].wireColor = (color 40 0 0)
	bgSIKPointList[i].name = "py_SpineLineCtrl_" + (i as string)
	bgSIKPointList[i].parent = CtrlRoot
	hideLayer.addNode bgSIKPointList[i]
)

CustAttributes.add rfSpineLine curveInfoCA
rfSpineLine.OriginLength.controller = bezier_float()
rfSpineLine.StretchRatio.controller = bezier_float()
rfSpineLine.OriginLength = curveLength rfSpineLine
rfSpineLine.StretchRatio = 0.5
rfSpineLine.Length.controller = float_script()
rfSpineLine.Length.controller.IScriptCtrl.AddNode "self" rfSpineLine
rfSpineLine.Length.controller.IScriptCtrl.SetExpression "curveLength self"
tmpScript = float_script()
tmpScript.IScriptCtrl.AddNode "self" rfSpineLine
-- tmpScript.IScriptCtrl.AddTarget "oriLen" rfSpineLine.OriginLength.controller
-- tmpScript.IScriptCtrl.AddTarget "curLen" rfSpineLine.Length.controller
-- tmpScript.IScriptCtrl.AddTarget "Ratio" rfSpineLine.StretchRatio.controller
-- tmpScript.IScriptCtrl.SetExpression "((curveLength self) - oriLen) * Ratio + oriLen"
tmpScript.IScriptCtrl.SetExpression "(self.Length - self.OriginLength) * self.StretchRatio + self.OriginLength"
rfSpineLine.StretchLength.controller = tmpScript
-- rfSpineLine.StretchLength.controller = float_script()
-- rfSpineLine.StretchLength.controller.IScriptCtrl.AddTarget "oriLen" rfSpineLine.OriginLength.controller
-- rfSpineLine.StretchLength.controller.IScriptCtrl.AddTarget "curLen" rfSpineLine.Length.controller
-- rfSpineLine.StretchLength.controller.IScriptCtrl.AddTarget "Ratio" rfSpineLine.StretchRatio.controller
-- rfSpineLine.StretchLength.controller.IScriptCtrl.SetExpression "(curLen - oriLen) * Ratio + oriLen"



lpWaistA1 = point name:"lpWaistA1" pos:posSpNode3 size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
lpWaistA2 = point name:"lpWaistA2" pos:posSpNode3 size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
lpWaistB1 = point name:"lpWaistB1" pos:posSpNode2 size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
lpWaistB2 = point name:"lpWaistB2" pos:posSpNode2 size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
cpWaistA = point name:"cpWaistA" pos:posSpNode3 size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
cpWaistB = point name:"cpWaistB" pos:posSpNode3 size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off

lpWaistA1.parent = ctrlChest
lpWaistA2.parent = ctrlWaist
lpWaistB1.parent = conSpineRoot
lpWaistB2.parent = ctrlWaist
cpWaistA.parent = ctrlWaist
cpWaistB.parent = ctrlWaist

cpWaistA.position.controller = Position_Constraint()
cpWaistA.position.controller.appendtarget lpWaistA1 50
cpWaistA.position.controller.appendtarget lpWaistA2 50
cpWaistB.position.controller = Position_Constraint()
cpWaistB.position.controller.appendtarget lpWaistB1 50
cpWaistB.position.controller.appendtarget lpWaistB2 50


scriptStr1 = "dis = (distance [0,0,0] NodePos) * 0.2\n" + \
			"if dis > 1 do dis = 1\n" + \
			"v = (1 - dis) * val\n" + \
			"return v * 50"
scriptStr2 = "dis = (distance [0,0,0] NodePos) * 0.2\n" + \
			"if dis > 1 do dis = 1\n" + \
			"v = (1 - dis) * val\n" + \
			"return (1 - v) * 50"

fScript1 = float_script()
fScript1.IScriptCtrl.AddTarget "val" ctrlChest.XAngle.controller
fScript1.IScriptCtrl.AddTarget "NodePos" ctrlWaist.position.controller
fScript1.IScriptCtrl.SetExpression scriptStr1

fScript2 = float_script()
fScript2.IScriptCtrl.AddTarget "val" ctrlChest.XAngle.controller
fScript2.IScriptCtrl.AddTarget "NodePos" ctrlWaist.position.controller
fScript2.IScriptCtrl.SetExpression scriptStr2

cpWaistA.position.controller.weight[1].controller = fScript1
cpWaistA.position.controller.weight[2].controller = fScript2
cpWaistB.position.controller.weight[1].controller = fScript1
cpWaistB.position.controller.weight[2].controller = fScript2

hideLayer.addNode lpWaistA1
hideLayer.addNode lpWaistA2
hideLayer.addNode lpWaistB1
hideLayer.addNode lpWaistB2
hideLayer.addNode cpWaistA
hideLayer.addNode cpWaistB

bgSIKPointList[1].parent = conSpineRoot
bgSIKPointList[2].parent = cpWaistB
bgSIKPointList[3].parent = cpWaistA
bgSIKPointList[4].parent = ctrlChest

bgSIKPointList[1].transform = getAimMatrix 1 conSpineRoot.transform.row1 3 conSpineRoot.transform.row3 conSpineRoot.transform.pos
spineLineEnd = point name:"spineLineEnd" pos:posSpNode4 size:1 cross:on Box:off wirecolor:(color 0 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
spineLineEnd.pos.controller = Path_Constraint percent:100 follow:true path:rfSpineLine loop:off
deleteKeys spineLineEnd #AllKeys
spineLineEnd.parent = CtrlRoot
hideLayer.addNode spineLineEnd

---------------
pathConstNode1 = point name:"pathConstNode1" pos:posSpSeg1 size:1 cross:on Box:off wirecolor:(color 0 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
pathConstNode2 = point name:"pathConstNode2" pos:posSpSeg2 size:1 cross:on Box:off wirecolor:(color 0 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
-- pathConstNode3 = point name:"pathConstNode3" pos:posSpSeg3 size:1 cross:on Box:off wirecolor:(color 0 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
pathConstNode4 = point name:"pathConstNode4" pos:posSpNode4 size:1 cross:on Box:off wirecolor:(color 0 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
pathConstNode1.parent = CtrlRoot
pathConstNode2.parent = CtrlRoot
-- pathConstNode3.parent = CtrlRoot
pathConstNode4.parent = CtrlRoot
hideLayer.addNode pathConstNode1
hideLayer.addNode pathConstNode2
-- hideLayer.addNode pathConstNode3
hideLayer.addNode pathConstNode4

pathConstNode1.pos.controller = Path_Constraint percent:persSeg1 follow:false path:rfSpineLine loop:off
pathConstNode1.pos.controller.percent.controller = float_script()
pathConstNode1.pos.controller.percent.controller.IScriptCtrl.AddNode "curve" rfSpineLine
scriptStr = "(curve.StretchLength * " + ((persSeg1*0.01) as string) + ") / curve.Length"
pathConstNode1.pos.controller.percent.controller.IScriptCtrl.SetExpression scriptStr

pathConstNode2.pos.controller = Path_Constraint percent:persSeg2 follow:false path:rfSpineLine loop:off
pathConstNode2.pos.controller.percent.controller = float_script()
pathConstNode2.pos.controller.percent.controller.IScriptCtrl.AddNode "curve" rfSpineLine
scriptStr = "(curve.StretchLength * " + ((persSeg2*0.01) as string) + ") / curve.Length"
pathConstNode2.pos.controller.percent.controller.IScriptCtrl.SetExpression scriptStr

-- pathConstNode3.pos.controller = Path_Constraint percent:persSeg3 follow:false path:rfSpineLine loop:off
-- pathConstNode3.pos.controller.percent.controller = float_script()
-- pathConstNode3.pos.controller.percent.controller.IScriptCtrl.AddNode "curve" rfSpineLine
-- scriptStr = "(curve.StretchLength * " + ((persSeg3*0.01) as string) + ") / curve.Length"
-- pathConstNode3.pos.controller.percent.controller.IScriptCtrl.SetExpression scriptStr

pathConstNode4.pos.controller = Path_Constraint percent:100 follow:false path:rfSpineLine loop:off
pathConstNode4.pos.controller.percent.controller = float_script()
pathConstNode4.pos.controller.percent.controller.IScriptCtrl.AddNode "curve" rfSpineLine
scriptStr = "curve.StretchLength / curve.Length"
pathConstNode4.pos.controller.percent.controller.IScriptCtrl.SetExpression scriptStr

locSpine4 = point name:"locSpine4" pos:posSpNode4 size:1.5 cross:off Box:on wirecolor:(color 128 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
-- locSpine3 = point name:"locSpine3" pos:posSpSeg3 size:1.5 cross:off Box:on wirecolor:(color 128 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
locSpine4.parent = pathConstNode4
-- locSpine3.parent = pathConstNode3
hideLayer.addNode locSpine4
-- hideLayer.addNode locSpine3

locSpine4.pos.controller = position_script()
locSpine4.pos.controller.IScriptCtrl.AddNode "parentNode" pathConstNode4
locSpine4.pos.controller.IScriptCtrl.AddNode "tanNode" spineLineEnd
locSpine4.pos.controller.IScriptCtrl.AddNode "curve" rfSpineLine
scriptStr = "Ratio = parentNode.pos.controller.percent / 100.0\n" + \
			"if Ratio <= 1.0 then return [0,0,0]\n" + \
			"else (\n" + \
			"    wPos = (Ratio - 1) * tanNode.transform.row1 * curve.StretchLength + parentNode.transform.pos\n" + \
			"    return wPos * (inverse parentNode.transform))"

locSpine4.pos.controller.IScriptCtrl.SetExpression scriptStr

-- locSpine3.pos.controller = position_script()
-- locSpine3.pos.controller.IScriptCtrl.AddNode "parentNode" pathConstNode3
-- locSpine3.pos.controller.IScriptCtrl.AddNode "tanNode" spineLineEnd
-- locSpine3.pos.controller.IScriptCtrl.AddNode "curve" rfSpineLine
-- scriptStr = "Ratio = parentNode.pos.controller.percent / 100.0\n" + \
-- 			"if Ratio <= 1.0 then return [0,0,0]\n" + \
-- 			"else (\n" + \
-- 			"    wPos = (Ratio - 1) * tanNode.transform.row1 * curve.StretchLength + parentNode.transform.pos\n" + \
-- 			"    return wPos * (inverse parentNode.transform))"
-- locSpine3.pos.controller.IScriptCtrl.SetExpression scriptStr
--------------------------------------------------------------------------

boneSpineList = #()
-- boneHip = BoneSys.createBone bgSIKPointList[1].transform.pos pathConstNode1.transform.pos [0,1,0]
boneSpine1 = BoneSys.createBone bgSIKPointList[1].transform.pos pathConstNode1.transform.pos [0,1,0]
boneSpine2 = BoneSys.createBone pathConstNode1.transform.pos pathConstNode2.transform.pos [0,1,0]
boneSpine3 = BoneSys.createBone pathConstNode2.transform.pos pathConstNode4.transform.pos [0,1,0]
-- boneSpine4 = BoneSys.createBone pathConstNode3.transform.pos pathConstNode4.transform.pos [0,1,0]
boneSpineE = BoneSys.createBone pathConstNode4.transform.pos pathConstNode4.transform.pos [0,1,0]
append boneSpineList boneSpine1
append boneSpineList boneSpine2
append boneSpineList boneSpine3
-- append boneSpineList boneSpine4
append boneSpineList boneSpineE

for sp in boneSpineList do
(
	-- name:"bgRfSpine1" wireColor:(color 254 7 1) showFrozenInGray:false isFrozen:true
	sp.wireColor = (color 5 17 33)
	sp.width = 4
	sp.height = 4
	sp.Taper = 90
	sp.sidefins = off
	sp.sidefinssize = 2
	sp.frontfin = off
	sp.frontfinsize = 2
	sp.backfin = off
	sp.backfinsize = 2
	hideLayer.addNode sp
)
boneSpineE.width = 2
boneSpineE.height = 2
boneSpineE.length = 2

boneSpine1.parent = bgSIKPointList[1]
boneSpine2.parent = boneSpine1
boneSpine3.parent = boneSpine2
-- boneSpine4.parent = boneSpine3
boneSpineE.parent = boneSpine3
boneSpineE.rotation.controller.value = (quat 0 0 0 1)

boneSpine1.rotation.controller = rotation_script()
boneSpine1.rotation.controller.IScriptCtrl.AddObject "NodePos" boneSpine1.pos.controller
boneSpine1.rotation.controller.IScriptCtrl.AddNode "Parent" bgSIKPointList[1]
boneSpine1.rotation.controller.IScriptCtrl.AddNode "Target" pathConstNode1
boneSpine1.rotation.controller.IScriptCtrl.SetExpression ("theTargetVector=(Target.transform.position * Inverse Parent.transform)-NodePos.value\n" + \
														"theAxis=Normalize (cross theTargetVector [1,0,0])\n" + \
														"theAngle=acos (dot (Normalize theTargetVector) [1,0,0])\n" + \
														"Quat theAngle theAxis")

--------------
boneSpine2.position.controller = Position_Constraint()
boneSpine2.position.controller.appendtarget pathConstNode1 50

boneSpine2.rotation.controller = rotation_script()
-- boneSpine2.rotation.controller.IScriptCtrl.AddObject "Roll" ctrlChest.ChestRoll.controller
boneSpine2.rotation.controller.IScriptCtrl.AddNode "Node" pathConstNode1
boneSpine2.rotation.controller.IScriptCtrl.AddNode "Parent" boneSpine1
boneSpine2.rotation.controller.IScriptCtrl.AddNode "Target" pathConstNode2
boneSpine2.rotation.controller.IScriptCtrl.SetExpression ("theTargetVector=(Target.transform.position * Inverse Parent.transform) - (Node.transform.position * Inverse Parent.transform)\n" + \
														"theAxis=Normalize (cross theTargetVector [1,0,0])\n" + \
														"theAngle=acos (dot (Normalize theTargetVector) [1,0,0])\n" + \
														"Quat theAngle theAxis")--"(eulerToQuat (eulerAngles (Roll.value/3) 0 0)) * (Quat theAngle theAxis)")
----------------------
boneSpine3.position.controller = Position_Constraint()
boneSpine3.position.controller.appendtarget pathConstNode2 50

boneSpine3.rotation.controller = rotation_script()
-- boneSpine3.rotation.controller.IScriptCtrl.AddObject "Roll" ctrlChest.ChestRoll.controller
boneSpine3.rotation.controller.IScriptCtrl.AddNode "Node" pathConstNode2
boneSpine3.rotation.controller.IScriptCtrl.AddNode "Parent" boneSpine2
boneSpine3.rotation.controller.IScriptCtrl.AddNode "Target" locSpine4
boneSpine3.rotation.controller.IScriptCtrl.SetExpression ("theTargetVector=(Target.transform.position * Inverse Parent.transform) - (Node.transform.position * Inverse Parent.transform)\n" + \
														"theAxis=Normalize (cross theTargetVector [1,0,0])\n" + \
														"theAngle=acos (dot (Normalize theTargetVector) [1,0,0])\n" + \
														"Quat theAngle theAxis")--"(eulerToQuat (eulerAngles (Roll.value/3) 0 0)) * (Quat theAngle theAxis)")
------------------------------
-- boneSpine4.position.controller = Position_Constraint()
-- boneSpine4.position.controller.appendtarget locSpine3 50

-- boneSpine4.rotation.controller = rotation_script()
-- boneSpine4.rotation.controller.IScriptCtrl.AddObject "Roll" ctrlChest.ChestRoll.controller
-- boneSpine4.rotation.controller.IScriptCtrl.AddNode "Node" locSpine3
-- boneSpine4.rotation.controller.IScriptCtrl.AddNode "Parent" boneSpine3
-- boneSpine4.rotation.controller.IScriptCtrl.AddNode "Target" locSpine4
-- boneSpine4.rotation.controller.IScriptCtrl.SetExpression ("theTargetVector=(Target.transform.position * Inverse Parent.transform) - (Node.transform.position * Inverse Parent.transform)\n" + \
-- 														"theAxis=Normalize (cross theTargetVector [1,0,0])\n" + \
-- 														"theAngle=acos (dot (Normalize theTargetVector) [1,0,0])\n" + \
-- 														"(eulerToQuat (eulerAngles (Roll.value/3) 0 0)) * (Quat theAngle theAxis)")
-------------------------


----------------------
chestRollScript = float_script()
chestRollScript.IScriptCtrl.AddNode "Node0" boneSpine3
chestRollScript.IScriptCtrl.AddNode "Node1" ctrlChest
scriptStr = "locQuat = (Node1.transform * (inverse Node0.transform)).rotation\n" + \
			"RollEuler = quatToEuler (Quat locQuat.x 0 0 locQuat.w)\n" + \
			"return RollEuler.x"
chestRollScript.IScriptCtrl.SetExpression scriptStr
ctrlChest.ChestRoll.controller = chestRollScript

------------------------------
pySpine1 = point name:"pySpine1" size:1.5 cross:off Box:on wirecolor:(color 0 128 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
pySpine2 = point name:"pySpine1" size:1.5 cross:off Box:on wirecolor:(color 0 128 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
pySpine3 = point name:"pySpine1" size:1.5 cross:off Box:on wirecolor:(color 0 128 0) axistripod:off centermarker:off drawontop:off constantscreensize:off

pySpine1.transform = boneSpine1.transform
pySpine2.transform = boneSpine2.transform
pySpine3.transform = boneSpine3.transform
pySpine1.parent = boneSpine1
pySpine2.parent = boneSpine2
pySpine3.parent = boneSpine3
hideLayer.addNode pySpine1
hideLayer.addNode pySpine2
hideLayer.addNode pySpine3

pySpine1.rotation.X_Rotation.controller = float_script()
pySpine1.rotation.X_Rotation.controller.IScriptCtrl.AddObject "Roll" ctrlChest.ChestRoll.controller
pySpine1.rotation.X_Rotation.controller.IScriptCtrl.SetExpression "Roll.value*0.005817764"

pySpine2.rotation.X_Rotation.controller = float_script()
pySpine2.rotation.X_Rotation.controller.IScriptCtrl.AddObject "Roll" ctrlChest.ChestRoll.controller
pySpine2.rotation.X_Rotation.controller.IScriptCtrl.SetExpression "Roll.value*0.011635528"

pySpine3.rotation.X_Rotation.controller = float_script()
pySpine3.rotation.X_Rotation.controller.IScriptCtrl.AddObject "Roll" ctrlChest.ChestRoll.controller
pySpine3.rotation.X_Rotation.controller.IScriptCtrl.SetExpression "Roll.value*0.0174532925"

-- pySpine1.scale.controller = scale_script()
-- pySpine1.scale.controller.IScriptCtrl.AddNode "target" boneSpine1
-- scriptStr = "target.stretchTM.scale"
-- pySpine1.scale.controller.IScriptCtrl.SetExpression scriptStr

-- pySpine2.scale.controller = scale_script()
-- pySpine2.scale.controller.IScriptCtrl.AddNode "target" boneSpine2
-- scriptStr = "target.stretchTM.scale"
-- pySpine2.scale.controller.IScriptCtrl.SetExpression scriptStr

-- pySpine3.scale.controller = scale_script()
-- pySpine3.scale.controller.IScriptCtrl.AddNode "target" boneSpine3
-- scriptStr = "target.stretchTM.scale"
-- pySpine3.scale.controller.IScriptCtrl.SetExpression scriptStr
-----------------------------------------------
boneSpineE.position.controller = Position_Constraint()
boneSpineE.position.controller.appendtarget locSpine4 50

boneSpineE.rotation.controller = Orientation_Constraint()
boneSpineE.rotation.controller.appendtarget pySpine3 50
---------------------------------------------------
pyBodyCenter = point name:"pyBodyCenter" size:1 cross:on Box:off wirecolor:(color 128 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
hideLayer.addNode pyBodyCenter
pyBodyCenter.parent = CtrlRoot
pyBodyCenter.pos.controller = Position_Constraint()
pyBodyCenter.pos.controller.appendtarget boneSpine1 50
pyBodyCenter.pos.controller.appendtarget boneSpineE 50

rtRootCtrl = point name:"rtRootCtrl" size:1 cross:on Box:off wirecolor:(color 128 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
hideLayer.addNode rtRootCtrl
rtRootCtrl.parent = CtrlRoot
rtRootCtrl.pos.controller = position_script()
rtRootCtrl.pos.controller.IScriptCtrl.AddNode "target" pyBodyCenter
rtRootCtrl.pos.controller.IScriptCtrl.AddNode "parent" CtrlRoot
rtRootCtrl.pos.controller.IScriptCtrl.AddTarget "vX" CtrlRoot.bRootSd.controller
rtRootCtrl.pos.controller.IScriptCtrl.AddTarget "vY" CtrlRoot.bRootFw.controller
offsetPos = pyBodyCenter.transform.pos
offsetPos.z = 0
scriptStr = "val_X = if vX then 1.0 else 0.0\n" + \
			"val_Y = if vY then 1.0 else 0.0\n" + \
			"if (not vX) and (not vY) then [0,0,0]\n" + \
			"else (\n" + \
			"	wPos = [target.transform.pos.x * val_X, target.transform.pos.y * val_Y, 0]\n" + \
			"	wPos * (inverse parent.transform)\n)"
rtRootCtrl.pos.controller.IScriptCtrl.SetExpression scriptStr

rtRootCtrl.rotation.controller = rotation_script()
rtRootCtrl.rotation.controller.IScriptCtrl.AddNode "parent" CtrlRoot
rtRootCtrl.rotation.controller.IScriptCtrl.AddTarget "YR" CtrlRoot.bRootYR.controller
scriptStr = "if YR then (\n" + \
			"	(quat 0 0 0 1)\n" + \
			") else (\n" + \
			"	((matrix3 1) * (inverse $ControlRoot.transform)).rotation\n)"
rtRootCtrl.rotation.controller.IScriptCtrl.SetExpression scriptStr


r=16
ctrlRootMPointList = #(
	[(cos    0) * r ,(sin    0) * r , 0],
	[(cos   15) * r ,(sin   15) * r , 0],
	[(cos   30) * r ,(sin   30) * r , 0],
	[(cos   45) * r ,(sin   45) * r , 0],
	[(cos   60) * r ,(sin   60) * r , 0],
	[(cos   75) * r ,(sin   75) * r , 0],
	[(cos   90) * r ,(sin   90) * r , 0],
	[(cos  105) * r ,(sin  105) * r , 0],
	[(cos  120) * r ,(sin  120) * r , 0],
	[(cos  135) * r ,(sin  135) * r , 0],
	[(cos  150) * r ,(sin  150) * r , 0],
	[(cos  165) * r ,(sin  165) * r , 0],
	[(cos  180) * r ,(sin  180) * r , 0],
	[(cos  195) * r ,(sin  195) * r , 0],
	[(cos  210) * r ,(sin  210) * r , 0],
	[(cos  225) * r ,(sin  225) * r , 0],
	[(cos  240) * r ,(sin  240) * r , 0],
	[(cos  255) * r ,(sin  255) * r , 0],
	[(cos  255) * r ,((sin  255) - 0.125) * r , 0],
	[(cos  240) * r ,((sin  255) - 0.125) * r , 0],
	[0, -1.5 * r, 0],
	[(cos  300) * r ,((sin  285) - 0.125) * r , 0],
	[(cos  285) * r ,((sin  285) - 0.125) * r , 0],
	[(cos  285) * r ,(sin  285) * r , 0],
	[(cos  300) * r ,(sin  300) * r , 0],
	[(cos  315) * r ,(sin  315) * r , 0],
	[(cos  330) * r ,(sin  330) * r , 0],
	[(cos  345) * r ,(sin  345) * r , 0],
	[(cos    0) * r ,(sin    0) * r , 0]
)
CtrlRootMotion = createLineCtrl ctrlRootMPointList false
CtrlRootMotion.wireColor = (color 255 114 0)
CtrlRootMotion.name = "Ctrl_RootMotion"
CtrlRootMotion.parent = rtRootCtrl
layer.addNode CtrlRootMotion
CtrlRootMotion.scale.controller = SlaveScale()