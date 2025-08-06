import torch
from reversi.agents.pg.policy import PolicyNetwork
from reversi.agents.pg.utils import getModelInput

class PGAgent:
    def __init__(self, config, training=False):
        self.config = config
        self.width = config["width"]
        self.height = config["height"]
        self.policy_network = PolicyNetwork(config["width"], config["height"])
        self.p2i = lambda p : p[0] * self.width + p[1]
        self.i2p = lambda i : (i // self.width, i % self.width)
        self.training = training
        if training:
            self.policy_network.train()
        else:
            self.policy_network.eval()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # print(f"Using device: {self.device}")
        
        self.policy_network.to(self.device)

    def load_weights(self, path):
        self.policy_network.load_state_dict(torch.load(path))

    def selectAction(self, state, do_sample=False, top_k=None):
        model_input = getModelInput(state, self.device)

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
        if do_sample:
            if top_k is not None:
                top_k_actual = min(top_k, len(legal_moves))
                top_probs, top_indices = torch.topk(probabilities, top_k_actual, dim=1)
                
                filtered_probs = torch.zeros_like(probabilities)
                filtered_probs.scatter_(1, top_indices, top_probs)
                
                filtered_probs = filtered_probs / filtered_probs.sum(dim=1, keepdim=True)
                filtered_distribution = torch.distributions.Categorical(filtered_probs)
                action = filtered_distribution.sample()
            else:
                action = distribution.sample()
        else:
            action = torch.argmax(probabilities, dim=1)
        move = self.i2p(action.item())

        return move, distribution.log_prob(action)