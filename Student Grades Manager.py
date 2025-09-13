import tkinter as tk
from tkinter import ttk, messagebox
import csv, os

FILENAME = "students.csv"

# Utility Functions
def save_to_csv(data):
    """Append a student record to CSV."""
    with open(FILENAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)

def load_from_csv():
    """Load all records from CSV."""
    records = []
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            reader = csv.reader(f)
            records = list(reader)
    return records

# Core Functions
def add_student():
    sid = entry_id.get().strip()
    name = entry_name.get().strip()
    math = entry_math.get().strip()
    eng = entry_eng.get().strip()
    sci = entry_sci.get().strip()

    if not sid or not name or not math or not eng or not sci:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        math, eng, sci = int(math), int(eng), int(sci)
    except ValueError:
        messagebox.showerror("Error", "Marks must be numbers!")
        return

    row = [sid, name, math, eng, sci]
    tree.insert("", "end", values=row)
    save_to_csv(row)

    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_math.delete(0, tk.END)
    entry_eng.delete(0, tk.END)
    entry_sci.delete(0, tk.END)

def load_data():
    for row in load_from_csv():
        tree.insert("", "end", values=row)

def search_student():
    keyword = entry_search.get().strip().lower()
    for row in tree.get_children():
        tree.delete(row)

    all_records = load_from_csv()
    for rec in all_records:
        if keyword in rec[0].lower() or keyword in rec[1].lower():
            tree.insert("", "end", values=rec)

def show_all():
    for row in tree.get_children():
        tree.delete(row)
    load_data()

def show_statistics():
    records = load_from_csv()
    if not records:
        messagebox.showinfo("Stats", "No data available.")
        return

    math_scores = [int(r[2]) for r in records]
    eng_scores = [int(r[3]) for r in records]
    sci_scores = [int(r[4]) for r in records]

    stats = f"""
    Mathematics → Avg: {sum(math_scores)/len(math_scores):.2f}, 
                  High: {max(math_scores)}, Low: {min(math_scores)}

    English     → Avg: {sum(eng_scores)/len(eng_scores):.2f}, 
                   High: {max(eng_scores)}, Low: {min(eng_scores)}

    Science     → Avg: {sum(sci_scores)/len(sci_scores):.2f}, 
                   High: {max(sci_scores)}, Low: {min(sci_scores)}
    """
    messagebox.showinfo("Statistics", stats)

# GUI Setup

root = tk.Tk()
root.title("Student Grades Manager")
root.geometry("800x500")

# --- Input Frame ---
frame_input = tk.Frame(root, pady=10)
frame_input.pack(fill="x")

tk.Label(frame_input, text="ID").grid(row=0, column=0)
entry_id = tk.Entry(frame_input, width=10)
entry_id.grid(row=0, column=1)

tk.Label(frame_input, text="Name").grid(row=0, column=2)
entry_name = tk.Entry(frame_input, width=20)
entry_name.grid(row=0, column=3)

tk.Label(frame_input, text="Math").grid(row=0, column=4)
entry_math = tk.Entry(frame_input, width=10)
entry_math.grid(row=0, column=5)

tk.Label(frame_input, text="English").grid(row=0, column=6)
entry_eng = tk.Entry(frame_input, width=10)
entry_eng.grid(row=0, column=7)

tk.Label(frame_input, text="Science").grid(row=0, column=8)
entry_sci = tk.Entry(frame_input, width=10)
entry_sci.grid(row=0, column=9)

btn_add = tk.Button(frame_input, text="Add Student", command=add_student, bg="green", fg="white")
btn_add.grid(row=0, column=10, padx=10)

# --- Search Frame ---
frame_search = tk.Frame(root, pady=10)
frame_search.pack(fill="x")

tk.Label(frame_search, text="Search (ID/Name)").pack(side="left")
entry_search = tk.Entry(frame_search, width=20)
entry_search.pack(side="left", padx=5)
tk.Button(frame_search, text="Search", command=search_student, bg="orange", fg="white").pack(side="left", padx=5)
tk.Button(frame_search, text="Show All", command=show_all,  bg="purple", fg="white").pack(side="left", padx=5)
tk.Button(frame_search, text="Statistics", command=show_statistics, bg="red", fg="white").pack(side="right", padx=5)

# --- Table Frame ---
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True)

columns = ("ID", "Name", "Math", "English", "Science")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

# Load existing data on startup
load_data()
root.mainloop()
