from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PantryPalBaseModelDomain(BaseModel):
    id: int
    created_at: datetime


class PantryPalMutableModelDomain(PantryPalBaseModelDomain):
    updated_at: Optional[datetime]
