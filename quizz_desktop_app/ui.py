import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import logic
import uiFunctions
import requests
import os
import json


def start_ui():
    root = tk.Tk()
    root.title("Quiz Maker ver-0.1")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "assets", "quiz_maker_icon_img_01.png")
    icon = tk.PhotoImage(file=icon_path)
    root.iconphoto(True, icon)
    show_main_menu(root)
    root.geometry("800x600")
    root.mainloop()
    
def show_main_menu(root):
    for widget in root.winfo_children():
        widget.destroy()

    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    left_frame = tk.Frame(container)
    left_frame.pack(side="left", padx=40, pady=40, anchor="n")

    right_frame = tk.Frame(container, bg="lightgray")
    right_frame.pack(side="right", padx=40, pady=40, expand=True, fill="both")

    # Get the directory of the currently running script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, "assets", "quiz_maker_menu_img_02.png")

    # Load and place image in right_frame
    img = Image.open(img_path)
    img = img.resize((300, 300), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)

    img_label = tk.Label(right_frame, image=img_tk, bg="lightgray")
    img_label.image = img_tk  # Keep a reference!
    img_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the image

    # Buttons (unchanged)
    button_font = tkfont.Font(size=14)

    button_new = tk.Button(left_frame, text="New Quiz", width=20, height=2, font=button_font,
                           command=lambda: show_new_quiz_screen(root))
    button_new.pack(pady=10)

    button_manage = tk.Button(left_frame, text="Manage Quiz", width=20, height=2, font=button_font,
                              command=lambda: show_manage_quiz_screen(root))
    button_manage.pack(pady=10)

    button_upload = tk.Button(left_frame, text="Upload Quiz", width=20, height=2, font=button_font,
                              command=lambda: show_upload_quiz_screen(root))
    button_upload.pack(pady=10)

    button_exit = tk.Button(left_frame, text="Exit", width=20, height=2, font=button_font, command=exit)
    button_exit.pack(pady=10)

    contact_frame = tk.Frame(root, bg="lightgray")
    contact_frame.pack(side="bottom", pady=5)

    tk.Label(contact_frame, text="Developed by Victor Espinha", bg="lightgray", font=("Arial", 10)).pack()
    tk.Label(contact_frame, text="📞 +244 936 223 426  |  ✉️ victorespinha204@gmail.com", bg="lightgray", font=("Arial", 9)).pack()

def show_new_quiz_screen(root):
    
    for widget in root.winfo_children():
        widget.destroy()
    scrollable = logic.make_scrollable_frame(root)

    text_font = tkfont.Font(family="Arial", size=11)

        # Frame for Title and Description
    meta_frame = tk.LabelFrame(scrollable, text="Quiz Info", padx=10, pady=10, font=("Arial", 12, "bold"))
    meta_frame.pack(padx=20, pady=(20, 10), fill="x")

    # Title
    label = tk.Label(meta_frame, text="Enter Title:", font=("Arial", 11))
    label.pack(anchor="w", pady=(0, 5))

    title_box = tk.Text(meta_frame, height=1, width=60, wrap="word",
                        bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
    title_box.pack(fill="x")
    title_box.bind("<KeyRelease>", lambda event: logic.auto_resize_textbox(title_box, text_font))

    # Description
    label = tk.Label(meta_frame, text="Enter Description:", font=("Arial", 11))
    label.pack(anchor="w", pady=(10, 5))

    desc_box = tk.Text(meta_frame, height=1, width=60, wrap="word",
                       bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
    desc_box.pack(fill="x")
    desc_box.bind("<KeyRelease>", lambda event: logic.auto_resize_textbox(desc_box, text_font))


    # Button inside its own Frame with left-only padding
    button_frame = tk.Frame(scrollable)
    button_frame.pack(anchor="w", padx=(20, 0), pady=(10, 0))

    #add button
    add_button = tk.Button(button_frame, text="+", width=1, height=1, command= lambda: add_questions_button_onlcick(root))
    add_button.pack()

    #exit button
    exit = tk.Button(scrollable, text="back", command= lambda: show_main_menu(root))
    exit.pack()
    def add_questions_button_onlcick(root):
        
        #create window
        root_add = tk.Toplevel(root)
        root_add.title("Add questions")
        root_add.geometry("300x250")
        
        tk.Label(root_add, text="How many questions?: ", font=("Arial", 12)).pack()
        entry_ques = tk.Entry(root_add)
        entry_ques.pack()

        tk.Label(root_add, text="How many choices per question?: ", font=("Arial", 12)).pack()
        entry_choice = tk.Entry(root_add)
        entry_choice.pack()

        tk.Label(root_add, text="Max Score: ", font=("Arial", 12)).pack()
        entry_max_score = tk.Entry(root_add)
        entry_max_score.pack()

        tk.Label(root_add, text="How many answers?: ", font=("Arial", 12)).pack()
        entry_answers = tk.Entry(root_add)
        entry_answers.pack()
        
        def on_accept():
            questions = int(entry_ques.get())
            choices = int(entry_choice.get())
            max_score = int(entry_max_score.get())
            answers = int(entry_answers.get())
            present_questions_loop(questions=questions, choices=choices, max_score=max_score, answers=answers)
            add_button.destroy()
            exit.destroy()
            root_add.destroy()

        tk.Button(root_add, text="Accept", command=lambda:  on_accept()).pack()

    def present_questions_loop(**data):
        
        ques_count = data["questions"]
        choice_count = data["choices"]
        max_score = data["max_score"]
        answers = data["answers"]
        
        ques_text = []
        ques_options = []
        
        answer_text = []
        answer_conditions = []

        #render ques/opt
        for i in range(ques_count):
            # Box frame for each question
            ques_frame = tk.LabelFrame(scrollable, text=f"Question {i + 1}", padx=10, pady=10, font=("Arial", 11, "bold"))
            ques_frame.pack(padx=20, pady=15, fill="x", expand=True)

            # Question text
            ques_label = tk.Label(ques_frame, text="Question Text:", font=("Arial", 11))
            ques_label.pack(anchor="w", pady=(0, 5))

            present_ques_text = tk.Text(ques_frame, height=1, width=60, wrap="word",
                                        bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
            present_ques_text.pack(fill="x")
            present_ques_text.bind("<KeyRelease>", lambda event, box=present_ques_text: logic.auto_resize_textbox(box, text_font))
            ques_text.append(present_ques_text)

            ques_options_for_this_question = []

            for c in range(choice_count):
                option_frame = tk.Frame(ques_frame)
                option_frame.pack(fill="x", padx=20, pady=8)

                label = tk.Label(option_frame, text=f"Option {c + 1}:", font=("Arial", 10))
                label.grid(row=0, column=0, sticky="w")

                present_choice_text = tk.Text(option_frame, height=1, width=50, wrap="word",
                                            bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
                present_choice_text.grid(row=0, column=1, padx=(10, 0), sticky="w")
                present_choice_text.bind("<KeyRelease>", lambda event, box=present_choice_text: logic.auto_resize_textbox(box, text_font))

                # Points field with label
                point_label = tk.Label(option_frame, text="Points:", font=("Arial", 10))
                point_label.grid(row=0, column=2, padx=(20, 5), sticky="e")

                present_choice_point = tk.Text(option_frame, height=1, width=4,
                                            bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
                present_choice_point.grid(row=0, column=3, sticky="w")

                ques_option = {
                    "text": present_choice_text,
                    "point": present_choice_point
                }
                ques_options_for_this_question.append(ques_option)

            ques_options.append(ques_options_for_this_question)

        
        #render answer/points
        for i in range(answers):
            answer_score = {}

            # Outer frame for each answer block
            answer_frame = tk.LabelFrame(scrollable, text=f"Answer {i + 1}", padx=10, pady=10, font=("Arial", 11, "bold"))
            answer_frame.pack(padx=20, pady=15, fill="x", expand=True)

            # Frame for "From" and "To" fields on the same row
            range_frame = tk.Frame(answer_frame)
            range_frame.pack(anchor="w", pady=(0, 10))

            # From
            tk.Label(range_frame, text="From:", font=("Arial", 10)).grid(row=0, column=0, padx=(0, 5), sticky="w")
            answer_from = tk.Text(range_frame, height=1, width=4, bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
            answer_from.grid(row=0, column=1, padx=(0, 20), sticky="w")

            # To
            tk.Label(range_frame, text="To:", font=("Arial", 10)).grid(row=0, column=2, padx=(0, 5), sticky="w")
            answer_to = tk.Text(range_frame, height=1, width=4, bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
            answer_to.grid(row=0, column=3, sticky="w")

            # Answer explanation text box
            tk.Label(answer_frame, text="Answer Text:", font=("Arial", 10)).pack(anchor="w", padx=(0, 5), pady=(0, 5))
            present_answer_text = tk.Text(answer_frame, height=2, width=60, wrap="word",
                                        bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
            present_answer_text.pack(padx=10, fill="x")
            present_answer_text.bind("<KeyRelease>", lambda event, box=present_answer_text: logic.auto_resize_textbox(box, text_font))

            answer_score["from"] = answer_from
            answer_score["to"] = answer_to

            answer_conditions.append(answer_score)
            answer_text.append(present_answer_text)
   

                                                                          
        Save_button = tk.Button(scrollable, text="Save", command= lambda: logic.validate_new(title_box.get("1.0", "end-1c"),
                                                                                            desc_box.get("1.0", "end-1c"),
                                                                                            logic.get_ques_text(ques_text),
                                                                                            logic.get_options_box(ques_options),
                                                                                            logic.get_answer_text(answer_text),
                                                                                            logic.get_answer_score(answer_conditions),
                                                                                            max_score))
        Save_button.pack()
        #exit button
        exit = tk.Button(scrollable, text="back", command= lambda: show_main_menu(root))
        exit.pack()  
    
    
def show_upload_quiz_screen(root):
    for widget in root.winfo_children():
        widget.destroy()
    scrollable = logic.make_scrollable_frame(root)

    text_font = tkfont.Font(family="Arial", size=11)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(base_dir, "quizzes")
    file_list = [f for f in os.listdir(folder_path) if f.endswith('.json')]

    def selected_file(file_list, i):
        selected_file = file_list[i]
        return selected_file
    
    for i, file in enumerate(file_list):
        file_str = file.replace(".json", "")

        # Frame for each file row
        file_frame = tk.Frame(scrollable, pady=5, padx=10, bd=1, relief="groove")
        file_frame.pack(pady=10)

        # Center the contents of the frame
        inner_frame = tk.Frame(file_frame)
        inner_frame.pack()

        # File name label
        name_label = tk.Label(inner_frame, text=file_str, font=("Arial", 12))
        name_label.pack(side="left", padx=(5, 20))

        # Upload button
        upload_btn = tk.Button(inner_frame, text="Upload", width=10,
                            command=lambda i=i: upload_ask_confirm(root, selected_file(file_list, i)))
        upload_btn.pack(side="left")


    def upload_ask_confirm(root, selected):
        
        root_up_ask = tk.Toplevel(root)
        root_up_ask.title("comfirm")
        root_up_ask.geometry("300x150")
            
        tk.Label(root_up_ask, text="Do you comfirm this selection?", font=("Arial", 12)).pack()
        tk.Label(root_up_ask, text=selected, font=("Arial", 12)).pack()
        
        def on_accept():
            upload_json(selected)
            root_up_ask.destroy()

        tk.Button(root_up_ask, text="Accept", command=lambda:  on_accept()).pack()
        tk.Button(root_up_ask, text="Cancel", command=lambda:  root_up_ask.destroy()).pack()


    def upload_json(file):
        title = file

        def load_json(file):
            # Get base path relative to script location
            
            selected_filepath_locaction = os.path.join(base_dir, "quizzes", file)

            with open(selected_filepath_locaction, "r", encoding="utf-8") as f:
                data = json.load(f)

            return data
        quiz_data = load_json(title)

        response = requests.post("http://127.0.0.1:5000/submit-quiz", json=quiz_data)
        if response.ok:
           print("✅ Quiz successfully sent!")
           print(file)
        else:
            print("❌ Failed to send quiz:", response.status_code, response.text)
    #exit button
    tk.Button(scrollable, text="back", command= lambda: show_main_menu(root)).pack()

def show_manage_quiz_screen(root):

    for widget in root.winfo_children():
        widget.destroy()
    scrollable = logic.make_scrollable_frame(root)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(base_dir, "quizzes")
    file_list = [f for f in os.listdir(folder_path) if f.endswith('.json')]

    def selected_file(file_list, i):
        selected_file = file_list[i]
        print(selected_file)
        return selected_file
    
    for i, file in enumerate(file_list):
        file_str = file.replace(".json", "")

        # Frame for each file row
        file_frame = tk.Frame(scrollable, pady=5, padx=10, bd=1, relief="groove")
        file_frame.pack(fill="x", padx=20, pady=10)

        # File name label
        name_label = tk.Label(file_frame, text=file_str, font=("Arial", 12))
        name_label.pack(side="left", padx=(5, 20))

        # Button group on the right
        button_frame = tk.Frame(file_frame)
        button_frame.pack(side="right")

        edit_btn = tk.Button(button_frame, text="Edit", width=8,
                             command=lambda i=i: manage_edit_screen(root, selected_file(file_list, i)))
        edit_btn.pack(side="left", padx=(0, 5))

        delete_btn = tk.Button(button_frame, text="Delete", width=8,
                               command=lambda i=i: manage_delete_confirm(root, selected_file(file_list, i)))
        delete_btn.pack(side="left")

    def manage_delete_confirm(root, selected):
        selected_filepath_locaction = os.path.join(base_dir, "quizzes", selected)
        uiFunctions.ask_delete_permission(root, selected_filepath_locaction)
         
    
    def manage_edit_screen(root, selected,):
        selected_filepath_locaction = os.path.join(base_dir, "quizzes", selected)
        def load_json(selected_filepath_locaction):
            # Get base path relative to script location
            with open(selected_filepath_locaction, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        data = load_json(selected_filepath_locaction)
        render_edit(root ,selected_filepath_locaction, data)
    #exit button
    tk.Button(scrollable, text="back", command= lambda: show_main_menu(root)).pack()

    def render_edit(root, path, json):

        for widget in root.winfo_children():
            widget.destroy()
        scrollable = logic.make_scrollable_frame(root)
        text_font = tkfont.Font(family="Arial", size=11)

        # -- Title & Description Section --
        meta_frame = tk.LabelFrame(scrollable, text="Quiz Info", padx=10, pady=10, font=("Arial", 12, "bold"))
        meta_frame.pack(padx=20, pady=(20, 10), fill="x")

        # Title
        tk.Label(meta_frame, text="Edit Title:", font=("Arial", 11)).pack(anchor="w", pady=(0, 5))
        title_box = tk.Text(meta_frame, height=1, width=60, wrap="word", bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
        title_box.insert("1.0", json["title"])
        title_box.pack(fill="x")
        title_box.bind("<KeyRelease>", lambda event: logic.auto_resize_textbox(title_box, text_font))

        # Description
        tk.Label(meta_frame, text="Edit Description:", font=("Arial", 11)).pack(anchor="w", pady=(10, 5))
        desc_box = tk.Text(meta_frame, height=1, width=60, wrap="word", bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
        desc_box.insert("1.0", json["description"])
        desc_box.pack(fill="x")
        desc_box.bind("<KeyRelease>", lambda event: logic.auto_resize_textbox(desc_box, text_font))

        # -- Parse counts --
        ques_count = len(json["questions"])
        choice_count = len(json["questions"]["question 1"]["options"])
        answers = len(json["answers"])

        ques_text = []
        ques_options = []
        answer_text = []
        answer_conditions = []

        # -- Questions Section --
        for i in range(ques_count):
            q_frame = tk.LabelFrame(scrollable, text=f"Question {i + 1}", padx=10, pady=10, font=("Arial", 11, "bold"))
            q_frame.pack(padx=20, pady=15, fill="x", expand=True)

            # Question Text
            tk.Label(q_frame, text="Question Text:", font=("Arial", 10)).pack(anchor="w", pady=(0, 5))
            present_ques_text = tk.Text(q_frame, height=1, width=60, wrap="word", bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
            present_ques_text.insert("1.0", json["questions"][f"question {i + 1}"]["text"])
            present_ques_text.pack(fill="x")
            present_ques_text.bind("<KeyRelease>", lambda event, box=present_ques_text: logic.auto_resize_textbox(box, text_font))
            ques_text.append(present_ques_text)

            # Options
            ques_options_for_this_question = []
            for c in range(choice_count):
                opt_frame = tk.Frame(q_frame)
                opt_frame.pack(fill="x", padx=20, pady=8)

                tk.Label(opt_frame, text=f"Option {c + 1}:", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
                present_choice_text = tk.Text(opt_frame, height=1, width=50, wrap="word", bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
                present_choice_text.grid(row=0, column=1, padx=(10, 0), sticky="w")
                present_choice_text.insert("1.0", json["questions"][f"question {i + 1}"]["options"][f"option {c + 1}"]["text"])
                present_choice_text.bind("<KeyRelease>", lambda event, box=present_choice_text: logic.auto_resize_textbox(box, text_font))

                tk.Label(opt_frame, text="Points:", font=("Arial", 10)).grid(row=0, column=2, padx=(20, 5), sticky="e")
                present_choice_point = tk.Text(opt_frame, height=1, width=4, bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
                present_choice_point.grid(row=0, column=3, sticky="w")
                present_choice_point.insert("1.0", json["questions"][f"question {i + 1}"]["options"][f"option {c + 1}"]["point"])

                ques_option = {"text": present_choice_text, "point": present_choice_point}
                ques_options_for_this_question.append(ques_option)

            ques_options.append(ques_options_for_this_question)

        # -- Answers Section --
        for i in range(answers):
            a_frame = tk.LabelFrame(scrollable, text=f"Answer {i + 1}", padx=10, pady=10, font=("Arial", 11, "bold"))
            a_frame.pack(padx=20, pady=15, fill="x", expand=True)

            range_frame = tk.Frame(a_frame)
            range_frame.pack(anchor="w", pady=(0, 10))

            tk.Label(range_frame, text="From:", font=("Arial", 10)).grid(row=0, column=0, padx=(0, 5), sticky="w")
            answer_from = tk.Text(range_frame, height=1, width=4, bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
            answer_from.grid(row=0, column=1, padx=(0, 20), sticky="w")
            answer_from.insert("1.0", json["answers"][f"answer {i + 1}"]["conditions"]["from"])

            tk.Label(range_frame, text="To:", font=("Arial", 10)).grid(row=0, column=2, padx=(0, 5), sticky="w")
            answer_to = tk.Text(range_frame, height=1, width=4, bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
            answer_to.grid(row=0, column=3, sticky="w")
            answer_to.insert("1.0", json["answers"][f"answer {i + 1}"]["conditions"]["to"])

            # Answer Text
            tk.Label(a_frame, text="Answer Text:", font=("Arial", 10)).pack(anchor="w", padx=(0, 5), pady=(0, 5))
            present_answer_text = tk.Text(a_frame, height=2, width=60, wrap="word", bd=1, relief="solid", font=text_font, bg=root.cget("bg"))
            present_answer_text.insert("1.0", json["answers"][f"answer {i + 1}"]["text"])
            present_answer_text.pack(padx=10, fill="x")
            present_answer_text.bind("<KeyRelease>", lambda event, box=present_answer_text: logic.auto_resize_textbox(box, text_font))

            answer_score = {"from": answer_from, "to": answer_to}
            answer_conditions.append(answer_score)
            answer_text.append(present_answer_text)

               


        Save_button = tk.Button(scrollable, text="Save edits", command= lambda: uiFunctions.ask_edit_permission(root,
                                                                                            title_box.get("1.0", "end-1c"),
                                                                                            desc_box.get("1.0", "end-1c"),
                                                                                            logic.get_ques_text(ques_text),
                                                                                            logic.get_options_box(ques_options),
                                                                                            logic.get_answer_text(answer_text),
                                                                                            logic.get_answer_score(answer_conditions),
                                                                                            path))
        Save_button.pack() 
        
        #exit button
        tk.Button(scrollable, text="back", command= lambda: show_main_menu(root)).pack() 
