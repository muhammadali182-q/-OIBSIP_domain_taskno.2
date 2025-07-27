import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DB_NAME = "bmi_data.db"

BMI_CATEGORIES = [
    ("Underweight", 0, 18.5, "#87CEEB"),
    ("Normal", 18.5, 25, "#90EE90"),
    ("Overweight", 25, 30, "#FFD700"),
    ("Obese", 30, 100, "#FF6347")
]

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bmi_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            category TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_bmi(user, weight, height, bmi, category):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO bmi_history (user, weight, height, bmi, category, date) VALUES (?, ?, ?, ?, ?, ?)",
              (user, weight, height, bmi, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def fetch_history(user):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT date, bmi, category FROM bmi_history WHERE user=? ORDER BY date ASC", (user,))
    data = c.fetchall()
    conn.close()
    return data

def calculate_bmi(weight, height):
    try:
        bmi = float(weight) / ((float(height)/100)**2)
        return round(bmi, 2)
    except Exception:
        return None

def categorize_bmi(bmi):
    for cat, low, high, color in BMI_CATEGORIES:
        if low <= bmi < high:
            return cat, color
    return "Unknown", "#ffffff"

class BMICalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced BMI Calculator")
        self.configure(bg="#222831")
        self.geometry("620x540")
        self.resizable(False, False)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#222831", foreground="#eeeeee", font=("Segoe UI", 12))
        self.style.configure("TButton", font=("Segoe UI", 12), background="#00adb5", foreground="#eeeeee")
        self.create_widgets()
        init_db()

    def create_widgets(self):
        title = ttk.Label(self, text="🌟 Advanced BMI Calculator 🌟", font=("Segoe UI", 22, "bold"))
        title.pack(pady=12)
        frm = ttk.Frame(self)
        frm.pack(pady=5)
        ttk.Label(frm, text="Username:").grid(row=0, column=0, padx=8, pady=4, sticky="e")
        self.user_entry = ttk.Entry(frm, width=20)
        self.user_entry.grid(row=0, column=1, padx=8, pady=4)
        ttk.Label(frm, text="Weight (kg):").grid(row=1, column=0, padx=8, pady=4, sticky="e")
        self.weight_entry = ttk.Entry(frm, width=10)
        self.weight_entry.grid(row=1, column=1, padx=8, pady=4)
        ttk.Label(frm, text="Height (cm):").grid(row=2, column=0, padx=8, pady=4, sticky="e")
        self.height_entry = ttk.Entry(frm, width=10)
        self.height_entry.grid(row=2, column=1, padx=8, pady=4)
        calc_btn = ttk.Button(frm, text="Calculate BMI", command=self.on_calculate)
        calc_btn.grid(row=3, column=0, columnspan=2, pady=8)

        self.result_frame = ttk.Frame(self)
        self.result_frame.pack(pady=6)
        self.bmi_label = ttk.Label(self.result_frame, text="BMI: --", font=("Segoe UI", 15, "bold"))
        self.bmi_label.grid(row=0, column=0, padx=5)
        self.category_label = ttk.Label(self.result_frame, text="Category: --", font=("Segoe UI", 15))
        self.category_label.grid(row=0, column=1, padx=5)

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=7)
        hist_btn = ttk.Button(self, text="Show History & Trends", command=self.show_history)
        hist_btn.pack(pady=5)

        info = ttk.Label(self, text="• Input your weight and height to calculate BMI.\n• View your historical data and trends.", font=("Segoe UI", 10))
        info.pack(pady=6)

    def on_calculate(self):
        user = self.user_entry.get().strip()
        weight = self.weight_entry.get().strip()
        height = self.height_entry.get().strip()
        if not user:
            messagebox.showerror("Input Error", "Please enter a username.")
            return
        try:
            w = float(weight)
            h = float(height)
            if not (20 <= w <= 300 and 80 <= h <= 250):
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Weight must be 20-300kg, Height 80-250cm.")
            return

        bmi = calculate_bmi(w, h)
        if bmi is None:
            messagebox.showerror("Calculation Error", "Unable to calculate BMI.")
            return
        category, color = categorize_bmi(bmi)
        self.bmi_label.config(text=f"BMI: {bmi}", foreground=color)
        self.category_label.config(text=f"Category: {category}", foreground=color)
        save_bmi(user, w, h, bmi, category)

    def show_history(self):
        user = self.user_entry.get().strip()
        if not user:
            messagebox.showerror("Input Error", "Enter a username to view history.")
            return
        data = fetch_history(user)
        if not data:
            messagebox.showinfo("No Data", "No BMI records found for this user.")
            return
        hist_win = tk.Toplevel(self)
        hist_win.title(f"{user}'s BMI History & Trends")
        hist_win.geometry("650x480")
        hist_win.configure(bg="#393e46")
        ttk.Label(hist_win, text=f"BMI History for {user}", font=("Segoe UI", 16, "bold")).pack(pady=10)

        tree = ttk.Treeview(hist_win, columns=("Date", "BMI", "Category"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("BMI", text="BMI")
        tree.heading("Category", text="Category")
        for date, bmi, cat in data:
            tree.insert("", "end", values=(date, bmi, cat))
        tree.pack(pady=10, fill="x", padx=20)

        # Plot BMI trend
        dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in data]
        bmis = [row[1] for row in data]

        if len(bmis) > 1:
            fig = plt.Figure(figsize=(5,2.3), dpi=100)
            ax = fig.add_subplot(111)
            ax.plot(dates, bmis, marker='o', color='#00adb5', linewidth=2)
            ax.set_title("BMI Trend")
            ax.set_xlabel("Date")
            ax.set_ylabel("BMI")
            fig.autofmt_xdate()
            canvas = FigureCanvasTkAgg(fig, master=hist_win)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=13)
        else:
            ttk.Label(hist_win, text="Add more entries to view your BMI trend graph.", background="#393e46", foreground="#eeeeee").pack(pady=20)

if __name__ == "__main__":
    BMICalculatorApp().mainloop()