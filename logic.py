import json
import os
import tkinter as tk

def make_scrollable_frame(container):
    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scrollable_frame



def construct_dictionary(headers, content):
    package_json = {}

    for i, header in enumerate(headers):
        if i == 0:
            package_json["title"] = header
        else:
            package_json["description"] = header

    package_json["content"] = content
    return package_json

def save_json(package):

    filename = package["title"]
    os.makedirs("quizzes", exist_ok=True)

    filepath = os.path.join("quizzes", "quiz_" + filename + ".json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(package, f, indent=4, ensure_ascii=False)

    print(f"Quiz saved to {filepath}")

    
     
        


    
