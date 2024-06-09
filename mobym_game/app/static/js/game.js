let canvas = document.getElementById('gameCanvas');
let ctx = canvas.getContext('2d');
let dino = { x: 50, y: 150, width: 50, height: 50, color: 'green' };
let obstacle = { x: 800, y: 150, width: 50, height: 50, color: 'red' };
let interval, score = 0;

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawDino();
    drawObstacle();
    updateObstacle();
    checkCollision();
    score++;
    ctx.fillStyle = 'black';
    ctx.fillText('Score: ' + score, 700, 50);
}

function drawDino() {
    ctx.fillStyle = dino.color;
    ctx.fillRect(dino.x, dino.y, dino.width, dino.height);
}

function drawObstacle() {
    ctx.fillStyle = obstacle.color;
    ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
}

function updateObstacle() {
    obstacle.x -= 5;
    if (obstacle.x < 0) {
        obstacle.x = 800;
        score++;
    }
}

function checkCollision() {
    if (dino.x < obstacle.x + obstacle.width && dino.x + dino.width > obstacle.x && dino.y < obstacle.y + obstacle.height && dino.y + dino.height > obstacle.y) {
        clearInterval(interval);
        alert('Game Over!');
        resetGame();
    }
}

function resetGame() {
    score = 0;
    obstacle.x = 800;
    interval = setInterval(draw, 1000 / 60);
}

interval = setInterval(draw, 1000 / 60);

document.addEventListener('keydown', function(event) {
    if (event.code === 'Space' && dino.y === 150) {
        dino.y -= 100;
        setTimeout(() => { dino.y = 150; }, 500);
    }
});
