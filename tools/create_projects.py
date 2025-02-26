from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

from publish import broadcast

class Widget(QtWidgets.QWidget):

    def __init__(self, parent=None, **kwargs):
        super(Widget, self).__init__(parent)

        self.resize(400, 200)
        self.setWindowTitle("Create a new show")


        self.verticallayout = QtWidgets.QVBoxLayout(self)


        self.label_header = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)

        self.label_header.setFont(font)
        self.label_header.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_header.setText("Create a new Project (show)")
        self.verticallayout.addWidget(self.label_header)



        self.gridLayout = QtWidgets.QGridLayout()
        self.verticallayout.addLayout(self.gridLayout)

        self.label_longname = QtWidgets.QLabel(self)
        self.label_longname.setText("Long Name: ")
        self.label_longname.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_longname, 0, 0, 1, 1)

        self.lineedit_longname = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.lineedit_longname, 0, 1, 1, 1)

        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setText("Name: ")
        self.label_name.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_name, 1, 0, 1, 1)

        self.lineedit_name = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.lineedit_name, 1, 1, 1, 1)

        self.label_description = QtWidgets.QLabel(self)

        self.label_description.setMinimumSize(QtCore.QSize(100, 0))
        self.label_description.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_description.setText("Description")
        self.gridLayout.addWidget(self.label_description, 2, 0, 1, 1)

        self.lineedit_description = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.lineedit_description, 2, 1, 1, 1)

        self.pushbutton_create = QtWidgets.QPushButton(self)
        self.pushbutton_create.setText("Create")
        self.gridLayout.addWidget(self.pushbutton_create, 3, 1, 1, 1)

        self.pushbutton_create.clicked.connect(self.createProject)
    
    def createProject(self):
        input = {
            # "longname": self.lineedit_longname.text(),
            "name": self.lineedit_name.text(),
            "description": self.lineedit_description.text(),
        }

        import importlib
        importlib.reload(broadcast)
        
        broadcast._register_("project",  input)  




if __name__ == "__main__":

    import sys

    application = QtWidgets.QApplication(sys.argv)
    widget = Widget(parent=None)
    widget.show()
    sys.exit(application.exec())
