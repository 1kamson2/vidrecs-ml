from collections import defaultdict
from typing import Any, Dict
import numpy as np
from tqdm import tqdm


class VRModel:
    def __init__(self, **config: Dict[str, Any]):
        """
            Parameters:
                - config: specifies all the variables used in training /
                  validation / inference mode.
            The class specifies the model, which will be used in training or
            recommending. 
            Functions:

        """
        model_cfg = config["model"]
        self.config = config
        self.mode = model_cfg["mode"]
        self.batch_size = model_cfg["batch_size"]
        self.lr = model_cfg["lr"] 
        self.eps = model_cfg["eps"] 
        self.eps_decay = model_cfg["eps_decay"] 
        self.eps_final = model_cfg["eps_final"] 
        self.gamma = model_cfg["gamma"] 
        self.nepisodes = model_cfg["nepisodes"]
        self.nactions = model_cfg["action_space_size"]
        self.q_values = defaultdict(lambda: np.zeros(self.nactions))
        self.training_err = np.array([], dtype=np.float32) 
        # observation is the next video or something.




