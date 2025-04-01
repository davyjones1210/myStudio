from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

from publish import utils
from publish import broadcast

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.resize(400, 200)
        self.setWindowTitle("Publish Versions")
        self.verticallayout = QtWidgets.QVBoxLayout(self)
        self.label_header = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_header.setFont(font)
        self.label_header.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_header.setText("Publish domain versions")
        self.verticallayout.addWidget(self.label_header)
        self.gridLayout = QtWidgets.QGridLayout()
        self.verticallayout.addLayout(self.gridLayout)
        

        self.label_categories = QtWidgets.QLabel(self)
        self.label_categories.setText("Categories: ")
        self.label_categories.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_categories, 0, 0, 1, 1)

        print("\n", broadcast.getAllDomains())
        self.combobox_categorie = QtWidgets.QComboBox(self)
        self.combobox_categorie.addItems(broadcast.getAllDomains())

        category, index = broadcast.getCategoryFromDomain(utils.environmantValue("DOMAIN_NAME"))
        self.combobox_categorie.setCurrentIndex(index)
        
        self.gridLayout.addWidget(self.combobox_categorie, 0, 1, 1, 1)
 
        # Project Abbreviation
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setText("Domain name: ")
        self.label_name.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_name, 1, 0, 1, 1)
    
        self.lineedit_name = QtWidgets.QLineEdit(self)
        self.lineedit_name.setText(utils.environmantValue("DOMAIN_NAME"))
        self.gridLayout.addWidget(self.lineedit_name, 1, 1, 1, 1)
        
        self.label_department = QtWidgets.QLabel(self)
        self.label_department.setText("Department: ")
        self.label_department.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_department, 2, 0, 1, 1)

        self.combobox_department = QtWidgets.QComboBox(self)
        self.gridLayout.addWidget(self.combobox_department, 2, 1, 1, 1)

        # category, name, department, typed
        self.label_typed = QtWidgets.QLabel(self)
        self.label_typed.setText("Typed: ")
        self.label_typed.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_typed, 3, 0, 1, 1)

        self.combobox_typed = QtWidgets.QComboBox(self)
        self.gridLayout.addWidget(self.combobox_typed, 3, 1, 1, 1)


        # Description
        self.label_comments = QtWidgets.QLabel(self)
        self.label_comments.setMinimumSize(QtCore.QSize(100, 0))
        self.label_comments.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_comments.setText("Comments")
        self.gridLayout.addWidget(self.label_comments, 4, 0, 1, 1)

        self.lineedit_comments = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.lineedit_comments, 4, 1, 1, 1)
        
        # Create Button
        self.pushbutton_publish = QtWidgets.QPushButton(self)
        self.pushbutton_publish.setText("Publish")
        self.gridLayout.addWidget(self.pushbutton_publish, 5, 1, 1, 1)
        self.pushbutton_publish.clicked.connect(self.publishVersion)
 
    
    def publishVersion(self):
        input = {
            "name": self.lineedit_name.text(),
            "abbreviation": self.lineedit_abbreviation.text(),
            "createdBy": getpass.getuser(),
            "description": self.lineedit_description.text(),
        }


        # Get all the inputs from the maya gui and pass it to main.py and 
        # pick all arguments and execute there
  