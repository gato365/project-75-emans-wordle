Tournament Mode
1. 5 words lighting rounds
2. 2 hours 
3. Should be done in 1 day
4. General Location for Tournament in Building foyer with donuts and coffee
Bragging rights
5. Second Competition - analysis of game results
    
6. UI/UX Design
    a. Leaderboard day after Tournament
    b. Login without cal poly information as a group
    c. words are random but have characteristics of easy. medium, hard
    d. Maximum time between words is 5 minutes 
    e. Work in teams of 2-4
    f. Let group connect to single user account
    g. specific time for tournament 
    h. secret password so that I can ensure people get the code who attend the tournament
    i. 2 hours to complete the tournament
    j. Students cannot skip
    h. a scoring mechanism is created based on words, time to completion, and number of words completed

## -------------------------------------------------------------------
The following is based on the 
General steps for playing tournament:

1. Clcik on tournament mode
2. Logs in with group information
3. Once logged in the tournament, they will see Welcome to the Fall 2024 STAT theWurdz Tournament
4. A timer will count down exactly at 10 am that day 
(Words will be randomly selected from 3 categories: easy, medium, hard, 2 easy, 2 medium, 1 hard in which the order will be random)
5. They will see their 1st word if they get the word correct within the 6 attempts they will move on to the next word and be given a 1 for that word, they will see a total of 5 words
6. If they get the word wrong on the sixth attempt, they will be given a new word and will be given a 0 for that word
7. If they complete the tournament before the 2 hours are up the game will return to the home screen
8. If they do not complete the tournament in the 2 hours, the game will return to the home screen noting the score and action



# Tournament Mode User Story - theWurdz Fall 2024

## Prerequisites
- Tournament is scheduled for specific date/time (e.g., Fall 2024 at 10 AM)
- Words database is pre-populated with categorized words (easy, medium, hard)
- Access code has been distributed to participants

## User Flow

### 1. Tournament Access
- User navigates to main application
- Clicks "Tournament Mode" button in navigation
- System checks if tournament is currently active
  - If not active: Shows countdown to tournament start
  - If active: Proceeds to team login

### 2. Team Registration/Login
- Team enters:
  - Team name (required)
  - Number of team members (2-4 players)
  - Tournament access code (required)
  - Team member names and Cal Poly email addresses
- System validates:
  - Team size constraints
  - Access code correctness
  - No duplicate team members across teams
  - Email domain verification (@calpoly.edu)

### 3. Tournament Lobby
- Display: "Welcome to the Fall 2024 STAT theWurdz Tournament"
- Show:
  - Team information
  - Current team members present
  - Tournament rules
  - Countdown timer to 10 AM start
  - Number of teams registered
- System locks registration 5 minutes before start time

### 4. Tournament Initialization
- At exactly 10 AM:
  - All teams simultaneously start
  - Word selection process:
    - 2 Easy words (randomly selected)
    - 2 Medium words (randomly selected)
    - 1 Hard word (randomly selected)
    - Random ordering of difficulty levels
  - Initialize team score tracking
  - Start 2-hour tournament timer

### 5. Gameplay Mechanics
For each word:
- Display current word position (1/5, 2/5, etc.)
- Show difficulty level of current word
- Allow 6 attempts per word
- Track:
  - Time spent on each word
  - Number of attempts used
  - Success/failure status

Scoring System:
- Successful word completion (within 6 attempts) = 1 point
- Failed word (after 6 attempts) = 0 points
- Additional metrics:
  - Time to completion
  - Number of attempts used
  - Difficulty level completed

### 6. Word Progression
Success Case:
- Word correctly guessed within 6 attempts
- Award 1 point
- Show success animation/message
- Progress to next word after 5-second delay

Failure Case:
- Six unsuccessful attempts
- Record 0 points
- Show correct word
- Progress to next word after 5-second delay

### 7. Tournament Completion
Normal Completion:
- All 5 words attempted
- Display:
  - Final score (X/5)
  - Time taken
  - Success rate by difficulty
  - Return to home screen
  - Option to view leaderboard

Time Limit Exceeded:
- At 2-hour mark:
  - Force-end current word attempt
  - Record partial completion
  - Display:
    - Partial score
    - Number of words completed
    - Time expired message
    - Return to home screen

### 8. Post-Tournament
- Display final tournament statistics:
  - Team's final score
  - Words completed
  - Time taken
  - Comparison to other teams (if all finished)
- Option to:
  - View full leaderboard
  - See detailed team performance
  - Download team results
  - Return to home screen

## Technical Requirements
- Real-time synchronization of tournament start
- Secure storage of tournament progress
- Handling of:
  - Network disconnections
  - Browser refreshes
  - Accidental closures
- Rate limiting for word submissions
- Anti-cheating measures
- Real-time leaderboard updates

## Data Collection
Track per team:
- Word completion times
- Number of attempts per word
- Success rate by difficulty level
- Overall completion time
- Team size impact on performance
- Pattern of guesses

## Error Handling
- Connection loss during tournament
- Invalid word submissions
- Team member disconnections
- Browser refresh/closure
- Server issues



----------------------------------------------------

