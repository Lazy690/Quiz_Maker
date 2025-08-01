import json
import os
import tkinter as tk

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
            print(f"get ques text: {question_list}")
            return question_list
        
def get_options_box(ques_options):
              
            options_list = []
            for i in ques_options: 
                options_for_question_list = []
                
                for c in i:
                    option = {}
                    option["text"] = (c["text"].get("1.0", "end-1c"))
                    option["point"] = (c["point"].get("1.0", "end-1c"))
                    options_for_question_list.append(option) 

                options_list.append(options_for_question_list)
                       
            print(f"get ques options: {options_list}")
            return options_list

def get_answer_text(answer_text):
            answers_text_list = []
            for i in range(len(answer_text)):
                answers_text_list.append(answer_text[i].get("1.0", "end-1c"))
            print(f"get answer text: {answers_text_list}")
            return answers_text_list

def get_answer_score(answer_score):
            answer_score_list = []  

            for i in answer_score:  
                score_list = {}
                 
                score_list["from"] = (i["from"].get("1.0", "end-1c")) 
                score_list["to"] = (i["to"].get("1.0", "end-1c"))   
                answer_score_list.append(score_list)  
            print(f"get answer score: {answer_score_list}")
            return answer_score_list



def construct_dictionary(title, description, questions, answers):
    package_json = {}

    package_json["title"] = title
    package_json["description"] = description

    package_json["questions"] = questions
    package_json["answers"] = answers
    return package_json


def save_json(package):
    filename = package["title"]

    # Get the absolute path to the current script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    quizzes_dir = os.path.join(base_dir, "quizzes")

    os.makedirs(quizzes_dir, exist_ok=True)

    filepath = os.path.join(quizzes_dir, "quiz_" + filename + ".json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(package, f, indent=4, ensure_ascii=False)

    print(f"Quiz saved to {filepath}")

def replace_json(package, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(package, f, ensure_ascii=False, indent=4)

def new_save_button(Title, Description, Questions, Options, Answers, Scores):

            title = Title
            description = Description
            questions = Questions
            options = Options
            answers = Answers
            scores = Scores


            questions_dick = {}
            answers_dick = {}

            def make_questions_dick(questions, options):
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

                print(f"questions final dictionary: {questions_dick}")
                return questions_dick            
            def make_answers_dick(answers, scores):
                #This makes the answers dictionary
                for i in range(len(answers)):
                    answers_dick[f"answer {i + 1}"] = {}
                    answers_dick[f"answer {i + 1}"]["text"] = answers[i]
                    answers_dick[f"answer {i + 1}"]["conditions"] = {}
                    
                    score = scores[i]

                    answers_dick[f"answer {i + 1}"]["conditions"]["from"] = score["from"]
                    answers_dick[f"answer {i + 1}"]["conditions"]["to"] =   score["to"]

                print(f"answers final dictionary: {answers_dick}")         
                return answers_dick

            save_json(construct_dictionary(title, description, make_questions_dick(questions, options), make_answers_dick(answers, scores)))  

def edit_save_button(Title, Description, Questions, Options, Answers, Scores, location):

            title = Title
            description = Description
            questions = Questions
            options = Options
            answers = Answers
            scores = Scores


            questions_dick = {}
            answers_dick = {}

            def make_questions_dick(questions, options):
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

                print(f"questions final dictionary: {questions_dick}")
                return questions_dick            
            def make_answers_dick(answers, scores):
                #This makes the answers dictionary
                for i in range(len(answers)):
                    answers_dick[f"answer {i + 1}"] = {}
                    answers_dick[f"answer {i + 1}"]["text"] = answers[i]
                    answers_dick[f"answer {i + 1}"]["conditions"] = {}
                    
                    score = scores[i]

                    answers_dick[f"answer {i + 1}"]["conditions"]["from"] = score["from"]
                    answers_dick[f"answer {i + 1}"]["conditions"]["to"] =   score["to"]

                print(f"answers final dictionary: {answers_dick}")         
                return answers_dick

            save_json(construct_dictionary(title, description, make_questions_dick(questions, options), make_answers_dick(answers, scores), location))  
     
        
        


    
