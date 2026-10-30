-- =====================================================
-- Project: Retail Sales Analytics Platform
-- Script : 02_data_ingestion.sql
-- Purpose: Verify and review raw retail sales data
-- =====================================================

-- Select the project database and schema
USE DATABASE RETAIL_SALES_DB;
USE SCHEMA RAW;

-- 1. Review the raw dataset
SELECT *
FROM RETAIL_SALES_DB.RAW.RETAIL_ORDERS_RAW
LIMIT 5;

-- 2. Check the total number of records
SELECT COUNT(*) AS TOTAL_RECORDS
FROM RETAIL_SALES_DB.RAW.RETAIL_ORDERS_RAW;

-- 3. Review the table structure
DESCRIBE TABLE RETAIL_SALES_DB.RAW.RETAIL_ORDERS_RAW;

-- 4. Check the order date range
SELECT
    MIN(ORDER_DATE) AS FIRST_ORDER_DATE,
    MAX(ORDER_DATE) AS LAST_ORDER_DATE
FROM RETAIL_SALES_DB.RAW.RETAIL_ORDERS_RAW;
