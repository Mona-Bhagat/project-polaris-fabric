# Project Polaris


## Enterprise SaaS Analytics Platform on Microsoft Fabric

Project Polaris is an end-to-end enterprise analytics platform designed and built on Microsoft Fabric for NimbusFlow, a fictional SaaS workflow automation company.

The project was structured as a full analytics-platform engagement rather than a standalone dashboard build. It covers solution architecture, synthetic source-system design, data ingestion, medallion-layer transformations, data-quality controls, business modelling, pipeline orchestration, semantic modelling and executive reporting.

All datasets are synthetic and were created exclusively for this project. No employer, customer or production data was used.

---

## Data Generation

A Python data generator was developed to create realistic synthetic SaaS data with historical customer behaviour.

## Engagement Overview

NimbusFlow required a unified analytics platform to support executive reporting across subscription revenue, product usage and customer health.

Operational data was assumed to be distributed across separate CRM, billing and product platforms, with inconsistent KPI definitions and no shared analytical layer.

Project Polaris was designed as a platform-modernisation engagement covering:

- Business requirements and KPI definition
- Source-system and data-model design
- Microsoft Fabric solution architecture
- Bronze, Silver and Gold data processing
- Data-quality monitoring and auditability
- Revenue and customer-health modelling
- Pipeline orchestration
- Direct Lake semantic modelling
- Power BI reporting
  

---

## Client Problem

NimbusFlow lacked a trusted, shared view of its customer and subscription lifecycle.

Key challenges included:

- Revenue metrics calculated independently by different teams
- No reconciled monthly MRR bridge
- Limited visibility of upgrades, downgrades and churn
- Product-usage data disconnected from commercial reporting
- No consistent method for identifying disengaged customers
- No operational record of data-quality issues
- Manual dependency management between transformation stages

## Engagement Objectives

The platform was designed to achieve five objectives:

1. Establish a governed analytical foundation in Microsoft Fabric
2. Create trusted definitions for MRR, ARR, churn and customer growth
3. Combine commercial and product-usage data at customer-month grain
4. Introduce reusable data-quality and audit controls
5. Deliver executive and operational reporting through a shared semantic model

## Scope of Delivery

### Architecture
- End-to-end Microsoft Fabric solution design
- OneLake and Lakehouse structure
- Medallion architecture
- Notebook and pipeline dependency design
- Direct Lake reporting architecture

### Data Engineering
- Synthetic source-data generator
- Bronze file ingestion
- Silver cleansing and standardisation
- Referential-integrity validation
- Business-rule validation
- Gold analytical modelling

### Data Quality and Controls
- Row-count reconciliation
- Duplicate detection
- Missing-value monitoring
- Foreign-key validation
- Business-rule testing
- Append-only audit history

### Business Modelling
- Customer-month MRR snapshots
- New, expansion, contraction and churned MRR
- ARR and revenue-retention metrics
- Monthly product-usage aggregation
- Credit-utilisation analysis
- Explainable customer-health classification

### Reporting
- Executive SaaS performance dashboard
- Product-usage dashboard
- Customer-health and churn-risk dashboard


### Delivery Approach

Project Polaris was developed using an engagement-style delivery approach.

The work progressed through the following stages:

1. Define the business scenario and decision-making requirements
2. Design source systems and synthetic business data
3. Establish the target Fabric architecture
4. Build the Bronze, Silver and Gold layers
5. Introduce data-quality and audit controls
6. Reconcile key business metrics
7. Orchestrate notebook execution through pipelines
8. Build the shared semantic model
9. Deliver executive and operational reporting
10. Document architectural decisions and lessons learned


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

## Data Quality Monitoring

The Bronze-to-Silver notebook writes operational metrics into notebook slv_data_quality_log

Possible statuses are: PASS, PASS_WITH_WARNINGS, FAIL. The table is append-only, allowing data-quality results to be reviewed across multiple pipeline executions


## Power BI Reports

The Direct Lake semantic model supports three connected analytical pages.

 - Executive SaaS Performance

   <img width="1047" height="591" alt="01-executive-summary" src="https://github.com/user-attachments/assets/279465cb-de61-4954-8a16-cc214428651c" />


 - Product Usage Analytics

   <img width="1045" height="580" alt="03-usage-analysis" src="https://github.com/user-attachments/assets/7e40f5b7-aded-4050-aa70-1b8e49a3565b" />


 - Customer Health and Churn Risk

   <img width="1040" height="575" alt="02-customer-health" src="https://github.com/user-attachments/assets/bd609401-b17f-4d64-9419-221ab18b227f" />



## Key Engineering Decisions
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



# Known Constraints and Future Roadmap

## Current Constraints

The current implementation uses manually uploaded synthetic source files and a development-only Fabric environment.

The solution does not currently include:

- Automated external source ingestion
- Dev/Test/Prod deployment pipelines
- Row-level security
- CI/CD integration
- Production alerting
- Capacity monitoring
- Incremental source ingestion

## Production Roadmap

A production implementation would extend the platform with:

- Automated API and database ingestion
- Parameterised pipelines
- Incremental and watermark-based loading
- Dev/Test/Prod workspace separation
- Deployment pipelines
- Security roles and access controls
- Failure notifications
- Capacity and performance monitoring
- Formal data contracts and ownership



## Disclaimer

NimbusFlow is a fictional company.

All datasets, company names, customer records and financial values were generated synthetically for learning and portfolio purposes.

No employer, customer or production data was used.




