📊 Data Pipeline QA Dashboard

An interactive Streamlit web application designed to automate the Quality Assurance (QA) process by validating internal project management records against live API data feeds.

💡 The Business Problem

In modern data and marketing operations, ensuring data parity between planning tools (like ClickUp, Asana, or Jira) and actual data warehouses (fed by APIs like Supermetrics or Fivetran) is a highly manual, error-prone process. This dashboard automates that workflow. It instantly identifies missing assets, duplicate entries, data entry errors, and date mismatches, saving hours of manual validation and ensuring data integrity.

Note: This repository contains a "clean room" version of the architecture. To protect proprietary company data, the database connections (Snowflake) have been replaced with a local mock-data generator. The UI, logic, and data structures reflect the original enterprise deployment.

✨ Features

Automated Discrepancy Detection: Instantly flags assets that exist in the PM tool but are missing from the API feed (and vice versa).

Date & Field Validation: Highlights mismatched posting dates and missing required fields (e.g., Campaign, Pillar) to ensure downstream reporting accuracy.

KPI Scorecards: Provides a high-level summary of total records vs. total issues.

Dynamic Filtering: Allows users to filter issues by brand/client, platform, and specific error type.

🛠️ Tech Stack

Frontend/Framework: Python, Streamlit

Data Manipulation: Pandas, NumPy

Original Enterprise Architecture (Not included in repo): Snowflake (Snowpark API), automated deployment pipelines.

Technical Highlight: The original enterprise version of this tool implemented a custom Union-Find (Disjoint-Set) algorithm to cluster and map complex many-to-many duplicate records across different data sources.

🚀 How to Run Locally

Because this version uses generated mock data, you can run this dashboard on your local machine in under a minute without needing any database credentials.

Prerequisites
Make sure you have Python installed on your machine.

1. Clone the repository
Bash
git clone https://github.com/YourUsername/your-repo-name.git
cd your-repo-name
2. Install dependencies
It is recommended to use a virtual environment, but you can also install the requirements directly:

Bash
pip install -r requirements.txt
3. Run the app
Bash
streamlit run app.py
The dashboard will automatically open in your default web browser at http://localhost:8501.

Author: Alvin Chang https://www.linkedin.com/in/alvin-chang-125b77181

Status: Portfolio Project
