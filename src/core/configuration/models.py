from typing import Optional

from pydantic import BaseModel

from src.core.common.constants import JSON_FIELD_OPTION_TYPES


class ConfigurationDomain(BaseModel):
    key: str
    value: JSON_FIELD_OPTION_TYPES
    description: Optional[str]
