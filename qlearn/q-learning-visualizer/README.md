# Q-Learning Visualizer

This project is a web application that visualizes a Q-learning agent navigating a simple grid environment. The application is built using Flask and provides an interactive user interface to observe the agent's learning process and decision-making.

## Project Structure

- **app.py**: Main entry point of the application. Sets up the web server and handles routing.
- **q_learning/agent.py**: Contains the implementation of the Q-learning agent, including the Q-table and methods for action selection and Q-value updates.
- **static/css/style.css**: CSS styles for the user interface, defining the layout and appearance of the web application.
- **static/js/script.js**: JavaScript code for handling user interactions and visualizing the agent's actions and state transitions.
- **templates/index.html**: HTML template for the main page of the application, linking to the CSS and JavaScript files.
- **requirements.txt**: Lists the dependencies required for the project, such as Flask and other necessary libraries.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd q-learning-visualizer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your web browser and navigate to `http://127.0.0.1:5000` to view the application.

## Usage

Once the application is running, you can interact with the Q-learning agent through the user interface. The agent will explore the grid environment, learn from its experiences, and you can visualize its path to the goal.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.