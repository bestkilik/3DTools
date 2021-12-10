# -*- coding: utf-8 -*-
import os,sys
import maya.cmds as cmds
import maya.mel as mel
import os,sys
import shutil

def Install(rootPath):
	usd = cmds.internalVar(usd=True)
	usrFold = usd[:-8]
	usrPlugFold = usrFold+"plugins/"
	usrScrptFold = usrFold+"scripts/"
	usrImgFold = usrFold+"prefs/icons/"

	if( not os.path.exists(usrPlugFold )):
		os.makedirs(usrPlugFold)

	ToolPath = rootPath+'tools/'
	srcIconFoldPath = rootPath+'icons/'

	listIconsName = os.listdir(srcIconFoldPath)
	for icon in listIconsName:
		srcIconPath = srcIconFoldPath+icon
		tarIconPath = usrImgFold+icon
		if os.path.isfile(tarIconPath):
			os.chmod(tarIconPath, 755)
			os.remove(tarIconPath)
			
		shutil.copy2(srcIconPath, tarIconPath)
		os.chmod(tarIconPath, 755)

	g_ShelfTopLevel = mel.eval("$Temp = $gShelfTopLevel") # 取得maya global: gShelfTopLevel

	
	listToolsName = os.listdir(ToolPath)
	# print(cmds.tabLayout(g_ShelfTopLevel, q = True, ex = True))
	if cmds.tabLayout(g_ShelfTopLevel, q = True, ex = True):
		_tab = cmds.tabLayout(g_ShelfTopLevel,q=True,st=True)
		shelfButtons = cmds.shelfLayout(_tab , q=True, ca=True )
		# if (shelfButtons):
		for tName in listToolsName:
			toolFold = ToolPath + tName + '/'
			melPath = toolFold + tName + '.mel'
			melCommand = 'source "' + melPath + '";'

			if os.path.isfile(melPath):
				if shelfButtons:
					for btn in shelfButtons:
						if (cmds.control(btn,ex=True)):
							sfbtn = cmds.shelfButton(btn,q=True,annotation=True)
							if (sfbtn == 'Open '+tName):
								cmds.deleteUI(btn)

				cmds.shelfButton(parent = g_ShelfTopLevel + '|' + _tab ,
					image = tName+'Icon.png',
					iol = tName[1:-5],
					label = tName,
					sourceType = 'mel',
					annotation = 'Open '+tName,
					command = melCommand
					)
	else:
		error('Must have active shelf to create shelf button')

			
