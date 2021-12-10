try(
	DestroyDialog KAnmTools2
)catch()

W = 455
H = 640
strNameSpace = ""

rollout roBiped "Biped" rolledUp:false (
	editText edtNameSpace "" width:96 height:16 pos:[8,8] enabled:false
	button btnUpdateNS "..." width:18 height:18 pos:[109,8]


	local con = dotNetClass "system.windows.forms.control"
	---------- Buttons -----------
		--imgtag imgHuman "" bitmap:( openBitmap ("D:\\man.tga") )-- align:#center
		dotNetControl dbtnSAll "System.Windows.Forms.Button" height:21 width:147 pos:[132,533]
		dotNetControl dbtnSRoot "System.Windows.Forms.Button" height:16 width:59 pos:[176,513]
		dotNetControl dbtnSRm "System.Windows.Forms.Button" height:16 width:20 pos:[195,493]
		
		dotNetControl dbtnSHip "System.Windows.Forms.Button" height:24 width:63 pos:[173,271]
		dotNetControl dbtnSWaist "System.Windows.Forms.Button" height:27 width:31 pos:[189,240]
		dotNetControl dbtnSChest "System.Windows.Forms.Button" height:21 width:66 pos:[171,214]
		dotNetControl dbtnSNeck "System.Windows.Forms.Button" height:27 width:23 pos:[193,183]
		dotNetControl dbtnSHead "System.Windows.Forms.Button" height:57 width:47 pos:[181,122]
		
		dotNetControl dbtnSLegUpvR "System.Windows.Forms.Button" height:22 width:23 pos:[169,371]
		dotNetControl dbtnSLegUpvL "System.Windows.Forms.Button" height:22 width:23 pos:[217,371]
		dotNetControl dbtnSFootPadR "System.Windows.Forms.Button" height:24 width:33 pos:[159,468]
		dotNetControl dbtnSFootPadL "System.Windows.Forms.Button" height:25 width:33 pos:[217,468]
		dotNetControl dbtnSFootR "System.Windows.Forms.Button" height:13 width:60 pos:[132,495]
		dotNetControl dbtnSFootL "System.Windows.Forms.Button" height:13 width:60 pos:[217,495]
		
		dotNetControl dbtnSShoulderR "System.Windows.Forms.Button" height:14 width:36 pos:[152,196]
		dotNetControl dbtnSShoulderL "System.Windows.Forms.Button" height:14 width:36 pos:[220,196]
		
		dotNetControl dbtnSFKUpperArmR "System.Windows.Forms.Button" height:69 width:16 pos:[132,196]
		dotNetControl dbtnSFKUpperArmL "System.Windows.Forms.Button" height:70 width:16 pos:[259,196]
		
		dotNetControl dbtnSFKForeArmR "System.Windows.Forms.Button" height:69 width:16 pos:[132,269]
		dotNetControl dbtnSFKForeArmL "System.Windows.Forms.Button" height:70 width:16 pos:[259,269]
		
		dotNetControl dbtnSFKHandR "System.Windows.Forms.Button" height:27 width:25 pos:[132,342]
		dotNetControl dbtnSFKHandL "System.Windows.Forms.Button" height:27 width:25 pos:[250,342]
		
		dotNetControl dbtnSIKArmUpvR "System.Windows.Forms.Button" height:20 width:20 pos:[108,258]
		dotNetControl dbtnSIKArmUpvL "System.Windows.Forms.Button" height:20 width:20 pos:[278,258]
		
		dotNetControl dbtnSIKHandR "System.Windows.Forms.Button" height:20 width:20 pos:[108,330]
		dotNetControl dbtnSIKHandL "System.Windows.Forms.Button" height:20 width:20 pos:[278,330]
		----
		dotNetControl dbtnSFinger00R "System.Windows.Forms.Button" height:24 width:12 pos:[8,467]
		dotNetControl dbtnSFinger01R "System.Windows.Forms.Button" height:24 width:12 pos:[8,440]
		dotNetControl dbtnSFinger02R "System.Windows.Forms.Button" height:24 width:12 pos:[8,413]
		dotNetControl dbtnSFinger0R "System.Windows.Forms.Button" height:10 width:10 pos:[9,400]
		
		dotNetControl dbtnSFinger10R "System.Windows.Forms.Button" height:24 width:12 pos:[26,423]
		dotNetControl dbtnSFinger11R "System.Windows.Forms.Button" height:24 width:12 pos:[26,396]
		dotNetControl dbtnSFinger12R "System.Windows.Forms.Button" height:24 width:12 pos:[26,369]
		dotNetControl dbtnSFinger1R "System.Windows.Forms.Button" height:10 width:10 pos:[27,356]
		
		dotNetControl dbtnSFinger20R "System.Windows.Forms.Button" height:24 width:12 pos:[42,423]
		dotNetControl dbtnSFinger21R "System.Windows.Forms.Button" height:24 width:12 pos:[42,396]
		dotNetControl dbtnSFinger22R "System.Windows.Forms.Button" height:24 width:12 pos:[42,369]
		dotNetControl dbtnSFinger2R "System.Windows.Forms.Button" height:10 width:10 pos:[43,356]
		
		dotNetControl dbtnSFinger30R "System.Windows.Forms.Button" height:24 width:12 pos:[58,423]
		dotNetControl dbtnSFinger31R "System.Windows.Forms.Button" height:24 width:12 pos:[58,396]
		dotNetControl dbtnSFinger32R "System.Windows.Forms.Button" height:24 width:12 pos:[58,369]
		dotNetControl dbtnSFinger3R "System.Windows.Forms.Button" height:10 width:10 pos:[59,356]
		
		dotNetControl dbtnSFinger40R "System.Windows.Forms.Button" height:24 width:12 pos:[74,423]
		dotNetControl dbtnSFinger41R "System.Windows.Forms.Button" height:24 width:12 pos:[74,396]
		dotNetControl dbtnSFinger42R "System.Windows.Forms.Button" height:24 width:12 pos:[74,369]
		dotNetControl dbtnSFinger4R "System.Windows.Forms.Button" height:10 width:10 pos:[75,356]
		
		dotNetControl dbtnSFingerS0R "System.Windows.Forms.Button" height:22 width:10 pos:[90,424]
		dotNetControl dbtnSFingerS1R "System.Windows.Forms.Button" height:22 width:10 pos:[90,397]
		dotNetControl dbtnSFingerS2R "System.Windows.Forms.Button" height:22 width:10 pos:[90,370]
		----
		dotNetControl dbtnSFinger00L "System.Windows.Forms.Button" height:24 width:12 pos:[388,467]
		dotNetControl dbtnSFinger01L "System.Windows.Forms.Button" height:24 width:12 pos:[388,440]
		dotNetControl dbtnSFinger02L "System.Windows.Forms.Button" height:24 width:12 pos:[388,413]
		dotNetControl dbtnSFinger0L "System.Windows.Forms.Button" height:10 width:10 pos:[389,400]
		
		dotNetControl dbtnSFinger10L "System.Windows.Forms.Button" height:24 width:12 pos:[370,423]
		dotNetControl dbtnSFinger11L "System.Windows.Forms.Button" height:24 width:12 pos:[370,396]
		dotNetControl dbtnSFinger12L "System.Windows.Forms.Button" height:24 width:12 pos:[370,369]
		dotNetControl dbtnSFinger1L "System.Windows.Forms.Button" height:10 width:10 pos:[371,356]
		
		dotNetControl dbtnSFinger20L "System.Windows.Forms.Button" height:24 width:12 pos:[354,423]
		dotNetControl dbtnSFinger21L "System.Windows.Forms.Button" height:24 width:12 pos:[354,396]
		dotNetControl dbtnSFinger22L "System.Windows.Forms.Button" height:24 width:12 pos:[354,369]
		dotNetControl dbtnSFinger2L "System.Windows.Forms.Button" height:10 width:10 pos:[355,356]
		
		dotNetControl dbtnSFinger30L "System.Windows.Forms.Button" height:24 width:12 pos:[338,423]
		dotNetControl dbtnSFinger31L "System.Windows.Forms.Button" height:24 width:12 pos:[338,396]
		dotNetControl dbtnSFinger32L "System.Windows.Forms.Button" height:24 width:12 pos:[338,369]
		dotNetControl dbtnSFinger3L "System.Windows.Forms.Button" height:10 width:10 pos:[339,356]
		
		dotNetControl dbtnSFinger40L "System.Windows.Forms.Button" height:24 width:12 pos:[322,423]
		dotNetControl dbtnSFinger41L "System.Windows.Forms.Button" height:24 width:12 pos:[322,396]
		dotNetControl dbtnSFinger42L "System.Windows.Forms.Button" height:24 width:12 pos:[322,369]
		dotNetControl dbtnSFinger4L "System.Windows.Forms.Button" height:10 width:10 pos:[323,356]
		
		dotNetControl dbtnSFingerS0L "System.Windows.Forms.Button" height:22 width:10 pos:[309,424]
		dotNetControl dbtnSFingerS1L "System.Windows.Forms.Button" height:22 width:10 pos:[309,397]
		dotNetControl dbtnSFingerS2L "System.Windows.Forms.Button" height:22 width:10 pos:[309,370]
		----
		dotNetControl bnThighR "System.Windows.Forms.Button" height:69 width:23 pos:[169,299]
		dotNetControl bnThighL "System.Windows.Forms.Button" height:69 width:23 pos:[217,299]
		dotNetControl bnCalfR "System.Windows.Forms.Button" height:69 width:23 pos:[169,396]
		dotNetControl bnCalfL "System.Windows.Forms.Button" height:69 width:23 pos:[217,396]
		dotNetControl bnHandR "System.Windows.Forms.Button" height:66 width:61 pos:[26,450]
		dotNetControl bnHandL "System.Windows.Forms.Button" height:66 width:61 pos:[322,450]
	
	on btnUpdateNS pressed do (
		selCount = selection.count
		if selCount > 0 then (
			
			strElems = filterString selection[1].name ":"
			
			strNameSpace = (substring selection[1].name 1 (selection[1].name.count-strElems[strElems.count].count) )
			edtNameSpace.text = strNameSpace

		) else (
			strNameSpace = ""
		)
	)

	on roBiped open do (
		edtNameSpace.text = strNameSpace

		mColor = dotnetclass "System.drawing.color"
		mAlign = dotnetclass "System.Drawing.ContentAlignment"
		mFlatStyle = dotnetobject "System.Windows.Forms.FlatStyle" Popup
		
		mColor_Gray = mColor.FromArgb 94 94 94
		mColor_DarkRed = mColor.FromArgb 112 10 10
		
		mColor_RightSide1 = mColor.FromArgb 6 134 6
		mColor_LeftSide1 = mColor.FromArgb 25 33 151
		
		mColor_RightSide2 = mColor.FromArgb 40 160 40
		mColor_LeftSide2 = mColor.FromArgb 30 50 160
		
		-- bnThighR --
		bnThighR.flatstyle = mFlatStyle
		bnThighR.FlatAppearance.BorderSize = 0
		bnThighR.backcolor = mColor_Gray
		bnThighR.Enabled = false
		-- bnThighL --
		bnThighL.flatstyle = mFlatStyle
		bnThighL.FlatAppearance.BorderSize = 0
		bnThighL.backcolor = mColor_Gray
		bnThighL.Enabled = false
		-- bnCalfR --
		bnCalfR.flatstyle = mFlatStyle
		bnCalfR.FlatAppearance.BorderSize = 0
		bnCalfR.backcolor = mColor_Gray
		bnCalfR.Enabled = false
		-- bnCalfL --
		bnCalfL.flatstyle = mFlatStyle
		bnCalfL.FlatAppearance.BorderSize = 0
		bnCalfL.backcolor = mColor_Gray
		bnCalfL.Enabled = false
		-- bnHandR --
		bnHandR.flatstyle = mFlatStyle
		bnHandR.FlatAppearance.BorderSize = 0
		bnHandR.backcolor = mColor_Gray
		bnHandR.Enabled = false
		-- bnHandL --
		bnHandL.flatstyle = mFlatStyle
		bnHandL.FlatAppearance.BorderSize = 0
		bnHandL.backcolor = mColor_Gray
		bnHandL.Enabled = false
		
		-- dbtnSAll --
		dbtnSAll.text = "All"
		dbtnSAll.flatstyle = mFlatStyle
		dbtnSAll.FlatAppearance.BorderSize = 0
		--dbtnSAll.FlatAppearance.MouseOverBackColor = mColor.FromArgb 255 128 128
		dbtnSAll.backcolor = mColor_DarkRed
		dbtnSAll.forecolor = mColor.FromArgb 171 115 115
		
		-- dbtnSRoot --
		dbtnSRoot.text = "Root"
		dbtnSRoot.flatstyle = mFlatStyle
		dbtnSRoot.FlatAppearance.BorderSize = 0
		dbtnSRoot.backcolor = mColor.FromArgb 0 255 0
		dbtnSRoot.forecolor = mColor.FromArgb 0 0 0
		
		-- dbtnSRm --
		dbtnSRm.flatstyle = mFlatStyle
		dbtnSRm.FlatAppearance.BorderSize = 0
		dbtnSRm.backcolor = mColor.FromArgb 255 114 0
		
		-- dbtnSHip --
		dbtnSHip.flatstyle = mFlatStyle
		dbtnSHip.FlatAppearance.BorderSize = 0
		dbtnSHip.backcolor = mColor.FromArgb 10 144 177
		
		-- dbtnSWaist --
		dbtnSWaist.flatstyle = mFlatStyle
		dbtnSWaist.FlatAppearance.BorderSize = 0
		dbtnSWaist.backcolor = mColor.FromArgb 10 144 177
		
		-- dbtnSChest --
		dbtnSChest.flatstyle = mFlatStyle
		dbtnSChest.FlatAppearance.BorderSize = 0
		dbtnSChest.backcolor = mColor.FromArgb 10 144 177
		
		-- dbtnSNeck --
		dbtnSNeck.flatstyle = mFlatStyle
		dbtnSNeck.FlatAppearance.BorderSize = 0
		dbtnSNeck.backcolor = mColor.FromArgb 10 144 177
		
		-- dbtnSHead --
		dbtnSHead.flatstyle = mFlatStyle
		dbtnSHead.FlatAppearance.BorderSize = 0
		dbtnSHead.backcolor = mColor.FromArgb 166 202 240
		
		-- dbtnSLegUpvR --
		dbtnSLegUpvR.flatstyle = mFlatStyle
		dbtnSLegUpvR.FlatAppearance.BorderSize = 0
		dbtnSLegUpvR.backcolor = mColor_RightSide1
		
		-- dbtnSLegUpvL --
		dbtnSLegUpvL.flatstyle = mFlatStyle
		dbtnSLegUpvL.FlatAppearance.BorderSize = 0
		dbtnSLegUpvL.backcolor = mColor_LeftSide1
		
		-- dbtnSFootPadR --
		dbtnSFootPadR.flatstyle = mFlatStyle
		dbtnSFootPadR.FlatAppearance.BorderSize = 0
		dbtnSFootPadR.backcolor = mColor_RightSide1
		
		-- dbtnSFootPadL --
		dbtnSFootPadL.flatstyle = mFlatStyle
		dbtnSFootPadL.FlatAppearance.BorderSize = 0
		dbtnSFootPadL.backcolor = mColor_LeftSide1
		
		-- dbtnSFootR --
		dbtnSFootR.flatstyle = mFlatStyle
		dbtnSFootR.FlatAppearance.BorderSize = 0
		dbtnSFootR.backcolor = mColor_RightSide1
		
		-- dbtnSFootL --
		dbtnSFootL.flatstyle = mFlatStyle
		dbtnSFootL.FlatAppearance.BorderSize = 0
		dbtnSFootL.backcolor = mColor_LeftSide1
		
		-- dbtnSShoulderR --
		dbtnSShoulderR.flatstyle = mFlatStyle
		dbtnSShoulderR.FlatAppearance.BorderSize = 0
		dbtnSShoulderR.backcolor = mColor_RightSide1
		
		-- dbtnSShoulderL --
		dbtnSShoulderL.flatstyle = mFlatStyle
		dbtnSShoulderL.FlatAppearance.BorderSize = 0
		dbtnSShoulderL.backcolor = mColor_LeftSide1
		
		-- dbtnSFKUpperArmR --
		dbtnSFKUpperArmR.flatstyle = mFlatStyle
		dbtnSFKUpperArmR.FlatAppearance.BorderSize = 0
		dbtnSFKUpperArmR.backcolor = mColor_RightSide1
		
		-- dbtnSFKUpperArmL --
		dbtnSFKUpperArmL.flatstyle = mFlatStyle
		dbtnSFKUpperArmL.FlatAppearance.BorderSize = 0
		dbtnSFKUpperArmL.backcolor = mColor_LeftSide1
		
		-- dbtnSFKForeArmR --
		dbtnSFKForeArmR.flatstyle = mFlatStyle
		dbtnSFKForeArmR.FlatAppearance.BorderSize = 0
		dbtnSFKForeArmR.backcolor = mColor_RightSide1
		
		-- dbtnSFKForeArmL --
		dbtnSFKForeArmL.flatstyle = mFlatStyle
		dbtnSFKForeArmL.FlatAppearance.BorderSize = 0
		dbtnSFKForeArmL.backcolor = mColor_LeftSide1
		
		-- dbtnSFKHandR --
		dbtnSFKHandR.flatstyle = mFlatStyle
		dbtnSFKHandR.FlatAppearance.BorderSize = 0
		dbtnSFKHandR.backcolor = mColor_RightSide1
		
		-- dbtnSFKHandL --
		dbtnSFKHandL.flatstyle = mFlatStyle
		dbtnSFKHandL.FlatAppearance.BorderSize = 0
		dbtnSFKHandL.backcolor = mColor_LeftSide1
		
		-- dbtnSIKArmUpvR --
		dbtnSIKArmUpvR.flatstyle = mFlatStyle
		dbtnSIKArmUpvR.FlatAppearance.BorderSize = 0
		dbtnSIKArmUpvR.backcolor = mColor_RightSide2
		
		-- dbtnSIKArmUpvL --
		dbtnSIKArmUpvL.flatstyle = mFlatStyle
		dbtnSIKArmUpvL.FlatAppearance.BorderSize = 0
		dbtnSIKArmUpvL.backcolor = mColor_LeftSide2
		
		-- dbtnSIKHandR --
		dbtnSIKHandR.flatstyle = mFlatStyle
		dbtnSIKHandR.FlatAppearance.BorderSize = 0
		dbtnSIKHandR.backcolor = mColor_RightSide2
		
		-- dbtnSIKHandL --
		dbtnSIKHandL.flatstyle = mFlatStyle
		dbtnSIKHandL.FlatAppearance.BorderSize = 0
		dbtnSIKHandL.backcolor = mColor_LeftSide2
		-----------
		-- dbtnSFinger00R --
		dbtnSFinger00R.flatstyle = mFlatStyle
		dbtnSFinger00R.FlatAppearance.BorderSize = 0
		dbtnSFinger00R.backcolor = mColor_RightSide1
		-- dbtnSFinger01R --
		dbtnSFinger01R.flatstyle = mFlatStyle
		dbtnSFinger01R.FlatAppearance.BorderSize = 0
		dbtnSFinger01R.backcolor = mColor_RightSide1
		-- dbtnSFinger02R --
		dbtnSFinger02R.flatstyle = mFlatStyle
		dbtnSFinger02R.FlatAppearance.BorderSize = 0
		dbtnSFinger02R.backcolor = mColor_RightSide1
		-- dbtnSFinger0R --
		dbtnSFinger0R.flatstyle = mFlatStyle
		dbtnSFinger0R.FlatAppearance.BorderSize = 0
		dbtnSFinger0R.backcolor = mColor_DarkRed
		
		-- dbtnSFinger10R --
		dbtnSFinger10R.flatstyle = mFlatStyle
		dbtnSFinger10R.FlatAppearance.BorderSize = 0
		dbtnSFinger10R.backcolor = mColor_RightSide1
		-- dbtnSFinger11R --
		dbtnSFinger11R.flatstyle = mFlatStyle
		dbtnSFinger11R.FlatAppearance.BorderSize = 0
		dbtnSFinger11R.backcolor = mColor_RightSide1
		-- dbtnSFinger12R --
		dbtnSFinger12R.flatstyle = mFlatStyle
		dbtnSFinger12R.FlatAppearance.BorderSize = 0
		dbtnSFinger12R.backcolor = mColor_RightSide1
		-- dbtnSFinger1R --
		dbtnSFinger1R.flatstyle = mFlatStyle
		dbtnSFinger1R.FlatAppearance.BorderSize = 0
		dbtnSFinger1R.backcolor = mColor_DarkRed
		
		-- dbtnSFinger20R --
		dbtnSFinger20R.flatstyle = mFlatStyle
		dbtnSFinger20R.FlatAppearance.BorderSize = 0
		dbtnSFinger20R.backcolor = mColor_RightSide1
		-- dbtnSFinger21R --
		dbtnSFinger21R.flatstyle = mFlatStyle
		dbtnSFinger21R.FlatAppearance.BorderSize = 0
		dbtnSFinger21R.backcolor = mColor_RightSide1
		-- dbtnSFinger22R --
		dbtnSFinger22R.flatstyle = mFlatStyle
		dbtnSFinger22R.FlatAppearance.BorderSize = 0
		dbtnSFinger22R.backcolor = mColor_RightSide1
		-- dbtnSFinger2R --
		dbtnSFinger2R.flatstyle = mFlatStyle
		dbtnSFinger2R.FlatAppearance.BorderSize = 0
		dbtnSFinger2R.backcolor = mColor_DarkRed
		
		-- dbtnSFinger30R --
		dbtnSFinger30R.flatstyle = mFlatStyle
		dbtnSFinger30R.FlatAppearance.BorderSize = 0
		dbtnSFinger30R.backcolor = mColor_RightSide1
		-- dbtnSFinger31R --
		dbtnSFinger31R.flatstyle = mFlatStyle
		dbtnSFinger31R.FlatAppearance.BorderSize = 0
		dbtnSFinger31R.backcolor = mColor_RightSide1
		-- dbtnSFinger32R --
		dbtnSFinger32R.flatstyle = mFlatStyle
		dbtnSFinger32R.FlatAppearance.BorderSize = 0
		dbtnSFinger32R.backcolor = mColor_RightSide1
		-- dbtnSFinger3R --
		dbtnSFinger3R.flatstyle = mFlatStyle
		dbtnSFinger3R.FlatAppearance.BorderSize = 0
		dbtnSFinger3R.backcolor = mColor_DarkRed
		
		-- dbtnSFinger40R --
		dbtnSFinger40R.flatstyle = mFlatStyle
		dbtnSFinger40R.FlatAppearance.BorderSize = 0
		dbtnSFinger40R.backcolor = mColor_RightSide1
		-- dbtnSFinger41R --
		dbtnSFinger41R.flatstyle = mFlatStyle
		dbtnSFinger41R.FlatAppearance.BorderSize = 0
		dbtnSFinger41R.backcolor = mColor_RightSide1
		-- dbtnSFinger42R --
		dbtnSFinger42R.flatstyle = mFlatStyle
		dbtnSFinger42R.FlatAppearance.BorderSize = 0
		dbtnSFinger42R.backcolor = mColor_RightSide1
		-- dbtnSFinger4R --
		dbtnSFinger4R.flatstyle = mFlatStyle
		dbtnSFinger4R.FlatAppearance.BorderSize = 0
		dbtnSFinger4R.backcolor = mColor_DarkRed
		
		-- dbtnSFingerS0R --
		dbtnSFingerS0R.flatstyle = mFlatStyle
		dbtnSFingerS0R.FlatAppearance.BorderSize = 0
		dbtnSFingerS0R.backcolor = mColor_DarkRed
		-- dbtnSFingerS1R --
		dbtnSFingerS1R.flatstyle = mFlatStyle
		dbtnSFingerS1R.FlatAppearance.BorderSize = 0
		dbtnSFingerS1R.backcolor = mColor_DarkRed
		-- dbtnSFingerS2R --
		dbtnSFingerS2R.flatstyle = mFlatStyle
		dbtnSFingerS2R.FlatAppearance.BorderSize = 0
		dbtnSFingerS2R.backcolor = mColor_DarkRed
		
		-----------
		-- dbtnSFinger00L --
		dbtnSFinger00L.flatstyle = mFlatStyle
		dbtnSFinger00L.FlatAppearance.BorderSize = 0
		dbtnSFinger00L.backcolor = mColor_LeftSide1
		-- dbtnSFinger01L --
		dbtnSFinger01L.flatstyle = mFlatStyle
		dbtnSFinger01L.FlatAppearance.BorderSize = 0
		dbtnSFinger01L.backcolor = mColor_LeftSide1
		-- dbtnSFinger02L --
		dbtnSFinger02L.flatstyle = mFlatStyle
		dbtnSFinger02L.FlatAppearance.BorderSize = 0
		dbtnSFinger02L.backcolor = mColor_LeftSide1
		-- dbtnSFinger0L --
		dbtnSFinger0L.flatstyle = mFlatStyle
		dbtnSFinger0L.FlatAppearance.BorderSize = 0
		dbtnSFinger0L.backcolor = mColor_DarkRed
		
		-- dbtnSFinger10L --
		dbtnSFinger10L.flatstyle = mFlatStyle
		dbtnSFinger10L.FlatAppearance.BorderSize = 0
		dbtnSFinger10L.backcolor = mColor_LeftSide1
		-- dbtnSFinger11L --
		dbtnSFinger11L.flatstyle = mFlatStyle
		dbtnSFinger11L.FlatAppearance.BorderSize = 0
		dbtnSFinger11L.backcolor = mColor_LeftSide1
		-- dbtnSFinger12L --
		dbtnSFinger12L.flatstyle = mFlatStyle
		dbtnSFinger12L.FlatAppearance.BorderSize = 0
		dbtnSFinger12L.backcolor = mColor_LeftSide1
		-- dbtnSFinger1L --
		dbtnSFinger1L.flatstyle = mFlatStyle
		dbtnSFinger1L.FlatAppearance.BorderSize = 0
		dbtnSFinger1L.backcolor = mColor_DarkRed
		
		-- dbtnSFinger20L --
		dbtnSFinger20L.flatstyle = mFlatStyle
		dbtnSFinger20L.FlatAppearance.BorderSize = 0
		dbtnSFinger20L.backcolor = mColor_LeftSide1
		-- dbtnSFinger21L --
		dbtnSFinger21L.flatstyle = mFlatStyle
		dbtnSFinger21L.FlatAppearance.BorderSize = 0
		dbtnSFinger21L.backcolor = mColor_LeftSide1
		-- dbtnSFinger22L --
		dbtnSFinger22L.flatstyle = mFlatStyle
		dbtnSFinger22L.FlatAppearance.BorderSize = 0
		dbtnSFinger22L.backcolor = mColor_LeftSide1
		-- dbtnSFinger2L --
		dbtnSFinger2L.flatstyle = mFlatStyle
		dbtnSFinger2L.FlatAppearance.BorderSize = 0
		dbtnSFinger2L.backcolor = mColor_DarkRed
		
		-- dbtnSFinger30L --
		dbtnSFinger30L.flatstyle = mFlatStyle
		dbtnSFinger30L.FlatAppearance.BorderSize = 0
		dbtnSFinger30L.backcolor = mColor_LeftSide1
		-- dbtnSFinger31L --
		dbtnSFinger31L.flatstyle = mFlatStyle
		dbtnSFinger31L.FlatAppearance.BorderSize = 0
		dbtnSFinger31L.backcolor = mColor_LeftSide1
		-- dbtnSFinger32L --
		dbtnSFinger32L.flatstyle = mFlatStyle
		dbtnSFinger32L.FlatAppearance.BorderSize = 0
		dbtnSFinger32L.backcolor = mColor_LeftSide1
		-- dbtnSFinger3L --
		dbtnSFinger3L.flatstyle = mFlatStyle
		dbtnSFinger3L.FlatAppearance.BorderSize = 0
		dbtnSFinger3L.backcolor = mColor_DarkRed
		
		-- dbtnSFinger40L --
		dbtnSFinger40L.flatstyle = mFlatStyle
		dbtnSFinger40L.FlatAppearance.BorderSize = 0
		dbtnSFinger40L.backcolor = mColor_LeftSide1
		-- dbtnSFinger41L --
		dbtnSFinger41L.flatstyle = mFlatStyle
		dbtnSFinger41L.FlatAppearance.BorderSize = 0
		dbtnSFinger41L.backcolor = mColor_LeftSide1
		-- dbtnSFinger42L --
		dbtnSFinger42L.flatstyle = mFlatStyle
		dbtnSFinger42L.FlatAppearance.BorderSize = 0
		dbtnSFinger42L.backcolor = mColor_LeftSide1
		-- dbtnSFinger4L --
		dbtnSFinger4L.flatstyle = mFlatStyle
		dbtnSFinger4L.FlatAppearance.BorderSize = 0
		dbtnSFinger4L.backcolor = mColor_DarkRed
		
		-- dbtnSFingerS0L --
		dbtnSFingerS0L.flatstyle = mFlatStyle
		dbtnSFingerS0L.FlatAppearance.BorderSize = 0
		dbtnSFingerS0L.backcolor = mColor_DarkRed
		-- dbtnSFingerS1L --
		dbtnSFingerS1L.flatstyle = mFlatStyle
		dbtnSFingerS1L.FlatAppearance.BorderSize = 0
		dbtnSFingerS1L.backcolor = mColor_DarkRed
		-- dbtnSFingerS2L --
		dbtnSFingerS2L.flatstyle = mFlatStyle
		dbtnSFingerS2L.FlatAppearance.BorderSize = 0
		dbtnSFingerS2L.backcolor = mColor_DarkRed
	)
	
	on dbtnSAll click do (
		--print keyboard.controlPressed
		layer = LayerManager.getLayerFromName "Controller"
		layer.nodes &ctrlList
		if keyboard.controlPressed then (
			selectMore ctrlList
		) else (
			select ctrlList
		)
	)

	on dbtnSRoot click do (
		obj = getNodeByName (strNameSpace + "ControlRoot")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSRm click do (
		obj = getNodeByName (strNameSpace + "Ctrl_RootMotion")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSHip click do (
		obj = getNodeByName (strNameSpace + "Ctrl_Hip")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSWaist click do (
		obj = getNodeByName (strNameSpace + "Ctrl_Waist")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSChest click do (
		obj = getNodeByName (strNameSpace + "Ctrl_Chest")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSNeck click do (
		obj = getNodeByName (strNameSpace + "Ctrl_Neck")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSHead click do (
		obj = getNodeByName (strNameSpace + "Ctrl_Head")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSShoulderR click do (
		obj = getNodeByName (strNameSpace + "Ctrl_Shoulder_R")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSShoulderL click do (
		obj = getNodeByName (strNameSpace + "Ctrl_Shoulder_L")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSFKUpperArmR click do (
		obj = getNodeByName (strNameSpace + "Ctrl_UpperArmFK_R")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSFKUpperArmL click do (
		obj = getNodeByName (strNameSpace + "Ctrl_UpperArmFK_L")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSFKForeArmR click do (
		obj = getNodeByName (strNameSpace + "Ctrl_ForeArmFK_R")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSFKForeArmL click do (
		obj = getNodeByName (strNameSpace + "Ctrl_ForeArmFK_L")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSFKHandR click do (
		obj = getNodeByName (strNameSpace + "Ctrl_HandFK_R")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSFKHandL click do (
		obj = getNodeByName (strNameSpace + "Ctrl_HandFK_L")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSIKHandR click do (
		obj = getNodeByName (strNameSpace + "Ctrl_HandIK_R")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSIKHandL click do (
		obj = getNodeByName (strNameSpace + "Ctrl_HandIK_L")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSIKArmUpvR click do (
		obj = getNodeByName (strNameSpace + "Ctrl_ArmUpV_R")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSIKArmUpvL click do (
		obj = getNodeByName (strNameSpace + "Ctrl_ArmUpV_L")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSLegUpvR click do (
		obj = getNodeByName (strNameSpace + "Ctrl_LegUpV_R")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)
	
	on dbtnSLegUpvL click do (
		obj = getNodeByName (strNameSpace + "Ctrl_LegUpV_L")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSFootPadR click do (
		obj = getNodeByName (strNameSpace + "Ctrl_FootPad_R")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSFootPadL click do (
		obj = getNodeByName (strNameSpace + "Ctrl_FootPad_L")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSFootR click do (
		obj = getNodeByName (strNameSpace + "Ctrl_Foot_R")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)

	on dbtnSFootL click do (
		obj = getNodeByName (strNameSpace + "Ctrl_Foot_L")
		if keyboard.controlPressed then (
			selectMore obj
		) else (
			select obj
		)
	)
)

rollout roBBB "BBB" rolledUp:false (
	
)

rollout roCCC "CCC" rolledUp:false (
	
)

rolloutList = #(roBiped, roBBB, roCCC)

rollout KAnmTools2 "Anim Tools"
(
	dotNetControl DotNetTab "TabControl" height:22 width:(W - 16) pos:[8,8]
	
	subRollout theSubRollout height:(H - 40)
	
	local currentPageIdx = 0
	
	
	
	on DotNetTab Click do (
		--print ((currentPageIdx as string) + " >> " + (DotNetTab.SelectedIndex as string))
		if currentPageIdx != DotNetTab.SelectedIndex then (
			removeSubRollout theSubRollout rolloutList[currentPageIdx+1]
			addSubRollout theSubRollout rolloutList[DotNetTab.SelectedIndex+1]
			currentPageIdx = DotNetTab.SelectedIndex
		)
		
		currentPageIdx = DotNetTab.SelectedIndex
	)
	
	on KAnmTools2 open do (
		TempTabPageA = DotNetObject "System.Windows.Forms.TabPage"
		TempTabPageB = DotNetObject "System.Windows.Forms.TabPage"
		TempTabPageC = DotNetObject "System.Windows.Forms.TabPage"
		TempTabPageA.Text = "Human Biped"
		TempTabPageB.Text = "BBB"
		TempTabPageC.Text = "CCC"
		
		KAnmTools2.DotNetTab.Controls.Add TempTabPageA
		KAnmTools2.DotNetTab.Controls.Add TempTabPageB
		KAnmTools2.DotNetTab.Controls.Add TempTabPageC
		
		addSubRollout theSubRollout rolloutList[currentPageIdx+1]
	)
	
	
)



createDialog KAnmTools2 W H