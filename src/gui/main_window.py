from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QTabWidget, QListWidgetItem
from PyQt5.QtGui import QColor
from gui.code_widget import CodeWidget
from gui.projects_widget import ProjectsWidget
from gui.test_widget import TestWidget
from gui.diagram_widget import DiagramWidget
import time
from map import Task, TaskSystem

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.secure_namespace = {}
        self.tab_index = 0

    def initUI(self):
        self.setWindowTitle("Maximum Automatic Parallelization")
        self.setLayout(QHBoxLayout())

        self.projects_widget = ProjectsWidget(self)
        self.tabs = QTabWidget()
        self.code_widget = CodeWidget()
        self.diagram_widget = DiagramWidget()
        self.test_widget = TestWidget()

        self.tabs.addTab(self.code_widget, "Code Editor")
        self.tabs.addTab(self.diagram_widget, "Schema")
        self.tabs.addTab(self.test_widget, "Tests")

        self.tabs.tabBarClicked.connect(self.selectTab)

        self.layout().addWidget(self.projects_widget)
        self.layout().addWidget(self.tabs)

    def convertStringToCallable(self, code: str):
        assert type(code) is str, "Domain Error: String expected"
        try:
            exec("def converted_function():\n\t" + code.replace("\n", "\n\t") + "\n\tpass", self.secure_namespace)
            return self.secure_namespace["converted_function"]
        except:
            return None

    def getCodeContent(self):
        return self.code_widget.text_edit.toPlainText()

    def setCodeContent(self, code):
        self.code_widget.text_edit.setPlainText(code)
        self.tabs.setCurrentIndex(0)

    def compileTask(self, task_item: QListWidgetItem, task_code):
        if self.convertStringToCallable(task_code) is None:
            task_item.setForeground(QColor(0xFF0000))
        else:
            task_item.setForeground(QColor(0x00FF00))

    def createSystem(self):
        tasks = []
        for name, code in self.projects_widget.current_project.tasks.items():
            f = self.convertStringToCallable(code)
            if f is None:
                raise Exception("Undefined function")
            else:
                tasks.append(Task(name, f))
        return TaskSystem(tasks, namespace=self.secure_namespace)

    def parallelize(self):
        if self.projects_widget.current_project is None: return
        self.diagram_widget.drawGraph(self.createSystem())

    def selectTab(self, index):
        self.tab_index = index
        if index == 1:
            if self.projects_widget.current_project is not None and self.projects_widget.selected_task is not None:
                self.projects_widget.current_project.tasks[self.projects_widget.selected_task.text()] = self.getCodeContent()
            self.parallelize()
        elif index == 2:
            self.test_widget.compareSystemCost(self.createSystem())

    def __del__(self):
        if self.projects_widget.selected_task is not None:
            self.projects_widget.current_project.tasks[self.projects_widget.selected_task.text()] = self.getCodeContent()

def startMainWindow():
    app = QApplication([])
    window = MainWindow()
    window.show()
    return app.exec_()
