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
        # self.fig, self.ax = plt.subplots()
        # self.canvas = FigureCanvas(self.fig)
        # self.ax.set_title("Tasks")
        # self.ax.legend(handles=self.ax.plot([], [], 'ro', label="Task") + self.ax.plot([], [], 'g-', label="Dependency"))

        # self.layout().addWidget(self.canvas)

        def f(): return None
        T1 = Task("T1", f, ["1"], ["4"])
        T2 = Task("T2", f, ["3", "4"], ["1"])
        T3 = Task("T3", f, ["3", "4"], ["5"])
        T4 = Task("T4", f, ["4"], ["2"])
        T5 = Task("T5", f, ["5"], ["5"])
        T6 = Task("T6", f, ["1", "2"], ["4"])

        sys = TaskSystem([T1, T2, T3, T4, T5, T6], { T1: set(), T2: {T1}, T3: {T1}, T4: {T2, T3}, T5: {T3}, T6: {T4, T5} })

        # x_coords, y_coords = [], []
        # for i, layer in enumerate(sys.layers):
        #     x_coords += [i] * len(layer)
        #     for j, task in enumerate(layer):
        #         task.coords = (i, j)
        #         y_coords.append(j)
        #         self.ax.annotate(task.name, (i, j), (i+0.02, j+0.01)) # , arrowprops={"arrowstyle": '->'}

        # self.ax.plot(x_coords, y_coords, 'ro')

        # for task, deps in sys.dependencies.items():
        #     for dep in deps:
        #         self.ax.plot([task.coords[0], dep.coords[0]], [task.coords[1], dep.coords[1]], 'b-')

        self.canvas = FigureCanvas(plt.figure(figsize=(5, 4)))
        self.layout().addWidget(self.canvas)

        # Draw graph
        G = nx.DiGraph()
        for task, deps in sys.dependencies.items():
            for dep in deps:
                G.add_edge(dep.name, task.name)

        ax = self.canvas.figure.add_subplot(111)
        ax.clear()
        nx.draw(G, ax=ax, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        self.canvas.draw()