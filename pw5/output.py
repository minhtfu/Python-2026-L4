import curses
from input import (
    curses_prompt,
    curses_pause,
    input_students,
    input_courses,
    input_marks,
)


def show_courses(stdscr, manager, base_y=0):
    y = base_y
    stdscr.addstr(y, 0, "--- Courses ---")
    y += 1
    for course in manager.courses.values():
        stdscr.addstr(y, 0, str(course))
        y += 1
    curses_pause(stdscr, y + 1)


def show_students(stdscr, manager, base_y=0):
    y = base_y
    stdscr.addstr(y, 0, "--- Students ---")
    y += 1
    for student in manager.students.values():
        stdscr.addstr(y, 0, str(student))
        y += 1
    curses_pause(stdscr, y + 1)


def show_marks_for_course(stdscr, manager, base_y=0):
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
    stdscr.addstr(y, 0, f"--- Marks for {manager.courses[cid].name} ---")
    y += 1
    for student in manager.students.values():
        mark = student.get_mark(cid)
        mark_display = mark if mark is not None else "N/A"
        stdscr.addstr(y, 0, f"{student.sid} {student.name}: {mark_display}")
        y += 1
    curses_pause(stdscr, y + 1)


def show_gpa_ranking(stdscr, manager, base_y=0):
    y = base_y
    stdscr.addstr(y, 0, "--- GPA Ranking (descending) ---")
    y += 1
    for student, gpa in manager.students_sorted_by_gpa():
        stdscr.addstr(y, 0, f"{student.sid} {student.name}: GPA {gpa:.2f}")
        y += 1
    curses_pause(stdscr, y + 1)


def handle_choice(stdscr, manager, index, nrows):
    stdscr.clear()

    if index == 0:
        input_students(stdscr, manager)
    elif index == 1:
        input_courses(stdscr, manager)
    elif index == 2:
        input_marks(stdscr, manager)
    elif index == 3:
        show_courses(stdscr, manager)
    elif index == 4:
        show_students(stdscr, manager)
    elif index == 5:
        show_marks_for_course(stdscr, manager)
    elif index == 6:
        show_gpa_ranking(stdscr, manager)
    elif index == nrows - 1:  # exit
        return False

    return True


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
            if not handle_choice(stdscr, manager, current, len(options)):
                break
        elif key in (ord("q"), ord("Q")):
            break


def run_curses(manager):
    def wrapped(stdscr):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses_menu(stdscr, manager)

    curses.wrapper(wrapped)
