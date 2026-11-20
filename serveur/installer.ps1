#Requires -RunAsAdministrator
<#
  Installe l'impression automatique T7200 sur le serveur.
  A lancer UNE fois, en administrateur, depuis le dossier qui contient
  installer.ps1, surveiller.ps1, papiers.csv et SumatraPDF.exe :

    powershell -ExecutionPolicy Bypass -File .\installer.ps1

  Si l'imprimante ne s'appelle pas PRT29 sur ce serveur :
    powershell -ExecutionPolicy Bypass -File .\installer.ps1 -ImprimanteSource "Nom exact"
#>
param(
  [string]$ImprimanteSource = "PRT29",
  [string]$Racine = "C:\ImpressionT7200",
  [string]$NomPartage = "ImpressionT7200"
)
$ErrorActionPreference = "Stop"
$ici = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Verifications
$src = Get-Printer -Name $ImprimanteSource -ErrorAction SilentlyContinue
if (-not $src) {
  Write-Host "Imprimante '$ImprimanteSource' introuvable sur ce serveur. Imprimantes presentes :" -ForegroundColor Red
  Get-Printer | Select-Object Name, DriverName, PortName | Format-Table -AutoSize
  exit 1
}
if (-not (Test-Path (Join-Path $ici "SumatraPDF.exe"))) {
  Write-Host "SumatraPDF.exe manquant. Telecharge la version portable 64 bits sur sumatrapdfreader.org et place-la a cote de ce script." -ForegroundColor Red
  exit 1
}

# 2. Copie des fichiers
New-Item -ItemType Directory -Force -Path $Racine | Out-Null
foreach ($f in "surveiller.ps1", "papiers.csv", "SumatraPDF.exe") {
  Copy-Item -Force (Join-Path $ici $f) $Racine
}
$papiers = Import-Csv (Join-Path $Racine "papiers.csv") -Delimiter ";" -Encoding UTF8

# 3. Une file d'impression par papier, vers la meme T7200
foreach ($p in $papiers) {
  if (Get-Printer -Name $p.Imprimante -ErrorAction SilentlyContinue) {
    Write-Host "File deja presente : $($p.Imprimante)"
  } else {
    Add-Printer -Name $p.Imprimante -DriverName $src.DriverName -PortName $src.PortName
    Write-Host "File creee : $($p.Imprimante)" -ForegroundColor Green
  }
}

# 4. Dossiers de depot partages
$depot = Join-Path $Racine "Depot"
foreach ($p in $papiers) {
  New-Item -ItemType Directory -Force -Path (Join-Path $depot $p.Dossier) | Out-Null
  New-Item -ItemType Directory -Force -Path (Join-Path $Racine "Imprimes\$($p.Dossier)") | Out-Null
}
New-Item -ItemType Directory -Force -Path (Join-Path $Racine "Erreurs") | Out-Null
# Utilisateurs authentifies : modification dans Depot (SID, fonctionne en francais comme en anglais)
icacls $depot /grant "*S-1-5-11:(OI)(CI)M" | Out-Null
if (-not (Get-SmbShare -Name $NomPartage -ErrorAction SilentlyContinue)) {
  $tous = (New-Object System.Security.Principal.SecurityIdentifier("S-1-5-11")).Translate([System.Security.Principal.NTAccount]).Value
  New-SmbShare -Name $NomPartage -Path $depot -ChangeAccess $tous | Out-Null
}
Write-Host "Partage : \\$env:COMPUTERNAME\$NomPartage" -ForegroundColor Green

# 5. Tache planifiee qui surveille les dossiers (demarre avec le serveur)
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
  -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$Racine\surveiller.ps1`""
$declencheur = New-ScheduledTaskTrigger -AtStartup
$compte = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$options = New-ScheduledTaskSettingsSet -ExecutionTimeLimit ([TimeSpan]::Zero) `
  -RestartCount 99 -RestartInterval (New-TimeSpan -Minutes 1) -StartWhenAvailable
Register-ScheduledTask -TaskName "Impression T7200" -Action $action -Trigger $declencheur `
  -Principal $compte -Settings $options -Force | Out-Null
Start-ScheduledTask -TaskName "Impression T7200"

Write-Host ""
Write-Host "Installation terminee." -ForegroundColor Green
Write-Host "IMPORTANT : regle maintenant les 'Valeurs par defaut' de chaque file T7200 (voir LISEZMOI.txt, etape 3)."
