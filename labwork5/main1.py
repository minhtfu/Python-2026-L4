import pandas as pd

df = pd.read_csv("students.csv")
# df = pd.read_excel("students.xlsx")

# Display first five rows
print(df.head())

# Number of rows and columns
rows, cols = df.shape
print(f"Rows: {rows}, Columns: {cols}")

# Select name and GPA
print(df[["name", "GPA"]])

# Students with GPA >= 3.5
high_gpa = df[df["GPA"] >= 3.5]
print(high_gpa)

# Sort students by GPA (highest first)
sorted_df = df.sort_values(by="GPA", ascending=False)
print(sorted_df)

# Average GPA by major
print(df.groupby("major")["GPA"].mean())
