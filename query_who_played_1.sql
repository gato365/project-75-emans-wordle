SELECT 
    wordle_game.id AS game_id,
    wordle_game.user_id,
    users_customuser.username
FROM 
    wordle_game
JOIN 
    users_customuser
ON 
    wordle_game.user_id = users_customuser.id;