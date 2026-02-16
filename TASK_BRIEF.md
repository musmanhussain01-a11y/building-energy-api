# Backend Engineering Task: Building Energy Data API

## Overview
This is a practical backend engineering task designed to assess your API design, code structure, and problem-solving approach. You will build a REST API that manages building energy consumption data.

- **Time Allocation:** 4-5 hours (strictly time-boxed)
- **Language:** Python (required)
- **Framework:** Your choice (Flask, FastAPI, Django REST, or any other)
- **Database:** In-memory storage is acceptable (no database setup required)
- **Authentication:** Not required

## Scenario
You are building a backend service for a building management platform. The service needs to store building information and track energy consumption readings from various sensors. Your API will be used by frontend applications and third-party integrations.

## Requirements

### 1. Data Models
Design and implement data models for:

#### Buildings
- Unique identifier
- Building name
- Address
- Building type (e.g., residential, commercial, industrial)

#### Energy Readings
- Timestamp
- Building reference
- Energy consumption in kWh
- Energy source type (e.g., solar, grid, battery)

### 2. API Endpoints
Implement the following 3 RESTful endpoints:

#### a) Create Building
```
POST /buildings
```
Create a new building with the provided information.

#### b) Add Energy Reading
```
POST /buildings/{id}/readings
```
Add a new energy reading for a specific building.

#### c) Get Energy Readings
```
GET /buildings/{id}/readings
```
Retrieve energy readings for a building with optional query filters:
- Filter by date range (start_date, end_date)
- Filter by energy source type
- Return total count of readings

### 3. Data Quality & Validation
Implement proper validation and error handling:
- Energy consumption values cannot be negative
- Timestamps must be valid and properly formatted
- Building must exist before adding readings
- Handle duplicate reading prevention (same building, timestamp, source)
- Return appropriate HTTP status codes and error messages

### 4. Documentation
Create a README.md file that includes:
- Project overview and purpose
- Setup instructions (dependencies, installation, running the service)
- API endpoint documentation with example requests/responses
- Key design decisions and trade-offs you made
- Any assumptions you made during implementation

## Evaluation Criteria

| Criteria | What We Look For |
|----------|------------------|
| Code Organization | Clear structure, separation of concerns, readable code |
| API Design | RESTful principles, appropriate HTTP methods and status codes |
| Error Handling | Graceful error handling with meaningful messages |
| Data Validation | Proper input validation and edge case handling |
| Documentation | Clear setup instructions and API documentation |
| Performance Awareness | Understanding of potential bottlenecks (even if not fully optimized) |

## Bonus Points (Optional - Not Required)
These are completely optional and should only be attempted if you have extra time:
- Unit tests for critical business logic
- Pagination for large datasets
- Basic rate limiting awareness/implementation
- Docker setup for easy deployment

## Submission Guidelines
1. **Code Repository:** Share your code via GitHub, GitLab, or a ZIP file
2. **README.md:** Include clear documentation as specified above
3. **Time Tracking:** Please note approximately how much time you spent on the task in your README
4. **Deadline:** Submit within 5 days of receiving this task

## Important Notes
✓ Focus on code quality and clear thinking over perfect implementation  
✓ Use any Python framework you are comfortable with  
✓ You can use online resources and documentation (that's normal!)  
✓ In-memory storage is perfectly acceptable - no need for a database  
✓ Ask questions if anything is unclear - we're happy to clarify  

✗ Do not spend more than 5 hours - time management is part of the evaluation  
✗ Do not over-engineer - we value pragmatic solutions  

## Example API Request/Response

### Create Building Request:
```http
POST /buildings
Content-Type: application/json

{
  "name": "Tech Campus Building A",
  "address": "123 Innovation Street, Berlin",
  "type": "commercial"
}
```

### Expected Response:
```http
HTTP 201 Created
Content-Type: application/json

{
  "id": "bldg_001",
  "name": "Tech Campus Building A",
  "address": "123 Innovation Street, Berlin",
  "type": "commercial",
  "created_at": "2024-02-16T10:30:00Z"
}
```

## Questions?
If you have any questions or need clarification on any requirements, please don't hesitate to reach out. We want you to succeed!

Good luck! We're excited to see your approach to solving this problem.
