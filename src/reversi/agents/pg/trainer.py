import torch
import torch.optim as optim
from reversi.core.board import Board

class Trainer:
    def __init__(self, agent, learning_rate=0.001, gamma=0.99):
        self.agent = agent
        self.optimizer = optim.Adam(agent.policy_network.parameters(), lr=learning_rate)
        self.gamma = gamma

    def update_policy(self, log_probabilities, rewards):
        policy_loss = []
        for log_prob, reward in zip(log_probabilities, rewards):
            policy_loss.append(-log_prob * reward)
        policy_loss = torch.cat(policy_loss).sum()

        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()

    def run(self, num_episodes):
        for episode in range(num_episodes):
            board = Board()
            log_probabilities = []
            move_players = []
            
            while board.getResult() == -1:
                current_player = board.getTurn()
                
                move, log_prob = self.agent.selectAction(board)
                log_probabilities.append(log_prob)
                move_players.append(current_player)
                
                board.makeMove(move[0], move[1])
            
            result = board.getResult()
            
            # Assign rewards based on final game result for each player
            rewards = []
            for player in move_players:
                if result == player:
                    reward = 1.0
                elif result == 0:
                    reward = 0.0
                else:
                    reward = -1.0
                rewards.append(reward)
            
            rewards = torch.tensor(rewards, dtype=torch.float32)
            
            self.agent.policy_network.train()
            self.update_policy(log_probabilities, rewards)
            
            if episode % 100 == 0:
                print(f"Episode {episode}, Result: {result}")
