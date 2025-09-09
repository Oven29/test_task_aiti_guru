SELECT
    u.name AS customer_name,
    SUM(o.amount) AS total_amount
FROM
    users u
    JOIN orders o ON u.id = o.user_id
GROUP BY
    u.name
ORDER BY
    total_amount DESC;