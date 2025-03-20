from PyQt5.QtWidgets import QVBoxLayout, QWidget, QComboBox, QListWidget, QListWidgetItem
import json
import os

class Project:
    def __init__(self, path: str): # Load
        with open(path, 'r') as f:
            project = json.loads(f.read())
            self.name = project["name"]
            self.tasks = project["tasks"]
        self.path = path

    def __del__(self): # Store
        project = { "name": self.name, "tasks": self.tasks }
        with open(self.path, 'w') as f:
            json.dump(project, f, indent=2)

class TestWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.projects: list[Project] = []
        self.selected_task = None

        for path in os.listdir("res/projects"):
            self.projects.append( Project("res/projects/" + path) )
        self.current_project: Project = None if self.projects is None else self.projects[0]

        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())

        self.tests_list = QComboBox()
        self.tests_list.addItems([project.name for project in self.projects])

        self.tasks_list = QListWidget()
        self.tasks_list.addItems([task for task in self.current_project.tasks or []])
        self.tasks_list.currentItemChanged.connect(self.selectItem)

        self.layout().addWidget(self.tests_list)
        self.layout().addWidget(self.tasks_list)

    def selectItem(self, item: QListWidgetItem):
        if self.selected_task is not None:
            code = self.current_project.tasks[self.selected_task.text()] = self.parent().getCodeContent()
            self.parent().compileTask(self.selected_task, code)
        self.selected_task = item
        self.parent().setCodeContent(self.current_project.tasks[item.text()])
