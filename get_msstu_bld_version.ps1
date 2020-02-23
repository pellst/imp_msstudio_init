#[assembly: AssemblyFileVersionAttribute("2.3.0.3407")]
$pattern = '"'
#$content = Get-Content C:\Users\Administrator\Documents\GitHub\MassSpecStudio\source\MassSpecStudio\MassSpecStudio\Properties\GlobalAssemblyInfo.cs | Out-String
$content = sls AssemblyFileVersionAttribute C:\Users\Administrator\Documents\GitHub\MassSpecStudio\source\MassSpecStudio\MassSpecStudio\Properties\GlobalAssemblyInfo.cs -ca| select -exp Line
$bldversion = $content.Split($pattern,[System.StringSplitOptions]::RemoveEmptyEntries) | Where-Object {$_ -match '[0-9].[0-9].*'} 
$srcfilename = "C:\Users\Administrator\Documents\GitHub\MassSpecStudio\Output\Installer-Full"
$destfilename = "C:\Users\Administrator\Documents\GitHub\MassSpecStudio\MassSpecStudio-$bldversion-x64-Full.zip"
#Compress-Archive -Path C:\Users\Administrator\Documents\GitHub\MassSpecStudio\Output\Installer-Full -DestinationPath C:\Users\Administrator\Documents\GitHub\MassSpecStudio\MassSpecStudio-$bldversion-x64-Full -force
Compress-Archive -Path $srcfilename -DestinationPath $destfilename -force
