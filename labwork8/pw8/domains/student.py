import math
import numpy as np


class Student:
    def __init__(self, sid, name, dob):
        self.sid = sid
        self.name = name
        self.dob = dob
        self.marks = {}  # course_id -> mark

    def set_mark(self, cid, mark):
        rounded = math.floor(mark * 10) / 10
        self.marks[cid] = rounded

    def get_mark(self, cid):
        return self.marks.get(cid, None)

    def gpa(self, courses):
        if not self.marks:
            return 0.0

        points = []
        weights = []

        for cid, mark in self.marks.items():
            course = courses.get(cid)
            if course is None:
                continue
            points.append(mark)
            weights.append(course.credits)

        if not weights or sum(weights) == 0:
            return 0.0

        points = np.array(points, dtype=float)
        weights = np.array(weights, dtype=float)

        return float(np.sum(points * weights) / np.sum(weights))

    def __str__(self):
        return f"{self.sid}: {self.name}, DoB: {self.dob}"
