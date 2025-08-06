import torch
import torch.optim as optim
import os
import random
from reversi.core.board import Board
from reversi.agents.pg.agent import PGAgent

class Trainer:
    def __init__(
            self,
            agent: PGAgent,
            learning_rate=1e-4,
            gamma=0.99,
            gain_weight=1,
            border_weight=1,
            max_opponents=5,
        ):
        self.agent = agent
        self.device = self.agent.device
        
        self.optimizer = optim.Adam(agent.policy_network.parameters(), lr=learning_rate)
        self.gamma = gamma
        self.gain_weight = gain_weight
        self.border_weight = border_weight
        
        self.max_opponents = max_opponents
        self.opponent_pool = []
        self.opponent_weights = []
        
        self.use_random_opponent_prob = 0.25

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

    def add_opponent_to_pool(self):
        current_weights = {k: v.cpu().clone() for k, v in self.agent.policy_network.state_dict().items()}
        self.opponent_weights.append(current_weights)
        
        opponent = PGAgent(self.agent.config, training=False)
        opponent.policy_network.load_state_dict(current_weights)
        self.opponent_pool.append(opponent)
        
        if len(self.opponent_pool) > self.max_opponents:
            self.opponent_pool.pop(0)
            self.opponent_weights.pop(0)
        
        print(f"Added opponent to pool. Pool size: {len(self.opponent_pool)}")

    def get_random_opponent(self):
        if random.random() < self.use_random_opponent_prob:
            return "random"
        elif not self.opponent_pool:
            return None
        else:
            return random.choice(self.opponent_pool)

    def make_random_move(self, board):
        legal_moves = board.getAllLegalMoves()
        if not legal_moves:
            return (-1, -1), None
        move = random.choice(legal_moves)
        return move, None

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
            
            training_player = random.choice([1, 2])
            opponent = self.get_random_opponent()
            
            while board.getResult() == -1:
                current_player = board.getTurn()
                
                if current_player == training_player:
                    move, log_prob = self.agent.selectAction(board, do_sample=True, top_k=5)
                elif opponent == "random":
                    move, log_prob = self.make_random_move(board)
                elif opponent is not None:
                    move, log_prob = opponent.selectAction(board, do_sample=True, top_k=5)
                else:
                    move, log_prob = self.agent.selectAction(board, do_sample=True, top_k=5)
                
                if move == (-1, -1):
                    board.makeEmptyMove()
                    continue

                b, w = board.getScores()
                adv_before = b - w if current_player == 1 else w - b
                
                board.makeMove(move[0], move[1])

                b, w = board.getScores()
                adv_after = b - w if current_player == 1 else w - b

                gain = adv_after - adv_before
                gain_reward = 0.05 * self.gain_weight * gain * (self.agent.config["height"] * self.agent.config["width"]) ** -0.5
                
                border_reward = 0.0
                if (move[0] == 0 and move[1] == 0) or (move[0] == self.agent.config["height"]-1 and move[1] == self.agent.config["width"]-1):
                    border_reward = 0.1
                if ((move[0] == 0) ^ (move[1] == 0)) or ((move[0] == self.agent.config["height"]-1) ^ (move[1] == self.agent.config["width"]-1)):
                    border_reward = 0.02
                border_reward *= self.border_weight

                immediate_reward = gain_reward + border_reward
                
                log_probs[current_player].append(log_prob)
                rewards[current_player].append(immediate_reward)
            
            result = board.getResult()
            
            total_loss = None
            if rewards[training_player]:
                if result == training_player:
                    final_reward = 1.0
                elif result == 0:
                    final_reward = 0.0
                else:
                    final_reward = -1.0
                
                rewards[training_player][-1] = final_reward
                
                discounted_rewards = []
                cumulative_reward = 0.0
                for reward in reversed(rewards[training_player]):
                    cumulative_reward = cumulative_reward * self.gamma + reward
                    discounted_rewards.append(cumulative_reward)
                discounted_rewards = list(reversed(discounted_rewards))
                discounted_rewards = torch.tensor(discounted_rewards, dtype=torch.float32, device=self.device)
                
                if len(discounted_rewards) > 1:
                    reward_std = discounted_rewards.std()
                    if reward_std > 1e-6:
                        discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / reward_std
                
                total_loss = self.compute_loss(log_probs[training_player], discounted_rewards)
            
            if total_loss is not None:
                self.update_policy(total_loss)

            if (episode+1) % 100 == 0:
                print(f"Episode {episode+1}/{num_episodes}")
            
            if (episode+1) % 500 == 0:
                self.add_opponent_to_pool()
            
            if (episode+1) % 1000 == 0:
                self.save_model(episode+1)
                self.test_dummy(episode+1)

    def save_model(self, ckpt):
        save_dir = "runs/pg"
        os.makedirs(save_dir, exist_ok=True)
        
        model_path = os.path.join(save_dir, f"policy_network_ckpt_{ckpt}.pth")
        torch.save(self.agent.policy_network.state_dict(), model_path)
        print(f"Model saved to {model_path}")

    def test_dummy(self, ckpt): # Bad implementation
        from reversi.game.executor import GameExecutor
        from reversi.game.player import DummyPlayer, PolicyPlayer
        from reversi.game.utils import getDefaultConfig
        config = getDefaultConfig(6)

        p1 = PolicyPlayer(config, f"runs/pg/policy_network_ckpt_{ckpt}.pth")
        p2 = DummyPlayer(config)

        score = {0:0, 1:0, 2:0}

        num_games = 400
        for game in range(num_games):
            if game % 2 == 0:
                g = GameExecutor(config, p1, p2, verbose=False)
                res = g.runGame()
                score[res] += 1
            else:
                g = GameExecutor(config, p2, p1, verbose=False)
                res = g.runGame()
                if res != 0:
                    res = 3-res
                score[res] += 1

        print(score)
        print((score[1]+score[0]/2)/num_games)

        
