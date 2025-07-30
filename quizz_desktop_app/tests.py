import tkinter as tk

entries = [{"text": "this is text 01", "point": "1"},
           {"text": "this is text 02", "point": "0"}]

entries_dick = {}
i = 0
for key in entries:
    entries_dick[f"entry {i + 1}"] = {}
    entries_dick[f"entry {i + 1}"]["text"] = key["text"]
    entries_dick[f"entry {i + 1}"]["point"] = key["point"]
    i += 1
print(entries_dick)