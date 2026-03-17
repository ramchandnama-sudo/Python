import tkinter as tk
from tkinter import messagebox
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("400x350")
        self.root.configure(bg="#2c3e50")  # Dark blue-grey background

        # Game state
        self.secret_number = random.randint(1, 100)
        self.attempts = 0

        # UI Layout
        self.title_label = tk.Label(root, text="Guess the Number!", font=("Helvetica", 20, "bold"), 
                                    bg="#2c3e50", fg="#ecf0f1", pady=20)
        self.title_label.pack()

        self.subtitle_label = tk.Label(root, text="Pick a number between 1 and 100", 
                                       font=("Helvetica", 12), bg="#2c3e50", fg="#bdc3c7")
        self.subtitle_label.pack()

        self.entry = tk.Entry(root, font=("Helvetica", 18), justify='center', width=10)
        self.entry.pack(pady=20)
        self.entry.bind('<Return>', lambda event: self.check_guess()) # Press Enter to submit

        self.guess_button = tk.Button(root, text="Submit Guess", command=self.check_guess, 
                                      font=("Helvetica", 12, "bold"), bg="#27ae60", fg="white", 
                                      padx=20, pady=10, relief="flat", cursor="hand2")
        self.guess_button.pack()

        self.feedback_label = tk.Label(root, text="", font=("Helvetica", 12, "italic"), 
                                       bg="#2c3e50", fg="#e74c3c", pady=20)
        self.feedback_label.pack()

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1

            if guess < 1 or guess > 100:
                self.feedback_label.config(text="Hey! Keep it between 1 and 100.", fg="#f1c40f")
            elif guess < self.secret_number:
                self.feedback_label.config(text="Too Low! Try a higher number.", fg="#3498db")
            elif guess > self.secret_number:
                self.feedback_label.config(text="Too High! Try a lower number.", fg="#e67e22")
            else:
                messagebox.showinfo("You Won!", f"🎉 Correct! The number was {self.secret_number}.\nIt took you {self.attempts} attempts.")
                self.reset_game()

            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid whole number.")

    def reset_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.feedback_label.config(text="Game Reset! Try again.", fg="#2ecc71")

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()
