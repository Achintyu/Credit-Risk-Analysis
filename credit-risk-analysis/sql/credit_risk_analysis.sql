-- Credit risk dataset storage and analysis script
-- Target dialect: PostgreSQL
-- Source file: data/featured/credit_risk_dataset_featured.csv

DROP TABLE IF EXISTS credit_risk_customers;

CREATE TABLE credit_risk_customers (
    person_age INTEGER,
    person_income INTEGER,
    person_home_ownership VARCHAR(20),
    person_emp_length NUMERIC(10, 2),
    loan_intent VARCHAR(30),
    loan_grade VARCHAR(5),
    loan_amnt INTEGER,
    loan_int_rate NUMERIC(10, 2),
    loan_status INTEGER,
    loan_percent_income NUMERIC(10, 4),
    cb_person_default_on_file VARCHAR(5),
    cb_person_cred_hist_length INTEGER,
    loan_to_income_ratio NUMERIC(10, 4),
    residual_income_after_loan INTEGER,
    employment_tenure_band VARCHAR(20),
    risk_level VARCHAR(10)
);

-- Load the enriched CSV into PostgreSQL.
-- Update the file path if needed for your machine or database server.
COPY credit_risk_customers
FROM 'data/featured/credit_risk_dataset_featured.csv'
WITH (
    FORMAT csv,
    HEADER true
);

-- Optional indexes for faster analysis queries.
CREATE INDEX idx_credit_risk_risk_level
    ON credit_risk_customers (risk_level);

CREATE INDEX idx_credit_risk_default_flag
    ON credit_risk_customers (cb_person_default_on_file);

CREATE INDEX idx_credit_risk_loan_amount
    ON credit_risk_customers (loan_amnt);


-- 1. High-risk customers
-- Returns customers labeled HIGH risk, ordered by largest loan burden.
SELECT
    person_age,
    person_income,
    loan_amnt,
    loan_int_rate,
    loan_grade,
    cb_person_default_on_file,
    loan_to_income_ratio,
    risk_level
FROM credit_risk_customers
WHERE risk_level = 'HIGH'
ORDER BY loan_to_income_ratio DESC, loan_amnt DESC;


-- 2. Average income by default history
-- Compares average applicant income between customers with and without past default.
SELECT
    cb_person_default_on_file AS default_flag,
    COUNT(*) AS customer_count,
    ROUND(AVG(person_income), 2) AS avg_income
FROM credit_risk_customers
GROUP BY cb_person_default_on_file
ORDER BY cb_person_default_on_file;


-- 3. Loan distribution summary
-- Shows how loan amounts are distributed overall.
SELECT
    COUNT(*) AS total_loans,
    MIN(loan_amnt) AS min_loan_amount,
    ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY loan_amnt), 2) AS q1_loan_amount,
    ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY loan_amnt), 2) AS median_loan_amount,
    ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY loan_amnt), 2) AS q3_loan_amount,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,
    MAX(loan_amnt) AS max_loan_amount
FROM credit_risk_customers;


-- 4. Loan distribution by risk level
-- Useful for seeing how loan sizes vary across LOW, MEDIUM, and HIGH risk customers.
SELECT
    risk_level,
    COUNT(*) AS customer_count,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,
    ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY loan_amnt), 2) AS median_loan_amount,
    MIN(loan_amnt) AS min_loan_amount,
    MAX(loan_amnt) AS max_loan_amount
FROM credit_risk_customers
GROUP BY risk_level
ORDER BY
    CASE risk_level
        WHEN 'HIGH' THEN 1
        WHEN 'MEDIUM' THEN 2
        WHEN 'LOW' THEN 3
        ELSE 4
    END;
