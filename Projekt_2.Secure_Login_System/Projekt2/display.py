import tkinter as tk
from tkinter import messagebox
import security

def set_display_window(width, height, title):
    window = tk.Tk()
    window.title(title)
    window.geometry(f"{width}x{height}")
    window.configure(bg="black")
    return window

# --- Registrierung ---
def open_register_window():
    win = tk.Toplevel(root)
    win.title("Register")
    win.geometry("500x400")
    win.configure(bg="black")

    tk.Label(win, text="Enter Username:", fg="red", bg="black").pack(pady=5)
    entry_username = tk.Entry(win, font=("Helvetica", 14))
    entry_username.pack(pady=5)

    tk.Label(win, text="Enter Password:", fg="red", bg="black").pack(pady=5)
    entry_password = tk.Entry(win, show="*", font=("Helvetica", 14))
    entry_password.pack(pady=5)

    tk.Label(win, text="Confirm Password:", fg="red", bg="black").pack(pady=5)
    entry_confirm = tk.Entry(win, show="*", font=("Helvetica", 14))
    entry_confirm.pack(pady=5)

    def submit_register():
        username = entry_username.get().strip()
        pw1 = entry_password.get()
        pw2 = entry_confirm.get()

        if not username or not pw1 or not pw2:
            messagebox.showerror("Error", "Fill in all fields")
            return
        if pw1 != pw2:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Passwort Regeln
        letters = sum(c.isalpha() for c in pw1)
        digits = sum(c.isdigit() for c in pw1)
        specials = sum(c in "!$%&?*#" for c in pw1)

        if len(pw1) < 10 or letters < 6 or digits < 2 or specials < 2:
            messagebox.showerror("Error", "Password must be 10+ chars, 6 letters, 2 numbers, 2 special (!$%&?*#)")
            return

        users = security.load_users()
        if username in users:
            messagebox.showerror("Error", "Username already exists")
            return

        hashed_pw, salt = security.hash_password(pw1)
        users[username] = {
            "password_hash": hashed_pw,
            "salt": salt,
            "failed_attempts": 0,
            "blocked_until": 0
        }
        security.save_users(users)
        messagebox.showinfo("Success", "Registered successfully!")
        win.destroy()
        open_login_window()

    tk.Button(win, text="Submit", fg="red", bg="black", command=submit_register).pack(pady=15)

# --- Login ---
def open_login_window():
    win = tk.Toplevel()
    win.title("Login")
    win.geometry("500x400")
    win.configure(bg="black")

    tk.Label(win, text="Enter Username:", fg="red", bg="black").pack(pady=10)
    entry_username = tk.Entry(win, font=("Helvetica", 14))
    entry_username.pack(pady=10)

    tk.Label(win, text="Enter Password:", fg="red", bg="black").pack(pady=10)
    entry_password = tk.Entry(win, show="*", font=("Helvetica", 14))
    entry_password.pack(pady=10)

    def submit_login():
        username = entry_username.get().strip()
        password = entry_password.get()

        users = security.load_users()
        if username not in users:
            messagebox.showerror("Error", "User does not exist")
            return

        user_data = users[username]

        if not security.can_login(user_data):
            return

        if not security.check_password(password, user_data["password_hash"]):
            security.handle_failed_login(user_data, username)
            security.save_users(users)
            return

        # Erfolg
        security.handle_success_login(user_data)
        security.save_users(users)
        messagebox.showinfo("Success", "Login successful!")
        win.destroy()

    tk.Button(win, text="Submit", fg="red", bg="black", command=submit_login).pack(pady=20)

# --- Hauptfenster ---
def set_button(window, text, command):
    tk.Button(window, text=text, fg="red", bg="black", font=("Helvetica", 14), command=command).pack(pady=10)

root = set_display_window(500, 400, "Secure Login System")
tk.Label(root, text="Secure Login System", fg="red", bg="black", font=("Helvetica", 16)).pack(pady=20)

set_button(root, "Register", open_register_window)
set_button(root, "Login", open_login_window)
set_button(root, "Exit", root.destroy)

root.mainloop()

