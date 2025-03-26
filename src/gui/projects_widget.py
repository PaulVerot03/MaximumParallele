from PyQt5.QtWidgets import QVBoxLayout, QWidget, QComboBox, QListWidget, QListWidgetItem, QInputDialog
import json
import os

class Project:
    def __init__(self, name: str):
        self.name = name
        self.tasks = {}
        self.path = "res/projects/" + name + ".json"

    def load(self):
        with open(self.path, 'r') as f:
            project = json.loads(f.read())
            self.name = project["name"]
            self.tasks = project["tasks"]
        return self

    def __del__(self): # Store
        project = { "name": self.name, "tasks": self.tasks }
        with open(self.path, 'w') as f:
            json.dump(project, f, indent=2)

class ProjectsWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.projects: list[Project] = []
        self.selected_task = None

        for path in os.listdir("res/projects"):
            self.projects.append( Project(path.replace(".json", "")).load() )
        self.current_project: Project = None

        self.initUI()
        self.loadProject(0)

    def initUI(self):
        self.setLayout(QVBoxLayout())

        self.tests_list = QComboBox()
        self.tests_list.addItems(["NEW PROJECT"] + [project.name for project in self.projects])
        self.previous_project_index = 1 if len(self.projects) > 0 else 0
        self.tests_list.setCurrentIndex(self.previous_project_index)
        self.tests_list.currentIndexChanged.connect(self.selectProject)

        self.tasks_list = QListWidget()
        if self.projects == []:
            self.tasks_list.addItem("CREATE FIRST PROJECT")
            self.tasks_list.currentItemChanged.connect(self.firstProject)
        else:
            self.tasks_list.currentItemChanged.connect(self.selectItem)
        self.tasks_list.itemPressed.connect(self.newTask)

        self.layout().addWidget(self.tests_list)
        self.layout().addWidget(self.tasks_list)

    def loadProject(self, index):
        if index < 0 or index >= len(self.projects):
            return
        self.selected_task = None
        self.current_project = self.projects[index]
        self.tasks_list.clear()
        self.tasks_list.addItems(["NEW TASK"] + [task for task in self.current_project.tasks])

    def firstProject(self, item: QListWidgetItem):
        if item is None or item.text() != "CREATE FIRST PROJECT": return
        print(item.text())
        self.tasks_list.currentItemChanged.connect(lambda _: None)
        self.selectProject(0)
        self.tasks_list.currentItemChanged.connect(self.selectItem if len(self.projects) > 0 else self.firstProject)

    def selectProject(self, index):
        if index == 0:
            name, ok = QInputDialog().getText(self, "New project", "Project's name:")
            if ok and name and all([project.name != name for project in self.projects]):
                self.projects.append( Project(name) )
                self.tests_list.addItem(name)
                self.tests_list.setCurrentIndex(self.tests_list.count() - 1)
            else:
                self.tests_list.setCurrentIndex(self.previous_project_index)
                return
        self.loadProject(index - 1)
        self.previous_project_index = index - 1

    def selectItem(self, item: QListWidgetItem):
        if item is None or item.text() == "NEW TASK": return
        if self.selected_task is not None:
            code = self.current_project.tasks[self.selected_task.text()] = self.parent().getCodeContent()
            self.parent().compileTask(self.selected_task, code)
        self.selected_task = item
        self.parent().setCodeContent(self.current_project.tasks[item.text()])

    def newTask(self, item):
        if item is None or item.text() != "NEW TASK": return
        name, ok = QInputDialog().getText(self, "New Task", "Task's name:")
        if not ok or name == "" or name in self.current_project.tasks:
            return
        self.current_project.tasks[name] = ""
        self.tasks_list.addItem(name)
        self.tasks_list.setCurrentItem(self.tasks_list.item(self.tasks_list.count() - 1))