import random
from matplotlib import pyplot as plt
import numpy as np
import numpy.random as rand
from math import pi as pi
from statistics import mean


class Estimate_e(object):
    """
    Using the MCMC method and base on the Bayesian Inference,
    estimate the posterior probability for e(the base of normal distribution)
    """

    def __init__(self, number_points):
        """
        Initialize the estimate

        Parameters
        ------------
        number_points: int
            Controls the number of points generated using normal distribution, thus control the number of data points.

        Attributes:
        data: list
            Store data in the this data list for further analyzation

        """
        self.data = [rand.normal() for _ in range(number_points)]

    def posterior(self, a):
        """
        Calculate posterior based on Bayesian Theorem

        Parameters
        --------------
        x:float
            calculate the posterior for a particular value of parameter a

        """
        # We use a uniform prior p(a), which is independent of a
        post = 1
        for x in self.data:
            post = post * np.sqrt(np.log(a) / (2 * pi)) * \
                np.exp(- np.log(a) * x**2 / 2)

        return post


class MCMC(Estimate_e):
    """
    Defines the MCMC
    """

    def __init__(
            self,
            number_points,
            steps=10**4,
            initial_state=2):
        """
        initialize the initial state

        Parameters
        -------------
        steps: int
            That's how many steps we're gonna run in the MCMC chain.
        initial_state: float
            Which value do we want to start in the parameter space.
        """
        super().__init__(number_points)
        self.steps = steps
        self.states = [initial_state]  # .append([0 for _ in range(steps - 1)])
        self.current_state = initial_state
        # Estimate_e.data

    def gen_fcn(self, sigma=1):
        """
        defines the generating function

        Parameters:
        -----------------
        mcmcstep: int
            Tells the generator which step we are at so that it knows where
            in the self.states list to find the current state.
        sigma: float
            The variance of the normal distribution that makes up the generating function.
        """
        a = 0
        while a <= 1:
            a = rand.normal(self.current_state, sigma)
        return a

    def evolve(self, sigma=1):
        """
        Evolve according to my current state and generating function

        Parameters
        ---------------
        sigma:float
            The variance of the normal distribution that makes up the generating function.

        """
        for _ in range(self.steps):
            a = self.gen_fcn(sigma)
            r = rand.uniform()
            ratio = self.posterior(a) / self.posterior(self.current_state)
            if r < ratio:
                self.states.append(a)
                self.current_state = a
            if r >= ratio:
                self.states.append(self.current_state)
        #print("number of states generated is" + str(len(self.states)))
        #print("number of steps is" + str(self.steps))
        return self.states


# evolve and get the effective chain
MCMCChain = MCMC(100)
MCMCChain.evolve(sigma=0.1)

# start to plot
plt.figure(1)
ax1 = plt.subplot(311)
plt.hist(MCMCChain.states[int(0.2 * MCMCChain.steps):], bins=100)


print("Estimation of e is " +
      str(mean(MCMCChain.states[int(0.2*MCMCChain.steps):])))

xval = np.linspace(1.5, 5, 1000)
yval = MCMCChain.posterior(xval)
# print("Estimation of e using posterior is " + str(mean(yval)))
ax2 = plt.subplot(312, sharex=ax1)
plt.plot(xval, yval, 'r')

# construct trace plot
num_samp = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
estim = []
for i in num_samp:
    Chain = MCMC(i, steps=10 ** 3)
    Chain.evolve(sigma=0.1)
    estim.append(mean(Chain.states[int(0.2*Chain.steps):]))

ax3 = plt.subplot(313)
plt.plot(num_samp, estim, 'b')
ax1.set(xlabel='Estimated e value')
ax3.set(xlabel='Number of data points')
ax3.set(ylabel='Estimated e value')
ax3.set_title('Trace plot')
plt.show()
