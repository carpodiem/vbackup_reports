import pandas as pd

def save_to_excel(backup_sizes, backup_durations, output_file):
    # Create a new Excel writer
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    # Create a new DataFrame to store formatted data
    formatted_data = []

    # Iterate over backup sizes
    for index, row in backup_sizes.iterrows():
        policy_name = row['Policy Name']
        size = row['Backup Size']

        # Add a row for policy name and backup size
        formatted_data.append({'Policy Name': policy_name, 'Size': size, 'VM Name': '', 'Average Duration': ''})

        # Filter backup durations for the current policy
        policy_durations = backup_durations[backup_durations['Policy Name'] == policy_name]

        # Add rows for VM names and average durations
        for _, duration_row in policy_durations.iterrows():
            formatted_data.append({'Policy Name': '', 'Size': '', 'VM Name': duration_row['VM Name'], 'Average Duration': duration_row['Duration']})

    # Create a DataFrame from the formatted data
    formatted_df = pd.DataFrame(formatted_data)

    # Add a row for total size
    total_size = backup_sizes['Backup Size'].sum()
    formatted_df = formatted_df.append({'Policy Name': 'Total', 'Size': total_size, 'VM Name': '', 'Average Duration': ''}, ignore_index=True)

    # Write the formatted DataFrame to Excel
    formatted_df.to_excel(writer, index=False, sheet_name='Report')

    # Save the Excel file
    writer.save()

