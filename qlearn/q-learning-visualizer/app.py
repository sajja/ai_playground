import os
from flask import Flask, render_template, jsonify

from q_learning.agent import QLearningAgent, START, GOAL

app = Flask(__name__)
agent = QLearningAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def train():
    agent.train()
    return jsonify(success=True)

@app.route('/get_q_table', methods=['GET'])
def get_q_table():
    # Convert tuple keys to strings for JSON serialization
    q_table_serializable = {str(k): v for k, v in agent.Q.items()}
    return jsonify(q_table_serializable)

@app.route('/get_path', methods=['GET'])
def get_path():
    path = []
    state = START
    done = False
    steps = 0
    while not done and steps < 20:
        action = agent.choose_action(state, epsilon=0)  # Greedy action
        path.append({'state': state, 'action': action})
        state, _, done = agent.step(state, action)
        steps += 1
    if done:
        path.append({'state': state, 'action': 'done'})
    return jsonify(path=path)

if __name__ == '__main__':
    app.run(debug=True)