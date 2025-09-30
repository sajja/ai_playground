import numpy as np
import random

# ----- Environment -----
GRID_SIZE = 3
START = (0, 0)
GOAL = (2, 2)

ACTIONS = ["up", "down", "left", "right"]

def step(state, action):
    x, y = state
    if action == "up":
        x = max(0, x - 1)
    elif action == "down":
        x = min(GRID_SIZE - 1, x + 1)
    elif action == "left":
        y = max(0, y - 1)
    elif action == "right":
        y = min(GRID_SIZE - 1, y + 1)

    new_state = (x, y)
    reward = 1 if new_state == GOAL else 0
    done = (new_state == GOAL)
    return new_state, reward, done

# ----- Q-Learning Agent -----
Q = {}  # Q-table as dictionary

def get_Q(state, action):
    return Q.get((state, action), 0.0)

def choose_action(state, epsilon=0.2):
    if random.random() < epsilon:  # exploration
        return random.choice(ACTIONS)
    else:  # exploitation
        qs = [get_Q(state, a) for a in ACTIONS]
        max_q = max(qs)
        best_actions = [a for a, q in zip(ACTIONS, qs) if q == max_q]
        return random.choice(best_actions)

def update_Q(state, action, reward, next_state, alpha=0.1, gamma=0.9):
    old_q = get_Q(state, action)
    next_q = max([get_Q(next_state, a) for a in ACTIONS])
    new_q = old_q + alpha * (reward + gamma * next_q - old_q)
    Q[(state, action)] = new_q

# ----- Training -----
episodes = 200
for episode in range(episodes):
    state = START
    done = False
    while not done:
        action = choose_action(state)
        next_state, reward, done = step(state, action)
        update_Q(state, action, reward, next_state)
        state = next_state

# ----- Test the learned policy -----
print("\nAgent's learned path:")
state = START
done = False
steps = 0
while not done and steps < 10:
    action = choose_action(state, epsilon=0)  # greedy (no exploration)
    print(f"State: {state}, Action: {action}")
    state, reward, done = step(state, action)
    steps += 1

if done:
    print(f"Reached the goal at {state}!")
else:
    print("Did not reach the goal.")

