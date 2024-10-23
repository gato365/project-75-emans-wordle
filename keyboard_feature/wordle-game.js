const WORD = "KNACK";
const WORD_LENGTH = 5;
const MAX_GUESSES = 6;
const KEYBOARD_LAYOUT = [
  ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
  ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
  ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
];

class WordleGame {
  constructor() {
    this.guesses = [];
    this.currentGuess = '';
    this.keyboardStatus = Object.fromEntries(KEYBOARD_LAYOUT.flat().map(key => [key, 'unused']));
    this.gameOver = false;
    this.message = '';

    this.initializeDOM();
    this.renderBoard();
    this.renderKeyboard();
  }

  initializeDOM() {
    // const boardElement = document.getElementById('board');
    // boardElement.innerHTML = `
    //   ${Array(MAX_GUESSES).fill().map((_, index) => `
    //     <div class="row" id="row-${index}">
    //       ${Array(WORD_LENGTH).fill().map((_, cellIndex) => `<div class="cell" id="cell-${index}-${cellIndex}"></div>`).join('')}
    //     </div>
    //   `).join('')}
    // `;

    const keyboardElement = document.getElementById('keyboard');
    keyboardElement.innerHTML = KEYBOARD_LAYOUT.map(row => `
      <div class="keyboard-row">
        ${row.map(key => `<button class="key" data-key="${key}">${key}</button>`).join('')}
      </div>
    `).join('');

    keyboardElement.addEventListener('click', (e) => {
      if (e.target.classList.contains('key')) {
        this.handleKeyPress(e.target.dataset.key);
      }
    });

    document.getElementById('backspace').addEventListener('click', () => this.handleKeyPress('BACKSPACE'));
    document.getElementById('enter').addEventListener('click', () => this.handleKeyPress('ENTER'));
    document.addEventListener('keydown', (e) => {
      const key = e.key.toUpperCase();
      if (key === 'BACKSPACE' || key === 'ENTER' || (key.length === 1 && key >= 'A' && key <= 'Z')) {
        this.handleKeyPress(key);
      }
    });
  }

  renderBoard() {
    // Clear all cells
    for (let i = 0; i < MAX_GUESSES; i++) {
      for (let j = 0; j < WORD_LENGTH; j++) {
        const cell = document.getElementById(`cell-${i}-${j}`);
        cell.textContent = '';
        cell.className = 'cell';
      }
    }

    // Render past guesses
    this.guesses.forEach((guess, rowIndex) => {
      guess.split('').forEach((letter, cellIndex) => {
        const cell = document.getElementById(`cell-${rowIndex}-${cellIndex}`);
        cell.textContent = letter;
      });
    });

    // Render current guess
    if (this.guesses.length < MAX_GUESSES) {
      this.currentGuess.split('').forEach((letter, cellIndex) => {
        const cell = document.getElementById(`cell-${this.guesses.length}-${cellIndex}`);
        cell.textContent = letter;
      });
    }
  }

  renderKeyboard() {
    Object.entries(this.keyboardStatus).forEach(([key, status]) => {
      const keyElement = document.querySelector(`[data-key="${key}"]`);
      if (keyElement) {
        keyElement.className = `key ${status}`;
      }
    });
  }

  handleKeyPress(key) {
    if (this.gameOver) return;

    if (key === 'ENTER') {
      this.submitGuess();
    } else if (key === 'BACKSPACE') {
      this.currentGuess = this.currentGuess.slice(0, -1);
    } else if (this.currentGuess.length < WORD_LENGTH) {
      this.currentGuess += key;
    }

    this.renderBoard();
    document.getElementById('message').textContent = this.message;
  }

  submitGuess() {
    if (this.currentGuess.length !== WORD_LENGTH) {
      this.message = 'Not enough letters';
      return;
    }

    const result = this.checkGuess(this.currentGuess);
    this.updateKeyboardStatus(this.currentGuess, result);
    this.guesses.push(this.currentGuess);
    this.currentGuess = '';

    if (this.currentGuess === WORD) {
      this.message = 'Congratulations! You won!';
      this.gameOver = true;
    } else if (this.guesses.length === MAX_GUESSES) {
      this.message = `Game over. The word was ${WORD}.`;
      this.gameOver = true;
    }

    this.renderBoard();
    this.renderKeyboard();
  }

  checkGuess(guess) {
    const result = Array(WORD_LENGTH).fill('absent');
    const letterCount = {};

    // Count occurrences of each letter in the target word
    for (const letter of WORD) {
      letterCount[letter] = (letterCount[letter] || 0) + 1;
    }

    // First pass: mark correct letters
    for (let i = 0; i < WORD_LENGTH; i++) {
      if (guess[i] === WORD[i]) {
        result[i] = 'correct';
        letterCount[guess[i]]--;
      }
    }

    // Second pass: mark present letters
    for (let i = 0; i < WORD_LENGTH; i++) {
      if (result[i] === 'absent' && letterCount[guess[i]] > 0) {
        result[i] = 'present';
        letterCount[guess[i]]--;
      }
    }

    return result;
  }

  updateKeyboardStatus(guess, result) {
    guess.split('').forEach((letter, index) => {
      const currentStatus = this.keyboardStatus[letter];
      const newStatus = result[index];
      
      if (newStatus === 'correct' || (newStatus === 'present' && currentStatus !== 'correct') || (newStatus === 'absent' && currentStatus !== 'correct' && currentStatus !== 'present')) {
        this.keyboardStatus[letter] = newStatus;
      }
    });
  }
}

// Initialize the game when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
  new WordleGame();
});