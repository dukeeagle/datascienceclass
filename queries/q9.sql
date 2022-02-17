/*(SQL Only: Recursive CTEs, 10 pts) Find the genres of movies with the highest average rating. 
Note that the text Action,Thriller should be treated as two genres (Action and Thriller). 
You may reuse the recursive CTE csv parser. Return the genre and the average rating. S
ort by average rating (descending) and genre (ascending) to break ties. 
Be sure to filter out the null genre (genres='\N').*/
WITH split(title_id, genre, str) AS (
    SELECT
        title_id,
        '', 
        genres || ',' 
    FROM (
        SELECT 
            title_id, genres
        FROM
            titles 
        WHERE 
            type = 'movie'
            AND genres != '\N'
    )
    UNION ALL 
    SELECT
        title_id,
        substr(str, 0, instr(str, ',')),
        substr(str, instr(str, ',')+1)
    FROM split 
    WHERE str!=''
)

SELECT
    split.title_id,
    split.genre,
    AVG(r.rating) as avg_rating
FROM
    split, ratings as r 
WHERE
    split.title_id = r.title_id
    AND split.genre != ""
    AND split.genre != "\N"
GROUP BY
    genre
ORDER BY
    avg_rating DESC,
    genre ASC;
