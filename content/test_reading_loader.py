from app.reading.reading_loader import load_readings

readings = load_readings()

print("Total readings:", len(readings))

for r in readings:
    print("\n----------------")
    print(r[:200])