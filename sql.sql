-- 1)
SELECT
    tbl1.*,
    CASE WHEN tbl2.numbers IS NULL THEN 0 ELSE tbl2.numbers END AS numbers
FROM
    loan tbl1
LEFT JOIN
(
    SELECT
        loan_no,
        COUNT(1) AS numbers
    FROM borrower
    GROUP BY loan_no
) AS tbl2
ON tbl1.loan_no = tbl2.loan_no

-- 2)
SELECT
    *
FROM
(
    SELECT
        tbl1.*,
        CASE WHEN tbl2.numbers IS NULL THEN 0 ELSE tbl2.numbers END AS numbers
    FROM
        loan tbl1
    LEFT JOIN
    (
        SELECT
            loan_no,
            COUNT(1) AS numbers
        FROM borrower
        GROUP BY loan_no
    ) AS tbl2
    ON tbl1.loan_no = tbl2.loan_no
) as tbl3
WHERE tbl3.numbers > 0