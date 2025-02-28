import getpass
from PySide6 import QtGui, QtCore, QtWidgets
import datetime
import bin.utils as bin_utils
from publish import broadcast
from publish.database import myDatabase
# This should not happen because we want to follow some disciple to see what comes from where.


class CreateProjectWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CreateProjectWidget, self).__init__(parent)
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
        
        # Project Name
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setText("Project Name: ")
        self.label_name.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.lineedit_name = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.lineedit_name, 0, 1, 1, 1)
        
        # Project Abbreviation
        self.label_abbreviation = QtWidgets.QLabel(self)
        self.label_abbreviation.setText("Project Abbreviation: ")
        self.label_abbreviation.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_abbreviation, 1, 0, 1, 1)
        self.lineedit_abbreviation = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.lineedit_abbreviation, 1, 1, 1, 1)
        
        # Description
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
        
        # Create Button
        self.pushbutton_create = QtWidgets.QPushButton(self)
        self.pushbutton_create.setText("Create")
        self.gridLayout.addWidget(self.pushbutton_create, 3, 1, 1, 1)
        self.pushbutton_create.clicked.connect(self.createProject)
    
    def createProject(self):
        input = {
            "name": self.lineedit_name.text(),
            "abbreviation": self.lineedit_abbreviation.text(),
            "createdBy": getpass.getuser(),
            "createdAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": self.lineedit_description.text(),
        }
        import importlib
        importlib.reload(broadcast)
        broadcast._register_("projects",  input) 
        self.close()  # Close the CreateProjectWidget window after creating the project
 
class CreateArtistWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CreateArtistWidget, self).__init__(parent)
        self.resize(400, 200)
        self.setWindowTitle("Create a new artist")
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
        self.label_header.setText("Create a new Artist")
        self.verticallayout.addWidget(self.label_header)
        self.gridLayout = QtWidgets.QGridLayout()
        self.verticallayout.addLayout(self.gridLayout)
        
        # Artist Name
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setText("Artist Name: ")
        self.label_name.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.lineedit_name = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.lineedit_name, 0, 1, 1, 1)
        
        # Artist Email
        self.label_email = QtWidgets.QLabel(self)
        self.label_email.setText("Artist Email: ")
        self.label_email.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_email, 1, 0, 1, 1)
        self.lineedit_email = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.lineedit_email, 1, 1, 1, 1)
        
        # Artist Password
        self.label_password = QtWidgets.QLabel(self)
        self.label_password.setText("Artist Password: ")
        self.label_password.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_password, 2, 0, 1, 1)
        self.lineedit_password = QtWidgets.QLineEdit(self)
        self.lineedit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gridLayout.addWidget(self.lineedit_password, 2, 1, 1, 1)
        
        # Create Button
        self.pushbutton_create = QtWidgets.QPushButton(self)
        self.pushbutton_create.setText("Create")
        self.gridLayout.addWidget(self.pushbutton_create, 3, 1, 1, 1)
        self.pushbutton_create.clicked.connect(self.createArtist)
    
    def createArtist(self):
        input = {
            "name": self.lineedit_name.text(),
            "email": self.lineedit_email.text(),
            "password": self.lineedit_password.text(),
        }
        import importlib
        importlib.reload(broadcast)
        broadcast._register_("artists",  input) 
        self.close()  # Close the CreateArtistWidget window after creating the artist


class CreateCategoryWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CreateCategoryWidget, self).__init__(parent)
        self.resize(400, 200)
        self.setWindowTitle("Create a new category")
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
        self.label_header.setText("Create a new Category")
        self.verticallayout.addWidget(self.label_header)
        self.gridLayout = QtWidgets.QGridLayout()
        self.verticallayout.addLayout(self.gridLayout)
        
        # Category Name
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setText("Category Name: ")
        self.label_name.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.lineedit_name = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.lineedit_name, 0, 1, 1, 1)
        
        # Create Button
        self.pushbutton_create = QtWidgets.QPushButton(self)
        self.pushbutton_create.setText("Create")
        self.gridLayout.addWidget(self.pushbutton_create, 1, 1, 1, 1)
        self.pushbutton_create.clicked.connect(self.createCategory)
    
    def createCategory(self):
        input = {
            "name": self.lineedit_name.text(),
        }
        import importlib
        importlib.reload(broadcast)
        broadcast._register_("category",  input) 
        self.close()  # Close the CreateCategoryWidget window after creating the category

class CreateDomainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CreateDomainWidget, self).__init__(parent)
        self.resize(400, 200)
        self.setWindowTitle("Create a new domain")
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
        self.label_header.setText("Create a new Domain")
        self.verticallayout.addWidget(self.label_header)
        self.gridLayout = QtWidgets.QGridLayout()
        self.verticallayout.addLayout(self.gridLayout)
        
        # Domain Name
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setText("Domain Name: ")
        self.label_name.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.lineedit_name = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.lineedit_name, 0, 1, 1, 1)
        
        # Category Dropdown
        self.label_category = QtWidgets.QLabel(self)
        self.label_category.setText("Category: ")
        self.label_category.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_category, 1, 0, 1, 1)
        self.combobox_category = QtWidgets.QComboBox(self)
        self.gridLayout.addWidget(self.combobox_category, 1, 1, 1, 1)
        
        # Department Dropdown
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
        
        # Project Dropdown
        self.label_project = QtWidgets.QLabel(self)
        self.label_project.setText("Project: ")
        self.label_project.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_project, 3, 0, 1, 1)
        self.combobox_project = QtWidgets.QComboBox(self)
        self.gridLayout.addWidget(self.combobox_project, 3, 1, 1, 1)
        
        # Populate the category, department, and project dropdowns
        self.populateCategories()
        self.populateDepartments()
        self.populateProjects()
        
        # Create Button
        self.pushbutton_create = QtWidgets.QPushButton(self)
        self.pushbutton_create.setText("Create")
        self.gridLayout.addWidget(self.pushbutton_create, 4, 1, 1, 1)
        self.pushbutton_create.clicked.connect(self.createDomain)
    
    def populateCategories(self):
        db = myDatabase()
        categories = db.query("category", "name")
        
        # Add categories to the combobox
        for category in categories:
            self.combobox_category.addItem(category['name'])
    
    def populateDepartments(self):
        db = myDatabase()
        departments = db.query("departments", "name")
        
        # Add departments to the combobox
        for department in departments:
            self.combobox_department.addItem(department['name'])
    
    def populateProjects(self):
        db = myDatabase()
        projects = db.query("projects", "id, name")
        
        # Store project IDs and names
        self.project_ids = {}
        for project in projects:
            self.combobox_project.addItem(project['name'])
            self.project_ids[project['name']] = project['id']
    
    def createDomain(self):
        input = {
            "name": self.lineedit_name.text(),
            "category": self.combobox_category.currentText(),
            "department": self.combobox_department.currentText(),
            "project_id": self.project_ids[self.combobox_project.currentText()]
        }
        import importlib
        importlib.reload(broadcast)
        broadcast._register_("domains",  input) 
        self.close()  # Close the CreateDomainWidget window after creating the domain
                
class LoadDCCWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LoadDCCWidget, self).__init__(parent)
        self.resize(400, 200)
        self.setWindowTitle("Load DCC")
        self.verticallayout = QtWidgets.QVBoxLayout(self)
        self.label_header = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label_header.setFont(font)
        self.label_header.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.label_header.setText("Load DCC")
        self.verticallayout.addWidget(self.label_header)
        
        self.gridLayout = QtWidgets.QGridLayout()
        self.verticallayout.addLayout(self.gridLayout)
        
        # DCC Dropdown
        self.label_dcc = QtWidgets.QLabel(self)
        self.label_dcc.setText("DCC: ")
        self.label_dcc.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_dcc, 0, 0, 1, 1)
        self.combobox_dcc = QtWidgets.QComboBox(self)
        self.combobox_dcc.addItems(["Maya", "Blender"])
        self.gridLayout.addWidget(self.combobox_dcc, 0, 1, 1, 1)
        
        # Project Dropdown
        self.label_project = QtWidgets.QLabel(self)
        self.label_project.setText("Project: ")
        self.label_project.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_project, 1, 0, 1, 1)
        self.combobox_project = QtWidgets.QComboBox(self)
        self.gridLayout.addWidget(self.combobox_project, 1, 1, 1, 1)
        
        # Domain Dropdown
        self.label_domain = QtWidgets.QLabel(self)
        self.label_domain.setText("Domain: ")
        self.label_domain.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.gridLayout.addWidget(self.label_domain, 2, 0, 1, 1)
        self.combobox_domain = QtWidgets.QComboBox(self)
        self.gridLayout.addWidget(self.combobox_domain, 2, 1, 1, 1)
        
        # Populate the project and domain dropdowns
        self.populateProjects()
        self.populateDomains()
        
        # Load Button
        self.pushbutton_load = QtWidgets.QPushButton(self)
        self.pushbutton_load.setText("Load")
        self.gridLayout.addWidget(self.pushbutton_load, 3, 1, 1, 1)
        self.pushbutton_load.clicked.connect(self.loadDCC)
    
    def populateProjects(self):
        db = myDatabase()
        projects = db.query("projects", "name")
        
        # Add projects to the combobox
        for project in projects:
            self.combobox_project.addItem(project['name'])
    
    def populateDomains(self):
        db = myDatabase()
        domains = db.query("domains", "name")
        
        # Add domains to the combobox
        for domain in domains:
            self.combobox_domain.addItem(domain['name'])
    
    def loadDCC(self):
        dcc = self.combobox_dcc.currentText().lower()
        if dcc == "blender":
            dcc = "blender4.0"
        project = self.combobox_project.currentText()
        domain = self.combobox_domain.currentText()
        
        # Check if the project exists
        if broadcast.checkIfProjectExistsInDB(project):
            # Placeholder for the load DCC logic
            print(f"Loading {dcc} for project {project} and domain {domain}")
            bin_utils.triggerOpen(dcc)


class MainMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainMenu, self).__init__(parent)
        self.resize(400, 200)
        self.setWindowTitle("Main Menu")
        self.verticallayout = QtWidgets.QVBoxLayout(self)
        self.label_header = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label_header.setFont(font)
        self.label_header.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.label_header.setText("Main Menu")
        self.verticallayout.addWidget(self.label_header)
        self.gridLayout = QtWidgets.QGridLayout()
        self.verticallayout.addLayout(self.gridLayout)
        self.pushbutton_create_project = QtWidgets.QPushButton(self)
        self.pushbutton_create_project.setText("Create Project")
        self.gridLayout.addWidget(self.pushbutton_create_project, 0, 0, 1, 1)
        self.pushbutton_create_project.clicked.connect(self.openCreateProject)
        self.pushbutton_create_artist = QtWidgets.QPushButton(self)
        self.pushbutton_create_artist.setText("Create Artist")
        self.gridLayout.addWidget(self.pushbutton_create_artist, 1, 0, 1, 1)
        self.pushbutton_create_artist.clicked.connect(self.openCreateArtist)
        self.pushbutton_create_domain = QtWidgets.QPushButton(self)
        self.pushbutton_create_domain.setText("Create Domain")
        self.gridLayout.addWidget(self.pushbutton_create_domain, 2, 0, 1, 1)
        self.pushbutton_create_domain.clicked.connect(self.openCreateDomain)
        self.pushbutton_create_category = QtWidgets.QPushButton(self)
        self.pushbutton_create_category.setText("Create Category")
        self.gridLayout.addWidget(self.pushbutton_create_category, 3, 0, 1, 1)
        self.pushbutton_create_category.clicked.connect(self.openCreateCategory)
        self.pushbutton_load_dcc = QtWidgets.QPushButton(self)
        self.pushbutton_load_dcc.setText("Load DCC")
        self.gridLayout.addWidget(self.pushbutton_load_dcc, 4, 0, 1, 1)
        self.pushbutton_load_dcc.clicked.connect(self.openLoadDCC)

    def openCreateProject(self):
        self.create_project_widget = CreateProjectWidget()
        self.create_project_widget.show()
    
    def openCreateArtist(self):
        self.create_artist_widget = CreateArtistWidget()
        self.create_artist_widget.show()
    
    def openCreateDomain(self):
        self.create_domain_widget = CreateDomainWidget()
        self.create_domain_widget.show()
    
    def openCreateCategory(self):
        self.create_category_widget = CreateCategoryWidget()
        self.create_category_widget.show()

    def openLoadDCC(self):
        self.load_dcc_widget = LoadDCCWidget()
        self.load_dcc_widget.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec())

    # application = QtWidgets.QApplication(sys.argv)
    # widget = Widget(parent=None)
    # widget.show()
    # sys.exit(application.exec())
