# Ken Andrea Bahian
# 2nd Year | BS Statistics
# CCC151 STT-B 
# ASSIGNMENT NO. 3
# SSIS VERSION 1



import csv
import tkinter as tk
from tkinter import messagebox, ttk

# Global variables
students_file = 'students.csv'
courses_file = 'courses.csv'
gender_choices = ['Male', 'Female']
year_level_choices = ['1st year', '2nd year', '3rd year', '4th year']

def get_course_code(course_code):
    with open(courses_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == course_code:
                return row[0]
    return None

# Student Management System functions
def create_student():
    student_id = entry_id.get()
    name = entry_name.get()
    gender = combo_gender.get()
    year_level = combo_year_level.get()
    course_code = entry_course_code.get()

    if not validate_course_code(course_code):
        messagebox.showinfo('Error', 'Invalid course code. Please enter a valid course code.')
        return

    with open(students_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([student_id, name, gender, year_level, course_code])

    clear_entries()
    messagebox.showinfo('Success', 'Student created successfully.')

def validate_course_code(course_code):
    with open(courses_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == course_code:
                return True
    return False 
 
def list_students():
    clear_listbox()
    header = f"{'| ID':<17}{'| Name':<27}{'| Gender':<12}{'| Year Level':<17}{'| Course Code'}"
    separator = '-' * (len(header) + 1)
    listbox.insert(tk.END, header)
    listbox.insert(tk.END, separator)

    with open(students_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            course_code = get_course_code(row[4])  # Get course name based on course code
            student_info = f"| {row[0]:<15}| {row[1]:<25}| {row[2]:<10}| {row[3]:<15}| {course_code}"
            listbox.insert(tk.END, student_info)

    listbox.insert(tk.END, separator)
    
def read_student():
    student_id = entry_search_id.get()

    with open(students_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == student_id:
                entry_id.delete(0, tk.END)
                entry_id.insert(tk.END, row[0])
                entry_name.delete(0, tk.END)
                entry_name.insert(tk.END, row[1])
                combo_gender.set(row[2])
                combo_year_level.set(row[3])
                entry_course_code.delete(0, tk.END)
                entry_course_code.insert(tk.END, row[4])
                return

    messagebox.showinfo('Not Found', 'Student ID not found.')
    
def search_student():
    student_id = entry_search_id.get()

    with open(students_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == student_id:
                clear_listbox()
                listbox.insert(tk.END, f"{'| ID':<17}{'| Name':<27}{'| Gender':<12}{'| Year Level':<17}{'| Course Code'}")
                listbox.insert(tk.END, '-' * 70)
                listbox.insert(tk.END, f"| {row[0]:<15}| {row[1]:<25}| {row[2]:<10}| {row[3]:<15}| {row[4]}")
                return

    messagebox.showinfo('Not Found', 'Student ID not found.')
    
def update_student():
    student_id = entry_id.get()
    name = entry_name.get()
    gender = combo_gender.get()
    year_level = combo_year_level.get()
    course_code = entry_course_code.get()

    with open(students_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    found = False
    for i in range(len(rows)):
        if rows[i][0] == student_id:
            rows[i] = [student_id, name, gender, year_level, course_code]
            found = True
            break

    if found:
        with open(students_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        clear_entries()
        messagebox.showinfo('Success', 'Student updated successfully.')
    else:
        messagebox.showinfo('Not Found', 'Student ID not found.')

def delete_student():
    student_id = entry_id.get()

    with open(students_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    found = False
    for i in range(len(rows)):
        if rows[i][0] == student_id:
            rows.pop(i)
            found = True
            break

    if found:
        with open(students_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        clear_entries()
        messagebox.showinfo('Success', 'Student deleted successfully.')
    else:
        messagebox.showinfo('Not Found', 'Student ID not found.')

# Course Management System functions
def create_course():
    course_code = entry_code.get()
    course_name = entry_course_name.get()

    with open(courses_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([course_code, course_name])
    
    clear_entries()
    messagebox.showinfo('Success', 'Course created successfully.')

def read_course():
    course_code = entry_search_code.get()

    with open(courses_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == course_code:
                entry_code.delete(0, tk.END)
                entry_code.insert(tk.END, row[0])
                entry_course_name.delete(0, tk.END)
                entry_course_name.insert(tk.END, row[1])
                return

    messagebox.showinfo('Not Found', 'Course code not found.')

def list_courses():
    clear_listbox()
    header = f"{'| Code':<10}{'| Course Name':<27}"
    separator = '-' * (len(header) + 1)
    listbox.insert(tk.END, header)
    listbox.insert(tk.END, separator)

    with open(courses_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            course_info = f"| {row[0]:<8}| {row[1]:<23}"
            listbox.insert(tk.END, course_info)

    listbox.insert(tk.END, separator)
            
def search_course():
    course_code = entry_search_code.get()

    with open(courses_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == course_code:
                clear_listbox()
                listbox.insert(tk.END, f"{'| Code':<12}{'| Course Name':<25}")
                listbox.insert(tk.END, '-' * 50)
                listbox.insert(tk.END, f"| {row[0]:<10}| {row[1]:<25}")
                return

    messagebox.showinfo('Not Found', 'Course code not found.')

def update_course():
    course_code = entry_code.get()
    course_name = entry_course_name.get()

    with open(courses_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    found = False
    for i in range(len(rows)):
        if rows[i][0] == course_code:
            rows[i] = [course_code, course_name]
            found = True
            break

    if found:
        with open(courses_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        clear_entries()
        messagebox.showinfo('Success', 'Course updated successfully.')
    else:
        messagebox.showinfo('Not Found', 'Course code not found.')

def delete_course():
    course_code = entry_code.get()

    with open(courses_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    found = False
    for i in range(len(rows)):
        if rows[i][0] == course_code:
            rows.pop(i)
            found = True
            break

    if found:
        with open(courses_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        clear_entries()
        messagebox.showinfo('Success', 'Course deleted successfully.')
    else:
        messagebox.showinfo('Not Found', 'Course code not found.')

# GUI Functions
def clear_entries():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    combo_gender.set('')
    combo_year_level.set('')
    entry_course_code.delete(0, tk.END)
    entry_code.delete(0, tk.END)
    entry_course_name.delete(0, tk.END)
    entry_search_id.delete(0, tk.END)
    entry_search_code.delete(0, tk.END)

def clear_listbox():
    listbox.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title('Student and Course Management System')
root.geometry("1375x1000")
root.configure(bg='lightpink')

style = ttk.Style()
style.configure("Custom.TFrame", background="skyblue")

# Customize the style of the tab headers
style.configure("TNotebook.Tab", font=("Courier New", 12, "bold"))
style.configure("TNotebook.Tab", foreground="black")
# Create the notebook (tabbed interface)
notebook = ttk.Notebook(root)

# Create the student management tab
tab_student = ttk.Frame(notebook, style="Custom.TFrame")
notebook.add(tab_student, text='Student Management')

# Define a custom font
custom_font=("Courier New", 12, "bold")

# Create the student management widgets
label_id = tk.Label(tab_student, text='ID:', bg="skyblue", font=custom_font)
label_id.grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_id = tk.Entry(tab_student, font=custom_font)
entry_id.grid(row=0, column=1, padx=5, pady=5)

label_name = tk.Label(tab_student, text='Name:', bg="skyblue", font=custom_font)
label_name.grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_name = tk.Entry(tab_student, font=custom_font)
entry_name.grid(row=1, column=1, padx=5, pady=5)

label_gender = tk.Label(tab_student, text='Gender:', bg="skyblue", font=custom_font)
label_gender.grid(row=2, column=0, padx=5, pady=5, sticky='e')
combo_gender = ttk.Combobox(tab_student, values=gender_choices, font=custom_font)
combo_gender.grid(row=2, column=1, padx=5, pady=5)
combo_gender.configure(font=custom_font)

label_year_level = tk.Label(tab_student, text='Year Level:', bg="skyblue", font=custom_font)
label_year_level.grid(row=3, column=0, padx=5, pady=5, sticky='e')
combo_year_level = ttk.Combobox(tab_student, values=year_level_choices, font=custom_font)
combo_year_level.grid(row=3, column=1, padx=5, pady=5)
combo_year_level.configure(font=custom_font)


label_course_code = tk.Label(tab_student, text='Course Code:', bg="skyblue", font=custom_font)
label_course_code.grid(row=4, column=0, padx=5, pady=5, sticky='e')
entry_course_code = tk.Entry(tab_student, font=custom_font)
entry_course_code.grid(row=4, column=1, padx=5, pady=5)

button_create_student = tk.Button(tab_student, text='Create', bg="lightpink", fg="black", command=create_student, font=custom_font)
button_create_student.grid(row=5, column=0, padx=5, pady=5, sticky='w')

button_list_students = tk.Button(tab_student, text='List', bg="lightpink", fg="black", command=list_students, font=custom_font)
button_list_students.grid(row=5, column=1, padx=5, pady=5, sticky='e')

button_delete_student = tk.Button(tab_student, text='Delete', bg="lightpink", fg="black", command=delete_student, font=custom_font)
button_delete_student.grid(row=6, column=0, padx=5, pady=5, sticky='w')

button_update_student = tk.Button(tab_student, text='Update', bg="lightpink", fg="black", command=update_student, font=custom_font)
button_update_student.grid(row=6, column=1, padx=5, pady=5, sticky='e')

label_search_id = tk.Label(tab_student, text='Search ID:', bg="skyblue", font=custom_font)
label_search_id.grid(row=7, column=0, padx=5, pady=5, sticky='e')
entry_search_id = tk.Entry(tab_student, font=custom_font)
entry_search_id.grid(row=7, column=1, padx=5, pady=5)

button_search_student = tk.Button(tab_student, text='Search', bg="lightpink", fg="black", command=search_student, font=custom_font)
button_search_student.grid(row=8, column=0, padx=5, pady=5, sticky='w')

button_read_student = tk.Button(tab_student, text='Read', bg="lightpink", fg="black", command=read_student, font=custom_font)
button_read_student.grid(row=8, column=1, padx=5, pady=5, sticky='w')

button_clear_student = tk.Button(tab_student, text='Clear', bg="lightpink", fg="black", command=clear_entries, font=custom_font)
button_clear_student.grid(row=9, column=0, padx=5, pady=5, sticky='w')

# Create the course management tab
tab_course = ttk.Frame(notebook, style="Custom.TFrame")
notebook.add(tab_course, text='Course Management')

# Create the course management widgets
label_code = tk.Label(tab_course, text='Code:', bg="skyblue", font=custom_font)
label_code.grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_code = tk.Entry(tab_course, font=custom_font)
entry_code.grid(row=0, column=1, padx=5, pady=5)

label_course_name = tk.Label(tab_course, text='Course Name:', bg="skyblue", font=custom_font)
label_course_name.grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_course_name = tk.Entry(tab_course, font=custom_font)
entry_course_name.grid(row=1, column=1, padx=5, pady=5)

button_create_course = tk.Button(tab_course, text='Create', bg="lightpink", fg="black", command=create_course, font=custom_font)
button_create_course.grid(row=3, column=0, padx=5, pady=5, sticky='w')

button_read_courses = tk.Button(tab_course, text='List', bg="lightpink", fg="black", command=list_courses, font=custom_font)
button_read_courses.grid(row=3, column=1, padx=5, pady=5, sticky='e')

button_delete_course = tk.Button(tab_course, text='Delete', bg="lightpink", fg="black", command=delete_course, font=custom_font)
button_delete_course.grid(row=4, column=0, padx=5, pady=5, sticky='w')

button_update_course = tk.Button(tab_course, text='Update', bg="lightpink", fg="black", command=update_course, font=custom_font)
button_update_course.grid(row=4, column=1, padx=5, pady=5, sticky='e')

label_search_code = tk.Label(tab_course, text='Search Code:', bg="skyblue", font=custom_font)
label_search_code.grid(row=5, column=0, padx=5, pady=5, sticky='e')
entry_search_code = tk.Entry(tab_course, font=custom_font)
entry_search_code.grid(row=5, column=1, padx=5, pady=5)

button_search_course = tk.Button(tab_course, text='Search', bg="lightpink", fg="black", command=search_course, font=custom_font)
button_search_course.grid(row=6, column=0, padx=5, pady=5, sticky='w')

button_read_course = tk.Button(tab_course, text='Read', bg="lightpink", fg="black", command=read_course, font=custom_font)
button_read_course.grid(row=6, column=1, padx=5, pady=5, sticky='w')

button_clear_course = tk.Button(tab_course, text='Clear', bg="lightpink", fg="black", command=clear_entries, font=custom_font)
button_clear_course.grid(row=7, column=0, padx=5, pady=5, sticky='w')

# Create the listbox and scrollbar
listbox = tk.Listbox(root, width=90, font=("Courier New", 11))
listbox.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

scrollbarX = tk.Scrollbar(root)
scrollbarX.pack(side=tk.BOTTOM, fill=tk.X)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
scrollbarX.config(command=listbox.xview)

# Add the notebook to the root window
notebook.pack(padx=20, pady=120)

# Start the main event loop
root.mainloop()
