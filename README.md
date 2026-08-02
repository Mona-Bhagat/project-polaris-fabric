# Project Polaris


## Enterprise SaaS Analytics Platform on Microsoft Fabric

Project Polaris is an end-to-end enterprise analytics platform designed and built on Microsoft Fabric for NimbusFlow, a fictional SaaS workflow automation company.

The platform combines subscription revenue, customer data and product-usage activity into a governed analytical solution using OneLake, Lakehouse architecture, Delta tables, PySpark notebooks, Data Factory pipelines, Direct Lake and Power BI.

All data used in this project is synthetic. The project contains no employer, customer or production data.

---

## Business Scenario

NimbusFlow provides workflow automation and API integration services through monthly subscription plans.

Its data is distributed across separate operational domains:

- Customer and account information
- Subscription billing
- Product usage
- Plan and pricing information

This creates inconsistent definitions of recurring revenue, customer growth, churn and product adoption.

Project Polaris was designed to provide a trusted analytical platform for answering questions such as:

- How is monthly recurring revenue changing?
- What is driving MRR growth or contraction?
- Which customers are using the platform most heavily?
- Which customers are showing signs of disengagement?
- How much recurring revenue is associated with at-risk customers?

---

## Solution Architecture

The platform follows a medallion architecture:

<img width="1205" height="562" alt="project-polaris-architecture png" src="https://github.com/user-attachments/assets/1a7374f3-c1fa-41ec-bad1-2e34abdc1af3" />

## Medallion Architecture

 - Bronze - Raw CSV extracts are stored in the Lakehouse Files section without transformation. The Bronze layer preserves source fidelity and provides a replayable ingestion point.

 - Silver - Fabric PySpark notebooks clean and validate the source data before writing curated Delta tables.

 - Gold - The Gold layer converts operational entities into business-ready analytical models.

## Technology Stack
 - Microsoft Fabric
 - OneLake
 - Fabric Lakehouse
 - Delta Lake
 - Fabric Data Factory
 - Fabric Notebooks
 - PySpark
 - Python
 - Direct Lake
 - Power BI
 - DAX
 - GitHub
 - Visual Studio Code

## Data Generation

A Python data generator was developed to create realistic synthetic SaaS data with historical customer behaviour.
  

## Data Quality Monitoring

The Bronze-to-Silver notebook writes operational metrics into notebook slv_data_quality_log

Possible statuses are: PASS, PASS_WITH_WARNINGS, FAIL. The table is append-only, allowing data-quality results to be reviewed across multiple pipeline executions

## Pipeline Orchestration

The Fabric Data Factory pipeline executes the notebooks in dependency order:

Downstream notebooks run only after the preceding activity succeeds.
This prevents Gold analytical tables from being refreshed when an upstream transformation fails.

## Power BI Reports

The Direct Lake semantic model supports three connected analytical pages.

 - Executive SaaS Performance

 - Product Usage Analytics

 - Customer Health and Churn Risk


##  Engineering Decisions
 - Why a Lakehouse?

   The Lakehouse supports raw files, scalable Spark transformations and Delta tables within a single Fabric data platform.

 - Why Bronze, Silver and Gold?

   The separation preserves source data, centralises cleaning and validation, and provides stable business-ready datasets for reporting.

 - Why PySpark?

   PySpark was used for repeatable transformations across more than 349,000 daily usage events and for implementing relationship and business-rule validations.

 - Why Direct Lake?

    Direct Lake allows Power BI to query OneLake Delta tables through a shared semantic model without importing another copy of the data into the report.

 - Why customer-month snapshots?

    Recurring-revenue movements depend on comparing each customer's current MRR with the previous month. The customer-month grain provides a reusable basis for MRR bridging, churn analysis     and customer-health reporting.




## Lessons Learned

This project reinforced several practical lessons:

- Successful pipeline execution does not guarantee trusted data.
- Data-quality results should be recorded alongside transformation outputs.
- Subscription status and subscription history must be modelled separately from current customer status.
- Churn is an event, while inactivity is an ongoing state.
- Gold tables should represent business concepts rather than copies of source-system tables.
- Direct Lake separates semantic-model development from thin-report development.
- Visual validation can reveal business-logic defects that technical validation may not detect.



## Disclaimer

NimbusFlow is a fictional company.

All datasets, company names, customer records and financial values were generated synthetically for learning and portfolio purposes.

No employer, customer or production data was used.




