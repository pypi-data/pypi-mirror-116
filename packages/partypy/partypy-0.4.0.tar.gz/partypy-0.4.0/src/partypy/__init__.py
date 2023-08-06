# read version from installed package
from importlib.metadata import version
__version__ = version(__name__)

# populate package namespace
from partypy.simulate import simulate_party
from partypy.plotting import plot_simulation
from partypy.datasets import load_party

__all__ = ["simulate_party", "plot_simulation", "load_party"]
