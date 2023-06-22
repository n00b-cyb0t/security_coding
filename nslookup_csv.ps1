# open txt file, change this path to the file you want
$input = get-content "C:\Users\$env:USERNAME\Desktop\servers.txt" 
$output = "C:\Users\$env:USERNAME\Desktop\results.csv"

$iplist = @()

# read column of IPs, !!! change "$ip" to "$ip.column_name" to the column name you want to target if this is a csv !!!
foreach ($ip in $input)
{
    $iplist += $ip
}


# Get only the unique values in the column
$uniq = $iplist | Sort-Object | Get-Unique


$results = @()

# output dns name 
foreach ($ip in $uniq)
{
    
    $x = Resolve-DnsName -name $ip 
    $results += $x
    #Write-Output $x
}

$results2 = @()

foreach ($x in $results)
{
    
    $r = Resolve-DnsName -name $x.NameHost
    $results2 += $r
    Write-Output $r
}



# output this to a file
$results2 | export-csv -Path $output 


$count1 = $uniq.Count
$count2 = $results.count
$c3 = $count1 - $count2

write-output ""
write-output "We found '$count2' resolved IPs"
Write-Output "There were '$count1' original IPs from the list, so '$c3'. Look at the above error logs to see which one[s] failed"
write-output ""
write-output "Output saved to $output"
