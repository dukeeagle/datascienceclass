/*(Simple subquery/CTE, 10 pts) Find the movie with the most actors and actresses (cumulatively). 
Unlike in question (3), you should return all such movies. Again, return the title_id, primary title and number of actors. 
Order by primary title (ascending).
*/
WITH actee_counts AS (
    SELECT
        t.title_id, 
        t.primary_title,
        COUNT(DISTINCT c.person_id) AS num_actees
    FROM
        titles AS t, crew AS c
    WHERE
        t.type = 'movie'
        AND t.title_id = c.title_id
        AND (c.category = 'actor' OR c.category = 'actress')
    GROUP BY
        t.title_id
)

SELECT
    title_id,
    primary_title,
    num_actees
FROM
    actee_counts
WHERE
    num_actees = (
        SELECT
            MAX(num_actees)
        FROM
            actee_counts
    )
ORDER BY
    primary_title ASC;