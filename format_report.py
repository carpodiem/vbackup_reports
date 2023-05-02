import pandas as pd
from datetime import datetime

def create_report_dataframe(policy_static_data, backup_data, duration_data):
    report_data = []
  
    for policy, static_data in policy_static_data.items():
        # Append policy name and backup size
        backup_size_data = backup_data.loc[backup_data["Policy Name"] == policy, "Backup Size (GB)"]

        if not backup_size_data.empty:
            backup_size = backup_size_data.values[0]
        else:
            backup_size = 0  # или другое значение по умолчанию

        policy_data = [policy, "", "", "", backup_size, ""]
        report_data.append(policy_data)

        # Append VMs with duration
        policy_vms = duration_data[duration_data["Policy Name"] == policy]
        for index, row in policy_vms.iterrows():
            duration = str(pd.to_timedelta(row["Duration"]))
            duration = duration.replace("0 days ", "")
            formatted_duration = datetime.strptime(str(duration), "%H:%M:%S").strftime("%H:%M:%S")
            vm_data = [
                row["VM Name"],
                static_data["StartTime"],
                static_data["Incremental"],
                static_data["Full"],
                "",
                formatted_duration,
            ]
            report_data.append(vm_data)
    
    report_df = pd.DataFrame(
        report_data,
        columns=[
            "VM Display Name",
            "StartTime",
            "Инкрементальный",
            "Полный",
            "Текущий Backup Size GB",
            "Длительность инкрементального бэкапа",
        ],
    )

    return report_df