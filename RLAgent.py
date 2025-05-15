import random
import json
import copy
from collections import defaultdict
import asyncio

class RLAgent:
    def __init__(self, game, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.game = game
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = defaultdict(float)  # Q-table: (state, action) -> Q-value
        self.q_table_file = "q_table.json"

    def get_state(self):
        """Convert game state to a hashable tuple."""
        return (
            tuple(self.game.dan_count),
            tuple(self.game.quan_count),
            tuple(self.game.point_count[0] + self.game.point_count[1]),
            self.game.player1_turn
        )

    def get_actions(self, player1_turn):
        """Get valid actions: (index, direction) pairs."""
        actions = []
        indices = range(1, 6) if player1_turn else range(7, 12)
        for idx in indices:
            if self.game.dan_count[idx] > 0:
                actions.append((idx, 1))  # Clockwise
                actions.append((idx, -1))  # Counterclockwise
        return actions

    def choose_action(self, state, player1_turn):
        """Epsilon-greedy action selection."""
        actions = self.get_actions(player1_turn)
        print(actions)
        if not actions:
            return None
        if random.random() < self.epsilon:
            return random.choice(actions)
        q_values = [(self.q_table[(state, action)], action) for action in actions]
        max_q = max(q_values, key=lambda x: x[0])[0] if q_values else 0
        best_actions = [action for q, action in q_values if q == max_q]
        return random.choice(best_actions) if best_actions else random.choice(actions)

    def get_reward(self, old_points, new_points, player1_turn):
        """Calculate reward based on points gained."""
        player_idx = 0 if player1_turn else 1
        old_score = old_points[player_idx][0] + old_points[player_idx][1] * self.game.QUAN_COEFFICIENT
        new_score = new_points[player_idx][0] + new_points[player_idx][1] * self.game.QUAN_COEFFICIENT
        return new_score - old_score

    async def train(self, episodes=1000):
        """Train the RL agent over multiple episodes."""
        for episode in range(episodes):
            self.game.reset()
            while self.game.win_player == 0:
                state = self.get_state()
                player1_turn = self.game.player1_turn
                action = self.choose_action(state, player1_turn)
                if not action:
                    self.game.player1_turn = not self.game.player1_turn
                    continue
                idx, direction = action
                old_points = copy.deepcopy(self.game.point_count)
                self.game.selected_cell = idx
                self.game.cells[idx].select_cell()
                arrow_idx = 1 if direction == 1 else 0
                self.game.cells[idx].arrow_cells[arrow_idx].select_cell()
                await self.game.ai_play(direction == 1)
                new_state = self.get_state()
                reward = self.get_reward(old_points, self.game.point_count, player1_turn)
                actions = self.get_actions(self.game.player1_turn)
                future_q = max([self.q_table[(new_state, a)] for a in actions], default=0)
                self.q_table[(state, action)] += self.alpha * (
                    reward + self.gamma * future_q - self.q_table[(state, action)]
                )
                await asyncio.sleep(0)
            print(f"Episode {episode} completed")
            # if episode % 100 == 0:
            #     print(f"Episode {episode} completed")
        self.save_q_table()

    def save_q_table(self):
        """Save Q-table to a JSON file."""
        serializable_q_table = {
            str((state, action)): q_value
            for (state, action), q_value in self.q_table.items()
        }
        try:
            with open(self.q_table_file, 'w') as f:
                json.dump(serializable_q_table, f)
        except Exception as e:
            print(f"Error saving Q-table: {e}")

    def load_q_table(self):
        """Load Q-table from a JSON file."""
        try:
            with open(self.q_table_file, 'r') as f:
                serializable_q_table = json.load(f)
            for key, q_value in serializable_q_table.items():
                state, action = eval(key)
                self.q_table[(state, action)] = q_value
        except FileNotFoundError:
            print("No Q-table found, starting fresh.")
        except Exception as e:
            print(f"Error loading Q-table: {e}")

    def play(self, state, player1_turn):
        """Select action for gameplay using trained Q-table."""
        action = self.choose_action(state, player1_turn)
        return action if action else (random.choice([1, 2, 3, 4, 5, 7, 8, 9, 10, 11]), random.choice([1, -1]))