import numpy as np
import pandas as pd


def simulate_party(p, n_simulations=500):
    """Simulate guest attendance at a party.

    The attendance of each guest is treated as a Bernoulli random variable
    with probability of attendance `p`. The total number of attending guests
    is summed up for each `n_simulations`.

    Parameters
    ----------
    p : float or array_like of floats
        Probability of guest attendance, >= 0 and <=1.
    n_simulations : int, optional
        Number of simulations to run. By default, 500.

    Returns
    -------
    pandas.DataFrame
        DataFrame with total number of guests per simulation.

    Examples
    --------
    >>> simulate_party([0.1, 0.5, 0.9], n_simulations=5)
                Total guests
    Simulation
    1                      2
    2                      2
    3                      2
    4                      2
    5                      2
    """
    if n_simulations < 1:
        raise ValueError("n_simulations must be greater than 0.")
    result = np.random.binomial(n=1, p=p, size=(n_simulations, len(p))).sum(axis=1)
    return pd.DataFrame(
        {"Total guests": result, "Simulation": range(1, n_simulations + 1)}
    ).set_index("Simulation")
