class StarGame {
  constructor() {
    this.score = 0;
    this.timeLeft = 60;
    this.gameActive = false;
    this.starCount = 15; // Reduced count since stars are bigger
    this.nightSky = document.getElementById('nightSky');
    this.scoreElement = document.getElementById('score');
    this.timerElement = document.getElementById('timer');
    this.startButton = document.getElementById('startGame');
    
    this.startButton.addEventListener('click', () => this.startGame());
  }

  startGame() {
    if (this.gameActive) return;
    
    this.gameActive = true;
    this.score = 0;
    this.timeLeft = 60;
    this.updateScore();
    this.startButton.textContent = 'Game in Progress!';
    this.startButton.disabled = true;
    
    this.generateStars();
    this.startTimer();
  }

  generateStars() {
    this.nightSky.innerHTML = '';
    for (let i = 0; i < this.starCount; i++) {
      const star = document.createElement('div');
      star.className = 'star';
      star.style.left = `${Math.random() * 100}%`;
      star.style.top = `${Math.random() * 100}%`;
      star.style.animationDelay = `${Math.random() * 2}s`;
      star.style.animationDuration = `${10 + Math.random() * 10}s`; // Random duration between 10-20s
      
      star.addEventListener('click', () => this.collectStar(star));
      this.nightSky.appendChild(star);
    }
  }

  collectStar(star) {
    if (!this.gameActive) return;
    
    star.remove();
    this.score++;
    this.updateScore();
    
    // Generate a new star
    const newStar = document.createElement('div');
    newStar.className = 'star';
    newStar.style.left = `${Math.random() * 100}%`;
    newStar.style.top = `${Math.random() * 100}%`;
    newStar.style.animationDelay = `${Math.random() * 2}s`;
    newStar.style.animationDuration = `${10 + Math.random() * 10}s`; // Random duration between 10-20s
    newStar.addEventListener('click', () => this.collectStar(newStar));
    this.nightSky.appendChild(newStar);
  }

  updateScore() {
    this.scoreElement.textContent = this.score;
  }

  startTimer() {
    const timer = setInterval(() => {
      this.timeLeft--;
      this.timerElement.textContent = this.timeLeft;
      
      if (this.timeLeft <= 0) {
        clearInterval(timer);
        this.endGame();
      }
    }, 1000);
  }

  endGame() {
    this.gameActive = false;
    this.startButton.textContent = 'Play Again!';
    this.startButton.disabled = false;
    
    // Show final score
    alert(`Game Over! You found ${this.score} stars!`);
  }
}

// Initialize the game when the page loads
window.addEventListener('load', () => {
  new StarGame();
}); 