import re 
import pandas as pd


def read_tsv_file(file_path):
    return pd.read_csv(file_path, sep='\s+', engine='python')


def read_csv_file(file_path, skip_rows=0, skip_footer=0):
    # Read the filtered lines into a DataFrame
    data = pd.read_csv(file_path, skiprows=skip_rows, skipfooter=skip_footer, engine='python', thousands=',')

    # Remove all the spaces befora and after column name
    data.columns = data.columns.str.strip()

    return data


def process_veeam_backup_size_report(veeam_data):
    # Calculate backup size in GB
    veeam_data['Backup Size (GB)'] = pd.to_numeric(veeam_data['BackupSize'])
    veeam_data['Backup Size (GB)'] = (veeam_data['Backup Size (GB)'] / 1024 ** 3 ) 

    # Extract Policy name from a column Name
    pattern = r'(.+?)D\d{4}'
    veeam_data['Policy Name'] = \
        veeam_data['Name'].apply(lambda x: re.search(pattern, x).group(1))

    # Group and sum data from field BackupSize
    result = veeam_data.groupby('Policy Name').agg({'Backup Size (GB)': 'sum'}).reset_index()
    result['Backup Size (GB)'] = result['Backup Size (GB)'].round()

#    print(data.columns)
#
#    veeam_data = data.iloc[1:]
#    veeam_data['BackupSize'] = pd.to_numeric(veeam_data['BackupSize']) 
#    veeam_data['BackupSize'] = veeam_data['BackupSize'] / (1024 * 1024 * 1024)
#
#    # Extract Policy name from a column Name
#    #pattern = r'(?:(?:Backup Job )?)(.+?-\d{1,3})D'
#    pattern = r'(.+?)D\d{4}'
#    veeam_data['PolicyName'] = \
#        veeam_data['Name'].apply(lambda x: re.search(pattern, x).group(1))
#
#    # Group and sum data from field BackupSize
#    result = veeam_data.groupby('PolicyName').agg({'BackupSize': 'sum'}).reset_index()
#    result['BackupSize'] = result['BackupSize'].round()
#     
    return result


def process_veeam_incr_report(data):
    # Filter out failed tasks
    data = data[data['Status'] != 'Failed']

    # Convert Duration to timedelta
    data.loc[:, 'Duration'] = pd.to_timedelta(data['Duration'])

    # Group and calculate the average duration per VM within each backup policy
    result = data.groupby(['JobName', 'Name']).agg({'Duration': 'mean'}).reset_index()
    result = result.rename(columns={'JobName': 'Policy Name', 'Name': 'VM Name'})

    # Convert the average duration back to a readable string format
    result['Duration'] = result['Duration'].apply(lambda x: str(x).split('.')[0])

    return result


def process_nb_incr_report(data):
    # Convert Duration to timedelta
    data['Duration'] = pd.to_timedelta(data['Job Duration']) 

    # Group and calculate the average duration per VM within each backup policy
    result = data.groupby(['Policy Name', 'Client Name']).agg({'Duration': 'mean'}).reset_index()
    result = result.rename(columns={'Client Name': 'VM Name'})

    # Convert the average duration back to a readable string format
    result['Duration'] = result['Duration'].apply(lambda x: str(x).split('.')[0])

    return result


def process_nb_dedup_rate_report(data):
    # Calculate the mean of the 'Deduplication Rate' column
    mean_dedup_rate = data['Deduplication Rate'].mean()

    return mean_dedup_rate


def process_nb_backup_sizes(policy_sizes, mean_dedup_rate):

    policy_sizes['Total Unexpired Backup Size (GB)'] = pd.to_numeric(policy_sizes['Total Unexpired Backup Size (GB)'])
    # Calculate the volume per policy

    if mean_dedup_rate > 95:
        mean_dedup_rate = 95

    policy_sizes['Backup Size (GB)'] = policy_sizes['Total Unexpired Backup Size (GB)'] * ((100 - mean_dedup_rate) / 100)
    policy_sizes['Backup Size (GB)'] = policy_sizes['Backup Size (GB)'].round()

    # Return the final dataframe with the added column
    return policy_sizes[['Policy Name', 'Backup Size (GB)']]
