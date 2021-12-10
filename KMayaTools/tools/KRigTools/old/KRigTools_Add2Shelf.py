# -*- coding: utf-8 -*-
import os,sys
import maya.cmds as cmds
import maya.mel as mel
import shutil

def Install(ToolRoot):
	usd = cmds.internalVar(usd=True)
	usrFold = usd[:-8]
	usrPlugFold = usrFold+"plugins/"
	usrScrptFold = usrFold+"scripts/"
	usrImgFold = usrFold+"prefs/icons/"

	#if plugins folder not exist, create one
	if( not os.path.exists(usrPlugFold )):
		os.makedirs(usrPlugFold)

	#get maya version
	mVer = (os.path.dirname(sys.prefix).split('/'))[-1]

	plgFod = ToolRoot + '/'

	JFRigToolFile = plgFod + 'KRigTools.py'
	cpyDestJFRigToolFile = usrScrptFold + 'KRigTools.py'

	try:
		os.remove(cpyDestJFRigToolFile)
	except:
		try:
			os.chmod(cpyDestJFRigToolFile, 755)
			os.remove(cpyDestJFRigToolFile)
		except :
			pass


	shutil.copy2(JFRigToolFile, cpyDestJFRigToolFile)

	g_ShelfTopLevel = mel.eval("$Temp = $gShelfTopLevel") # 取得maya global: gShelfTopLevel
	if cmds.tabLayout(g_ShelfTopLevel, q = True, ex = True):
		_tab = cmds.tabLayout(g_ShelfTopLevel,q=True,st=True)
		shelfButtons = cmds.shelfLayout(_tab , q=True, ca=True )
		
		if(shelfButtons):
			for btn in shelfButtons:
				if(cmds.control(btn,ex=True)):
					sfbtn = cmds.shelfButton(btn,q=True,annotation=True)
					if( sfbtn == "Open KRigTools" ):
						cmds.deleteUI(btn)