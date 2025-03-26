from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx

class TestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())

        self.canvas = FigureCanvas(plt.figure(figsize=(5, 4)))
        self.layout().addWidget(self.canvas)

        self.ax = self.canvas.figure.add_subplot()