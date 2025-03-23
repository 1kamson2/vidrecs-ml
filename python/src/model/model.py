from collections import defaultdict
from typing import Any, Dict, Tuple
import numpy as np
from environment.Environment import Environment
from tqdm import tqdm

from utils.enums import Actions


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
        self.q_values: dict = defaultdict(
            lambda: np.zeros(model_config["action_space_size"])
        )
        self.missing_genres = set()
        self.training_err = []
        # observation is the next video or something.

    # TODO: Consider using namedtuples.
    def run(self) -> None:
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

    # attrs = vars(self)
    # print(", ".join(f"{key} : {value}" for key, value in attrs.items()))

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
        # TODO: Test more this bounds
        if 0 <= rnd_choice <= self.eps:
            return Actions.UPVOTE if np.random.random() < 0.5 else Actions.DOWNVOTE
        elif self.eps < rnd_choice < min(1, self.eps + 0.25):
            # TODO: Here consider probabilities
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
                        self.missing_genres.add(genre)
            rnd_action = np.random.random()
            return Actions.UPVOTE if rnd_action <= cum_prob else Actions.DOWNVOTE

        else:
            print("[INFO] get_action(): Unhandled case.")
            return Actions.DOWNVOTE

    def update_model(
        self,
        obs: Tuple,
        next_obs: Tuple,
        action: Actions,
        reward: float,
        terminated: bool,
    ) -> None:
        action_value = action.value
        fut_q_val = (not terminated) * np.max(self.q_values[next_obs])
        temp_diff = reward + self.gamma * fut_q_val * self.q_values[obs][action_value]
        self.q_values[obs][action_value] = (
            self.q_values[obs][action_value] + self.lr * temp_diff
        )
        self.training_err.append(temp_diff)

    def update_eps(self) -> None:
        self.eps = max(self.eps_final, self.eps - self.eps_decay)
