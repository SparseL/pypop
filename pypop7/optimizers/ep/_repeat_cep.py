"""Repeat the following two papers for `CEP`:
    Yao, X., Liu, Y. and Lin, G., 1999.
    Evolutionary programming made faster.
    IEEE Transactions on Evolutionary Computation, 3(2), pp.82-102.
    https://ieeexplore.ieee.org/abstract/document/771163

    Bäck, T. and Schwefel, H.P., 1993.
    An overview of evolutionary algorithms for parameter optimization.
    Evolutionary Computation, 1(1), pp.1-23.
    https://direct.mit.edu/evco/article-abstract/1/1/1/1092/An-Overview-of-Evolutionary-Algorithms-for

    Note that we first update individual step-sizes and then update offspring for each generation as the
    second paper, in order to obtain fast local convergence.

    Very close performance can be obtained by our code. Therefore, we argue that the repeatability of
    `CEP` can be well-documented (*at least partly*).
"""
import numpy as np

from pypop7.benchmarks.base_functions import sphere, step, rosenbrock, rastrigin, ackley
from pypop7.optimizers.ep.cep import CEP


if __name__ == '__main__':
    ndim_problem = 30

    problem = {'fitness_function': rastrigin,
               'ndim_problem': ndim_problem,
               'lower_boundary': -5.12*np.ones((ndim_problem,)),
               'upper_boundary': 5.12*np.ones((ndim_problem,))}
    options = {'max_function_evaluations': 5000 * 100,
               'seed_rng': 0,  # undefined in the original paper
               'sigma': 3.0}
    cep = CEP(problem, options)
    results = cep.optimize()
    print(results)
    print(results['best_so_far_y'])
    # 57.707348276918225
    # vs 89 (from the original paper)

    problem = {'fitness_function': ackley,
               'ndim_problem': ndim_problem,
               'lower_boundary': -32*np.ones((ndim_problem,)),
               'upper_boundary': 32*np.ones((ndim_problem,))}
    options = {'max_function_evaluations': 1500 * 100,
               'seed_rng': 0,  # undefined in the original paper
               'sigma': 3.0}
    cep = CEP(problem, options)
    results = cep.optimize()
    print(results)
    print(results['best_so_far_y'])
    # 0.047112659488285136
    # vs 9.2 (from the original paper)

    problem = {'fitness_function': sphere,
               'ndim_problem': ndim_problem,
               'lower_boundary': -100*np.ones((ndim_problem,)),
               'upper_boundary': 100*np.ones((ndim_problem,))}
    options = {'max_function_evaluations': 1500 * 100,
               'seed_rng': 0,  # undefined in the original paper
               'sigma': 3.0}
    cep = CEP(problem, options)
    results = cep.optimize()
    print(results)
    print(results['best_so_far_y'])
    # 0.00021076229028199638
    # vs 2.2e-4 (from the original paper)

    problem = {'fitness_function': step,
               'ndim_problem': ndim_problem,
               'lower_boundary': -100 * np.ones((ndim_problem,)),
               'upper_boundary': 100 * np.ones((ndim_problem,))}
    options = {'max_function_evaluations': 1500 * 100,
               'seed_rng': 0,  # undefined in the original paper
               'sigma': 3.0}
    cep = CEP(problem, options)
    results = cep.optimize()
    print(results)
    print(results['best_so_far_y'])
    # 9.0
    # vs mean 577.76 std 1125.76 (from the original paper)

    problem = {'fitness_function': rosenbrock,
               'ndim_problem': ndim_problem,
               'lower_boundary': -30*np.ones((ndim_problem,)),
               'upper_boundary': 30*np.ones((ndim_problem,))}
    options = {'max_function_evaluations': 20000 * 100,
               'seed_rng': 0,  # undefined in the original paper
               'sigma': 3.0}
    cep = CEP(problem, options)
    results = cep.optimize()
    print(results)
    print(results['best_so_far_y'])
    # 7.1820167322999175
    # vs mean 6.17 std 13.61 (from the original paper)