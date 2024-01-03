import random
from tkinter import *
from tkinter import messagebox
import pandas


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
# ---------------------------- Create New Flash Cards ------------------------------- #
try:
    data = pandas.read_csv("data/missed_words.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
except pandas.errors.EmptyDataError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_title_text, text="French", fill="black")
    canvas.itemconfig(canvas_word_text, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=canvas_fr_image)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_title_text, text="English", fill="white")
    canvas.itemconfig(canvas_word_text, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_image, image=canvas_en_image)


def is_know_word():
    global to_learn
    to_learn.remove(current_card)
    data_frame = pandas.DataFrame(to_learn)
    data_frame.to_csv("./data/missed_words.csv", index=False)
    if len(to_learn) < 1:
        answer = messagebox.askyesno("Success", "You have already learnt all words.\nDo you want to reply?")
        if not answer:
            window.destroy()
        else:
            to_learn = original_data.to_dict(orient="records")
            next_word()
    else:
        next_word()


def is_not_know_word():
    next_word()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Card")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_fr_image = PhotoImage(file="./images/card_front.png")
canvas_en_image = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=canvas_fr_image)
canvas_title_text = canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
canvas_word_text = canvas.create_text(400, 263, font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, border=0, activebackground=BACKGROUND_COLOR,
                      activeforeground=BACKGROUND_COLOR, command=is_not_know_word)
wrong_button.grid(row=1, column=0)

# Buttons
right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, border=0, activebackground=BACKGROUND_COLOR,
                      activeforeground=BACKGROUND_COLOR, command=is_know_word)
right_button.grid(row=1, column=1)

flip_timer = window.after(3000, flip_card)

next_word()


window.mainloop()
