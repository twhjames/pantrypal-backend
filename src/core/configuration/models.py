from typing import Optional

from src.core.base.models import PantryPalBaseModelDomain
from src.core.common.constants import JSON_FIELD_OPTION_TYPES


class ConfigurationDomain(PantryPalBaseModelDomain):
    key: str
    value: JSON_FIELD_OPTION_TYPES
    description: Optional[str]
