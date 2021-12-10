# -*- coding: utf-8 -*-
import os,sys
import maya.cmds as cmds
import maya.mel as mel
import shutil

def EnvSet(ToolRoot):
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

	plgFod = ToolRoot + '/scripts/'

	jfEnvSettingFile = plgFod + 'userSetup.mel'
	cpyDestJFEnvSettingFile = usrScrptFold + 'userSetup.mel'

	try:
		os.remove(cpyDestJFEnvSettingFile)
	except:
		pass

	shutil.copy2(jfEnvSettingFile, cpyDestJFEnvSettingFile)

	mel.eval("source \"" + cpyDestJFEnvSettingFile+"\"")

	cmds.upAxis(ax='z', rv=True)