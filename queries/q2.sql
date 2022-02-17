SELECT 
        t.title_id, t.primary_title, r.rating
FROM 
        titles as t, ratings as r
WHERE
        t.title_id = r.title_id
        AND t.genres LIKE '%action%'
        AND t.premiered == 2021
        AND t.type = 'tvSeries'
        AND r.rating >= 8
        AND r.votes >= 100
ORDER BY
        r.rating DESC,
        t.primary_title ASC;
