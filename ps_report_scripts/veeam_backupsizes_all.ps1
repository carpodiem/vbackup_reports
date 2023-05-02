$backups = Get-VBRBackup
#Create the VM report
$VMReport = @()
foreach ($backup in $backups) {
  $storages = $backup.GetAllStorages()
  foreach ($storage in $storages) {
    $JobOutput = $storage | select @{n='Name';e={$_.PartialPath}}, @{n='DataSize';e={$_.Stats.DataSize}}, `
    @{n='BackupSize';e={$_.Stats.BackupSize}}
    $VMReport += $JobOutput
  }
}

# Replace the output file path with the desired location
$dateString = Get-Date -Format "yyyy-MM-dd"
$outputFilePath = "C:\temp\veeam_backup_sizes_$($dateString).csv"
$VMReport | Export-Csv -Path $outputFilePath -NoTypeInformation