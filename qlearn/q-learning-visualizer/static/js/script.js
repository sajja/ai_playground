// This file contains JavaScript code for the user interface, handling user interactions, and visualizing the Q-learning agent's actions and state transitions.

document.addEventListener('DOMContentLoaded', () => {
    const gridContainer = document.getElementById('grid-container');
    const trainBtn = document.getElementById('train-btn');
    const runBtn = document.getElementById('run-btn');
    const gridSize = 3;
    const start = [0, 0];
    const goal = [2, 2];

    // Create the grid
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            const cell = document.createElement('div');
            cell.classList.add('grid-cell');
            cell.dataset.row = i;
            cell.dataset.col = j;
            if (i === start[0] && j === start[1]) {
                cell.classList.add('start');
                cell.textContent = 'Start';
            }
            if (i === goal[0] && j === goal[1]) {
                cell.classList.add('goal');
                cell.textContent = 'Goal';
            }
            gridContainer.appendChild(cell);
        }
    }

    trainBtn.addEventListener('click', () => {
        fetch('/train', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Training complete!');
                }
            });
    });

    runBtn.addEventListener('click', () => {
        fetch('/get_path')
            .then(response => response.json())
            .then(data => {
                visualizePath(data.path);
            });
    });

    function visualizePath(path) {
        let step = 0;
        const interval = setInterval(() => {
            if (step < path.length) {
                // Clear previous agent positions
                document.querySelectorAll('.agent').forEach(cell => cell.classList.remove('agent'));

                const { state, action } = path[step];
                const [row, col] = state;
                const cell = document.querySelector(`[data-row='${row}'][data-col='${col}']`);
                if (cell) {
                    cell.classList.add('agent');
                }
                step++;
            } else {
                clearInterval(interval);
                alert('Path visualization complete!');
            }
        }, 500);
    }
});