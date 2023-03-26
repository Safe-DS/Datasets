import pytest
from safeds.data.tabular.containers import Table
from safeds.data.tabular.typing import (
    FloatColumnType,
    IntColumnType,
    StringColumnType,
    TableSchema,
)
from safeds_examples.tabular import describe_titanic_columns, load_titanic


class TestLoadTitanic:
    @pytest.fixture
    def titanic(self) -> Table:
        return load_titanic()

    @pytest.mark.smoke
    def test_returns_table(self) -> None:
        titanic = load_titanic()

        assert isinstance(titanic, Table)

    def test_row_count(self, titanic: Table) -> None:
        assert titanic.count_rows() == 1309

    def test_schema(self, titanic: Table) -> None:
        assert titanic.schema == TableSchema(
            {
                "id": IntColumnType(),
                "name": StringColumnType(),
                "sex": StringColumnType(),
                "age": FloatColumnType(),
                "siblings_spouses": IntColumnType(),
                "parents_children": IntColumnType(),
                "ticket": StringColumnType(),
                "travel_class": IntColumnType(),
                "fare": FloatColumnType(),
                "cabin": StringColumnType(),
                "port_embarked": StringColumnType(),
                "survived": IntColumnType(),
            }
        )

    def test_columns_with_missing_values(self, titanic: Table) -> None:
        actual_column_names = {column.name for column in titanic.list_columns_with_missing_values()}

        assert actual_column_names == {"age", "port_embarked", "fare", "cabin"}


class TestDescribeTitanicColumns:
    def test_all_columns_have_descriptions(self) -> None:
        titanic = load_titanic()
        descriptions = describe_titanic_columns()

        assert set(descriptions.get_column("Name")._data) == set(titanic.get_column_names())
