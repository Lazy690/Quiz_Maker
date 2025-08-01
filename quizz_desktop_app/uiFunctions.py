import tkinter as tk
from tkinter import font as tkfont
import logic
import requests
import os
import json

def present_edits_loop(root, json, location):
    for widget in root.winfo_children():
        widget.destroy()
    

    text_font = tkfont.Font(family="Arial", size=11)
    

    # Title
    label = tk.Label(root, text="Edit Title:", font=("Arial", 12))
    label.pack(anchor="w", padx=(20, 0), pady=(20, 5))

    title_box = tk.Text(root,
                        height=1,
                        width=60,
                        wrap="word",
                        bd=1,
                        relief="solid",
                        font=text_font,
                        bg=root.cget("bg"))
    #insert default text
    title_box.insert("1.0", json["title"])
    
    title_box.pack(padx=20, fill="x")
    title_box.bind("<KeyRelease>", lambda event: logic.auto_resize_textbox(title_box, text_font))
    
    # Description
    label = tk.Label(root, text="Edit Description:", font=("Arial", 12))
    label.pack(anchor="w", padx=(20, 0), pady=(20, 5))

    desc_box = tk.Text(root,
                       height=1,
                       width=60,
                       wrap="word",
                       bd=1,
                       relief="solid",
                       font=text_font,
                       bg=root.cget("bg"))
    desc_box.pack(padx=20, fill="x")
    #insert default text
    desc_box.insert("1.0", json["description"])
    desc_box.bind("<KeyRelease>", lambda event: logic.auto_resize_textbox(desc_box, text_font))

    ques_num = len(json["questions"])
    choice_num = len(json["questions"]["question 1"]["options"])
    answers_num = len(json["answers"])
    
    present_questions_loop(questions=ques_num, choices=choice_num)
    
    def present_questions_loop(**data):
        
        ques_count = data["questions"]
        choice_count = data["choices"]

        
        ques_text = []
        ques_options = []
        

        for i in range(ques_count):
            
           

            label = tk.Label(root, text=f"- Edit question number {i + 1}:", font=("Arial", 12))
            label.pack(anchor="w", padx=(20, 0), pady=(20, 5))

            present_ques_text = tk.Text(root,
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
                label = tk.Label(root, text=f".Option number {c + 1}:", font=("Arial", 12))
                label.pack(anchor="w", padx=(20, 0), pady=(20, 5))

                present_choice_text = tk.Text(root,
                                    height=1,
                                    width=60,
                                    wrap="word",
                                    bd=1,
                                    relief="solid",
                                    font=text_font,
                                    bg=root.cget("bg"))
                #insert default 
                present_choice_text.insert("1.0", json["questions"][f"question {i + 1}"]["options"][f"option {c + 1}"]["text"])

                present_choice_text.pack(padx=20, fill="x")
                present_choice_text.bind("<KeyRelease>", lambda event, box=present_choice_text: logic.auto_resize_textbox(box, text_font))

                present_choice_point = tk.Text(root,
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
        
        present_answers_loop(answers=answers_num)
        answer_text = []
        answer_conditions = []
        def present_answers_loop(**data):
            
            max_score = data["max_score"]
            answers = data["answers"]

            
            
            

            for i in range(answers):
                answer_score = {}
                
                tk.Label(root, text=f"-Edit answer number {i + 1}:", font=("Arial", 12)).pack(anchor="w", padx=(20, 0), pady=(20, 5))
                tk.Label(root, text=f".From: ", font=("Arial", 12)).pack(anchor="w", padx=(20, 0), pady=(20, 5))
                answer_from = tk.Text(root,
                                                    height=1,
                                                    width=2,
                                                    bd=1,
                                                    relief="solid",
                                                    font=text_font,
                                                    bg=root.cget("bg"))
                #insert default
                answer_from.insert("1.0", json["answers"][f"answer {i + 1}"]["conditions"]["from"])

                answer_from.pack()
                tk.Label(root, text=f".To: ", font=("Arial", 12)).pack(anchor="w", padx=(20, 0), pady=(20, 5))
                answer_to = tk.Text(root,
                                                    height=1,
                                                    width=2,
                                                    bd=1,
                                                    relief="solid",
                                                    font=text_font,
                                                    bg=root.cget("bg"))
                #insert default
                answer_to.insert("1.0", json["answers"][f"answer {i + 1}"]["conditions"]["to"])

                answer_to.pack()

                present_answer_text = tk.Text(root,
                                    height=50,
                                    width=60,
                                    wrap="word",
                                    bd=1,
                                    relief="solid",
                                    font=text_font,
                                    bg=root.cget("bg"))
                #insert default
                answer_from.insert("1.0", json["answers"][f"answer {i + 1}"]["text"])

                present_answer_text.pack(padx=20, fill="x")
                present_answer_text.bind("<KeyRelease>", lambda event, box=present_answer_text: logic.auto_resize_textbox(box, text_font))
                
                answer_score["from"] = answer_from
                answer_score["to"] = answer_to
                
                answer_conditions.append(answer_score)
                answer_text.append(present_answer_text)
            print(f"ui answer text: {answer_text}")
            print(f"ui answer conditions: {answer_conditions}") 

        

        
        Save_button = tk.Button(root, text="Save", command= lambda: logic.edit_save_button(title_box.get("1.0", "end-1c"),
                                                                                                desc_box.get("1.0", "end-1c"),
                                                                                                logic.get_ques_text(ques_text),
                                                                                                logic.get_options_box(ques_options),
                                                                                                logic.get_answer_text(answer_text),
                                                                                                logic.get_answer_score(answer_conditions),
                                                                                                location,
                                                                                                json))
        Save_button.pack() 
    