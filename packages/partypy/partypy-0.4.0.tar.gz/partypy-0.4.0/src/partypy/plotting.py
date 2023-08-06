import pandas as pd
import altair as alt


def _quantiles(results, C=0.95):
    """Calculate quantiles of simulation results.

    Parameters
    ----------
    results : pandas.DataFrame
        DataFrame of simulation results from `partpy.simulate_party()`
    C : float, optional
        Confidence level, between 0 and 1. By default, 0.95.
    """
    if not 0 < C < 1:
        raise ValueError("ci must be 0 < ci < 1.")
    lower_q = results.quantile(0.5 - C / 2).to_numpy()
    upper_q = results.quantile(0.5 + C / 2).to_numpy()
    return lower_q, upper_q


def plot_simulation(results, C=None):
    """Plot a histogram of simulation results.

    Parameters
    ----------
    results : pandas.DataFrame
        DataFrame of simulation results from `partpy.simulate_party()`
    C : float, optional
        Confidence level, between 0 and 1. If provided, confidence intervals
        will be displayed on chart. By default, 0.95.

    Returns
    -------
    altair.Chart
        Histogram of simulation results.

    Examples
    --------
    >>> from partypy.simulate import simulate_party
    >>> from partypy.plotting import plot_simulation
    >>> results = simulate([0.1, 0.5, 0.9])
    >>> plot_simulation(results)
    altair.Chart
    """

    histogram = (
        alt.Chart(results)
        .mark_bar()
        .encode(
            x=alt.X(
                "Total guests",
                bin=alt.Bin(maxbins=30),
                axis=alt.Axis(format=".0f"),
            ),
            y="count()",
            tooltip="count()",
        )
    )

    if C is not None:
        lower_q, upper_q = _quantiles(results, C)
        quantiles = (
            alt.Chart(
                pd.DataFrame({"quantiles": [lower_q, upper_q]})
            )
            .mark_rule(color="red", strokeWidth=3)
            .encode(x="quantiles:Q")
        )
        return histogram + quantiles
    else:
        return histogram
