const GRID_SIZE = 20;
const CELL_SIZE = 20;
const INITIAL_SNAKE = [
    { x: 10, y: 10 },
    { x: 9, y: 10 },
    { x: 8, y: 10 }
];

function Game() {
    const [snake, setSnake] = React.useState(INITIAL_SNAKE);
    const [food, setFood] = React.useState({ x: 15, y: 15 });
    const [direction, setDirection] = React.useState('RIGHT');
    const [gameOver, setGameOver] = React.useState(false);
    const [score, setScore] = React.useState(0);

    React.useEffect(() => {
        document.addEventListener('keydown', handleKeyPress);
        const gameInterval = setInterval(moveSnake, 100);
        
        return () => {
            document.removeEventListener('keydown', handleKeyPress);
            clearInterval(gameInterval);
        };
    }, [snake, direction, gameOver]);

    const handleKeyPress = (event) => {
        switch (event.key) {
            case 'ArrowUp':
                if (direction !== 'DOWN') setDirection('UP');
                break;
            case 'ArrowDown':
                if (direction !== 'UP') setDirection('DOWN');
                break;
            case 'ArrowLeft':
                if (direction !== 'RIGHT') setDirection('LEFT');
                break;
            case 'ArrowRight':
                if (direction !== 'LEFT') setDirection('RIGHT');
                break;
        }
    };

    const moveSnake = () => {
        if (gameOver) return;

        const newSnake = [...snake];
        const head = { ...newSnake[0] };

        switch (direction) {
            case 'UP':
                head.y -= 1;
                break;
            case 'DOWN':
                head.y += 1;
                break;
            case 'LEFT':
                head.x -= 1;
                break;
            case 'RIGHT':
                head.x += 1;
                break;
        }

        // Check for collisions
        if (
            head.x < 0 || head.x >= GRID_SIZE ||
            head.y < 0 || head.y >= GRID_SIZE ||
            snake.some(segment => segment.x === head.x && segment.y === head.y)
        ) {
            setGameOver(true);
            return;
        }

        newSnake.unshift(head);

        // Check if snake ate food
        if (head.x === food.x && head.y === food.y) {
            setScore(score + 1);
            generateFood(newSnake);
        } else {
            newSnake.pop();
        }

        setSnake(newSnake);
    };

    const generateFood = (currentSnake) => {
        let newFood;
        do {
            newFood = {
                x: Math.floor(Math.random() * GRID_SIZE),
                y: Math.floor(Math.random() * GRID_SIZE)
            };
        } while (currentSnake.some(segment => 
            segment.x === newFood.x && segment.y === newFood.y));
        setFood(newFood);
    };

    const resetGame = () => {
        setSnake(INITIAL_SNAKE);
        setDirection('RIGHT');
        setGameOver(false);
        setScore(0);
        generateFood(INITIAL_SNAKE);
    };

    return (
        <div className="game-container">
            <div className="score">Score: {score}</div>
            <div className="game-board" 
                 style={{
                     width: GRID_SIZE * CELL_SIZE + 'px',
                     height: GRID_SIZE * CELL_SIZE + 'px'
                 }}>
                {snake.map((segment, index) => (
                    <div key={index}
                         className="snake-segment"
                         style={{
                             left: segment.x * CELL_SIZE + 'px',
                             top: segment.y * CELL_SIZE + 'px',
                             width: CELL_SIZE + 'px',
                             height: CELL_SIZE + 'px'
                         }}
                    />
                ))}
                <div className="food"
                     style={{
                         left: food.x * CELL_SIZE + 'px',
                         top: food.y * CELL_SIZE + 'px',
                         width: CELL_SIZE + 'px',
                         height: CELL_SIZE + 'px'
                     }}
                />
            </div>
            {gameOver && (
                <div className="game-over">
                    <h2>Game Over!</h2>
                    <p>Final Score: {score}</p>
                    <button onClick={resetGame}>Play Again</button>
                </div>
            )}
        </div>
    );
}

ReactDOM.render(<Game />, document.getElementById('root'));