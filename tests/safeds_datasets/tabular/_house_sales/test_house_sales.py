import pytest
from safeds_datasets.tabular import load_house_sales
from safeds_datasets.tabular.containers import TableWithDescriptions


class TestLoadHouseSales:
    @pytest.fixture()
    def house_sales(self) -> TableWithDescriptions:
        return load_house_sales()

    @pytest.mark.smoke()
    def test_returns_table(self) -> None:
        house_sales = load_house_sales()

        assert isinstance(house_sales, TableWithDescriptions)

    def test_row_count(self, house_sales: TableWithDescriptions) -> None:
        assert house_sales.data.row_count == 21613

    def test_column_names(self, house_sales: TableWithDescriptions) -> None:
        assert house_sales.data.column_names == [
            "id",
            "year",
            "month",
            "day",
            "zipcode",
            "latitude",
            "longitude",
            "sqft_lot",
            "sqft_living",
            "sqft_above",
            "sqft_basement",
            "floors",
            "bedrooms",
            "bathrooms",
            "waterfront",
            "view",
            "condition",
            "grade",
            "year_built",
            "year_renovated",
            "sqft_lot_15nn",
            "sqft_living_15nn",
            "price",
        ]

    def test_columns_with_missing_values(self, house_sales: TableWithDescriptions) -> None:
        actual_column_names = {column.name for column in house_sales.data.to_columns() if column.missing_value_count()}

        assert actual_column_names == set()


class TestColumnDescriptions:
    def test_all_columns_have_descriptions(self) -> None:
        house_sales = load_house_sales()
        descriptions = house_sales.column_descriptions

        assert set(descriptions.get_column("Name").to_list()) == set(house_sales.data.column_names)
