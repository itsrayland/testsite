class BeachTreasureGame {
  constructor() {
    this.score = 0;
    this.timeLeft = 60;
    this.gameActive = false;
    this.treasureCount = 15; // Reduced count since treasures are bigger
    this.beachScene = document.getElementById('nightSky'); // Keeping the same ID for compatibility
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
    this.startButton.textContent = '🌊 Beach Hunt in Progress!';
    this.startButton.disabled = true;
    
    this.generateTreasures();
    this.startTimer();
  }

  generateTreasures() {
    this.beachScene.innerHTML = '';
    
    // Add some beach ambience elements
    this.addBeachAmbience();
    
    for (let i = 0; i < this.treasureCount; i++) {
      const treasure = document.createElement('div');
      treasure.className = 'star'; // Keeping the same class for CSS compatibility
      treasure.style.left = `${Math.random() * 95}%`;
      treasure.style.top = `${Math.random() * 90}%`;
      treasure.style.animationDelay = `${Math.random() * 3}s`;
      treasure.style.animationDuration = `${12 + Math.random() * 8}s`; // Random duration between 12-20s
      
      treasure.addEventListener('click', () => this.collectTreasure(treasure));
      this.beachScene.appendChild(treasure);
    }
  }

  addBeachAmbience() {
    // Add subtle beach wave effects
    for (let i = 0; i < 3; i++) {
      const wave = document.createElement('div');
      wave.className = 'beach-wave';
      wave.style.cssText = `
        position: absolute;
        bottom: ${i * 15}px;
        left: 0;
        width: 100%;
        height: 20px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: waveFlow ${8 + i * 2}s linear infinite;
        pointer-events: none;
      `;
      this.beachScene.appendChild(wave);
    }
  }

  collectTreasure(treasure) {
    if (!this.gameActive) return;
    
    treasure.remove();
    this.score++;
    this.updateScore();
    
    // Generate a new treasure
    const newTreasure = document.createElement('div');
    newTreasure.className = 'star'; // Keeping the same class for CSS compatibility
    newTreasure.style.left = `${Math.random() * 100}%`;
    newTreasure.style.top = `${Math.random() * 100}%`;
    newTreasure.style.animationDelay = `${Math.random() * 2}s`;
    newTreasure.style.animationDuration = `${10 + Math.random() * 10}s`; // Random duration between 10-20s
    newTreasure.addEventListener('click', () => this.collectTreasure(newTreasure));
    this.beachScene.appendChild(newTreasure);
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
    this.startButton.textContent = '🏖️ Start New Beach Hunt!';
    this.startButton.disabled = false;
    
    // Show final score with beach theme
    const treasureTypes = ['🐚', '⭐', '💎', '🏆', '🦀', '🌊', '🏝️', '☀️'];
    const randomTreasure = treasureTypes[Math.floor(Math.random() * treasureTypes.length)];
    const randomTreasure2 = treasureTypes[Math.floor(Math.random() * treasureTypes.length)];
    
    let message = `🏖️ Beach Hunt Complete! ${randomTreasure}\n\n`;
    message += `🐚 Treasures Found: ${this.score}\n`;
    
    if (this.score >= 50) {
      message += `🏆 AMAZING! You're a Beach Treasure Master! ${randomTreasure2}`;
    } else if (this.score >= 30) {
      message += `🌟 Excellent treasure hunting skills! ${randomTreasure2}`;
    } else if (this.score >= 15) {
      message += `🌊 Good work, beach explorer! ${randomTreasure2}`;
    } else {
      message += `🏖️ Keep practicing your treasure hunting! ${randomTreasure2}`;
    }
    
    alert(message);
  }
}

// Initialize the beach treasure game when the page loads
window.addEventListener('load', () => {
  new BeachTreasureGame();
}); 