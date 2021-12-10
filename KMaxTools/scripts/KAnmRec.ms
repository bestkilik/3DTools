try(
	DestroyDialog KAnmRec
) catch ()

W = 205
H = 210

MirrorInfoCA = attributes "MirrorInfo"
attribID:#(0x3cc1de32, 0x79c53a9b)
(
	parameters main rollout:BipedControl
	(
		SymmetryNode type:#string ui:btnSysmNode default:""
		FlipAxis type:#integer ui:rdoFlipAxis default:2
	)
	rollout BipedControl "Mirror Info"
	(
		button btnSysmNode "" align:#center
		radioButtons rdoFlipAxis "Flip Axis" align:#center labels:#( "X", "Y" , "Z" ) columns:3 

		on btnSysmNode pressed do (
			pickObj = pickObject message:"Pick Target"
			if pickObj != undefined then
			(
				SymmetryNode = pickObj.name
				btnSysmNode.text = pickObj.name
			)
		)

		on BipedControl open do (
			btnSysmNode.text = SymmetryNode
		)
	)

	
)

fn fixRotation obj = (
	obj.rotation.controller = tcb_rotation ()
	obj.rotation.controller = Euler_XYZ ()
)

fn GetMirrorMatrix Mtx3 flipAxis = (
	case flipAxis of (
		1:(
			return (matrix3 [ Mtx3[1].x,-Mtx3[1].y,-Mtx3[1].z] [-Mtx3[2].x, Mtx3[2].y, Mtx3[2].z] [-Mtx3[3].x, Mtx3[3].y, Mtx3[3].z] [-Mtx3[4].x, Mtx3[4].y, Mtx3[4].z])
		)
		2:(
			return (matrix3 [-Mtx3[1].x, Mtx3[1].y, Mtx3[1].z] [ Mtx3[2].x,-Mtx3[2].y,-Mtx3[2].z] [-Mtx3[3].x, Mtx3[3].y, Mtx3[3].z] [-Mtx3[4].x, Mtx3[4].y, Mtx3[4].z])
		)
		3:(
			return (matrix3 [-Mtx3[1].x, Mtx3[1].y, Mtx3[1].z] [-Mtx3[2].x, Mtx3[2].y, Mtx3[2].z] [ Mtx3[3].x,-Mtx3[3].y,-Mtx3[3].z] [-Mtx3[4].x, Mtx3[4].y, Mtx3[4].z])
		)
	)
	return undefined
)

rollout KAnmRec "Anm Rec."
(
	group "Pose" (
		button BTN_PoseEx "Export" across:2 align:#center width:80 height:24 toolTip:"Export Pose..."
		button BTN_PoseIm "Import"  align:#center width:80 height:56 toolTip:"Import Pose..."
		button BTN_MPoseEx "Mirror Export" offset:[-45,-29] align:#center width:80 height:24 toolTip:"Mirror Export Pose..."
	)
	
	group "Animation" (
		button BTN_AnmEx "Export" across:2 align:#center width:80 height:24 toolTip:"Export Anm..."
		button BTN_AnmIm "Import" width:80 height:56 toolTip:"Import Anm..."
		button BTN_MAnmEx "Mirror Export" offset:[-45,-29] align:#center width:80 height:24 toolTip:"Mirror Export Anm..."
	)

	button btnAddMirrorInfo "Add Mirror Info Attr." across:2 align:#left
	checkbox CB_scale "Scale" align:#right checked:false

	on btnAddMirrorInfo pressed do
	(
		for o in selection do
		(
			CustAttributes.add o MirrorInfoCA
		)
	)

	on BTN_PoseEx pressed do
	(
		if selection.count > 0 then
		(
			ExpFileName = getSaveFileName caption:"Save Pose..." types:"Pose file(*.pose)|*.pose|"
			if (ExpFileName != undefined) then
			(
				fs = createFile ExpFileName
				format "PoseData\n" to:fs
				format "%\n" selection.count to:fs
				--pickObj = point()
				for i = 1 to selection.count do
				(
					format "%\n" selection[i].name to:fs
				)
				for i = 1 to selection.count do
				(
					if selection[i].parent != undefined then (
						pTran = selection[i].parent.transform
					)else(
						pTran = matrix3 1
					)

					locTrans = selection[i].transform * (inverse pTran)

					vPos = locTrans.pos
					vRot = locTrans.rotation
					vScl = locTrans.scale
					format "%\t%\t%\n" vPos vRot vScl to:fs
				)
				--delete pickObj
				close fs
				messageBox "Success!!" title:"" beep:off
			)
		)
		else
		(
			messageBox "你必須選一個物件..." title:"警告!" beep:on
		)
	)--BTN_PoseEx END
		
	on BTN_MPoseEx pressed do
	(
		if selection.count > 0 then
		(
			ExpFileName = getSaveFileName caption:"Save Pose..." types:"Pose file(*.pose)|*.pose|"
			if (ExpFileName != undefined) then
			(
				fs = createFile ExpFileName
				format "PoseData\n" to:fs
				format "%\n" selection.count to:fs

				for i = 1 to selection.count do
				(
					try (
						tarName = selection[i].SymmetryNode
						if tarName.count == 0 do (
							tarName = selection[i].name
						)
					) 
					catch (
						tarName = selection[i].name
					)
					format "%\n" tarName to:fs
				)

				for i = 1 to selection.count do
				(
					try (
						flipAxis = selection[i].FlipAxis
					)
					catch (
						flipAxis = 2
					)

					if selection[i].parent == undefined then (
						pTrans = (matrix3 1)
					) else (
						try (
							pFlipAxis = selection[i].parent.FlipAxis
							pTrans = GetMirrorMatrix selection[i].parent.transform pFlipAxis
						) catch (
							pTrans = GetMirrorMatrix selection[i].parent.transform flipAxis
						)
					)

					wTrans = GetMirrorMatrix selection[i].transform flipAxis
					locTrans = wTrans * (inverse pTrans)

					vPos = locTrans.pos
					vRot = locTrans.rotation
					vScl = locTrans.scale

					format "%\t%\t%\n" vPos vRot vScl to:fs
				)
			)
		)
		else
		(
			messageBox "你必須選一個物件..." title:"警告!" beep:on
		)
	)

	on BTN_PoseIm pressed do
	(
		ImpFileName = getOpenFileName caption:"Select a Pose file..." types:"Pose file(*.pose)|*.pose|"
		if (ImpFileName != undefined) then
		(
			fs = openFile ImpFileName
			CheckWord = readLine fs
			if (CheckWord == "PoseData") then
			(
				ObjCount = readValue fs
				TargetObjArray = #()
				for i = 1 to ObjCount do
				(
					ObjName = readLine fs
					PickTarget = getNodebyName ObjName exact:true
					append TargetObjArray PickTarget
				)
				undo "" on
				(
					for j = 1 to ObjCount do
					(
						targetPos = readValue fs
						targetRot = readValue fs
						targetScl = readValue fs
						
						if TargetObjArray[j] != undefined then
						(
							TargetObjArray[j].pos.controller.value = targetPos
							TargetObjArray[j].rotation.controller.value = targetRot
							if CB_scale.checked == true then (TargetObjArray[j].scale.controller.value = targetScl)
						)
					)
				)
				messageBox "Pose Import OK!!" title:"^o^//" beep:off
			)
			else
			(
				messageBox "這不是正確的Pose檔!" title:"警告" beep:on
			)
			close fs
		)
	)--BTN_PoseIm END
		
	on BTN_AnmEx pressed do
	(
		if selection.count > 0 then
		(
			ExpFileName = getSaveFileName caption:"Save Animation..." types:"Anm file(*.anm)|*.anm|"
			if (ExpFileName != undefined) then
			(
				fs = createFile ExpFileName
				format "AnmData\n" to:fs
				tStart = animationRange.start
				tEnd = animationRange.end
				tNow = currentTime
				TimeLength = (tEnd - tStart) + 1f
				format "%\n" TimeLength to:fs
				--pickObj = point()
				format "<" to:fs
				format "%" selection[1].name to:fs
				for n = 2 to selection.count do
				(
					format ",%" selection[n].name to:fs
				)
				format ">\n" to:fs
				for vT = tStart to tEnd do
				(
					format "<%><\n" vT to:fs
					sliderTime = vT
					for i = 1 to selection.count do
					(
						if selection[i].parent != undefined then (
							pTran = selection[i].parent.transform
						)else(
							pTran = matrix3 1
						)

						locTrans = selection[i].transform * (inverse pTran)

						vPos = locTrans.pos
						vRot = locTrans.rotation
						vScl = locTrans.scale
						--pickObj.transform = selection[i].transform
						--pickObj.parent = selection[i].parent
						--vPos = in coordsys parent pickObj.pos
						--vRot = in coordsys parent pickObj.rotation
						--vScl = in coordsys parent pickObj.scale
						format "\t% % %\n" vPos vRot vScl to:fs
					)
					format ">\n" to:fs
				)
				--delete pickObj
				sliderTime = tNow
				close fs
				messageBox "Success!!" title:"^o^//" beep:off
			)
		)
		else
		(
			messageBox "你必須選一個物件..." title:"警告" beep:on
		)
	)--BTN_AnmEx END
	
	on BTN_MAnmEx pressed do
	(
		if selection.count > 0 then
		(
			ExpFileName = getSaveFileName caption:"Save Animation..." types:"Anm file(*.anm)|*.anm|"
			if (ExpFileName != undefined) then
			(
				fs = createFile ExpFileName
				format "AnmData\n" to:fs
				tStart = animationRange.start
				tEnd = animationRange.end
				tNow = currentTime
				TimeLength = (tEnd - tStart) + 1f
				format "%\n" TimeLength to:fs
				--pickObj = point()
				format "<" to:fs
				format "%" selection[1].name to:fs
				for n = 2 to selection.count do
				(
					format ",%" selection[n].name to:fs
				)
				format ">\n" to:fs
				for vT = tStart to tEnd do
				(
					format "<%><\n" vT to:fs
					sliderTime = vT
					for i = 1 to selection.count do
					(
						try (
							flipAxis = selection[i].FlipAxis
						)
						catch (
							flipAxis = 2
						)

						if selection[i].parent == undefined then (
							pTrans = (matrix3 1)--GetMirrorMatrix (matrix3 1) flipAxis
						) else (
							try (
								pFlipAxis = selection[i].parent.FlipAxis
								pTrans = GetMirrorMatrix selection[i].parent.transform pFlipAxis
							) catch (
								pTrans = GetMirrorMatrix selection[i].parent.transform flipAxis
							)
						)

						wTrans = GetMirrorMatrix selection[i].transform flipAxis
						locTrans = wTrans * (inverse pTrans)

						vPos = locTrans.pos
						vRot = locTrans.rotation
						vScl = locTrans.scale

						format "\t% % %\n" vPos vRot vScl to:fs
					)
					format ">\n" to:fs
				)
				--delete pickObj
				sliderTime = tNow
				close fs
				messageBox "Success!!" title:"^o^//" beep:off
			)
		)
		else
		(
			messageBox "你必須選一個物件..." title:"警告" beep:on
		)
	)--BTN_MAnmEx END

	on BTN_AnmIm pressed do
	(
		ImpFileName = getOpenFileName caption:"Select a Anm file..." types:"Anm file(*.anm)|*.anm|"
		if (ImpFileName != undefined) then
		(
			fs = openFile ImpFileName
			CheckWord = readLine fs
			if (CheckWord == "AnmData") then
			(
				TimeLength = readValue fs
				TimeArray = #()
				PosArray = #()
				RotArray = #()
				SclArray = #()
				ObjNames = readLine fs
				TargetObjArray = filterString ObjNames "<>,"
				
				for TL = 1 to TimeLength do
				(
					TimeStr = filterString (readLine fs) "<>"
					append TimeArray TimeStr[1]
					for oNum = 1 to TargetObjArray.count do
					(
						tmpLine = readLine fs
						--print (QWER)
						tmpArray = filterString tmpLine "	 [](),"
						append PosArray (Point3 (tmpArray[1] as float) (tmpArray[2] as float) (tmpArray[3] as float))
						append RotArray (quat (tmpArray[5] as float) (tmpArray[6] as float) (tmpArray[7] as float) (tmpArray[8] as float))
						append SclArray (Point3 (tmpArray[9] as float) (tmpArray[10] as float) (tmpArray[11] as float))
						--append PosArray (readValue fs)
						--append RotArray (readValue fs)
						--append SclArray (readValue fs)
					)
					readLine fs
					--print ("SKIP" +QWER)
					--skipToNextLine fs
				)
				
				tNow = currentTime
				undo "" on
				(
					for tV = 1 to TimeArray.count do
					(
						nTime = tNow + ((TimeArray[tV] as Integer)as Time)
						for SA = 1 to TargetObjArray.count do
						(
							cObj = getNodeByName TargetObjArray[SA]
							vO = TargetObjArray.count * (tV - 1) + SA
							if cObj != undefined then
							(
								animate on
								(
									at Time nTime 
									(
										--in coordsys parent cObj.rotation = RotArray[vO];
										--in coordsys parent cObj.pos = PosArray[vO];
										--if CB_scale.checked == true then (in coordsys parent cObj.scale = SclArray[vO])
										cObj.pos.controller.value = PosArray[vO]
										cObj.rotation.controller.value = RotArray[vO]
										if CB_scale.checked == true then (cObj.scale.controller.value = SclArray[vO])

									)
								)--end animate
							)--end if
						)--end for
					)--end for
					for SA = 1 to TargetObjArray.count do
					(
						cObj = getNodeByName TargetObjArray[SA]
						if cObj != undefined then
						(
							fixRotation cObj
						)
					)

				)--end undo
			)
			else
			(
				messageBox "這不是正確的Anm檔!" title:"警告" beep:on
			)
			close fs
		)
	)--BTN_AnmIm END
)

createDialog KAnmRec W H