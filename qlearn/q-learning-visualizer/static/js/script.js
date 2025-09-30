// This file contains JavaScript code for the user interface, handling user interactions, and visualizing the Q-learning agent's actions and state transitions.

document.addEventListener('DOMContentLoaded', () => {
    const gridContainer = document.getElementById('grid-container');
    const trainBtn = document.getElementById('train-btn');
    const runBtn = document.getElementById('run-btn');
    const gridSizeInput = document.getElementById('grid-size');
    const resizeBtn = document.getElementById('resize-btn');
    const envTypeSelect = document.getElementById('env-type');
    
    let gridSize = 5;
    let start = [0, 0];
    let goal = [4, 4];

    function createGrid(size) {
        gridContainer.innerHTML = '';
        gridContainer.style.gridTemplateColumns = `repeat(${size}, 100px)`;
        gridSize = size;
        start = [0, 0];
        goal = [size - 1, size - 1];

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
    }

    createGrid(parseInt(gridSizeInput.value));

    resizeBtn.addEventListener('click', () => {
        const newSize = parseInt(gridSizeInput.value);
        const envType = envTypeSelect.value;
        createGrid(newSize);
        fetch('/resize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ size: newSize, env_type: envType }),
        }).then(() => {
            alert(`Grid resized to ${newSize}x${newSize} with ${envType} environment. Agent reset.`);
        });
    });

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