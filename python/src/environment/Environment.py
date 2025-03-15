from enum import Enum 
from db.Database import Database
TOLERANCE = 1e-5

class Actions(Enum):
    UPVOTE = 0,
    DOWNVOTE = 1


class Environment:
    cls_name = "Environment"
    def __init__(self, db: Database, **config):
        self.config = config
        action_up, action_down = config["actions"]
        self.actions = {
            action_up : Actions.UPVOTE, 
            action_down : Actions.DOWNVOTE
        }

        reward_up, reward_down = config["rewards"]
        self.rewards = {
            Actions.UPVOTE : reward_up,
            Actions.DOWNVOTE : reward_down
        }

        self.render_mode = config["render_mode"]
        self.upvote_prob = config["likeness"]
        self.db = db
        self.validate_members()

    def validate_members(self)->None:
        cum_prob = 0
        for prob in self.upvote_prob.values():
            cum_prob += prob

        if not (cum_prob - TOLERANCE <= cum_prob <= cum_prob + TOLERANCE):
            print("[ERROR] validate_members(): Cumulative probability doesn't " 
                "equal to 1. ", end="")
            print(f"Equals to {cum_prob}")
            exit(1)

    def __repr__(self):
        # This dict is too long to display. Shorten it.
        upvote_prob_keys = list(self.upvote_prob.keys())
        upvote_prob_str = f"{upvote_prob_keys[0]}: {self.upvote_prob[upvote_prob_keys[0]]}, ..., {upvote_prob_keys[-1]}: {self.upvote_prob[upvote_prob_keys[-1]]}"

        rows = {
            "actions": self.actions,
            "rewards": self.rewards,
            "render_mode": self.render_mode,
            "upvote_prob": upvote_prob_str
        }

        max_length = max(len(f"{key}: {value}") for key, value in rows.items())
        title = f" {self.cls_name} "
        padding = (max_length - len(title)) // 2
        header = f"{'=' * padding}{title}{'=' * padding}"
        header = header.ljust(max_length, "=")

        formatted_rows = [f"{key}: {str(value).rjust(max_length - len(key) - 2)}" for key, value in rows.items()]
        return f"{header}\n" + "\n".join(formatted_rows) + f"\n{'=' * len(header)}"

