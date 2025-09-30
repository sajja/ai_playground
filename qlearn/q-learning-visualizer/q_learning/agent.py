import numpy as np
import random

ACTIONS = ["up", "down", "left", "right", "up-left", "up-right", "down-left", "down-right"]

class QLearningAgent:
    def __init__(self, size=3):
        self.grid_size = size
        self.START = (0, 0)
        self.GOAL = (size - 1, size - 1)
        self.Q = {}  # Q-table as dictionary

    def get_Q(self, state, action):
        return self.Q.get((state, action), 0.0)

    def choose_action(self, state, epsilon=0.2):
        if random.random() < epsilon:  # exploration
            return random.choice(ACTIONS)
        else:  # exploitation
            qs = [self.get_Q(state, a) for a in ACTIONS]
            max_q = max(qs)
            best_actions = [a for a, q in zip(ACTIONS, qs) if q == max_q]
            return random.choice(best_actions)

    def update_Q(self, state, action, reward, next_state, alpha=0.1, gamma=0.9):
        old_q = self.get_Q(state, action)
        next_q = max([self.get_Q(next_state, a) for a in ACTIONS])
        new_q = old_q + alpha * (reward + gamma * next_q - old_q)
        self.Q[(state, action)] = new_q

    def train(self, episodes=200):
        for episode in range(episodes):
            state = self.START
            done = False
            while not done:
                action = self.choose_action(state)
                next_state, reward, done = self.step(state, action)
                self.update_Q(state, action, reward, next_state)
                state = next_state

    def step(self, state, action):
        x, y = state
        if action == "up":
            x = max(0, x - 1)
        elif action == "down":
            x = min(self.grid_size - 1, x + 1)
        elif action == "left":
            y = max(0, y - 1)
        elif action == "right":
            y = min(self.grid_size - 1, y + 1)
        elif action == "up-left":
            x = max(0, x - 1)
            y = max(0, y - 1)
        elif action == "up-right":
            x = max(0, x - 1)
            y = min(self.grid_size - 1, y + 1)
        elif action == "down-left":
            x = min(self.grid_size - 1, x + 1)
            y = max(0, y - 1)
        elif action == "down-right":
            x = min(self.grid_size - 1, x + 1)
            y = min(self.grid_size - 1, y + 1)

        new_state = (x, y)
        reward = 1 if new_state == self.GOAL else 0
        done = (new_state == self.GOAL)
        return new_state, reward, done

    def test_policy(self):
        path = []
        state = self.START
        done = False
        steps = 0
        while not done and steps < self.grid_size * self.grid_size * 2:
            action = self.choose_action(state, epsilon=0)  # Greedy action
            path.append({'state': state, 'action': action})
            state, _, done = self.step(state, action)
            steps += 1
        if done:
            path.append({'state': state, 'action': 'done'})
        return path, done, state

class DynamicQLearningAgent(QLearningAgent):
    def __init__(self, size=5):
        super().__init__(size)
        self.obstacle = None
        self.place_obstacle()

    def place_obstacle(self):
        while True:
            self.obstacle = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if self.obstacle != self.START and self.obstacle != self.GOAL:
                break

    def step(self, state, action):
        new_state, reward, done = super().step(state, action)

        if new_state == self.obstacle:
            reward = -1  # Penalty for hitting an obstacle
            # Go back to the previous state
            return state, reward, False 

        if done:
            self.place_obstacle() # Move obstacle for next episode

        return new_state, reward, done