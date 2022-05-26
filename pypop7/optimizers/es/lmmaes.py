import numpy as np

from pypop7.optimizers.es.es import ES


class LMMAES(ES):
    """Limited-Memory Matrix Adaptation Evolution Strategy (LMMAES).

    Reference
    ---------
    Loshchilov, I., Glasmachers, T. and Beyer, H.G., 2019.
    Large scale black-box optimization by limited-memory matrix adaptation.
    IEEE Transactions on Evolutionary Computation, 23(2), pp.353-358.
    https://ieeexplore.ieee.org/abstract/document/8410043

    See the official Python version from Glasmachers:
    https://www.ini.rub.de/upload/editor/file/1604950981_dc3a4459a4160b48d51e/lmmaes.py
    """
    def __init__(self, problem, options):
        ES.__init__(self, problem, options)
        self.options = options
        n_evolution_paths = 4 + int(3 * np.log(self.ndim_problem))
        self.n_evolution_paths = options.get('n_evolution_paths', n_evolution_paths)  # m in Algorithm 1
        self.c_s = None  # c_sigma in Algorithm 1
        self._s_1 = None  # for Line 13 in Algorithm 1
        self._s_2 = None  # for Line 13 in Algorithm 1
        self._c_d = 1 / (self.ndim_problem * np.power(1.5, np.arange(self.n_evolution_paths)))
        self._c_c = None

    def initialize(self, is_restart=False):
        self.c_s = self.options.get('c_s', 2 * self.n_individuals / self.ndim_problem)
        _s_1 = 1 - self.c_s
        if _s_1 < 0:  # undefined in the original paper
            _s_1 = 0.5
        self._s_1 = _s_1
        _s_2 = self._mu_eff * self.c_s * (2 - self.c_s)
        if _s_2 < 0:  # undefined in the original paper
            _s_2 = np.power(0.5, 2)
        self._s_2 = np.sqrt(_s_2)
        self._c_c = self.n_individuals / (self.ndim_problem * np.power(4.0, np.arange(self.n_evolution_paths)))
        z = np.empty((self.n_individuals, self.ndim_problem))  # Gaussian noise for mutation
        d = np.empty((self.n_individuals, self.ndim_problem))  # search directions
        mean = self._initialize_mean(is_restart)  # mean of Gaussian search distribution
        s = np.zeros((self.ndim_problem,))  # evolution path (p in Algorithm 1)
        tm = np.zeros((self.n_evolution_paths, self.ndim_problem))  # transformation matrix M
        y = np.empty((self.n_individuals,))  # fitness (no evaluation)
        return z, d, mean, s, tm, y

    def iterate(self, z=None, d=None, mean=None, tm=None, y=None, args=None):
        for k in range(self.n_individuals):
            if self._check_terminations():
                return z, d, y
            z[k] = self.rng_optimization.standard_normal((self.ndim_problem,))
            d[k] = z[k]
            for j in range(np.minimum(self._n_generations, self.n_evolution_paths)):
                d[k] = (1 - self._c_d[j]) * d[k] + self._c_d[j] * tm[j] * np.dot(tm[j], d[k])
            y[k] = self._evaluate_fitness(mean + self.sigma * d[k], args)
        return z, d, y

    def _update_distribution(self, z=None, d=None, mean=None, s=None, tm=None, y=None):
        order = np.argsort(y)
        d_w, z_w = np.zeros((self.ndim_problem,)), np.zeros((self.ndim_problem,))
        for k in range(self.n_parents):
            d_w += self._w[k] * d[order[k]]
            z_w += self._w[k] * z[order[k]]
        # update distribution mean
        mean += self.sigma * d_w
        # update evolution path (p_c, s) and low-rank transformation matrix (tm)
        s = self._s_1 * s + self._s_2 * z_w
        for k in range(self.n_evolution_paths):  # rank-m
            _tm_1 = 1 - self._c_c[k]
            if _tm_1 < 0:  # undefined in the original paper
                _tm_1 = 0.5
            _tm_2 = self._mu_eff * self._c_c[k] * (2 - self._c_c[k])
            if _tm_2 < 0:  # undefined in the original paper
                _tm_2 = np.power(0.5, 2)
            tm[k] = _tm_1 * tm[k] + np.sqrt(_tm_2) * z_w
        # update global step-size
        self.sigma *= np.exp(self.c_s / 2 * (np.sum(np.power(s, 2)) / self.ndim_problem - 1))
        return mean, s, tm

    def restart_initialize(self, z=None, d=None, mean=None, s=None, tm=None, y=None):
        if ES.restart_initialize(self):
            z, d, mean, s, tm, y = self.initialize(True)
        return z, d, mean, s, tm, y

    def optimize(self, fitness_function=None, args=None):  # for all generations (iterations)
        fitness = ES.optimize(self, fitness_function)
        z, d, mean, s, tm, y = self.initialize()
        while True:
            z, d, y = self.iterate(z, d, mean, tm, y, args)  # sample and evaluate offspring population
            if self.record_fitness:
                fitness.extend(y)
            if self._check_terminations():
                break
            mean, s, tm = self._update_distribution(z, d, mean, s, tm, y)
            self._n_generations += 1
            self._print_verbose_info(y)
            z, d, mean, s, tm, y = self.restart_initialize(z, d, mean, s, tm, y)
        results = self._collect_results(fitness, mean)
        results['s'] = s
        results['tm'] = tm
        return results
