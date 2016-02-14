# Most of the code in this file comes from PBNT by Elliot Cohen. See
# separate file in this project with PBNT license.

# import numpy as np
import random as ra

# from Potential import *
from DiscreteCondPot import *


class DiscreteUniPot(DiscreteCondPot):
    """
    A DiscreteUniPot or discrete uni-potential is a DiscreteCondPot that
    depends on a single node. Hence it represents either P(x) or A(x),
    where x is the focus node.

    Attributes
    ----------
    focus_node : BayesNode

    is_quantum : bool
    nd_sizes : list[int]
    nodes ; set[Node]
    num_nodes : int
    ord_nodes : list[Node]
    por_arr : numpy.ndarray

    """

    def __init__(self, is_quantum, node, pot_arr=None, bias=1):
        """
        Constructor

        Parameters
        ----------
        is_quantum : bool
        node : BayesNode
        pot_arr : numpy.ndarray
        bias : complex

        Returns
        -------

        """
        DiscreteCondPot.__init__(self, is_quantum, [node], pot_arr, bias)

    def size(self):
        """
        This returns the size (number of states) of the focus node.

        Returns
        -------
        int

        """
        return self.focus_node.size

    def sample(self):
        """
        This samples a state of the focus node using pot_arr as a
        distribution. It first normalizes pot_arr (1-norm for classical and
        2-norm for quantum). For the quantum case, it actually samples from
        the classical PD obtained by taking the absolute value squared of
        pot_arr.

        Returns
        -------
        int

        """

        # print("inside sample")
        # print("pot", self, "\n")

        self.normalize_self()

        # random float between 0 and 1
        rnum = ra.random()
        prob_sum = 0
        i = -1
        for x in self.pot_arr:
            if not self.is_quantum:
                prob = x
            else:
                prob = x*np.conjugate(x)
            prob_sum += prob
            i += 1
            if rnum <= prob_sum:
                break

        # print("sample=", i, "\n")

        return i

    def get_probs_from_amps(self):
        """
        First checks that is_quantum=True and if so returns a new
        DiscreteUniPot calculated by taking the magnitude squared of
        self.pot_arr. Thus, this function gets probabilities from
        amplitudes. Analogous function in DiscreteCondPot returns a
        DiscreteCondPot instead of a DiscreteUniPot.


        Returns
        -------
        DiscreteUniPot

        """
        assert self.is_quantum
        arr = self.pot_arr
        arr2 = (arr*np.conjugate(arr)).real
        return DiscreteUniPot(
            False, self.focus_node, pot_arr=arr2)

    def __deepcopy__(self, memo):
        """
        We want deepcopy to produce a copy of pot_arr but not of the nodes
        in self.nodes so need to override the usual deepcopy.

        Parameters
        ----------
        memo

        Returns
        -------
        DiscreteUniPot

        """
        copy_pot_arr = cp.deepcopy(self.pot_arr)
        return DiscreteUniPot(self.is_quantum,
                                self.focus_node, pot_arr=copy_pot_arr)

if __name__ == "__main__":
    print(5)