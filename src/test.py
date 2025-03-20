import random
import sys
from map import Task, TaskSystem
from gui.main_window import startMainWindow

def f():
    t = 1

def det_test_rnd(task_system):
    # j'aime imaginer que c'est Leonard Bernstein qui à fait ça, ca aurait été drôle
    results = []
    for _ in range(5):
        random.seed(42)  # Fixer une graine pour la reproductibilité
        task_system.run()
        results.append(hash(str(task_system.tasks)))
    if len(set(results)) > 1:
        print("Le système n'est pas déterministe !")
    else:
        print("Le système est déterministe.")

# Définition des variables globales
X, Y, Z = None, None, None

def tests():
    T1 = Task("T1", f, ["1"], ["4"])
    T2 = Task("T2", f, ["3", "4"], ["1"])
    T3 = Task("T3", f, ["3", "4"], ["5"])
    T4 = Task("T4", f, ["4"], ["2"])
    T5 = Task("T5", f, ["5"], ["5"])
    T6 = Task("T6", f, ["1", "2"], ["4"])

    sys = TaskSystem([T1, T2, T3, T4, T5, T6], { T1: {}, T2: {T1}, T3: {T1}, T4: {T2, T3}, T5: {T3}, T6: {T4, T5} })
    # Tester l'exécution séquentielle
    print("=== Exécution séquentielle ===")
    sys.run_seq()

    # Tester l'exécution parallèle
    print("=== Exécution parallèle ===")
    sys.run()

    # Afficher le graphe de précédence
    print("=== Graphe de précédence ===")
    sys.draw()

    # Tester le déterminisme
    print("=== Test de déterminisme ===")
    det_test_rnd(sys)

    # Comparer les coûts d'exécution
    print("=== Comparaison des temps d'exécution ===")
    sys.par_cost()

def main(args):
    if "-nogui" in args:
        return tests()

    return startMainWindow()

if __name__ == "__main__":
    sys.exit(main(sys.argv))