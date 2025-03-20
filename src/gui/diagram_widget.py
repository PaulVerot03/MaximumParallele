from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class DiagramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.ax.set_title("Tasks")
        self.ax.legend(handles=self.ax.plot([], [], 'ro', label="Task") + self.ax.plot([], [], 'g-', label="Dependency"))

        self.layout().addWidget(self.canvas)