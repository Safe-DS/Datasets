from safeds.data.tabular.containers import Table
from safeds.data.tabular.exceptions import UnknownColumnNameError


class ExampleTable(Table):
    """
    A `Table` with descriptions for its columns.

    Parameters
    ----------
    table : Table
        The table.
    column_descriptions : dict[str, str]
        A dictionary mapping column names to their descriptions.

    Raises
    ------
    UnknownColumnNameError
        If a column name in `descriptions` does not exist in `table`.
    """

    def __init__(self, table: Table, column_descriptions: dict[str, str]) -> None:
        # Check that all column names in `descriptions` exist in `table`
        invalid_column_names = set(column_descriptions.keys()) - set(table.column_names)
        if invalid_column_names:
            raise UnknownColumnNameError(list(invalid_column_names))

        super().__init__(table._data, table.schema)
        self._descriptions = column_descriptions

    @property
    def column_descriptions(self) -> Table:
        """
        Return a `Table` contain the name of a column and its description.

        The name is stored in a column called `"Name"` and the description in a column called `"Description"`.
        """
        return Table(
            [
                {"Name": column_name, "Description": self.get_column_description(column_name)}
                for column_name in self.column_names
            ],
        )

    def get_column_description(self, column_name: str) -> str:
        """
        Get the description of a column. If no description exists, an empty string is returned.

        Parameters
        ----------
        column_name : str
            The name of the column.

        Returns
        -------
        description : str
            The description of the column.

        Raises
        ------
        UnknownColumnNameError
            If no column with the given name exists.
        """
        if column_name not in self.column_names:
            raise UnknownColumnNameError([column_name])

        return self._descriptions.get(column_name, "")
