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

root = tk.Tk()
create_entries(root, 5)  # Create 5 entries for example

btn = tk.Button(root, text="Print Values", command=get_entry_values)
btn.pack()

root.mainloop()
