# Data Dictionary – Retail Sales Analytics Platform

## 1. Overview

This document describes the structure of the cleaned retail sales dataset stored in:

`RETAIL_SALES_DB.TRANSFORM.RETAIL_SALES_CLEAN`

The table contains 22 columns covering order information, customer details, product information, shipping details, and sales metrics.

## 2. Table Information

| Property | Description |
|---|---|
| Database | RETAIL_SALES_DB |
| Schema | TRANSFORM |
| Table | RETAIL_SALES_CLEAN |
| Total Columns | 22 |
| Original Records | 9,995 |

## 3. Column Definitions

### Order Information

| Column | Data Type | Description |
|---|---|---|
| ORDER_ID | NUMBER(10,0) | Numeric order identifier extracted from the original order ID. |
| ORDER_DATE | DATE | Date when the customer placed the order. |
| SHIP_DATE | DATE | Date when the order was shipped. |
| SHIP_MODE | VARCHAR(200) | Shipping method selected for the order. |
| ORDER_YEAR | NUMBER(4,0) | Year extracted from the original order ID. |
| DAYS_TO_SHIP | NUMBER(3,0) | Number of days between order date and shipping date. |

### Customer Information

| Column | Data Type | Description |
|---|---|---|
| CUSTOMER_ID | NUMBER(10,0) | Numeric customer identifier. |
| CUSTOMER_NAME | VARCHAR(300) | Name of the customer. |
| SEGMENT | VARCHAR(100) | Customer segment, such as Consumer, Corporate, or Home Office. |

### Geographic Information

| Column | Data Type | Description |
|---|---|---|
| COUNTRY | VARCHAR(100) | Country associated with the transaction. |
| CITY | VARCHAR(100) | City associated with the transaction. |
| STATE | VARCHAR(100) | State associated with the transaction. |
| POSTAL_CODE | NUMBER(10,0) | Postal code associated with the transaction. |
| REGION | VARCHAR(100) | Geographic region associated with the transaction. |

### Product Information

| Column | Data Type | Description |
|---|---|---|
| PRODUCT_ID | NUMBER(10,0) | Numeric product identifier. |
| CATEGORY | VARCHAR(100) | Main product category. |
| SUB_CATEGORY | VARCHAR(100) | Product sub-category. |

### Sales Information

| Column | Data Type | Description |
|---|---|---|
| PRICE | NUMBER(10,4) | Unit price of the product. |
| QUANTITY | NUMBER(3,0) | Number of units purchased. |
| DISCOUNT | NUMBER(7,2) | Discount rate applied to the product, represented as a decimal value. |
| SALES | NUMBER(15,5) | Gross sales before applying discounts. |
| NET_SALES | NUMBER(15,5) | Sales amount after applying discounts. |

## 4. Business Calculations

### Gross Sales

Calculates the total product value before discounts.

```sql
SALES = PRICE * QUANTITY
```

### Discount Amount

Calculates the monetary discount applied to the transaction.

```sql
DISCOUNT_AMOUNT = SALES * DISCOUNT
```

### Net Sales

Calculates the final sales value after discounts.

```sql
NET_SALES = PRICE * QUANTITY * (1 - DISCOUNT)
```

### Shipping Duration

Calculates the number of days between order placement and shipping.

```sql
DAYS_TO_SHIP = DATEDIFF('DAY', ORDER_DATE, SHIP_DATE)
```

## 5. Data Transformation Notes

The project uses Snowflake SQL UDFs to transform selected fields:

| UDF | Transformed Column | Description |
|---|---|---|
| GET_ORDER_ID | ORDER_ID | Extracts the numeric order identifier. |
| GET_CUSTOMER_ID | CUSTOMER_ID | Extracts the numeric customer identifier. |
| GET_PRODUCT_ID | PRODUCT_ID | Removes non-numeric characters from the product identifier. |
| GET_ORDER_YEAR | ORDER_YEAR | Extracts the year from the original order ID. |
| GET_DAYS_TO_SHIP | DAYS_TO_SHIP | Calculates shipping duration. |
| GET_SALES | SALES | Calculates gross sales. |

## 6. Data Quality Notes

The project performs validation checks for:

- Missing values in important business columns.
- Invalid prices and quantities.
- Discount values outside the valid range.
- Invalid order and shipping dates.
- Incorrect gross and net sales calculations.
- Duplicate transaction records.

The deduplicated dataset contains 9,994 records.

## 7. Important Notes

- All 22 columns are defined as nullable (`Y`) in the Snowflake table metadata.
- The discount column stores decimal discount rates, such as 0.20 for 20%.
- PRICE represents the unit price, not the total transaction value.
- SALES represents gross sales, whereas NET_SALES represents sales after discounts.
- ORDER_YEAR is derived using the original order identifier.
- POSTAL_CODE is stored as a numeric column.

