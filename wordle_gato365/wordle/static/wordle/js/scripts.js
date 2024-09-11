



let attemptsList = [];
let currentWordIndex = 0;
let attempts = 6;
let startTime, endTime;





let words = [
  "beach", "coast", "horse", "learn",
  "nudge", "fiber", "mayor", "ghost",
  "lapel", "frack", "audio", "uncap"
];

document.getElementById('startButton').addEventListener('click', startGame);
document.getElementById('restartButton').addEventListener('click', restartGame);
document.getElementById('guessInput').addEventListener('keypress', function(event) {
    if (event.key === "Enter") {
        submitGuess();
    }
});

document.getElementById('guessInput').addEventListener('input', function() {
  this.value = this.value.toLowerCase();
});


document.addEventListener('DOMContentLoaded', function () {
  let displayElement = document.getElementById('feedback');
  if (displayElement) {
      displayElement.innerHTML = '';
  }
});

function shuffleWords() {
  for (let i = words.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [words[i], words[j]] = [words[j], words[i]];
  }
}

words = words.map(word => word.toLowerCase());
shuffleWords();




















function startGame() {
  fetch('/game/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    if (data.status === 'success') {
      attempts = 6;
      attemptsList = [];
      currentWordIndex = Math.floor(Math.random() * words.length);

      document.getElementById('startButton').style.display = 'none';
      document.getElementById('guessInput').style.display = 'block';
      document.getElementById('submitGuessButton').style.display = 'block';

      document.getElementById('sessionInfo').value = '';
      document.getElementById('attemptsLeft').textContent = `You have ${attempts} attempts left.`;
      document.getElementById('attemptedWords').innerHTML = '';
      document.getElementById('feedback').innerHTML = '';

      document.getElementById('guessInput').disabled = false;
  
      startTimer();
    } else {
      throw new Error('Game initialization failed');
    }
  }).catch(error => {
    console.error('There was a problem with the fetch operation:', error);
    // Display error to user
    document.getElementById('feedback').innerHTML = 'Failed to start game. Please try again.';
  });
}


function restartGame() {
  document.getElementById('restartButton').style.display = 'none';
  document.getElementById('startButton').style.display = 'block';
  
  document.getElementById('guessInput').style.display = 'none';
  document.getElementById('submitGuessButton').style.display = 'none';
  document.getElementById('sessionInfo').style.display = 'none';
  document.getElementById('feedback').innerHTML = '';
  document.getElementById('attemptsLeft').textContent = '';
  document.getElementById('attemptedWords').innerHTML = '';
}

function submitGuessOLD() {
  let guess = document.getElementById('guessInput').value.toLowerCase();
  
  if (guess.length !== 5) {
    alert("Please enter a 5-letter word.");
    return;
  }

  let answer = words[currentWordIndex];
  calculateAndDisplayFeedback(guess, answer);
  
  attempts--;
  document.getElementById('attemptsLeft').textContent = `You have ${attempts} attempts left.`;

  let attemptedWordsDiv = document.getElementById('attemptedWords');
  

  attemptsList.push(guess);

  document.getElementById('guessInput').value = '';

  if (guess === answer) {
    endGame(true);
  } else if (attempts === 0) {
    endGame(false);
  }
}

function calculateAndDisplayFeedbackOLD(guess, answer) {
  let feedback = Array(5).fill('⬛');
  let letterCounts = {};
  let displayElement = document.getElementById('feedback');
  let htmlContent = "";

  for (let letter of answer) {
      letterCounts[letter] = (letterCounts[letter] || 0) + 1;
  }

  for (let i = 0; i < 5; i++) {
      if (guess[i] === answer[i]) {
          feedback[i] = '🟩';
          letterCounts[guess[i]] -= 1;
      }
  }

  for (let i = 0; i < 5; i++) {
      if (guess[i] !== answer[i] && letterCounts[guess[i]] > 0) {
          feedback[i] = '🟨';
          letterCounts[guess[i]] -= 1;
      }
  }

  for (let i = 0; i < 5; i++) {
      let colorClass = (feedback[i] === '🟩' ? 'green' : (feedback[i] === '🟨' ? 'yellow' : 'gray'));
      htmlContent += `<span class="${colorClass}">${guess[i]}</span>`;
  }

  displayElement.innerHTML += `${htmlContent}<br/>`;
}


function submitGuess() {
  let guess = document.getElementById('guessInput').value.toLowerCase();

  if (guess.length !== 5) {
    alert("Please enter a 5-letter word.");
    return;
  }

  let answer = words[currentWordIndex];
  calculateAndDisplayFeedback(guess, answer);

  attempts--;
  document.getElementById('attemptsLeft').textContent = `You have ${attempts} attempts left.`;
  let attemptedWordsDiv = document.getElementById('attemptedWords');

  attemptsList.push(guess);
  document.getElementById('guessInput').value = '';

  if (guess === answer) {
    endGame(true);
  } else if (attempts === 0) {
    endGame(false);
  }
}


function calculateAndDisplayFeedback(guess, answer) {
  let feedback = Array(5).fill('⬛');
  let letterCounts = {};
  let displayElement = document.getElementById('feedback');
  let htmlContent = '<div class="attempt-box">';

  for (let letter of answer) {
    letterCounts[letter] = (letterCounts[letter] || 0) + 1;
  }

  for (let i = 0; i < 5; i++) {
    if (guess[i] === answer[i]) {
      feedback[i] = '🟩';
      letterCounts[guess[i]] -= 1;
    }
  }

  for (let i = 0; i < 5; i++) {
    if (guess[i] !== answer[i] && letterCounts[guess[i]] > 0) {
      feedback[i] = '🟨';
      letterCounts[guess[i]] -= 1;
    }
  }

  for (let i = 0; i < 5; i++) {
    let colorClass = (feedback[i] === '🟩' ? 'green' : (feedback[i] === '🟨' ? 'yellow' : 'gray'));
    htmlContent += `<span class="letter-box ${colorClass}">${guess[i]}</span>`;
  }

  htmlContent += '</div>';
  displayElement.innerHTML += `${htmlContent}<br/>`;
}



function endGame(isWin) {
  document.getElementById('guessInput').disabled = true;
  showSessionInfo();
  updateSessionInfo(attempts, attemptsList);
  document.getElementById('restartButton').style.display = 'block';
  
  if (isWin) {
    alert("Congratulations! You've guessed the word correctly!");
  } else {
    alert(`You've run out of attempts! The correct word was ${words[currentWordIndex]}.`);
  }
}

function getUserId() {
    return `user-${Math.floor(Math.random() * 1000000)}`;
}

function updateSessionInfo(attemptsLeft, attemptsList) {
    let sessionInfo = document.getElementById('sessionInfo');
    let currentTime = new Date();
    let timeTaken = endTimer();
    let attemptsStr = attemptsList.join(', ');
    let userId = getUserId();

    sessionInfo.value += `User ID: ${userId} - Word: ${words[currentWordIndex]} - Attempts: ${6 - attemptsLeft} - Date: ${currentTime.toLocaleDateString()} - Time: ${currentTime.toLocaleTimeString()} - Duration: ${timeTaken} seconds - Sequence Number: ${currentWordIndex + 1} - Guesses: [${attemptsStr}]\n---\n`;
}

function showSessionInfo() {
    document.getElementById('sessionInfo').style.display = 'block';
}

function startTimer() {
    startTime = new Date();
}

function endTimer() {
    endTime = new Date();
    let timeDiff = (endTime - startTime) / 1000;
    return Math.round(timeDiff);
}


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}