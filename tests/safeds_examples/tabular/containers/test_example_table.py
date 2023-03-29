import pytest
from safeds.data.tabular.containers import Table, Column
from safeds.exceptions import UnknownColumnNameError

from safeds_examples.tabular.containers import ExampleTable


@pytest.fixture
def example_table() -> ExampleTable:
    return ExampleTable(
        Table.from_columns(
            [
                Column("a", [1, 2, 3]),
                Column("b", [4, 5, 6]),
            ]
        ),
        column_descriptions={"a": "The first column"}
    )


class TestInit:
    def test_should_raise_if_column_does_not_exist(self) -> None:
        with pytest.raises(UnknownColumnNameError):
            ExampleTable(
                Table.from_columns(
                    [
                        Column("a", [1, 2, 3]),
                        Column("b", [4, 5, 6]),
                    ]
                ),
                column_descriptions={"c": "The first column"}
            )


class TestColumnDescriptions:
    def test_should_map_column_names_to_descriptions(self, example_table: ExampleTable) -> None:
        assert example_table.column_descriptions == Table.from_columns(
            [
                Column("Name", ["a", "b"]),
                Column("Description", ["The first column", ""]),
            ]
        )


class TestGetColumnDescription:
    def test_should_return_description_for_column(self, example_table: ExampleTable) -> None:
        assert example_table.get_column_description("a") == "The first column"

    def test_should_return_empty_string_if_no_description_exists(self, example_table: ExampleTable) -> None:
        assert example_table.get_column_description("b") == ""

    def test_should_raise_error_if_column_does_not_exist(self, example_table: ExampleTable) -> None:
        with pytest.raises(UnknownColumnNameError):
            example_table.get_column_description("c")
