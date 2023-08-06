import numpy as np
import jax
import jax.numpy as jnp

class GaussianProposer:
    def __init__(self, delta):
        self._rng = np.random.default_rng()
        self.delta = delta

    def __call__(self, x):
        return x + self._rng.normal(size=x.shape)*self.delta

class SiteProposer:
    def __init__(self, delta):
        self._rng = np.random.default_rng()
        self.delta = delta

    def __call__(self, x):
        idx = tuple(self._rng.choice(np.arange(l)) for l in x.shape)
        return jax.ops.index_add(x,idx,self._rng.normal()*self.delta)

class Metropolis:
    def __init__(self, action, init, propose):
        self.action = jax.jit(action)
        self.state = init
        self.propose = propose
        
        self._shape = init.shape
        self._rng = np.random.default_rng()

        self._steps_proposed = 0
        self._steps_accepted = 0

    def __iter__(self):
        return self

    def __next__(self):
        # Initial action
        S = self.action(self.state)
        prop = self.propose(self.state)
        Sp = self.action(prop)

        # Accept/reject
        self._steps_proposed += 1
        if self._rng.uniform() < np.exp(S-Sp):
            self._steps_accepted += 1
            self.state = prop

        return self.state

    def acceptance_rate(self):
        return self._steps_accepted / self._steps_proposed

