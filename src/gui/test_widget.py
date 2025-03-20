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
    def __init__(self):
        super().__init__()
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
        self.tasks_list.currentItemChanged.connect(self.onItemClick)

        self.layout().addWidget(self.tests_list)
        self.layout().addWidget(self.tasks_list)

    def onItemClick(self, item: QListWidgetItem):
        print(self.selected_task.text() if self.selected_task else "", item.text())
        self.selected_task = item
