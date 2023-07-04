import tkinter as tk
from tkinter import filedialog
import json
import pandas as pd
import matplotlib as plt

questions = []
current_question = 0
score = 0
quiz_loaded = False
user_responses = []


import json

def upload():
    file_path = filedialog.askopenfilename(title="Select Sample Questions File", filetypes=[("Text Files", "*.txt")])
    
    if file_path:
        with open(file_path, 'r') as file:
            sample_data = file.readlines()

        questions = []
        current_question = None
        for line in sample_data:
            line = line.strip()
            if line.startswith("Q:"):
                if current_question is not None:
                    questions.append(current_question)
                current_question = {"ques": line[2:], "answ": [], "ans": [], "choices": []}
            elif line.startswith("A:"):
                current_question["answ"].append(line[2:])
            elif line.startswith("C:"):
                current_question["choices"].append(line[2:])
            elif line.startswith("Correct:"):
                correct_answers = line[8:].split(",")
                current_question["ans"] = [int(answer.strip()) for answer in correct_answers]

        if current_question is not None:
            questions.append(current_question)

        quiz_data = {"questions": questions}

        with open('quiz.json', 'w') as json_file:
            json.dump(quiz_data, json_file, indent=4)
            
        print("Quiz uploaded successfully!")


def load_quiz():
    global quiz_loaded
    file_path = filedialog.askopenfilename(title="Select Quiz JSON file", filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path) as file:
            quiz_data = json.load(file)
            global questions
            questions = quiz_data["questions"]

        btn_load_quiz.configure(state=tk.DISABLED)
        btn_next.configure(state=tk.NORMAL)
        next_question()

        quiz_loaded = True

def next_question():
    global current_question
    if current_question < len(questions):
        question = questions[current_question]
        lbl_question.configure(text=question["ques"])

        options = question["answ"]
        for i, option in enumerate(options):
            btn_options[i].configure(text=option, state=tk.NORMAL)

        current_question += 1
    else:
        display_scorecard()
        perform_analysis()

def check_answer(selected_option):
    question = questions[current_question - 1]
    correct_answers = question["ans"]

    global score
    if selected_option in correct_answers:
        score += 1

    user_responses.append({"question": question["ques"], "selected_option": selected_option, "correct": selected_option in correct_answers})

    for btn in btn_options:
        btn.configure(state=tk.DISABLED)

    next_question()

def display_scorecard():
    lbl_question.configure(text=f"Quiz Completed!\nYour score: {score}/{len(questions)}")
    btn_next.configure(state=tk.DISABLED)

def perform_analysis():
    data = pd.DataFrame(user_responses)
    
    accuracy = score / len(questions) * 100
    
    accuracy_per_question = data.groupby("question")["correct"].mean() * 100
    plt.figure(figsize=(7, 6))
    plt.bar(accuracy_per_question.index, accuracy_per_question)
    plt.xlabel("Question")
    plt.ylabel("Accuracy (%)")
    plt.title("Accuracy per Question")
    plt.xticks(rotation=90)
    plt.show()

root = tk.Tk()
root.title("Quiz App")
root.geometry("400x400")
root.config(bg='light goldenrod yellow')

lbl_heading = tk.Label(root, text='Quiz App', wraplength=200)
lbl_heading.pack()

lbl_question = tk.Label(root, text="", wraplength=380)
lbl_question.pack(pady=20)

btn_options = []
for i in range(4):
    btn = tk.Button(root, text="", width=30, command=lambda i=i: check_answer(i), state=tk.DISABLED)
    btn.pack(pady=5)
    btn_options.append(btn)

btn_load_quiz = tk.Button(root, text="Load Json File Quiz", command=load_quiz)
btn_load_quiz.pack(pady=10)

btn_next = tk.Button(root, text="Next Question", command=next_question)
btn_next.pack(pady=5)
btn_next.configure(state=tk.DISABLED)

play_again = tk.Button(root, text="Play Again", command=lambda: [play_again(), perform_analysis()])
play_again.pack(pady=5)

btn_load_quiz = tk.Button(root, text="Upload Text File Quiz", command=upload)
btn_load_quiz.pack(pady=10)


def play_again():
    global quiz_loaded, current_question, score, user_responses
    quiz_loaded = False
    current_question = 0
    score = 0
    user_responses = []
    lbl_question.configure(text="")
    for btn in btn_options:
        btn.configure(text="", state=tk.DISABLED)
    btn_load_quiz.configure(state=tk.NORMAL)
    btn_next.configure(state=tk.DISABLED)

import numpy as np
from sklearn.metrics import balanced_accuracy_score
actual = np.repeat([1, 0], repeats=[20, 380])
pred = np.repeat([1, 0, 1, 0], repeats=[15, 5, 5, 375])
balanced_accuracy_score(actual, pred)


root.mainloop()
