students = {}
courses = {}


def input_students():
    n = int(input("Enter the number of students: "))

    for _ in range(n):
        sid = input("Enter student ID: ")
        name = input("Enter student name: ")
        dob = input("Enter student DOB: ")

        students[sid] = {"name": name, "dob": dob, "marks": {}}


def input_courses():
    n = int(input("Enter the number of courses: "))

    for _ in range(n):
        cid = input("Enter course ID: ")
        name = input("Enter course name: ")

        courses[cid] = {"name": name}


def input_marks():
    if not courses:
        print("No courses yet")
        return

    list_courses()

    cid = input("Enter course ID: ")

    if cid not in courses:
        print("Course doesn't exist")
        return

    for sid, info in students.items():
        mark = float(input(f"Enter mark for {info['name']} ({sid}): "))

        info["marks"][cid] = mark


def show_marks_for_course():
    if not courses:
        print("No courses yet")
        return

    list_courses()

    cid = input("Enter course ID: ")

    if cid not in courses:
        print("Course doesn't exist")
        return

    print(f"--- Marks for {courses[cid]['name']} ---")
    for sid, info in students.items():
        mark = info["marks"].get(cid, "N/A")

        print(f"{sid} - {info['name']}: {mark}")


def list_courses():
    print("--- Courses ---")

    for cid, info in courses.items():
        print(f"{cid}: {info['name']}")


def list_students():
    print("--- Students ---")

    for sid, info in students.items():
        print(f"{sid}: {info['name']}, DoB: {info['dob']}")

def main():
    while True:
        print("""
        1. Input students
        2. Input courses
        3. Input marks for a course
        4. List courses
        5. List students
        6. Show marks for course
        0. Exit
        """)

        choice = int(input("Enter a choice: "))

        if choice == 1:
            input_students()
        elif choice == 2:
            input_courses()
        elif choice == 3:
            input_marks()
        elif choice == 4:
            list_courses()
        elif choice == 5:
            list_students()
        elif choice == 6:
            show_marks_for_course()
        elif choice == 0:
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
