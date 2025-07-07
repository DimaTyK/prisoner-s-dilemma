from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

player_choices = {}
app = FastAPI()

class ChoiceEnum(str, Enum):
    cooperate = "C"
    defec = "D"

class PlayerChoice(BaseModel):
    player_id: str
    choice: ChoiceEnum

@app.get("/")
def read_root():
    return {"message": "Welcome to prison's Dilemma game!"}

@app.post("/submit")
def submit_choice(choice: PlayerChoice):
    player_choices[choice.player_id] = choice.choice
    
    if len(player_choices) == 2:
        p1_id, p2_id = list(player_choices.keys())
        p1_choice = player_choices[p1_id]
        p2_choice = player_choices[p2_id]

        payoffs = {
            ("C", "C"): (3, 3),
            ("C", "D"): (0, 5),
            ("D", "C"): (5, 0),
            ("D", "D"): (1, 1),
        }
        results = payoffs[(p1_choice, p2_choice)]

        player_choices.clear()

        return {
            "player_1": {"id":p1_id, "choice": p1_choice, "score": results[0]},
            "player_2": {"id":p2_id, "choice": p2_choice, "score": results[1]},
        }
    else:
        return {"messege": "Waiting for the other player..."}
        
