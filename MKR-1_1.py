import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt

class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade
        self.attendance = []
        self.grades = []

    def __str__(self):
        return f"{self.student_id}: {self.name} (Клас {self.grade})"

class AttendanceRecord:
    def __init__(self, date, present):
        self.date = date
        self.present = present

    def __str__(self):
        return f"{self.date}: {'Присутній' if self.present else 'Відсутній'}"

class GradeRecord:
    def __init__(self, subject, grade):
        self.subject = subject
        self.grade = grade

    def __str__(self):
        return f"{self.subject}: {self.grade}"

class SchoolDiary:
    def __init__(self):
        self.students = {}

    def add_student(self, student_id, name, grade):
        if student_id in self.students:
            return f"Студент з ID {student_id} вже існує."
        else:
            self.students[student_id] = Student(student_id, name, grade)
            return f"Студента '{name}' успішно додано."

    def record_attendance(self, student_id, date, present):
        if student_id not in self.students:
            return f"Студента з ID {student_id} не знайдено."
        else:
            self.students[student_id].attendance.append(AttendanceRecord(date, present))
            return f"Відвідування для студента '{self.students[student_id].name}' успішно записано."

    def record_grade(self, student_id, subject, grade):
        if student_id not in self.students:
            return f"Студента з ID {student_id} не знайдено."
        else:
            self.students[student_id].grades.append(GradeRecord(subject, grade))
            return f"Оцінку для студента '{self.students[student_id].name}' успішно записано."

    def list_students(self):
        return list(self.students.values())

    def get_attendance(self, student_id):
        if student_id not in self.students:
            return f"Студента з ID {student_id} не знайдено."
        else:
            return self.students[student_id].attendance

    def get_grades(self, student_id):
        if student_id not in self.students:
            return f"Студента з ID {student_id} не знайдено."
        else:
            return self.students[student_id].grades


class SchoolDiaryApp(tk.Tk):
    def __init__(self, diary):
        super().__init__()
        self.diary = diary
        self.title("Шкільний щоденник")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.create_student_frame()
        self.create_attendance_frame()
        self.create_grades_frame()
        self.create_list_frame()

    def create_student_frame(self):
        self.student_frame = self.create_label_frame("Студенти", 0)
        self.student_id_entry = self.create_label_and_entry(self.student_frame, "ID студента:", 0)
        self.student_name_entry = self.create_label_and_entry(self.student_frame, "Ім'я:", 1)
        self.student_grade_entry = self.create_label_and_entry(self.student_frame, "Клас:", 2)
        self.create_button(self.student_frame, "Додати студента", self.add_student, 3)

    def create_attendance_frame(self):
        self.attendance_frame = self.create_label_frame("Відвідуваність", 1)
        self.attendance_student_id_entry = self.create_label_and_entry(self.attendance_frame, "ID студента:", 0)
        self.attendance_date_entry = self.create_label_and_entry(self.attendance_frame, "Дата (рррр-мм-дд):", 1)
        self.attendance_present_var = tk.IntVar()
        tk.Label(self.attendance_frame, text="Присутній:").grid(row=2, column=0)
        tk.Checkbutton(self.attendance_frame, variable=self.attendance_present_var).grid(row=2, column=1)
        self.create_button(self.attendance_frame, "Записати відвідуваність", self.record_attendance, 3)

    def create_grades_frame(self):
        self.grades_frame = self.create_label_frame("Оцінки", 2)
        self.grades_student_id_entry = self.create_label_and_entry(self.grades_frame, "ID студента:", 0)
        self.grades_subject_entry = self.create_label_and_entry(self.grades_frame, "Предмет:", 1)
        self.grades_grade_entry = self.create_label_and_entry(self.grades_frame, "Оцінка:", 2)
        self.create_button(self.grades_frame, "Записати оцінку", self.record_grade, 3)

    def create_list_frame(self):
        self.list_frame = self.create_label_frame("Списки", 3)
        self.create_button(self.list_frame, "Список студентів", self.show_students, 0, 0)
        self.create_button(self.list_frame, "Список відвідуваності", self.show_attendance, 0, 1)
        self.create_button(self.list_frame, "Список оцінок", self.show_grades, 0, 2)
        self.create_button(self.list_frame, "Візуалізація відвідуваності", self.visualize_attendance, 0, 3)
        self.create_button(self.list_frame, "Візуалізація оцінок", self.visualize_grades, 0, 4)
        self.list_text = tk.Text(self.list_frame, height=10)
        self.list_text.grid(row=1, column=0, columnspan=5)

    def create_label_frame(self, text, row):
        frame = tk.LabelFrame(self, text=text)
        frame.pack(fill="both", expand="yes", padx=10, pady=10)
        return frame

    def create_label_and_entry(self, frame, label_text, row):
        tk.Label(frame, text=label_text).grid(row=row, column=0)
        entry = tk.Entry(frame)
        entry.grid(row=row, column=1)
        return entry

    def create_button(self, frame, text, command, row, column=0):
        tk.Button(frame, text=text, command=command).grid(row=row, column=column, columnspan=2)

    def add_student(self):
        student_id = int(self.student_id_entry.get())
        name = self.student_name_entry.get()
        grade = self.student_grade_entry.get()
        message = self.diary.add_student(student_id, name, grade)
        messagebox.showinfo("Інформація", message)
        self.clear_entries()

    def record_attendance(self):
        student_id = int(self.attendance_student_id_entry.get())
        date = self.attendance_date_entry.get()
        present = bool(self.attendance_present_var.get())
        message = self.diary.record_attendance(student_id, date, present)
        messagebox.showinfo("Інформація", message)
        self.clear_entries()

    def record_grade(self):
        student_id = int(self.grades_student_id_entry.get())
        subject = self.grades_subject_entry.get()
        grade = self.grades_grade_entry.get()
        message = self.diary.record_grade(student_id, subject, grade)
        messagebox.showinfo("Інформація", message)
        self.clear_entries()

    def show_students(self):
        self.display_list(self.diary.list_students())

    def show_attendance(self):
        self.display_records(self.diary.get_attendance, self.attendance_student_id_entry.get())

    def show_grades(self):
        self.display_records(self.diary.get_grades, self.grades_student_id_entry.get())

    def display_list(self, items):
        self.list_text.delete(1.0, tk.END)
        for item in items:
            self.list_text.insert(tk.END, str(item) + "\n")

    def display_records(self, get_records_func, student_id):
        try:
            student_id = int(student_id)
            records = get_records_func(student_id)
            if isinstance(records, str):  # error message
                messagebox.showinfo("Інформація", records)
            else:
                self.display_list(records)
        except ValueError:
            messagebox.showerror("Помилка", "ID студента повинен бути числом.")

    def visualize_attendance(self):
        self.visualize(self.diary.get_attendance, self.attendance_student_id_entry.get(), "Відвідуваність", ["Відсутній", "Присутній"])

    def visualize_grades(self):
        self.visualize(self.diary.get_grades, self.grades_student_id_entry.get(), "Оцінки", range(
