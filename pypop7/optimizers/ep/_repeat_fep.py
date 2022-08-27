"""Repeat the following paper for `FEP`:
"""
import numpy as np

from pypop7.benchmarks.base_functions import sphere, step, rosenbrock, rastrigin, ackley
from pypop7.optimizers.ep.fep import FEP


if __name__ == '__main__':
    ndim_problem = 30

    problem = {'fitness_function': rastrigin,
               'ndim_problem': ndim_problem,
               'lower_boundary': -5.12 * np.ones((ndim_problem,)),
               'upper_boundary': 5.12 * np.ones((ndim_problem,))}
    options = {'max_function_evaluations': 5000 * 100,
               'seed_rng': 0,  # undefined in the original paper
               'sigma': 3.0}
    fep = FEP(problem, options)
    results = fep.optimize()
    print(results)
    print(results['best_so_far_y'])
    # 22.88404827530138
    # vs 4.6e-2 (from the original paper)

    problem = {'fitness_function': ackley,
               'ndim_problem': ndim_problem,
               'lower_boundary': -32 * np.ones((ndim_problem,)),
               'upper_boundary': 32 * np.ones((ndim_problem,))}
    options = {'max_function_evaluations': 1500 * 100,
               'seed_rng': 0,  # undefined in the original paper
               'sigma': 3.0}
    fep = FEP(problem, options)
    results = fep.optimize()
    print(results)
    print(results['best_so_far_y'])
    # 1.9075267778220923
    # vs 1.8e-2 (from the original paper)

    problem = {'fitness_function': sphere,
               'ndim_problem': ndim_problem,
               'lower_boundary': -100*np.ones((ndim_problem,)),
               'upper_boundary': 100*np.ones((ndim_problem,))}
    options = {'max_function_evaluations': 1500 * 100,
               'seed_rng': 0,  # undefined in the original paper
               'sigma': 3.0}
    fep = FEP(problem, options)
    results = fep.optimize()
    print(results)
    print(results['best_so_far_y'])
    # 0.20284227582986794
    # vs 5.7e-4 (from the original paper)

    problem = {'fitness_function': step,
               'ndim_problem': ndim_problem,
               'lower_boundary': -100 * np.ones((ndim_problem,)),
               'upper_boundary': 100 * np.ones((ndim_problem,))}
    options = {'max_function_evaluations': 1500 * 100,
               'seed_rng': 0,  # undefined in the original paper
               'sigma': 3.0}
    fep = FEP(problem, options)
    results = fep.optimize()
    print(results)
    print(results['best_so_far_y'])
    # 47.0
    # vs 0 (from the original paper)

    problem = {'fitness_function': rosenbrock,
               'ndim_problem': ndim_problem,
               'lower_boundary': -30*np.ones((ndim_problem,)),
               'upper_boundary': 30*np.ones((ndim_problem,))}
    options = {'max_function_evaluations': 20000 * 100,
               'seed_rng': 0,  # undefined in the original paper
               'sigma': 3.0}
    fep = FEP(problem, options)
    results = fep.optimize()
    print(results)
    print(results['best_so_far_y'])
    # 19.653232176391665
    # vs mean 5.06 std 5.87 (from the original paper)