import os

from safeds.data.tabular.containers import Table

_path = os.path.join(os.path.dirname(__file__), "data", "titanic.csv")


def load_titanic() -> Table:
    """
    Loads the "Titanic" dataset.

    Returns
    -------
    Table
        The "Titanic" dataset.
    """

    return Table.from_csv(_path)


def describe_titanic_columns() -> Table:
    """
    Returns a `Table` with two columns `"Name"` and `"Description"`, containing the name of a column in the "Titanic"
    dataset and its description respectively.

    Returns
    -------
    Table
        A `Table` with names and descriptions for all columns of the "Titanic" dataset.
    """

    return Table(
        [
            {"Name": "id", "Description": "A unique identifier"},
            {"Name": "name", "Description": "Name of the passenger"},
            {"Name": "sex", "Description": "Sex of the passenger"},
            {"Name": "age", "Description": "Age of the passenger at the time of the accident"},
            {"Name": "siblings_spouses", "Description": "Number of siblings or spouses aboard"},
            {"Name": "parents_children", "Description": "Number of parents or children aboard"},
            {"Name": "ticket", "Description": "Ticket number"},
            {"Name": "travel_class", "Description": "Travel class (1 = first, 2 = second, 3 = third)"},
            {"Name": "fare", "Description": "Fare"},
            {"Name": "cabin", "Description": "Cabin number"},
            {"Name": "port_embarked", "Description": "Port of embarkation"},
            {"Name": "survived", "Description": "Whether the passenger survived the accident"},
        ]
    )
