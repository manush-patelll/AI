# Database Query Optimization Cheat Sheet

This document outlines common SQL performance bottlenecks and their respective optimizations, ranging from basic indexing to solving the N+1 problem and handling functional scans.

---

## 1. Missing Index Optimization
**Scenario:** Filtering on a column that lacks an index results in a full table (sequential) scan.

* **Original Query:**
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM products WHERE price BETWEEN 1000 AND 2000;
    ```
* **Performance Impact:** * Execution Strategy: Sequential Scan
    * Execution Time: **0.456 ms**

### The Fix: B-Tree Index
```sql
CREATE INDEX idx_products_price ON products(price);
Result:

Execution Strategy: Index Scan

Execution Time: 0.182 ms (~60% improvement)

2. Solving the N+1 Problem
Scenario: Fetching a list of records and then performing a separate query for every individual record to fetch related data.

The Problematic Flow:

SELECT id, name FROM users; (Returns 100 users)

Loop through users: SELECT * FROM orders WHERE user_id = ?; (Executes 100 times)

Total Queries: 101

The Fix: SQL Joins
Combine the requests into a single database trip to reduce round-trip latency and overhead.

SQL

SELECT u.id, u.name, o.id AS order_id, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
Result: Total queries reduced to 1.

3. Function Breaking Index (SARGability)
Scenario: Applying a function (like LOWER()) to an indexed column in the WHERE clause prevents the database from using the standard index.

Problematic Query:

SQL

SELECT * FROM users WHERE LOWER(email) = 'manush@gmail.com';
The Fixes:
Data Normalization: Store all emails in lowercase during insertion/update.

SQL

SELECT id, email FROM users WHERE email = 'manush@gmail.com';
Functional Index: If you cannot change the data, index the result of the function.

SQL

CREATE INDEX idx_users_email_lower ON users(LOWER(email));
4. Inefficient Composite Index
Scenario: An index exists, but it doesn't cover the ORDER BY clause, forcing the database to perform an expensive "Filesort" step.

Query:

SQL

SELECT * FROM transactions 
WHERE status = 'completed' AND user_id = 500 
ORDER BY created_at DESC;
Existing Index: (status, user_id) — Supports filtering but not sorting.

The Fix: Covering Composite Index
Create an index that follows the order of operations: Filter Columns -> Sort Columns.

SQL

CREATE INDEX idx_transactions_user_status_created 
ON transactions(user_id, status, created_at DESC);
Result: Eliminates the manual sorting step by reading the index in order.

5. Leading Wildcard Searches
Scenario: Standard B-Tree indexes cannot be used for LIKE patterns starting with a wildcard (%text%).

Problematic Query:

SQL

SELECT * FROM products WHERE name LIKE '%iphone%';
Performance Impact: Forces a full table scan because the index cannot "seek" the start of the string.

The Fix: Trigram Index (PostgreSQL)
Trigram indexes break strings into 3-character chunks, allowing for efficient partial matches.

SQL

-- Ensure pg_trgm extension is enabled
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_products_name_trgm 
ON products USING GIN (name gin_trgm_ops);
Result: Moves from a Sequential Scan to a GIN Index Scan.
