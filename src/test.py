import random
import time
import sys
from map import Task, TaskSystem
from gui.main_window import startMainWindow

def f():
    t = 1

# I like to imagine that Leonard Bernstein did that, it would have been quite funny
def det_test_rnd(task_system):
    results = []
    for _ in range(5):
        random.seed(42)  # Fix the random seed
        task_system.run()
        results.append(hash(str(task_system.tasks)))
    if len(set(results)) > 1:
        print("Le système n'est pas déterministe !")
    else:
        print("Le système est déterministe.")

# allow the program to calculate the time taken by each task sequence
def compareCost(sys: TaskSystem):
    start = time.time()
    sys.runSequence()
    seq_time = time.time() - start

    start = time.time()
    sys.run()
    par_time = time.time() - start

    print(f"Temps séquentiel: {seq_time:.5f}s, Temps parallèle: {par_time:.5f}s")

# Declare the global variables
X, Y, Z = None, None, None

def tests():
    T1 = Task("T1", f, ["1"], ["4"])
    T2 = Task("T2", f, ["3", "4"], ["1"])
    T3 = Task("T3", f, ["3", "4"], ["5"])
    T4 = Task("T4", f, ["4"], ["2"])
    T5 = Task("T5", f, ["5"], ["5"])
    T6 = Task("T6", f, ["1", "2"], ["4"])

    sys = TaskSystem([T1, T2, T3, T4, T5, T6], { T1: {}, T2: {T1}, T3: {T1}, T4: {T2, T3}, T5: {T3}, T6: {T4, T5} })

    # Test the sequential execution
    print("=== Exécution séquentielle ===")
    sys.runSequence()

    # Test the parallel execution of the program
    print("=== Exécution parallèle ===")
    sys.run()

    # Show the result of the execution
    print("=== Graphe de précédence ===")
    sys.draw()

    # Test if the sequence is deterministic
    print("=== Test de déterminisme ===")
    det_test_rnd(sys)

    # Compare the execution cost
    print("=== Comparaison des temps d'exécution ===")
    compareCost(sys)

def main(args):
    if "-nogui" in args:
        return tests()

    return startMainWindow()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
