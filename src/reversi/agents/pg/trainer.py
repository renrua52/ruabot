import torch
import torch.optim as optim
import os
from reversi.core.board import Board

class Trainer:
    def __init__(self, agent, learning_rate=0.001, gamma=0.99):
        self.agent = agent
        self.optimizer = optim.Adam(agent.policy_network.parameters(), lr=learning_rate)
        self.gamma = gamma

    def compute_loss(self, log_probabilities, rewards):
        policy_loss = []
        for log_prob, reward in zip(log_probabilities, rewards):
            policy_loss.append(-log_prob * reward)
        policy_loss = torch.cat(policy_loss).sum()
        return policy_loss

    def update_policy(self, total_loss):
        self.optimizer.zero_grad()
        total_loss.backward()
        self.optimizer.step()

    def run(self, num_episodes):
        for episode in range(num_episodes):
            board = Board(self.agent.config)
            log_probs = {
                1: [],
                2: []
            }
            rewards = {
                1: [],
                2: []
            }
            
            while board.getResult() == -1:
                move, log_prob = self.agent.selectAction(board)
                if move == (-1, -1):
                    board.makeEmptyMove()
                    continue
                board.makeMove(move[0], move[1])
                current_player = board.getTurn()
                log_probs[current_player].append(log_prob)
                rewards[current_player].append(0)
            
            result = board.getResult()
            
            total_loss = None
            
            for player in [1, 2]:
                if rewards[player]:
                    if result == player:
                        final_reward = 1.0
                    elif result == 0:
                        final_reward = 0.0
                    else:
                        final_reward = -1.0
                    
                    rewards[player][-1] = final_reward
                    
                    discounted_rewards = []
                    cumulative_reward = 0.0
                    for reward in reversed(rewards[player]):
                        cumulative_reward = cumulative_reward * self.gamma + reward
                        discounted_rewards.append(cumulative_reward)
                    discounted_rewards = list(reversed(discounted_rewards))
                    discounted_rewards = torch.tensor(discounted_rewards, dtype=torch.float32)
                    
                    if len(discounted_rewards) > 1:
                        discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + 1e-9)
                    
                    player_loss = self.compute_loss(log_probs[player], discounted_rewards)
                    
                    if total_loss is None:
                        total_loss = player_loss
                    else:
                        total_loss = total_loss + player_loss
            
            if total_loss is not None:
                self.update_policy(total_loss)
            
            if (episode+1) % 1000 == 0:
                print(f"Episode {episode+1}")
                self.save_model(episode+1)

    def save_model(self, ckpt):
        save_dir = "runs/pg"
        os.makedirs(save_dir, exist_ok=True)
        
        model_path = os.path.join(save_dir, f"policy_network_ckpt_{ckpt}.pth")
        torch.save(self.agent.policy_network.state_dict(), model_path)
        print(f"Model saved to {model_path}")
