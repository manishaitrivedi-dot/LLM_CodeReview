SELECT 
    customer_id,
    first_name,
    last_name,
    email,
    COUNT(order_id) AS total_orders,
    SUM(order_amount) AS total_spent,
    AVG(order_amount) AS avg_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2021-01-01' 
  AND o.order_date <= '2021-12-31'
  AND c.status = 'active'
GROUP BY customer_id;
