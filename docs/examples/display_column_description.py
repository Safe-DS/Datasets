import pandas as pd
from IPython.core.display_functions import DisplayHandle
from IPython.display import display
from safeds.data.tabular.containers import Table


def display_column_descriptions(column_descriptions: Table) -> DisplayHandle:
    """
    Displays a Table containing the column descriptions.

    Parameters
    ----------
    column_descriptions : Table
        The column descriptions.

    Returns
    -------
    DisplayHandle
        The display handle.
    """

    # Remember the current value of the max_colwidth option
    max_colwidth = pd.get_option("max_colwidth")

    # Don't cut off the column descriptions
    pd.set_option("max_colwidth", None)

    # Create a DisplayHandle that displays the column descriptions nicely
    styler = (
        column_descriptions._data.style.relabel_index(["Name", "Description"], axis="columns")
        .hide(axis="index")
        .set_properties(
            **{
                "text-align": "left",
                "white-space": "pre-wrap",
            }
        )
    )
    result = display(styler)

    # Restore the max_colwidth option
    pd.set_option("max_colwidth", max_colwidth)

    return result
