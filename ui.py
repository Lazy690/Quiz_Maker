import tkinter as tk
from tkinter import font as tkfont
import logic 

def start_ui():
    root = tk.Tk()
    root.title("Quiz Maker ver-0.1")
    show_main_menu(root)
    root.geometry("800x600")
    root.mainloop()
    
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

def show_main_menu(root):
    
    button_new = tk.Button(root, text="New Quiz", width=25, command=lambda: show_new_quiz_screen(root))
    button_new.pack()
    button_manage = tk.Button(root, text="Manage Quiz", width=25)
    button_manage.pack()
    button_upload = tk.Button(root, text="Upload Quiz", width=25)
    button_upload.pack()
    button_exit = tk.Button(root, text="Exit", width=25, command=exit)
    button_exit.pack()

def show_new_quiz_screen(root):
    
    for widget in root.winfo_children():
        widget.destroy()
    scrollable = make_scrollable_frame(root)

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
    title_box.bind("<KeyRelease>", lambda event: auto_resize_textbox(title_box, text_font))

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
    desc_box.bind("<KeyRelease>", lambda event: auto_resize_textbox(desc_box, text_font))

    # Button inside its own Frame with left-only padding
    button_frame = tk.Frame(scrollable)
    button_frame.pack(anchor="w", padx=(20, 0), pady=(10, 0))
    add_button = tk.Button(button_frame, text="+", width=1, height=1, command= lambda: add_button_onlcick(root))
    add_button.pack()

    def collect_values(**kwargs):
        return kwargs
    
    def present_questions_loop(data, root):
        
        
        def get_header():
            header = []
            header.append(title_box.get("1.0", "end-1c"))
            header.append(desc_box.get("1.0", "end-1c"))
            return header
        def get_big_dick():
            for i in range(ques_count):
                questions_dick[f"question {i + 1}"] = {}

                text = ques_text[i].get("1.0", "end-1c")
                
                questions_dick[f"question {i + 1}"]["text"] = text
                questions_dick[f"question {i + 1}"]["options"] = {}

                for c in range(choice_count):

                    opt = ques_options[i][c].get("1.0", "end-1c")
                    questions_dick[f"question {i + 1}"]["options"][f"option {c + 1}"] = opt
            return questions_dick

        ques_count = data["questions"]
        choice_count = data["choices"]

        questions_dick = {}
        ques_text = []
        ques_options = []
        

        for i in range(ques_count):
            
            ques_option = []

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
            present_ques_text.bind("<KeyRelease>", lambda event, box=present_ques_text: auto_resize_textbox(box, text_font))
            
            ques_text.append(present_ques_text)

            
            for c in range(choice_count):
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
                present_choice_text.bind("<KeyRelease>", lambda event, box=present_choice_text: auto_resize_textbox(box, text_font))
                ques_option.append(present_choice_text)
            ques_options.append(ques_option)
        
        Save_button = tk.Button(scrollable, text="Save", command= lambda: new_save_button())
        Save_button.pack()
                
        def new_save_button():
            header = get_header()
            content = get_big_dick()
            save_json(construct_dictionary(header, content))
            

            
        

    def add_button_onlcick(root):
        
        root_add = tk.Topleverl(root)
        root_add.title("Add questions")
        root_add.geometry("300x200")

        label_ques = tk.Label(root_add, text="How many questions?: ", font=("Arial", 12))
        label_ques.pack()
        entry_ques = tk.Entry(root_add)
        entry_ques.pack()

        label_choice = tk.Label(root_add, text="How many choices per question?: ", font=("Arial", 12))
        label_choice.pack()
        entry_choice = tk.Entry(root_add)
        entry_choice.pack()

        tk.Button(root_add, text="Accept", command=lambda:  present_questions_loop(collect_values(questions = int(entry_ques.get()), choices = int(entry_choice.get())), root)).pack()
        



        


