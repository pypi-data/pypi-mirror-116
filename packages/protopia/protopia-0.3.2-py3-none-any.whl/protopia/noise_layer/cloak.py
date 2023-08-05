import torch
from torch import nn


class Cloak(nn.Module):
    def __init__(self, input_shape=(-1, 3, 224, 224), scale=(0.0001, 2.0), threshold=1.0):
        super().__init__()

        self.given_shape = input_shape[1:]

        self.threshold_value = 1.0

        self.threshold_value = threshold

        self.locs = torch.nn.Parameter(torch.zeros(self.given_shape))
        self.rhos = torch.nn.Parameter(torch.ones(self.given_shape) * -4)

        # Normal Distribution buffers
        self.register_buffer("loc", torch.tensor(0.))
        self.register_buffer("scale", torch.tensor(1.))

        self.min_scale = scale[0]
        self.max_scale = scale[1]

        self.rhos.requires_grad = False
        self.locs.requires_grad = False

    def print_locs(self):
        print(self.locs)

    def print_rhos(self):
        print(self.rhos)

    def forward(self, x):
        std = (1.0 +torch.tanh(self.rhos))/2*(self.max_scale-self.min_scale) +self.min_scale
        mask = (std < self.threshold_value).float()
        data = x + std * torch.randn(size=self.given_shape)

        x = torch.clamp(
            data * mask + -1 * (1 - mask) + self.locs,
            -1,
            1,
        )

        return x
