from PySide6 import QtGui, QtCore, QtWidgets
from publish import main
import importlib
import getpass
import sys
import os
from publish import utils
from publish import broadcast
from tools import create_entries
importlib.reload(create_entries)

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # Set up the main window
        self.resize(400, 400)
        self.setWindowTitle("Publish Versions")

        # Create the main layout
        self.verticallayout = QtWidgets.QVBoxLayout(self)

        # Header label
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

        # Grid layout for input fields
        self.gridLayout = QtWidgets.QGridLayout()
        self.verticallayout.addLayout(self.gridLayout)

        # Project input
        self.label_project = QtWidgets.QLabel(self)
        self.label_project.setText("Project: ")
        self.label_project.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_project, 0, 0, 1, 1)

        self.label_project_value = QtWidgets.QLabel(self)
        self.label_project_value.setText(os.environ["PROJECT_NAME"])  # Replace with actual project name
        self.gridLayout.addWidget(self.label_project_value, 0, 1, 1, 1)

        # Artist input
        self.label_artist = QtWidgets.QLabel(self)
        self.label_artist.setText("Artist: ")
        self.label_artist.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_artist, 1, 0, 1, 1)

        self.label_artist_value = QtWidgets.QLabel(self)
        self.label_artist_value.setText(getpass.getuser())  # Automatically fill with the current user's name
        self.gridLayout.addWidget(self.label_artist_value, 1, 1, 1, 1)

        # Category input
        self.label_categories = QtWidgets.QLabel(self)
        self.label_categories.setText("Categories: ")
        self.label_categories.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_categories, 2, 0, 1, 1)

        self.combobox_categorie = QtWidgets.QComboBox(self)
        self.gridLayout.addWidget(self.combobox_categorie, 2, 1, 1, 1)
        self.populateCategories()

        # Name input
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setText("Name: ")
        self.label_name.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_name, 3, 0, 1, 1)

        self.lineedit_name = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.lineedit_name, 3, 1, 1, 1)

        # Department input
        self.label_department = QtWidgets.QLabel(self)
        self.label_department.setText("Department: ")
        self.label_department.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_department, 4, 0, 1, 1)

        self.combobox_department = QtWidgets.QComboBox(self)
        self.gridLayout.addWidget(self.combobox_department, 4, 1, 1, 1)
        self.populateDepartments()

        # Type input
        self.label_typed = QtWidgets.QLabel(self)
        self.label_typed.setText("Typed: ")
        self.label_typed.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_typed, 5, 0, 1, 1)

        self.combobox_typed = QtWidgets.QComboBox(self)
        self.combobox_typed.addItems(["sourcefile", "usdFile", "alembicFile", "mp4File", "movFile"])
        self.gridLayout.addWidget(self.combobox_typed, 5, 1, 1, 1)

        # Comments input
        self.label_comments = QtWidgets.QLabel(self)
        self.label_comments.setMinimumSize(QtCore.QSize(100, 0))
        self.label_comments.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_comments.setText("Comments")
        self.gridLayout.addWidget(self.label_comments, 6, 0, 1, 1)

        self.lineedit_comments = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.lineedit_comments, 6, 1, 1, 1)

        # Publish button
        self.pushbutton_publish = QtWidgets.QPushButton(self)
        self.pushbutton_publish.setText("Publish")
        self.gridLayout.addWidget(self.pushbutton_publish, 7, 1, 1, 1)
        self.pushbutton_publish.clicked.connect(self.publishVersion)

    def populateCategories(self):
        """
        Populate the category combobox with values from the category table in the database.
        """
        entry_creator = create_entries.CreateDomainWidget()  # Create an instance of the CreateDomainWidget class
        categories = entry_creator.populateCategories()  # Call the populateCategories method

        if categories:
            for category in categories:
                self.combobox_categorie.addItem(category['name'])
        else:
            QtWidgets.QMessageBox.warning(self, "Database Error", "No categories found in the database.")

    def populateDepartments(self):
        """
        Populate the department combobox with values from the department table in the database.
        """
        entry_creator = create_entries.CreateDomainWidget()  # Create an instance of the CreateDomainWidget class
        departments = entry_creator.populateDepartments()  # Call the populateDepartments method

        if departments:
            for department in departments:
                self.combobox_department.addItem(department['name'])
        else:
            QtWidgets.QMessageBox.warning(self, "Database Error", "No departments found in the database.")

    def publishVersion(self):
        # Get input values
        project = self.label_project_value.text()
        artist = self.label_artist_value.text()
        category = self.combobox_categorie.currentText()
        name = self.lineedit_name.text()
        department = self.combobox_department.currentText()
        typed = self.combobox_typed.currentText()
        comments = self.lineedit_comments.text()

        # Check if all fields are filled out
        if not project or not artist or not category or not name or not department or not typed:
            QtWidgets.QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
            return

        try:
            # Reload the main module and set PUBLISH_DCC
            importlib.reload(main)
            main.PUBLISH_DCC = "maya"
            result = main.sourceFile(category, name, department, typed, comments)
            
            QtWidgets.QMessageBox.information(self, "Success", f"Successfully published: {result}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())


# from tools import publishGUI
# import importlib
# importlib.reload(publishGUI)

# widget = publishGUI.Widget()
# widget.show()