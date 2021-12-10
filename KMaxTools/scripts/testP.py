from PySide2 import QtCore
from PySide2 import QtWidgets
import MaxPlus
import pymxs

class PyMaxDialog(QtWidgets.QDialog):
    def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
        super(PyMaxDialog, self).__init__(parent)
        self.setWindowTitle('Pyside Qt Window')
        main_layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Click button to create a cylinder in the scene")
        main_layout.addWidget(label)
        
        edit_box = QtWidgets.QLineEdit("Cyl Name")
        main_layout.addWidget(edit_box)

        cylinder_btn = QtWidgets.QPushButton("Cylinder")
        cylinder_btn.clicked.connect(self.make_cylinder)
        main_layout.addWidget(cylinder_btn)
        
        self.setLayout(main_layout)
        self.resize(250, 100)           
        
    def make_cylinder(self):
        #~ cyl_name = self.findChild(QtWidgets.QLineEdit).text()
        #~ cyl = pymxs.runtime.Cylinder(radius=10, height=30, name=cyl_name)
        #~ pymxs.runtime.redrawViews() 
        #~ MaxPlus.Core.EvalMAXScript('filein "E:\CloudDrive\Dropbox\tools\KMaxTools\scripts\BipedGuide.ms"')
		MaxPlus.Core.EvalMAXScript('print "test"')
		MaxPlus.Core.EvalMAXScript('fileIn "E:/CloudDrive/Dropbox/tools/KMaxTools/scripts/BipedGuide.ms"')

def main():
    w = PyMaxDialog()
    w.show()

if __name__ == '__main__':
    main()