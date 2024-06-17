"""Display column descriptions."""

from __future__ import annotations

from IPython.core.display import DisplayObject
from IPython.display import Markdown
from safeds.data.tabular.containers import Table


def display_column_descriptions(column_descriptions: Table) -> DisplayObject:
    """
    Display a Table containing the column descriptions.

    Parameters
    ----------
    column_descriptions:
        The column descriptions.

    Returns
    -------
    display_object:
        The display object.
    """
    result = ""

    for name, description in column_descriptions._data_frame.iter_rows():
        result += f"- **{name}:** {description}\n"

    return Markdown(result)
