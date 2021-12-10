--------------------------------------------------
	posJntHip				= ctrlHip.transform.pos
	posJntWaist				= pySpine1.transform.pos
	posJntChest0			= pySpine2.transform.pos
	posJntChest1			= pySpine3.transform.pos
-- 	posJntNeck				= ctrlNeck.transform.pos
	posJntNeck1				= locNeck1.transform.pos
	posJntNeck2				= locNeck2.transform.pos
	posJntHead				= ctrlHead.transform.pos
	posJntHeadTop			= posHeadTopNode
	posJntShoulder_R		= ctrlShoulder_R.transform.pos
	posJntUpperArm_R		= UpperArmTwistBoneList_R[1].transform.pos
	posJntUpperArmTw1_R		= UpperArmTwistBoneList_R[2].transform.pos
	posJntUpperArmTw2_R		= UpperArmTwistBoneList_R[3].transform.pos
	posJntUpperArmTw3_R		= UpperArmTwistBoneList_R[4].transform.pos
	posJntElbow_R			= boneElbow_R.transform.pos
	posJntForeArm_R			= ForeArmTwistBoneList_R[1].transform.pos
	posJntForeArmTw1_R		= ForeArmTwistBoneList_R[2].transform.pos
	posJntForeArmTw2_R		= ForeArmTwistBoneList_R[3].transform.pos
	posJntForeArmTw3_R		= ForeArmTwistBoneList_R[4].transform.pos
	posJntHand_R			= boneHand_R.transform.pos
	posJntFinger00_R		= posFinger00_R
	posJntFinger01_R		= posFinger01_R
	posJntFinger02_R		= posFinger02_R
	posJntFinger0E_R		= posFinger0E_R
	posJntFinger10_R		= posFinger10_R
	posJntFinger11_R		= posFinger11_R
	posJntFinger12_R		= posFinger12_R
	posJntFinger1E_R		= posFinger1E_R
	posJntFinger20_R		= posFinger20_R
	posJntFinger21_R		= posFinger21_R
	posJntFinger22_R		= posFinger22_R
	posJntFinger2E_R		= posFinger2E_R
	posJntFinger30_R		= posFinger30_R
	posJntFinger31_R		= posFinger31_R
	posJntFinger32_R		= posFinger32_R
	posJntFinger3E_R		= posFinger3E_R
	posJntFinger40_R		= posFinger40_R
	posJntFinger41_R		= posFinger41_R
	posJntFinger42_R		= posFinger42_R
	posJntFinger4E_R		= posFinger4E_R

	posJntShoulder_L		= ctrlShoulder_L.transform.pos
	posJntUpperArm_L		= UpperArmTwistBoneList_L[1].transform.pos
	posJntUpperArmTw1_L		= UpperArmTwistBoneList_L[2].transform.pos
	posJntUpperArmTw2_L		= UpperArmTwistBoneList_L[3].transform.pos
	posJntUpperArmTw3_L		= UpperArmTwistBoneList_L[4].transform.pos
	posJntElbow_L			= boneElbow_L.transform.pos
	posJntForeArm_L			= ForeArmTwistBoneList_L[1].transform.pos
	posJntForeArmTw1_L		= ForeArmTwistBoneList_L[2].transform.pos
	posJntForeArmTw2_L		= ForeArmTwistBoneList_L[3].transform.pos
	posJntForeArmTw3_L		= ForeArmTwistBoneList_L[4].transform.pos
	posJntHand_L			= boneHand_L.transform.pos
	posJntFinger00_L		= posFinger00_L
	posJntFinger01_L		= posFinger01_L
	posJntFinger02_L		= posFinger02_L
	posJntFinger0E_L		= posFinger0E_L
	posJntFinger10_L		= posFinger10_L
	posJntFinger11_L		= posFinger11_L
	posJntFinger12_L		= posFinger12_L
	posJntFinger1E_L		= posFinger1E_L
	posJntFinger20_L		= posFinger20_L
	posJntFinger21_L		= posFinger21_L
	posJntFinger22_L		= posFinger22_L
	posJntFinger2E_L		= posFinger2E_L
	posJntFinger30_L		= posFinger30_L
	posJntFinger31_L		= posFinger31_L
	posJntFinger32_L		= posFinger32_L
	posJntFinger3E_L		= posFinger3E_L
	posJntFinger40_L		= posFinger40_L
	posJntFinger41_L		= posFinger41_L
	posJntFinger42_L		= posFinger42_L
	posJntFinger4E_L		= posFinger4E_L

	posJntThigh_R			= posThigh_R
	posJntThighTw1_R		= LegTwistBoneList_R[2].transform.pos
	posJntThighTw2_R		= LegTwistBoneList_R[3].transform.pos
	posJntThighTw3_R		= LegTwistBoneList_R[4].transform.pos
	posJntKnee_R			= posKneeStart_R
	posJntCalf_R			= posKneeEnd_R
	posJntFoot_R			= posFoot_R
	posJntToe_R				= posToe_R
	posJntToeE_R			= posToeE_R

	posJntThigh_L			= posThigh_L
	posJntThighTw1_L		= LegTwistBoneList_L[2].transform.pos
	posJntThighTw2_L		= LegTwistBoneList_L[3].transform.pos
	posJntThighTw3_L		= LegTwistBoneList_L[4].transform.pos
	posJntKnee_L			= posKneeStart_L
	posJntCalf_L			= posKneeEnd_L
	posJntFoot_L			= posFoot_L
	posJntToe_L				= posToe_L
	posJntToeE_L			= posToeE_L

	locShoulderRotMat = ctrlShoulder_R.transform * (inverse pySpine3.transform)
	locPos = [locShoulderRotMat.pos.x, 0, 0]
	posShoulderRoot = locPos * pySpine3.transform

	locTeresMajoMat = boneTeresMajor_R.transform * (inverse pySpine3.transform)
	locPos = [locTeresMajoMat.pos.x, 0, 0]
	posTeresMajoRoot = locPos * pySpine3.transform

--------------------------------------------------------------
	BoneLayer = LayerManager.getLayerFromName "0.Bone"
	if BoneLayer == undefined then (
		BoneLayer = LayerManager.newLayer()
		BoneLayer.setname "0.Bone"
	)

	BoneList = #()
--------------------------------------------------------------
	bRoot = point name:"RootNode" size:4 cross:off Box:on wirecolor:(color 0 255 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
	bRoot.transform = matrix3 1
	BoneLayer.addNode bRoot

	bHip = BoneSys.createBone posJntHip posJntWaist [0,1,0]
	bHip.name = "B_Hip"
	bHip.transform = ctrlHip.transform
	bHip.width = 5.5
	bHip.height = 5.5
	bHip.Taper = 90
	bHip.sidefins = off
	bHip.sidefinssize = 2
	bHip.frontfin = off
	bHip.frontfinsize = 2
	bHip.backfin = off
	bHip.backfinsize = 2
	bHip.parent = bRoot
	BoneLayer.addNode bHip
	append BoneList bHip

	HipInvScl0 = point name:"InvSclHip0" size:1 cross:off Box:on wirecolor:(color 128 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
	HipInvScl0.transform = bHip.transform
	HipInvScl0.parent = bHip
	BoneLayer.addNode HipInvScl0

	HipInvScl = point name:"InvSclHip" size:1 cross:off Box:on wirecolor:(color 128 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
	HipInvScl.transform = bHip.transform
	HipInvScl.pos = posJntWaist
	HipInvScl.parent = bHip
	BoneLayer.addNode HipInvScl

	bWaist = BoneSys.createBone posJntWaist posJntChest0 [0,1,0]
	bWaist.name = "B_Waist"
	bWaist.transform = pySpine1.transform
	bWaist.width = 5.5
	bWaist.height = 5.5
	bWaist.Taper = 90
	bWaist.sidefins = off
	bWaist.sidefinssize = 2
	bWaist.frontfin = off
	bWaist.frontfinsize = 2
	bWaist.backfin = off
	bWaist.backfinsize = 2
	bWaist.parent = HipInvScl
	BoneLayer.addNode bWaist
	append BoneList bWaist

	WaistInvScl = point name:"InvSclWaist" size:1 cross:off Box:on wirecolor:(color 128 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
	WaistInvScl.transform = bWaist.transform
	WaistInvScl.pos = posJntChest0
	WaistInvScl.parent = bWaist
	BoneLayer.addNode WaistInvScl

	bChest0 = BoneSys.createBone posJntChest0 posJntChest1 [0,1,0]
	bChest0.name = "B_Chest0"
	bChest0.transform = pySpine2.transform
	bChest0.width = 5.5
	bChest0.height = 5.5
	bChest0.Taper = 90
	bChest0.sidefins = off
	bChest0.sidefinssize = 2
	bChest0.frontfin = off
	bChest0.frontfinsize = 2
	bChest0.backfin = off
	bChest0.backfinsize = 2
	bChest0.parent = WaistInvScl
	BoneLayer.addNode bChest0
	append BoneList bChest0

	Chest0InvScl = point name:"InvSclChest0" size:1 cross:off Box:on wirecolor:(color 128 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
	Chest0InvScl.transform = bChest0.transform
	Chest0InvScl.pos = posJntChest1
	Chest0InvScl.parent = bChest0
	BoneLayer.addNode Chest0InvScl

	bChest1 = BoneSys.createBone posJntChest1 posJntNeck1 [0,1,0]
	bChest1.name = "B_Chest1"
	bChest1.transform = pySpine3.transform
	bChest1.width = 5.5
	bChest1.height = 5.5
	bChest1.Taper = 90
	bChest1.sidefins = off
	bChest1.sidefinssize = 2
	bChest1.frontfin = off
	bChest1.frontfinsize = 2
	bChest1.backfin = off
	bChest1.backfinsize = 2
	bChest1.parent = Chest0InvScl
	BoneLayer.addNode bChest1
	append BoneList bChest1
	Chest1InvScl = point name:"InvSclChest1" size:1 cross:off Box:on wirecolor:(color 128 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
	Chest1InvScl.transform = bChest1.transform
	Chest1InvScl.pos = posJntNeck1
	Chest1InvScl.parent = bChest1
	BoneLayer.addNode Chest1InvScl

-- 	bNeck = BoneSys.createBone posJntNeck posJntHead [0,1,0]
-- 	bNeck.name = "B_Neck"
-- 	bNeck.transform = ctrlNeck.transform
-- 	bNeck.width = 3.5
-- 	bNeck.height = 3.5
-- 	bNeck.Taper = 90
-- 	bNeck.sidefins = off
-- 	bNeck.sidefinssize = 2
-- 	bNeck.frontfin = off
-- 	bNeck.frontfinsize = 2
-- 	bNeck.backfin = off
-- 	bNeck.backfinsize = 2
-- 	bNeck.parent = Chest1InvScl
-- 	BoneLayer.addNode bNeck
-- 	append BoneList bNeck
	bNeck1 = BoneSys.createBone posJntNeck1 posJntNeck2 [0,1,0]
	bNeck1.name = "B_Neck1"
	bNeck1.transform = locNeck1.transform
	bNeck1.width = 3.5
	bNeck1.height = 3.5
	bNeck1.Taper = 90
	bNeck1.sidefins = off
	bNeck1.sidefinssize = 2
	bNeck1.frontfin = off
	bNeck1.frontfinsize = 2
	bNeck1.backfin = off
	bNeck1.backfinsize = 2
	bNeck1.parent = Chest1InvScl
	BoneLayer.addNode bNeck1
	append BoneList bNeck1

	bNeck2 = BoneSys.createBone posJntNeck2 posJntHead [0,1,0]
	bNeck2.name = "B_Neck2"
	bNeck2.transform = locNeck2.transform
	bNeck2.width = 3.5
	bNeck2.height = 3.5
	bNeck2.Taper = 90
	bNeck2.sidefins = off
	bNeck2.sidefinssize = 2
	bNeck2.frontfin = off
	bNeck2.frontfinsize = 2
	bNeck2.backfin = off
	bNeck2.backfinsize = 2
	bNeck2.parent = bNeck1
	BoneLayer.addNode bNeck2
	append BoneList bNeck2



	bHead = BoneSys.createBone posJntHead posJntHeadTop [0,1,0]
	bHead.name = "B_Head"
	bHead.transform = ctrlHead.transform
	bHead.width = 6.5
	bHead.height = 6.5
	bHead.Taper = 50
	bHead.sidefins = off
	bHead.sidefinssize = 2
	bHead.frontfin = off
	bHead.frontfinsize = 2
	bHead.backfin = off
	bHead.backfinsize = 2
	bHead.parent = bNeck2
	BoneLayer.addNode bHead
	append BoneList bHead

	bHeadEff = BoneSys.createBone posJntHeadTop posJntHeadTop [0,1,0]
	bHeadEff.name = "eff_Head"
	bHeadEff.width = 3
	bHeadEff.height = 3
	bHeadEff.Taper = 90
	bHeadEff.sidefins = off
	bHeadEff.sidefinssize = 2
	bHeadEff.frontfin = off
	bHeadEff.frontfinsize = 2
	bHeadEff.backfin = off
	bHeadEff.backfinsize = 2
	bHeadEff.parent = bHead
	bHeadEff.length = 3
	bHeadEff.rotation.controller.value = (quat 0 0 0 1)
	BoneLayer.addNode bHeadEff
	append BoneList bHeadEff
	-----------------------------------------------
	bThigh_R = BoneSys.createBone posJntThigh_R posJntKnee_R [0,1,0]
	bThigh_R.name = "B_Thigh_R"
	bThigh_R.transform = LegTwistBoneList_R[1].transform
	bThigh_R.width = 5.5
	bThigh_R.height = 5.5
	bThigh_R.Taper = 90
	bThigh_R.sidefins = off
	bThigh_R.sidefinssize = 2
	bThigh_R.frontfin = off
	bThigh_R.frontfinsize = 2
	bThigh_R.backfin = off
	bThigh_R.backfinsize = 2
	bThigh_R.parent = HipInvScl0
	BoneLayer.addNode bThigh_R
	append BoneList bThigh_R

	bCalf_R = BoneSys.createBone posJntCalf_R posJntFoot_R [0,1,0]
	bCalf_R.name = "B_Thigh_R"
	bCalf_R.transform = boneCalf_R.transform
	bCalf_R.width = 5.5
	bCalf_R.height = 5.5
	bCalf_R.Taper = 90
	bCalf_R.sidefins = off
	bCalf_R.sidefinssize = 2
	bCalf_R.frontfin = off
	bCalf_R.frontfinsize = 2
	bCalf_R.backfin = off
	bCalf_R.backfinsize = 2
	bCalf_R.parent = bThigh_R
	BoneLayer.addNode bCalf_R
	append BoneList bCalf_R

	bFoot_R = BoneSys.createBone posJntFoot_R posJntToe_R [0,1,0]
	bFoot_R.name = "B_Foot_R"
	bFoot_R.transform = boneFoot_R.transform
	bFoot_R.width = 4.5
	bFoot_R.height = 4.5
	bFoot_R.Taper = 90
	bFoot_R.sidefins = off
	bFoot_R.sidefinssize = 2
	bFoot_R.frontfin = off
	bFoot_R.frontfinsize = 2
	bFoot_R.backfin = off
	bFoot_R.backfinsize = 2
	bFoot_R.parent = bCalf_R
	BoneLayer.addNode bFoot_R
	append BoneList bFoot_R

	bToe_R = BoneSys.createBone posJntToe_R posJntToeE_R [0,1,0]
	bToe_R.name = "B_Toe_R"
	bToe_R.transform = boneToe_R.transform
	bToe_R.width = 2.5
	bToe_R.height = 2.5
	bToe_R.Taper = 90
	bToe_R.sidefins = off
	bToe_R.sidefinssize = 2
	bToe_R.frontfin = off
	bToe_R.frontfinsize = 2
	bToe_R.backfin = off
	bToe_R.backfinsize = 2
	bToe_R.parent = bFoot_R
	BoneLayer.addNode bToe_R
	append BoneList bToe_R

	bToeEff_R = BoneSys.createBone posJntToeE_R posJntToeE_R [0,1,0]
	bToeEff_R.name = "eff_Toe_R"
	bToeEff_R.width = 1
	bToeEff_R.height = 1
	bToeEff_R.Taper = 90
	bToeEff_R.sidefins = off
	bToeEff_R.sidefinssize = 2
	bToeEff_R.frontfin = off
	bToeEff_R.frontfinsize = 2
	bToeEff_R.backfin = off
	bToeEff_R.backfinsize = 2
	bToeEff_R.parent = bToe_R
	bToeEff_R.length = 1
	bToeEff_R.rotation.controller.value = (quat 0 0 0 1)
	BoneLayer.addNode bToeEff_R
	append BoneList bToeEff_R

	bKnee_R = BoneSys.createBone posJntKnee_R posJntCalf_R [0,1,0]
	bKnee_R.name = "B_Knee_R"
	bKnee_R.transform = boneKnee_R.transform
	bKnee_R.width = 2.5
	bKnee_R.height = 2.5
	bKnee_R.Taper = 90
	bKnee_R.sidefins = off
	bKnee_R.sidefinssize = 2
	bKnee_R.frontfin = off
	bKnee_R.frontfinsize = 2
	bKnee_R.backfin = off
	bKnee_R.backfinsize = 2
	bKnee_R.parent = bThigh_R
	BoneLayer.addNode bKnee_R
	append BoneList bKnee_R

	bThighTw1_R = BoneSys.createBone posJntThighTw1_R posJntThighTw2_R [0,1,0]
	bThighTw1_R.name = "B_ThighTw1_R"
	bThighTw1_R.transform = LegTwistBoneList_R[2].transform
	bThighTw1_R.width = 5.5
	bThighTw1_R.height = 5.5
	bThighTw1_R.Taper = 10
	bThighTw1_R.sidefins = off
	bThighTw1_R.sidefinssize = 2
	bThighTw1_R.frontfin = off
	bThighTw1_R.frontfinsize = 2
	bThighTw1_R.backfin = off
	bThighTw1_R.backfinsize = 2
	bThighTw1_R.parent = bThigh_R
	BoneLayer.addNode bThighTw1_R
	append BoneList bThighTw1_R

	bThighTw2_R = BoneSys.createBone posJntThighTw2_R posJntThighTw3_R [0,1,0]
	bThighTw2_R.name = "B_ThighTw2_R"
	bThighTw2_R.transform = LegTwistBoneList_R[3].transform
	bThighTw2_R.width = 5.5
	bThighTw2_R.height = 5.5
	bThighTw2_R.Taper = 10
	bThighTw2_R.sidefins = off
	bThighTw2_R.sidefinssize = 2
	bThighTw2_R.frontfin = off
	bThighTw2_R.frontfinsize = 2
	bThighTw2_R.backfin = off
	bThighTw2_R.backfinsize = 2
	bThighTw2_R.parent = bThigh_R
	BoneLayer.addNode bThighTw2_R
	append BoneList bThighTw2_R

	bThighTw3_R = BoneSys.createBone posJntThighTw3_R posJntKnee_R [0,1,0]
	bThighTw3_R.name = "B_ThighTw3_R"
	bThighTw3_R.transform = LegTwistBoneList_R[4].transform
	bThighTw3_R.width = 5
	bThighTw3_R.height = 5
	bThighTw3_R.Taper = 30
	bThighTw3_R.sidefins = off
	bThighTw3_R.sidefinssize = 2
	bThighTw3_R.frontfin = off
	bThighTw3_R.frontfinsize = 2
	bThighTw3_R.backfin = off
	bThighTw3_R.backfinsize = 2
	bThighTw3_R.parent = bThigh_R
	BoneLayer.addNode bThighTw3_R
	append BoneList bThighTw3_R
	---------------------------------------
	bThigh_L = BoneSys.createBone posJntThigh_L posJntKnee_L [0,1,0]
	bThigh_L.name = "B_Thigh_L"
	bThigh_L.transform = LegTwistBoneList_L[1].transform
	bThigh_L.width = 5.5
	bThigh_L.height = 5.5
	bThigh_L.Taper = 90
	bThigh_L.sidefins = off
	bThigh_L.sidefinssize = 2
	bThigh_L.frontfin = off
	bThigh_L.frontfinsize = 2
	bThigh_L.backfin = off
	bThigh_L.backfinsize = 2
	bThigh_L.parent = HipInvScl0
	BoneLayer.addNode bThigh_L
	append BoneList bThigh_L

	bCalf_L = BoneSys.createBone posJntCalf_L posJntFoot_L [0,1,0]
	bCalf_L.name = "B_Thigh_L"
	bCalf_L.transform = boneCalf_L.transform
	bCalf_L.width = 5.5
	bCalf_L.height = 5.5
	bCalf_L.Taper = 90
	bCalf_L.sidefins = off
	bCalf_L.sidefinssize = 2
	bCalf_L.frontfin = off
	bCalf_L.frontfinsize = 2
	bCalf_L.backfin = off
	bCalf_L.backfinsize = 2
	bCalf_L.parent = bThigh_L
	BoneLayer.addNode bCalf_L
	append BoneList bCalf_L

	bFoot_L = BoneSys.createBone posJntFoot_L posJntToe_L [0,1,0]
	bFoot_L.name = "B_Foot_L"
	bFoot_L.transform = boneFoot_L.transform
	bFoot_L.width = 4.5
	bFoot_L.height = 4.5
	bFoot_L.Taper = 90
	bFoot_L.sidefins = off
	bFoot_L.sidefinssize = 2
	bFoot_L.frontfin = off
	bFoot_L.frontfinsize = 2
	bFoot_L.backfin = off
	bFoot_L.backfinsize = 2
	bFoot_L.parent = bCalf_L
	BoneLayer.addNode bFoot_L
	append BoneList bFoot_L

	bToe_L = BoneSys.createBone posJntToe_L posJntToeE_L [0,1,0]
	bToe_L.name = "B_Toe_L"
	bToe_L.transform = boneToe_L.transform
	bToe_L.width = 2.5
	bToe_L.height = 2.5
	bToe_L.Taper = 90
	bToe_L.sidefins = off
	bToe_L.sidefinssize = 2
	bToe_L.frontfin = off
	bToe_L.frontfinsize = 2
	bToe_L.backfin = off
	bToe_L.backfinsize = 2
	bToe_L.parent = bFoot_L
	BoneLayer.addNode bToe_L
	append BoneList bToe_L

	bToeEff_L = BoneSys.createBone posJntToeE_L posJntToeE_L [0,1,0]
	bToeEff_L.name = "eff_Toe_L"
	bToeEff_L.width = 1
	bToeEff_L.height = 1
	bToeEff_L.Taper = 90
	bToeEff_L.sidefins = off
	bToeEff_L.sidefinssize = 2
	bToeEff_L.frontfin = off
	bToeEff_L.frontfinsize = 2
	bToeEff_L.backfin = off
	bToeEff_L.backfinsize = 2
	bToeEff_L.parent = bToe_L
	bToeEff_L.length = 1
	bToeEff_L.rotation.controller.value = (quat 0 0 0 1)
	BoneLayer.addNode bToeEff_L
	append BoneList bToeEff_L

	bKnee_L = BoneSys.createBone posJntKnee_L posJntCalf_L [0,1,0]
	bKnee_L.name = "B_Knee_L"
	bKnee_L.transform = boneKnee_L.transform
	bKnee_L.width = 2.5
	bKnee_L.height = 2.5
	bKnee_L.Taper = 90
	bKnee_L.sidefins = off
	bKnee_L.sidefinssize = 2
	bKnee_L.frontfin = off
	bKnee_L.frontfinsize = 2
	bKnee_L.backfin = off
	bKnee_L.backfinsize = 2
	bKnee_L.parent = bThigh_L
	BoneLayer.addNode bKnee_L
	append BoneList bKnee_L

	bThighTw1_L = BoneSys.createBone posJntThighTw1_L posJntThighTw2_L [0,1,0]
	bThighTw1_L.name = "B_ThighTw1_L"
	bThighTw1_L.transform = LegTwistBoneList_L[2].transform
	bThighTw1_L.width = 5.5
	bThighTw1_L.height = 5.5
	bThighTw1_L.Taper = 10
	bThighTw1_L.sidefins = off
	bThighTw1_L.sidefinssize = 2
	bThighTw1_L.frontfin = off
	bThighTw1_L.frontfinsize = 2
	bThighTw1_L.backfin = off
	bThighTw1_L.backfinsize = 2
	bThighTw1_L.parent = bThigh_L
	BoneLayer.addNode bThighTw1_L
	append BoneList bThighTw1_L

	bThighTw2_L = BoneSys.createBone posJntThighTw2_L posJntThighTw3_L [0,1,0]
	bThighTw2_L.name = "B_ThighTw2_L"
	bThighTw2_L.transform = LegTwistBoneList_L[3].transform
	bThighTw2_L.width = 5.5
	bThighTw2_L.height = 5.5
	bThighTw2_L.Taper = 10
	bThighTw2_L.sidefins = off
	bThighTw2_L.sidefinssize = 2
	bThighTw2_L.frontfin = off
	bThighTw2_L.frontfinsize = 2
	bThighTw2_L.backfin = off
	bThighTw2_L.backfinsize = 2
	bThighTw2_L.parent = bThigh_L
	BoneLayer.addNode bThighTw2_L
	append BoneList bThighTw2_L

	bThighTw3_L = BoneSys.createBone posJntThighTw3_L posJntKnee_L [0,1,0]
	bThighTw3_L.name = "B_ThighTw3_L"
	bThighTw3_L.transform = LegTwistBoneList_L[4].transform
	bThighTw3_L.width = 5
	bThighTw3_L.height = 5
	bThighTw3_L.Taper = 30
	bThighTw3_L.sidefins = off
	bThighTw3_L.sidefinssize = 2
	bThighTw3_L.frontfin = off
	bThighTw3_L.frontfinsize = 2
	bThighTw3_L.backfin = off
	bThighTw3_L.backfinsize = 2
	bThighTw3_L.parent = bThigh_L
	BoneLayer.addNode bThighTw3_L
	append BoneList bThighTw3_L
------------Butt-------------------
	bButt_R = point name:"B_Butt_R" size:8 cross:off Box:on wirecolor:(color 174 186 203) axistripod:off centermarker:off drawontop:off constantscreensize:off
	bButt_R.transform = boneButt_R.transform
	bButt_R.parent = HipInvScl0
	BoneLayer.addNode bButt_R

	bButt_L = point name:"B_Butt_L" size:8 cross:off Box:on wirecolor:(color 174 186 203) axistripod:off centermarker:off drawontop:off constantscreensize:off
	bButt_L.transform = boneButt_L.transform
	bButt_L.parent = HipInvScl0
	BoneLayer.addNode bButt_L
---------------------------------
	Chest1InvScl_Sh = point name:"InvSclChest1_Sh" size:1 cross:off Box:on wirecolor:(color 128 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
	Chest1InvScl_Sh.transform = bChest1.transform
	Chest1InvScl_Sh.pos = posShoulderRoot
	Chest1InvScl_Sh.parent = bChest1
	BoneLayer.addNode Chest1InvScl_Sh

	Chest1InvScl_Tm = point name:"InvSclChest1_Tm" size:1 cross:off Box:on wirecolor:(color 128 0 0) axistripod:off centermarker:off drawontop:off constantscreensize:off
	Chest1InvScl_Tm.transform = bChest1.transform
	Chest1InvScl_Tm.pos = posTeresMajoRoot
	Chest1InvScl_Tm.parent = bChest1
	BoneLayer.addNode Chest1InvScl_Tm
--------Right Arm-----------
	bShoulder_R = BoneSys.createBone posJntShoulder_R posJntUpperArm_R [0,1,0]
	bShoulder_R.name = "B_Shoulder_R"
	bShoulder_R.transform = ctrlShoulder_R.transform
	bShoulder_R.width = 5.5
	bShoulder_R.height = 5.5
	bShoulder_R.Taper = 90
	bShoulder_R.sidefins = off
	bShoulder_R.sidefinssize = 2
	bShoulder_R.frontfin = off
	bShoulder_R.frontfinsize = 2
	bShoulder_R.backfin = off
	bShoulder_R.backfinsize = 2
	bShoulder_R.parent = Chest1InvScl_Sh
	BoneLayer.addNode bShoulder_R
	append BoneList bShoulder_R

	bUpperArm_R = BoneSys.createBone posJntUpperArm_R posJntElbow_R [0,1,0]
	bUpperArm_R.name = "B_UpperArm_R"
	bUpperArm_R.transform = UpperArmTwistBoneList_R[1].transform
	bUpperArm_R.width = 4
	bUpperArm_R.height = 4
	bUpperArm_R.Taper = 90
	bUpperArm_R.sidefins = off
	bUpperArm_R.sidefinssize = 2
	bUpperArm_R.frontfin = off
	bUpperArm_R.frontfinsize = 2
	bUpperArm_R.backfin = off
	bUpperArm_R.backfinsize = 2
	bUpperArm_R.parent = bShoulder_R
	BoneLayer.addNode bUpperArm_R
	append BoneList bUpperArm_R

	bForeArm_R = BoneSys.createBone posJntForeArm_R posJntHand_R [0,1,0]
	bForeArm_R.name = "B_ForeArm_R"
	bForeArm_R.transform = ForeArmTwistBoneList_R[1].transform
	bForeArm_R.width = 4
	bForeArm_R.height = 4
	bForeArm_R.Taper = 90
	bForeArm_R.sidefins = off
	bForeArm_R.sidefinssize = 2
	bForeArm_R.frontfin = off
	bForeArm_R.frontfinsize = 2
	bForeArm_R.backfin = off
	bForeArm_R.backfinsize = 2
	bForeArm_R.parent = bUpperArm_R
	BoneLayer.addNode bForeArm_R
	append BoneList bForeArm_R

	bHand_R = BoneSys.createBone posJntHand_R posJntHand_R [0,1,0]
	bHand_R.name = "B_Hand_R"
	bHand_R.transform = boneHand_R.transform
	bHand_R.width = 3
	bHand_R.height = 3
	bHand_R.Taper = 90
	bHand_R.sidefins = off
	bHand_R.sidefinssize = 2
	bHand_R.frontfin = off
	bHand_R.frontfinsize = 2
	bHand_R.backfin = off
	bHand_R.backfinsize = 2
	bHand_R.parent = bForeArm_R
	bHand_R.length = boneHand_R.length
	BoneLayer.addNode bHand_R
	append BoneList bHand_R

	bFinger00_R = BoneSys.createBone posJntFinger00_R posJntFinger01_R [0,1,0]
	bFinger00_R.name = "B_Finger00_R"
	bFinger00_R.transform = CtrlFinger00_R.transform
	bFinger00_R.width = 1
	bFinger00_R.height = 1
	bFinger00_R.Taper = 90
	bFinger00_R.sidefins = off
	bFinger00_R.sidefinssize = 2
	bFinger00_R.frontfin = off
	bFinger00_R.frontfinsize = 2
	bFinger00_R.backfin = off
	bFinger00_R.backfinsize = 2
	bFinger00_R.parent = bHand_R
	BoneLayer.addNode bFinger00_R
	append BoneList bFinger00_R

	bFinger01_R = BoneSys.createBone posJntFinger01_R posJntFinger02_R [0,1,0]
	bFinger01_R.name = "B_Finger01_R"
	bFinger01_R.transform = CtrlFinger01_R.transform
	bFinger01_R.width = 1
	bFinger01_R.height = 1
	bFinger01_R.Taper = 90
	bFinger01_R.sidefins = off
	bFinger01_R.sidefinssize = 2
	bFinger01_R.frontfin = off
	bFinger01_R.frontfinsize = 2
	bFinger01_R.backfin = off
	bFinger01_R.backfinsize = 2
	bFinger01_R.parent = bFinger00_R
	BoneLayer.addNode bFinger01_R
	append BoneList bFinger01_R

	bFinger02_R = BoneSys.createBone posJntFinger02_R posJntFinger0E_R [0,1,0]
	bFinger02_R.name = "B_Finger02_R"
	bFinger02_R.transform = CtrlFinger02_R.transform
	bFinger02_R.width = 1
	bFinger02_R.height = 1
	bFinger02_R.Taper = 90
	bFinger02_R.sidefins = off
	bFinger02_R.sidefinssize = 2
	bFinger02_R.frontfin = off
	bFinger02_R.frontfinsize = 2
	bFinger02_R.backfin = off
	bFinger02_R.backfinsize = 2
	bFinger02_R.parent = bFinger01_R
	BoneLayer.addNode bFinger02_R
	append BoneList bFinger02_R

	effFinger0_R = BoneSys.createBone posJntFinger0E_R posJntFinger0E_R [0,1,0]
	effFinger0_R.name = "eff_Finger0_R"
	effFinger0_R.width = 0.5
	effFinger0_R.height = 0.5
	effFinger0_R.Taper = 90
	effFinger0_R.sidefins = off
	effFinger0_R.sidefinssize = 2
	effFinger0_R.frontfin = off
	effFinger0_R.frontfinsize = 2
	effFinger0_R.backfin = off
	effFinger0_R.backfinsize = 2
	effFinger0_R.length = 0.5
	effFinger0_R.parent = bFinger02_R
	effFinger0_R.rotation.controller.value = (quat 0 0 0 1)
	BoneLayer.addNode effFinger0_R
	append BoneList effFinger0_R
	----
	bFinger10_R = BoneSys.createBone posJntFinger10_R posJntFinger11_R [0,1,0]
	bFinger10_R.name = "B_Finger10_R"
	bFinger10_R.transform = CtrlFinger10_R.transform
	bFinger10_R.width = 1
	bFinger10_R.height = 1
	bFinger10_R.Taper = 90
	bFinger10_R.sidefins = off
	bFinger10_R.sidefinssize = 2
	bFinger10_R.frontfin = off
	bFinger10_R.frontfinsize = 2
	bFinger10_R.backfin = off
	bFinger10_R.backfinsize = 2
	bFinger10_R.parent = bHand_R
	BoneLayer.addNode bFinger10_R
	append BoneList bFinger10_R

	bFinger11_R = BoneSys.createBone posJntFinger11_R posJntFinger12_R [0,1,0]
	bFinger11_R.name = "B_Finger11_R"
	bFinger11_R.transform = CtrlFinger11_R.transform
	bFinger11_R.width = 1
	bFinger11_R.height = 1
	bFinger11_R.Taper = 90
	bFinger11_R.sidefins = off
	bFinger11_R.sidefinssize = 2
	bFinger11_R.frontfin = off
	bFinger11_R.frontfinsize = 2
	bFinger11_R.backfin = off
	bFinger11_R.backfinsize = 2
	bFinger11_R.parent = bFinger10_R
	BoneLayer.addNode bFinger11_R
	append BoneList bFinger11_R

	bFinger12_R = BoneSys.createBone posJntFinger12_R posJntFinger1E_R [0,1,0]
	bFinger12_R.name = "B_Finger12_R"
	bFinger12_R.transform = CtrlFinger12_R.transform
	bFinger12_R.width = 1
	bFinger12_R.height = 1
	bFinger12_R.Taper = 90
	bFinger12_R.sidefins = off
	bFinger12_R.sidefinssize = 2
	bFinger12_R.frontfin = off
	bFinger12_R.frontfinsize = 2
	bFinger12_R.backfin = off
	bFinger12_R.backfinsize = 2
	bFinger12_R.parent = bFinger11_R
	BoneLayer.addNode bFinger12_R
	append BoneList bFinger12_R

	effFinger1_R = BoneSys.createBone posJntFinger1E_R posJntFinger1E_R [0,1,0]
	effFinger1_R.name = "eff_Finger1_R"
	effFinger1_R.width = 0.5
	effFinger1_R.height = 0.5
	effFinger1_R.Taper = 90
	effFinger1_R.sidefins = off
	effFinger1_R.sidefinssize = 2
	effFinger1_R.frontfin = off
	effFinger1_R.frontfinsize = 2
	effFinger1_R.backfin = off
	effFinger1_R.backfinsize = 2
	effFinger1_R.length = 0.5
	effFinger1_R.parent = bFinger12_R
	effFinger1_R.rotation.controller.value = (quat 0 0 0 1)
	BoneLayer.addNode effFinger1_R
	append BoneList effFinger1_R
	----
	bFinger20_R = BoneSys.createBone posJntFinger20_R posJntFinger21_R [0,1,0]
	bFinger20_R.name = "B_Finger20_R"
	bFinger20_R.transform = CtrlFinger20_R.transform
	bFinger20_R.width = 1
	bFinger20_R.height = 1
	bFinger20_R.Taper = 90
	bFinger20_R.sidefins = off
	bFinger20_R.sidefinssize = 2
	bFinger20_R.frontfin = off
	bFinger20_R.frontfinsize = 2
	bFinger20_R.backfin = off
	bFinger20_R.backfinsize = 2
	bFinger20_R.parent = bHand_R
	BoneLayer.addNode bFinger20_R
	append BoneList bFinger20_R

	bFinger21_R = BoneSys.createBone posJntFinger21_R posJntFinger22_R [0,1,0]
	bFinger21_R.name = "B_Finger21_R"
	bFinger21_R.transform = CtrlFinger21_R.transform
	bFinger21_R.width = 1
	bFinger21_R.height = 1
	bFinger21_R.Taper = 90
	bFinger21_R.sidefins = off
	bFinger21_R.sidefinssize = 2
	bFinger21_R.frontfin = off
	bFinger21_R.frontfinsize = 2
	bFinger21_R.backfin = off
	bFinger21_R.backfinsize = 2
	bFinger21_R.parent = bFinger20_R
	BoneLayer.addNode bFinger21_R
	append BoneList bFinger21_R

	bFinger22_R = BoneSys.createBone posJntFinger22_R posJntFinger2E_R [0,1,0]
	bFinger22_R.name = "B_Finger22_R"
	bFinger22_R.transform = CtrlFinger22_R.transform
	bFinger22_R.width = 1
	bFinger22_R.height = 1
	bFinger22_R.Taper = 90
	bFinger22_R.sidefins = off
	bFinger22_R.sidefinssize = 2
	bFinger22_R.frontfin = off
	bFinger22_R.frontfinsize = 2
	bFinger22_R.backfin = off
	bFinger22_R.backfinsize = 2
	bFinger22_R.parent = bFinger21_R
	BoneLayer.addNode bFinger22_R
	append BoneList bFinger22_R

	effFinger2_R = BoneSys.createBone posJntFinger2E_R posJntFinger2E_R [0,1,0]
	effFinger2_R.name = "eff_Finger2_R"
	effFinger2_R.width = 0.5
	effFinger2_R.height = 0.5
	effFinger2_R.Taper = 90
	effFinger2_R.sidefins = off
	effFinger2_R.sidefinssize = 2
	effFinger2_R.frontfin = off
	effFinger2_R.frontfinsize = 2
	effFinger2_R.backfin = off
	effFinger2_R.backfinsize = 2
	effFinger2_R.length = 0.5
	effFinger2_R.parent = bFinger22_R
	effFinger2_R.rotation.controller.value = (quat 0 0 0 1)
	BoneLayer.addNode effFinger2_R
	append BoneList effFinger2_R
	----
	bFinger30_R = BoneSys.createBone posJntFinger30_R posJntFinger31_R [0,1,0]
	bFinger30_R.name = "B_Finger30_R"
	bFinger30_R.transform = CtrlFinger30_R.transform
	bFinger30_R.width = 1
	bFinger30_R.height = 1
	bFinger30_R.Taper = 90
	bFinger30_R.sidefins = off
	bFinger30_R.sidefinssize = 2
	bFinger30_R.frontfin = off
	bFinger30_R.frontfinsize = 2
	bFinger30_R.backfin = off
	bFinger30_R.backfinsize = 2
	bFinger30_R.parent = bHand_R
	BoneLayer.addNode bFinger30_R
	append BoneList bFinger30_R

	bFinger31_R = BoneSys.createBone posJntFinger31_R posJntFinger32_R [0,1,0]
	bFinger31_R.name = "B_Finger31_R"
	bFinger31_R.transform = CtrlFinger31_R.transform
	bFinger31_R.width = 1
	bFinger31_R.height = 1
	bFinger31_R.Taper = 90
	bFinger31_R.sidefins = off
	bFinger31_R.sidefinssize = 2
	bFinger31_R.frontfin = off
	bFinger31_R.frontfinsize = 2
	bFinger31_R.backfin = off
	bFinger31_R.backfinsize = 2
	bFinger31_R.parent = bFinger30_R
	BoneLayer.addNode bFinger31_R
	append BoneList bFinger31_R

	bFinger32_R = BoneSys.createBone posJntFinger32_R posJntFinger3E_R [0,1,0]
	bFinger32_R.name = "B_Finger32_R"
	bFinger32_R.transform = CtrlFinger32_R.transform
	bFinger32_R.width = 1
	bFinger32_R.height = 1
	bFinger32_R.Taper = 90
	bFinger32_R.sidefins = off
	bFinger32_R.sidefinssize = 2
	bFinger32_R.frontfin = off
	bFinger32_R.frontfinsize = 2
	bFinger32_R.backfin = off
	bFinger32_R.backfinsize = 2
	bFinger32_R.parent = bFinger31_R
	BoneLayer.addNode bFinger32_R
	append BoneList bFinger32_R

	effFinger3_R = BoneSys.createBone posJntFinger3E_R posJntFinger3E_R [0,1,0]
	effFinger3_R.name = "eff_Finger3_R"
	effFinger3_R.width = 0.5
	effFinger3_R.height = 0.5
	effFinger3_R.Taper = 90
	effFinger3_R.sidefins = off
	effFinger3_R.sidefinssize = 2
	effFinger3_R.frontfin = off
	effFinger3_R.frontfinsize = 2
	effFinger3_R.backfin = off
	effFinger3_R.backfinsize = 2
	effFinger3_R.length = 0.5
	effFinger3_R.parent = bFinger32_R
	effFinger3_R.rotation.controller.value = (quat 0 0 0 1)
	BoneLayer.addNode effFinger3_R
	append BoneList effFinger3_R
	----
	bFinger40_R = BoneSys.createBone posJntFinger40_R posJntFinger41_R [0,1,0]
	bFinger40_R.name = "B_Finger40_R"
	bFinger40_R.transform = CtrlFinger40_R.transform
	bFinger40_R.width = 1
	bFinger40_R.height = 1
	bFinger40_R.Taper = 90
	bFinger40_R.sidefins = off
	bFinger40_R.sidefinssize = 2
	bFinger40_R.frontfin = off
	bFinger40_R.frontfinsize = 2
	bFinger40_R.backfin = off
	bFinger40_R.backfinsize = 2
	bFinger40_R.parent = bHand_R
	BoneLayer.addNode bFinger40_R
	append BoneList bFinger40_R

	bFinger41_R = BoneSys.createBone posJntFinger41_R posJntFinger42_R [0,1,0]
	bFinger41_R.name = "B_Finger41_R"
	bFinger41_R.transform = CtrlFinger41_R.transform
	bFinger41_R.width = 1
	bFinger41_R.height = 1
	bFinger41_R.Taper = 90
	bFinger41_R.sidefins = off
	bFinger41_R.sidefinssize = 2
	bFinger41_R.frontfin = off
	bFinger41_R.frontfinsize = 2
	bFinger41_R.backfin = off
	bFinger41_R.backfinsize = 2
	bFinger41_R.parent = bFinger40_R
	BoneLayer.addNode bFinger41_R
	append BoneList bFinger41_R

	bFinger42_R = BoneSys.createBone posJntFinger42_R posJntFinger4E_R [0,1,0]
	bFinger42_R.name = "B_Finger42_R"
	bFinger42_R.transform = CtrlFinger42_R.transform
	bFinger42_R.width = 1
	bFinger42_R.height = 1
	bFinger42_R.Taper = 90
	bFinger42_R.sidefins = off
	bFinger42_R.sidefinssize = 2
	bFinger42_R.frontfin = off
	bFinger42_R.frontfinsize = 2
	bFinger42_R.backfin = off
	bFinger42_R.backfinsize = 2
	bFinger42_R.parent = bFinger41_R
	BoneLayer.addNode bFinger42_R
	append BoneList bFinger42_R

	effFinger4_R = BoneSys.createBone posJntFinger4E_R posJntFinger4E_R [0,1,0]
	effFinger4_R.name = "eff_Finger4_R"
	effFinger4_R.width = 0.5
	effFinger4_R.height = 0.5
	effFinger4_R.Taper = 90
	effFinger4_R.sidefins = off
	effFinger4_R.sidefinssize = 2
	effFinger4_R.frontfin = off
	effFinger4_R.frontfinsize = 2
	effFinger4_R.backfin = off
	effFinger4_R.backfinsize = 2
	effFinger4_R.length = 0.5
	effFinger4_R.parent = bFinger42_R
	effFinger4_R.rotation.controller.value = (quat 0 0 0 1)
	BoneLayer.addNode effFinger4_R
	append BoneList effFinger4_R
	----
	bAcrom_R = point name:"B_Acrom_R" size:6 cross:off Box:on wirecolor:(color 174 186 203) axistripod:off centermarker:off drawontop:off constantscreensize:off
	bAcrom_R.transform = jntAcrom_R.transform
	bAcrom_R.parent = bShoulder_R
	BoneLayer.addNode bAcrom_R

	bElbow_R = BoneSys.createBone posJntElbow_R posJntForeArm_R [0,1,0]
	bElbow_R.name = "B_Elbow_R"
	bElbow_R.transform = boneElbow_R.transform
	bElbow_R.width = 1
	bElbow_R.height = 1
	bElbow_R.Taper = 90
	bElbow_R.sidefins = off
	bElbow_R.sidefinssize = 2
	bElbow_R.frontfin = off
	bElbow_R.frontfinsize = 2
	bElbow_R.backfin = off
	bElbow_R.backfinsize = 2
	bElbow_R.parent = bUpperArm_R
	BoneLayer.addNode bElbow_R
	append BoneList bElbow_R

	bUpperArmTw1_R = BoneSys.createBone posJntUpperArmTw1_R posJntUpperArmTw2_R [0,1,0]
	bUpperArmTw1_R.name = "B_UpperArmTw1_R"
	bUpperArmTw1_R.transform = UpperArmTwistBoneList_R[2].transform
	bUpperArmTw1_R.width = 4
	bUpperArmTw1_R.height = 4
	bUpperArmTw1_R.Taper = 30
	bUpperArmTw1_R.sidefins = off
	bUpperArmTw1_R.sidefinssize = 2
	bUpperArmTw1_R.frontfin = off
	bUpperArmTw1_R.frontfinsize = 2
	bUpperArmTw1_R.backfin = off
	bUpperArmTw1_R.backfinsize = 2
	bUpperArmTw1_R.parent = bUpperArm_R
	BoneLayer.addNode bUpperArmTw1_R
	append BoneList bUpperArmTw1_R

	bUpperArmTw2_R = BoneSys.createBone posJntUpperArmTw2_R posJntUpperArmTw3_R [0,1,0]
	bUpperArmTw2_R.name = "B_UpperArmTw2_R"
	bUpperArmTw2_R.transform = UpperArmTwistBoneList_R[3].transform
	bUpperArmTw2_R.width = 4
	bUpperArmTw2_R.height = 4
	bUpperArmTw2_R.Taper = 30
	bUpperArmTw2_R.sidefins = off
	bUpperArmTw2_R.sidefinssize = 2
	bUpperArmTw2_R.frontfin = off
	bUpperArmTw2_R.frontfinsize = 2
	bUpperArmTw2_R.backfin = off
	bUpperArmTw2_R.backfinsize = 2
	bUpperArmTw2_R.parent = bUpperArm_R
	BoneLayer.addNode bUpperArmTw2_R
	append BoneList bUpperArmTw2_R

	bUpperArmTw3_R = BoneSys.createBone posJntUpperArmTw3_R posJntElbow_R [0,1,0]
	bUpperArmTw3_R.name = "B_UpperArmTw3_R"
	bUpperArmTw3_R.transform = UpperArmTwistBoneList_R[4].transform
	bUpperArmTw3_R.width = 4
	bUpperArmTw3_R.height = 4
	bUpperArmTw3_R.Taper = 30
	bUpperArmTw3_R.sidefins = off
	bUpperArmTw3_R.sidefinssize = 2
	bUpperArmTw3_R.frontfin = off
	bUpperArmTw3_R.frontfinsize = 2
	bUpperArmTw3_R.backfin = off
	bUpperArmTw3_R.backfinsize = 2
	bUpperArmTw3_R.parent = bUpperArm_R
	BoneLayer.addNode bUpperArmTw3_R
	append BoneList bUpperArmTw3_R

	----
	bForeArmTw1_R = BoneSys.createBone posJntForeArmTw1_R posJntForeArmTw2_R [0,1,0]
	bForeArmTw1_R.name = "B_ForeArmTw1_R"
	bForeArmTw1_R.transform = ForeArmTwistBoneList_R[2].transform
	bForeArmTw1_R.width = 4
	bForeArmTw1_R.height = 4
	bForeArmTw1_R.Taper = 30
	bForeArmTw1_R.sidefins = off
	bForeArmTw1_R.sidefinssize = 2
	bForeArmTw1_R.frontfin = off
	bForeArmTw1_R.frontfinsize = 2
	bForeArmTw1_R.backfin = off
	bForeArmTw1_R.backfinsize = 2
	bForeArmTw1_R.parent = bForeArm_R
	BoneLayer.addNode bForeArmTw1_R
	append BoneList bForeArmTw1_R

	bForeArmTw2_R = BoneSys.createBone posJntForeArmTw2_R posJntForeArmTw3_R [0,1,0]
	bForeArmTw2_R.name = "B_ForeArmTw2_R"
	bForeArmTw2_R.transform = ForeArmTwistBoneList_R[3].transform
	bForeArmTw2_R.width = 4
	bForeArmTw2_R.height = 4
	bForeArmTw2_R.Taper = 30
	bForeArmTw2_R.sidefins = off
	bForeArmTw2_R.sidefinssize = 2
	bForeArmTw2_R.frontfin = off
	bForeArmTw2_R.frontfinsize = 2
	bForeArmTw2_R.backfin = off
	bForeArmTw2_R.backfinsize = 2
	bForeArmTw2_R.parent = bForeArm_R
	BoneLayer.addNode bForeArmTw2_R
	append BoneList bForeArmTw2_R

	bForeArmTw3_R = BoneSys.createBone posJntForeArmTw3_R posJntHand_R [0,1,0]
	bForeArmTw3_R.name = "B_ForeArmTw3_R"
	bForeArmTw3_R.transform = ForeArmTwistBoneList_R[4].transform
	bForeArmTw3_R.width = 3
	bForeArmTw3_R.height = 3
	bForeArmTw3_R.Taper = 50
	bForeArmTw3_R.sidefins = off
	bForeArmTw3_R.sidefinssize = 2
	bForeArmTw3_R.frontfin = off
	bForeArmTw3_R.frontfinsize = 2
	bForeArmTw3_R.backfin = off
	bForeArmTw3_R.backfinsize = 2
	bForeArmTw3_R.parent = bForeArm_R
	BoneLayer.addNode bForeArmTw3_R
	append BoneList bForeArmTw3_R

	bWrist_R = point name:"B_Wrist_R" size:5 cross:off Box:on wirecolor:(color 174 186 203) axistripod:off centermarker:off drawontop:off constantscreensize:off
	bWrist_R.transform = jntWrist_R.transform
	bWrist_R.parent = bForeArm_R
	BoneLayer.addNode bWrist_R
--------Left Arm---------------
	bShoulder_L = BoneSys.createBone posJntShoulder_L posJntUpperArm_L [0,1,0]
	bShoulder_L.name = "B_Shoulder_L"
	bShoulder_L.transform = getSymMtx ctrlShoulder_R.transform "z"--ctrlShoulder_L.transform
	bShoulder_L.width = 5.5
	bShoulder_L.height = 5.5
	bShoulder_L.Taper = 90
	bShoulder_L.sidefins = off
	bShoulder_L.sidefinssize = 2
	bShoulder_L.frontfin = off
	bShoulder_L.frontfinsize = 2
	bShoulder_L.backfin = off
	bShoulder_L.backfinsize = 2
	bShoulder_L.parent = Chest1InvScl_Sh
	BoneLayer.addNode bShoulder_L
	append BoneList bShoulder_L

	bUpperArm_L = BoneSys.createBone posJntUpperArm_L posJntElbow_L [0,1,0]
	bUpperArm_L.name = "B_UpperArm_L"
	bUpperArm_L.transform = UpperArmTwistBoneList_L[1].transform
	bUpperArm_L.width = 4
	bUpperArm_L.height = 4
	bUpperArm_L.Taper = 90
	bUpperArm_L.sidefins = off
	bUpperArm_L.sidefinssize = 2
	bUpperArm_L.frontfin = off
	bUpperArm_L.frontfinsize = 2
	bUpperArm_L.backfin = off
	bUpperArm_L.backfinsize = 2
	bUpperArm_L.parent = bShoulder_L
	BoneLayer.addNode bUpperArm_L
	append BoneList bUpperArm_L

	bForeArm_L = BoneSys.createBone posJntForeArm_L posJntHand_L [0,1,0]
	bForeArm_L.name = "B_ForeArm_L"
	bForeArm_L.transform = ForeArmTwistBoneList_L[1].transform
	bForeArm_L.width = 4
	bForeArm_L.height = 4
	bForeArm_L.Taper = 90
	bForeArm_L.sidefins = off
	bForeArm_L.sidefinssize = 2
	bForeArm_L.frontfin = off
	bForeArm_L.frontfinsize = 2
	bForeArm_L.backfin = off
	bForeArm_L.backfinsize = 2
	bForeArm_L.parent = bUpperArm_L
	BoneLayer.addNode bForeArm_L
	append BoneList bForeArm_L

	bHand_L = BoneSys.createBone posJntHand_L posJntHand_L [0,1,0]
	bHand_L.name = "B_Hand_L"
	bHand_L.transform = boneHand_L.transform
	bHand_L.width = 3
	bHand_L.height = 3
	bHand_L.Taper = 90
	bHand_L.sidefins = off
	bHand_L.sidefinssize = 2
	bHand_L.frontfin = off
	bHand_L.frontfinsize = 2
	bHand_L.backfin = off
	bHand_L.backfinsize = 2
	bHand_L.parent = bForeArm_L
	bHand_L.length = boneHand_L.length
	BoneLayer.addNode bHand_L
	append BoneList bHand_L

	bFinger00_L = BoneSys.createBone posJntFinger00_L posJntFinger01_L [0,1,0]
	bFinger00_L.name = "B_Finger00_L"
	bFinger00_L.transform = CtrlFinger00_L.transform
	bFinger00_L.width = 1
	bFinger00_L.height = 1
	bFinger00_L.Taper = 90
	bFinger00_L.sidefins = off
	bFinger00_L.sidefinssize = 2
	bFinger00_L.frontfin = off
	bFinger00_L.frontfinsize = 2
	bFinger00_L.backfin = off
	bFinger00_L.backfinsize = 2
	bFinger00_L.parent = bHand_L
	BoneLayer.addNode bFinger00_L
	append BoneList bFinger00_L

	bFinger01_L = BoneSys.createBone posJntFinger01_L posJntFinger02_L [0,1,0]
	bFinger01_L.name = "B_Finger01_L"
	bFinger01_L.transform = CtrlFinger01_L.transform
	bFinger01_L.width = 1
	bFinger01_L.height = 1
	bFinger01_L.Taper = 90
	bFinger01_L.sidefins = off
	bFinger01_L.sidefinssize = 2
	bFinger01_L.frontfin = off
	bFinger01_L.frontfinsize = 2
	bFinger01_L.backfin = off
	bFinger01_L.backfinsize = 2
	bFinger01_L.parent = bFinger00_L
	BoneLayer.addNode bFinger01_L
	append BoneList bFinger01_L

	bFinger02_L = BoneSys.createBone posJntFinger02_L posJntFinger0E_L [0,1,0]
	bFinger02_L.name = "B_Finger02_L"
	bFinger02_L.transform = CtrlFinger02_L.transform
	bFinger02_L.width = 1
	bFinger02_L.height = 1
	bFinger02_L.Taper = 90
	bFinger02_L.sidefins = off
	bFinger02_L.sidefinssize = 2
	bFinger02_L.frontfin = off
	bFinger02_L.frontfinsize = 2
	bFinger02_L.backfin = off
	bFinger02_L.backfinsize = 2
	bFinger02_L.parent = bFinger01_L
	BoneLayer.addNode bFinger02_L
	append BoneList bFinger02_L

	effFinger0_L = BoneSys.createBone posJntFinger0E_L posJntFinger0E_L [0,1,0]
	effFinger0_L.name = "eff_Finger0_L"
	effFinger0_L.width = 0.5
	effFinger0_L.height = 0.5
	effFinger0_L.Taper = 90
	effFinger0_L.sidefins = off
	effFinger0_L.sidefinssize = 2
	effFinger0_L.frontfin = off
	effFinger0_L.frontfinsize = 2
	effFinger0_L.backfin = off
	effFinger0_L.backfinsize = 2
	effFinger0_L.length = 0.5
	effFinger0_L.parent = bFinger02_L
	effFinger0_L.rotation.controller.value = (quat 0 0 0 1)
	BoneLayer.addNode effFinger0_L
	append BoneList effFinger0_L
	----
	bFinger10_L = BoneSys.createBone posJntFinger10_L posJntFinger11_L [0,1,0]
	bFinger10_L.name = "B_Finger10_L"
	bFinger10_L.transform = CtrlFinger10_L.transform
	bFinger10_L.width = 1
	bFinger10_L.height = 1
	bFinger10_L.Taper = 90
	bFinger10_L.sidefins = off
	bFinger10_L.sidefinssize = 2
	bFinger10_L.frontfin = off
	bFinger10_L.frontfinsize = 2
	bFinger10_L.backfin = off
	bFinger10_L.backfinsize = 2
	bFinger10_L.parent = bHand_L
	BoneLayer.addNode bFinger10_L
	append BoneList bFinger10_L

	bFinger11_L = BoneSys.createBone posJntFinger11_L posJntFinger12_L [0,1,0]
	bFinger11_L.name = "B_Finger11_L"
	bFinger11_L.transform = CtrlFinger11_L.transform
	bFinger11_L.width = 1
	bFinger11_L.height = 1
	bFinger11_L.Taper = 90
	bFinger11_L.sidefins = off
	bFinger11_L.sidefinssize = 2
	bFinger11_L.frontfin = off
	bFinger11_L.frontfinsize = 2
	bFinger11_L.backfin = off
	bFinger11_L.backfinsize = 2
	bFinger11_L.parent = bFinger10_L
	BoneLayer.addNode bFinger11_L
	append BoneList bFinger11_L

	bFinger12_L = BoneSys.createBone posJntFinger12_L posJntFinger1E_L [0,1,0]
	bFinger12_L.name = "B_Finger12_L"
	bFinger12_L.transform = CtrlFinger12_L.transform
	bFinger12_L.width = 1
	bFinger12_L.height = 1
	bFinger12_L.Taper = 90
	bFinger12_L.sidefins = off
	bFinger12_L.sidefinssize = 2
	bFinger12_L.frontfin = off
	bFinger12_L.frontfinsize = 2
	bFinger12_L.backfin = off
	bFinger12_L.backfinsize = 2
	bFinger12_L.parent = bFinger11_L
	BoneLayer.addNode bFinger12_L
	append BoneList bFinger12_L

	effFinger1_L = BoneSys.createBone posJntFinger1E_L posJntFinger1E_L [0,1,0]
	effFinger1_L.name = "eff_Finger1_L"
	effFinger1_L.width = 0.5
	effFinger1_L.height = 0.5
	effFinger1_L.Taper = 90
	effFinger1_L.sidefins = off
	effFinger1_L.sidefinssize = 2
	effFinger1_L.frontfin = off
	effFinger1_L.frontfinsize = 2
	effFinger1_L.backfin = off
	effFinger1_L.backfinsize = 2
	effFinger1_L.length = 0.5
	effFinger1_L.parent = bFinger12_L
	effFinger1_L.rotation.controller.value = (quat 0 0 0 1)
	BoneLayer.addNode effFinger1_L
	append BoneList effFinger1_L
	----
	bFinger20_L = BoneSys.createBone posJntFinger20_L posJntFinger21_L [0,1,0]
	bFinger20_L.name = "B_Finger20_L"
	bFinger20_L.transform = CtrlFinger20_L.transform
	bFinger20_L.width = 1
	bFinger20_L.height = 1
	bFinger20_L.Taper = 90
	bFinger20_L.sidefins = off
	bFinger20_L.sidefinssize = 2
	bFinger20_L.frontfin = off
	bFinger20_L.frontfinsize = 2
	bFinger20_L.backfin = off
	bFinger20_L.backfinsize = 2
	bFinger20_L.parent = bHand_L
	BoneLayer.addNode bFinger20_L
	append BoneList bFinger20_L

	bFinger21_L = BoneSys.createBone posJntFinger21_L posJntFinger22_L [0,1,0]
	bFinger21_L.name = "B_Finger21_L"
	bFinger21_L.transform = CtrlFinger21_L.transform
	bFinger21_L.width = 1
	bFinger21_L.height = 1
	bFinger21_L.Taper = 90
	bFinger21_L.sidefins = off
	bFinger21_L.sidefinssize = 2
	bFinger21_L.frontfin = off
	bFinger21_L.frontfinsize = 2
	bFinger21_L.backfin = off
	bFinger21_L.backfinsize = 2
	bFinger21_L.parent = bFinger20_L
	BoneLayer.addNode bFinger21_L
	append BoneList bFinger21_L

	bFinger22_L = BoneSys.createBone posJntFinger22_L posJntFinger2E_L [0,1,0]
	bFinger22_L.name = "B_Finger22_L"
	bFinger22_L.transform = CtrlFinger22_L.transform
	bFinger22_L.width = 1
	bFinger22_L.height = 1
	bFinger22_L.Taper = 90
	bFinger22_L.sidefins = off
	bFinger22_L.sidefinssize = 2
	bFinger22_L.frontfin = off
	bFinger22_L.frontfinsize = 2
	bFinger22_L.backfin = off
	bFinger22_L.backfinsize = 2
	bFinger22_L.parent = bFinger21_L
	BoneLayer.addNode bFinger22_L
	append BoneList bFinger22_L

	effFinger2_L = BoneSys.createBone posJntFinger2E_L posJntFinger2E_L [0,1,0]
	effFinger2_L.name = "eff_Finger2_L"
	effFinger2_L.width = 0.5
	effFinger2_L.height = 0.5
	effFinger2_L.Taper = 90
	effFinger2_L.sidefins = off
	effFinger2_L.sidefinssize = 2
	effFinger2_L.frontfin = off
	effFinger2_L.frontfinsize = 2
	effFinger2_L.backfin = off
	effFinger2_L.backfinsize = 2
	effFinger2_L.length = 0.5
	effFinger2_L.parent = bFinger22_L
	effFinger2_L.rotation.controller.value = (quat 0 0 0 1)
	BoneLayer.addNode effFinger2_L
	append BoneList effFinger2_L
	----
	bFinger30_L = BoneSys.createBone posJntFinger30_L posJntFinger31_L [0,1,0]
	bFinger30_L.name = "B_Finger30_L"
	bFinger30_L.transform = CtrlFinger30_L.transform
	bFinger30_L.width = 1
	bFinger30_L.height = 1
	bFinger30_L.Taper = 90
	bFinger30_L.sidefins = off
	bFinger30_L.sidefinssize = 2
	bFinger30_L.frontfin = off
	bFinger30_L.frontfinsize = 2
	bFinger30_L.backfin = off
	bFinger30_L.backfinsize = 2
	bFinger30_L.parent = bHand_L
	BoneLayer.addNode bFinger30_L
	append BoneList bFinger30_L

	bFinger31_L = BoneSys.createBone posJntFinger31_L posJntFinger32_L [0,1,0]
	bFinger31_L.name = "B_Finger31_L"
	bFinger31_L.transform = CtrlFinger31_L.transform
	bFinger31_L.width = 1
	bFinger31_L.height = 1
	bFinger31_L.Taper = 90
	bFinger31_L.sidefins = off
	bFinger31_L.sidefinssize = 2
	bFinger31_L.frontfin = off
	bFinger31_L.frontfinsize = 2
	bFinger31_L.backfin = off
	bFinger31_L.backfinsize = 2
	bFinger31_L.parent = bFinger30_L
	BoneLayer.addNode bFinger31_L
	append BoneList bFinger31_L

	bFinger32_L = BoneSys.createBone posJntFinger32_L posJntFinger3E_L [0,1,0]
	bFinger32_L.name = "B_Finger32_L"
	bFinger32_L.transform = CtrlFinger32_L.transform
	bFinger32_L.width = 1
	bFinger32_L.height = 1
	bFinger32_L.Taper = 90
	bFinger32_L.sidefins = off
	bFinger32_L.sidefinssize = 2
	bFinger32_L.frontfin = off
	bFinger32_L.frontfinsize = 2
	bFinger32_L.backfin = off
	bFinger32_L.backfinsize = 2
	bFinger32_L.parent = bFinger31_L
	BoneLayer.addNode bFinger32_L
	append BoneList bFinger32_L

	effFinger3_L = BoneSys.createBone posJntFinger3E_L posJntFinger3E_L [0,1,0]
	effFinger3_L.name = "eff_Finger3_L"
	effFinger3_L.width = 0.5
	effFinger3_L.height = 0.5
	effFinger3_L.Taper = 90
	effFinger3_L.sidefins = off
	effFinger3_L.sidefinssize = 2
	effFinger3_L.frontfin = off
	effFinger3_L.frontfinsize = 2
	effFinger3_L.backfin = off
	effFinger3_L.backfinsize = 2
	effFinger3_L.length = 0.5
	effFinger3_L.parent = bFinger32_L
	effFinger3_L.rotation.controller.value = (quat 0 0 0 1)
	BoneLayer.addNode effFinger3_L
	append BoneList effFinger3_L
	----
	bFinger40_L = BoneSys.createBone posJntFinger40_L posJntFinger41_L [0,1,0]
	bFinger40_L.name = "B_Finger40_L"
	bFinger40_L.transform = CtrlFinger40_L.transform
	bFinger40_L.width = 1
	bFinger40_L.height = 1
	bFinger40_L.Taper = 90
	bFinger40_L.sidefins = off
	bFinger40_L.sidefinssize = 2
	bFinger40_L.frontfin = off
	bFinger40_L.frontfinsize = 2
	bFinger40_L.backfin = off
	bFinger40_L.backfinsize = 2
	bFinger40_L.parent = bHand_L
	BoneLayer.addNode bFinger40_L
	append BoneList bFinger40_L

	bFinger41_L = BoneSys.createBone posJntFinger41_L posJntFinger42_L [0,1,0]
	bFinger41_L.name = "B_Finger41_L"
	bFinger41_L.transform = CtrlFinger41_L.transform
	bFinger41_L.width = 1
	bFinger41_L.height = 1
	bFinger41_L.Taper = 90
	bFinger41_L.sidefins = off
	bFinger41_L.sidefinssize = 2
	bFinger41_L.frontfin = off
	bFinger41_L.frontfinsize = 2
	bFinger41_L.backfin = off
	bFinger41_L.backfinsize = 2
	bFinger41_L.parent = bFinger40_L
	BoneLayer.addNode bFinger41_L
	append BoneList bFinger41_L

	bFinger42_L = BoneSys.createBone posJntFinger42_L posJntFinger4E_L [0,1,0]
	bFinger42_L.name = "B_Finger42_L"
	bFinger42_L.transform = CtrlFinger42_L.transform
	bFinger42_L.width = 1
	bFinger42_L.height = 1
	bFinger42_L.Taper = 90
	bFinger42_L.sidefins = off
	bFinger42_L.sidefinssize = 2
	bFinger42_L.frontfin = off
	bFinger42_L.frontfinsize = 2
	bFinger42_L.backfin = off
	bFinger42_L.backfinsize = 2
	bFinger42_L.parent = bFinger41_L
	BoneLayer.addNode bFinger42_L
	append BoneList bFinger42_L

	effFinger4_L = BoneSys.createBone posJntFinger4E_L posJntFinger4E_L [0,1,0]
	effFinger4_L.name = "eff_Finger4_L"
	effFinger4_L.width = 0.5
	effFinger4_L.height = 0.5
	effFinger4_L.Taper = 90
	effFinger4_L.sidefins = off
	effFinger4_L.sidefinssize = 2
	effFinger4_L.frontfin = off
	effFinger4_L.frontfinsize = 2
	effFinger4_L.backfin = off
	effFinger4_L.backfinsize = 2
	effFinger4_L.length = 0.5
	effFinger4_L.parent = bFinger42_L
	effFinger4_L.rotation.controller.value = (quat 0 0 0 1)
	BoneLayer.addNode effFinger4_L
	append BoneList effFinger4_L
	----
	bAcrom_L = point name:"B_Acrom_L" size:6 cross:off Box:on wirecolor:(color 174 186 203) axistripod:off centermarker:off drawontop:off constantscreensize:off
	bAcrom_L.transform = jntAcrom_L.transform
	bAcrom_L.parent = bShoulder_L
	BoneLayer.addNode bAcrom_L

	bElbow_L = BoneSys.createBone posJntElbow_L posJntForeArm_L [0,1,0]
	bElbow_L.name = "B_Elbow_L"
	bElbow_L.transform = boneElbow_L.transform
	bElbow_L.width = 1
	bElbow_L.height = 1
	bElbow_L.Taper = 90
	bElbow_L.sidefins = off
	bElbow_L.sidefinssize = 2
	bElbow_L.frontfin = off
	bElbow_L.frontfinsize = 2
	bElbow_L.backfin = off
	bElbow_L.backfinsize = 2
	bElbow_L.parent = bUpperArm_L
	BoneLayer.addNode bElbow_L
	append BoneList bElbow_L

	bUpperArmTw1_L = BoneSys.createBone posJntUpperArmTw1_L posJntUpperArmTw2_L [0,1,0]
	bUpperArmTw1_L.name = "B_UpperArmTw1_L"
	bUpperArmTw1_L.transform = UpperArmTwistBoneList_L[2].transform
	bUpperArmTw1_L.width = 4
	bUpperArmTw1_L.height = 4
	bUpperArmTw1_L.Taper = 30
	bUpperArmTw1_L.sidefins = off
	bUpperArmTw1_L.sidefinssize = 2
	bUpperArmTw1_L.frontfin = off
	bUpperArmTw1_L.frontfinsize = 2
	bUpperArmTw1_L.backfin = off
	bUpperArmTw1_L.backfinsize = 2
	bUpperArmTw1_L.parent = bUpperArm_L
	BoneLayer.addNode bUpperArmTw1_L
	append BoneList bUpperArmTw1_L

	bUpperArmTw2_L = BoneSys.createBone posJntUpperArmTw2_L posJntUpperArmTw3_L [0,1,0]
	bUpperArmTw2_L.name = "B_UpperArmTw2_L"
	bUpperArmTw2_L.transform = UpperArmTwistBoneList_L[3].transform
	bUpperArmTw2_L.width = 4
	bUpperArmTw2_L.height = 4
	bUpperArmTw2_L.Taper = 30
	bUpperArmTw2_L.sidefins = off
	bUpperArmTw2_L.sidefinssize = 2
	bUpperArmTw2_L.frontfin = off
	bUpperArmTw2_L.frontfinsize = 2
	bUpperArmTw2_L.backfin = off
	bUpperArmTw2_L.backfinsize = 2
	bUpperArmTw2_L.parent = bUpperArm_L
	BoneLayer.addNode bUpperArmTw2_L
	append BoneList bUpperArmTw2_L

	bUpperArmTw3_L = BoneSys.createBone posJntUpperArmTw3_L posJntElbow_L [0,1,0]
	bUpperArmTw3_L.name = "B_UpperArmTw3_L"
	bUpperArmTw3_L.transform = UpperArmTwistBoneList_L[4].transform
	bUpperArmTw3_L.width = 4
	bUpperArmTw3_L.height = 4
	bUpperArmTw3_L.Taper = 30
	bUpperArmTw3_L.sidefins = off
	bUpperArmTw3_L.sidefinssize = 2
	bUpperArmTw3_L.frontfin = off
	bUpperArmTw3_L.frontfinsize = 2
	bUpperArmTw3_L.backfin = off
	bUpperArmTw3_L.backfinsize = 2
	bUpperArmTw3_L.parent = bUpperArm_L
	BoneLayer.addNode bUpperArmTw3_L
	append BoneList bUpperArmTw3_L

	----
	bForeArmTw1_L = BoneSys.createBone posJntForeArmTw1_L posJntForeArmTw2_L [0,1,0]
	bForeArmTw1_L.name = "B_ForeArmTw1_L"
	bForeArmTw1_L.transform = ForeArmTwistBoneList_L[2].transform
	bForeArmTw1_L.width = 4
	bForeArmTw1_L.height = 4
	bForeArmTw1_L.Taper = 30
	bForeArmTw1_L.sidefins = off
	bForeArmTw1_L.sidefinssize = 2
	bForeArmTw1_L.frontfin = off
	bForeArmTw1_L.frontfinsize = 2
	bForeArmTw1_L.backfin = off
	bForeArmTw1_L.backfinsize = 2
	bForeArmTw1_L.parent = bForeArm_L
	BoneLayer.addNode bForeArmTw1_L
	append BoneList bForeArmTw1_L

	bForeArmTw2_L = BoneSys.createBone posJntForeArmTw2_L posJntForeArmTw3_L [0,1,0]
	bForeArmTw2_L.name = "B_ForeArmTw2_L"
	bForeArmTw2_L.transform = ForeArmTwistBoneList_L[3].transform
	bForeArmTw2_L.width = 4
	bForeArmTw2_L.height = 4
	bForeArmTw2_L.Taper = 30
	bForeArmTw2_L.sidefins = off
	bForeArmTw2_L.sidefinssize = 2
	bForeArmTw2_L.frontfin = off
	bForeArmTw2_L.frontfinsize = 2
	bForeArmTw2_L.backfin = off
	bForeArmTw2_L.backfinsize = 2
	bForeArmTw2_L.parent = bForeArm_L
	BoneLayer.addNode bForeArmTw2_L
	append BoneList bForeArmTw2_L

	bForeArmTw3_L = BoneSys.createBone posJntForeArmTw3_L posJntHand_L [0,1,0]
	bForeArmTw3_L.name = "B_ForeArmTw3_L"
	bForeArmTw3_L.transform = ForeArmTwistBoneList_L[4].transform
	bForeArmTw3_L.width = 3
	bForeArmTw3_L.height = 3
	bForeArmTw3_L.Taper = 50
	bForeArmTw3_L.sidefins = off
	bForeArmTw3_L.sidefinssize = 2
	bForeArmTw3_L.frontfin = off
	bForeArmTw3_L.frontfinsize = 2
	bForeArmTw3_L.backfin = off
	bForeArmTw3_L.backfinsize = 2
	bForeArmTw3_L.parent = bForeArm_L
	BoneLayer.addNode bForeArmTw3_L
	append BoneList bForeArmTw3_L

	bWrist_L = point name:"B_Wrist_L" size:5 cross:off Box:on wirecolor:(color 174 186 203) axistripod:off centermarker:off drawontop:off constantscreensize:off
	bWrist_L.transform = jntWrist_L.transform
	bWrist_L.parent = bForeArm_L
	BoneLayer.addNode bWrist_L
---------Bust---------------------
	bBust0_R = BoneSys.createBone posBust0_R posBust1_R [0,1,0]
	bBust0_R.name = "B_Bust0_R"
	bBust0_R.transform = boneBust0_R.transform
	bBust0_R.parent = Chest0InvScl
	bBust0_R.width = 2
	bBust0_R.height = 2
	bBust0_R.Taper = 90
	bBust0_R.sidefins = off
	bBust0_R.sidefinssize = 2
	bBust0_R.frontfin = off
	bBust0_R.frontfinsize = 2
	bBust0_R.backfin = off
	bBust0_R.backfinsize = 2
	BoneLayer.addNode bBust0_R

	bBust1_R = BoneSys.createBone posBust1_R posBustE_R [0,1,0]
	bBust1_R.name = "B_Bust1_R"
	bBust1_R.transform = boneBust1_R.transform
	bBust1_R.parent = bBust0_R
	bBust1_R.width = 2
	bBust1_R.height = 2
	bBust1_R.Taper = 90
	bBust1_R.sidefins = off
	bBust1_R.sidefinssize = 2
	bBust1_R.frontfin = off
	bBust1_R.frontfinsize = 2
	bBust1_R.backfin = off
	bBust1_R.backfinsize = 2
	BoneLayer.addNode bBust1_R

	effBust_R = BoneSys.createBone posBustE_R posBustE_R [0,1,0]
	effBust_R.name = "eff_Bust_R"
	effBust_R.parent = bBust1_R
	effBust_R.rotation.controller.value = (quat 0 0 0 1)
	effBust_R.length = 0.5
	effBust_R.width = 0.5
	effBust_R.height = 0.5
	effBust_R.Taper = 90
	effBust_R.sidefins = off
	effBust_R.sidefinssize = 2
	effBust_R.frontfin = off
	effBust_R.frontfinsize = 2
	effBust_R.backfin = off
	effBust_R.backfinsize = 2
	BoneLayer.addNode effBust_R

	-----
	bBust0_L = BoneSys.createBone posBust0_L posBust1_L [0,1,0]
	bBust0_L.name = "B_Bust0_L"
	bBust0_L.transform = boneBust0_L.transform
	bBust0_L.parent = Chest0InvScl
	bBust0_L.width = 2
	bBust0_L.height = 2
	bBust0_L.Taper = 90
	bBust0_L.sidefins = off
	bBust0_L.sidefinssize = 2
	bBust0_L.frontfin = off
	bBust0_L.frontfinsize = 2
	bBust0_L.backfin = off
	bBust0_L.backfinsize = 2
	BoneLayer.addNode bBust0_L

	bBust1_L = BoneSys.createBone posBust1_L posBustE_L [0,1,0]
	bBust1_L.name = "B_Bust1_L"
	bBust1_L.transform = boneBust1_L.transform
	bBust1_L.parent = bBust0_L
	bBust1_L.width = 2
	bBust1_L.height = 2
	bBust1_L.Taper = 90
	bBust1_L.sidefins = off
	bBust1_L.sidefinssize = 2
	bBust1_L.frontfin = off
	bBust1_L.frontfinsize = 2
	bBust1_L.backfin = off
	bBust1_L.backfinsize = 2
	BoneLayer.addNode bBust1_L

	effBust_L = BoneSys.createBone posBustE_L posBustE_L [0,1,0]
	effBust_L.name = "eff_Bust_L"
	effBust_L.parent = bBust1_L
	effBust_L.rotation.controller.value = (quat 0 0 0 1)
	effBust_L.length = 0.5
	effBust_L.width = 0.5
	effBust_L.height = 0.5
	effBust_L.Taper = 90
	effBust_L.sidefins = off
	effBust_L.sidefinssize = 2
	effBust_L.frontfin = off
	effBust_L.frontfinsize = 2
	effBust_L.backfin = off
	effBust_L.backfinsize = 2
	BoneLayer.addNode effBust_L
----------TeresMajor---------------------
	bTeresMajor_R = BoneSys.createBone posTeresMajor1_R posTeresMajor2_R [0,1,0]
	bTeresMajor_R.name = "B_TeresMajor_R"
	bTeresMajor_R.transform = boneTeresMajor_R.transform
	bTeresMajor_R.parent = Chest1InvScl_Tm
	bTeresMajor_R.width = 1.2
	bTeresMajor_R.height = 1.2
	bTeresMajor_R.Taper = 90
	bTeresMajor_R.sidefins = off
	bTeresMajor_R.sidefinssize = 2
	bTeresMajor_R.frontfin = off
	bTeresMajor_R.frontfinsize = 2
	bTeresMajor_R.backfin = off
	bTeresMajor_R.backfinsize = 2
	BoneLayer.addNode bTeresMajor_R

	bTeresMajor_L = BoneSys.createBone posTeresMajor1_L posTeresMajor2_L [0,1,0]
	bTeresMajor_L.name = "B_TeresMajor_L"
	bTeresMajor_L.transform = boneTeresMajor_L.transform
	bTeresMajor_L.parent = Chest1InvScl_Tm
	bTeresMajor_L.width = 1.2
	bTeresMajor_L.height = 1.2
	bTeresMajor_L.Taper = 90
	bTeresMajor_L.sidefins = off
	bTeresMajor_L.sidefinssize = 2
	bTeresMajor_L.frontfin = off
	bTeresMajor_L.frontfinsize = 2
	bTeresMajor_L.backfin = off
	bTeresMajor_L.backfinsize = 2
	BoneLayer.addNode bTeresMajor_L
----------Global setting--------------------
	for b in BoneList do (
		b.boneFreezeLength	= false
		b.boneAutoAlign		= false
		b.boneAutoAlign		= false
		b.boneScaleType		= #none
	)

	bNeck1.boneScaleType=#scale
	bNeck2.boneScaleType=#scale
-----------Transform connect-----------------

	bRoot.pos.controller = Position_Constraint()
	bRoot.pos.controller.appendtarget CtrlRootMotion 50
	bRoot.rotation.controller = Orientation_Constraint()
	bRoot.rotation.controller.appendtarget CtrlRootMotion 50

	bHip.pos.controller = Position_Constraint()
	bHip.pos.controller.appendtarget ctrlHip 50
	bHip.rotation.controller = Orientation_Constraint()
	bHip.rotation.controller.appendtarget ctrlHip 50
	bHip.scale.controller = scale_script()
-- 	bHip.scale.controller.IScriptCtrl.AddNode "target" ctrlHip
	scriptStr = "[1,1,1]"
	bHip.scale.controller.IScriptCtrl.SetExpression scriptStr

	HipInvScl0.scale.controller = scale_script()
	HipInvScl0.scale.controller.IScriptCtrl.AddNode "Parent" bHip
	scriptStr = "1.0 / Parent.scale.controller.value"
	HipInvScl0.scale.controller.IScriptCtrl.SetExpression scriptStr

	HipInvScl.scale.controller = scale_script()
	HipInvScl.scale.controller.IScriptCtrl.AddNode "Parent" bHip
	scriptStr = "1.0 / Parent.scale.controller.value"
	HipInvScl.scale.controller.IScriptCtrl.SetExpression scriptStr

	--bWaist.pos.controller = Position_Constraint()
	--bWaist.pos.controller.appendtarget pySpine2 50
	bWaist.rotation.controller = Orientation_Constraint()
	bWaist.rotation.controller.appendtarget pySpine1 50
	bWaist.scale.controller = scale_script()
	bWaist.scale.controller.IScriptCtrl.AddNode "target" boneSpine1--pySpine1
	scriptStr = "target.stretchTM.scale"
	bWaist.scale.controller.IScriptCtrl.SetExpression scriptStr

	WaistInvScl.scale.controller = scale_script()
	WaistInvScl.scale.controller.IScriptCtrl.AddNode "Parent" bWaist
	scriptStr = "1.0 / Parent.scale.controller.value"
	WaistInvScl.scale.controller.IScriptCtrl.SetExpression scriptStr

	--bChest0.pos.controller = Position_Constraint()
	--bChest0.pos.controller.appendtarget pySpine3 50
	bChest0.rotation.controller = Orientation_Constraint()
	bChest0.rotation.controller.appendtarget pySpine2 50
	bChest0.scale.controller = scale_script()
	bChest0.scale.controller.IScriptCtrl.AddNode "target" boneSpine2--pySpine2
	scriptStr = "target.stretchTM.scale"
	bChest0.scale.controller.IScriptCtrl.SetExpression scriptStr

	Chest0InvScl.scale.controller = scale_script()
	Chest0InvScl.scale.controller.IScriptCtrl.AddNode "Parent" bChest0
	scriptStr = "1.0 / Parent.scale.controller.value"
	Chest0InvScl.scale.controller.IScriptCtrl.SetExpression scriptStr

	--bChest1.pos.controller = Position_Constraint()
	--bChest1.pos.controller.appendtarget pySpine3 50
	bChest1.rotation.controller = Orientation_Constraint()
	bChest1.rotation.controller.appendtarget pySpine3 50
	bChest1.scale.controller = scale_script()
	bChest1.scale.controller.IScriptCtrl.AddNode "target" boneSpine3--pySpine3
	scriptStr = "target.stretchTM.scale"
	bChest1.scale.controller.IScriptCtrl.SetExpression scriptStr

	Chest1InvScl.scale.controller = scale_script()
	Chest1InvScl.scale.controller.IScriptCtrl.AddNode "Parent" bChest1
	scriptStr = "1.0 / Parent.scale.controller.value"
	Chest1InvScl.scale.controller.IScriptCtrl.SetExpression scriptStr

	Chest1InvScl_Sh.scale.controller = scale_script()
	Chest1InvScl_Sh.scale.controller.IScriptCtrl.AddNode "Parent" bChest1
	scriptStr = "1.0 / Parent.scale.controller.value"
	Chest1InvScl_Sh.scale.controller.IScriptCtrl.SetExpression scriptStr

	Chest1InvScl_Tm.scale.controller = scale_script()
	Chest1InvScl_Tm.scale.controller.IScriptCtrl.AddNode "Parent" bChest1
	scriptStr = "1.0 / Parent.scale.controller.value"
	Chest1InvScl_Tm.scale.controller.IScriptCtrl.SetExpression scriptStr

	--bNeck.pos.controller = Position_Constraint()
	--bNeck.pos.controller.appendtarget ctrlNeck 50
	--bNeck.rotation.controller = Orientation_Constraint()
	--bNeck.rotation.controller.appendtarget ctrlNeck 50
	bNeck1.pos.controller = Position_Constraint()
	bNeck1.pos.controller.appendtarget locNeck1 50
	bNeck1.rotation.controller = Orientation_Constraint()
	bNeck1.rotation.controller.appendtarget locNeck1 50

	bNeck2.pos.controller = Position_Constraint()
	bNeck2.pos.controller.appendtarget locNeck2 50
	bNeck2.rotation.controller = Orientation_Constraint()
	bNeck2.rotation.controller.appendtarget locNeck2 50

	bHead.pos.controller = Position_Constraint()
	bHead.pos.controller.appendtarget ctrlHead 50
	bHead.rotation.controller = Orientation_Constraint()
	bHead.rotation.controller.appendtarget ctrlHead 50

	bThigh_R.rotation.controller = Orientation_Constraint()
	bThigh_R.rotation.controller.appendtarget LegTwistBoneList_R[1] 50

	bCalf_R.pos.controller = Position_Constraint()
	bCalf_R.pos.controller.appendtarget boneCalf_R 50
	bCalf_R.rotation.controller = Orientation_Constraint()
	bCalf_R.rotation.controller.appendtarget boneCalf_R 50

	bFoot_R.rotation.controller = Orientation_Constraint()
	bFoot_R.rotation.controller.appendtarget boneFoot_R 50

	bToe_R.rotation.controller = Orientation_Constraint()
	bToe_R.rotation.controller.appendtarget boneToe_R 50

	bButt_R.rotation.controller = Orientation_Constraint()
	bButt_R.rotation.controller.appendtarget boneButt_R 50
	bButt_R.scale.controller = scale_script()
	bButt_R.scale.controller.IScriptCtrl.AddNode "Target" boneButt_R
	scriptStr = "Target.scale.controller.value"
	bButt_R.scale.controller.IScriptCtrl.SetExpression scriptStr

	bThighTw1_R.rotation.controller = Orientation_Constraint()
	bThighTw1_R.rotation.controller.appendtarget LegTwistBoneList_R[2] 50

	bThighTw2_R.rotation.controller = Orientation_Constraint()
	bThighTw2_R.rotation.controller.appendtarget LegTwistBoneList_R[3] 50

	bThighTw3_R.rotation.controller = Orientation_Constraint()
	bThighTw3_R.rotation.controller.appendtarget LegTwistBoneList_R[4] 50

	bKnee_R.rotation.controller = Orientation_Constraint()
	bKnee_R.rotation.controller.appendtarget boneKnee_R 50
	----------
	bThigh_L.rotation.controller = Orientation_Constraint()
	bThigh_L.rotation.controller.appendtarget LegTwistBoneList_L[1] 50

	bCalf_L.pos.controller = Position_Constraint()
	bCalf_L.pos.controller.appendtarget boneCalf_L 50
	bCalf_L.rotation.controller = Orientation_Constraint()
	bCalf_L.rotation.controller.appendtarget boneCalf_L 50

	bFoot_L.rotation.controller = Orientation_Constraint()
	bFoot_L.rotation.controller.appendtarget boneFoot_L 50

	bToe_L.rotation.controller = Orientation_Constraint()
	bToe_L.rotation.controller.appendtarget boneToe_L 50

	bButt_L.rotation.controller = Orientation_Constraint()
	bButt_L.rotation.controller.appendtarget boneButt_L 50
	bButt_L.scale.controller = scale_script()
	bButt_L.scale.controller.IScriptCtrl.AddNode "Target" boneButt_L
	scriptStr = "Target.scale.controller.value"
	bButt_L.scale.controller.IScriptCtrl.SetExpression scriptStr

	bThighTw1_L.rotation.controller = Orientation_Constraint()
	bThighTw1_L.rotation.controller.appendtarget LegTwistBoneList_L[2] 50

	bThighTw2_L.rotation.controller = Orientation_Constraint()
	bThighTw2_L.rotation.controller.appendtarget LegTwistBoneList_L[3] 50

	bThighTw3_L.rotation.controller = Orientation_Constraint()
	bThighTw3_L.rotation.controller.appendtarget LegTwistBoneList_L[4] 50

	bKnee_L.rotation.controller = Orientation_Constraint()
	bKnee_L.rotation.controller.appendtarget boneKnee_L 50
	-----------
	bShoulder_R.rotation.controller = Orientation_Constraint()
	bShoulder_R.rotation.controller.appendtarget ctrlShoulder_R 50

	bAcrom_R.rotation.controller = Orientation_Constraint()
	bAcrom_R.rotation.controller.appendtarget jntAcrom_R 50

	bUpperArm_R.rotation.controller = Orientation_Constraint()
	bUpperArm_R.rotation.controller.appendtarget UpperArmTwistBoneList_R[1] 50

	bForeArm_R.pos.controller = Position_Constraint()
	bForeArm_R.pos.controller.appendtarget ForeArmTwistBoneList_R[1] 50
	bForeArm_R.rotation.controller = Orientation_Constraint()
	bForeArm_R.rotation.controller.appendtarget ForeArmTwistBoneList_R[1] 50

	bHand_R.rotation.controller = Orientation_Constraint()
	bHand_R.rotation.controller.appendtarget boneHand_R 50

	bUpperArmTw1_R.rotation.controller = Orientation_Constraint()
	bUpperArmTw1_R.rotation.controller.appendtarget UpperArmTwistBoneList_R[2] 50

	bUpperArmTw2_R.rotation.controller = Orientation_Constraint()
	bUpperArmTw2_R.rotation.controller.appendtarget UpperArmTwistBoneList_R[3] 50

	bUpperArmTw3_R.rotation.controller = Orientation_Constraint()
	bUpperArmTw3_R.rotation.controller.appendtarget UpperArmTwistBoneList_R[4] 50

	bElbow_R.rotation.controller = Orientation_Constraint()
	bElbow_R.rotation.controller.appendtarget jntElbow_R 50
	bElbow_R.scale.controller = scale_script()
	bElbow_R.scale.controller.IScriptCtrl.AddNode "target" jntElbow_R
	scriptStr = "target.scale.controller.value"
	bElbow_R.scale.controller.IScriptCtrl.SetExpression scriptStr

	bForeArmTw1_R.rotation.controller = Orientation_Constraint()
	bForeArmTw1_R.rotation.controller.appendtarget ForeArmTwistBoneList_R[2] 50

	bForeArmTw2_R.rotation.controller = Orientation_Constraint()
	bForeArmTw2_R.rotation.controller.appendtarget ForeArmTwistBoneList_R[3] 50

	bForeArmTw3_R.rotation.controller = Orientation_Constraint()
	bForeArmTw3_R.rotation.controller.appendtarget ForeArmTwistBoneList_R[4] 50

	bWrist_R.rotation.controller = Orientation_Constraint()
	bWrist_R.rotation.controller.appendtarget jntWrist_R 50

	bFinger00_R.rotation.controller = Orientation_Constraint()
	bFinger00_R.rotation.controller.appendtarget CtrlFinger00_R 50

	bFinger01_R.rotation.controller = Orientation_Constraint()
	bFinger01_R.rotation.controller.appendtarget CtrlFinger01_R 50

	bFinger02_R.rotation.controller = Orientation_Constraint()
	bFinger02_R.rotation.controller.appendtarget CtrlFinger02_R 50

	bFinger10_R.rotation.controller = Orientation_Constraint()
	bFinger10_R.rotation.controller.appendtarget CtrlFinger10_R 50

	bFinger11_R.rotation.controller = Orientation_Constraint()
	bFinger11_R.rotation.controller.appendtarget CtrlFinger11_R 50

	bFinger12_R.rotation.controller = Orientation_Constraint()
	bFinger12_R.rotation.controller.appendtarget CtrlFinger12_R 50

	bFinger20_R.rotation.controller = Orientation_Constraint()
	bFinger20_R.rotation.controller.appendtarget CtrlFinger20_R 50

	bFinger21_R.rotation.controller = Orientation_Constraint()
	bFinger21_R.rotation.controller.appendtarget CtrlFinger21_R 50

	bFinger22_R.rotation.controller = Orientation_Constraint()
	bFinger22_R.rotation.controller.appendtarget CtrlFinger22_R 50

	bFinger30_R.pos.controller = Position_Constraint()
	bFinger30_R.pos.controller.appendtarget CtrlFinger30_R 50
	bFinger30_R.rotation.controller = Orientation_Constraint()
	bFinger30_R.rotation.controller.appendtarget CtrlFinger30_R 50

	bFinger31_R.rotation.controller = Orientation_Constraint()
	bFinger31_R.rotation.controller.appendtarget CtrlFinger31_R 50

	bFinger32_R.rotation.controller = Orientation_Constraint()
	bFinger32_R.rotation.controller.appendtarget CtrlFinger32_R 50

	bFinger40_R.pos.controller = Position_Constraint()
	bFinger40_R.pos.controller.appendtarget CtrlFinger40_R 50
	bFinger40_R.rotation.controller = Orientation_Constraint()
	bFinger40_R.rotation.controller.appendtarget CtrlFinger40_R 50

	bFinger41_R.rotation.controller = Orientation_Constraint()
	bFinger41_R.rotation.controller.appendtarget CtrlFinger41_R 50

	bFinger42_R.rotation.controller = Orientation_Constraint()
	bFinger42_R.rotation.controller.appendtarget CtrlFinger42_R 50

	-----------
	bShoulder_L.rotation.controller = Orientation_Constraint()
	bShoulder_L.rotation.controller.appendtarget ctrlShoulder_L 50
	bShoulder_L.rotation.controller.relative = true

	bAcrom_L.rotation.controller = Orientation_Constraint()
	bAcrom_L.rotation.controller.appendtarget jntAcrom_L 50

	bUpperArm_L.rotation.controller = Orientation_Constraint()
	bUpperArm_L.rotation.controller.appendtarget UpperArmTwistBoneList_L[1] 50

	bForeArm_L.pos.controller = Position_Constraint()
	bForeArm_L.pos.controller.appendtarget ForeArmTwistBoneList_L[1] 50
	bForeArm_L.rotation.controller = Orientation_Constraint()
	bForeArm_L.rotation.controller.appendtarget ForeArmTwistBoneList_L[1] 50

	bHand_L.rotation.controller = Orientation_Constraint()
	bHand_L.rotation.controller.appendtarget boneHand_L 50

	bUpperArmTw1_L.rotation.controller = Orientation_Constraint()
	bUpperArmTw1_L.rotation.controller.appendtarget UpperArmTwistBoneList_L[2] 50

	bUpperArmTw2_L.rotation.controller = Orientation_Constraint()
	bUpperArmTw2_L.rotation.controller.appendtarget UpperArmTwistBoneList_L[3] 50

	bUpperArmTw3_L.rotation.controller = Orientation_Constraint()
	bUpperArmTw3_L.rotation.controller.appendtarget UpperArmTwistBoneList_L[4] 50

	bElbow_L.rotation.controller = Orientation_Constraint()
	bElbow_L.rotation.controller.appendtarget jntElbow_L 50
	bElbow_L.scale.controller = scale_script()
	bElbow_L.scale.controller.IScriptCtrl.AddNode "target" jntElbow_L
	scriptStr = "target.scale.controller.value"
	bElbow_L.scale.controller.IScriptCtrl.SetExpression scriptStr

	bForeArmTw1_L.rotation.controller = Orientation_Constraint()
	bForeArmTw1_L.rotation.controller.appendtarget ForeArmTwistBoneList_L[2] 50

	bForeArmTw2_L.rotation.controller = Orientation_Constraint()
	bForeArmTw2_L.rotation.controller.appendtarget ForeArmTwistBoneList_L[3] 50

	bForeArmTw3_L.rotation.controller = Orientation_Constraint()
	bForeArmTw3_L.rotation.controller.appendtarget ForeArmTwistBoneList_L[4] 50

	bWrist_L.rotation.controller = Orientation_Constraint()
	bWrist_L.rotation.controller.appendtarget jntWrist_L 50

	bFinger00_L.rotation.controller = Orientation_Constraint()
	bFinger00_L.rotation.controller.appendtarget CtrlFinger00_L 50

	bFinger01_L.rotation.controller = Orientation_Constraint()
	bFinger01_L.rotation.controller.appendtarget CtrlFinger01_L 50

	bFinger02_L.rotation.controller = Orientation_Constraint()
	bFinger02_L.rotation.controller.appendtarget CtrlFinger02_L 50

	bFinger10_L.rotation.controller = Orientation_Constraint()
	bFinger10_L.rotation.controller.appendtarget CtrlFinger10_L 50

	bFinger11_L.rotation.controller = Orientation_Constraint()
	bFinger11_L.rotation.controller.appendtarget CtrlFinger11_L 50

	bFinger12_L.rotation.controller = Orientation_Constraint()
	bFinger12_L.rotation.controller.appendtarget CtrlFinger12_L 50

	bFinger20_L.rotation.controller = Orientation_Constraint()
	bFinger20_L.rotation.controller.appendtarget CtrlFinger20_L 50

	bFinger21_L.rotation.controller = Orientation_Constraint()
	bFinger21_L.rotation.controller.appendtarget CtrlFinger21_L 50

	bFinger22_L.rotation.controller = Orientation_Constraint()
	bFinger22_L.rotation.controller.appendtarget CtrlFinger22_L 50

	bFinger30_L.pos.controller = Position_Constraint()
	bFinger30_L.pos.controller.appendtarget CtrlFinger30_L 50
	bFinger30_L.rotation.controller = Orientation_Constraint()
	bFinger30_L.rotation.controller.appendtarget CtrlFinger30_L 50

	bFinger31_L.rotation.controller = Orientation_Constraint()
	bFinger31_L.rotation.controller.appendtarget CtrlFinger31_L 50

	bFinger32_L.rotation.controller = Orientation_Constraint()
	bFinger32_L.rotation.controller.appendtarget CtrlFinger32_L 50

	bFinger40_L.pos.controller = Position_Constraint()
	bFinger40_L.pos.controller.appendtarget CtrlFinger40_L 50
	bFinger40_L.rotation.controller = Orientation_Constraint()
	bFinger40_L.rotation.controller.appendtarget CtrlFinger40_L 50

	bFinger41_L.rotation.controller = Orientation_Constraint()
	bFinger41_L.rotation.controller.appendtarget CtrlFinger41_L 50

	bFinger42_L.rotation.controller = Orientation_Constraint()
	bFinger42_L.rotation.controller.appendtarget CtrlFinger42_L 50
	-----
	bBust0_R.pos.controller = Position_Constraint()
	bBust0_R.pos.controller.appendtarget boneBust0_R 50
	bBust0_R.rotation.controller = Orientation_Constraint()
	bBust0_R.rotation.controller.appendtarget boneBust0_R 50

	bBust1_R.rotation.controller = Orientation_Constraint()
	bBust1_R.rotation.controller.appendtarget boneBust1_R 50

	bBust0_L.pos.controller = Position_Constraint()
	bBust0_L.pos.controller.appendtarget boneBust0_L 50
	bBust0_L.rotation.controller = Orientation_Constraint()
	bBust0_L.rotation.controller.appendtarget boneBust0_L 50

	bBust1_L.rotation.controller = Orientation_Constraint()
	bBust1_L.rotation.controller.appendtarget boneBust1_L 50
	---------------
	bTeresMajor_R.rotation.controller = Orientation_Constraint()
	bTeresMajor_R.rotation.controller.appendtarget boneTeresMajor_R 50
	bTeresMajor_R.scale.controller = scale_script()
	bTeresMajor_R.scale.controller.IScriptCtrl.AddNode "target" boneTeresMajor_R
	scriptStr = "target.scale.controller.value"
	bTeresMajor_R.scale.controller.IScriptCtrl.SetExpression scriptStr

	bTeresMajor_L.rotation.controller = Orientation_Constraint()
	bTeresMajor_L.rotation.controller.appendtarget boneTeresMajor_L 50
	bTeresMajor_L.scale.controller = scale_script()
	bTeresMajor_L.scale.controller.IScriptCtrl.AddNode "target" boneTeresMajor_L
	scriptStr = "target.scale.controller.value"
	bTeresMajor_L.scale.controller.IScriptCtrl.SetExpression scriptStr

--------End---------
clearSelection()
hideLayer.ishidden = true
