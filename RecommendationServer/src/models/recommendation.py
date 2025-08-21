from collections import defaultdict
from typing import Any, Dict, Tuple
import numpy as np
from environment.Environment import Environment
from tqdm import tqdm
from utils.io import pkl_save, pkl_load
from utils.log import logger_builder
from pathlib import Path
from utils.enums import Actions

# [WARNING]: DO NOT REUSE THOSE VARIABLES, THOSE ARE MADE TO USE ONLY IN THIS
# FILE
logger = logger_builder("__name__", Path("resource/logs/"))


class VRModel:
    cls_name = "VRModel"

    def __init__(self, **full_config: Dict[str, Any]):
        """
        Parameters:
            - config: specifies all the variables used in training /
              validation / inference mode.
        Functions:
            - get_action(...): Returns the action based on user's config
              possibility to press YES or NO.
            - update_model(...): Updates the model's q_values and other
              class' members.
            - update_eps(...): Updates the model's epsilon values.
        The class specifies the model, which will be used in training or
        recommending.
        """
        model_config = full_config["model"]
        self._full_config: Dict[str, Any] = full_config
        self.mode: str = model_config["mode"]
        self.batch_size: int = model_config["batch_size"]
        self.lr: float = model_config["lr"]
        self.eps: float = model_config["eps"]
        self.eps_decay: float = model_config["eps_decay"]
        self.eps_final: float = model_config["eps_final"]
        self.gamma: float = model_config["gamma"]
        self.env: Environment = Environment(**full_config)
        q_values_info = self._full_config["paths"]["q_values_load"]
        q_values_filename, q_values_load = (
            q_values_info["filename"],
            q_values_info["load"],
        )

        self.q_values: dict = (
            pkl_load(q_values_filename, self._full_config["paths"]["cfg"])
            if q_values_load
            else defaultdict(lambda: np.zeros(model_config["action_space_size"]))
        )
        self.missing_genres = set()
        self.training_err = []
        self.user_first_choice = True
        self.user_prev_obs: Tuple

    def run_user_choice(self, action: Actions) -> Tuple:
        if self.user_first_choice:
            obs, _ = self.env.reset()
            self.user_prev_obs = obs
            self.user_first_choice = False
            return obs

        next_obs, reward, terminated = self.env.step(action)
        self.update_model(self.user_prev_obs, next_obs, action, reward, terminated)
        self.user_prev_obs = next_obs
        return next_obs

    def run(self) -> None:
        """
        Function:
            Run fully automated recommendation algorithm.
        """
        for episode in tqdm(range(self.env.nepisodes)):
            obs, _ = self.env.reset()
            done = False
            while not done:
                action = self.get_action(obs)
                next_obs, reward, terminated = self.env.step(action)
                self.update_model(obs, next_obs, action, reward, terminated)
                done = terminated
                obs = next_obs
                self.update_eps()

        q_values_info = self._full_config["paths"]["q_values_save"]
        q_values_filename, q_values_save = (
            q_values_info["filename"],
            q_values_info["save"],
        )
        if q_values_save:
            pkl_save(
                self.q_values, q_values_filename, self._full_config["paths"]["cfg"]
            )

    def get_action(self, obs: Tuple) -> Actions:
        """
        Parameters:
            - obs: Tuple: Tuple of observations used in the training.
        Function:
            This function is fully automated, meaning that it cannot be used
            by a user. This function will simulate what user would choose,
            based on the probabilities.
        """
        likeness = self._full_config["env"]["likeness"]
        rnd_choice: float = np.random.random()
        if 0 <= rnd_choice <= self.eps:
            return Actions.UPVOTE if np.random.random() < 0.5 else Actions.DOWNVOTE
        elif self.eps < rnd_choice < min(1, self.eps + 0.25):
            return (
                Actions.UPVOTE
                if int(np.argmax(self.q_values[obs])) == 0
                else Actions.DOWNVOTE
            )
        elif max(0, self.eps + 0.25) < rnd_choice < min(1, self.eps + 1):
            genres = obs[3]
            cum_prob = 0
            for genre in genres:
                if genre in likeness.keys():
                    cum_prob += likeness[genre]
                else:
                    if genre not in self.missing_genres:
                        print(f"[WARNING] get_action(): {genre} not in keys.")
                        logger.warning(f"[WARNING] get_action(): {genre} not in keys.")
                        self.missing_genres.add(genre)
            rnd_action = np.random.random()
            return Actions.UPVOTE if rnd_action <= cum_prob else Actions.DOWNVOTE

        else:
            print("[INFO] get_action(): Unhandled case.")
            logger.info("[INFO] get_action(): Unhandled case.")
            return Actions.DOWNVOTE

    def update_model(
        self,
        obs: Tuple,
        next_obs: Tuple,
        action: Actions,
        reward: float,
        terminated: bool,
    ) -> None:
        """
        Alternatives: KNN
        """
        action_value = action.value
        fut_q_val = (not terminated) * np.max(self.q_values[next_obs])
        temp_diff = reward + self.gamma * fut_q_val * self.q_values[obs][action_value]
        self.q_values[obs][action_value] = (
            self.q_values[obs][action_value] + self.lr * temp_diff
        )
        self.training_err.append(temp_diff)

    def update_eps(self) -> None:
        self.eps = max(self.eps_final, self.eps - self.eps_decay)
