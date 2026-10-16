import pandas as pd

students = pd.read_csv("students.csv")
scores = pd.read_csv("scores.csv")

# Check missing values
print(students.isnull().sum())
print(scores.isnull().sum())

# Fill missing data
subjects = ["python", "math", "database"]
scores[subjects] = scores[subjects].fillna(scores[subjects].median())
students["age"] = students["age"].fillna(students["age"].median())
students["GPA"] = students["GPA"].fillna(students["GPA"].median())

merged = pd.merge(students, scores, on="student_id", how="inner")
print(merged.head())

# Each student's average score
merged["avg_score"] = merged[subjects].mean(axis=1).round(2)
print(merged[["student_id", "name", "major", "avg_score"]])

# Top 5 students
top5 = merged.sort_values(by="avg_score", ascending=False).head(5)
print(top5[["student_id", "name", "major", "avg_score"]])

# Average score by major
print(merged.groupby("major")["avg_score"].mean().round(2))
