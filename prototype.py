import sqlite3
from tkinter import *
from tkinter import messagebox
import statistics

class MentalPathway:
    def __init__(self, window):
        self.window = window
        self.window.title("Mental Pathway Quiz")
        self.window.geometry("960x720")
        self.window.configure(bg="black")
        self.labels = []  # Initialize labels list
        self.create_widgets()

    def create_widgets(self):
        self.questions = [
            "Question 1: How many meals do you approximately eat in a day?",
            "Question 2: How frequently do you find yourself stressed?",
            "Question 3: How often do you exercise?",
            "Question 4: How often do you think of self-harm?",
            "Question 5: Do you have difficulty doing day-to-day tasks?"
        ]
        self.answers = [
            ["1. Less than 2 meals", "2. 2-3 meals", "3. 3-4 meals", "4. 4-5 meals"],
            ["1. Never", "2. Rarely", "3. Sometimes", "4. Often", "5. Always"],
            ["1. 1-2 times a week", "2. 3-4 times a week", "3. 4-5 times a week", "4. 5-6 times a week", "5. 6-7 times a week"],
            ["1. Never", "2. Rarely", "3. Sometimes", "4. Often", "5. Always"],
            ["1. Never", "2. Rarely", "3. Sometimes", "4. Often", "5. Always"]
        ]
        self.results_of_questions = []
        for i in range(len(self.questions)):
            question_label = Label(self.window, text=self.questions[i], bg="black", fg="white")
            question_label.pack(anchor=W, padx=10, pady=5)
            self.labels.append(question_label)

            var = StringVar()
            var.set(self.answers[i][0])
            for answer in self.answers[i]:
                answer_radio = Radiobutton(self.window, text=answer, variable=var, value=answer)
                answer_radio.pack(anchor=W, padx=20)
            self.results_of_questions.append(var)

        submit_button = Button(self.window, text="Submit", command=self.submit_quiz)
        submit_button.pack(pady=10)

    def submit_quiz(self):
        responses = [var.get() for var in self.results_of_questions]

        # Calculate mood
        mood, _, foods = self.calculate_mood(responses)

        # Display result
        result_message = f"Based on your responses, you seem {mood}.\nHere are some foods you might like to improve your mood: {', '.join(foods)}"
        messagebox.showinfo("Result", result_message)

    def calculate_mood(self, responses):
        # Convert answers to numerical values
        converted_responses = []
        for response in responses:
            converted_responses.append(int(response.split('.')[0]))

        # Calculate average response
        average_response = statistics.mean(converted_responses)

        # Determine mood based on average response
        mood = ""
        foods = ["Dark Chocolate", "Strawberries", "Nuts", "Turkey", "Avocado", "Beef Liver", "Salmon", "Bananas", "Yogurt", "Quinoa", "Spinach", "Blueberries"]
        if average_response < 2.5:
            mood = "Scarlet"
            foods = foods[:3]
        elif 2.5 <= average_response < 3.5:
            mood = "Starky"
            foods = foods[3:6]
        elif 3.5 <= average_response < 4.5:
            mood = "Brave"
            foods = foods[6:9]
        else:
            mood = "QuickSilver"
            foods = foods[9:]

        return mood, converted_responses, foods

def main():
    root = Tk()
    app = MentalPathway(root)
    root.mainloop()

if __name__ == "__main__":
    main()
