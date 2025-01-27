import os
import json
import random
import string
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox, simpledialog

# File paths
KEY_FILE = "key.key"
DATA_FILE = "passwords.json"

# Generate or load encryption key
def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

key = generate_key()
cipher = Fernet(key)

# Add category options
CATEGORIES = ["Logins", "Payments", "Personal Info"]

# Function to update input fields based on selected category
def update_input_fields(*args):
    category = category_var.get()
    clear_input_fields()

    if category == "Logins":
        tk.Label(input_frame, text="Website URL:").pack()
        global website_url_entry, username_entry, password_entry
        website_url_entry = tk.Entry(input_frame, width=40)
        website_url_entry.pack()

        tk.Label(input_frame, text="Username:").pack()
        username_entry = tk.Entry(input_frame, width=40)
        username_entry.pack()

        tk.Label(input_frame, text="Password:").pack()
        password_entry = tk.Entry(input_frame, width=40, show="*")
        password_entry.pack()

    elif category == "Payments":
        tk.Label(input_frame, text="Cardholder Name:").pack()
        global cardholder_name_entry, card_number_entry, expiry_date_entry, cvv_entry
        cardholder_name_entry = tk.Entry(input_frame, width=40)
        cardholder_name_entry.pack()

        tk.Label(input_frame, text="Card Number:").pack()
        card_number_entry = tk.Entry(input_frame, width=40)
        card_number_entry.pack()

        tk.Label(input_frame, text="Expiry Date:").pack()
        expiry_date_entry = tk.Entry(input_frame, width=40)
        expiry_date_entry.pack()

        tk.Label(input_frame, text="CVV:").pack()
        cvv_entry = tk.Entry(input_frame, width=40)
        cvv_entry.pack()

    elif category == "Personal Info":
        tk.Label(input_frame, text="Full Name:").pack()
        global full_name_entry, email_entry, phone_number_entry, address_entry
        full_name_entry = tk.Entry(input_frame, width=40)
        full_name_entry.pack()

        tk.Label(input_frame, text="Email:").pack()
        email_entry = tk.Entry(input_frame, width=40)
        email_entry.pack()

        tk.Label(input_frame, text="Phone Number:").pack()
        phone_number_entry = tk.Entry(input_frame, width=40)
        phone_number_entry.pack()

        tk.Label(input_frame, text="Address:").pack()
        address_entry = tk.Entry(input_frame, width=40)
        address_entry.pack()

    tk.Label(input_frame, text="Item Name:").pack()
    global item_name_entry
    item_name_entry = tk.Entry(input_frame, width=40)
    item_name_entry.pack()

# Function to clear all input fields
def clear_input_fields():
    for widget in input_frame.winfo_children():
        widget.destroy()

# Function to save data
def save_data():
    category = category_var.get()
    item_name = item_name_entry.get()

    if not item_name:
        messagebox.showwarning("Input Error", "Item Name is required!")
        return

    data = {}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Data file is corrupted!")
            return

    try:
        if category == "Logins":
            website_url = website_url_entry.get()
            username = username_entry.get()
            password = password_entry.get()

            if not website_url or not username or not password:
                messagebox.showwarning("Input Error", "All fields are required!")
                return

            encrypted_password = cipher.encrypt(password.encode()).decode()
            data[item_name] = {
                "category": category,
                "website_url": website_url,
                "username": username,
                "password": encrypted_password
            }

        elif category == "Payments":
            cardholder_name = cardholder_name_entry.get()
            card_number = card_number_entry.get()
            expiry_date = expiry_date_entry.get()
            cvv = cvv_entry.get()

            if not cardholder_name or not card_number or not expiry_date or not cvv:
                messagebox.showwarning("Input Error", "All fields are required!")
                return

            encrypted_card_number = cipher.encrypt(card_number.encode()).decode()
            encrypted_cvv = cipher.encrypt(cvv.encode()).decode()
            data[item_name] = {
                "category": category,
                "cardholder_name": cardholder_name,
                "card_number": encrypted_card_number,
                "expiry_date": expiry_date,
                "cvv": encrypted_cvv
            }

        elif category == "Personal Info":
            full_name = full_name_entry.get()
            email = email_entry.get()
            phone_number = phone_number_entry.get()
            address = address_entry.get()

            if not full_name or not email or not phone_number or not address:
                messagebox.showwarning("Input Error", "All fields are required!")
                return

            encrypted_phone_number = cipher.encrypt(phone_number.encode()).decode()
            data[item_name] = {
                "category": category,
                "full_name": full_name,
                "email": email,
                "phone_number": encrypted_phone_number,
                "address": address
            }

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo("Success", f"Data saved for {item_name}!")
        clear_input_fields()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to generate a strong password
def generate_password():
    if 'password_entry' not in globals():
        messagebox.showwarning("Error", "Password field is not available!")
        return

    length = simpledialog.askinteger("Generate Password", "Enter password length:", minvalue=8, maxvalue=32)
    if not length:
        return

    characters = string.ascii_letters + string.digits + string.punctuation
    new_password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, new_password)

# GUI Setup
root = tk.Tk()
root.title("Password Manager")
root.geometry("500x450")

# Category Selection
tk.Label(root, text="Select Category:").pack()
category_var = tk.StringVar(value=CATEGORIES[0])
category_menu = tk.OptionMenu(root, category_var, *CATEGORIES, command=update_input_fields)
category_menu.pack()

# Input Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Buttons
tk.Button(root, text="Save Data", command=save_data).pack(pady=5)
tk.Button(root, text="Generate Password", command=generate_password).pack(pady=5)

# Initialize input fields
update_input_fields()

root.mainloop()