import pytest
from safeds_datasets.tabular import load_titanic
from safeds_datasets.tabular.containers import TableWithDescriptions


class TestLoadTitanic:
    @pytest.fixture()
    def titanic(self) -> TableWithDescriptions:
        return load_titanic()

    @pytest.mark.smoke()
    def test_returns_table(self) -> None:
        titanic = load_titanic()

        assert isinstance(titanic, TableWithDescriptions)

    def test_row_count(self, titanic: TableWithDescriptions) -> None:
        assert titanic.data.row_count == 1309

    def test_column_names(self, titanic: TableWithDescriptions) -> None:
        assert titanic.data.column_names == [
            "id",
            "name",
            "sex",
            "age",
            "siblings_spouses",
            "parents_children",
            "ticket",
            "travel_class",
            "fare",
            "cabin",
            "port_embarked",
            "survived",
        ]

    def test_columns_with_missing_values(self, titanic: TableWithDescriptions) -> None:
        actual_column_names = {column.name for column in titanic.data.to_columns() if column.missing_value_count()}

        assert actual_column_names == {"age", "port_embarked", "fare", "cabin"}


class TestColumnDescriptions:
    def test_all_columns_have_descriptions(self) -> None:
        titanic = load_titanic()
        descriptions = titanic.column_descriptions

        assert set(descriptions.get_column("Name").to_list()) == set(titanic.data.column_names)
