WITH 
excellent_art (primary_title, premiered, type, rating, votes) AS (
    SELECT 
        t.primary_title, t.premiered, t.type, r.rating, r.votes
    FROM 
        titles AS t, ratings AS r
    WHERE
        t.title_id = r.title_id -- Join condition 
        AND (t.type = 'movie' OR t.type = 'tvSeries')
        AND r.rating >= 8 AND r.votes >= 100 AND t.premiered == 2021
)
SELECT
    type, primary_title, rating,
    RANK() OVER (PARTITION BY type ORDER BY rating DESC) as rank
FROM 
    excellent_art
ORDER BY
    type ASC,
    rating DESC,
    primary_title ASC;