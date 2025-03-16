from collections import defaultdict
from typing import Any, Dict, List 
import numpy as np
from environment.Environment import Environment
from tqdm import tqdm


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
        self.nepisodes: int = model_config["nepisodes"]
        self.nactions: int = model_config["action_space_size"]
        self.env: Environment = Environment(**full_config)
        self.q_values: dict = defaultdict(lambda: np.zeros(self.nactions))
        self.training_err = np.array([], dtype=np.float32) 
        # observation is the next video or something.
    def get_action(self)->None:
        assert False, "TODO: Agent's policy, not implemented"

    def update_model(self)->None:
        assert False, "TODO: Agent update model function, not implemented"

    def update_eps(self)->None:
        assert False, "TODO: Agent update eps function, not implemented"
