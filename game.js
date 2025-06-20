class BeachTreasureGame {
  constructor() {
    this.score = 0;
    this.timeLeft = 60;
    this.gameActive = false;
    this.treasureCount = 12; // Beach treasures are more valuable
    this.beachScene = document.getElementById('nightSky'); // Beach scene container
    this.scoreElement = document.getElementById('score');
    this.timerElement = document.getElementById('timer');
    this.startButton = document.getElementById('startGame');
    // 🏖️ Beach Treasure Collection - Each with different rarity!
    this.treasureTypes = [
      '🐚', '🦀', '⭐', '💎', '🏆', '🌊', '🏝️', '☀️', '🐠', '🦑', 
      '🐙', '🦞', '🐡', '🌺', '🥥', '⚡', '🔱', '🧜‍♀️'
    ];
    this.collectedTreasures = [];
    
    this.startButton.addEventListener('click', () => this.startBeachHunt());
  }

  startBeachHunt() {
    if (this.gameActive) return;
    
    this.gameActive = true;
    this.score = 0;
    this.timeLeft = 60;
    this.collectedTreasures = [];
    this.updateScore();
    this.startButton.textContent = '🌊 Exploring the Beach... 🏖️';
    this.startButton.disabled = true;
    
    this.generateBeachTreasures();
    this.startBeachTimer();
  }

  generateBeachTreasures() {
    this.beachScene.innerHTML = '';
    
    // Add beach ambience and environment
    this.addBeachAmbience();
    
    for (let i = 0; i < this.treasureCount; i++) {
      const treasure = document.createElement('div');
      treasure.className = 'star'; // Beach treasure styling
      treasure.style.left = `${Math.random() * 92}%`;
      treasure.style.top = `${Math.random() * 88}%`;
      treasure.style.animationDelay = `${Math.random() * 4}s`;
      treasure.style.animationDuration = `${15 + Math.random() * 10}s`; // Slower, more graceful movement
      
      // Add treasure type data for scoring variety
      treasure.dataset.treasureType = this.treasureTypes[Math.floor(Math.random() * this.treasureTypes.length)];
      treasure.dataset.points = Math.floor(Math.random() * 3) + 1; // 1-3 points per treasure
      
      treasure.addEventListener('click', () => this.collectBeachTreasure(treasure));
      this.beachScene.appendChild(treasure);
    }
  }

  addBeachAmbience() {
    // 🌊 Create magical beach wave effects
    for (let i = 0; i < 4; i++) {
      const wave = document.createElement('div');
      wave.className = 'beach-wave';
      wave.style.cssText = `
        position: absolute;
        bottom: ${i * 12}px;
        left: 0;
        width: 100%;
        height: ${18 + i * 3}px;
        background: linear-gradient(90deg, 
          transparent, 
          rgba(255,255,255,${0.1 + i * 0.05}), 
          rgba(64,224,208,0.1),
          transparent);
        animation: waveFlow ${7 + i * 2}s linear infinite;
        pointer-events: none;
        border-radius: 50% 50% 0 0;
      `;
      this.beachScene.appendChild(wave);
    }
    
    // ✨ Add sparkling water effect
    for (let i = 0; i < 6; i++) {
      const sparkle = document.createElement('div');
      sparkle.style.cssText = `
        position: absolute;
        width: 4px;
        height: 4px;
        background: radial-gradient(circle, #40E0D0, transparent);
        top: ${20 + Math.random() * 40}%;
        left: ${Math.random() * 100}%;
        animation: sparkleEffect ${2 + Math.random() * 3}s infinite;
        pointer-events: none;
      `;
      this.beachScene.appendChild(sparkle);
    }
  }

  collectBeachTreasure(treasure) {
    if (!this.gameActive) return;
    
    // Get treasure info
    const treasureType = treasure.dataset.treasureType;
    const points = parseInt(treasure.dataset.points);
    
    // Add to collected treasures
    this.collectedTreasures.push(treasureType);
    
    // Create collection effect
    this.createCollectionEffect(treasure, treasureType, points);
    
    treasure.remove();
    this.score += points;
    this.updateScore();
    
    // Generate a new beach treasure
    const newTreasure = document.createElement('div');
    newTreasure.className = 'star'; // Beach treasure styling
    newTreasure.style.left = `${Math.random() * 92}%`;
    newTreasure.style.top = `${Math.random() * 88}%`;
    newTreasure.style.animationDelay = `${Math.random() * 2}s`;
    newTreasure.style.animationDuration = `${15 + Math.random() * 10}s`;
    
    newTreasure.dataset.treasureType = this.treasureTypes[Math.floor(Math.random() * this.treasureTypes.length)];
    newTreasure.dataset.points = Math.floor(Math.random() * 3) + 1;
    
    newTreasure.addEventListener('click', () => this.collectBeachTreasure(newTreasure));
    this.beachScene.appendChild(newTreasure);
  }

  createCollectionEffect(treasure, treasureType, points) {
    const effect = document.createElement('div');
    effect.style.cssText = `
      position: absolute;
      left: ${treasure.style.left};
      top: ${treasure.style.top};
      pointer-events: none;
      font-size: 24px;
      font-weight: bold;
      color: #FFD700;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
      animation: collectEffect 1s ease-out forwards;
      z-index: 1000;
    `;
    effect.textContent = `${treasureType} +${points}`;
    this.beachScene.appendChild(effect);
    
    setTimeout(() => effect.remove(), 1000);
  }

  updateScore() {
    this.scoreElement.textContent = this.score;
  }

  startBeachTimer() {
    const timer = setInterval(() => {
      this.timeLeft--;
      this.timerElement.textContent = this.timeLeft;
      
      if (this.timeLeft <= 0) {
        clearInterval(timer);
        this.endBeachHunt();
      }
    }, 1000);
  }

  endBeachHunt() {
    this.gameActive = false;
    this.startButton.textContent = '🏖️ Start New Beach Adventure!';
    this.startButton.disabled = false;
    
    // Calculate unique treasures collected
    const uniqueTreasures = [...new Set(this.collectedTreasures)];
    const totalTreasures = this.collectedTreasures.length;
    
    // Show comprehensive beach-themed results
    let message = `🏖️ Beach Treasure Hunt Complete! 🌊\n\n`;
    message += `🐚 Total Score: ${this.score} points\n`;
    message += `🏆 Treasures Collected: ${totalTreasures}\n`;
    message += `✨ Unique Types Found: ${uniqueTreasures.length}/10\n\n`;
    
    if (uniqueTreasures.length > 0) {
      message += `� Your Beach Collection: ${uniqueTreasures.join(' ')}\n\n`;
    }
    
    // Beach achievement rankings
    if (this.score >= 60) {
      message += `🏆 LEGENDARY! Beach Treasure Master! 🌟\nYou've become one with the ocean! 🌊`;
    } else if (this.score >= 40) {
      message += `🥇 AMAZING! Expert Beach Explorer! ⭐\nThe sea reveals its secrets to you! 🐚`;
    } else if (this.score >= 25) {
      message += `🥈 GREAT! Skilled Treasure Hunter! 💎\nYou have a keen eye for beach treasures! 🔍`;
    } else if (this.score >= 15) {
      message += `🥉 GOOD! Beach Adventure Novice! 🌊\nYou're getting the hang of treasure hunting! 🏖️`;
    } else {
      message += `🏖️ Keep exploring the beach paradise! ☀️\nEvery treasure hunter started somewhere! 🐚`;
    }
    
    alert(message);
  }
}

// Initialize the beach treasure game when the page loads
window.addEventListener('load', () => {
  new BeachTreasureGame();
}); 