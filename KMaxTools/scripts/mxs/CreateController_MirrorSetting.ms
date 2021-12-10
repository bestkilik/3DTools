/******************************************************************
Ctrl_Root
Ctrl_Hip
Ctrl_Waist
Ctrl_Chest
Ctrl_Head
Ctrl_RootMotion

Ctrl_Shoulder_R
Ctrl_HandIK_R
Ctrl_ArmUpV_R
Ctrl_UpperArmFK_R
Ctrl_ForeArmFK_R
Ctrl_HandFK_R
Ctrl_SubFingers_R
Ctrl_Finger00_R
Ctrl_Finger01_R
Ctrl_Finger02_R
Ctrl_Finger10_R
Ctrl_Finger11_R
Ctrl_Finger12_R
Ctrl_Finger20_R
Ctrl_Finger21_R
Ctrl_Finger22_R
Ctrl_Finger30_R
Ctrl_Finger31_R
Ctrl_Finger32_R
Ctrl_Finger40_R
Ctrl_Finger41_R
Ctrl_Finger42_R
Ctrl_Foot_R
Ctrl_FootPad_R
Ctrl_LegUpV_R
Ctrl_Bust0_R
Ctrl_Bust1_R

----------
rotXUpFix
rotYUpFix
rtRootCtrl
rpWaist
lpHead

----------
ShoulderRoot_R
BustRoot_R
Finger0Root_R
Finger1Root_R
Finger2Root_R
Finger3Root_R
Finger4Root_R
******************************************************************/

listMirName = #(
	"ControlRoot",
	"Ctrl_Hip",
	"Ctrl_Waist",
	"Ctrl_Chest",
	"Ctrl_Head",
	"Ctrl_RootMotion",
	"rotXUpFix",
	"rotYUpFix",
	"rtRootCtrl",
	"rpWaist",
	"ctrlHeadRoot",
	"ShoulderRoot_R",
	"BustRoot_R",
	"Finger0Root_R",
	"Finger1Root_R",
	"Finger2Root_R",
	"Finger3Root_R",
	"Finger4Root_R",
	"ShoulderRoot_L",
	"BustRoot_L",
	"Finger0Root_L",
	"Finger1Root_L",
	"Finger2Root_L",
	"Finger3Root_L",
	"Finger4Root_L",
	"Ctrl_Shoulder_R",
	"Ctrl_HandIK_R",
	"Ctrl_ArmUpV_R",
	"Ctrl_UpperArmFK_R",
	"Ctrl_ForeArmFK_R",
	"Ctrl_HandFK_R",
	"Ctrl_SubFingers_R",
	"Ctrl_Finger00_R",
	"Ctrl_Finger01_R",
	"Ctrl_Finger02_R",
	"Ctrl_Finger10_R",
	"Ctrl_Finger11_R",
	"Ctrl_Finger12_R",
	"Ctrl_Finger20_R",
	"Ctrl_Finger21_R",
	"Ctrl_Finger22_R",
	"Ctrl_Finger30_R",
	"Ctrl_Finger31_R",
	"Ctrl_Finger32_R",
	"Ctrl_Finger40_R",
	"Ctrl_Finger41_R",
	"Ctrl_Finger42_R",
	"Ctrl_Foot_R",
	"Ctrl_FootPad_R",
	"Ctrl_LegUpV_R",
	"Ctrl_Bust0_R",
	"Ctrl_Bust1_R",
	"Ctrl_Shoulder_L",
	"Ctrl_HandIK_L",
	"Ctrl_ArmUpV_L",
	"Ctrl_UpperArmFK_L",
	"Ctrl_ForeArmFK_L",
	"Ctrl_HandFK_L",
	"Ctrl_SubFingers_L",
	"Ctrl_Finger00_L",
	"Ctrl_Finger01_L",
	"Ctrl_Finger02_L",
	"Ctrl_Finger10_L",
	"Ctrl_Finger11_L",
	"Ctrl_Finger12_L",
	"Ctrl_Finger20_L",
	"Ctrl_Finger21_L",
	"Ctrl_Finger22_L",
	"Ctrl_Finger30_L",
	"Ctrl_Finger31_L",
	"Ctrl_Finger32_L",
	"Ctrl_Finger40_L",
	"Ctrl_Finger41_L",
	"Ctrl_Finger42_L",
	"Ctrl_Foot_L",
	"Ctrl_FootPad_L",
	"Ctrl_LegUpV_L",
	"Ctrl_Bust0_L",
	"Ctrl_Bust1_L")

listFlipX = #(
	"ControlRoot",
	"Ctrl_RootMotion",
	"rotYUpFix",
	"rtRootCtrl",
	"Ctrl_HandIK_R",
	"Ctrl_ArmUpV_R",
	"Ctrl_Foot_R",
	"Ctrl_FootPad_R",
	"Ctrl_LegUpV_R",
	"Ctrl_HandIK_L",
	"Ctrl_ArmUpV_L",
	"Ctrl_Foot_L",
	"Ctrl_FootPad_L",
	"Ctrl_LegUpV_L"
)

listFlipY = #(
	"Finger0Root_R",
	"Finger1Root_R",
	"Finger2Root_R",
	"Finger3Root_R",
	"Finger4Root_R",
	"Finger0Root_L",
	"Finger1Root_L",
	"Finger2Root_L",
	"Finger3Root_L",
	"Finger4Root_L",
	"Ctrl_UpperArmFK_R",
	"Ctrl_ForeArmFK_R",
	"Ctrl_HandFK_R",
	"Ctrl_SubFingers_R",
	"Ctrl_Finger00_R",
	"Ctrl_Finger01_R",
	"Ctrl_Finger02_R",
	"Ctrl_Finger10_R",
	"Ctrl_Finger11_R",
	"Ctrl_Finger12_R",
	"Ctrl_Finger20_R",
	"Ctrl_Finger21_R",
	"Ctrl_Finger22_R",
	"Ctrl_Finger30_R",
	"Ctrl_Finger31_R",
	"Ctrl_Finger32_R",
	"Ctrl_Finger40_R",
	"Ctrl_Finger41_R",
	"Ctrl_Finger42_R",
	"Ctrl_UpperArmFK_L",
	"Ctrl_ForeArmFK_L",
	"Ctrl_HandFK_L",
	"Ctrl_SubFingers_L",
	"Ctrl_Finger00_L",
	"Ctrl_Finger01_L",
	"Ctrl_Finger02_L",
	"Ctrl_Finger10_L",
	"Ctrl_Finger11_L",
	"Ctrl_Finger12_L",
	"Ctrl_Finger20_L",
	"Ctrl_Finger21_L",
	"Ctrl_Finger22_L",
	"Ctrl_Finger30_L",
	"Ctrl_Finger31_L",
	"Ctrl_Finger32_L",
	"Ctrl_Finger40_L",
	"Ctrl_Finger41_L",
	"Ctrl_Finger42_L")

listFlipZ = #(
	"Ctrl_Hip",
	"Ctrl_Waist",
	"Ctrl_Chest",
	"Ctrl_Head",
	"rotXUpFix",
	"rpWaist",
	"ctrlHeadRoot",
	"BustRoot_R",
	"BustRoot_L",
	"Ctrl_Bust0_R",
	"Ctrl_Bust1_R",
	"Ctrl_Bust0_L",
	"Ctrl_Bust1_L")

listFlipAll = #(
	"ShoulderRoot_R",
	"ShoulderRoot_L",
	"Ctrl_Shoulder_R",
	"Ctrl_Shoulder_L"
)

-- listMirrorCtrlNode = #()
for n in listMirName do (
	obj = getNodeByName n
	if obj != undefined then (
		mirrorInfoCA = custAttributes.get obj CAMirrorInfo
		if mirrorInfoCA == undefined then custAttributes.add obj CAMirrorInfo

		side = substring n (n.count-1) 2
		if side == "_R" then (
		    obj.SymmetryNode = (substring n 1 (n.count-2)) + "_L"
		)
		else if side == "_L" then (
			obj.SymmetryNode = (substring n 1 (n.count-2)) + "_R"
		)
		else (
			obj.SymmetryNode = n
		)
	)
)

for n in listFlipX do (
	obj = getNodeByName n
	if obj != undefined then (
		obj.FlipAxis = 1
	)
)

for n in listFlipY do (
	obj = getNodeByName n
	if obj != undefined then (
		obj.FlipAxis = 2
	)
)

for n in listFlipZ do (
	obj = getNodeByName n
	if obj != undefined then (
		obj.FlipAxis = 3
	)
)

for n in listFlipAll do (
	obj = getNodeByName n
	if obj != undefined then (
		obj.FlipAxis = 4
	)
)