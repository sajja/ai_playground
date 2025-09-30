from flask import Flask, render_template, jsonify, request
from q_learning.agent import QLearningAgent, DynamicQLearningAgent

app = Flask(__name__)
agent = QLearningAgent(size=5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def train():
    agent.train()
    return jsonify(success=True)

@app.route('/get_path', methods=['GET'])
def get_path():
    path, done, final_state = agent.test_policy()
    return jsonify({
        "path": path,
        "done": done,
        "final_state": final_state
    })

@app.route('/resize', methods=['POST'])
def resize():
    global agent
    size = request.json.get('size', 5)
    env_type = request.json.get('env_type', 'static')
    if env_type == 'dynamic':
        agent = DynamicQLearningAgent(size=size)
    else:
        agent = QLearningAgent(size=size)
    return jsonify(success=True)

@app.route('/get_q_table', methods=['GET'])
def get_q_table():
    # The Q-table keys are tuples, which are not directly JSON serializable.
    # Convert them to strings.
    q_table_serializable = {str(k): v for k, v in agent.Q.items()}
    return jsonify(q_table_serializable)

if __name__ == '__main__':
    app.run(debug=True)