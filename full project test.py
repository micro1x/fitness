import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import 


start_window = tk.Tk()
start_window.title("My Personal GymBro")
signupWindow = tk.Frame(start_window)
loginWindow = tk.Frame(start_window)
start_window.configure(bg='blue')


def calculate_bmi(weight, height, system='metric'):
    try:
        if system == 'metric':
            # BMI calculation for metric system (weight in kg, height in meters)
            bmi = weight / (height ** 2)
        elif system == 'imperial':
            # BMI calculation for imperial system (weight in lbs, height in inches)
            bmi = (weight / (height ** 2)) * 703
        else:
            raise ValueError("invalid")
    except ValueError:
        pass
    return bmi

def interpret_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    elif bmi >= 30:
        return "Obesity"

def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
              (username TEXT PRIMARY KEY, password TEXT, Height FLOAT, Weight FLOAT, BMI FLOAT)''')
    conn.commit()
    conn.close()

def signup():
    register_status = StringVar()
    signupWindow.pack(fill=tk.BOTH, expand=True)
    hideframe.pack_forget()

    username_label = Label(signupWindow, text="Username:")
    username_label.pack()
    username_entry = Entry(signupWindow)
    username_entry.pack()

    password_label = Label(signupWindow, text="Password:")
    password_label.pack()
    password_entry = Entry(signupWindow, show="*")
    password_entry.pack()

    weight_label = Label(signupWindow, text="Weight (lbs):")
    weight_label.pack()
    weight_entry = Entry(signupWindow)
    weight_entry.pack()

    height_label = Label(signupWindow, text="Height (inches):")
    height_label.pack()
    height_entry = Entry(signupWindow)
    height_entry.pack()

    system_label = Label(signupWindow, text="System (metric/imperial):")
    system_label.pack()
    system_entry = Entry(signupWindow)
    system_entry.pack()

    register_status = StringVar()
    register_status_label = Label(signupWindow, textvariable=register_status)
    register_status_label.pack()

    def submit_signup():
        username = username_entry.get()
        password = password_entry.get()
        hashed_password = hash_password(password)
        height = height_entry.get()
        weight = weight_entry.get()

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, Height, Weight, BMI) VALUES (?, ?, ?, ?, ?)", 
                  (username, hashed_password, height, weight, calculate_bmi(float(height), float(weight))))

        conn.commit()
        conn.close()

        weight_entry.delete(0, END)
        height_entry.delete(0, END)
        register_status.set("Registration successful!")

        time.sleep(3)

        signupWindow.destroy()
        start_window.destroy()
        moodtest = tk.Tk()
        screen_width = moodtest.winfo_screenwidth()
        screen_height = moodtest.winfo_screenheight()

# Set the window dimensions to match the screen resolution
        moodtest.geometry(f"{screen_width}x{screen_height}")
        moodtest.mainloop()

    submitButton = tk.Button(signupWindow, text="Submit", command=submit_signup)
    submitButton.pack()


def login():
    def log_in():
        username = username_entry.get()
        password = password_entry.get()
        hashed_password = hash_password(password)

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # Fetch user from the database
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = c.fetchone()

        conn.close()

        if user:
            login_status.set("Login successful!")
            weight = user[2]
            height = user[3]
            messagebox.showinfo("Information", f"Your current weight is {weight} lbs and height is {height} inches")
            switch_prompt=messagebox.askyesno("Change weight and height", "Do you want to change your weight and height by any chance?")
            if switch_prompt:
                switch_weight_height(username)
        else:
            login_status.set("Invalid username or password")

    loginWindow.pack(fill=tk.BOTH, expand=True)
    hideframe.pack_forget()

    username_label = Label(loginWindow, text="Username:")
    username_label.pack()
    username_entry = Entry(loginWindow)
    username_entry.pack()

    password_label = Label(loginWindow, text="Password:")
    password_label.pack()
    password_entry = Entry(loginWindow, show="*")
    password_entry.pack()

    login_status = StringVar()
    login_status_label = Label(loginWindow, textvariable=login_status)
    login_status_label.pack()

    submitButton = tk.Button(loginWindow, text="Submit", command=log_in)
    submitButton.pack()

def switch_weight_height(username):
    def submit_changes():
        new_weight = float(weight_entry.get())
        new_height = float(height_entry.get())

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("UPDATE users SET Weight=?, Height=? WHERE username=?", (new_weight, new_height, username))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Weight and height updated successfully!")

    changeWindow = Toplevel()
    changeWindow.title("Change Weight and Height")

    weight_label = Label(changeWindow, text="New Weight (lbs):")
    weight_label.pack()
    weight_entry = Entry(changeWindow)
    weight_entry.pack()

    height_label = Label(changeWindow, text="New Height (inches):")
    height_label.pack()
    height_entry = Entry(changeWindow)
    height_entry.pack()

    submitButton = Button(changeWindow, text="Submit", command=submit_changes)
    submitButton.pack()

def hash_password(password):
    # Implement your password hashing algorithm here (e.g., bcrypt, hashlib)
    # For demonstration, let's just return the password as is
    return password

hideframe = tk.Frame(start_window)

sign_button = tk.Button(start_window, text="Sign Up", width=35, height=5, bg="black", fg="white", command=signup)
sign_button.pack(pady=10)
login_button = tk.Button(start_window, text="Login", width=35, height=5, bg="black", fg="white", command=login)
login_button.pack(pady=10)

create_table()

start_window.mainloop()