
## Solution Architecture

Project Polaris uses Microsoft Fabric to process synthetic CRM, billing and product-usage data through Bronze, Silver and Gold layers.

Raw source extracts are preserved in OneLake, PySpark notebooks perform cleansing and analytical transformations, and Fabric Data Factory orchestrates execution. Gold Delta tables are exposed through a Direct Lake semantic model for Power BI reporting.


<img width="1053" height="500" alt="project-polaris-architecture png" src="https://github.com/user-attachments/assets/3ea80f99-8998-42c2-8d95-3bed975856a3" />



