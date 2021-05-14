import pickle

# Sert à réinitialiser le leaderboard du Snake

def save_obj(obj, name ):
    with open(name, 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

dico = (load_obj("score.txt"))

print("Classement actuel : "+str(dico))
dico = {}
save_obj(dico, "score.txt")
dico = (load_obj("score.txt"))
print("Nouveau classement : "+str(dico))