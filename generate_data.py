import pandas as pd
import random
from datetime import datetime, timedelta

# Sample data
airlines = ["IndiGo", "Air India", "SpiceJet", "Vistara", "GoAir"]
cities = ["Bangalore", "New Delhi", "Mumbai", "Hyderabad", "Chennai", "Kolkata"]

data = []

for _ in range(1000):  # 🔥 1000 rows
    source = random.choice(cities)
    destination = random.choice([c for c in cities if c != source])

    airline = random.choice(airlines)
    price = random.randint(2000, 15000)

    duration_hours = random.randint(1, 5)
    duration_minutes = random.choice([0, 15, 30, 45])
    duration = f"{duration_hours}h {duration_minutes}m"

    # Random date within next 10 days
    random_date = datetime.today() + timedelta(days=random.randint(0, 10))
    date = random_date.strftime("%Y-%m-%d")

    data.append([airline, source, destination, price, duration, date])

# Create DataFrame
df = pd.DataFrame(data, columns=["Airline", "Source", "Destination", "Price", "Duration", "Date"])

# Save CSV
df.to_csv("flights.csv", index=False)

print("✅ Dataset generated: flights.csv")