from safeds._validation import _check_columns_exist
from safeds.data.tabular.containers import Table


class TableWithDescriptions:
    """
    A `Table` with descriptions for its columns.

    Parameters
    ----------
    table:
        The table.
    column_descriptions:
        A dictionary mapping column names to their descriptions.

    Raises
    ------
    ColumnNotFoundError
        If a column name in `descriptions` does not exist in `table`.
    """

    def __init__(self, table: Table, column_descriptions: dict[str, str]) -> None:
        # Check that all column names in `descriptions` exist in `table`
        _check_columns_exist(table, list(column_descriptions.keys()))

        self._data = table
        self._descriptions = column_descriptions

    @property
    def data(self) -> Table:
        """The data."""
        return self._data

    @property
    def column_descriptions(self) -> Table:
        """
        Return a `Table` contain the name of a column and its description.

        The name is stored in a column called `"Name"` and the description in a column called `"Description"`.
        """
        return Table(
            {
                "Name": self._data.column_names,
                "Description": [self.get_column_description(column_name) for column_name in self._data.column_names],
            },
        )

    def get_column_description(self, column_name: str) -> str:
        """
        Get the description of a column. If no description exists, an empty string is returned.

        Parameters
        ----------
        column_name:
            The name of the column.

        Returns
        -------
        column_description:
            The description of the column.

        Raises
        ------
        ColumnNotFoundError
            If no column with the given name exists.
        """
        _check_columns_exist(self._data, [column_name])

        return self._descriptions.get(column_name, "")
