-- ==============================================================================
-- LAB EXERCISE: Trigger Design & Mutating Tables (ORA-04091)
-- Course: Advanced Database System
-- Ton Duc Thang University (TDTU)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. AI HALLUCINATION / MUTATING TEMPLATE (Passive Code Output)
-- Description: AI attempts to write a row-level trigger that queries the same 
-- table ("employees") that fired the trigger. This causes an immediate 
-- ORA-04091: table is mutating, trigger may not see it error.
-- ------------------------------------------------------------------------------
/*
[AI GENERATED CODE]:
CREATE OR REPLACE TRIGGER audit_salary_trigger
AFTER UPDATE OF salary ON employees
FOR EACH ROW
DECLARE
    v_avg_salary NUMBER;
BEGIN
    -- This query triggers ORA-04091 because the row is in the middle of modification
    SELECT AVG(salary) INTO v_avg_salary FROM employees;
    
    IF :NEW.salary > v_avg_salary * 1.5 THEN
        INSERT INTO salary_alerts(employee_id, alert_date, reason)
        VALUES(:NEW.employee_id, SYSDATE, 'Salary exceeds 150% of average');
    END IF;
END;
/
*/

-- ------------------------------------------------------------------------------
-- 2. AUDITING INSTRUCTIONS (For Student Auditor)
-- Task:
--   - Explain why Oracle bans row-level triggers from reading mutating tables.
--   - Refactor this trigger using a COMPOUND TRIGGER to separate row-level 
--     collection from statement-level validation, thus avoiding ORA-04091.
-- ------------------------------------------------------------------------------

-- ------------------------------------------------------------------------------
-- 3. EXPECTED STUDENT SOLUTION (Active Code Audit & Refactoring via Compound Trigger)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE TRIGGER audit_salary_trigger
FOR UPDATE OF salary ON employees
COMPOUND TRIGGER

    -- Define global collection to store row IDs and values in statement state
    TYPE t_emp_salary IS RECORD (
        employee_id employees.employee_id%TYPE,
        new_salary  employees.salary%TYPE
    );
    TYPE t_emp_list IS TABLE OF t_emp_salary;
    g_updated_employees t_emp_list := t_emp_list();
    g_avg_salary NUMBER;

    -- Phase 1: Before Statement - Pre-calculate global averages
    BEFORE STATEMENT IS
    BEGIN
        SELECT AVG(salary) INTO g_avg_salary FROM employees;
    END BEFORE STATEMENT;

    -- Phase 2: Each Row - Buffer row changes in-memory without querying table
    AFTER EACH ROW IS
    BEGIN
        g_updated_employees.EXTEND;
        g_updated_employees(g_updated_employees.LAST).employee_id := :NEW.employee_id;
        g_updated_employees(g_updated_employees.LAST).new_salary  := :NEW.salary;
    END AFTER EACH ROW;

    -- Phase 3: After Statement - Safe validation as table is no longer mutating
    AFTER STATEMENT IS
    BEGIN
        FOR i IN 1..g_updated_employees.COUNT LOOP
            IF g_updated_employees(i).new_salary > g_avg_salary * 1.5 THEN
                INSERT INTO salary_alerts(employee_id, alert_date, reason)
                VALUES(
                    g_updated_employees(i).employee_id, 
                    SYSDATE, 
                    'Salary exceeds 150% of average (Verified Avg: ' || g_avg_salary || ')'
                );
            END IF;
        END LOOP;
    END AFTER STATEMENT;

END audit_salary_trigger;
/