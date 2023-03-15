import pytest
from safeds.data.tabular import Table
from safeds.data.tabular.typing import FloatColumnType, IntColumnType, TableSchema
from safeds_examples.tabular import describe_house_sales_columns, load_house_sales


class TestLoadHouseSales:
    @pytest.fixture
    def house_sales(self) -> Table:
        return load_house_sales()

    @pytest.mark.smoke
    def test_returns_table(self) -> None:
        house_sales = load_house_sales()

        assert isinstance(house_sales, Table)

    def test_row_count(self, house_sales: Table) -> None:
        assert house_sales.count_rows() == 21613

    def test_schema(self, house_sales: Table) -> None:
        assert house_sales.schema == TableSchema(
            {
                "bathrooms": FloatColumnType(),
                "bedrooms": IntColumnType(),
                "condition": IntColumnType(),
                "day": IntColumnType(),
                "floors": FloatColumnType(),
                "grade": IntColumnType(),
                "id": IntColumnType(),
                "latitude": FloatColumnType(),
                "longitude": FloatColumnType(),
                "month": IntColumnType(),
                "price": IntColumnType(),
                "sqft_above": IntColumnType(),
                "sqft_basement": IntColumnType(),
                "sqft_living": IntColumnType(),
                "sqft_living_15nn": IntColumnType(),
                "sqft_lot": IntColumnType(),
                "sqft_lot_15nn": IntColumnType(),
                "view": IntColumnType(),
                "waterfront": IntColumnType(),
                "year": IntColumnType(),
                "year_built": IntColumnType(),
                "year_renovated": IntColumnType(),
                "zipcode": IntColumnType(),
            }
        )

    def test_columns_with_missing_values(self, house_sales: Table) -> None:
        actual_column_names = {column.name for column in house_sales.list_columns_with_missing_values()}

        assert actual_column_names == set()


class TestDescribeHouseSalesColumns:
    @pytest.fixture
    def house_sales(self) -> Table:
        return load_house_sales()

    def test_all_columns_have_descriptions(self, house_sales: Table) -> None:
        house_sales = load_house_sales()
        descriptions = describe_house_sales_columns()

        assert set(descriptions.get_column("Name")._data) == set(house_sales.get_column_names())
