from safeds.data.tabular.containers import Table
from safeds.exceptions import UnknownColumnNameError


class TabularDataset(Table):
    """
    A `Table` with descriptions for its columns.

    Parameters
    ----------
    table
        The table.
    column_descriptions
        A dictionary mapping column names to their descriptions.

    Raises
    ------
    UnknownColumnNameError
        If a column name in `descriptions` does not exist in `table`.
    """

    # noinspection PyMissingConstructor
    def __init__(self, table: Table, column_descriptions: dict[str, str]) -> None:
        # Check that all column names in `descriptions` exist in `table`
        invalid_column_names = set(column_descriptions.keys()) - set(table.column_names)
        if invalid_column_names:
            raise UnknownColumnNameError(list(invalid_column_names))

        self._data = table._data
        self._schema = table.schema
        self._descriptions = column_descriptions

    @property
    def column_descriptions(self) -> Table:
        """
        Return a `Table` contain the name of a column and its description.

        The name is stored in a column called `"Name"` and the description in a column called `"Description"`.
        """
        return Table(
            {
                "Name": self.column_names,
                "Description": [self.get_column_description(column_name) for column_name in self.column_names],
            },
        )

    def get_column_description(self, column_name: str) -> str:
        """
        Get the description of a column. If no description exists, an empty string is returned.

        Parameters
        ----------
        column_name
            The name of the column.

        Returns
        -------
        column_description :
            The description of the column.

        Raises
        ------
        UnknownColumnNameError
            If no column with the given name exists.
        """
        if column_name not in self.column_names:
            raise UnknownColumnNameError([column_name])

        return self._descriptions.get(column_name, "")
