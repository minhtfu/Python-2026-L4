class MarkManager:
    def __init__(self):
        self.students = {}  # sid -> Student
        self.courses = {}   # cid -> Course

    def students_sorted_by_gpa(self):
        """Return list of (student, gpa) sorted by GPA descending."""
        pairs = [(s, s.gpa(self.courses)) for s in self.students.values()]
        pairs.sort(key=lambda pair: pair[1], reverse=True)
        return pairs
