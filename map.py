import networkx as nx
import matplotlib.pyplot as plt
import time
import threading
from typing import List, Dict, Callable

class Task:
    def __init__(self, name: str, run: Callable, reads: List[str] = None, writes: List[str] = None):
        assert type(name) is str and type(run).__name__ == "function", "Domain error"
        self.name = name
        self.run = run
        self.reads = set(reads if reads else run.__code__.co_names)
        self.writes = set(writes if writes else run.__code__.co_names)
    def __repr__(self):
        return '&' + self.name

class TaskSystem:
    def __init__(self, tasks: list[Task], precedence: dict[Task, set[Task]]=None):
        self.tasks = tasks
        if precedence is not None:
            self.dependencies = precedence
            self.validate()
            print(self.isDeterministic())
        self.maximizeParalization()

    def maximizeParalization(self): # Complexity: O(n*log(n)) ?
        tasks: list[tuple[set[str], set[str]]] = [] # (deps, all_deps: set(str))
        for i, task1 in enumerate(self.tasks):
            deps, all_deps = set(), set()
            for j, task2 in enumerate(self.tasks[:i][::-1]):
                if task2 not in all_deps and (task1.writes & (task2.writes | task2.reads) or task2.writes & task1.reads):
                    deps.add(task2)
                    all_deps.update((task2,), tasks[i - j - 1][1])
            tasks.append( (deps, all_deps) )
        self.dependencies = { self.tasks[i]: tasks[i][0] for i in range(len(tasks)) }

    def isDeterministic(self):
        assert (type(self.dependencies) is dict)
        tasks = [set() for _ in range(len(self.tasks))]
        for i, task1 in enumerate(self.tasks):
            for j, task2 in enumerate(self.tasks[:i][::-1]):
                if (task1.writes & (task2.writes | task2.reads) or task2.writes & task1.reads):
                    tasks[i].update((task2,), tasks[i - j - 1])
            print(self.dependencies[task1], tasks[i])
            if not tasks[i].issubset(self.dependencies[task1]):
                return "Error"

    def validate(self):
        # Vérifier que toutes les tâches dans precedence existent
        for task, deps in self.dependencies.items():
            if task not in self.tasks:
                raise ValueError(f"Tâche inconnue: {task}")
            for dep in deps:
                if dep not in self.tasks:
                    raise ValueError(f"Dépendance inconnue: {dep}")
        print("Validation réussie !")

    def get_dependencies(self, task_name: str):
        return self.precedence.get(task_name, [])

    def run_seq(self):
        for task in self.tasks:
            task.run()

    def run(self):
        threads = {}
        executed = set()

        def execute_parallel(task_name):
            for dep in self.get_dependencies(task_name):
                if dep not in executed:
                    return  # Attendre que la dépendance soit exécutée
            print(f"Exécution parallèle: {task_name}")
            self.tasks[task_name].run()
            executed.add(task_name)

        for task_name in self.tasks:
            threads[task_name] = threading.Thread(target=execute_parallel, args=(task_name,))

        for task_name in self.precedence:
            threads[task_name].start()

        for task_name in self.precedence:
            threads[task_name].join()

    def draw(self):
        G = nx.DiGraph()
        for task, deps in self.precedence.items():
            for dep in deps:
                G.add_edge(dep, task)
        nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        plt.show()

    def par_cost(self):
        start = time.time()
        self.run_seq()
        seq_time = time.time() - start

        start = time.time()
        self.run()
        par_time = time.time() - start

        print(f"Temps séquentiel: {seq_time:.5f}s, Temps parallèle: {par_time:.5f}s")


def f(): return

T1 = Task("T1", f, ["1"], ["4"])
T2 = Task("T2", f, ["3", "4"], ["1"])
T3 = Task("T3", f, ["3", "4"], ["5"])
T4 = Task("T4", f, ["4"], ["2"])
T5 = Task("T5", f, ["5"], ["5"])
T6 = Task("T6", f, ["1", "2"], ["4"])

sys = TaskSystem([T1, T2, T3, T4, T5, T6], { T1: {}, T2: {T1}, T3: {T1}, T4: {T2, T3}, T5: {T3}, T6: {T4, T5} })

# sys.maximizeParalization()
print(sys.dependencies)
print(sys.isDeterministic())