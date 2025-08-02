import tkinter as tk
from tkinter import font as tkfont
import logic
import uiFunctions
import requests
import os
import json


def start_ui():
    root = tk.Tk()
    root.title("Quiz Maker ver-0.1")
    show_main_menu(root)
    root.geometry("800x600")
    root.mainloop()
    
def show_main_menu(root):
    for widget in root.winfo_children():
        widget.destroy()
    button_new = tk.Button(root, text="New Quiz", width=25, command=lambda: show_new_quiz_screen(root))
    button_new.pack()
    button_manage = tk.Button(root, text="Manage Quiz", width=25, command=lambda: show_manage_quiz_screen(root))
    button_manage.pack()
    button_upload = tk.Button(root, text="Upload Quiz", width=25, command=lambda: show_upload_quiz_screen(root))
    button_upload.pack()
    button_exit = tk.Button(root, text="Exit", width=25, command=exit)
    button_exit.pack()

def show_new_quiz_screen(root):
    
    for widget in root.winfo_children():
        widget.destroy()
    scrollable = logic.make_scrollable_frame(root)

    text_font = tkfont.Font(family="Arial", size=11)

    # Title
    label = tk.Label(scrollable, text="Enter Title:", font=("Arial", 12))
    label.pack(anchor="w", padx=(20, 0), pady=(20, 5))

    title_box = tk.Text(scrollable,
                        height=1,
                        width=60,
                        wrap="word",
                        bd=1,
                        relief="solid",
                        font=text_font,
                        bg=root.cget("bg"))
    title_box.pack(padx=20, fill="x")
    title_box.bind("<KeyRelease>", lambda event: logic.auto_resize_textbox(title_box, text_font))

    # Description
    label = tk.Label(scrollable, text="Enter Description:", font=("Arial", 12))
    label.pack(anchor="w", padx=(20, 0), pady=(20, 5))

    desc_box = tk.Text(scrollable,
                       height=1,
                       width=60,
                       wrap="word",
                       bd=1,
                       relief="solid",
                       font=text_font,
                       bg=root.cget("bg"))
    desc_box.pack(padx=20, fill="x")
    desc_box.bind("<KeyRelease>", lambda event: logic.auto_resize_textbox(desc_box, text_font))

    # Button inside its own Frame with left-only padding
    button_frame = tk.Frame(scrollable)
    button_frame.pack(anchor="w", padx=(20, 0), pady=(10, 0))

    #add button
    add_button = tk.Button(button_frame, text="+", width=1, height=1, command= lambda: add_questions_button_onlcick(root))
    add_button.pack()
    
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
            
            label = tk.Label(scrollable, text=f"-Question number {i + 1}:", font=("Arial", 12))
            label.pack(anchor="w", padx=(20, 0), pady=(20, 5))

            present_ques_text = tk.Text(scrollable,
                                height=1,
                                width=60,
                                wrap="word",
                                bd=1,
                                relief="solid",
                                font=text_font,
                                bg=root.cget("bg"))
            present_ques_text.pack(padx=20, fill="x")
            present_ques_text.bind("<KeyRelease>", lambda event, box=present_ques_text: logic.auto_resize_textbox(box, text_font))
            
            ques_text.append(present_ques_text)
            ques_options_for_this_question = []
             
            for c in range(choice_count):
               
                ques_option = {}
                label = tk.Label(scrollable, text=f".Option number {c + 1}:", font=("Arial", 12))
                label.pack(anchor="w", padx=(20, 0), pady=(20, 5))

                present_choice_text = tk.Text(scrollable,
                                    height=1,
                                    width=60,
                                    wrap="word",
                                    bd=1,
                                    relief="solid",
                                    font=text_font,
                                    bg=root.cget("bg"))
                present_choice_text.pack(padx=20, fill="x")
                present_choice_text.bind("<KeyRelease>", lambda event, box=present_choice_text: logic.auto_resize_textbox(box, text_font))

                present_choice_point = tk.Text(scrollable,
                                                height=1,
                                                width=2,
                                                bd=1,
                                                relief="solid",
                                                font=text_font,
                                                bg=root.cget("bg"))
                present_choice_point.pack()
               

                ques_option["text"] = present_choice_text
                ques_option["point"] = present_choice_point
                ques_options_for_this_question.append(ques_option)
            ques_options.append(ques_options_for_this_question)
        
        #render answer/points
        for i in range(answers):
            answer_score = {}
                
            tk.Label(scrollable, text=f"-Answer number {i + 1}:", font=("Arial", 12)).pack(anchor="w", padx=(20, 0), pady=(20, 5))
            tk.Label(scrollable, text=f".From: ", font=("Arial", 12)).pack(anchor="w", padx=(20, 0), pady=(20, 5))
            answer_from = tk.Text(scrollable,
                                            height=1,
                                            width=2,
                                            bd=1,
                                            relief="solid",
                                            font=text_font,
                                            bg=root.cget("bg"))
            answer_from.pack()
            tk.Label(scrollable, text=f".To: ", font=("Arial", 12)).pack(anchor="w", padx=(20, 0), pady=(20, 5))
            answer_to = tk.Text(scrollable,
                                                    height=1,
                                                    width=2,
                                                    bd=1,
                                                    relief="solid",
                                                    font=text_font,
                                                    bg=root.cget("bg"))
            answer_to.pack()

            present_answer_text = tk.Text(scrollable,
                                    height=50,
                                    width=60,
                                    wrap="word",
                                    bd=1,
                                    relief="solid",
                                    font=text_font,
                                    bg=root.cget("bg"))
            present_answer_text.pack(padx=20, fill="x")
            present_answer_text.bind("<KeyRelease>", lambda event, box=present_answer_text: logic.auto_resize_textbox(box, text_font))
                
            answer_score["from"] = answer_from
            answer_score["to"] = answer_to
                
            answer_conditions.append(answer_score)
            answer_text.append(present_answer_text)
            print(f"ui answer text: {answer_text}")
            print(f"ui answer conditions: {answer_conditions}")   


            Save_button = tk.Button(scrollable, text="Save", command= lambda: logic.new_save_button(title_box.get("1.0", "end-1c"),
                                                                                            desc_box.get("1.0", "end-1c"),
                                                                                            logic.get_ques_text(ques_text),
                                                                                            logic.get_options_box(ques_options),
                                                                                            logic.get_answer_text(answer_text),
                                                                                            logic.get_answer_score(answer_conditions)))
            Save_button.pack()  

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
        tk.Button(scrollable, text=file_str, command=lambda i=i: upload_ask_confirm(root, selected_file(file_list, i))).pack()

    def upload_ask_confirm(root, selected):
        
        root_up_ask = tk.Toplevel(root)
        root_up_ask.title("comfirm")
        root_up_ask.geometry("300x200")
            
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
        tk.Label(scrollable, text=file_str, font=("Arial", 12)).pack()
        tk.Button(scrollable, text="edit", command=lambda i=i: manage_edit_screen(root, selected_file(file_list, i))).pack()
        tk.Button(scrollable, text="delete", command=lambda i=i: manage_delete_confirm(root, selected_file(file_list, i))).pack()

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

        # Title
        tk.Label(scrollable, text="Edit Title:", font=("Arial", 12)).pack(anchor="w", padx=(20, 0), pady=(20, 5))
       

        title_box = tk.Text(scrollable,
                            height=1,
                            width=60,
                            wrap="word",
                            bd=1,
                            relief="solid",
                            font=text_font,
                            bg=root.cget("bg"))
        #insert default
        title_box.insert("1.0", json["title"])
        title_box.pack(padx=20, fill="x")
        title_box.bind("<KeyRelease>", lambda event: logic.auto_resize_textbox(title_box, text_font))

        # Description
        tk.Label(scrollable, text="Enter Description:", font=("Arial", 12)).pack(anchor="w", padx=(20, 0), pady=(20, 5))
        

        desc_box = tk.Text(scrollable,
                        height=1,
                        width=60,
                        wrap="word",
                        bd=1,
                        relief="solid",
                        font=text_font,
                        bg=root.cget("bg"))
        #insert default
        desc_box.insert("1.0", json["description"])
        desc_box.pack(padx=20, fill="x")
        desc_box.bind("<KeyRelease>", lambda event: logic.auto_resize_textbox(desc_box, text_font))

        ##render lists section##

        ques_count = len(json["questions"])
        choice_count = len(json["questions"]["question 1"]["options"])
        answers = len(json["answers"])

        #render ques/opt

        ques_text = []
        ques_options = []
        
        answer_text = []
        answer_conditions = []

        for i in range(ques_count):
            
            label = tk.Label(scrollable, text=f"-Question number {i + 1}:", font=("Arial", 12))
            label.pack(anchor="w", padx=(20, 0), pady=(20, 5))

            present_ques_text = tk.Text(scrollable,
                                height=1,
                                width=60,
                                wrap="word",
                                bd=1,
                                relief="solid",
                                font=text_font,
                                bg=root.cget("bg"))
            #insert default
            present_ques_text.insert("1.0", json["questions"][f"question {i + 1}"]["text"])
            present_ques_text.pack(padx=20, fill="x")
            present_ques_text.bind("<KeyRelease>", lambda event, box=present_ques_text: logic.auto_resize_textbox(box, text_font))
            
            ques_text.append(present_ques_text)
            ques_options_for_this_question = []
             
            for c in range(choice_count):
               
                ques_option = {}
                label = tk.Label(scrollable, text=f".Option number {c + 1}:", font=("Arial", 12))
                label.pack(anchor="w", padx=(20, 0), pady=(20, 5))

                present_choice_text = tk.Text(scrollable,
                                    height=1,
                                    width=60,
                                    wrap="word",
                                    bd=1,
                                    relief="solid",
                                    font=text_font,
                                    bg=root.cget("bg"))
                present_choice_text.pack(padx=20, fill="x")
                #insert default
                present_choice_text.insert("1.0", json["questions"][f"question {i + 1}"]["options"][f"option {c + 1}"]["text"])
                present_choice_text.bind("<KeyRelease>", lambda event, box=present_choice_text: logic.auto_resize_textbox(box, text_font))

                present_choice_point = tk.Text(scrollable,
                                                height=1,
                                                width=2,
                                                bd=1,
                                                relief="solid",
                                                font=text_font,
                                                bg=root.cget("bg"))
                #insert default
                present_choice_point.insert("1.0", json["questions"][f"question {i + 1}"]["options"][f"option {c + 1}"]["point"])
                present_choice_point.pack()
               

                ques_option["text"] = present_choice_text
                ques_option["point"] = present_choice_point
                ques_options_for_this_question.append(ques_option)
            ques_options.append(ques_options_for_this_question)
        
        #render answer/points
        for i in range(answers):
            answer_score = {}
                
            tk.Label(scrollable, text=f"-Answer number {i + 1}:", font=("Arial", 12)).pack(anchor="w", padx=(20, 0), pady=(20, 5))
            tk.Label(scrollable, text=f".From: ", font=("Arial", 12)).pack(anchor="w", padx=(20, 0), pady=(20, 5))
            answer_from = tk.Text(scrollable,
                                            height=1,
                                            width=2,
                                            bd=1,
                                            relief="solid",
                                            font=text_font,
                                            bg=root.cget("bg"))
            #insert default
            answer_from.insert("1.0", json["answers"][f"answer {i + 1}"]["conditions"]["from"])
            answer_from.pack()
            tk.Label(scrollable, text=f".To: ", font=("Arial", 12)).pack(anchor="w", padx=(20, 0), pady=(20, 5))
            answer_to = tk.Text(scrollable,
                                                    height=1,
                                                    width=2,
                                                    bd=1,
                                                    relief="solid",
                                                    font=text_font,
                                                    bg=root.cget("bg"))
            #insert default
            answer_to.insert("1.0", json["answers"][f"answer {i + 1}"]["conditions"]["to"])
            answer_to.pack()

            present_answer_text = tk.Text(scrollable,
                                    height=50,
                                    width=60,
                                    wrap="word",
                                    bd=1,
                                    relief="solid",
                                    font=text_font,
                                    bg=root.cget("bg"))
            #insert default
            present_answer_text.insert("1.0", json["answers"][f"answer {i + 1}"]["text"])
            present_answer_text.pack(padx=20, fill="x")
            present_answer_text.bind("<KeyRelease>", lambda event, box=present_answer_text: logic.auto_resize_textbox(box, text_font))
                
            answer_score["from"] = answer_from
            answer_score["to"] = answer_to
                
            answer_conditions.append(answer_score)
            answer_text.append(present_answer_text)
            print(f"ui answer text: {answer_text}")
            print(f"ui answer conditions: {answer_conditions}")   


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
        
            

            
        

    

