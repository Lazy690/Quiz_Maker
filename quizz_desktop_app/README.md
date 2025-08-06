pyinstaller --onefile --add-data "quizzes:quizzes" --add-data ".env:." --add-data "assets:assets" --hidden-import "PIL._tkinter_finder" main.py

windows:
pyinstaller --onefile --add-data "quizzes;quizzes" --add-data ".env;." --add-data "assets;assets" --hidden-import "PIL._tkinter_finder" main.py