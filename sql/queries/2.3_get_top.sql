WITH RECURSIVE
  cat_root AS (
    SELECT
      id,
      name,
      parent_id,
      id AS root_id,
      name AS root_name
    FROM
      categories
    WHERE
      parent_id IS NULL
    UNION ALL
    SELECT
      c.id,
      c.name,
      c.parent_id,
      cr.root_id,
      cr.root_name
    FROM
      categories c
      JOIN cat_root cr ON c.parent_id = cr.id
  )
SELECT
  p.name AS product_name,
  cr.root_name AS category_level_1,
  SUM(oi.count) AS total_sold
FROM
  order_items oi
  JOIN orders o ON oi.order_id = o.id
  JOIN products p ON oi.product_id = p.id
  JOIN cat_root cr ON p.category_id = cr.id
WHERE
  o.created_at >= NOW () - INTERVAL '1 month'
GROUP BY
  p.id,
  p.name,
  cr.root_id,
  cr.root_name
ORDER BY
  total_sold DESC
LIMIT
  5;