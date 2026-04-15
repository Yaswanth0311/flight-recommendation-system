import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle

df = pd.read_csv("flights.csv")

# Simple preprocessing
df = df.dropna()

X = df[["Airline","Source","Destination","Duration","Total_Stops"]]
y = df["Price"]

X = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = RandomForestRegressor()
model.fit(X_train, y_train)

pickle.dump((model, X.columns), open("model.pkl", "wb"))

print("Model trained & saved")