from os import path
import json
import pandas as pd
from process_reports import (
    process_veeam_backup_size_report,
    process_veeam_incr_report,
    process_nb_incr_report,
    process_nb_dedup_rate_report,
    process_nb_backup_sizes,
    read_csv_file
)
from format_report import create_report_dataframe
from datetime import datetime
from format_xlsx import format_excel_file
from pprint import pprint

def load_policy_static_data(policy_data_file):
    policy_data = pd.read_excel(policy_data_file)

    # Remove spaces before and after string in field 'Policy Name'
    policy_data.columns = [col.strip() for col in policy_data.columns]
    policy_data['Policy Name'] = policy_data['Policy Name'].apply(lambda x: x.strip())

    policy_data = pd.read_excel(policy_data_file, index_col="Policy Name")
    return policy_data.to_dict(orient="index")


def process_reports_and_save_to_excel(reports_directory, policy_data_file, output_file):
    # Load reports
    vim_sizes_report = read_csv_file(path.join(reports_directory, REPORT_FILES['veeam_sizes_report']+ ".csv")) 
    vim_inc_report = read_csv_file(path.join(reports_directory, REPORT_FILES['veeam_incr_report'] + ".csv"))
    nb_dedup_rate_report = read_csv_file(path.join(reports_directory, REPORT_FILES['nb_dedup_rate_report'] + ".csv"), skip_rows=3, skip_footer=1)
    nb_sizes_report = read_csv_file(path.join(reports_directory, REPORT_FILES['nb_sizes_report'] + ".csv"), skip_rows=3, skip_footer=1)
    nb_inc_report = read_csv_file(path.join(reports_directory,REPORT_FILES['nb_incr_report'] + ".csv"), skip_rows=3, skip_footer=1)

    # Load static policy data
    policy_static_data = load_policy_static_data(policy_data_file)

    # Process loaded reports
    veeam_duration_data = process_veeam_incr_report(vim_inc_report)
    veeam_backup_sizes = process_veeam_backup_size_report(vim_sizes_report) 
    nb_mean_dedup_rate = process_nb_dedup_rate_report(nb_dedup_rate_report)
    nb_duration_data = process_nb_incr_report(nb_inc_report)
    nb_backup_sizes = process_nb_backup_sizes(nb_sizes_report,nb_mean_dedup_rate)

    backup_sizes = pd.concat([nb_backup_sizes, veeam_backup_sizes], ignore_index=True)
    duration_data = pd.concat([nb_duration_data, veeam_duration_data], ignore_index=True)

    # Check if there is new policies addet to the backup systems
    check_new_policies(policy_static_data, backup_sizes)

    # Dataframe creation for the target report
    report_df = create_report_dataframe(policy_static_data, backup_sizes, duration_data)

    # Save dataframe to the target report excel-file
    report_df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"Rerport saved to {output_file}")


def check_new_policies(policy_static_data, backup_sizes):
    static_policy_names = set(policy_static_data.keys())
    backup_policy_names = set(backup_sizes["Policy Name"])
    print("Backup policies in the report:")
    pprint(backup_policy_names)
    print("\n")
    print("Backup policies in the static file:")
    pprint(static_policy_names)

    new_policies = backup_policy_names - static_policy_names

    if new_policies:
        print("Warning! The following new policies were found in the reports but not in the static file:")
        for policy in new_policies:
            print(f"- {policy}")
        print("Please update the static file with the new policy information.")


if __name__ == "__main__":

    with open('config.json', 'r') as f:
        config = json.load(f)

    REPORT_FILES = config['REPORT_FILES']
    REPORT_DIR = "reports"

    policy_data_file = "policy_data.xlsx"  
    target_report_file = "Backup_report.xlsx"
    process_reports_and_save_to_excel(REPORT_DIR, policy_data_file, target_report_file)
    print("Excel report created successfully.")
    
    # Get the current date as a string
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Use the current date in the file name
    formatted_report_file = f"Backup_report_{current_date}.xlsx"
    format_excel_file(target_report_file, formatted_report_file)
