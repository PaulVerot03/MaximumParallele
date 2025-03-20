from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QTabWidget
from gui.code_widget import CodeWidget
from gui.test_widget import TestWidget
from gui.diagram_widget import DiagramWidget

class HighlighterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.secure_namespace = {}

    def initUI(self):
        self.setWindowTitle("Maximum Paralallllllllllllllllllllllllllllllllllllllllllllll")
        self.setLayout(QHBoxLayout())

        self.test_widget = TestWidget()
        self.tabs = QTabWidget()
        self.code_widget = CodeWidget()
        self.diagram_widget = DiagramWidget()

        self.tabs.addTab(self.code_widget, "Code Editor")
        self.tabs.addTab(self.diagram_widget, "Schema")

        self.layout().addWidget(self.test_widget)
        self.layout().addWidget(self.tabs)

    def convertStringToCallable(self, code: str):
        assert type(code) is str, "Domain Error: String expected"
        exec("def converted_function():\n\t" + code.replace("\n", "\n\t") + "\n\tpass", self.secure_namespace)
        return self.secure_namespace["converted_function"]

def startMainWindow():
    app = QApplication([])
    window = HighlighterApp()
    window.show()
    return app.exec_()
