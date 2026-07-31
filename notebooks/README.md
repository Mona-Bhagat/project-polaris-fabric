This folder contains the Microsoft Fabric notebooks used in Project Polaris.

## Execution order

1. `nb_bronze_to_silver.ipynb`
   - Reads raw CSV files from the Bronze layer
   - Standardises data types and descriptive attributes
   - Removes duplicate customer records
   - Validates relationships and business rules
   - Writes Silver Delta tables
   - Appends data-quality results to the audit log

2. `nb_silver_to_gold.ipynb`
   - Converts subscription history into customer-month MRR snapshots
   - Calculates new, expansion, contraction and churned MRR
   - Produces the monthly MRR bridge and executive summary tables

3. `nb_gold_product_usage.ipynb`
   - Aggregates daily product usage to customer-month level
   - Calculates credit utilisation and usage trends
   - Combines product engagement with MRR
   - Produces an explainable customer-health classification

4. `nb_date_table.ipynb`
   - Creates reusable daily and monthly date dimensions

## Platform

The notebooks were developed and executed using Microsoft Fabric Spark
and write curated outputs as Delta tables in a Fabric Lakehouse.

All data used in this project is synthetic 
