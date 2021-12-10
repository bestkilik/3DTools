Chest0Node = pySpine3--boneSpine3
Chest0FixNode = point name:"Chest0FixNode" pos:Chest0Node.transform.pos size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
Chest0FixNode.parent = Chest0Node
Chest0FixNode.transform = Chest0Node.transform
Chest0FixNode.scale.controller = scale_script()
Chest0FixNode.scale.controller.IScriptCtrl.AddNode "ref" Chest0Node
scriptStr = "ref.stretchTM.scale"
Chest0FixNode.scale.controller.IScriptCtrl.SetExpression scriptStr
hideLayer.addNode Chest0FixNode

rf_BustLine = getNodeByName "rf_BustLine"
posLineCtrl2_R = rf_BustLine.modifiers[#splineIKcontrol].helper_list[2].transform.pos
posLineCtrl2_L = [-posLineCtrl2_R.x, posLineCtrl2_R.y, posLineCtrl2_R.z]

maxOps.cloneNodes rf_BustLine cloneType:#copy newNodes:&nnl
BustPath_R = nnl[1]
convertto BustPath_R NURBSCurveshape
BustPath_R.name = "BustPath_R"
hideLayer.addNode BustPath_R

maxOps.cloneNodes BustPath_R cloneType:#copy newNodes:&nnl
BustPath_L = nnl[1]
BustPath_L.name = "BustPath_L"
BustPath_L.scale.controller.value = [-1,1,1]
ResetXform BustPath_L
maxOps.CollapseNode BustPath_L off

BustPath_R.parent = CtrlRoot
BustPath_L.parent = CtrlRoot

BustPath_R_Modifier = Spline_IK_Control()
addModifier BustPath_R BustPath_R_Modifier
BustPath_R_Modifier.helper_size = 2
BustPath_R_Modifier.createHelper 3

BustPathHelpList_R = BustPath_R_Modifier.helper_list
for i = 1 to (BustPathHelpList_R.count) do
(
	BustPathHelpList_R[i].wireColor = (color 40 0 0)
	BustPathHelpList_R[i].name = "py_BustLineCtrl_" + (i as string)
	BustPathHelpList_R[i].parent = CtrlRoot
	hideLayer.addNode BustPathHelpList_R[i]
)

lpBustPathCtrlA_R = point name:"lpBustPathCtrlA_R" pos:posLineCtrl2_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
lpBustPathCtrlB_R = point name:"lpBustPathCtrlB_R" pos:posLineCtrl2_R size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
lpBustPathCtrlA_R.parent = Chest0FixNode
lpBustPathCtrlB_R.parent = ChestFixNode
hideLayer.addNode lpBustPathCtrlA_R
hideLayer.addNode lpBustPathCtrlB_R

BustPathHelpList_R[1].parent = ChestFixNode
BustPathHelpList_R[2].parent = ChestFixNode
BustPathHelpList_R[3].parent = ctrlShoulder_R

BustPathHelpList_R[2].pos.controller = Position_Constraint()
BustPathHelpList_R[2].pos.controller.appendtarget lpBustPathCtrlA_R 50
BustPathHelpList_R[2].pos.controller.appendtarget lpBustPathCtrlB_R 50

-----------
BustPath_L_Modifier = Spline_IK_Control()
addModifier BustPath_L BustPath_L_Modifier
BustPath_L_Modifier.helper_size = 2
BustPath_L_Modifier.createHelper 3

BustPathHelpList_L = BustPath_L_Modifier.helper_list
for i = 1 to (BustPathHelpList_L.count) do
(
	BustPathHelpList_L[i].wireColor = (color 40 0 0)
	BustPathHelpList_L[i].name = "py_BustLineCtrl_" + (i as string)
	BustPathHelpList_L[i].parent = CtrlRoot
	hideLayer.addNode BustPathHelpList_L[i]
)

lpBustPathCtrlA_L = point name:"lpBustPathCtrlA_L" pos:posLineCtrl2_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
lpBustPathCtrlB_L = point name:"lpBustPathCtrlB_L" pos:posLineCtrl2_L size:1 cross:on Box:off axistripod:off centermarker:off drawontop:off constantscreensize:off
lpBustPathCtrlA_L.parent = Chest0FixNode
lpBustPathCtrlB_L.parent = ChestFixNode
hideLayer.addNode lpBustPathCtrlA_L
hideLayer.addNode lpBustPathCtrlB_L

BustPathHelpList_L[1].parent = ChestFixNode
BustPathHelpList_L[2].parent = ChestFixNode
BustPathHelpList_L[3].parent = ctrlShoulder_L

BustPathHelpList_L[2].pos.controller = Position_Constraint()
BustPathHelpList_L[2].pos.controller.appendtarget lpBustPathCtrlA_L 50
BustPathHelpList_L[2].pos.controller.appendtarget lpBustPathCtrlB_L 50

-------------------------
bgTeresMajor1 = getNodeByName "bg_TeresMajor1"
bgTeresMajor2 = getNodeByName "bg_TeresMajor2"

posTeresMajor1_R = bgTeresMajor1.transform.pos
posTeresMajor2_R = bgTeresMajor2.transform.pos

posTeresMajor1_L = [-posTeresMajor1_R.x, posTeresMajor1_R.y, posTeresMajor1_R.z]
posTeresMajor2_L = [-posTeresMajor2_R.x, posTeresMajor2_R.y, posTeresMajor2_R.z]



----------------------
rtTeresMajor_R = point name:"rtTeresMajor_R" pos:pathConstNode2.transform.pos size:2 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
rtTeresMajor_R.transform = getAimMatrix 2 Chest0Node.transform.row1 1 ctrlHip.transform.row3 pathConstNode2.transform.pos
rtTeresMajor_R.parent = Chest0Node

lpTeresMajor1_R = point name:"lpTeresMajor1_R" pos:posTeresMajor1_R size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
lpTeresMajor2_R = point name:"lpTeresMajor2_R" pos:posTeresMajor2_R size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off

lpTeresMajor1_R.parent = ChestFixNode
lpTeresMajor2_R.parent = UpperArmTwistBoneList_R[1]

boneTeresMajor_R = BoneSys.createBone posTeresMajor1_R posTeresMajor2_R [0,1,0]
boneTeresMajor_R.name = "boneTeresMajor_R"
boneTeresMajor_R.parent = rtTeresMajor_R
boneTeresMajor_R.boneEnable = false
boneTeresMajor_R.width = 1
boneTeresMajor_R.height = 1
boneTeresMajor_R.Taper = 90
boneTeresMajor_R.sidefins = off
boneTeresMajor_R.sidefinssize = 2
boneTeresMajor_R.frontfin = off
boneTeresMajor_R.frontfinsize = 2
boneTeresMajor_R.backfin = off
boneTeresMajor_R.backfinsize = 2
boneTeresMajor_R.rotation.controller = rotation_script()
boneTeresMajor_R.rotation.controller.IScriptCtrl.AddObject "NodePos" boneTeresMajor_R.pos.controller
boneTeresMajor_R.rotation.controller.IScriptCtrl.AddNode "Parent" rtTeresMajor_R
boneTeresMajor_R.rotation.controller.IScriptCtrl.AddNode "Target" lpTeresMajor2_R
boneTeresMajor_R.rotation.controller.IScriptCtrl.SetExpression ("theTargetVector=(Target.transform.position * Inverse Parent.transform)-NodePos.value\n" + \
																"theAxis=Normalize (cross theTargetVector [1,0,0])\n" + \
																"theAngle=acos (dot (Normalize theTargetVector) [1,0,0])\n" + \
																"Quat theAngle theAxis")
boneTeresMajor_R.scale.controller = scale_script()
boneTeresMajor_R.scale.controller.IScriptCtrl.AddNode "Target" lpTeresMajor2_R
boneTeresMajor_R.scale.controller.IScriptCtrl.AddNode "Src" lpTeresMajor1_R
boneTeresMajor_R.scale.controller.IScriptCtrl.SetExpression ("dis = distance Src.transform.pos Target.transform.pos\n" + \
															"scaleX = dis / " + (boneTeresMajor_R.length as string) + "\n" + \
															"[scaleX, 1, 1]")

boneTeresMajor_R.pos.controller = Position_Constraint()
boneTeresMajor_R.pos.controller.appendtarget lpTeresMajor1_R 50


hideLayer.addNode rtTeresMajor_R
hideLayer.addNode lpTeresMajor1_R
hideLayer.addNode lpTeresMajor2_R
hideLayer.addNode boneTeresMajor_R
-----------
rtTeresMajor_L = point name:"rtTeresMajor_L" pos:pathConstNode2.transform.pos size:2 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
rtTeresMajor_L.transform = getAimMatrix 2 -Chest0Node.transform.row1 1 -ctrlHip.transform.row3 pathConstNode2.transform.pos
rtTeresMajor_L.parent = Chest0Node

lpTeresMajor1_L = point name:"lpTeresMajor1_L" pos:posTeresMajor1_L size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
lpTeresMajor2_L = point name:"lpTeresMajor2_L" pos:posTeresMajor2_L size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off

lpTeresMajor1_L.parent = ChestFixNode
lpTeresMajor2_L.parent = UpperArmTwistBoneList_L[1]

boneTeresMajor_L = BoneSys.createBone posTeresMajor1_L posTeresMajor2_L [0,1,0]
boneTeresMajor_L.name = "boneTeresMajor_L"
boneTeresMajor_L.parent = rtTeresMajor_L
boneTeresMajor_L.boneEnable = false
boneTeresMajor_L.width = 1
boneTeresMajor_L.height = 1
boneTeresMajor_L.Taper = 90
boneTeresMajor_L.sidefins = off
boneTeresMajor_L.sidefinssize = 2
boneTeresMajor_L.frontfin = off
boneTeresMajor_L.frontfinsize = 2
boneTeresMajor_L.backfin = off
boneTeresMajor_L.backfinsize = 2
boneTeresMajor_L.rotation.controller = rotation_script()
boneTeresMajor_L.rotation.controller.IScriptCtrl.AddObject "NodePos" boneTeresMajor_L.pos.controller
boneTeresMajor_L.rotation.controller.IScriptCtrl.AddNode "Parent" rtTeresMajor_L
boneTeresMajor_L.rotation.controller.IScriptCtrl.AddNode "Target" lpTeresMajor2_L
boneTeresMajor_L.rotation.controller.IScriptCtrl.SetExpression ("theTargetVector=(Target.transform.position * Inverse Parent.transform)-NodePos.value\n" + \
																"theAxis=Normalize (cross theTargetVector [1,0,0])\n" + \
																"theAngle=acos (dot (Normalize theTargetVector) [1,0,0])\n" + \
																"Quat theAngle theAxis")
boneTeresMajor_L.scale.controller = scale_script()
boneTeresMajor_L.scale.controller.IScriptCtrl.AddNode "Target" lpTeresMajor2_L
boneTeresMajor_L.scale.controller.IScriptCtrl.AddNode "Src" lpTeresMajor1_L
boneTeresMajor_L.scale.controller.IScriptCtrl.SetExpression ("dis = distance Src.transform.pos Target.transform.pos\n" + \
															"scaleX = dis / " + (boneTeresMajor_L.length as string) + "\n" + \
															"[scaleX, 1, 1]")

boneTeresMajor_L.pos.controller = Position_Constraint()
boneTeresMajor_L.pos.controller.appendtarget lpTeresMajor1_L 50

hideLayer.addNode rtTeresMajor_L
hideLayer.addNode lpTeresMajor1_L
hideLayer.addNode lpTeresMajor2_L
hideLayer.addNode boneTeresMajor_L
----------------------------
bgBust0 = getNodeByName "bg_Bust0"
bgBust1 = getNodeByName "bg_Bust1"
bgBustE = getNodeByName "bg_BustEff"
BustPathPercent = bgBust0.pos.controller.percent

posBust0_R = bgBust0.transform.pos
posBust1_R = bgBust1.transform.pos
posBustE_R = bgBustE.transform.pos

xVecBust0_R = bgBust0.transform.row1
xVecBust1_R = bgBust1.transform.row1

posBust0_L = [-posBust0_R.x,posBust0_R.y,posBust0_R.z]
posBust1_L = [-posBust1_R.x,posBust1_R.y,posBust1_R.z]
posBustE_L = [-posBustE_R.x,posBustE_R.y,posBustE_R.z]

xVecBust0_L = [-xVecBust0_R.x,xVecBust0_R.y,xVecBust0_R.z]
xVecBust1_L = [-xVecBust1_R.x,xVecBust1_R.y,xVecBust1_R.z]

------------------
BustRoot_R = point name:"BustRoot_R" size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
BustRoot_R.parent = Chest0Node
BustRoot_R.transform = getAimMatrix 1 xVecBust0_R 2 [0,0,1] posBust0_R
BustRoot_R.pos.controller = Path_Constraint percent:BustPathPercent follow:false path:BustPath_R loop:off
deleteKeys BustRoot_R #AllKeys
hideLayer.addNode BustRoot_R

boneBust0_R = BoneSys.createBone posBust0_R posBust1_R [0,1,0]
boneBust0_R.wireColor = (color 245 156 0)
boneBust0_R.name = "Ctrl_Bust0_R"
boneBust0_R.transform = getAimMatrix 1 xVecBust0_R 2 [0,0,1] posBust0_R
boneBust0_R.parent = BustRoot_R
boneBust0_R.pos.controller = SlavePos()
boneBust0_R.scale.controller = SlaveScale()
boneBust0_R.width = 5
boneBust0_R.height = 5
boneBust0_R.Taper = 90
boneBust0_R.sidefins = off
boneBust0_R.sidefinssize = 2
boneBust0_R.frontfin = off
boneBust0_R.frontfinsize = 2
boneBust0_R.backfin = off
boneBust0_R.backfinsize = 2
layer.addNode boneBust0_R

boneBust1_R = BoneSys.createBone posBust1_R posBustE_R [0,1,0]
boneBust1_R.wireColor = (color 253 30 0)
boneBust1_R.name = "Ctrl_Bust1_R"
boneBust1_R.transform = getAimMatrix 1 xVecBust1_R 3 boneBust0_R.transform.row3 posBust1_R
boneBust1_R.parent = boneBust0_R
locPos = boneBust1_R.pos.controller.value
boneBust1_R.pos.controller = position_script()
boneBust1_R.pos.controller.IScriptCtrl.SetExpression (locPos as string)
boneBust1_R.scale.controller = SlaveScale()
boneBust1_R.width = 2
boneBust1_R.height = 2
boneBust1_R.Taper = -95
boneBust1_R.sidefins = off
boneBust1_R.sidefinssize = 2
boneBust1_R.frontfin = off
boneBust1_R.frontfinsize = 2
boneBust1_R.backfin = off
boneBust1_R.backfinsize = 2
layer.addNode boneBust1_R

boneBustE_R = BoneSys.createBone posBustE_R posBustE_R [0,1,0]
boneBustE_R.parent = boneBust1_R
boneBustE_R.rotation.controller.value = (quat 0 0 0 1)
boneBustE_R.length = 1
boneBustE_R.width = 1
boneBustE_R.height = 1
boneBustE_R.Taper = 90
boneBustE_R.sidefins = off
boneBustE_R.sidefinssize = 2
boneBustE_R.frontfin = off
boneBustE_R.frontfinsize = 2
boneBustE_R.backfin = off
boneBustE_R.backfinsize = 2
hideLayer.addNode boneBustE_R

------------------
BustRoot_L = point name:"BustRoot_L" size:1 cross:off Box:on axistripod:off centermarker:off drawontop:off constantscreensize:off
BustRoot_L.parent = Chest0Node
BustRoot_L.transform = getAimMatrix 1 xVecBust0_L 2 [0,0,1] posBust0_L
BustRoot_L.pos.controller = Path_Constraint percent:BustPathPercent follow:false path:BustPath_L loop:off
deleteKeys BustRoot_L #AllKeys
hideLayer.addNode BustRoot_L

boneBust0_L = BoneSys.createBone posBust0_L posBust1_L [0,1,0]
boneBust0_L.wireColor = (color 245 156 0)
boneBust0_L.name = "Ctrl_Bust0_L"
boneBust0_L.transform = getAimMatrix 1 xVecBust0_L 2 [0,0,1] posBust0_L
boneBust0_L.parent = BustRoot_L
boneBust0_L.pos.controller = SlavePos()
boneBust0_L.scale.controller = SlaveScale()
boneBust0_L.width = 5
boneBust0_L.height = 5
boneBust0_L.Taper = 90
boneBust0_L.sidefins = off
boneBust0_L.sidefinssize = 2
boneBust0_L.frontfin = off
boneBust0_L.frontfinsize = 2
boneBust0_L.backfin = off
boneBust0_L.backfinsize = 2
layer.addNode boneBust0_L

boneBust1_L = BoneSys.createBone posBust1_L posBustE_L [0,1,0]
boneBust1_L.wireColor = (color 253 30 0)
boneBust1_L.name = "Ctrl_Bust1_L"
boneBust1_L.transform = getAimMatrix 1 xVecBust1_L 3 boneBust0_L.transform.row3 posBust1_L
boneBust1_L.parent = boneBust0_L
locPos = boneBust1_L.pos.controller.value
boneBust1_L.pos.controller = position_script()
boneBust1_L.pos.controller.IScriptCtrl.SetExpression (locPos as string)
boneBust1_L.scale.controller = SlaveScale()
boneBust1_L.width = 2
boneBust1_L.height = 2
boneBust1_L.Taper = -95
boneBust1_L.sidefins = off
boneBust1_L.sidefinssize = 2
boneBust1_L.frontfin = off
boneBust1_L.frontfinsize = 2
boneBust1_L.backfin = off
boneBust1_L.backfinsize = 2
layer.addNode boneBust1_L

boneBustE_L = BoneSys.createBone posBustE_L posBustE_L [0,1,0]
boneBustE_L.parent = boneBust1_L
boneBustE_L.rotation.controller.value = (quat 0 0 0 1)
boneBustE_L.length = 1
boneBustE_L.width = 1
boneBustE_L.height = 1
boneBustE_L.Taper = 90
boneBustE_L.sidefins = off
boneBustE_L.sidefinssize = 2
boneBustE_L.frontfin = off
boneBustE_L.frontfinsize = 2
boneBustE_L.backfin = off
boneBustE_L.backfinsize = 2
hideLayer.addNode boneBustE_L
------------------------------

layer.nodes &CtrlList

for obj in CtrlList do (
	obj.setSkinPose()
)

clearSelection()
