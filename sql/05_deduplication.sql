-- =====================================================
-- Project: Retail Sales Analytics Platform
-- Script : 05_deduplication.sql
-- Purpose: Identify and remove exact duplicate records
-- =====================================================

USE DATABASE RETAIL_SALES_DB;
USE SCHEMA TRANSFORM;

-- 1. Check original record count
SELECT COUNT(*) AS ORIGINAL_RECORDS
FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_CLEAN;

-- 2. Identify exact duplicate records
SELECT
    *,
    COUNT(*) AS DUPLICATE_COUNT
FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_CLEAN
GROUP BY ALL
HAVING COUNT(*) > 1;

-- 3. Create a deduplicated table
CREATE OR REPLACE TABLE
    RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_DEDUP
AS
SELECT DISTINCT *
FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_CLEAN;

-- 4. Verify deduplicated record count
SELECT COUNT(*) AS DEDUPLICATED_RECORDS
FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_DEDUP;

-- 5. Verify no exact duplicates remain
SELECT COUNT(*) AS REMAINING_DUPLICATE_GROUPS
FROM (
    SELECT *
    FROM RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_DEDUP
    GROUP BY ALL
    HAVING COUNT(*) > 1
);
