
## Solution Architecture

Project Polaris uses Microsoft Fabric to process synthetic CRM, billing and product-usage data through Bronze, Silver and Gold layers.

Raw source extracts are preserved in OneLake, PySpark notebooks perform cleansing and analytical transformations, and Fabric Data Factory orchestrates execution. Gold Delta tables are exposed through a Direct Lake semantic model for Power BI reporting.


<img width="1205" height="562" alt="project-polaris-architecture png" src="https://github.com/user-attachments/assets/ae3e4802-b28a-421b-af1f-6415d19a0d9a" />

