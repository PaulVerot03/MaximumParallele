from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QTabWidget, QListWidgetItem
from PyQt5.QtGui import QColor
from gui.code_widget import CodeWidget
from gui.test_widget import TestWidget
from gui.diagram_widget import DiagramWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.secure_namespace = {}

    def initUI(self):
        self.setWindowTitle("Maximum Paralallllllllllllllllllllllllllllllllllllllllllllll")
        self.setLayout(QHBoxLayout())

        self.test_widget = TestWidget(self)
        self.tabs = QTabWidget()
        self.code_widget = CodeWidget()
        self.diagram_widget = DiagramWidget()

        self.tabs.addTab(self.code_widget, "Code Editor")
        self.tabs.addTab(self.diagram_widget, "Schema")

        self.layout().addWidget(self.test_widget)
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

    def __del__(self):
        if self.test_widget.selected_task is not None:
            self.test_widget.current_project.tasks[self.test_widget.selected_task.text()] = self.getCodeContent()

def startMainWindow():
    app = QApplication([])
    window = MainWindow()
    window.show()
    return app.exec_()
