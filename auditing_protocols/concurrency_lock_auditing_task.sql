-- ==============================================================================
-- LAB EXERCISE: Concurrency Control & Lock Neglect (Race Conditions)
-- Course: Advanced Database System / DBMS
-- Ton Duc Thang University (TDTU)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. AI HALLUCINATION / UNSAFE TRANSACTION (Passive Code Output)
-- Description: AI wrote an automated balance transfer block but neglected 
-- concurrency locks. If two requests for p_from execute at the exact same 
-- millisecond, both read the original balance before writing, leading to double-spending.
-- ------------------------------------------------------------------------------
/*
[AI GENERATED CODE]:
CREATE OR REPLACE PROCEDURE process_transfer(
    p_from IN INT,
    p_to IN INT,
    p_amount IN NUMBER
) AS
    v_balance NUMBER;
BEGIN
    -- Unsafe read: Balance checked without pessimistic locking
    SELECT balance INTO v_balance FROM bank_accounts WHERE id = p_from;
    
    IF v_balance >= p_amount THEN
        UPDATE bank_accounts SET balance = balance - p_amount WHERE id = p_from;
        UPDATE bank_accounts SET balance = balance + p_amount WHERE id = p_to;
        COMMIT;
    ELSE
        ROLLBACK;
    END IF;
END;
/
*/

-- ------------------------------------------------------------------------------
-- 2. AUDITING INSTRUCTIONS (For Student Auditor)
-- Task:
--   - Identify how a race condition can cause double-spending.
--   - Inject pessimistic concurrency locking (FOR UPDATE) to block concurrent 
--     transactions until the lock owner commits.
-- ------------------------------------------------------------------------------

-- ------------------------------------------------------------------------------
-- 3. EXPECTED STUDENT SOLUTION (Active Code Audit & Pessimistic Lock Injection)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE process_transfer(
    p_from IN INT,
    p_to IN INT,
    p_amount IN NUMBER
) AS
    v_balance NUMBER;
BEGIN
    -- Crucial: FOR UPDATE statement locks the record and serializes concurrent calls
    SELECT balance INTO v_balance 
    FROM bank_accounts 
    WHERE id = p_from 
    FOR UPDATE;
    
    IF v_balance >= p_amount THEN
        UPDATE bank_accounts 
        SET balance = balance - p_amount 
        WHERE id = p_from;
        
        UPDATE bank_accounts 
        SET balance = balance + p_amount 
        WHERE id = p_to;
        
        COMMIT;
    ELSE
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20001, 'Insufficient funds for transfer.');
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/