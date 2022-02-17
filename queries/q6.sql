/* Find the actors/actresses with at least 5 movies that have the highest average ratings on their movies. 
Return the name, the number of titles and the average rating. 
Order the results by average rating (descending) and then name (ascending).
*/
WITH actees AS (
    SELECT
        c.category,
        c.person_id,
        COUNT(c.person_id) AS num_appearances
    FROM
        crew as c, titles as t, ratings as r
    WHERE 
        c.title_id = t.title_id -- join 1
        AND num_appearances >= 5
        AND (c.category = 'actor'
        OR c.category = 'actress')
        AND t.type = 'movie'
    GROUP BY
        c.person_id
)

SELECT
    p.name,
    actees.category,
    actees.num_appearances
FROM
    actees, people as p, titles as t, ratings as r
WHERE
    p.person_id = actees.person_id
ORDER BY
    actees.num_appearances DESC,
    p.name ASC
LIMIT 10;