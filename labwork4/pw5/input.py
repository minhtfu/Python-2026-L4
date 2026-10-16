import curses
from domains import Course, Student
from storage import save_students, save_courses, save_marks


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


def input_students(stdscr, manager, base_y=0):
    n = int(curses_prompt(stdscr, base_y, "Number of students: "))
    for i in range(n):
        row = base_y + 1 + i * 3
        sid = curses_prompt(stdscr, row, f"[{i + 1}] Student ID: ")
        name = curses_prompt(stdscr, row + 1, f"[{i + 1}] Name: ")
        dob = curses_prompt(stdscr, row + 2, f"[{i + 1}] DoB: ")
        manager.students[sid] = Student(sid, name, dob)

    save_students(manager)


def input_courses(stdscr, manager, base_y=0):
    n = int(curses_prompt(stdscr, base_y, "Number of courses: "))
    for i in range(n):
        row = base_y + 1 + i * 3
        cid = curses_prompt(stdscr, row, f"[{i + 1}] Course ID: ")
        name = curses_prompt(stdscr, row + 1, f"[{i + 1}] Name: ")
        credits = int(curses_prompt(stdscr, row + 2, f"[{i + 1}] Credits: "))
        manager.courses[cid] = Course(cid, name, credits)

    save_courses(manager)


def input_marks(stdscr, manager, base_y=0):
    if not manager.courses:
        stdscr.addstr(base_y, 0, "No courses yet.")
        curses_pause(stdscr, base_y + 1)
        return
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
        return
    y += 3
    for student in manager.students.values():
        mark = float(
            curses_prompt(stdscr, y, f"Mark for {student.name} ({student.sid}): ")
        )
        student.set_mark(cid, mark)
        y += 1

    save_marks(manager)
