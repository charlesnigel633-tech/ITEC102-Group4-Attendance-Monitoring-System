
import json
import os
import tempfile
from datetime import datetime

# -------------------- DATA STORAGE --------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "attendance.json")


def empty_data():
    return {"students": [], "attendance": []}


def load_data():
    """Load student and attendance records from JSON."""
    if not os.path.exists(DATA_FILE):
        return empty_data()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            loaded = json.load(file)

        if not isinstance(loaded, dict):
            raise ValueError("Invalid JSON structure.")

        students = loaded.get("students", [])
        attendance = loaded.get("attendance", [])

        if not isinstance(students, list) or not isinstance(attendance, list):
            raise ValueError("Invalid records format.")

        return {
            "students": students,
            "attendance": attendance
        }

    except (json.JSONDecodeError, OSError, ValueError) as error:
        print("Error reading attendance.json:", error)
        print("Starting with empty records for this session.")
        return empty_data()


data = load_data()


def save_data():
    """Save records safely to JSON."""
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=BASE_DIR,
            delete=False
        ) as temporary:
            json.dump(data, temporary, indent=4)
            temporary.write("\n")
            temp_name = temporary.name

        os.replace(temp_name, DATA_FILE)
        return True

    except OSError as error:
        print("Error saving records:", error)
        return False


# -------------------- HELPER FUNCTIONS --------------------

def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty. Please try again.")


def get_valid_date():
    while True:
        date_text = input("Enter date (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return date_text

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")


def find_student(student_id):
    for student in data["students"]:
        if student["id"].casefold() == student_id.casefold():
            return student

    return None


def find_attendance(student_id, date_text):
    for record in data["attendance"]:
        if (
            record["student_id"].casefold() == student_id.casefold()
            and record["date"] == date_text
        ):
            return record

    return None


# -------------------- STUDENT CRUD --------------------

def add_student():
    print("\n--- ADD STUDENT ---")

    student_id = get_non_empty_input("Student ID: ")

    if find_student(student_id):
        print("Error: Student ID already exists.")
        return

    name = get_non_empty_input("Full name: ")
    course_section = get_non_empty_input("Course and section: ")

    student = {
        "id": student_id,
        "name": name,
        "course_section": course_section
    }

    data["students"].append(student)

    if save_data():
        print("Student added successfully.")


def view_students():
    print("\n--- ALL STUDENTS ---")

    if not data["students"]:
        print("No student records found.")
        return

    print("-" * 70)
    print(f"{'ID':<15}{'NAME':<30}{'COURSE/SECTION':<25}")
    print("-" * 70)

    for student in data["students"]:
        print(
            f"{student['id']:<15}"
            f"{student['name']:<30}"
            f"{student['course_section']:<25}"
        )

    print("-" * 70)


def search_student():
    print("\n--- SEARCH STUDENT ---")

    student_id = get_non_empty_input("Enter student ID: ")
    student = find_student(student_id)

    if student:
        print("\nStudent found:")
        print("Student ID:", student["id"])
        print("Name:", student["name"])
        print("Course/Section:", student["course_section"])

    else:
        print("No student found with that ID.")


def update_student():
    print("\n--- UPDATE STUDENT ---")

    student_id = get_non_empty_input("Enter student ID to update: ")
    student = find_student(student_id)

    if not student:
        print("No student found with that ID.")
        return

    print("Press Enter to keep the current information.")

    new_name = input(
        f"Full name [{student['name']}]: "
    ).strip()

    new_section = input(
        f"Course/Section [{student['course_section']}]: "
    ).strip()

    if new_name:
        student["name"] = new_name

    if new_section:
        student["course_section"] = new_section

    if save_data():
        print("Student record updated successfully.")


def delete_student():
    print("\n--- DELETE STUDENT ---")

    student_id = get_non_empty_input("Enter student ID to delete: ")
    student = find_student(student_id)

    if not student:
        print("No student found with that ID.")
        return

    confirm = input(
        f"Delete {student['name']} and their attendance records? (Y/N): "
    ).strip().casefold()

    if confirm == "y":
        data["students"].remove(student)

        data["attendance"] = [
            record for record in data["attendance"]
            if record["student_id"].casefold() != student_id.casefold()
        ]

        if save_data():
            print("Student and related attendance records deleted.")

    else:
        print("Delete cancelled.")


# -------------------- ATTENDANCE MANAGEMENT --------------------

def record_attendance():
    print("\n--- RECORD ATTENDANCE ---")

    student_id = get_non_empty_input("Enter student ID: ")
    student = find_student(student_id)

    if not student:
        print("No student found. Add the student first.")
        return

    date_text = get_valid_date()

    if find_attendance(student_id, date_text):
        print("Attendance for this student on this date is already recorded.")
        return

    print("\nSelect attendance status:")
    print("[1] Present")
    print("[2] Absent")
    print("[3] Late")

    statuses = {
        "1": "Present",
        "2": "Absent",
        "3": "Late"
    }

    while True:
        choice = input("Enter choice: ").strip()

        if choice in statuses:
            break

        print("Invalid choice. Please select 1, 2, or 3.")

    attendance_record = {
        "student_id": student["id"],
        "date": date_text,
        "status": statuses[choice]
    }

    data["attendance"].append(attendance_record)

    if save_data():
        print(
            f"Attendance saved: {student['name']} - "
            f"{statuses[choice]} on {date_text}"
        )


def view_attendance_records():
    print("\n--- ATTENDANCE RECORDS ---")

    if not data["attendance"]:
        print("No attendance records found.")
        return

    sorted_records = sorted(
        data["attendance"],
        key=lambda record: (
            record["date"],
            record["student_id"]
        )
    )

    print("-" * 75)
    print(
        f"{'DATE':<15}"
        f"{'STUDENT ID':<15}"
        f"{'STUDENT NAME':<30}"
        f"{'STATUS':<15}"
    )
    print("-" * 75)

    for record in sorted_records:
        student = find_student(record["student_id"])

        student_name = student["name"] if student else "Unknown"

        print(
            f"{record['date']:<15}"
            f"{record['student_id']:<15}"
            f"{student_name:<30}"
            f"{record['status']:<15}"
        )

    print("-" * 75)


def update_attendance():
    print("\n--- UPDATE ATTENDANCE ---")

    student_id = get_non_empty_input("Enter student ID: ")

    if not find_student(student_id):
        print("No student found with that ID.")
        return

    date_text = get_valid_date()
    record = find_attendance(student_id, date_text)

    if not record:
        print("No attendance record found.")
        return

    print("Current status:", record["status"])

    print("[1] Present")
    print("[2] Absent")
    print("[3] Late")

    statuses = {
        "1": "Present",
        "2": "Absent",
        "3": "Late"
    }

    while True:
        choice = input("Select new status: ").strip()

        if choice in statuses:
            break

        print("Invalid choice. Select 1, 2, or 3.")

    record["status"] = statuses[choice]

    if save_data():
        print("Attendance record updated successfully.")


def delete_attendance():
    print("\n--- DELETE ATTENDANCE ---")

    student_id = get_non_empty_input("Enter student ID: ")

    if not find_student(student_id):
        print("No student found with that ID.")
        return

    date_text = get_valid_date()
    record = find_attendance(student_id, date_text)

    if not record:
        print("No attendance record found.")
        return

    confirm = input(
        "Delete this attendance record? (Y/N): "
    ).strip().casefold()

    if confirm == "y":
        data["attendance"].remove(record)

        if save_data():
            print("Attendance record deleted successfully.")

    else:
        print("Delete cancelled.")


# -------------------- ATTENDANCE COMPUTATION --------------------

def get_student_attendance_stats(student_id):
    records = [
        record for record in data["attendance"]
        if record["student_id"].casefold() == student_id.casefold()
    ]

    present = sum(
        1 for record in records
        if record["status"] == "Present"
    )

    late = sum(
        1 for record in records
        if record["status"] == "Late"
    )

    absent = sum(
        1 for record in records
        if record["status"] == "Absent"
    )

    total = len(records)

    percentage = (
        ((present + late) / total) * 100
        if total > 0 else None
    )

    return total, present, late, absent, percentage


def check_attendance_percentage():
    print("\n--- ATTENDANCE PERCENTAGE ---")

    student_id = get_non_empty_input("Enter student ID: ")
    student = find_student(student_id)

    if not student:
        print("No student found with that ID.")
        return

    total, present, late, absent, percentage = (
        get_student_attendance_stats(student_id)
    )

    if total == 0:
        print("This student has no attendance records yet.")
        return

    print("\nStudent:", student["name"])
    print("Total recorded days:", total)
    print("Present:", present)
    print("Late:", late)
    print("Absent:", absent)
    print(f"Attendance percentage: {percentage:.2f}%")
    print("Note: Late is counted as attended.")


def generate_attendance_report():
    print("\n--- ATTENDANCE SUMMARY REPORT ---")

    if not data["students"]:
        print("No student records found.")
        return

    print("-" * 90)

    print(
        f"{'ID':<12}"
        f"{'NAME':<25}"
        f"{'PRESENT':<10}"
        f"{'LATE':<8}"
        f"{'ABSENT':<9}"
        f"{'ATTENDANCE %':<15}"
    )

    print("-" * 90)

    for student in data["students"]:

        total, present, late, absent, percentage = (
            get_student_attendance_stats(student["id"])
        )

        percentage_text = (
            f"{percentage:.2f}%"
            if percentage is not None
            else "No records"
        )

        print(
            f"{student['id']:<12}"
            f"{student['name'][:24]:<25}"
            f"{present:<10}"
            f"{late:<8}"
            f"{absent:<9}"
            f"{percentage_text:<15}"
        )

    print("-" * 90)
    print("Note: Late is counted as attended in the percentage.")


# -------------------- MAIN DASHBOARD --------------------

def main():

    while True:

        print("\n" + "=" * 52)
        print("       STUDENT ATTENDANCE MONITORING SYSTEM")
        print("=" * 52)

        print("\n                 MAIN DASHBOARD")

        print("\nSTUDENT MANAGEMENT")
        print("[1] Add Student")
        print("[2] View All Students")
        print("[3] Search Student")
        print("[4] Update Student")
        print("[5] Delete Student")

        print("\nATTENDANCE MANAGEMENT")
        print("[6] Record Attendance")
        print("[7] View Attendance Records")
        print("[8] Update Attendance")
        print("[9] Delete Attendance")
        print("[10] Check Attendance Percentage")
        print("[11] Generate Attendance Summary Report")

        print("\n[0] Exit")
        print("=" * 52)

        choice = input("Enter your choice: ").strip()

        actions = {
            "1": add_student,
            "2": view_students,
            "3": search_student,
            "4": update_student,
            "5": delete_student,
            "6": record_attendance,
            "7": view_attendance_records,
            "8": update_attendance,
            "9": delete_attendance,
            "10": check_attendance_percentage,
            "11": generate_attendance_report
        }

        if choice == "0":
            print(
                "\nThank you for using the "
                "Student Attendance Monitoring System!"
            )
            break

        elif choice in actions:
            actions[choice]()

        else:
            print("Invalid choice. Please select a number from 0 to 11.")


if __name__ == "__main__":
    main()
