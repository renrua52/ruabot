import torch
from reversi.agents.pg.policy import PolicyNetwork
from reversi.agents.pg.utils import getModelInput

class PGAgent:
    def __init__(self, config, training):
        self.config = config
        self.width = config["width"]
        self.height = config["height"]
        self.policy_network = PolicyNetwork(config["width"], config["height"])
        self.p2i = lambda p : p[0] * self.width + p[1]
        self.i2p = lambda i : (i // self.width, i % self.width)
        if training:
            self.policy_network.train()
        else:
            self.policy_network.eval()

    def load_weights(self, path):
        self.policy_network.load_state_dict(torch.load(path))

    def selectAction(self, state):
        model_input = getModelInput(state)

        legal_moves = state.getAllLegalMoves()
        if len(legal_moves) == 0:
            return (-1, -1), None

        logits = self.policy_network(model_input)

        masked_logits = logits.clone()
        for i in range(masked_logits.size(1)):
            if not self.i2p(i) in legal_moves:
                masked_logits[0, i] = -float('inf')
        probabilities = torch.softmax(masked_logits, dim=1)
        distribution = torch.distributions.Categorical(probabilities)
        action = distribution.sample()
        move = self.i2p(action.item())
        return move, distribution.log_prob(action)