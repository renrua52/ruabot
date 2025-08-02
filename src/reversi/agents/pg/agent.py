import torch
from reversi.agents.pg.policy import PolicyNetwork
from reversi.core.utils import getModelInput

class AgentPG:
    def __init__(self, config):
        self.width = config["width"]
        self.height = config["height"]
        self.policy_network = PolicyNetwork(config["width"], config["height"])
        self.p2i = lambda p : p[0] * self.width + p[1]
        self.i2p = lambda i : (i // self.width, i % self.width)

    def load_weights(self, path):
        self.policy_network.load_state_dict(path)

    def selectAction(self, state):
        model_input = getModelInput(state)

        self.policy_network.eval()
        logits = self.policy_network(model_input)

        legal_moves = state.getAllLegalMoves()
        for i in range(logits.size(1)):
            if not self.i2p(i) in legal_moves:
                logits[0, i] = -float('inf')
        probabilities = torch.softmax(logits, dim=1)
        distribution = torch.distributions.Categorical(probabilities)
        action = distribution.sample()
        move = self.i2p(action.item())
        return move, distribution.log_prob(action)