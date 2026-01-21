import bcrypt
import json
import time
from tkinter import messagebox

JSON_FILE = "users.json"

# Hashen
def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw.decode('utf-8'), salt.decode('utf-8')

# Prüfen
def check_password(input_password: str, stored_hash: str):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_hash.encode('utf-8'))

# JSON laden
def load_users():
    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# JSON speichern
def save_users(users):
    with open(JSON_FILE, "w") as f:
        json.dump(users, f, indent=2)

# Prüfen ob Login gesperrt
def can_login(user_data):
    current_time = time.time()
    if user_data.get("blocked_until", 0) > current_time:
        remaining = int(user_data["blocked_until"] - current_time)
        messagebox.showerror("Blocked", f"Too many tries! Try again in {remaining} seconds.")
        return False
    return True

# Fehlerhafte Loginversuche
def handle_failed_login(user_data, username):
    user_data["failed_attempts"] = user_data.get("failed_attempts", 0) + 1
    if user_data["failed_attempts"] >= 4:
        user_data["blocked_until"] = time.time() + 60  # 1 Minute Sperre
        user_data["failed_attempts"] = 0
        messagebox.showerror("Blocked", "Too many failed attempts. Try again in 1 minute.")
    else:
        remaining = 4 - user_data["failed_attempts"]
        messagebox.showerror("Error", f"Wrong password. {remaining} tries left.")

# Login erfolgreich
def handle_success_login(user_data):
    user_data["failed_attempts"] = 0
    user_data["blocked_until"] = 0



