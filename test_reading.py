from app.reading.reading_loader import load_readings

readings = load_readings()

print(f"Loaded {len(readings)} readings")

print(readings[0])