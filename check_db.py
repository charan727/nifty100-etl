import pandas as pd

df = pd.read_excel("data/supporting/sectors.xlsx")

print(df.head())

print("\nColumns:\n")

print(df.columns.tolist())

print("\nRows:", len(df))