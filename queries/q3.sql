/*
 Find the movie (titles.type=movie) with the most actors and actresses (cumulatively).
 If multiple movies are tied, return the one with the alphabetically smallest primary title.
 Return the title_id, primary title, and number of actors and actresses (cumulatively).
*/
SELECT
    t.title_id, t.primary_title,
    COUNT(DISTINCT c.person_id) AS num_actees
FROM
    titles AS t, crew AS c
WHERE
    t.type = 'movie'
    AND t.title_id = c.title_id
    AND (c.category = 'actor' OR c.category = 'actress')
GROUP BY
    t.title_id
ORDER BY
    num_actees DESC,
    t.primary_title ASC
LIMIT 1;