SELECT 
    u.username,
    u.password,    -- ❌ Exposing password in query
    SUM(o.amount) AS total_spent
FROM users u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date >= '2020-01-01'
  AND o.order_date <= '2025-12-31'
GROUP BY u.username, u.password
ORDER BY total_spent DESC
LIMIT 1000000;   -- ❌ Extremely high limit
