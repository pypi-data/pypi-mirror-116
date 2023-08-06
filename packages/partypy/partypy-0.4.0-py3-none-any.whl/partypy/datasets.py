import pandas as pd
from os.path import dirname, join


def load_party():
    """Return a dataframe of 100 party guests.

    Contains the following fields:
        name                           100 non-null object
        probability_of_attendance      100 non-null float

    Returns
    -------
    pandas.DataFrame
        DataFrame of party guest names and probabilities of attendance.

    Examples
    --------
    >>> data = load_party()
    >>> data.head()
                   name  probability_of_attendance
    0    Donovan Willis                       0.70
    1   Jocelyn Navarro                       0.70
    2     Houston Stein                       0.90
    3    Carlos Mullins                       0.50
    4    Bridger Pruitt                       0.70
    """
    module_path = dirname(__file__)  # directory location of datasets.py module
    data_path = join(module_path, "data", "party.csv")  # location of party.csv
    return pd.read_csv(data_path)
