import numpy as np
import random

ACTIONS = ["up", "down", "left", "right"]

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

        new_state = (x, y)
        reward = 1 if new_state == self.GOAL else 0
        done = (new_state == self.GOAL)
        return new_state, reward, done

    def test_policy(self, steps=10):
        state = self.START
        done = False
        path = []
        while not done and len(path) < steps:
            action = self.choose_action(state, epsilon=0)  # greedy (no exploration)
            path.append((state, action))
            state, reward, done = self.step(state, action)
        return path, done, state