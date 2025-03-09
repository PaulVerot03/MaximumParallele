import networkx as nx
import matplotlib.pyplot as plt
import time
import random
import threading
from typing import List, Dict, Callable

class Task:
    def __init__(self, name: str, reads: List[str] = None, writes: List[str] = None, run: Callable = None):
        self.name = name
        self.reads = reads if reads else []
        self.writes = writes if writes else []
        self.run = run

class TaskSystem:
    def __init__(self, tasks: List[Task], precedence: Dict[str, List[str]]):
        self.tasks = {task.name: task for task in tasks}
        self.precedence = precedence
        self.validate()

    def validate(self):
        # Vérifier que toutes les tâches dans precedence existent
        for task, deps in self.precedence.items():
            if task not in self.tasks:
                raise ValueError(f"Tâche inconnue: {task}")
            for dep in deps:
                if dep not in self.tasks:
                    raise ValueError(f"Dépendance inconnue: {dep}")
        print("Validation réussie !")

    def get_dependencies(self, task_name: str):
        return self.precedence.get(task_name, [])

    def run_seq(self):
        executed = set()
        for task_name in self.precedence:
            self._execute_task(task_name, executed)

    def _execute_task(self, task_name, executed):
        if task_name in executed:
            return
        for dep in self.get_dependencies(task_name):
            self._execute_task(dep, executed)
        print(f"Exécution séquentielle: {task_name}")
        self.tasks[task_name].run()
        executed.add(task_name)

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

    def det_test_rnd(self):
        # j'aime imaginer que c'est Leonard Bernstein qui à fait ça, ca aurait été drôle
        results = []
        for _ in range(5):
            random.seed(42)  # Fixer une graine pour la reproductibilité
            self.run()
            results.append(hash(str(self.tasks)))
        if len(set(results)) > 1:
            print("Le système n'est pas déterministe !")
        else:
            print("Le système est déterministe.")

    def par_cost(self):
        start = time.time()
        self.run_seq()
        seq_time = time.time() - start

        start = time.time()
        self.run()
        par_time = time.time() - start

        print(f"Temps séquentiel: {seq_time:.5f}s, Temps parallèle: {par_time:.5f}s")
