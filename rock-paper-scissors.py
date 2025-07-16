import tkinter as tk
import random

# Function to determine the winner
def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Scissors" and computer_choice == "Paper") or \
         (user_choice == "Paper" and computer_choice == "Rock"):
        return "You win!"
    else:
        return "You lose!"

# Function to play the game
def play_game(user_choice):
    computer_choice = random.choice(["Rock", "Paper", "Scissors"])
    result = determine_winner(user_choice, computer_choice)
    
    # Update the labels with the choices and result
    user_choice_label.config(text=f"Your choice: {user_choice}")
    computer_choice_label.config(text=f"Computer's choice: {computer_choice}")
    result_label.config(text=result)

    # Update scores
    if result == "You win!":
        global user_score
        user_score += 1
    elif result == "You lose!":
        global computer_score
        computer_score += 1

    score_label.config(text=f"Score - You: {user_score} | Computer: {computer_score}")

# Function to ask to play again
def play_again():
    play_again_response = tk.messagebox.askyesno("Play Again", "Do you want to play again?")
    if play_again_response:
        user_choice_label.config(text="")
        computer_choice_label.config(text="")
        result_label.config(text="")

# Initialize scores
user_score = 0
computer_score = 0

# Create the main window
root = tk.Tk()
root.title("Rock, Paper, Scissors Game")

# Create and place the widgets
instructions_label = tk.Label(root, text="Choose Rock, Paper, or Scissors:")
instructions_label.pack()

rock_button = tk.Button(root, text="Rock", command=lambda: play_game("Rock"))
rock_button.pack()

paper_button = tk.Button(root, text="Paper", command=lambda: play_game("Paper"))
paper_button.pack()

scissors_button = tk.Button(root, text="Scissors", command=lambda: play_game("Scissors"))
scissors_button.pack()

user_choice_label = tk.Label(root, text="")
user_choice_label.pack()

computer_choice_label = tk.Label(root, text="")
computer_choice_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()

score_label = tk.Label(root, text="Score - You: 0 | Computer: 0")
score_label.pack()


# Start the GUI event loop
root.mainloop()
