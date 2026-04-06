from pydantic import BaseModel, ConfigDict
from datetime import datetime, timezone


class CookingLogCreate(BaseModel):
    date_cooked: datetime = datetime.now(timezone.utc)
    notes: str | None = None
    rating: float
    recipe_id: int

class CookingLogResponse(CookingLogCreate):
    id: int