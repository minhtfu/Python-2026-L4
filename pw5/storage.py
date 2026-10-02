import csv
import os
import zipfile

from domains import Course, Student

STUDENTS_TXT = "students.txt"
COURSES_TXT = "courses.txt"
MARKS_TXT = "marks.txt"
DATA_FILE = "students.dat"
ALL_FILES = [STUDENTS_TXT, COURSES_TXT, MARKS_TXT]


def save_students(manager):
    with open(STUDENTS_TXT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for s in manager.students.values():
            writer.writerow([s.sid, s.name, s.dob])


def save_courses(manager):
    with open(COURSES_TXT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for c in manager.courses.values():
            writer.writerow([c.cid, c.name, c.credits])


def save_marks(manager):
    with open(MARKS_TXT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for s in manager.students.values():
            for cid, mark in s.marks.items():
                writer.writerow([s.sid, cid, mark])


def compress_data():
    with zipfile.ZipFile(DATA_FILE, "w", zipfile.ZIP_DEFLATED) as z:
        for filename in ALL_FILES:
            if os.path.exists(filename):
                z.write(filename)


def load_data(manager):
    if not os.path.exists(DATA_FILE):
        return
    with zipfile.ZipFile(DATA_FILE) as z:
        z.extractall()

    # Check courses and students first because marks need both
    if os.path.exists(COURSES_TXT):
        with open(COURSES_TXT, newline="", encoding="utf-8") as f:
            for cid, name, credits in csv.reader(f):
                manager.courses[cid] = Course(cid, name, int(credits))

    if os.path.exists(STUDENTS_TXT):
        with open(STUDENTS_TXT, newline="", encoding="utf-8") as f:
            for sid, name, dob in csv.reader(f):
                manager.students[sid] = Student(sid, name, dob)

    if os.path.exists(MARKS_TXT):
        with open(MARKS_TXT, newline="", encoding="utf-8") as f:
            for sid, cid, mark in csv.reader(f):
                if sid in manager.students:
                    manager.students[sid].marks[cid] = float(
                        mark
                    )  # mark is already rounded
