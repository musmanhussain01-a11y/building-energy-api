# Building Energy Data API

A production-ready REST API for managing building energy consumption data. Built with FastAPI and designed for scalability, reliability, and ease of use.

## Project Overview

This API provides a backend service for a building management platform that:
- Manages building information (name, address, type)
- Tracks energy consumption readings from various sensors
- Provides flexible querying and filtering of historical data
- Implements robust validation and error handling

## Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd building-energy-api
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the API

```bash
python main.py
```

The API will start on `http://localhost:8000`

**Interactive API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Buildings

#### 1. Create Building
```http
POST /buildings
Content-Type: application/json

{
  "name": "Tech Campus Building A",
  "address": "123 Innovation Street, Berlin",
  "type": "commercial"
}
```

**Response (201 Created):**
```json
{
  "id": "bldg_a1b2c3d4",
  "name": "Tech Campus Building A",
  "address": "123 Innovation Street, Berlin",
  "type": "commercial",
  "created_at": "2024-02-16T10:30:00"
}
```

**Parameters:**
- `name` (string, required): Building name (1-200 characters)
- `address` (string, required): Building address (1-500 characters)
- `type` (enum, required): One of `residential`, `commercial`, `industrial`

**Error Responses:**
- `400 Bad Request`: Invalid input data
- `422 Unprocessable Entity`: Validation error (e.g., invalid building type)

---

#### 2. Get Building
```http
GET /buildings/{building_id}
```

**Response (200 OK):**
```json
{
  "id": "bldg_a1b2c3d4",
  "name": "Tech Campus Building A",
  "address": "123 Innovation Street, Berlin",
  "type": "commercial",
  "created_at": "2024-02-16T10:30:00"
}
```

**Error Responses:**
- `404 Not Found`: Building not found

---

### Energy Readings

#### 3. Add Energy Reading
```http
POST /buildings/{building_id}/readings
Content-Type: application/json

{
  "timestamp": "2024-02-16T14:30:00",
  "consumption_kwh": 45.5,
  "source_type": "grid"
}
```

**Response (201 Created):**
```json
{
  "id": "read_x8y9z0a1",
  "building_id": "bldg_a1b2c3d4",
  "timestamp": "2024-02-16T14:30:00",
  "consumption_kwh": 45.5,
  "source_type": "grid",
  "created_at": "2024-02-16T14:31:00"
}
```

**Parameters:**
- `timestamp` (ISO 8601 datetime, required): Reading timestamp
- `consumption_kwh` (number, required): Energy consumption (≥ 0)
- `source_type` (enum, required): One of `solar`, `grid`, `battery`

**Validation Rules:**
- Energy consumption cannot be negative
- Building must exist
- Duplicate readings (same building, timestamp, source) are rejected

**Error Responses:**
- `400 Bad Request`: Invalid input or validation error
- `404 Not Found`: Building not found
- `409 Conflict`: Duplicate reading detected
- `422 Unprocessable Entity`: Invalid data type

---

#### 4. Get Energy Readings
```http
GET /buildings/{building_id}/readings?start_date=2024-02-16T00:00:00&end_date=2024-02-17T00:00:00&source_type=solar&limit=50&offset=0
```

**Response (200 OK):**
```json
{
  "readings": [
    {
      "id": "read_x8y9z0a1",
      "building_id": "bldg_a1b2c3d4",
      "timestamp": "2024-02-16T14:30:00",
      "consumption_kwh": 45.5,
      "source_type": "grid",
      "created_at": "2024-02-16T14:31:00"
    }
  ],
  "total_count": 1,
  "filters_applied": {
    "start_date": "2024-02-16T00:00:00",
    "end_date": "2024-02-17T00:00:00",
    "source_type": "solar"
  }
}
```

**Query Parameters:**
- `start_date` (ISO 8601 datetime, optional): Filter readings after this date
- `end_date` (ISO 8601 datetime, optional): Filter readings before this date
- `source_type` (enum, optional): Filter by source type (`solar`, `grid`, `battery`)
- `limit` (integer, optional): Max results per page (default: 100, max: 1000)
- `offset` (integer, optional): Pagination offset (default: 0)

**Features:**
- Results sorted by timestamp (newest first)
- Pagination support for large datasets
- `total_count` reflects all matching records (not just the current page)
- Comprehensive date range filtering

**Error Responses:**
- `400 Bad Request`: Invalid date format or source type
- `404 Not Found`: Building not found

---

### Health Check

#### 5. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-02-16T15:00:00"
}
```

---

## Testing

Run the test suite:

```bash
pytest test_main.py -v
```

Test coverage includes:
- Building creation and retrieval
- Energy reading creation with validation
- Date range filtering
- Source type filtering
- Pagination
- Duplicate prevention
- Error handling for all edge cases

## Design Decisions & Trade-offs

### 1. Framework Choice: FastAPI
**Decision:** Use FastAPI instead of Flask or Django REST Framework

**Rationale:**
- **Performance:** FastAPI is one of the fastest Python web frameworks
- **Type Safety:** Pydantic models provide automatic validation and serialization
- **Auto Documentation:** Automatic Swagger UI and ReDoc generation
- **Modern Python:** Uses async/await and type hints (Python 3.6+)
- **Developer Experience:** Clear, intuitive API design

### 2. In-Memory Storage
**Decision:** Use simple Python dictionaries for storage instead of a database

**Rationale:**
- **Requirements Met:** Task explicitly allows in-memory storage
- **Simplicity:** No database setup overhead
- **Development Speed:** Focuses on API design and business logic
- **Scalability Path:** Can be replaced with SQLAlchemy ORM in production

**Trade-off:** Data is lost on application restart. Add a database when:
- Persistence across restarts is required
- Multiple instances need to share data
- Data volume exceeds memory capacity

### 3. Duplicate Prevention Strategy
**Decision:** Track duplicates using a set of composite keys: (building_id, timestamp, source_type)

**Rationale:**
- **Uniqueness Definition:** Same building, timestamp, and source is a logical duplicate
- **Performance:** O(1) lookup in a set
- **Simplicity:** No need for complex query logic

**Implementation:** `reading_duplicates` set stores tuples of the composite key

### 4. Timestamp Handling
**Decision:** Use UTC timezone for all timestamps

**Rationale:**
- **Consistency:** Eliminates timezone-related bugs
- **International Support:** Works across regions
- **Standards:** ISO 8601 is the standard format

**Note:** All timestamps are in UTC. Convert to local time in client applications if needed.

### 5. ID Generation
**Decision:** Use UUID-based prefixed IDs (e.g., "bldg_a1b2c3d4")

**Rationale:**
- **Readability:** Prefixes indicate resource type
- **Uniqueness:** UUID ensures no collisions
- **URL-friendly:** Short 8-character hex strings
- **Scalability:** Works with distributed systems

### 6. Error Handling
**Decision:** Return specific HTTP status codes with detailed error messages

**Rationale:**
- **HTTP Best Practices:** 201 for creation, 404 for not found, 409 for conflicts
- **Client Integration:** Clients can handle errors programmatically
- **Debugging:** Detailed messages help identify issues
- **Consistency:** All errors follow the same response format

## Key Assumptions

1. **Timestamps are UTC:** All datetime values are assumed to be in UTC
2. **Building IDs are immutable:** Building identifiers don't change after creation
3. **No authentication required:** The task doesn't require auth - add if needed for production
4. **Reading sources are finite:** Only solar, grid, and battery are valid sources
5. **Energy consumption is always positive:** Negative values represent an error, not generation
6. **Single-instance deployment:** No distributed system constraints

## Performance Considerations

### Current Implementation
- Building lookup: O(1) dictionary access
- Reading retrieval: O(n) linear scan with filtering
- Duplicate check: O(1) set lookup
- Pagination: O(n log n) for sorting, then O(k) for slice

### Optimization Opportunities
1. **Add indexing** for timestamp and source_type fields
2. **Implement caching** for frequently accessed readings
3. **Add database** with proper indexes for large datasets (100k+ readings)
4. **Implement read replicas** for high-traffic scenarios
5. **Consider time-series databases** (InfluxDB, TimescaleDB) for sensor data

### Production Readiness Checklist
- [ ] Add database (PostgreSQL recommended)
- [ ] Implement connection pooling
- [ ] Add authentication/authorization
- [ ] Set up logging and monitoring
- [ ] Configure CORS if frontend is separate domain
- [ ] Add rate limiting
- [ ] Implement caching (Redis)
- [ ] Add request validation middleware
- [ ] Set up CI/CD pipeline
- [ ] Create deployment configuration

## File Structure

```
building-energy-api/
├── main.py                 # FastAPI application and route handlers
├── models.py               # Pydantic data models and schemas
├── storage.py              # In-memory storage implementation
├── test_main.py            # Comprehensive test suite
├── requirements.txt        # Python package dependencies
├── README.md               # This file
└── TASK_BRIEF.md          # Original task specification
```

## Dependencies

- **fastapi==0.104.1**: Web framework
- **uvicorn==0.24.0**: ASGI server
- **pydantic==2.5.0**: Data validation
- **python-dateutil==2.8.2**: Date parsing
- **pytest==7.4.3**: Testing framework
- **pytest-asyncio==0.21.1**: Async test support
- **httpx==0.25.2**: Test client

## Time Spent

- **Project Setup:** 15 minutes
- **Data Models & Validation:** 20 minutes
- **API Endpoints Implementation:** 35 minutes
- **Testing Suite:** 25 minutes
- **Documentation:** 25 minutes
- **Total: ~2 hours**

## Future Enhancements

1. **Batch Operations:** POST endpoint to create multiple readings at once
2. **Energy Statistics:** GET endpoint for building energy stats (daily avg, peak, etc.)
3. **Alerts:** Create alerts for energy consumption thresholds
4. **User Management:** Track which users made which readings
5. **WebSocket Support:** Real-time energy data streaming
6. **Export:** CSV/JSON export of readings data
7. **Building Groups:** Organize buildings by region/department

## Troubleshooting

### Port Already in Use
```bash
# Change port in main.py or run:
python -m uvicorn main:app --port 8001
```

### Import Errors
```bash
# Ensure virtual environment is activated and pip install worked
pip install -r requirements.txt
```

### Tests Failing
```bash
# Ensure in-memory storage is fresh and dependencies installed
pip install -r requirements.txt
pytest test_main.py -v
```

## Questions?

Refer to the API documentation at `http://localhost:8000/docs` when running the server.

---

**Status:** Production-ready for demonstration and testing purposes. For production deployment, follow the checklist in "Production Readiness Checklist" above.
