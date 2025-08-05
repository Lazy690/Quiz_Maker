import json
import os
import tkinter as tk
from tkinter import messagebox
import requests
from dotenv import load_dotenv


#break down new_save_button into smaller fucntions

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

def auto_resize_textbox(text_widget, text_font):
    content = text_widget.get("1.0", "end-1c")
    lines = content.split('\n')

    total_lines = 0
    for line in lines:
        pixel_width = text_font.measure(line)
        box_width = text_widget.winfo_width()
        if box_width <= 1:  # Widget might not be fully rendered yet
            continue
        wrapped_lines = max(1, int(pixel_width / box_width) + 1)
        total_lines += wrapped_lines

    text_widget.config(height=total_lines)

def get_ques_text(ques_text):
            question_list = []
            for i in range(len(ques_text)):
                question_list.append(ques_text[i].get("1.0", "end-1c"))
            
            return question_list
        
def get_options_box(ques_options, max_score):
              
            options_list = []
            biggest_points = []
            point_sum = []
            
            for i in ques_options: 
                options_for_question_list = []
                point = []
                for c in i:
                    option = {}
                    
                    
                    option["text"] = (c["text"].get("1.0", "end-1c"))
                    option["point"] = (c["point"].get("1.0", "end-1c"))
                    point.append(int((c["point"].get("1.0", "end-1c"))))
                    
                    options_for_question_list.append(option) 
                options_list.append(options_for_question_list)
                print(f"point {point}")
                biggest_points.append(max(point))
            
            print(f"biggest points {biggest_points}")
            
            if sum(biggest_points) > int(max_score):
                messagebox.showwarning("input error", f"The sum of the points cannot exeed max score: {max_score}")
            else:  
                return options_list

def get_answer_text(answer_text):
            answers_text_list = []
            for i in range(len(answer_text)):
                answers_text_list.append(answer_text[i].get("1.0", "end-1c"))
            
            return answers_text_list

def get_answer_score(answer_score):
            answer_score_list = []  

            for i in answer_score:  
                score_list = {}
                 
                score_list["from"] = (i["from"].get("1.0", "end-1c")) 
                score_list["to"] = (i["to"].get("1.0", "end-1c"))   
                answer_score_list.append(score_list)  
           
            return answer_score_list

def construct_dictionary(title, description, questions, options, answers, scores, max_score):
    
    

    def make_questions_dick(questions, options):
        questions_dick = {}
        #This makes the questions dictionary     
        for i in range(len(questions)):

            questions_dick[f"question {i + 1}"] = {}
            questions_dick[f"question {i + 1}"]["text"] = questions[i]
            questions_dick[f"question {i + 1}"]["options"] = {}
            opt_count = 0
            for option in options[i]:
                questions_dick[f"question {i + 1}"]["options"][f"option {opt_count + 1}"] = {}
                questions_dick[f"question {i + 1}"]["options"][f"option {opt_count + 1}"]["text"] = option["text"]
                questions_dick[f"question {i + 1}"]["options"][f"option {opt_count + 1}"]["point"] = option["point"]
                opt_count += 1

        return questions_dick   
             
    def make_answers_dick(answers, scores):
        answers_dick = {}
        #This makes the answers dictionary
        for i in range(len(answers)):
            answers_dick[f"answer {i + 1}"] = {}
            answers_dick[f"answer {i + 1}"]["text"] = answers[i]
            answers_dick[f"answer {i + 1}"]["conditions"] = {}
                        
            score = scores[i]

            answers_dick[f"answer {i + 1}"]["conditions"]["from"] = score["from"]
            answers_dick[f"answer {i + 1}"]["conditions"]["to"] =   score["to"]

        return answers_dick

    package_json = {}
    questions_dic = make_questions_dick(questions, options)
    answers_dic = make_answers_dick(answers, scores)
    package_json["title"] = title
    package_json["description"] = description
    package_json["max_score"] = max_score

    package_json["questions"] = questions_dic
    package_json["answers"] = answers_dic
    return package_json



    

##save buttons##
def new_save_button(title, description, questions, options, answers, scores, max_score):
    package = construct_dictionary(title, description, questions, options, answers, scores, max_score)
    save_json(package)

def edit_save_button(title, description, questions, options, answers, scores, max_score, path):
    package = construct_dictionary(title, description, questions, options, answers, scores, max_score)
    overwrite_json(package, path)  

##file management##

def save_json(package):
    filename = package["title"]

    # Get the absolute path to the current script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    quizzes_dir = os.path.join(base_dir, "quizzes")

    os.makedirs(quizzes_dir, exist_ok=True)

    filepath = os.path.join(quizzes_dir, "quiz_" + filename + ".json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(package, f, indent=4, ensure_ascii=False)
    messagebox.showinfo("Success", "Quiz saved successfully!")
    
def overwrite_json(package, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(package, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Success", "Edits saved successfully!")

def delete_json(path):
    if os.path.exists(path):
        os.remove(path)
        messagebox.showinfo("Success", "✅ Quiz successfully deleted!")
    else:
         print("file doesnt exist")

def upload_json(file, base_dir):
        title = file
        load_dotenv()  # loads .env

        upload_key = os.getenv("UPLOAD_KEY")
        def load_json(file):
            # Get base path relative to script location
            
            selected_filepath_locaction = os.path.join(base_dir, "quizzes", file)

            with open(selected_filepath_locaction, "r", encoding="utf-8") as f:
                data = json.load(f)
            

            return data
        quiz_data = load_json(title)

        response = requests.post("http://127.0.0.1:5000/submit-quiz", json=quiz_data, headers={"X-Upload-Key": upload_key})
        if response.ok:
           messagebox.showinfo("Success", "✅ Quiz successfully sent!")
           print(file)
        else:
            messagebox.showinfo("Failed", "❌ Failed to send quiz:")
            print("❌ Failed to send quiz:", response.status_code, response.text)
    
##Validate input##

def show_error(root, error): 
     #create window
        root_error = tk.Toplevel(root)
        root_error.title("error")
        root_error.geometry("300x250")
        
        tk.Label(error, text=error, font=("Arial", 12)).pack()
        
        def on_accept():
            root_error.destroy()

        tk.Button(root_error, text="back", command=lambda:  on_accept()).pack()
     
def validate_new(title, description, questions, options, answers, scores, max_score):
    
    points_sum = []
    for i in range(options):
        option = options[i]
        points_sum.append(option["point"])
        
    if sum(points_sum) > max_score:
            messagebox.showwarning("Invalid inputs","Sum of the points cannot exede the max score") 
    else:
        return new_save_button(title, description, questions, options, answers, scores)
