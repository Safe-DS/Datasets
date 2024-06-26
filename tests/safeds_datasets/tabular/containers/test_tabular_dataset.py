import pytest
from safeds.data.tabular.containers import Column, Table
from safeds.exceptions import ColumnNotFoundError
from safeds_datasets.tabular.containers import TableWithDescriptions


@pytest.fixture()
def tabular_dataset() -> TableWithDescriptions:
    return TableWithDescriptions(
        Table.from_columns(
            [
                Column("a", [1, 2, 3]),
                Column("b", [4, 5, 6]),
            ],
        ),
        column_descriptions={"a": "The first column"},
    )


class TestInit:
    def test_should_raise_if_column_does_not_exist(self) -> None:
        with pytest.raises(ColumnNotFoundError):
            TableWithDescriptions(
                Table.from_columns(
                    [
                        Column("a", [1, 2, 3]),
                        Column("b", [4, 5, 6]),
                    ],
                ),
                column_descriptions={"c": "The first column"},
            )


class TestColumnDescriptions:
    def test_should_map_column_names_to_descriptions(self, tabular_dataset: TableWithDescriptions) -> None:
        assert tabular_dataset.column_descriptions == Table.from_columns(
            [
                Column("Name", ["a", "b"]),
                Column("Description", ["The first column", ""]),
            ],
        )


class TestGetColumnDescription:
    def test_should_return_description_for_column(self, tabular_dataset: TableWithDescriptions) -> None:
        assert tabular_dataset.get_column_description("a") == "The first column"

    def test_should_return_empty_string_if_no_description_exists(self, tabular_dataset: TableWithDescriptions) -> None:
        assert tabular_dataset.get_column_description("b") == ""

    def test_should_raise_error_if_column_does_not_exist(self, tabular_dataset: TableWithDescriptions) -> None:
        with pytest.raises(ColumnNotFoundError):
            tabular_dataset.get_column_description("c")
