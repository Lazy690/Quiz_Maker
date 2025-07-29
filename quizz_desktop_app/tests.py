import tkinter as tk

entries = []

def create_entries(root, count):
    for _ in range(count):
        entry = tk.Entry(root)
        entry.pack()
        entries.append(entry)

def get_entry_values():
    values = [e.get() for e in entries]
    print(values)

list = [
    {"text": "Yes", "point": 2},
    {"text": "no", "point": 0},
    {"text": "maybe", "point": 1}]


for i in list:
    for c in i:
        print(i[c])