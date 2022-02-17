-- Write your query here.
SELECT
    category,
    COUNT(DISTINCT person_id) AS num_actees
FROM
    crew
WHERE 
    category = 'actor'
    OR category = 'actress'
GROUP BY
    category;

