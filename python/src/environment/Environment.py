from psycopg.rows import TupleRow
from utils.enums import Actions
from typing import List, Tuple
from db.Database import Database

TOLERANCE = 1e-3


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
            exit(1)

    def reset(self) -> Tuple:
        obs = self._db.get_random_entry()
        if isinstance(obs[3], Tuple) and obs[0] is not None:
            self.last_genres = obs[3]
        else:
            print(
                f"[ERROR] reset(): Record contain wrong types.\n        {type(obs[3])}"
            )
            exit(1)
        info = f"[INFO] First entry is: {obs}"
        return (obs, info)

    def step(self, action: Actions) -> Tuple:
        """
        TODO:
        For now this will return randomly observations etc, but realistically it
        should be based on our choices.
        Say our action is UPVOTE:
            That means the user liked the content, therefore we should tell the
            environment that he is likely to enjoy more of the movie with such
            genres. Therefore based on the q-values, we return the genres that
            are more likely to be watched.
        Say our action is DOWNVOTE:
            The same, but it will discourage the environment. (or something
            similar to this?)
        In general the environment must act upon given actions, then choose the
        best "observation" based on those q_values.
        Policy should be looking for the action based on the actions and
        simulate if user liked the movies recommended.
        Check classifiers
        The classifier really must be thought of, because some q-values should
        be rather negative, if we wanted to create a policy where the bigger sum
        the better - that means we should sum all categories (if they were
        always positive) because adding more positive values always yields the
        higher sum than less.
        Terminated if we hit some bound of recommendations etc.
        """

        """
        Algorithm: Naive.
        Probably we should use embedding (check on that), but for now, assume we
        get movie with genres A, B, ..., Z, for the sake of the example we will
        consider only A, B, C. They are sorted, so we will always yield the same
        results. If user upvoted this, that means we should assume that he
        liked, all genres. The next observation, should be the one with the
        highest q-value and have A, B, C, or (A, B), (B, C), (A, C) or (A, B,
        C). This operations should be fast because:
            - For now the database is not that big.
            - We operate on sets, which are fast operations.
        Otherwise, we will send out the movies randomly.
        How this will work out, will be checked in action.
        The observations will be choosen randomly 
        """
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
        # This dict is too long to display, so it is shortened.
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
