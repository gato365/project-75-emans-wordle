



let attemptsList = [];
let currentWordIndex = 0;
let attempts = 6;
let startTime, endTime;
let currentGameId = null;




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



async function startGame() {
  try {
      const response = await fetch('/game/', {
          method: 'POST',
          headers: {
              'X-CSRFToken': getCookie('csrftoken'),
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ start_game: true })
      });
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      const data = await response.json();
      currentGameId = data.game_id;

      // Hide/Show Elements
      document.getElementById('startButton').style.display = 'none';
      document.getElementById('guessInput').style.display = 'block';
      document.getElementById('submitGuessButton').style.display = 'block';

      // Reset/Initialize Values
      document.getElementById('sessionInfo').value = '';
      document.getElementById('attemptsLeft').textContent = `You have ${attempts} attempts left.`;
      document.getElementById('attemptedWords').innerHTML = '';
      document.getElementById('feedback').innerHTML = '';

      // Enable/Disable Elements
      document.getElementById('guessInput').disabled = false;

      // Start Timer
      startTimer();
  } catch (error) {
      console.error('There was a problem starting the game:', error);
  }
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






function submitGuess() {
  let guess = document.getElementById('guessInput').value.toLowerCase();

  if (guess.length !== 5) {
    alert("Please enter a 5-letter word.");
    return;
  }

  let requestBody = JSON.stringify({
    game_id: currentGameId,
    guess: guess
  });

  console.log('Request body:', requestBody);





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


function submitGuessNEW() {
  let guess = document.getElementById('guessInput').value.toLowerCase();

  if (guess.length !== 5) {
    alert("Please enter a 5-letter word.");
    return;
  }

  fetch('/game/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      game_id: currentGameId,
      guess: guess
    })
  })
  .then(response => response.json())
  .then(data => {



    calculateAndDisplayFeedback(data.feedback);
    attempts = data.attempts_left;
    document.getElementById('attemptsLeft').textContent = `You have ${attempts} attempts left.`;

    attemptsList.push(guess);
    document.getElementById('guessInput').value = '';

    if (data.game_over) {
      endGame(data.is_win, data.correct_word);
    }
  });
}



// function endGameNEW(isWin, correctWord) {
//   document.getElementById('guessInput').disabled = true;
//   showSessionInfo();
//   updateSessionInfo(attempts, attemptsList);
//   document.getElementById('restartButton').style.display = 'block';
  
//   if (isWin) {
//     alert("Congratulations! You've guessed the word correctly!");
//   } else {
//     alert(`You've run out of attempts! The correct word was ${correctWord}.`);
//   }

//   updateLeaderboard();
// }

















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








// function calculateAndDisplayFeedbackNEW(feedback) {
//   let displayElement = document.getElementById('feedback');
//   let htmlContent = '<div class="attempt-box">';

//   feedback.forEach(item => {
//     let colorClass = (item.result === 'correct' ? 'green' : (item.result === 'present' ? 'yellow' : 'gray'));
//     htmlContent += `<span class="letter-box ${colorClass}">${item.letter}</span>`;
//   });

//   htmlContent += '</div>';
//   displayElement.innerHTML += `${htmlContent}<br/>`;
// }


// function getUserId() {
//     return `user-${Math.floor(Math.random() * 1000000)}`;
// }

// function updateSessionInfo(attemptsLeft, attemptsList) {
//     let sessionInfo = document.getElementById('sessionInfo');
//     let currentTime = new Date();
//     let timeTaken = endTimer();
//     let attemptsStr = attemptsList.join(', ');
//     let userId = getUserId();

//     sessionInfo.value += `User ID: ${userId} - Attempts: ${6 - attemptsLeft} - Date: ${currentTime.toLocaleDateString()} - Time: ${currentTime.toLocaleTimeString()} - Duration: ${timeTaken} seconds - Guesses: [${attemptsStr}]\n---\n`;
// }

// function showSessionInfo() {
//     document.getElementById('sessionInfo').style.display = 'block';
// }

// function startTimer() {
//     startTime = new Date();
// }

// function endTimer() {
//     endTime = new Date();
//     let timeDiff = (endTime - startTime) / 1000;
//     return Math.round(timeDiff);
// }

// function updateLeaderboard() {
//   fetch('/get-leaderboard/')
//     .then(response => response.json())
//     .then(data => {
//       // Update leaderboard UI here
//     });
// }
