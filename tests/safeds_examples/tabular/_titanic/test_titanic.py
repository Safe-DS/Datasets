import pytest
from safeds.data.tabular.containers import Table
from safeds.data.tabular.typing import Anything, Integer, RealNumber, Schema, String
from safeds_examples.tabular import load_titanic


class TestLoadTitanic:
    @pytest.fixture()
    def titanic(self) -> Table:
        return load_titanic()

    @pytest.mark.smoke()
    def test_returns_table(self) -> None:
        titanic = load_titanic()

        assert isinstance(titanic, Table)

    def test_row_count(self, titanic: Table) -> None:
        assert titanic.number_of_rows == 1309

    def test_schema(self, titanic: Table) -> None:
        assert titanic.schema == Schema(
            {
                "id": Integer(),
                "name": String(),
                "sex": String(),
                "age": RealNumber(is_nullable=True),
                "siblings_spouses": Integer(),
                "parents_children": Integer(),
                "ticket": String(),
                "travel_class": Integer(),
                "fare": RealNumber(is_nullable=True),
                "cabin": Anything(is_nullable=True),
                "port_embarked": Anything(is_nullable=True),
                "survived": Integer(),
            },
        )

    def test_columns_with_missing_values(self, titanic: Table) -> None:
        actual_column_names = {column.name for column in titanic.to_columns() if column.has_missing_values()}

        assert actual_column_names == {"age", "port_embarked", "fare", "cabin"}


class TestColumnDescriptions:
    def test_all_columns_have_descriptions(self) -> None:
        titanic = load_titanic()
        descriptions = titanic.column_descriptions

        assert set(descriptions.get_column("Name")._data) == set(titanic.column_names)
