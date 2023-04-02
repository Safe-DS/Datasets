import pytest
from safeds.data.tabular.containers import Table
from safeds.data.tabular.typing import Integer, RealNumber, Schema
from safeds_examples.tabular import load_house_sales


class TestLoadHouseSales:
    @pytest.fixture()
    def house_sales(self) -> Table:
        return load_house_sales()

    @pytest.mark.smoke()
    def test_returns_table(self) -> None:
        house_sales = load_house_sales()

        assert isinstance(house_sales, Table)

    def test_row_count(self, house_sales: Table) -> None:
        assert house_sales.count_rows() == 21613

    def test_schema(self, house_sales: Table) -> None:
        assert house_sales.schema == Schema(
            {
                "id": Integer(),
                "year": Integer(),
                "month": Integer(),
                "day": Integer(),
                "zipcode": Integer(),
                "latitude": RealNumber(),
                "longitude": RealNumber(),
                "sqft_lot": Integer(),
                "sqft_living": Integer(),
                "sqft_above": Integer(),
                "sqft_basement": Integer(),
                "floors": RealNumber(),
                "bedrooms": Integer(),
                "bathrooms": RealNumber(),
                "waterfront": Integer(),
                "view": Integer(),
                "condition": Integer(),
                "grade": Integer(),
                "year_built": Integer(),
                "year_renovated": Integer(),
                "sqft_lot_15nn": Integer(),
                "sqft_living_15nn": Integer(),
                "price": Integer(),
            },
        )

    def test_columns_with_missing_values(self, house_sales: Table) -> None:
        actual_column_names = {column.name for column in house_sales.to_columns() if column.has_missing_values()}

        assert actual_column_names == set()


class TestColumnDescriptions:
    def test_all_columns_have_descriptions(self) -> None:
        house_sales = load_house_sales()
        descriptions = house_sales.column_descriptions

        assert set(descriptions.get_column("Name")._data) == set(house_sales.get_column_names())
