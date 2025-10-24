import tkinter as tk
from tkinter import messagebox
import random

# -------------------------------
# Code snippets with options
# -------------------------------
code_snippets = [
    {"snippet": "print(2 + 3 * 2)", "options": ["8", "10", "12", "7"], "answer": "8"},
    {"snippet": "print('Hello' + 'World')", "options": ["Hello World", "HelloWorld", "Hello+World", "Error"], "answer": "HelloWorld"},
    {"snippet": "print(len('Python'))", "options": ["5", "6", "7", "8"], "answer": "6"},
    {"snippet": "print(10 // 3)", "options": ["3", "3.33", "4", "10"], "answer": "3"},
    {"snippet": "print(5**2)", "options": ["10", "25", "32", "5"], "answer": "25"},
    {"snippet": "print([i for i in range(3)])", "options": ["[0,1,2]", "[1,2,3]", "[0,1,2,3]", "[1,2]"], "answer": "[0,1,2]"},
    {"snippet": "print('Python'[0])", "options": ["P", "y", "t", "h"], "answer": "P"},
    {"snippet": "print('Which one is immutable')", "options": ["Tuple", "List", "Dict", "Set"], "answer": "Tuple"},
    {"snippet": "print('index is start from)", "options": ["1", "2", "0", "none"], "answer": "0"},
    {"snippet": "print('What is the core data structure in NumPy?')", "options": ["list", "dict", "ndarray", "set"], "answer": "ndarray"}


    
]

random.shuffle(code_snippets)
current_index = 0
score = 0
time_limit = 20
time_left = time_limit

# -------------------------------
# Tkinter GUI
# -------------------------------
root = tk.Tk()
root.title("💻 Code Snippet Quiz")
root.geometry("800x500")
root.config(bg="#050542")

# Score & progress
score_label = tk.Label(root, text=f"Score: {score}", font=("Helvetica", 14), bg="#1E1E2F", fg="white")
score_label.pack(pady=10)

progress_frame = tk.Frame(root, bg="#1E1E2F")
progress_frame.pack()
progress_label = tk.Label(progress_frame, text=f"Question: {current_index + 1}/{len(code_snippets)}", font=("Helvetica", 12), bg="#1E1E2F", fg="white")
progress_label.pack(side="left", padx=10)

# Timer bar
timer_canvas = tk.Canvas(progress_frame, width=200, height=20, bg="#323248", highlightthickness=0)
timer_canvas.pack(side="left", padx=10)
timer_bar = timer_canvas.create_rectangle(0, 0, 200, 20, fill="#7E2029")

# Code snippet display (card style)
card_frame = tk.Frame(root, bg="#033D5F", padx=20, pady=20)
card_frame.pack(pady=20, fill="x", padx=50)
snippet_label = tk.Label(card_frame, text="", font=("Consolas", 16, "italic"), wraplength=700, bg="#2E2E3E", fg="#FFD700")
snippet_label.pack()

# Options
selected_option = tk.StringVar()
option_buttons = []

def on_enter(e):
    e.widget.config(bg="#761200")

def on_leave(e):
    e.widget.config(bg="#BC0061")

for i in range(4):
    btn = tk.Radiobutton(root, text="", variable=selected_option, value="", font=("Arial", 14),
                         bg="#A78E12", fg="white", selectcolor="#FF4500", width=25, pady=10)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.pack(pady=5)
    option_buttons.append(btn)

# -------------------------------
# Timer Function
# -------------------------------
def countdown():
    global time_left
    if time_left > 0:
        width = int((time_left / time_limit) * 200)
        timer_canvas.coords(timer_bar, 0, 0, width, 20)
        time_left -= 1
        root.after(1000, countdown)
    else:
        messagebox.showinfo("Time's up!", f"Correct answer: {code_snippets[current_index]['answer']}")
        next_question()

# -------------------------------
# Load Question
# -------------------------------
def load_question():
    global current_index, time_left
    if current_index < len(code_snippets):
        q = code_snippets[current_index]
        snippet_label.config(text=q["snippet"])
        options = q["options"]
        random.shuffle(options)
        for btn, option in zip(option_buttons, options):
            btn.config(text=option, value=option, bg="#323248")
        selected_option.set(None)
        progress_label.config(text=f"Question: {current_index + 1}/{len(code_snippets)}")
        time_left = time_limit
        countdown()
    else:
        message = f"🏆 Quiz Completed!\nYour final score: {score}/{len(code_snippets)}"
        if score == len(code_snippets):
            message += "\nPerfect Score! 🎉"
        elif score >= len(code_snippets)//2:
            message += "\nGood Job! 👍"
        else:
            message += "\nKeep Practicing! 💪"
        messagebox.showinfo("Result", message)
        root.destroy()

# -------------------------------
# Check Answer
# -------------------------------
def check_answer(answer):
    global score
    correct_answer = code_snippets[current_index]["answer"]
    if answer == correct_answer:
        score += 1
        option_buttons[[b["value"] for b in option_buttons].index(answer)].config(bg="#00FF00")  # green
        root.after(500, next_question)
    else:
        # Highlight wrong selection red and correct green
        for btn in option_buttons:
            if btn.cget("text") == answer:
                btn.config(bg="#EC1B1B")
            elif btn.cget("text") == correct_answer:
                btn.config(bg="#00FF00")
        root.after(1000, next_question)

def next_question():
    global current_index
    current_index += 1
    score_label.config(text=f"Score: {score}")
    load_question()

# Submit Button
submit_btn = tk.Button(root, text="Submit Answer", command=lambda: check_answer(selected_option.get()),
                       font=("Arial Rounded MT Bold", 14), bg="#7E9A19", fg="white", width=22, pady=15)
submit_btn.pack(pady=20)

# Start quiz
load_question()
root.mainloop()