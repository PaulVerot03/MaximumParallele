import random
from map import Task, TaskSystem

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

# Définition des fonctions des tâches
def runT1():
    global X
    X = 1
    print("T1 exécutée")

def runT2():
    global Y
    Y = 2
    print("T2 exécutée")

def runTsomme():
    global X, Y, Z
    Z = X + Y
    print(f"somme exécutée: Z = {Z}")

# Création des tâches
t1 = Task("T1", writes=["X"], run=runT1)
t2 = Task("T2", writes=["Y"], run=runT2)
tSomme = Task("somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)

# Définition du système de tâches avec précédences
task_system = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]})

# Tester l'exécution séquentielle
print("=== Exécution séquentielle ===")
task_system.run_seq()

# Tester l'exécution parallèle
print("=== Exécution parallèle ===")
task_system.run()

# Afficher le graphe de précédence
print("=== Graphe de précédence ===")
task_system.draw()

# Tester le déterminisme
print("=== Test de déterminisme ===")
task_system.det_test_rnd()

# Comparer les coûts d'exécution
print("=== Comparaison des temps d'exécution ===")
task_system.par_cost()
