"""
Simple tests for the Building Energy API
"""
from fastapi.testclient import TestClient
from main import app
from datetime import datetime, timedelta

# Create a test client
client = TestClient(app)

# ========================================
# Test Building Creation
# ========================================

def test_create_building():
    """Test creating a building"""
    response = client.post("/buildings", json={
        "name": "Office Building",
        "address": "123 Main Street",
        "type": "commercial"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Office Building"
    assert data["type"] == "commercial"
    assert "id" in data


def test_get_building():
    """Test getting a building"""
    # Create a building first
    create_response = client.post("/buildings", json={
        "name": "Test Building",
        "address": "456 Oak Ave",
        "type": "residential"
    })
    building_id = create_response.json()["id"]
    
    # Get it
    response = client.get(f"/buildings/{building_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Building"


def test_get_building_not_found():
    """Test getting a building that doesn't exist"""
    response = client.get("/buildings/fake_id")
    assert response.status_code == 404


# ========================================
# Test Energy Readings
# ========================================

def test_add_reading():
    """Test adding an energy reading"""
    # Create building first
    building_response = client.post("/buildings", json={
        "name": "Test Building",
        "address": "789 Street",
        "type": "commercial"
    })
    building_id = building_response.json()["id"]
    
    # Add reading
    now = datetime.utcnow()
    response = client.post(f"/buildings/{building_id}/readings", json={
        "timestamp": now.isoformat(),
        "consumption_kwh": 50.5,
        "source_type": "grid"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["consumption_kwh"] == 50.5
    assert data["source_type"] == "grid"


def test_add_reading_negative_consumption():
    """Test that negative consumption is rejected"""
    building_response = client.post("/buildings", json={
        "name": "Test",
        "address": "123 St",
        "type": "residential"
    })
    building_id = building_response.json()["id"]
    
    response = client.post(f"/buildings/{building_id}/readings", json={
        "timestamp": datetime.utcnow().isoformat(),
        "consumption_kwh": -10.0,
        "source_type": "solar"
    })
    
    assert response.status_code == 400


def test_get_readings():
    """Test getting readings"""
    # Create building
    building_response = client.post("/buildings", json={
        "name": "Test",
        "address": "123 St",
        "type": "commercial"
    })
    building_id = building_response.json()["id"]
    
    # Add 2 readings
    now = datetime.utcnow()
    for i in range(2):
        client.post(f"/buildings/{building_id}/readings", json={
            "timestamp": (now + timedelta(hours=i)).isoformat(),
            "consumption_kwh": 30.0,
            "source_type": "grid"
        })
    
    # Get readings
    response = client.get(f"/buildings/{building_id}/readings")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 2
    assert len(data["readings"]) == 2


if __name__ == "__main__":
    # Run a simple test
    print("Running basic tests...")
    test_create_building()
    print("✅ Create building test passed")
    
    test_get_building()
    print("✅ Get building test passed")
    
    test_add_reading()
    print("✅ Add reading test passed")
    
    print("\n✅ All tests passed!")
