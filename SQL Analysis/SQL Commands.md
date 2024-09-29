### Proper Process (actual lines to get into the database)
Format: mysql -u _username_ -p -h _hostname_ -P 3306 _Database_
mysql -u xzk7bhm1ba4tb18p -p -h ixnzh1cxch6rtdrx.cbetxkdyhwsb.us-east-1.rds.amazonaws.com -P 3306 n907uopch8fsfzxz
Password: wojozr7s3upemvu6

SHOW TABLES;
SELECT * FROM wordle_game; <!-- Outcome of the game -->
SELECT * FROM users_customuser; <!-- Displays Actual User -->

<!-- Get current directory in sql -->
system pwd;

<!-- Run a file in the sql -->
source query_who_played_1.sql
source query_number_games_played_2.sql