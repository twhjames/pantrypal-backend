from typing import Optional

from src.core.base.models import PantryPalMutableModelDomain


class ConfigurationDomain(PantryPalMutableModelDomain):
    key: str
    value: str
    description: Optional[str]
