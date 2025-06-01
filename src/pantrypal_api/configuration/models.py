from sqlalchemy import Column, Integer, String, Text

from src.core.configuration.models import ConfigurationDomain
from src.pantrypal_api.base.models import PantryPalBaseModel


class Configuration(PantryPalBaseModel):
    __tablename__ = "configuration"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String)
    value = Column(String)
    description = Column(Text, nullable=True)

    def to_domain(self) -> ConfigurationDomain:
        return ConfigurationDomain(key=self.key, value=self.value)
