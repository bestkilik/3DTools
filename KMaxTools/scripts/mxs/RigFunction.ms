-- fn XLookAtRoll oObj oTarget =
-- (
-- 	oObj.rotation.controller = Rotation_Script()
-- 	oObj.rotation.controller.IScriptCtrl.AddNode "Node" oObj
-- 	oObj.rotation.controller.IScriptCtrl.AddNode "Target" oTarget
-- 	oObj.rotation.controller.IScriptCtrl.SetExpression ("parentMtx = Matrix3 1\n" + \
-- 														"if Node.parent != undefined then (parentMtx = Node.parent.transform)\n" + \
-- 														"invPMtx = Inverse parentMtx\n" + \
-- 														"theTargetVector=Target.transform.position-Node.transform.pos\n" + \
-- 														"theAxis=Normalize (cross theTargetVector Node.parent.transform[0])\n" + \
-- 														"theAngle=acos (dot (Normalize theTargetVector) Node.parent.transform[0])\n" + \
-- 														"Quat theAngle (theAxis*invPMtx)")
-- )
fn XLookAtRoll oObj oParent oTarget =
(
	oObj.rotation.controller = Rotation_Script()
	oObj.rotation.controller.IScriptCtrl.AddObject "NodePos" oObj.pos.controller
	oObj.rotation.controller.IScriptCtrl.AddNode "Parent" oParent
	oObj.rotation.controller.IScriptCtrl.AddNode "Target" oTarget
	oObj.rotation.controller.IScriptCtrl.SetExpression ("theTargetVector=(Target.transform.position * Inverse Parent.transform)-NodePos.value\n" + \
																		"theAxis=Normalize (cross theTargetVector [1,0,0])\n" + \
																		"theAngle=acos (dot (Normalize theTargetVector) [1,0,0])\n" + \
																		"Quat theAngle theAxis")
)

fn XRotAlign oObj oTarget =
(
	oObj.rotation.controller = Rotation_Script()
	oObj.rotation.controller.IScriptCtrl.AddNode "Node" oObj
	oObj.rotation.controller.IScriptCtrl.AddNode "Target" oTarget
	oObj.rotation.controller.IScriptCtrl.SetExpression ("parentMtx = Matrix3 1\n" + \
														"if Node.parent != undefined then (parentMtx = Node.parent.transform)\n" + \
														"theRot=QuatToEuler (Target.transform * Inverse parentMtx).rotation order:7\n" + \
														"theRot.x=-theRot.z\n" + \
														"EulerToQuat theRot order:7")
)

fn XRotRatioAlign oObj oTarget cRoll vRatio =
(
	oObj.rotation.controller = Rotation_Script()
	oObj.rotation.controller.IScriptCtrl.AddTarget "Roll" cRoll.baseObject.XSpline_Ctrl["endRoll"]
	oObj.rotation.controller.IScriptCtrl.AddNode "Node" oObj
	oObj.rotation.controller.IScriptCtrl.AddNode "Target" oTarget
	oObj.rotation.controller.IScriptCtrl.SetExpression ("parentMtx = Matrix3 1\n" + \
														"if Node.parent != undefined then (parentMtx = Node.parent.transform)\n" + \
														"theRot=QuatToEuler (Target.transform * Inverse parentMtx).rotation order:7\n" + \
														"theRot.x=-theRot.z\n" + \
														"rollRot = EulerToQuat (eulerAngles (Roll*"+(vRatio as string)+") 0 0)\n" + \
														"outRot = rollRot*(EulerToQuat theRot order:7)")
)

fn GenXSplineIK lineObj seg ctrlSize bWidth bHeight bTaper = (
	xsikRoot = point name:(lineObj.name + "_spikRoot") wirecolor:(color 10 255 10) centermarker:off axistripod:off cross:on box:off size:(ctrlSize*0.1) constantscreensize:off drawontop:off

	custAttributes.add lineObj XSplineIKDataDef
	lineObj.pathLength.controller = Bezier_Float()
	lineObj.stretchValue.controller = Bezier_Float()
	lineObj.pathLength = curvelength lineObj
	lineObj.stretchValue = 0
	xsIKbaseArray = #()
	for i = 1 to (seg + 1) do (
		thisNode = point name:(uniquename (lineObj.name + "_seg"+(i as string))) wirecolor:(color 10 10 10) centermarker:off axistripod:off cross:off box:on size:(ctrlSize*0.1) constantscreensize:off drawontop:off
		thisNode.pos.controller = Path_Constraint percent:0 follow:true path:lineObj loop:off
		deleteKeys thisNode #AllKeys
		thisNode.pos.controller.percent.controller = float_script()
		thisNode.pos.controller.percent.controller.IScriptCtrl.AddNode "TargetPath" lineObj
		thisNode.pos.controller.percent.controller.IScriptCtrl.AddTarget "DefLength" lineObj.pathLength.controller
		thisNode.pos.controller.percent.controller.IScriptCtrl.AddTarget "vStretch" lineObj.stretchValue.controller
		thisNode.pos.controller.percent.controller.IScriptCtrl.SetExpression (
			"cLength = ( curvelength TargetPath )\n" + \
			"vlinePos = ( DefLength /" + (seg as string) + " * " + ((i - 1) as string) + " ) / cLength\n" + \
			"sLinePos = " + (((1.0 / seg) * (i - 1)) as string) + "\n" + \
			"return (vStretch * ( sLinePos - vlinePos ) + vlinePos)"
		)
		append xsIKbaseArray thisNode
	)
	xsikRoot.pos = xsIKbaseArray[1].transform.pos
	for o in xsIKbaseArray do (
		o.parent = xsikRoot
	)


	endNode = point name:(lineObj.name + "_endNode") wirecolor:(color 10 10 10) centermarker:off axistripod:off cross:on box:off size:1 constantscreensize:off drawontop:off
	endNode.pos.controller = Path_Constraint percent:100 follow:true path:lineObj loop:off
	deleteKeys endNode #AllKeys
	endNode.parent = xsikRoot

	xsIKPosList = #()
	for i = 2 to xsIKbaseArray.count do (
		loc = point name:(uniquename (lineObj.name + "_Loc"+(i as string))) size:(ctrlSize*0.25) cross:off Box:on wirecolor:(color 128 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
		loc.transform = xsIKbaseArray[i].transform
		loc.parent = xsIKbaseArray[i]

		loc.pos.controller = position_script()
		loc.pos.controller.IScriptCtrl.AddNode "parentNode" xsIKbaseArray[i]
		loc.pos.controller.IScriptCtrl.AddNode "tanNode" endNode
		loc.pos.controller.IScriptCtrl.AddNode "curve" lineObj
		scriptStr = "Ratio = parentNode.pos.controller.percent / 100.0\n" + \
					"if Ratio <= 1.0 then return [0,0,0]\n" + \
					"else (\n" + \
					"  oriLen = (curvelength curve)\n" + \
					"  targetLen = (Ratio-1)*oriLen\n" + \
					"  wPos = tanNode.transform.row1 * targetLen + parentNode.transform.pos\n" + \
					"  return wPos * (inverse parentNode.transform)\n)"
		loc.pos.controller.IScriptCtrl.SetExpression scriptStr
		append xsIKPosList loc
	)
	------------------------------------------------------------
	addModifier lineObj (Spline_IK_Control linkTypes:2 \
									helper_centermarker:off \
									helper_axistripod:off \
									helper_cross:off \
									Box:on \
									helper_size:ctrlSize \
									constantscreensize:off \
									drawontop:off)
	max modify mode
	pathKnotCount = lineObj.modifiers[1].getKnotCount()
	lineObj.modifiers[#Spline_IK_Control].createHelper pathKnotCount

	segJntList = #()
	for i = 1 to seg do (
		segJntNode = point name:(uniquename ("segJntNode_"+(i as string))) size:(ctrlSize*0.3) cross:off Box:on wirecolor:(color 0 128 255) axistripod:off centermarker:off drawontop:off constantscreensize:off
		append segJntList segJntNode
		posTarget = undefined
		aimTarget = xsIKPosList[i]
		if i == 1 then (
			posTarget = xsIKbaseArray[1]
		) else (
			posTarget = xsIKPosList[i-1]
			segJntNode.parent = segJntList[i-1]
		)
 		--print ("segJntNode: " + segJntNode.name/*  + "   aimTarget: " + aimTarget.name */)
		segJntNode.pos.controller = Position_Constraint ()
		segJntNode.pos.controller.appendtarget posTarget 50
		
		segJntNode.rotation.controller = LookAt_Constraint ()
		segJntNode.rotation.controller.appendtarget aimTarget 50
		segJntNode.rotation.controller.lookat_vector_length = 0
	)
	segJntEndNode = point name:(uniquename ("segJntNode_"+((seg + 1) as string))) size:(ctrlSize*0.3) cross:off Box:on wirecolor:(color 0 128 255) axistripod:off centermarker:off drawontop:off constantscreensize:off
	segJntEndNode.transform = segJntList[segJntList.count].transform
	segJntEndNode.parent = segJntList[segJntList.count]
	append segJntList segJntEndNode
	segJntEndNode.pos.controller = Position_Constraint ()
	segJntEndNode.pos.controller.appendtarget xsIKPosList[xsIKPosList.count] 50
	segJntList[1].parent = xsikRoot
	RollCtrl = lineObj.modifiers[#Spline_IK_Control].helper_list[1]
	xsikRoot.parent = RollCtrl
	------------------------------------------------------------
	custAttributes.add RollCtrl XSplineCtrlDef
	RollCtrl.endRoll.controller = Bezier_Float()

	spBoneList = #()
	for i = 1 to seg do (
		posA = segJntList[i].transform.pos
		posB = segJntList[i+1].transform.pos
		--posTarget = segJntList[i]
		--aimTarget = segJntList[i+1]

		segBone = BoneSys.createBone posA posB [0,1,0]
		segBone.width = 0.5
		segBone.height = 0.5
		segBone.Taper = 90
		segBone.sidefins = off
		segBone.sidefinssize = 2
		segBone.frontfin = off
		segBone.frontfinsize = 2
		segBone.backfin = off
		segBone.backfinsize = 2

		append spBoneList segBone

		segBone.pos.controller = Position_Constraint ()
		segBone.pos.controller.appendtarget segJntList[i] 50

		XRotAlign segBone segJntList[i]
	)
	spBoneList[1].width = bWidth
	spBoneList[1].height = bHeight
	posA = segJntList[segJntList.count].transform.pos
	posB = segJntList[segJntList.count].transform.pos + spBoneList[spBoneList.count].transform[1]*2
	segEndBone = BoneSys.createBone posA posB [0,1,0]
	segEndBone.width = bWidth*0.5
	segEndBone.height = bHeight*0.5
	segEndBone.Taper = bTaper
	append spBoneList segEndBone
	segEndBone.pos.controller = Position_Constraint ()
	segEndBone.pos.controller.appendtarget segJntList[segJntList.count] 50

	for i = 2 to spBoneList.count do (
		spBoneList[i].parent = spBoneList[i-1]
	)

	for i = 2 to seg do (
		posA = spBoneList[i].transform.pos
		posB = spBoneList[i+1].transform.pos

		rollBone = BoneSys.createBone posA posB [0,1,0]
		rollBone.width = bWidth
		rollBone.height = bHeight
		rollBone.Taper = bTaper
		rollBone.sidefins = off
		rollBone.sidefinssize = 2
		rollBone.frontfin = off
		rollBone.frontfinsize = 2
		rollBone.backfin = off
		rollBone.backfinsize = 2
		rollBone.boneEnable = false
		rollBone.parent = spBoneList[i]

		rollBone.rotation.controller = rotation_script()
		rollBone.rotation.controller.IScriptCtrl.AddTarget "Roll" RollCtrl.baseObject.XSpline_Ctrl["endRoll"]
		scriptStr = "EulerToQuat (eulerAngles (Roll*"+(((i-1.0)/(seg-1.0)) as string)+") 0 0)\n"
		rollBone.rotation.controller.IScriptCtrl.SetExpression scriptStr

		rollBone.scale.controller = scale_script()
		rollBone.scale.controller.IScriptCtrl.AddNode "Target" spBoneList[i]
		scriptStr = "Target.stretchTM.scale"
		rollBone.scale.controller.IScriptCtrl.SetExpression scriptStr
	)
)