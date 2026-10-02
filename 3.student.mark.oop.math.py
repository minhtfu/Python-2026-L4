import math
import curses
import numpy as np


class Course:
    def __init__(self, cid, name, credits):
        self.cid = cid
        self.name = name
        self.credits = credits

    def __str__(self):
        return f"{self.cid}: {self.name} ({self.credits} credits)"


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
        """Weighted average GPA (4.0 scale) using numpy, weighted by credits."""
        if not self.marks:
            return 0.0
        gpa_points = []
        weights = []
        for cid, mark in self.marks.items():
            course = courses.get(cid)
            if course is None:
                continue
            gpa_points.append(mark)
            weights.append(course.credits)
        if not weights or sum(weights) == 0:
            return 0.0
        gpa_points = np.array(gpa_points, dtype=float)
        weights = np.array(weights, dtype=float)
        return float(np.sum(gpa_points * weights) / np.sum(weights))

    def __str__(self):
        return f"{self.sid}: {self.name}, DoB: {self.dob}"


class MarkManager:
    def __init__(self):
        self.students = {}  # sid -> Student
        self.courses = {}  # cid -> Course

    def input_students(self):
        n = int(input("Number of students: "))
        for _ in range(n):
            sid = input("Student ID: ")
            name = input("Name: ")
            dob = input("Date of birth: ")
            self.students[sid] = Student(sid, name, dob)

    def input_courses(self):
        n = int(input("Number of courses: "))
        for _ in range(n):
            cid = input("Course ID: ")
            name = input("Course name: ")
            credits = int(input("Credits: "))
            self.courses[cid] = Course(cid, name, credits)

    def input_marks(self):
        if not self.courses:
            print("No courses yet.")
            return
        self.list_courses()
        cid = input("Select course ID: ")
        if cid not in self.courses:
            print("Invalid course.")
            return
        for student in self.students.values():
            mark = float(input(f"Mark for {student.name} ({student.sid}): "))
            student.set_mark(cid, mark)

    def list_courses(self):
        print("--- Courses ---")
        for course in self.courses.values():
            print(course)

    def list_students(self):
        print("--- Students ---")
        for student in self.students.values():
            print(student)

    def show_marks_for_course(self):
        self.list_courses()
        cid = input("Select course ID: ")
        if cid not in self.courses:
            print("Invalid course.")
            return
        print(f"--- Marks for {self.courses[cid].name} ---")
        for student in self.students.values():
            mark = student.get_mark(cid)
            mark_display = mark if mark is not None else "N/A"
            print(f"{student.sid} {student.name}: {mark_display}")

    def students_sorted_by_gpa(self):
        """Return list of (student, gpa) sorted by GPA descending."""
        pairs = [(s, s.gpa(self.courses)) for s in self.students.values()]
        pairs.sort(key=lambda pair: pair[1], reverse=True)
        return pairs

    def menu(self):
        while True:
            print("""
1. Input students
2. Input courses
3. Input marks for a course
4. List courses
5. List students
6. Show marks for a course
7. Show GPA ranking (sorted descending)
0. Exit
""")
            choice = input("Choose: ")
            if choice == "1":
                self.input_students()
            elif choice == "2":
                self.input_courses()
            elif choice == "3":
                self.input_marks()
            elif choice == "4":
                self.list_courses()
            elif choice == "5":
                self.list_students()
            elif choice == "6":
                self.show_marks_for_course()
            elif choice == "7":
                for student, gpa in self.students_sorted_by_gpa():
                    print(f"{student.sid} {student.name}: GPA {gpa:.2f}")
            elif choice == "0":
                break
            else:
                print("Invalid choice.")


def curses_prompt(stdscr, y, prompt):
    """Read a line of text input at row y, echoing what's typed."""
    curses.echo()
    stdscr.addstr(y, 0, prompt)
    stdscr.clrtoeol()
    stdscr.refresh()
    text = stdscr.getstr(y, len(prompt)).decode("utf-8")
    curses.noecho()
    return text


def curses_pause(stdscr, y):
    stdscr.addstr(y, 0, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getch()


def curses_menu(stdscr, manager):
    curses.curs_set(1)
    options = [
        "Input students",
        "Input courses",
        "Input marks for a course",
        "List courses",
        "List students",
        "Show marks for a course",
        "Show GPA ranking (sorted descending)",
        "Exit",
    ]
    current = 0

    while True:
        stdscr.clear()
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(0, 0, " Student Mark Management ".center(curses.COLS - 1, "="))
        stdscr.attroff(curses.color_pair(1))

        for i, opt in enumerate(options):
            marker = "> " if i == current else "  "
            if i == current:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(2 + i, 2, f"{marker}{opt}")
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(2 + i, 2, f"{marker}{opt}")

        stdscr.addstr(
            2 + len(options) + 2, 0, "Use UP/DOWN to move, ENTER to select, q to quit."
        )
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            current = (current - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(options)
        elif key in (curses.KEY_ENTER, 10, 13):
            handled = handle_choice(stdscr, manager, current, len(options))
            if not handled:
                break
        elif key in (ord("q"), ord("Q")):
            break


def handle_choice(stdscr, manager, index, nrows):
    stdscr.clear()
    base_y = 0

    if index == 0:  # input students
        n = int(curses_prompt(stdscr, base_y, "Number of students: "))
        for i in range(n):
            row = base_y + 1 + i * 3
            sid = curses_prompt(stdscr, row, f"[{i + 1}] Student ID: ")
            name = curses_prompt(stdscr, row + 1, f"[{i + 1}] Name: ")
            dob = curses_prompt(stdscr, row + 2, f"[{i + 1}] DoB: ")
            manager.students[sid] = Student(sid, name, dob)

    elif index == 1:  # input courses
        n = int(curses_prompt(stdscr, base_y, "Number of courses: "))
        for i in range(n):
            row = base_y + 1 + i * 3
            cid = curses_prompt(stdscr, row, f"[{i + 1}] Course ID: ")
            name = curses_prompt(stdscr, row + 1, f"[{i + 1}] Name: ")
            credits = int(curses_prompt(stdscr, row + 2, f"[{i + 1}] Credits: "))
            manager.courses[cid] = Course(cid, name, credits)

    elif index == 2:  # input marks
        if not manager.courses:
            stdscr.addstr(base_y, 0, "No courses yet.")
            curses_pause(stdscr, base_y + 1)
            return True
        y = base_y
        stdscr.addstr(y, 0, "--- Courses ---")
        y += 1
        for course in manager.courses.values():
            stdscr.addstr(y, 0, str(course))
            y += 1
        cid = curses_prompt(stdscr, y + 1, "Select course ID: ")
        if cid not in manager.courses:
            stdscr.addstr(y + 3, 0, "Invalid course.")
            curses_pause(stdscr, y + 4)
            return True
        y += 3
        for student in manager.students.values():
            mark = float(
                curses_prompt(stdscr, y, f"Mark for {student.name} ({student.sid}): ")
            )
            student.set_mark(cid, mark)
            y += 1

    elif index == 3:  # list courses
        y = base_y
        stdscr.addstr(y, 0, "--- Courses ---")
        y += 1
        for course in manager.courses.values():
            stdscr.addstr(y, 0, str(course))
            y += 1
        curses_pause(stdscr, y + 1)

    elif index == 4:  # list students
        y = base_y
        stdscr.addstr(y, 0, "--- Students ---")
        y += 1
        for student in manager.students.values():
            stdscr.addstr(y, 0, str(student))
            y += 1
        curses_pause(stdscr, y + 1)

    elif index == 5:  # show marks for course
        y = base_y
        stdscr.addstr(y, 0, "--- Courses ---")
        y += 1
        for course in manager.courses.values():
            stdscr.addstr(y, 0, str(course))
            y += 1
        cid = curses_prompt(stdscr, y + 1, "Select course ID: ")
        if cid not in manager.courses:
            stdscr.addstr(y + 3, 0, "Invalid course.")
            curses_pause(stdscr, y + 4)
            return True
        y += 3
        stdscr.addstr(y, 0, f"--- Marks for {manager.courses[cid].name} ---")
        y += 1
        for student in manager.students.values():
            mark = student.get_mark(cid)
            mark_display = mark if mark is not None else "N/A"
            stdscr.addstr(y, 0, f"{student.sid} {student.name}: {mark_display}")
            y += 1
        curses_pause(stdscr, y + 1)

    elif index == 6:  # GPA ranking
        y = base_y
        stdscr.addstr(y, 0, "--- GPA Ranking (descending) ---")
        y += 1
        for student, gpa in manager.students_sorted_by_gpa():
            stdscr.addstr(y, 0, f"{student.sid} {student.name}: GPA {gpa:.2f}")
            y += 1
        curses_pause(stdscr, y + 1)

    elif index == nrows - 1:  # exit
        return False

    return True


def run_curses(manager):
    def wrapped(stdscr):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses_menu(stdscr, manager)

    curses.wrapper(wrapped)


if __name__ == "__main__":
    manager = MarkManager()
    try:
        run_curses(manager)
    except curses.error:
        print("curses UI unavailable, falling back to console menu.")
        manager.menu()
