import pytest
from safeds.data.tabular import Table
from safeds.data.tabular.typing import TableSchema, FloatColumnType, StringColumnType, IntColumnType

from safeds_examples.tabular import load_titanic


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
                'Age': FloatColumnType(),
                'Cabin Number': StringColumnType(),
                'Fare': FloatColumnType(),
                'Name': StringColumnType(),
                'Number of Parents or Children Aboard': IntColumnType(),
                'Number of Siblings or Spouses Aboard': IntColumnType(),
                'Port of Embarkation': StringColumnType(),
                'Sex': StringColumnType(),
                'Survived': IntColumnType(),
                'Ticket Number': StringColumnType(),
                'Travel Class': IntColumnType()
            }
        )

    def test_columns_with_missing_values(self, titanic: Table) -> None:
        actual_column_names = {column.name for column in titanic.list_columns_with_missing_values()}

        assert actual_column_names == {'Age', 'Port of Embarkation', 'Fare', 'Cabin Number'}
