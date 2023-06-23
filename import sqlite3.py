import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk

# Database Connection
conn = sqlite3.connect('management_system.db')
cursor = conn.cursor()

# Create Tables
cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                    course_code INTEGER PRIMARY KEY,
                    course_name TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY,
                    name TEXT,
                    gender TEXT,
                    year_level TEXT,
                    course_code INTEGER,
                    FOREIGN KEY (course_code) REFERENCES courses(course_code))''')

# Create GUI Window
window = tk.Tk()
window.title("Student and Course Management System")
window.geometry("1375x1000")
window.configure(bg="lightpink")

# Create a style object
style = ttk.Style()
style.configure("Custom.TFrame", background="skyblue")

# Create Notebook
notebook = ttk.Notebook(window)
notebook.pack(pady=10)

# Students Frame
students_frame = ttk.Frame(notebook, width=1000, height=900, style="Custom.TFrame")
students_frame.pack(fill='both', expand=True)

# Course Management Frame
course_frame = ttk.Frame(notebook, width=1000, height=900, style="Custom.TFrame")
course_frame.pack(fill='both', expand=True)

notebook.add(students_frame, text="Student Management")
notebook.add(course_frame, text="Course Management")

# Customize the style of the tab headers
style.configure("TNotebook.Tab", font=("Courier New", 12, "bold"))
style.configure("TNotebook.Tab", foreground="black")

# Function to populate the listbox
def populate_listbox():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    for row in rows:
        listbox.insert(tk.END, row)

# Function to add a student
def add_student():
    if name_entry.get() and gender_var.get() and year_var.get() and course_code_var.get():
        cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)",
                       (student_id_entry.get(), name_entry.get(), gender_var.get(), year_var.get(), course_code_var.get()))
        conn.commit()
        populate_listbox()
        clear_entries()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

# Function to read student details
def read_student():
    selected_student = listbox.curselection()
    if selected_student:
        student_details = listbox.get(selected_student)
        student_id_entry.delete(0, tk.END)
        student_id_entry.insert(tk.END, student_details[0])
        name_entry.delete(0, tk.END)
        name_entry.insert(tk.END, student_details[1])
        gender_var.set(student_details[2])
        year_var.set(student_details[3])
        course_code_var.set(student_details[4])
    else:
        messagebox.showerror("Error", "No student selected.")

# Function to update student details
def update_student():
    selected_student = listbox.curselection()
    if selected_student:
        if name_entry.get() and gender_var.get() and year_var.get() and course_code_var.get():
            student_details = listbox.get(selected_student)
            cursor.execute("UPDATE students SET name=?, gender=?, year_level=?, course_code=? WHERE student_id=?",
                           (name_entry.get(), gender_var.get(), year_var.get(), course_code_var.get(), student_details[0]))
            conn.commit()
            populate_listbox()
            clear_entries()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    else:
        messagebox.showerror("Error", "No student selected.")

# Function to search for a student
def search_student():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM students WHERE student_id=?", (search_entry.get(),))
    rows = cursor.fetchall()
    for row in rows:
        listbox.insert(tk.END, row)

# Function to delete a student
def delete_student():
    selected_student = listbox.curselection()
    if selected_student:
        student_details = listbox.get(selected_student)
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this student?")
        if confirm:
            cursor.execute("DELETE FROM students WHERE student_id=?", (student_details[0],))
            conn.commit()
            populate_listbox()
            clear_entries()
    else:
        messagebox.showerror("Error", "No student selected.")

# Function to clear the entry fields
def clear_entries():
    student_id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    gender_var.set("")
    year_var.set("")
    course_code_var.set("")


# Function to populate course codes
def populate_course_codes():
    cursor.execute("SELECT course_code FROM courses")
    rows = cursor.fetchall()
    course_code_option['menu'].delete(0, tk.END)
    for row in rows:
        course_code_option['menu'].add_command(label=row[0], command=tk._setit(course_code_var, row[0]), font=custom_font)

# Function to populate gender options
def populate_gender_options():
    gender_option['menu'].delete(0, tk.END)
    for gender in ["Male", "Female"]:
        gender_option['menu'].add_command(label=gender, command=tk._setit(gender_var, gender), font=custom_font)

# Function to populate year level options
def populate_year_options():
    year_option['menu'].delete(0, tk.END)
    for year in ["1st Year", "2nd Year", "3rd Year", "4th Year"]:
        year_option['menu'].add_command(label=year, command=tk._setit(year_var, year), font=custom_font)

# Function to populate course management listbox
def populate_course_listbox():
    course_listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()
    for row in rows:
        course_listbox.insert(tk.END, row)

# Function to add a course
def add_course():
    if course_code_entry.get() and course_name_entry.get():
        cursor.execute("INSERT INTO courses VALUES (?, ?)", (course_code_entry.get(), course_name_entry.get()))
        conn.commit()
        populate_course_listbox()
        clear_course_entries()
        populate_course_codes()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")
        
# Function to read course details
def read_course():
    selected_course = course_listbox.curselection()
    if selected_course:
        course_details = course_listbox.get(selected_course)
        course_code_entry.delete(0, tk.END)
        course_code_entry.insert(tk.END, course_details[0])
        course_name_entry.delete(0, tk.END)
        course_name_entry.insert(tk.END, course_details[1])
    else:
        messagebox.showerror("Error", "No course selected.")

# Function to update course details
def update_course():
    selected_course = course_listbox.curselection()
    if selected_course:
        if course_code_entry.get() and course_name_entry.get():
            course_details = course_listbox.get(selected_course)
            cursor.execute("UPDATE courses SET course_name=? WHERE course_code=?",
                           (course_name_entry.get(), course_details[0]))
            conn.commit()
            populate_course_listbox()
            clear_course_entries()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    else:
        messagebox.showerror("Error", "No course selected.")

# Function to delete a course
def delete_course():
    selected_course = course_listbox.curselection()
    if selected_course:
        course_details = course_listbox.get(selected_course)
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this course?")
        if confirm:
            cursor.execute("DELETE FROM courses WHERE course_code=?", (course_details[0],))
            conn.commit()
            populate_course_listbox()
            clear_course_entries()
    else:
        messagebox.showerror("Error", "No course selected.")

# Function to clear the course entry fields
def clear_course_entries():
    course_code_entry.delete(0, tk.END)
    course_name_entry.delete(0, tk.END)

# Function to search for a course
def search_course():
    course_listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM courses WHERE course_code=?", (search_course_entry.get(),))
    rows = cursor.fetchall()
    for row in rows:
        course_listbox.insert(tk.END, row)

# Define a custom font
custom_font=("Courier New", 12, "bold") 

# Create Student Management GUI
student_id_label = tk.Label(students_frame, text="Student ID:", bg="skyblue", font=custom_font)
student_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")
student_id_entry = tk.Entry(students_frame, font=custom_font)
student_id_entry.grid(row=0, column=1, padx=5, pady=5)

name_label = tk.Label(students_frame, text="Name:", bg="skyblue", font=custom_font)
name_label.grid(row=1, column=0, padx=5, pady=5, sticky="W")
name_entry = tk.Entry(students_frame, font=custom_font)
name_entry.grid(row=1, column=1, padx=5, pady=5)

gender_label = tk.Label(students_frame, text="Gender:", bg="skyblue", font=custom_font)
gender_label.grid(row=2, column=0, padx=5, pady=5, sticky="W")
gender_var = tk.StringVar()
gender_option = ttk.OptionMenu(students_frame, gender_var, "", style="Custom.TMenubutton")
gender_option["menu"].config(bg="skyblue", font=custom_font)
gender_option.grid(row=2, column=1, padx=5, pady=5)
populate_gender_options()

year_label = tk.Label(students_frame, text="Year Level:", bg="skyblue", font=custom_font)
year_label.grid(row=3, column=0, padx=5, pady=5, sticky="W")
year_var = tk.StringVar()
year_option = ttk.OptionMenu(students_frame, year_var, "", style="Custom.TMenubutton")
year_option["menu"].config(bg="skyblue", font=custom_font)
year_option.grid(row=3, column=1, padx=5, pady=5)
populate_year_options()

course_code_label = tk.Label(students_frame, text="Course Code:", bg="skyblue", font=custom_font)
course_code_label.grid(row=4, column=0, padx=5, pady=5, sticky="W")
course_code_var = tk.StringVar()
course_code_option = ttk.OptionMenu(students_frame, course_code_var, "", style="Custom.TMenubutton")
course_code_option["menu"].config(bg="skyblue", font=custom_font)
course_code_option.grid(row=4, column=1, padx=5, pady=5)
populate_course_codes()

add_button = tk.Button(students_frame, text="Add Student", command=add_student, bg="lightpink", fg="black", font=custom_font)
add_button.grid(row=5, column=0, padx=5, pady=5)

update_button = tk.Button(students_frame, text="Update Student", command=update_student, bg="lightpink", fg="black", font=custom_font)
update_button.grid(row=5, column=1, padx=5, pady=5)

read_button = tk.Button(students_frame, text="Read Student", command=read_student, bg="lightpink", fg="black", font=custom_font)
read_button.grid(row=5, column=2, padx=5, pady=5)

list_button = tk.Button(students_frame, text="List Students", command=populate_listbox, bg="lightpink", fg="black", font=custom_font)
list_button.grid(row=5, column=3, padx=5, pady=5)

delete_button = tk.Button(students_frame, text="Delete Student", command=delete_student, bg="lightpink", fg="black", font=custom_font)
delete_button.grid(row=5, column=4, padx=5, pady=5)

clear_button = tk.Button(students_frame, text="Clear", command=clear_entries, bg="lightpink", fg="black", font=custom_font)
clear_button.grid(row=6, column=4, padx=5, pady=5)

search_label = tk.Label(students_frame, text="Search by Student ID:", bg="skyblue", font=custom_font)
search_label.grid(row=6, column=0, padx=5, pady=5, sticky="W")
search_entry = tk.Entry(students_frame, font=custom_font)
search_entry.grid(row=6, column=1, padx=5, pady=5)

search_button = tk.Button(students_frame, text="Search", command=search_student, bg="lightpink", fg="black", font=custom_font)
search_button.grid(row=6, column=3, padx=5, pady=5)

listbox = tk.Listbox(students_frame, height=20, width=125, font=("Courier New", 12))
listbox.grid(row=7, column=0, columnspan=5, padx=5, pady=5, sticky="W")

scrollbar = tk.Scrollbar(students_frame)
scrollbar.grid(row=7, column=6, sticky="NS")
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Create Course Management GUI
course_code_label = tk.Label(course_frame, text="Course Code:", bg="skyblue", font=custom_font)
course_code_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")
course_code_entry = tk.Entry(course_frame, font=custom_font)
course_code_entry.grid(row=0, column=1, padx=5, pady=5)

course_name_label = tk.Label(course_frame, text="Course Name:", bg="skyblue", font=custom_font)
course_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="W")
course_name_entry = tk.Entry(course_frame, font=custom_font)
course_name_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = tk.Button(course_frame, text="Add Course", command=add_course, bg="lightpink", fg="black", font=custom_font)
add_button.grid(row=5, column=0, padx=5, pady=5)

update_button = tk.Button(course_frame, text="Update Course", command=update_course, bg="lightpink", fg="black", font=custom_font)
update_button.grid(row=5, column=1, padx=5, pady=5)

read_button = tk.Button(course_frame, text="Read Course", command=read_course, bg="lightpink", fg="black", font=custom_font)
read_button.grid(row=5, column=2, padx=5, pady=5)

list_button = tk.Button(course_frame, text="List Course", command=populate_course_listbox, bg="lightpink", fg="black", font=custom_font)
list_button.grid(row=5, column=3, padx=5, pady=5)

delete_button = tk.Button(course_frame, text="Delete Course", command=delete_course, bg="lightpink", fg="black", font=custom_font)
delete_button.grid(row=5, column=4, padx=5, pady=5)

clear_button = tk.Button(course_frame, text="Clear", command=clear_course_entries, bg="lightpink", fg="black", font=custom_font)
clear_button.grid(row=6, column=3, padx=5, pady=5)

search_label = tk.Label(course_frame, text="Search by Course Code:", bg="skyblue", font=custom_font)
search_label.grid(row=6, column=0, padx=5, pady=5, sticky="W")
search_course_entry = tk.Entry(course_frame, font=custom_font)
search_course_entry.grid(row=6, column=1, padx=5, pady=5)

search_button = tk.Button(course_frame, text="Search", command=search_course, bg="lightpink", fg="black", font=custom_font)
search_button.grid(row=6, column=2, padx=5, pady=5)

course_listbox = tk.Listbox(course_frame, height=25, width=125, font=("Courier New", 12))
course_listbox.grid(row=7, column=0, columnspan=5, padx=5, pady=5, sticky="W")

scrollbar = tk.Scrollbar(course_frame)
scrollbar.grid(row=7, column=6, sticky="NS")
course_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

populate_listbox()
populate_course_listbox()


window.mainloop()

# Close Database Connection
conn.close()
