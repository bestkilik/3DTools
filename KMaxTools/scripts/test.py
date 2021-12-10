import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtGui
import json
from pymxs import runtime as rt
# from PySide2 import shiboken2 as wrapInstance
# from ctypes import pythonapi, c_void_p, py_object

def maya_main_window():
	main_window_ptr = MaxPlus.GetQMaxMainWindow()
	return wrapInstance(long(main_window_ptr), QtGui.QWidget)

class KAnimTools(QtGui.QDialog):
	def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
		
		super(KAnimTools, self).__init__(parent)
		self.closeExistingWindow()
		self.create()
	
	def closeExistingWindow(self):
		try:
			for qt in MaxPlus.GetQMaxMainWindow().findChildren(QtGui.QDialog):
				if qt.__class__.__name__ == self.__class__.__name__:
					qt.close()
					qt.deleteLater()
			pass
		except:
			pass

	def create(self):
		self.setWindowTitle('K Anim Tools v1.0')
		self.setWindowFlags(QtCore.Qt.Tool)
		self.setMinimumSize(320,500)
		self.setMaximumSize(320,500)

		self.create_layout()
		self.show()
	
	def create_layout(self):
		baseLayout = QtGui.QVBoxLayout(self)
		tabWidget = QtGui.QTabWidget()
		baseLayout.addWidget(tabWidget)
		#-----------------------------
		select_tab = QtGui.QWidget()
		tabWidget.addTab(select_tab, "選擇工具")
		tabWidget.currentChanged.connect(self.doChageTab)

		#------------------------------
		save_tab = QtGui.QWidget()
		tabWidget.addTab(save_tab, "動作記錄")

		btnTest = QtGui.QPushButton('測試')
		btnTest.setParent(save_tab)
		btnTest.move(20,20)
		btnTest.clicked.connect(self.doTest)

		pass

	def doTest(self):
		# select = MaxPlus.SelectionManager.Nodes
		# selList = []

		# for o in select:
		# 	selList.append(o)
		# print(selList)
		xx = rt.getnodebyname('Sphere001')
		rt.select(xx)

		# for o in select:
		# 	print(o.Transform)
		pass

	def doChageTab(self, idx):
		if idx == 0:
			self.setMinimumHeight(500)
			self.setMaximumHeight(500)
		elif idx == 1:
			self.setMinimumHeight(300)
			self.setMaximumHeight(300)

if __name__ == "__main__":
	kAnim_ui = KAnimTools() 