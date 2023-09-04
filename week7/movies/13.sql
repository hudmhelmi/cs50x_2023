-- Select name from specific movies
SELECT DISTINCT(name) FROM people
JOIN stars ON stars.person_id = people.id
JOIN movies ON movies.id = stars.movie_id
-- Find movies starred by Kevin Bacon
WHERE movies.id IN
(
    SELECT movies.id FROM movies
    JOIN stars ON stars.movie_id = movies.id
    JOIN people ON people.id = stars.person_id
    WHERE people.name = 'Kevin Bacon' AND people.birth = 1958
)
AND people.name != 'Kevin Bacon'