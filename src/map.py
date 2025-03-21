
import networkx as nx
import matplotlib.pyplot as plt
import time
import threading
from typing import Callable
import dis

# Declare a class Task taking as entry a name, function and possibly 2 strings lists.
class Task:
    def __init__(self, name: str, run: Callable, reads: list[str] = None, writes: list[str] = None):
        assert type(name) is str and type(run).__name__ == "function", "Domain error"
        self.name = name
        self.run = run
        self.reads = set(reads if reads else [instruction.argval for instruction in dis.Bytecode(run) if instruction.opname == "LOAD_GLOBAL"])
        self.writes = set(writes if writes else [instruction.argval for instruction in dis.Bytecode(run) if instruction.opname == "STORE_GLOBAL"])
    def __repr__(self):
        return '&' + self.name

# Declare the class TaskSystem and it's associated methods
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

    #Methods that check if the system is deterministic
    def isDeterministic(self):
        assert isinstance(self.dependencies, dict)
        tasks = [set() for _ in range(len(self.tasks))]
        for i, task1 in enumerate(self.tasks):
            for j, task2 in enumerate(self.tasks[:i]):
                # Check Bernstein conditions
                if (task1.writes & (task2.writes | task2.reads)) or (task2.writes & task1.reads):
                    tasks[i].update({task2})
                    tasks[i].update(tasks[j])
            print(self.dependencies.get(task1, set()), tasks[i])
            if not tasks[i].issubset(self.dependencies.get(task1, set())):
                return "Error"
        return "Deterministic"

    def validate(self):
        #Check that all tasks exist
        for task, deps in self.dependencies.items():
            if task not in self.tasks:
                raise ValueError(f"Tâche inconnue: {task}")
            for dep in deps:
                if dep not in self.tasks:
                    raise ValueError(f"Dépendance inconnue: {dep}")
        print("Validation réussie !")

    # get all dependecies
    def get_dependencies(self, task: Task):
        return self.dependencies.get(task, [])
# allow a sequence of task to run
    def run_seq(self):
        for task in self.tasks:
            task.run()
# allow the Tasks to run
    def run(self): 
        threads = {}
        executed = set()

# allow for tasks to be runned in parallel 
        def execute_parallel(task):
            for dep in self.get_dependencies(task):
                if dep not in executed:
                    return  # Wait for all dependecies to be executed
            print(f"Exécution parallèle: {task}")
            task.run()
            executed.add(task)

        for task in self.tasks:
            threads[task] = threading.Thread(target=execute_parallel, args=(task,))

        for task in self.dependencies:
            threads[task].start()

        for task in self.dependencies:
            threads[task].join()

    def draw(self):
        G = nx.DiGraph()
        for task, deps in self.dependencies.items():
            for dep in deps:
                G.add_edge(dep, task.name)
        nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        plt.show()

# allow the program to calculate the time taken by each task sequence
    def par_cost(self):
        start = time.time()
        self.run_seq()
        seq_time = time.time() - start

        start = time.time()
        self.run()
        par_time = time.time() - start

        print(f"Temps séquentiel: {seq_time:.5f}s, Temps parallèle: {par_time:.5f}s")
