# Building Energy Data API - Beginner's Guide

A simple REST API for managing building energy data. This code is meant to be easy to understand and learn from.

## What Does This API Do?

This API lets you:
1. **Create Buildings** - Add buildings to the system
2. **Add Energy Readings** - Record how much energy a building used
3. **Get Energy Readings** - View past energy readings

## Project Files Explained

### `main.py` - The Main Application
This is where all the API routes are defined. Think of routes as "endpoints" - they're URLs that do things.

**Main parts:**
- `POST /buildings` - Create a new building
- `GET /buildings/{id}` - Get building details
- `POST /buildings/{id}/readings` - Add an energy reading
- `GET /buildings/{id}/readings` - Get energy readings

### `models.py` - Data Structures
This file defines the "shape" of our data - what fields a building has, what fields a reading has, etc.

**Main models:**
- `BuildingCreate` - What data you send to CREATE a building
- `Building` - What the API returns when you get a building
- `EnergyReadingCreate` - What data you send to CREATE a reading
- `EnergyReading` - What the API returns when you get a reading

### `storage.py` - Storing Data
This file handles saving and retrieving data. Right now it just uses dictionaries (no database needed).

**Functions:**
- `create_building()` - Save a new building
- `get_building()` - Find a building by ID
- `add_reading()` - Save an energy reading
- `get_readings()` - Find readings with optional filters

### `test_simple.py` - Testing
Tests to make sure everything works correctly. You can run these with: `pytest test_simple.py`

## How to Run It

### 1. Install dependencies:
```bash
pip install fastapi uvicorn pydantic
```

### 2. Start the server:
```bash
python main.py
```

### 3. Visit the API:
Open http://localhost:9000/docs in your browser - you'll see interactive documentation!

## Code Walkthrough

### Creating a Building

**Code:**
```python
@app.post("/buildings")
def create_building(building: BuildingCreate):
    new_building = storage.create_building(building)
    return new_building
```

**What it does:**
1. Receives a POST request to `/buildings`
2. Takes the building data (name, address, type)
3. Calls the storage function to save it
4. Returns the saved building with an ID

**How to use it:**
```bash
curl -X POST http://localhost:9000/buildings \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Office Building",
    "address": "123 Main Street",
    "type": "commercial"
  }'
```

### Adding an Energy Reading

**Code:**
```python
@app.post("/buildings/{building_id}/readings")
def add_reading(building_id: str, reading: EnergyReadingCreate):
    if reading.consumption_kwh < 0:
        raise HTTPException(status_code=400, detail="Consumption cannot be negative")
    
    new_reading = storage.add_reading(building_id, reading)
    return new_reading
```

**What it does:**
1. Receives a POST request with reading data
2. Checks if consumption is negative (invalid!)
3. Saves the reading
4. Returns the saved reading with an ID

### Getting Energy Readings

**Code:**
```python
@app.get("/buildings/{building_id}/readings")
def get_readings(building_id: str, start_date: str = None, end_date: str = None):
    all_readings = storage.get_readings(building_id, start_date, end_date)
    return EnergyReadingsResponse(
        readings=all_readings,
        total_count=len(all_readings),
        filters_applied=filters_used
    )
```

**What it does:**
1. Gets the building ID from the URL
2. Gets optional filter parameters (dates, source type)
3. Retrieves readings from storage
4. Returns them in a nice format

## Data Validation (Input Checking)

The code checks your input to make sure it's valid:

- **Building type** must be: `residential`, `commercial`, or `industrial`
- **Energy source** must be: `solar`, `grid`, or `battery`
- **Consumption** cannot be negative
- **Dates** must be in ISO format: `2024-02-16T10:30:00`

## Storage System

Data is stored in Python dictionaries (not a database):

```python
buildings = {}     # Stores all buildings
readings = {}      # Stores all readings
used_readings = {} # Tracks which readings we've seen (to prevent duplicates)
```

This means:
- ✅ No database setup needed
- ✅ Simple and easy to understand
- ❌ Data is lost when you restart the server
- ❌ Only works with one server instance

## Common Tasks

### Create a Building
```python
from models import BuildingCreate
import storage

building_data = BuildingCreate(
    name="My Building",
    address="123 Street",
    type="commercial"
)
building = storage.create_building(building_data)
print(building.id)
```

### Add a Reading
```python
from datetime import datetime
from models import EnergyReadingCreate
import storage

reading_data = EnergyReadingCreate(
    timestamp=datetime.now(),
    consumption_kwh=45.5,
    source_type="grid"
)
reading = storage.add_reading("b_12345", reading_data)
```

### Get Readings with Filters
```python
from datetime import datetime, timedelta

start = datetime.now() - timedelta(days=1)
end = datetime.now()

readings = storage.get_readings(
    "b_12345",
    start_date=start,
    end_date=end,
    source_type="solar"
)
```

## Error Handling

When something goes wrong, the API returns an error:

```python
raise HTTPException(status_code=404, detail="Building not found")
```

This returns:
```json
{
  "detail": "Building not found"
}
```

Common status codes:
- `200` - Success
- `201` - Created successfully
- `400` - Bad request (invalid input)
- `404` - Not found
- `409` - Conflict (duplicate reading)


