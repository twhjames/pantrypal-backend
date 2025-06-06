from sqlalchemy import Column, String, Text

from src.core.configuration.models import ConfigurationDomain
from src.pantrypal_api.base.models import PantryPalBaseModel


class Configuration(PantryPalBaseModel):
    __tablename__ = "configuration"

    key = Column(String)
    value = Column(String)
    description = Column(Text, nullable=True)

    def to_domain(self) -> ConfigurationDomain:
        return ConfigurationDomain(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            key=self.key,
            value=self.value,
            description=self.description,
        )
