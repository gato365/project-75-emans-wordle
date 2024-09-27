SELECT 
    users_customuser.username,
    COUNT(wordle_game.id) AS games_played
FROM 
    wordle_game
JOIN 
    users_customuser
ON 
    wordle_game.user_id = users_customuser.id
WHERE 
    users_customuser.username NOT LIKE '%user%'
GROUP BY 
    users_customuser.username
ORDER BY 
    games_played DESC;