from psycopg.rows import TupleRow
from utils.enums import Actions
from typing import List, Tuple
from db.Database import Database
from pathlib import Path

from utils.log import logger_builder

# [WARNING]: DO NOT REUSE THOSE VARIABLES, THOSE ARE MADE TO USE ONLY IN THIS
# FILE
TOLERANCE = 1e-3
logger = logger_builder(__name__, Path("resource/logs/"))


class Environment:
    cls_name = "Environment"

    def __init__(self, **full_config):
        env_config = full_config["env"]
        self._full_config = full_config
        action_up, action_down = env_config["actions"]
        self.actions = {action_up: Actions.UPVOTE, action_down: Actions.DOWNVOTE}
        self._db = Database(
            **full_config["db"], **full_config["paths"], **full_config["model"]
        )
        self._db.table_init()
        reward_up, reward_down = env_config["rewards"]
        self.rewards = {Actions.UPVOTE: reward_up, Actions.DOWNVOTE: reward_down}

        self.render_mode = env_config["render_mode"]
        self.upvote_prob = env_config["likeness"]

        self.last_genres: Tuple[str]
        self.current_episode: int = 0
        model_config = full_config["model"]
        self.nepisodes: int = model_config["nepisodes"]
        self.nactions: int = model_config["action_space_size"]
        self.batch: TupleRow | List[TupleRow]
        self.record_tracker = 1 << 31
        self.validate_members()

    def validate_members(self) -> None:
        cum_prob = 0
        for prob in self.upvote_prob.values():
            cum_prob += prob

        if not (1 - TOLERANCE <= cum_prob <= 1 + TOLERANCE):
            print(
                "[ERROR] validate_members(): Cumulative probability doesn't "
                "equal to 1. "
            )
            print(f"        {1 - TOLERANCE} <= {cum_prob} <= {1 + TOLERANCE} ")
            logger.error(
                "[ERROR] validate_members(): Cumulative probability doesn't "
                "equal to 1. "
            )
            logger.error(f"        {1 - TOLERANCE} <= {cum_prob} <= {1 + TOLERANCE} ")

            exit(1)

    def reset(self) -> Tuple:
        obs = self._db.get_random_entry()
        if isinstance(obs[3], Tuple) and obs[0] is not None:
            self.last_genres = obs[3]
        else:
            print(
                f"[ERROR] reset(): Record contain wrong types.\n        {type(obs[3])}"
            )
            logger.error(
                f"[ERROR] reset(): Record contain wrong types.\n        {type(obs[3])}"
            )
            exit(1)
        info = f"[INFO] First entry is: {obs}"
        return (obs, info)

    def step(self, action: Actions) -> Tuple:
        if self.record_tracker > self._full_config["model"]["batch_size"] - 1:
            self.batch = self._db.get_batch(self.last_genres, action)
            self.record_tracker: int = 0

        reward = self.rewards[action]
        obs = self.batch[self.record_tracker]
        terminated = True if self.current_episode > self.nepisodes else False
        self.current_episode += 1
        self.last_genres = obs[3]
        self.record_tracker += 1

        if terminated:
            self.record_tracker = 1 << 31
            self.current_episode = 0

        return obs, reward, terminated

    def __repr__(self) -> str:
        upvote_prob_keys = list(self.upvote_prob.keys())
        upvote_prob_str = f"{upvote_prob_keys[0]}: {self.upvote_prob[upvote_prob_keys[0]]}, ..., {upvote_prob_keys[-1]}: {self.upvote_prob[upvote_prob_keys[-1]]}"
        rows = {
            "actions": self.actions,
            "rewards": self.rewards,
            "render_mode": self.render_mode,
            "upvote_prob": upvote_prob_str,
        }

        max_length = max(len(f"{key}: {value}") for key, value in rows.items())
        title = f" {self.cls_name} "
        padding = (max_length - len(title)) // 2
        header = f"{'=' * padding}{title}{'=' * padding}"
        header = header.ljust(max_length, "=")

        formatted_rows = [
            f"{key}: {str(value).rjust(max_length - len(key) - 2)}"
            for key, value in rows.items()
        ]
        return f"{header}\n" + "\n".join(formatted_rows) + f"\n{'=' * len(header)}"
