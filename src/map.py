
import networkx as nx
import matplotlib.pyplot as plt
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
    def __init__(self, tasks: list[Task], precedence: dict[Task, set[Task]]=None, namespace=None):
        self.tasks = tasks
        self.namespace = namespace

        for i, task in enumerate(tasks):
            assert task.name not in [t.name for t in tasks[i+1:]], "Task duplication"

        if precedence is not None:
            self.dependencies = precedence
            self.validate()
            self.computeAllDependencies()
            # To work with unordered tasks
            self.tasks.sort(key=lambda task: len(self.all_dependencies[task]))
            self.checkDeterminism()
        self.maximizeParalization()
        self.makeLayers()

    def makeLayers(self, sort_tasks=True):
        free_tasks = set(self.tasks)
        self.layers = [ [task for task, deps in self.dependencies.items() if len(deps) == 0] ]
        visited_tasks = set(self.layers[0])
        free_tasks.difference_update(visited_tasks)

        while len(free_tasks) != 0:
            next_layer = set()
            for task in free_tasks:
                if self.dependencies[task].issubset(visited_tasks):
                    next_layer.add(task)
            assert len(next_layer) != 0, "Cycle detected!"
            visited_tasks.update(next_layer)
            free_tasks.difference_update(next_layer)
            self.layers.append(next_layer)

        if sort_tasks:
            self.tasks = []
            for i, tasks in enumerate(self.layers):
                self.tasks += list(tasks)
                for task in tasks:
                    task.layer = i

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

    def __computeAllDependencies(self, task):
        if task in self.all_dependencies:
            return
        self.all_dependencies[task] = self.dependencies[task].copy()
        for dep in self.dependencies[task]:
            self.__computeAllDependencies(dep)
            self.all_dependencies[task].update(self.all_dependencies[dep])

        assert task not in self.all_dependencies[task], "Cycle detected"

    def computeAllDependencies(self):
        self.all_dependencies: dict[Task, set[Task]] = {}
        for task in self.tasks:
            self.__computeAllDependencies(task)

    def getDependencies(self):
        return self.dependencies

    def isPathBetween(self, A, B):
        return B in self.all_dependencies[A] or A in self.all_dependencies[B]

    def checkDeterminism(self):
        for i, task1 in enumerate(self.tasks):
            for j, task2 in enumerate(self.tasks[:i]):
                assert not ((task1.writes & (task2.writes | task2.reads)) or (task2.writes & task1.reads)) or self.isPathBetween(task1, task2), "Undeterministic Graph"

    def validate(self):
        #Check that all tasks exist
        for task, deps in self.dependencies.items():
            if task not in self.tasks:
                raise ValueError(f"Tâche inconnue: {task}")
            for dep in deps:
                if dep not in self.tasks:
                    raise ValueError(f"Dépendance inconnue: {dep}")
        print("Validation réussie !")

    # allow a sequence of task to run
    def runSequence(self):
        try:
            for task in self.tasks:
                task.run()
        except:
            return True
    # allow the Tasks to run
    def run(self):
        threads = {}
        error = False

        # allow for tasks to be runned in parallel
        def parallelExecution(task):
            nonlocal error
            # Wait for all dependecies to be executed
            for dep in self.dependencies[task]:
                while not dep.executed:
                    pass
            try:
                task.run()
            except:
                error = True
            task.executed = True

        for task in self.tasks:
            task.executed = False
            threads[task] = threading.Thread(target=parallelExecution, args=(task,))
            threads[task].start()

        for task in self.tasks:
            threads[task].join()

        return error

    def run_layers(self):
        threads = {}
        error = False

        # allow for tasks to be runned in parallel
        def parallelExecution(task):
            nonlocal error
            try:
                task.run()
            except:
                error = True

        for layer in self.layers:
            for task in layer:
                threads[task] = threading.Thread(target=parallelExecution, args=(task,))
                threads[task].start()
            for task in layer:
                threads[task].join()

        return error

    def draw(self):
        assert len(self.tasks) > 0
        G = nx.DiGraph()
        for task in self.tasks:
            G.add_node(task.name, layer=task.layer)
        for task, deps in self.dependencies.items():
            for dep in deps:
                G.add_edge(dep.name, task.name)
        pos = nx.multipartite_layout(G, subset_key="layer")
        nx.draw(G, pos=pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        plt.show()
