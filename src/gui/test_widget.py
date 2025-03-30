from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import time

class TestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())

        self.canvas = FigureCanvas(plt.figure(tight_layout=True)) # figsize=(5, 4)
        self.layout().addWidget(self.canvas)

        self.ax = self.canvas.figure.add_subplot()

    # allow the program to calculate the time taken by each task sequence
    def compareSystemCost(self, sys):
        start = time.time()
        sys.runSequence()
        seq_time = time.time() - start

        start = time.time()
        sys.run_layers()
        par_time = time.time() - start

        print(f"Temps séquentiel: {seq_time:.5f}s, Temps parallèle: {par_time:.5f}s")

        self.ax.clear()
        self.ax.barh((0, 1), [seq_time, par_time])
        self.ax.set_yticks((0, 1), labels=('Parallel', 'Sequential'))
        self.ax.set_xlim(0, max(seq_time, par_time))
        self.ax.set_xlabel("Time (s)")

        self.canvas.draw()