from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx

from map import TaskSystem, Task

class DiagramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())

        self.canvas = FigureCanvas(plt.figure(figsize=(5, 4)))
        self.layout().addWidget(self.canvas)

        self.ax = self.canvas.figure.add_subplot()

    def drawGraph(self, sys):
        self.ax.clear()

        G = nx.DiGraph()
        for task in sys.tasks:
            G.add_node(task.name, layer=task.layer)
        for task, deps in sys.dependencies.items():
            for dep in deps:
                G.add_edge(dep.name, task.name)

        pos = nx.multipartite_layout(G, subset_key="layer") # shell_layout(G) multipartite_layout(G, subset_key="layer")
        nx.draw(G, pos=pos, ax=self.ax, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)

        x_values, y_values = zip(*pos.values())
        margin = 0.25
        self.ax.set_xlim(min(x_values) - margin, max(x_values) + margin)
        self.ax.set_ylim(min(y_values) - margin, max(y_values) + margin)
        self.ax.set_aspect('equal')
        self.canvas.draw()
