from enum import Enum


class Unit(str, Enum):
    GRAMS = "grams"
    KILOGRAMS = "kg"
    MILLILITERS = "ml"
    LITERS = "liters"
    PIECES = "pieces"
    LOAF = "loaf"
    PACK = "pack"

    @classmethod
    def labels(cls):
        return {unit: unit.value for unit in cls}


class Category(str, Enum):
    FRUITS = "Fruits"
    VEGETABLES = "Vegetables"
    DAIRY = "Dairy"
    MEAT = "Meat"
    SEAFOOD = "Seafood"
    GRAINS = "Grains"
    STAPLES = "Staples"
    FROZEN = "Frozen"
    BEVERAGES = "Beverages"
    SNACKS = "Snacks"
    OTHER = "Other"

    @classmethod
    def descriptions(cls) -> dict:
        return {
            cls.FRUITS: "Fresh or packaged fruit items",
            cls.VEGETABLES: "Leafy greens and root vegetables",
            cls.DAIRY: "Milk, cheese, yogurt and similar items",
            cls.MEAT: "Raw or cooked meat products",
            cls.SEAFOOD: "Fish, prawns, clams, and other seafood",
            cls.GRAINS: "Staple grains like rice, oats, barley",
            cls.STAPLES: "Kitchen essentials like oil, salt, sugar, flour",
            cls.FROZEN: "Items stored in the freezer",
            cls.BEVERAGES: "Drinks including juice, soda, etc.",
            cls.SNACKS: "Packaged snacks like chips, biscuits, granola bars",
            cls.OTHER: "Doesn't fit into any above categories",
        }

    @classmethod
    def labels(cls):
        return {category: category.value for category in cls}
