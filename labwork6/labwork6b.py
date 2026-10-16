import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("scores.csv")
courses = ["math", "python", "database"]

# scatter plot of student scores
plt.figure(figsize=(10, 6))
for course in courses:
    plt.scatter(df["student_id"], df[course], label=course)
plt.title("Student scores")
plt.xlabel("student_id")
plt.ylabel("score")
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("scattered.png")
plt.close()

# histograms, one subplot per course
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, course in zip(axes, courses):
    ax.hist(df[course], bins=10, edgecolor="black")
    ax.set_title(course)
    ax.set_xlabel("score")
    ax.set_ylabel("frequency")
plt.tight_layout()
plt.savefig("histo.png")
plt.close()

# single box plot for all three courses
plt.figure(figsize=(6, 5))
df[courses].plot.box()
plt.title("Score distribution by course")
plt.ylabel("score")
plt.tight_layout()
plt.savefig("box.png")
plt.close()
