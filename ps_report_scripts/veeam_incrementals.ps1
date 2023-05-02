asnp VeeamPSSnapin
# Get a list of the scheduled jobs
$Jobs = Get-VBRBackupSession -Name "*Incremental*" | ?{$_.JobType -eq "Backup"} |?{$_.CreationTime -ge (Get-Date).AddDays(-27)}

# Create the VM report
$VMReport = @()
ForEach ($Job in $Jobs) {
   $VMReport += Get-VBRTaskSession $Job | 
   Select-Object Name ,JobName ,Status,
   @{Name="StartTime"; Expression = {$_.Progress.StartTimeLocal}},
   @{Name="TransferedGB"; Expression = {[math]::Round(($_.Progress.TransferedSize/1GB),2)}},
   @{Name="Duration"; Expression = {'{0:00}:{1:00}:{2:00}' -f $_.Progress.Duration.Hours, $_.Progress.Duration.Minutes, $_.Progress.Duration.Seconds}}
}

# Replace the output file path with the desired location
$dateString = Get-Date -Format "yyyy-MM-dd"
$outputFilePath = "C:\temp\veeam_$($dateString).csv"
$VMReport | Export-Csv -Path $outputFilePath -NoTypeInformation
