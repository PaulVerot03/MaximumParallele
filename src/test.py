import random
import time
import sys
from map import Task, TaskSystem
try:
    from gui.main_window import startMainWindow
    no_gui = False
except:
    no_gui = True

# I like to imagine that Leonard Bernstein did that, it would have been quite funny
def randomDeterminismTest(sys: TaskSystem, tests_count=5):
    namespace = sys.namespace if sys.namespace is not None else globals()
    writes = set()
    for task in sys.tasks:
        writes.update(task.writes)
    namespaces = []

    for _ in range(tests_count):
        try:
            for layer in sys.layers:
                layer = list(layer)
                random.shuffle(layer)
                for task in layer:
                    task.run()
            namespaces.append(namespace.copy())
        except Exception as e:
            print("Error in task's function:\n", e)
            return

    for write in writes:
        if any(map(lambda ns: ns[write] != namespaces[0][write], namespaces)):
            print("The system isn't deterministic")
            return
    print("The system may be deterministic")

# allow the program to calculate the time taken by each task sequence
def compareCost(sys: TaskSystem, n=5):
    seq_time, par_time = 0, 0
    for _ in range(n):
        start = time.time()
        sys.runSequence()
        seq_time += time.time() - start

        start = time.time()
        sys.run()
        par_time += time.time() - start

    print(f"Sequencial Time: {seq_time / n:.5f}s, Parallele Time: {par_time / n:.5f}s")

# Declare the global variables
A, B, C, D, E = None, None, None, None, None
def f():
    global A
    A = 1

def tests():
    T1 = Task("T1", f, ["A"], ["D"])
    T2 = Task("T2", f, ["C", "D"], ["A"])
    T3 = Task("T3", f, ["C", "D"], ["E"])
    T4 = Task("T4", f, ["D"], ["B"])
    T5 = Task("T5", f, ["E"], ["E"])
    T6 = Task("T6", f, ["A", "B"], ["D"])

    sys = TaskSystem([T1, T6, T2, T3, T4, T5], { T1: {}, T2: {T1}, T3: {T1}, T4: {T2, T3}, T5: {T3}, T6: {T4, T5} })

    # Test the sequential execution
    print("=== Sequencial Execution ===")
    sys.runSequence()

    # Test the parallel execution of the program
    print("=== Parallel Execution ===")
    sys.run()

    # Show the result of the execution
    print("=== Dependence Graph ===")
    sys.draw()

    # Test if the sequence is deterministic
    print("=== Testing for Determinism ===")
    randomDeterminismTest(sys)

    # Compare the execution cost
    print("=== Comparision for Time to Completion ===")
    compareCost(sys)

def main(args):
    if no_gui or "-nogui" in args:
        return tests()

    return startMainWindow()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
