import torch
from reversi.agents.policy import PolicyNetwork
from reversi.agents.utils import getModelInput

class ReversiAgent:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.policy_network = PolicyNetwork(width, height)
        self.p2i = lambda p : p[0] * self.width + p[1]
        self.i2p = lambda i : (i // self.width, i % self.width)

    def selectAction(self, state):
        model_input = getModelInput(state)

        self.policy_network.eval()
        logits = self.policy_network(model_input)

        legal_moves = state.getAllLegalMoves()
        for i in range(logits.size(1)-1): # last entry is empty move, which is always legal
            if not self.i2p(i) in legal_moves:
                logits[0, i] = -float('inf')
        probabilities = torch.softmax(logits, dim=1)
        distribution = torch.distributions.Categorical(probabilities)
        action = distribution.sample()
        move = (-1, -1) if action.item() == logits.size(1)-1 else self.i2p(action.item())
        return move, distribution.log_prob(action)