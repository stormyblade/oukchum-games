import pickle
import tkinter as tk
from tkinter import messagebox

# Sert à réinitialiser le leaderboard du Snake

def save_obj(obj, name ):
    with open(name, 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

dico = (load_obj("score.txt"))

print("Classement actuel : "+str(dico))
dico = {}
save_obj(dico, "score.txt")
dico = (load_obj("score.txt"))
print("Nouveau classement : "+str(dico))
message_box("Leaderboard Reset", "Successfully reset the Snake Leaderboard")