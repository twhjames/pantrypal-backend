from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PantryPalBaseModelDomain:
    id: int
    created_at: datetime


@dataclass
class PantryPalMutableModelDomain(PantryPalBaseModelDomain):
    updated_at: Optional[datetime]
