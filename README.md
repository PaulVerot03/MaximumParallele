# MaximumParallele Documentation

## Overview

This program defines a system for managing and executing tasks with dependencies and producing a visualisation of said tasks. It ensures proper execution order while maximizing parallelization where possible.

## Dependencies

- `networkx`

- `matplotlib.pyplot`

- `threading`

- `typing.Callable`

- `dis`

## Classes

### 1. `Task`

Represents a single task with a name, execution function, and optional read/write dependencies.

#### Attributes

- `name` (str): The name of the task.

- `run` (Callable): The function to be executed for the task.

- `reads` (set[str]): Variables read by the task.

- `writes` (set[str]): Variables written by the task.

#### Methods

- `__init__(self, name, run, reads=None, writes=None)`: Initializes the task with its properties.

- `__repr__(self)`: Returns a string representation of the task.

### 2. `TaskSystem`

Manages a collection of tasks, enforcing dependencies and parallel execution where possible.

#### Attributes

- `tasks` (list[Task]): List of tasks in the system.

- `dependencies` (dict[Task, set[Task]]): Task dependency mappings.

- `layers` (list[list[Task]]): Layers of tasks based on dependencies.

#### Methods

- `__init__(self, tasks, precedence=None)`: Initializes the system, validates dependencies, and prepares task execution.

- `makeLayers(self, sort_tasks=True)`: Organizes tasks into execution layers based on dependencies.

- `maximizeParalization(self)`: Optimizes task parallelization while ensuring dependencies are met.

- `checkDeterminism(self)`: Checks if the system follows a deterministic execution order.

- `validate(self)`: Ensures all tasks and dependencies are correctly defined.

- `runSequence(self)`: Executes tasks sequentially.

- `run(self)`: Executes tasks while respecting dependencies, utilizing multithreading for parallel execution.

- `draw(self)`: Visualizes the task dependency graph using NetworkX.

## Usage Example

```python
# Define task functions
T1 = Task("T1", f, ["1"], ["4"])
T2 = Task("T2", f, ["3", "4"], ["1"])
T3 = Task("T3", f, ["3", "4"], ["5"])
T4 = Task("T4", f, ["4"], ["2"])
T5 = Task("T5", f, ["5"], ["5"])
T6 = Task("T6", f, ["1", "2"], ["4"])

# Create and execute TaskSystem
task_system = TaskSystem([T1, T2, T3, T4, T5, T6], { T1: {}, T2: {T1}, T3: {T1}, T4: {T2, T3}, T5: {T3}, T6: {T4, T5} })
task_system.run()
```

## Visualization

To generate a dependency graph, call:

```python
task_system.draw()
```

This will display a directed graph of task dependencies.

## Usage

When launched with the provided makefile, the user can interact and set tasks using a GUI in which the user can set and use provided or custom sequences.

## Notes

- The system detects cyclic dependencies and prevents execution if found.

- Tasks are executed in parallel where dependencies allow.

- Ensure task functions are thread-safe when using parallel execution.

[Github Repository](https://github.com/PaulVerot03/MaximumParallele)
[PowerPoint presentation](https://ueve-my.sharepoint.com/:p:/g/personal/20220212_etud_univ-evry_fr/EbZ7mhL2wRxNiqbO6q6G5D0BxSINBMAM_Qw35S93nbx1SQ?e=ymnTNR)
