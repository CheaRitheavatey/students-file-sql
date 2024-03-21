import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import mysql.connector

class StudentData:
    def __init__(self, name, major, sex, grade):
        self.name = name
        self.major = major
        self.sex = sex
        self.grade = grade

class StudentAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Data Analyzer")

        self.student_data = []

        # Connect to MySQL database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  
            database="student"
        )

        self.create_widgets()

    def create_widgets(self):
        # Left panel
        left_panel = tk.Frame(self, width=200, height=300)
        left_panel.pack(side="left", padx=10, pady=10)

        tk.Label(left_panel, text="Name:").grid(row=0, column=0, sticky="e")
        self.name_entry = tk.Entry(left_panel)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(left_panel, text="Major:").grid(row=1, column=0, sticky="e")
        self.major_entry = tk.Entry(left_panel)
        self.major_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(left_panel, text="Sex:").grid(row=2, column=0, sticky="e")
        self.sex_entry = tk.Entry(left_panel)
        self.sex_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(left_panel, text="Grade:").grid(row=3, column=0, sticky="e")
        self.grade_entry = tk.Entry(left_panel)
        self.grade_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = tk.Button(left_panel, text="Add Student", command=self.add_student)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Plot graph button below left panel
        self.plot_button = tk.Button(left_panel, text="Plot Graph", command=self.plot_grade_graph)
        self.plot_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Status label for feedback
        self.status_label = tk.Label(left_panel, text="", fg="green")
        self.status_label.grid(row=6, column=0, columnspan=2)

        # Right panel
        right_panel = tk.Frame(self, width=250, height=300)
        right_panel.pack(side="right", padx=10, pady=10)

        self.table = ttk.Treeview(right_panel, columns=("Name", "Major", "Sex", "Grade"), show="headings")
        self.table.heading("Name", text="Name")
        self.table.heading("Major", text="Major")
        self.table.heading("Sex", text="Sex")
        self.table.heading("Grade", text="Grade")
        self.table.pack(fill="both", expand=True)

    def add_student(self):
        try:
            # Add student to the MySQL database
            cursor = self.db.cursor()
            name = self.name_entry.get()
            major = self.major_entry.get()
            sex = self.sex_entry.get()
            grade = self.grade_entry.get()

            if name and major and sex and grade:
                # Insert student data into MySQL database
                sql = "INSERT INTO students (name, major, sex, grade) VALUES (%s, %s, %s, %s)"
                val = (name, major, sex, grade)
                cursor.execute(sql, val)
                self.db.commit()
            
                # Add student data to the table
                self.student_data.append(StudentData(name, major, sex, grade))
                self.table.insert("", "end", values=(name, major, sex, grade))

                # Clear entry fields
                self.name_entry.delete(0, tk.END)
                self.major_entry.delete(0, tk.END)
                self.sex_entry.delete(0, tk.END)
                self.grade_entry.delete(0, tk.END)

                # Update status label
                self.status_label.config(text="Student added successfully!", fg="green")
            
        except (mysql.connector.Error, ValueError) as err:
            self.status_label.config(text=f"Error: {str(err)}", fg="red")

    def plot_grade_graph(self):
        grades = [student.grade for student in self.student_data]
        names = [student.name for student in self.student_data]

        plt.figure(figsize=(8, 6))
        plt.bar(names, grades)
        plt.xlabel('Name')
        plt.ylabel('Grade')
        plt.title('Student Grades')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = StudentAnalyzer()
    app.mainloop()
