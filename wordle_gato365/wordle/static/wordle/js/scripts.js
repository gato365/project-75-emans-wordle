



let attemptsList = [];
let currentWordIndex = 0;
let attempts = 6;
let startTime, endTime;
let currentGameId = null;
let correctWord = '';



document.getElementById('startButton').addEventListener('click', startGame);
document.getElementById('restartButton').addEventListener('click', restartGame);
document.getElementById('guessInput').addEventListener('keypress', function (event) {
  if (event.key === "Enter") {
    submitGuess();
  }
});

document.getElementById('guessInput').addEventListener('input', function () {
  this.value = this.value.toLowerCase();
});


document.addEventListener('DOMContentLoaded', function () {
  let displayElement = document.getElementById('feedback');
  if (displayElement) {
    displayElement.innerHTML = '';
  }
});




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
  // Hide/Show Elements
  document.getElementById('restartButton').style.display = 'none'; // Hide the restart button
  document.getElementById('startButton').style.display = 'block'; // Show the start button
  document.getElementById('guessInput').style.display = 'none'; // Hide the guess input field
  document.getElementById('submitGuessButton').style.display = 'none'; // Hide the submit guess button
  document.getElementById('sessionInfo').style.display = 'none'; // Hide the session info

  // Reset/Initialize Values
  document.getElementById('feedback').innerHTML = ''; // Clear the feedback
  document.getElementById('attemptsLeft').textContent = ''; // Clear the attempts left text
  document.getElementById('attemptedWords').innerHTML = ''; // Clear the attempted words
  attempts = 6; // Reset the attempts
}
















// Begin Work on the following section:


async function submitGuess() {

  try {
    let guess = document.getElementById('guessInput').value.toLowerCase();

    if (guess.length !== 5) {
      alert("Please enter a 5-letter word.");
      return;
    }

    const response = await fetch('/submit_guess/', {  // Note the change in URL
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        game_id: currentGameId,
        guess: guess,
      })
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }




    const data = await response.json();
    console.log('this is Data:', data);



    console.log('this is data.feedback:', data.feedback);

    calculateAndDisplayFeedback(data.feedback);


    correctWord = data.correct_word;
    attempts = data.attempts_left;
    document.getElementById('attemptsLeft').textContent = `You have ${attempts} attempts left.`;

    attemptsList.push(guess);
    document.getElementById('guessInput').value = '';

    if (data.game_over) {
      endGame(data.is_win, data.correct_word);
    }


  } catch (error) {
    console.error('There was a problem submitting the guess:', error);
  }
}



function endGame(isWin, correctWord) {
  document.getElementById('guessInput').disabled = true;
  showSessionInfo();
  updateSessionInfo(attempts, attemptsList);
  document.getElementById('restartButton').style.display = 'block';

  if (isWin) {
    alert("Congratulations! You've guessed the word correctly!");
  } else {
    alert(`You've run out of attempts! The correct word was ${correctWord}.`);
  }


}


function calculateAndDisplayFeedback(feedback) {
  let displayElement = document.getElementById('feedback');
  let htmlContent = '<div class="attempt-box">';

  feedback.forEach(item => {
    let colorClass = (item.result === 'correct' ? 'green' : (item.result === 'present' ? 'yellow' : 'gray'));
    htmlContent += `<span class="letter-box ${colorClass}">${item.letter}</span>`;
  });

  htmlContent += '</div>';
  displayElement.innerHTML += `${htmlContent}<br/>`;
}



// End of the section to work on




async function updateSessionInfo(attemptsLeft, attemptsList) {

  try {




    let sessionInfo = document.getElementById('sessionInfo');
    let currentTime = new Date();
    let timeTaken = endTimer();
    let attemptsStr = attemptsList.join(', ');
    



    sessionInfo.value += `Word: ${correctWord} - Attempts: ${6 - attemptsLeft} - Date: ${currentTime.toLocaleDateString()} - Time: ${currentTime.toLocaleTimeString()} - Duration: ${timeTaken} seconds - Sequence Number: ${currentWordIndex + 1} - Guesses: [${attemptsStr}]\n---\n`;
  } catch (error) {
    console.error('There was a problem updating the session info:', error);
  }
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









