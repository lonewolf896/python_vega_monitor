###################################
##### Reset Video Card driver #####
##### No error checking
$d = Get-PnpDevice| where {$_.friendlyname -like 'Radeon RX Vega'}
$d  | Disable-PnpDevice -ErrorAction Ignore -Confirm:$false | Out-Null
# Wait 5 seconds
Start-Sleep -s 5
$d  | Enable-PnpDevice -ErrorAction Ignore -Confirm:$false | Out-Null
# Wait 5 seconds
Start-Sleep -s 10
