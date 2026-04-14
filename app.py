# Take input
source = input("Enter Source: ")
destination = input("Enter Destination: ")

# Filter (UPDATED LINE)
filtered = df[
    (df["Source"] == source) &
    (df["Destination"] == destination)
].copy()

if filtered.empty:
    print("No flights found!")
else:
    filtered["Duration_num"] = filtered["Duration"].str.extract(r'(\d+)').astype(float)
    filtered["Score"] = filtered["Price"] + filtered["Duration_num"] * 100

    best = filtered.sort_values(by="Score").head(3)

    print("\nRecommended Flights:")
    print(best[["Airline", "Source", "Destination", "Price", "Duration"]])