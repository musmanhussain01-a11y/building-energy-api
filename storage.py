from datetime import datetime
from uuid import uuid4
from models import Building, EnergyReading, BuildingCreate, EnergyReadingCreate

# Simple global storage - just dictionaries to store data in memory
buildings = {}  # stores buildings: {id: building_object}
readings = {}   # stores readings: {building_id: [reading1, reading2, ...]}
used_readings = set()  # keep track of readings we've already seen (to prevent duplicates)

def create_building(building_data):
    """Create a new building and save it"""
    # Generate a simple ID
    building_id = f"b_{uuid4().hex[:6]}"
    
    # Create building object with timestamp
    building = Building(
        id=building_id,
        name=building_data.name,
        address=building_data.address,
        type=building_data.type,
        created_at=datetime.utcnow()
    )
    
    # Save it to our storage
    buildings[building_id] = building
    readings[building_id] = []  # Create empty list for this building's readings
    
    return building

def get_building(building_id):
    """Get a building by ID"""
    if building_id in buildings:
        return buildings[building_id]
    return None

def add_reading(building_id, reading_data):
    """Add a reading for a building"""
    # Check if building exists
    if building_id not in buildings:
        raise ValueError(f"Building {building_id} not found")
    
    # Check for duplicate readings (same building, time, and source)
    reading_key = (building_id, str(reading_data.timestamp), reading_data.source_type)
    if reading_key in used_readings:
        raise ValueError("This exact reading already exists!")
    
    # Generate reading ID
    reading_id = f"r_{uuid4().hex[:6]}"
    
    # Create reading object
    reading = EnergyReading(
        id=reading_id,
        building_id=building_id,
        timestamp=reading_data.timestamp,
        consumption_kwh=reading_data.consumption_kwh,
        source_type=reading_data.source_type,
        created_at=datetime.utcnow()
    )
    
    # Save to storage
    readings[building_id].append(reading)
    used_readings.add(reading_key)
    
    return reading

def get_readings(building_id, start_date=None, end_date=None, source_type=None):
    """Get readings for a building with optional filters"""
    # Check if building exists
    if building_id not in buildings:
        raise ValueError(f"Building {building_id} not found")
    
    # Get all readings for this building
    all_readings = readings.get(building_id, [])
    
    # Apply filters
    filtered = all_readings
    
    # Filter by date range if provided
    if start_date:
        filtered = [r for r in filtered if r.timestamp >= start_date]
    
    if end_date:
        filtered = [r for r in filtered if r.timestamp <= end_date]
    
    # Filter by source type if provided
    if source_type:
        filtered = [r for r in filtered if r.source_type == source_type]
    
    # Sort by newest first
    filtered.sort(key=lambda r: r.timestamp, reverse=True)
    
    return filtered
