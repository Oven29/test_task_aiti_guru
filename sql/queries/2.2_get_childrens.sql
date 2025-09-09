SELECT
    c.id AS category_id,
    c.name AS category_name,
    COUNT(child.id) AS children_count
FROM
    categories c
    LEFT JOIN categories child ON c.id = child.parent_id
GROUP BY
    c.id,
    c.name
ORDER BY
    children_count DESC;