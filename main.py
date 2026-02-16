"""
Building Energy Data API - Simple REST API for managing building energy
"""
from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
from models import BuildingCreate, Building, EnergyReadingCreate, EnergyReading, EnergyReadingsResponse
import storage

# Create the FastAPI app
app = FastAPI(
    title="Building Energy Data API",
    description="Simple API for managing building energy data"
)

# ============================================================
# BUILDING ENDPOINTS
# ============================================================

@app.post("/buildings", response_model=Building, status_code=201)
def create_building(building: BuildingCreate):
    """Create a new building
    
    Required fields:
    - name: Building name
    - address: Building address
    - type: "residential", "commercial", or "industrial"
    """
    # Check if type is valid
    valid_types = ["residential", "commercial", "industrial"]
    if building.type not in valid_types:
        raise HTTPException(status_code=400, detail=f"Type must be one of: {valid_types}")
    
    # Create building
    new_building = storage.create_building(building)
    return new_building


@app.get("/buildings/{building_id}", response_model=Building)
def get_building(building_id: str):
    """Get a building by ID"""
    building = storage.get_building(building_id)
    
    if not building:
        raise HTTPException(status_code=404, detail=f"Building {building_id} not found")
    
    return building


# ============================================================
# ENERGY READING ENDPOINTS
# ============================================================

@app.post("/buildings/{building_id}/readings", response_model=EnergyReading, status_code=201)
def add_reading(building_id: str, reading: EnergyReadingCreate):
    """Add an energy reading to a building
    
    Required fields:
    - timestamp: When the reading was taken (ISO format)
    - consumption_kwh: Energy used in kilowatt-hours (must be >= 0)
    - source_type: "solar", "grid", or "battery"
    """
    # Check if consumption is negative
    if reading.consumption_kwh < 0:
        raise HTTPException(status_code=400, detail="Consumption cannot be negative")
    
    # Check if source type is valid
    valid_sources = ["solar", "grid", "battery"]
    if reading.source_type not in valid_sources:
        raise HTTPException(status_code=400, detail=f"Source must be: {valid_sources}")
    
    try:
        # Add reading
        new_reading = storage.add_reading(building_id, reading)
        return new_reading
    except ValueError as e:
        # Handle errors like building not found or duplicate reading
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=404, detail=error_msg)
        elif "already exists" in error_msg:
            raise HTTPException(status_code=409, detail=error_msg)
        else:
            raise HTTPException(status_code=400, detail=error_msg)


@app.get("/buildings/{building_id}/readings", response_model=EnergyReadingsResponse)
def get_readings(
    building_id: str,
    start_date: str = Query(None, description="Start date in ISO format"),
    end_date: str = Query(None, description="End date in ISO format"),
    source_type: str = Query(None, description="Filter by: solar, grid, or battery")
):
    """Get energy readings for a building with optional filters"""
    
    # Parse dates if provided
    start_datetime = None
    end_datetime = None
    
    if start_date:
        try:
            start_datetime = datetime.fromisoformat(start_date)
        except:
            raise HTTPException(status_code=400, detail=f"Invalid start_date format: {start_date}")
    
    if end_date:
        try:
            end_datetime = datetime.fromisoformat(end_date)
        except:
            raise HTTPException(status_code=400, detail=f"Invalid end_date format: {end_date}")
    
    # Validate source type if provided
    if source_type and source_type not in ["solar", "grid", "battery"]:
        raise HTTPException(status_code=400, detail="Source must be: solar, grid, or battery")
    
    try:
        # Get readings from storage
        all_readings = storage.get_readings(
            building_id,
            start_date=start_datetime,
            end_date=end_datetime,
            source_type=source_type
        )
        
        # Track which filters were used
        filters_used = {}
        if start_date:
            filters_used["start_date"] = start_date
        if end_date:
            filters_used["end_date"] = end_date
        if source_type:
            filters_used["source_type"] = source_type
        
        # Return response
        return EnergyReadingsResponse(
            readings=all_readings,
            total_count=len(all_readings),
            filters_applied=filters_used
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():
    """Simple test endpoint"""
    return {
        "message": "Building Energy API is working!",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "OK", "time": datetime.utcnow().isoformat()}


# ============================================================
# RUN THE SERVER
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
