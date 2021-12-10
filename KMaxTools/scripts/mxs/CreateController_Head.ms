NeckRoot = pySpine3--boneSpineE


bgNeckNode = getNodeByName "bg_Neck"
bgHeadNode = getNodeByName "bg_Head"
bgHeadTopNode = getNodeByName "bg_HeadEff"

posNeckNode = bgNeckNode.transform.pos
posHeadNode = bgHeadNode.transform.pos
posHeadTopNode = bgHeadTopNode.transform.pos

-- ChestXAxis = normalize ChestXAxis
NeckXAxis = posHeadNode - posNeckNode
HeadXAxis = posHeadTopNode - posHeadNode

neckLength = distance posNeckNode posHeadNode
helfNeckLen = neckLength*0.2
r = 9
CtrlNeckPointList = #(
	[helfNeckLen, r*(sin 0), r*(cos 0)],
	[helfNeckLen, r*(sin 15), r*(cos 15)],
	[helfNeckLen, r*(sin 30), r*(cos 30)],
	[helfNeckLen, r*(sin 45), r*(cos 45)],
	[helfNeckLen, r*(sin 60), r*(cos 60)],
	[helfNeckLen, r*(sin 75), r*(cos 75)],
	[helfNeckLen, r*(sin 90), r*(cos 90)],
	[helfNeckLen, r*(sin 105), r*(cos 105)],
	[helfNeckLen, r*(sin 120), r*(cos 120)],
	[helfNeckLen, r*(sin 135), r*(cos 135)],
	[helfNeckLen, r*(sin 150), r*(cos 150)],
	[helfNeckLen, r*(sin 165), r*(cos 165)],
	[helfNeckLen, r*(sin 180), r*(cos 180)],
	[helfNeckLen, r*(sin 195), r*(cos 195)],
	[helfNeckLen, r*(sin 210), r*(cos 210)],
	[helfNeckLen, r*(sin 225), r*(cos 225)],
	[helfNeckLen, r*(sin 240), r*(cos 240)],
	[helfNeckLen, r*(sin 255), r*(cos 255)],
	[helfNeckLen, r*1.5*(sin 270), r*1.5*(cos 270)],
	[helfNeckLen, r*(sin 285), r*(cos 285)],
	[helfNeckLen, r*(sin 300), r*(cos 300)],
	[helfNeckLen, r*(sin 315), r*(cos 315)],
	[helfNeckLen, r*(sin 330), r*(cos 330)],
	[helfNeckLen, r*(sin 345), r*(cos 345)]
)

l = bgHeadNode.length
w = bgHeadNode.width * 0.5
h = bgHeadNode.height * 0.5
b = bgHeadNode.backfinsize
f = bgHeadNode.frontfinsize
s = bgHeadNode.sidefinssize
CtrlHeadPointList = #(
	[      l, -(h+b),  (w+s)],
	[-0.25*l, -(h+b),  (w+s)],
	[-0.25*l, -(h+b), -(w+s)],
	[      l, -(h+b), -(w+s)],
	[      l,  (h+f), -(w+s)],
	[      0,  (h+f), -(w+s)],
	[      0,      0, -(w+s)],
	[-0.25*l, -(h+b), -(w+s)],
	[-0.25*l, -(h+b),  (w+s)],
	[      0,      0,  (w+s)],
	[      0,  (h+f),  (w+s)],
	[      0,  (h+f), -(w+s)],
	[      l,  (h+f), -(w+s)],
	[      l,  (h+f),  (w+s)],
	[      0,  (h+f),  (w+s)],
	[      l,  (h+f),  (w+s)],
	[      l, -(h+b),  (w+s)],
	[      l, -(h+b), -(w+s)]
)

NeckKnot1Loc = posNeckNode + (normalize ChestXAxis)*(neckLength*0.2)
NeckKnot2Loc = posHeadNode + (normalize HeadXAxis)*(neckLength*-0.5)

nset = NURBSSet ()
pointList = #(posNeckNode, NeckKnot1Loc, NeckKnot2Loc, posHeadNode)


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
NeckLine = NURBSNode nset name:"NeckLine" pos:[0,0,0]
NeckLine.parent = CtrlRoot
hideLayer.addNode NeckLine

neckSpIKCtrlModify = Spline_IK_Control()
addModifier NeckLine neckSpIKCtrlModify

neckSpIKCtrlModify.helper_size = 4
neckSpIKCtrlModify.createHelper 4
neckIKPointList = neckSpIKCtrlModify.helper_list

for i = 1 to (neckIKPointList.count) do
(
	neckIKPointList[i].wireColor = (color 255 109 51)
	neckIKPointList[i].name = "neckLineCtrl_" + (i as string)
	hideLayer.addNode neckIKPointList[i]
)

neckSplineSeg1 = point name:"neckSplineSeg1" size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
neckSplineSeg2 = point name:"neckSplineSeg2" size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off

neckSplineSeg1.pos.controller = Path_Constraint percent:50 follow:false path:NeckLine loop:off
neckSplineSeg2.pos.controller = Path_Constraint percent:100 follow:false path:NeckLine loop:off
deleteKeys neckSplineSeg1 #AllKeys
deleteKeys neckSplineSeg2 #AllKeys
hideLayer.addNode neckSplineSeg1
hideLayer.addNode neckSplineSeg2

listRefNeckBone = #()
refNeck1 = BoneSys.createBone posNeckNode neckSplineSeg1.transform.pos [0,1,0]
refNeck2 = BoneSys.createBone neckSplineSeg1.transform.pos neckSplineSeg2.transform.pos [0,1,0]
refNeckE = BoneSys.createBone neckSplineSeg2.transform.pos (neckSplineSeg2.transform.pos+[0,0,1]) [0,1,0]
append listRefNeckBone refNeck1
append listRefNeckBone refNeck2
hideLayer.addNode refNeck1
hideLayer.addNode refNeck2
refNeck1.parent = boneSpineE
refNeck2.parent = refNeck1
refNeckE.parent = refNeck2
refNeckE.length = 1
refNeckE.width = 1
refNeckE.height = 1
refNeckE.rotation = (quat 0 0 0 1)
for b in listRefNeckBone do (
	b.width = 3
	b.height = 3
-- 	b.boneScaleType=#scale
)

refNeck1.rotation.controller = rotation_script()
refNeck1.rotation.controller.IScriptCtrl.AddObject "NodePos" refNeck1.pos.controller
refNeck1.rotation.controller.IScriptCtrl.AddNode "Parent" boneSpineE
refNeck1.rotation.controller.IScriptCtrl.AddNode "Target" neckSplineSeg1
refNeck1.rotation.controller.IScriptCtrl.SetExpression ("theTargetVector=(Target.transform.position * Inverse Parent.transform)-NodePos.value\n" + \
														"theAxis=Normalize (cross theTargetVector [1,0,0])\n" + \
														"theAngle=acos (dot (Normalize theTargetVector) [1,0,0])\n" + \
														"Quat theAngle theAxis")
----------------------------------------------------------
refNeck2.position.controller = Position_Constraint()
refNeck2.position.controller.appendtarget neckSplineSeg1 50

refNeck2.rotation.controller = rotation_script()
refNeck2.rotation.controller.IScriptCtrl.AddNode "Node" neckSplineSeg1
refNeck2.rotation.controller.IScriptCtrl.AddNode "Parent" refNeck1
refNeck2.rotation.controller.IScriptCtrl.AddNode "Target" neckSplineSeg2
refNeck2.rotation.controller.IScriptCtrl.SetExpression ("theTargetVector=(Target.transform.position * Inverse Parent.transform) - (Node.transform.position * Inverse Parent.transform)\n" + \
														"theAxis=Normalize (cross theTargetVector [1,0,0])\n" + \
														"theAngle=acos (dot (Normalize theTargetVector) [1,0,0])\n" + \
														"Quat theAngle theAxis")

refNeckE.position.controller = Position_Constraint()
refNeckE.position.controller.appendtarget neckSplineSeg2 50

--------------------------------
-- ctrlNeck = createLineCtrl CtrlNeckPointList true
-- ctrlNeck.name = "Ctrl_Neck"
-- ctrlNeck.wireColor = (color 10 144 177)
-- ctrlNeck.parent = boneSpineE
-- ctrlNeck.transform = getAimMatrix 1 bgNeckNode.transform.row1 3 [-1,0,0] posNeckNode
-- ctrlNeck.pos.controller = SlavePos()
-- ctrlNeck.scale.controller = SlaveScale()
-- layer.addNode ctrlNeck

ctrlHead = createLineCtrl CtrlHeadPointList false
ctrlHead.name = "Ctrl_Head"
ctrlHead.wireColor = (color 166 202 240)
ctrlHead.parent = rotXUpFix
ctrlHead.transform = getAimMatrix 1 HeadXAxis 3 [-1,0,0] posHeadNode
layer.addNode ctrlHead

lpHead = point name:"lpHead" pos:posHeadNode size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
hideLayer.addNode lpHead
lpHead.transform = (matrix3 [0,0,1] [0,1,0] [-1,0,0] posHeadNode)

lpHead.parent = boneSpineE

ctrlHeadRoot = point name:"ctrlHeadRoot" pos:posHeadNode size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
hideLayer.addNode ctrlHeadRoot
ctrlHeadRoot.transform = (matrix3 [0,0,1] [0,1,0] [-1,0,0] posHeadNode)
ctrlHeadRoot.parent = rotXUpFix
ctrlHeadRoot.pos.controller = Position_Constraint()
ctrlHeadRoot.pos.controller.appendtarget lpHead 50
ctrlHeadRoot.pos.controller.weight[1].controller = Float_Expression()
ctrlHeadRoot.pos.controller.weight[1].controller.SetExpression "50"
ctrlHead.parent = ctrlHeadRoot


-- ctrlHead.pos.controller = Position_Constraint()
-- ctrlHead.pos.controller.appendtarget lpHead 50
-- ctrlHead.pos.controller.weight[1].controller = Float_Expression()
-- ctrlHead.pos.controller.weight[1].controller.SetExpression "50"
ctrlHead.scale.controller = SlaveScale()

neckIKPointList[1].parent = boneSpineE
neckIKPointList[2].parent = boneSpineE
neckIKPointList[3].parent = ctrlHead
neckIKPointList[4].parent = ctrlHead

locNeck1 = point name:"locNeck1" size:3.5 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
locNeck2 = point name:"locNeck2" size:3.5 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
locNeck1.parent = refNeck1
locNeck2.parent = refNeck2
locNeck1.transform = refNeck1.transform
locNeck2.transform = refNeck2.transform
hideLayer.addNode locNeck1
hideLayer.addNode locNeck2