import os
from flask import Flask, render_template, jsonify, request

from q_learning.agent import QLearningAgent

app = Flask(__name__)
agent = QLearningAgent(size=3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def train():
    agent.train()
    return jsonify(success=True)

@app.route('/resize', methods=['POST'])
def resize():
    global agent
    size = request.json.get('size', 3)
    agent = QLearningAgent(size=size)
    return jsonify(success=True)

@app.route('/get_q_table', methods=['GET'])
def get_q_table():
    # Convert tuple keys to strings for JSON serialization
    q_table_serializable = {str(k): v for k, v in agent.Q.items()}
    return jsonify(q_table_serializable)

@app.route('/get_path', methods=['GET'])
def get_path():
    path = []
    state = agent.START
    done = False
    steps = 0
    while not done and steps < agent.grid_size * agent.grid_size * 2:
        action = agent.choose_action(state, epsilon=0)  # Greedy action
        path.append({'state': state, 'action': action})
        state, _, done = agent.step(state, action)
        steps += 1
    if done:
        path.append({'state': state, 'action': 'done'})
    return jsonify(path=path)

if __name__ == '__main__':
    app.run(debug=True)