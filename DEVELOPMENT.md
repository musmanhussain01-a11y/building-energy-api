# Development Guide

This document provides additional technical details for developers working with the Building Energy Data API.

## Quick Start for Development

### 1. Clone/Download the Project
```bash
cd building-energy-api
```

### 2. Run Setup Script

**On Windows:**
```bash
setup.bat
```

**On macOS/Linux:**
```bash
bash setup.sh
```

### 3. Start the API
```bash
python main.py
```

### 4. Access Documentation
Open http://localhost:8000/docs in your browser

## Project Structure

```
building-energy-api/
├── main.py                 # FastAPI application & route handlers (277 lines)
├── models.py               # Pydantic data models & validation (48 lines)
├── storage.py              # In-memory storage implementation (88 lines)
├── test_main.py            # Comprehensive test suite (350+ lines)
├── example_usage.py        # Example API usage script
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container configuration
├── docker-compose.yml      # Docker Compose setup
├── README.md               # User documentation
├── DEVELOPMENT.md          # This file
├── TASK_BRIEF.md           # Original task specification
├── setup.sh                # Linux/macOS setup script
├── setup.bat               # Windows setup script
└── .gitignore              # Git ignore rules
```

## Code Architecture

### main.py - Application Layer
Handles:
- FastAPI application setup
- API endpoint handlers
- Request validation
- Response formatting
- Error handling

**Key Functions:**
- `create_building()` - POST /buildings
- `get_building()` - GET /buildings/{id}
- `add_energy_reading()` - POST /buildings/{id}/readings
- `get_energy_readings()` - GET /buildings/{id}/readings (with filters)
- `health_check()` - GET /health

### models.py - Data Models
Pydantic schemas for:
- `BuildingCreate` - Request schema for creating buildings
- `Building` - Response schema with metadata
- `EnergyReadingCreate` - Request schema for readings
- `EnergyReading` - Response schema with IDs
- `EnergyReadingsResponse` - Paginated readings response
- `ErrorResponse` - Standardized error format

**Validation Rules:**
- Building name: 1-200 characters, whitespace trimmed
- Building address: 1-500 characters, whitespace trimmed
- Building type: Enum (residential, commercial, industrial)
- Energy consumption: Non-negative float (≥ 0)
- Source type: Enum (solar, grid, battery)
- Timestamp: ISO 8601 format

### storage.py - Data Access Layer
`BuildingStore` class provides:
- `create_building()` - Create and store building
- `get_building()` - Retrieve building by ID
- `building_exists()` - Check building existence
- `add_reading()` - Add reading with duplicate detection
- `get_readings()` - Retrieve with filtering and pagination

**In-Memory Storage Structure:**
```python
buildings = {
    "bldg_a1b2c3d4": Building(...),
    ...
}

readings = {
    "bldg_a1b2c3d4": [EnergyReading(...), ...],
    ...
}

reading_duplicates = {
    ("bldg_a1b2c3d4", "2024-02-16T10:30:00", "grid"),
    ...
}
```

### test_main.py - Test Suite
Test classes:
- `TestBuildings` - Building CRUD operations
- `TestEnergyReadings` - Reading operations and filtering
- `TestHealthEndpoints` - Health check endpoints

**Coverage:**
- ✅ Successful operations (all 3 endpoints)
- ✅ Validation errors
- ✅ Not found errors
- ✅ Date filtering
- ✅ Source type filtering
- ✅ Pagination
- ✅ Duplicate prevention
- ✅ Error handling

Run tests with:
```bash
pytest test_main.py -v

# Run specific test class
pytest test_main.py::TestBuildings -v

# Run with coverage
pytest test_main.py --cov=. --cov-report=html
```

## API Response Formats

### Success Response (2xx)
```json
{
  "id": "bldg_a1b2c3d4",
  "name": "Building Name",
  ...
}
```

### List Response
```json
{
  "readings": [...],
  "total_count": 42,
  "filters_applied": {
    "source_type": "solar"
  }
}
```

### Error Response
```json
{
  "detail": "Building with ID bldg_xyz not found",
  "status_code": 404
}
```

## HTTP Status Codes Used

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | GET successful |
| 201 | Created | POST successful |
| 400 | Bad Request | Invalid input format |
| 404 | Not Found | Building doesn't exist |
| 409 | Conflict | Duplicate reading |
| 422 | Unprocessable Entity | Validation failed |
| 500 | Server Error | Unexpected error |

## Data Validation Flow

### Building Creation
```
POST /buildings
  ↓
Pydantic validates request
  ↓
Check constraints (length, type)
  ↓
Generate ID & timestamp
  ↓
Store in memory
  ↓
Return 201 Created
```

### Reading Creation
```
POST /buildings/{id}/readings
  ↓
Pydantic validates request
  ↓
Check consumption >= 0
  ↓
Check timestamp format
  ↓
Check building exists
  ↓
Check duplicate (building_id, timestamp, source)
  ↓
Store reading
  ↓
Return 201 Created
```

### Reading Retrieval
```
GET /buildings/{id}/readings?filters
  ↓
Check building exists
  ↓
Parse & validate filters
  ↓
Apply date range filter
  ↓
Apply source type filter
  ↓
Sort by timestamp (desc)
  ↓
Apply pagination
  ↓
Return 200 OK with readings
```

## Example Development Tasks

### Add a New Endpoint

1. **Define the data model in `models.py`:**
```python
class BuildingStats(BaseModel):
    """Building energy statistics"""
    total_consumption: float
    average_consumption: float
    peak_consumption: float
    period: str
```

2. **Add the business logic in `storage.py`:**
```python
def get_building_stats(self, building_id: str) -> dict:
    """Calculate building statistics"""
    readings = self.readings.get(building_id, [])
    if not readings:
        return None
    consumptions = [r.consumption_kwh for r in readings]
    return {
        "total": sum(consumptions),
        "average": sum(consumptions) / len(consumptions),
        "peak": max(consumptions)
    }
```

3. **Add the route in `main.py`:**
```python
@app.get("/buildings/{building_id}/stats", response_model=BuildingStats)
def get_building_stats(building_id: str):
    """Get energy statistics for a building"""
    if not store.building_exists(building_id):
        raise HTTPException(status_code=404, detail="Building not found")
    
    stats = store.get_building_stats(building_id)
    if not stats:
        raise HTTPException(status_code=400, detail="No readings available")
    
    return stats
```

4. **Add tests in `test_main.py`:**
```python
def test_get_building_stats(self, building_id):
    """Test building statistics endpoint"""
    # Add some readings first
    # Then call the endpoint
    # Assert statistics are correct
```

### Add Authentication

1. **Install dependency:**
```bash
pip install fastapi-security
```

2. **Add auth logic:**
```python
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

@app.post("/buildings", response_model=Building)
def create_building(building: BuildingCreate, credentials: HTTPAuthCredentials = Depends(security)):
    # Verify token
    # Then proceed
```

### Add Rate Limiting

1. **Install dependency:**
```bash
pip install slowapi
```

2. **Configure in main.py:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/buildings")
@limiter.limit("10/minute")
def create_building(request: Request, building: BuildingCreate):
    # Rate limited to 10 per minute
```

## Performance Profiling

### Profile API Response Times

```python
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

Then check response headers:
```bash
curl -i http://localhost:8000/buildings/bldg_123/readings
# Look for: X-Process-Time: 0.012
```

### Load Testing with Locust

```bash
pip install locust
```

Create `locustfile.py`:
```python
from locust import HttpUser, task, constant

class APIUser(HttpUser):
    wait_time = constant(1)
    
    @task
    def get_readings(self):
        self.client.get("/buildings/bldg_123/readings")
```

Run: `locust -f locustfile.py`

## Debugging Tips

### Enable Debug Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Creating building: {building_data}")
```

### Use FastAPI Debug Mode
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, log_level="debug")
```

### Inspect Request/Response
```bash
# Use httpx with print statements
response = requests.get("http://localhost:8000/buildings")
print(response.headers)
print(response.json())
```

## Database Migration Path

To migrate from in-memory to PostgreSQL:

1. **Install SQLAlchemy:**
```bash
pip install sqlalchemy psycopg2-binary
```

2. **Create SQLAlchemy models:**
```python
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BuildingDB(Base):
    __tablename__ = "buildings"
    id = Column(String, primary_key=True)
    name = Column(String)
    address = Column(String)
    type = Column(String)
    created_at = Column(DateTime)
```

3. **Replace storage.py implementation** with SQLAlchemy queries

4. **Update requirements.txt** with database packages

5. **Run migrations** with Alembic

## Contributing Guidelines

1. **Follow PEP 8** style guide
2. **Add type hints** to all functions
3. **Write tests** for new features
4. **Update documentation** for API changes
5. **Commit messages** should be descriptive
6. **Keep functions small** and focused (single responsibility)

## Resources

- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **Pydantic Documentation:** https://docs.pydantic.dev/
- **SQLAlchemy:** https://www.sqlalchemy.org/
- **Pytest:** https://docs.pytest.org/
- **RESTful API Design:** https://restfulapi.net/

---

**Version:** 1.0.0  
**Last Updated:** February 16, 2024
