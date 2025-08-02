import tkinter as tk
import logic

##ask permission buttons##

def ask_edit_permission(root, title, description, questions, options, answers, scores, path):
        
        #create window
        root_ask_per = tk.Toplevel(root)
        root_ask_per.title("Ask if sure")
        root_ask_per.geometry("300x100")
        
        tk.Label(root_ask_per, text="Are you sure you want to save edits?", font=("Arial", 12)).pack()

        tk.Button(root_ask_per, text="confirm", command= lambda: on_accept()).pack()
        tk.Button(root_ask_per, text="cancel", command= lambda: on_cancel()).pack()
        def on_accept():
            logic.edit_save_button(title, description, questions, options, answers, scores, path)
            root_ask_per.destroy()
        def on_cancel():
            root_ask_per.destroy()

def ask_delete_permission(root, path):
        
        #create window
        root_ask_per = tk.Toplevel(root)
        root_ask_per.title("Ask if sure")
        root_ask_per.geometry("300x100")
        
        tk.Label(root_ask_per, text="Are you sure you want delete this file?", font=("Arial", 12)).pack()

        tk.Button(root_ask_per, text="confirm", command= lambda: on_accept()).pack()
        tk.Button(root_ask_per, text="cancel", command= lambda: on_cancel()).pack()
        def on_accept():
            logic.delete_json(path)
            root_ask_per.destroy()
        def on_cancel():
            root_ask_per.destroy()
    
