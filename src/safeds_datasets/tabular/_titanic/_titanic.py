from pathlib import Path

from safeds.data.tabular.containers import Table

from safeds_datasets.tabular.containers import TabularDataset

_path = Path(__file__).parent / "data" / "titanic.csv"


def load_titanic() -> TabularDataset:
    """
    Load the "Titanic" dataset.

    Returns
    -------
    titanic :
        The "Titanic" dataset.
    """
    return TabularDataset(
        Table.from_csv_file(str(_path)),
        column_descriptions={
            "id": "A unique identifier",
            "name": "Name of the passenger",
            "sex": "Sex of the passenger",
            "age": "Age of the passenger at the time of the accident",
            "siblings_spouses": "Number of siblings or spouses aboard",
            "parents_children": "Number of parents or children aboard",
            "ticket": "Ticket number",
            "travel_class": "Travel class (1 = first, 2 = second, 3 = third)",
            "fare": "Fare",
            "cabin": "Cabin number",
            "port_embarked": "Port of embarkation",
            "survived": "Whether the passenger survived the accident (0 = no, 1 = yes)",
        },
    )
