-- ==============================================================================
-- LAB EXERCISE: Algorithmic Complexity Auditing (O(N^2) to O(N))
-- Course: Advanced Database System
-- Ton Duc Thang University (TDTU)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. AI HALLUCINATION / UNOPTIMIZED TEMPLATE (Passive Code Output)
-- Description: AI generated a nested loop subquery to find the most expensive 
-- accounts for each branch. This triggers a full table scan of the "accounts" 
-- table for every single row processed.
-- ------------------------------------------------------------------------------
/* [AI GENERATED CODE]:
SELECT account_id, branch_id, balance 
FROM accounts a1
WHERE balance = (
    SELECT MAX(balance) 
    FROM accounts a2 
    WHERE a1.branch_id = a2.branch_id
);
*/

-- ------------------------------------------------------------------------------
-- 2. AUDITING INSTRUCTIONS (For Student Auditor)
-- Task:
--   - Analyze the execution plan. Notice the O(N^2) performance overhead.
--   - Identify how a table scan is being nested inside another table scan.
--   - Refactor this subquery using SQL Window Functions (Analytical Partitioning)
--     to reduce the complexity to a single O(N) heap pass.
-- ------------------------------------------------------------------------------

-- ------------------------------------------------------------------------------
-- 3. EXPECTED STUDENT SOLUTION (Active Code Audit & Refactoring)
-- Key requirements: Use RANK() or DENSE_RANK() with PARTITION BY.
-- ------------------------------------------------------------------------------
WITH RankedAccounts AS (
    SELECT 
        account_id, 
        branch_id, 
        balance,
        DENSE_RANK() OVER (
            PARTITION BY branch_id 
            ORDER BY balance DESC
        ) as balance_rank
    FROM accounts
)
SELECT account_id, branch_id, balance
FROM RankedAccounts
WHERE balance_rank = 1;
