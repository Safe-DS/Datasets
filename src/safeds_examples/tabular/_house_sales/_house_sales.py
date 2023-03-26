import os

from safeds.data.tabular.containers import Table

_path = os.path.join(os.path.dirname(__file__), "data", "house_sales.csv")


def load_house_sales() -> Table:
    """
    Loads the "House Sales" dataset.

    Returns
    -------
    Table
        The "House Sales" dataset.
    """

    return Table.from_csv(_path)


def describe_house_sales_columns() -> Table:
    """
    Returns a `Table` with two columns `"Name"` and `"Description"`, containing the name of a column in the "House
    Sales" dataset and its description respectively.

    Returns
    -------
    Table
        A `Table` with names and descriptions for all columns of the "House Sales" dataset.
    """

    return Table(
        [
            {"Name": "id", "Description": "A unique identifier"},
            {"Name": "year", "Description": "Year of sale"},
            {"Name": "month", "Description": "Month of sale"},
            {"Name": "day", "Description": "Day of sale"},
            {"Name": "zipcode", "Description": "Zipcode"},
            {"Name": "latitude", "Description": "Latitude"},
            {"Name": "longitude", "Description": "Longitude"},
            {"Name": "sqft_lot", "Description": "Lot area in square feet"},
            {"Name": "sqft_living", "Description": "Interior living space in square feet"},
            {"Name": "sqft_above", "Description": "Interior living space above ground in square feet"},
            {"Name": "sqft_basement", "Description": "Interior living space below ground in square feet"},
            {"Name": "floors", "Description": "Number of floors"},
            {"Name": "bedrooms", "Description": "Number of bedrooms"},
            {
                "Name": "bathrooms",
                "Description": "Number of bathrooms.\n\n"
                "Fractional values indicate that components (toilet/sink/shower/bathtub) are missing.",
            },
            {"Name": "waterfront", "Description": "Whether the building overlooks a waterfront (0 = no, 1 = yes)"},
            {"Name": "view", "Description": "Rating of the view (1 to 5, higher is better)"},
            {"Name": "condition", "Description": "Rating of the condition of the house (1 to 5, higher is better)"},
            {"Name": "grade", "Description": "Rating of building construction and design (1 to 13, higher is better)"},
            {"Name": "year_built", "Description": "Year the house was built"},
            {
                "Name": "year_renovated",
                "Description": "Year the house was last renovated.\n\n"
                "A value of 0 indicates that it was never renovated.",
            },
            {"Name": "sqft_lot_15nn", "Description": "Lot area of the 15 nearest neighbors in square feet"},
            {
                "Name": "sqft_living_15nn",
                "Description": "Interior living space of the 15 nearest neighbors in square feet",
            },
            {"Name": "price", "Description": "Price the house sold for in USD"},
        ]
    )
