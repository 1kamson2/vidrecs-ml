import torch
from torch import nn

from models.abstract import Model

class FunkSVD(nn.Module, Model):
    def __init__(self, 
                 n_users: int, 
                 n_items: int, 
                 embedding_dim: int,
                 regularization_rate: int
                 ):
        """
            Implementation of FunkSVD recommendation model.

            Arguments:
                n_users: define the number of users.
                n_items: define the number of items that will be used for
                         user recommendation.
                embedding_dim: define a hidden embedding dimension.
                regularization_rate: define the rate of how fast regularization
                                     goes
        """
        self.n_users: int = n_users
        self.n_items: int = n_items
        self.embedding_dim: int = embedding_dim
        self.regularization_rate: int = regularization_rate
        self.users: torch.Tensor = torch.zeros(n_users, embedding_dim,
                                               dtype=torch.int64) 
        self.items: torch.Tensor = torch.zeros(n_items, embedding_dim,
                                               dtype=torch.int64)

    def forward(self, item: int, user: int):
        return self.items[item].T * self.users[user] 

    def loss(self, *args, **kwargs) -> torch.Tensor:
        return torch.square(torch.norm(kwargs["objective"] - self.users * self.items.T,
                                       p="fro"))

    def feed(self):
        pass
