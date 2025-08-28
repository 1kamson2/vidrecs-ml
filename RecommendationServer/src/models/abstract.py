from abc import ABC, abstractmethod

import torch

class Model(ABC):
    @abstractmethod
    def feed(self, *args, **kwags):
        """
        Doc here
        """
        ...
    @abstractmethod
    def loss(self, *args, **kwargs) -> torch.Tensor:
        """
            Evaluate loss on given batch.

            Arguments:
                args, kwargs: Pass additional arguments, implementation
                              depended.

            Returns:
                Loss value in tensor.
        """
        ...

class Training(ABC):
    @abstractmethod
    def rate(self, *args, **kwargs) -> float:
        ...

    @abstractmethod
    def run(self, *args, **kwargs):
        ...

