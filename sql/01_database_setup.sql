-- =====================================================
-- Project: Retail Sales Analytics Platform
-- Script : 01_database_setup.sql
-- Purpose: Create the database and required schemas
-- =====================================================

-- Select the project role
USE ROLE SNOWFLAKE_LEARNING_ROLE;

-- Select the existing warehouse
USE WAREHOUSE SNOWFLAKE_LEARNING_WH;

-- Create the project database
CREATE DATABASE IF NOT EXISTS RETAIL_SALES_DB;

-- Select the project database
USE DATABASE RETAIL_SALES_DB;

-- Create the required schemas
CREATE SCHEMA IF NOT EXISTS RAW;

CREATE SCHEMA IF NOT EXISTS TRANSFORM;

CREATE SCHEMA IF NOT EXISTS ANALYTICS;

-- Verify the schemas
SHOW SCHEMAS IN DATABASE RETAIL_SALES_DB;
