-- =====================================================
-- Project: Retail Sales Analytics Platform
-- Script : 07_data_quality_checks.sql
-- Purpose: Validate data quality and financial accuracy
-- =====================================================

USE DATABASE RETAIL_SALES_DB;
USE SCHEMA TRANSFORM;

-- 1. Verify total records
SELECT COUNT(*) AS TOTAL_RECORDS
FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_DEDUP;

-- 2. Check duplicate records
SELECT COUNT(*) AS DUPLICATE_GROUPS
FROM (
    SELECT *
    FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_DEDUP
    GROUP BY ALL
    HAVING COUNT(*) > 1
);

-- 3. Check NULL values in important columns
SELECT
    COUNT_IF(ORDER_ID IS NULL) AS NULL_ORDER_ID,
    COUNT_IF(ORDER_DATE IS NULL) AS NULL_ORDER_DATE,
    COUNT_IF(CUSTOMER_ID IS NULL) AS NULL_CUSTOMER_ID,
    COUNT_IF(PRODUCT_ID IS NULL) AS NULL_PRODUCT_ID,
    COUNT_IF(PRICE IS NULL) AS NULL_PRICE,
    COUNT_IF(QUANTITY IS NULL) AS NULL_QUANTITY,
    COUNT_IF(DISCOUNT IS NULL) AS NULL_DISCOUNT
FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_DEDUP;

-- 4. Validate price and quantity
SELECT COUNT(*) AS INVALID_PRICE_QUANTITY
FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_DEDUP
WHERE PRICE <= 0 OR QUANTITY <= 0;

-- 5. Validate discount values
SELECT COUNT(*) AS INVALID_DISCOUNTS
FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_DEDUP
WHERE DISCOUNT < 0 OR DISCOUNT > 1;

-- 6. Validate order and shipping dates
SELECT COUNT(*) AS INVALID_SHIPPING_DATES
FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_DEDUP
WHERE SHIP_DATE < ORDER_DATE;

-- 7. Validate shipping duration
SELECT COUNT(*) AS INVALID_SHIPPING_DURATION
FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_DEDUP
WHERE DAYS_TO_SHIP != DATEDIFF('DAY', ORDER_DATE, SHIP_DATE);

-- 8. Validate gross sales calculation
SELECT COUNT(*) AS INVALID_GROSS_SALES
FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_DEDUP
WHERE ROUND(SALES, 5) != ROUND(PRICE * QUANTITY, 5);

-- 9. Validate net sales calculation
SELECT COUNT(*) AS INVALID_NET_SALES
FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_DEDUP
WHERE ROUND(NET_SALES, 5) !=
      ROUND(PRICE * QUANTITY * (1 - DISCOUNT), 5);

-- 10. Financial reconciliation
SELECT
    ROUND(SUM(SALES), 2) AS TOTAL_GROSS_SALES,
    ROUND(SUM(SALES * DISCOUNT), 2) AS TOTAL_DISCOUNT,
    ROUND(SUM(NET_SALES), 2) AS TOTAL_NET_SALES,
    ROUND(
        SUM(SALES) - SUM(SALES * DISCOUNT) - SUM(NET_SALES),
        2
    ) AS RECONCILIATION_DIFFERENCE
FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_DEDUP;



-- Expected results based on your earlier validation:

--      Validation	                Expected result
-- Total records	                      9,994
-- Duplicate groups	                      0
-- Invalid prices / quantities	          0
-- Invalid discounts	                    0
-- Invalid shipping dates	                0
-- Invalid shipping duration	            0
-- Invalid gross sales	                  0
-- Invalid net sales	                    0
-- Reconciliation difference	           $0.00
