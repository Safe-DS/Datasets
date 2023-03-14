from safeds.data.tabular import Table
from safeds_examples.tabular import load_titanic


def test_load_titanic() -> None:
    titanic = load_titanic()

    assert isinstance(titanic, Table)
    assert titanic.count_rows() > 0
