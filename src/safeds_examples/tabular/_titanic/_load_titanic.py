import os

from safeds.data.tabular import Table

_path = os.path.join(os.path.dirname(__file__), "data", "titanic.csv")


def load_titanic() -> Table:
    """
    Loads the Titanic dataset.

    Returns
    -------
    Table
        The Titanic dataset.
    """

    return Table.from_csv(_path)
