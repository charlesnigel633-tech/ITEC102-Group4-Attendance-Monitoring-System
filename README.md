# Student Attendance Monitoring System

**Course:** ITEC 102  
**Section:** BSCS-1B  
**Group:** 4  
**Instructor:** Mr. Edison Templo

## Project Description

The Student Attendance Monitoring System is a Python-based console application designed to manage student information and daily attendance records. It allows users to add, view, search, update, and delete student records. It also provides attendance recording, attendance percentage calculation, and attendance summary reporting.

The system uses JSON file handling to store student and attendance records so that information remains available even after the program is closed.

## Features

### Student Management
- Add Student
- View All Students
- Search Student
- Update Student
- Delete Student

### Attendance Management
- Record Attendance (Present, Absent, or Late)
- View Attendance Records
- Update Attendance
- Delete Attendance
- Check Attendance Percentage
- Generate Attendance Summary Report

### Other Features
- Prevents duplicate student IDs.
- Prevents duplicate attendance records for the same student and date.
- Validates user inputs and attendance dates.
- Saves records using JSON file storage.
- Maintains records after restarting the program.

## Technologies Used

- Python
- JSON
- Visual Studio Code

## Project Files

| File | Description |
|---|---|
| `main.py` | Main Python source code |
| `attendance.json` | Stores student and attendance records |
| `README.md` | Project documentation and instructions |
| `ITEC102_Group4_Project_Documentation_Final.pdf` | Project documentation |
| `Group4_Project_Presentation.mp4` | Project demonstration video |

## How to Run the Program

1. Install Python on your computer.
2. Download or clone this repository.
3. Open the project folder in Visual Studio Code.
4. Make sure `main.py` and `attendance.json` are in the same folder.
5. Open the VS Code terminal.
6. Run the following command:

```bash
python main.py
```

7. Use the numbered menu to navigate through the system.

## Group Members

1. Dela Cueva, Princess Hannah B.
2. De Guzman, Charles Nigel E.
3. Evangelista, Michael M.
4. Bandian, Althea D.
5. Rodio, Justine T.

---

**ITEC 102 – Student Attendance Monitoring System**  
Developed by Group 4, BSCS-1B.
