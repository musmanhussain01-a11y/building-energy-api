from pydantic import BaseModel
from datetime import datetime

# Simple model for creating a building request
class BuildingCreate(BaseModel):
    name: str
    address: str
    type: str  # "residential", "commercial", or "industrial"

# Model for building response (includes id and timestamp)
class Building(BuildingCreate):
    id: str
    created_at: datetime

# Simple model for creating an energy reading
class EnergyReadingCreate(BaseModel):
    timestamp: datetime
    consumption_kwh: float  # This should be >= 0
    source_type: str  # "solar", "grid", or "battery"

# Model for energy reading response
class EnergyReading(EnergyReadingCreate):
    id: str
    building_id: str
    created_at: datetime

# Response model for getting multiple readings
class EnergyReadingsResponse(BaseModel):
    readings: list
    total_count: int
    filters_applied: dict
