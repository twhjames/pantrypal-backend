from datetime import timedelta
from enum import Enum

from src.core.pantry.constants import Category

# Estimated shelf life for each pantry category (in days)
CATEGORY_EXPIRY_DAYS: dict[Category, timedelta] = {
    Category.FRUITS: timedelta(days=7),
    Category.VEGETABLES: timedelta(days=5),
    Category.DAIRY: timedelta(days=10),
    Category.MEAT: timedelta(days=3),
    Category.SEAFOOD: timedelta(days=2),
    Category.GRAINS: timedelta(days=180),
    Category.STAPLES: timedelta(days=365),
    Category.FROZEN: timedelta(days=90),
    Category.BEVERAGES: timedelta(days=60),
    Category.SNACKS: timedelta(days=120),
    Category.OTHER: timedelta(days=30),  # fallback/default
}


class SupermarketType(str, Enum):
    FAIRPRICE = "FairPrice"
    GIANT = "Giant"
