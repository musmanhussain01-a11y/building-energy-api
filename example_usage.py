"""
Example script showing how to use the Building Energy Data API
Run the API first: python main.py
Then run this script: python example_usage.py
"""
import requests
from datetime import datetime, timedelta
import json

# API base URL
BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")


def main():
    """Example usage of the Building Energy Data API"""
    
    print("\n🏢 Building Energy Data API - Example Usage\n")
    
    # ========================================
    # 1. Create Buildings
    # ========================================
    print("\n1️⃣  Creating buildings...")
    
    buildings = [
        {
            "name": "Tech Campus Building A",
            "address": "123 Innovation Street, Berlin",
            "type": "commercial"
        },
        {
            "name": "Green Office Complex",
            "address": "456 Solar Avenue, Munich",
            "type": "commercial"
        },
        {
            "name": "Residential Tower",
            "address": "789 Home Street, Hamburg",
            "type": "residential"
        }
    ]
    
    building_ids = []
    for building_data in buildings:
        response = requests.post(f"{BASE_URL}/buildings", json=building_data)
        print_response(f"Created: {building_data['name']}", response)
        building_ids.append(response.json()["id"])
    
    # ========================================
    # 2. Add Energy Readings
    # ========================================
    print("\n\n2️⃣  Adding energy readings...")
    
    now = datetime.utcnow()
    building_id = building_ids[0]
    
    readings = [
        {"timestamp": now - timedelta(hours=3), "consumption_kwh": 50.5, "source_type": "grid"},
        {"timestamp": now - timedelta(hours=2), "consumption_kwh": 45.2, "source_type": "solar"},
        {"timestamp": now - timedelta(hours=1), "consumption_kwh": 55.8, "source_type": "grid"},
        {"timestamp": now, "consumption_kwh": 40.3, "source_type": "battery"},
    ]
    
    for reading_data in readings:
        # Convert datetime to ISO format string
        reading_data["timestamp"] = reading_data["timestamp"].isoformat()
        response = requests.post(
            f"{BASE_URL}/buildings/{building_id}/readings",
            json=reading_data
        )
        source = reading_data["source_type"]
        print_response(f"Added reading from {source}", response)
    
    # ========================================
    # 3. Retrieve All Readings
    # ========================================
    response = requests.get(f"{BASE_URL}/buildings/{building_id}/readings")
    print_response("Retrieved all readings", response)
    
    # ========================================
    # 4. Filter by Date Range
    # ========================================
    start_date = (now - timedelta(hours=2.5)).isoformat()
    end_date = (now - timedelta(hours=0.5)).isoformat()
    
    response = requests.get(
        f"{BASE_URL}/buildings/{building_id}/readings",
        params={
            "start_date": start_date,
            "end_date": end_date
        }
    )
    print_response("Filtered by date range (2.5h-0.5h ago)", response)
    
    # ========================================
    # 5. Filter by Source Type
    # ========================================
    response = requests.get(
        f"{BASE_URL}/buildings/{building_id}/readings",
        params={"source_type": "grid"}
    )
    print_response("Filtered by source type (grid only)", response)
    
    # ========================================
    # 6. Multiple Filters
    # ========================================
    response = requests.get(
        f"{BASE_URL}/buildings/{building_id}/readings",
        params={
            "source_type": "solar",
            "start_date": (now - timedelta(hours=3)).isoformat(),
            "end_date": now.isoformat()
        }
    )
    print_response("Multiple filters (solar, last 3 hours)", response)
    
    # ========================================
    # 7. Pagination
    # ========================================
    response = requests.get(
        f"{BASE_URL}/buildings/{building_id}/readings",
        params={"limit": 2, "offset": 0}
    )
    print_response("Pagination (limit=2, offset=0)", response)
    
    # ========================================
    # 8. Test Error Cases
    # ========================================
    print("\n\n3️⃣  Testing error handling...\n")
    
    # Try to add reading to non-existent building
    response = requests.post(
        f"{BASE_URL}/buildings/bldg_nonexistent/readings",
        json={
            "timestamp": now.isoformat(),
            "consumption_kwh": 25.0,
            "source_type": "grid"
        }
    )
    print_response("Error: Add reading to non-existent building (404)", response)
    
    # Try to add reading with negative consumption
    response = requests.post(
        f"{BASE_URL}/buildings/{building_id}/readings",
        json={
            "timestamp": now.isoformat(),
            "consumption_kwh": -10.0,
            "source_type": "grid"
        }
    )
    print_response("Error: Negative consumption (422)", response)
    
    # Try to add duplicate reading
    duplicate_time = (now - timedelta(hours=3)).isoformat()
    requests.post(
        f"{BASE_URL}/buildings/{building_id}/readings",
        json={
            "timestamp": duplicate_time,
            "consumption_kwh": 100.0,
            "source_type": "wind"  # Invalid source, but let's try
        }
    )
    
    # Now try again with valid source
    response = requests.post(
        f"{BASE_URL}/buildings/{building_id}/readings",
        json={
            "timestamp": duplicate_time,
            "consumption_kwh": 100.0,
            "source_type": "grid"
        }
    )
    print_response("First duplicate reading (should succeed)", response)
    
    # Try exact duplicate
    response = requests.post(
        f"{BASE_URL}/buildings/{building_id}/readings",
        json={
            "timestamp": duplicate_time,
            "consumption_kwh": 100.0,
            "source_type": "grid"
        }
    )
    print_response("Second duplicate reading (409 Conflict)", response)
    
    # ========================================
    # 9. Health Check
    # ========================================
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health check", response)
    
    print("\n✅ Example usage complete!")
    print(f"View interactive API docs at: {BASE_URL}/docs")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API")
        print("Make sure the API is running: python main.py")
