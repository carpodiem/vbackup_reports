# Technical Specification: Utility for Automating the Creation of Virtual Machine Backup Reports

## Project Objective
The aim of the project is to develop a Python utility for processing backup reports of virtual machines obtained from Netbackup and Veeam systems, with the goal of creating a unified report in Excel (XLS) format.

## Input Data
1. Netbackup system reports in TSV format, containing information about backup volumes by tasks.
2. Veeam system reports in TSV format, containing information about backup volumes by tasks.
3. Reports from Netbackup and Veeam systems in TSV and CSV formats, containing information about the average incremental backup time of each virtual machine per month.

## Functional Requirements
1. Processing and normalization of input data:
    * Removal of unnecessary information and headers from the reports.
    * Conversion of report formats, if necessary.
2. Calculation of required data:
    * Summation of backup volumes by tasks.
    * Calculation of the average incremental backup time of each virtual machine per month.
3. Creation of the final report in Excel (XLS) format:
    * Formulation of the structure of the report (column names, data placement, etc.).
    * Addition of the calculated data to the report.
    * Saving the report in XLS format.

## Output Data
1. The final report on the backup of virtual machines in Excel (X
