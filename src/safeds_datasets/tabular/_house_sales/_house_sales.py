from pathlib import Path

from safeds.data.tabular.containers import Table

from safeds_datasets.tabular.containers import TabularDataset

_path = Path(__file__).parent / "data" / "house_sales.csv"


def load_house_sales() -> TabularDataset:
    """
    Load the "House Sales" dataset.

    Returns
    -------
    house_sales :
        The "House Sales" dataset.
    """
    return TabularDataset(
        Table.from_csv_file(str(_path)),
        column_descriptions={
            "id": "A unique identifier",
            "year": "Year of sale",
            "month": "Month of sale",
            "day": "Day of sale",
            "zipcode": "Zipcode",
            "latitude": "Latitude",
            "longitude": "Longitude",
            "sqft_lot": "Lot area in square feet",
            "sqft_living": "Interior living space in square feet",
            "sqft_above": "Interior living space above ground in square feet",
            "sqft_basement": "Interior living space below ground in square feet",
            "floors": "Number of floors",
            "bedrooms": "Number of bedrooms",
            "bathrooms": (
                "Number of bathrooms.\n\n"
                "Fractional values indicate that components (toilet/sink/shower/bathtub) are missing."
            ),
            "waterfront": "Whether the building overlooks a waterfront (0 = no, 1 = yes)",
            "view": "Rating of the view (1 to 5, higher is better)",
            "condition": "Rating of the condition of the house (1 to 5, higher is better)",
            "grade": "Rating of building construction and design (1 to 13, higher is better)",
            "year_built": "Year the house was built",
            "year_renovated": (
                "Year the house was last renovated.\n\nA value of 0 indicates that it was never renovated."
            ),
            "sqft_lot_15nn": "Lot area of the 15 nearest neighbors in square feet",
            "sqft_living_15nn": "Interior living space of the 15 nearest neighbors in square feet",
            "price": "Price the house sold for in USD",
        },
    )
