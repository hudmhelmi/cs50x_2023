-- SQL query to list the names of all songs in increasing order of tempo.
SELECT name FROM songs WHERE danceability > 0.75 AND energy > 0.75 AND valence > 0.75;