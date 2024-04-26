"""Tabular datasets."""

from ._house_sales import load_house_sales
from ._titanic import load_titanic

__all__ = ["load_house_sales", "load_titanic"]
