# <span style="color:#4078c0">args_to_db</span> - Data Generation Tool for Argument Optimisation

```sh
    pip install args_to_db
```

You want to analyze a (python) script for different arguments/settings? - Argument optimization is becoming more and more important in many application areas. <span style="color:#4078c0">args_to_db</span> is an attempt to generalize and simplify the process of running a programm in different modes or configurations and combining the resulting datasets to allow for further analysis.

## When should I use <span style="color:#4078c0">args_to_db</span>?
You have a programm which is highly dependent on parameters and arguments, for example a solver framework for linear system of equations. Different inputs vary performance of solving methods dramatically. So we want to optimize the solver and preonditioner used for a specific linear system of equations.

This is performed once and results in preferences which are then to be used automatically by the programm. <span style="color:#4078c0">args_to_db</span> simplifies the process of argument variation and dataset generation.

## How to use <span style="color:#4078c0">args_to_db</span>?

```python
commands = arg('python3') + arg('solver.py') + \
           option('--solver', ['cg', 'jacobi']) + \
           option('--preconditioner', ['gs', 'spai']) + \
           flag('--log', vary=False)

run(commands, threads=4)
```

## How to report results?
The parameters on which we want to optimize need to be logged and combined later on. <span style="color:#4078c0">args_to_db</span> makes this very easy.
```python
    add_result('solver_time', 20.3)
    add_result('solver_state', 'converged')

    write_results(__file__, args) 
```
