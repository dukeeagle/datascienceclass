-- /*
-- (Subqueries/CTEs, 10 pts) Find the actors/actresses who played in the largest number of movies. 
-- The result set may contain one or many persons. 
-- Return the category ('actor' or 'actress'), the name, and the number of appearances. 
-- Order the results by name (ascending). Use the people table to get the name of actors.
-- */
-- WITH actees AS (
--     SELECT
--         c.category,
--         c.person_id,
--         COUNT(c.person_id) AS num_appearances
--     FROM
--         crew as c, titles as t
--     WHERE 
--         c.title_id = t.title_id -- join 1
--         AND t.type = 'movie'
--         AND (c.category = 'actor'
--         OR c.category = 'actress')
--     GROUP BY
--         c.person_id
-- )

-- SELECT
--     p.name,
--     actees.category,
--     actees.num_appearances
-- FROM
--     actees, people as p
-- WHERE
--     p.person_id = actees.person_id
--     AND actees.num_appearances = (
--         SELECT
--             MAX(num_appearances)
--         FROM
--             actees
--     )
-- ORDER BY
--     p.name ASC;



WITH actors as (
    SELECT people.name,
        COUNT(crew.person_id) AS num_appearances,
        AVG(ratings.rating) AS average_rating
    FROM crew,
        titles,
        ratings,
        people
    WHERE crew.title_id = titles.title_id
        AND ratings.title_id = titles.title_id
        AND people.person_id = crew.person_id
        AND titles.type = "movie"
        AND (
            crew.category = "actor"
            OR crew.category = "actress"
        )
    GROUP BY crew.person_id
)
SELECT *
FROM actors
WHERE num_appearances = 5
    AND average_rating = (
        SELECT MAX(average_rating)
        FROM actors
        WHERE num_appearances = 5
    );