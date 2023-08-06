import altair as alt


def plot_simulation(results):
    """Plot a histogram of simulation results.

    Parameters
    ----------
    results : pandas.DataFrame
        DataFrame of simulation results from `partpy.simulate_party()`

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

    return histogram
