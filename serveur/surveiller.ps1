<#
  Surveille les dossiers de depot et imprime chaque PDF sur la file
  du papier correspondant. Lance automatiquement par la tache
  planifiee "Impression T7200". Ne pas lancer a la main.
#>
$Racine  = Split-Path -Parent $MyInvocation.MyCommand.Path
$Sumatra = Join-Path $Racine "SumatraPDF.exe"
$Journal = Join-Path $Racine "journal.txt"
$Papiers = Import-Csv (Join-Path $Racine "papiers.csv") -Delimiter ";" -Encoding UTF8
# fit = met le PDF a la taille du papier ; noscale = taille reelle
$Echelle = "fit"

function Log($msg) {
  "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $msg" | Add-Content -Path $Journal -Encoding UTF8
}
function Deplacer($fichier, $versDossier) {
  New-Item -ItemType Directory -Force -Path $versDossier | Out-Null
  $nom = "$(Get-Date -Format 'yyyyMMdd-HHmmss')_$($fichier.Name)"
  Move-Item -LiteralPath $fichier.FullName -Destination (Join-Path $versDossier $nom) -Force
}

Log "Demarrage de la surveillance"
while ($true) {
  foreach ($p in $Papiers) {
    $dossier = Join-Path $Racine "Depot\$($p.Dossier)"
    $pdfs = Get-ChildItem -LiteralPath $dossier -Filter *.pdf -File -ErrorAction SilentlyContinue
    foreach ($f in $pdfs) {
      # On attend que la copie du fichier soit terminee
      if (((Get-Date) - $f.LastWriteTime).TotalSeconds -lt 5) { continue }
      try { $flux = [IO.File]::Open($f.FullName, 'Open', 'Read', 'None'); $flux.Close() } catch { continue }

      $arguments = @("-print-to", "`"$($p.Imprimante)`"", "-print-settings", $Echelle, "-silent", "`"$($f.FullName)`"")
      $proc = Start-Process -FilePath $Sumatra -ArgumentList $arguments -PassThru -WindowStyle Hidden
      $fini = $proc.WaitForExit(600000)
      if ($fini -and $proc.ExitCode -eq 0) {
        Deplacer $f (Join-Path $Racine "Imprimes\$($p.Dossier)")
        Log "OK      $($p.Imprimante)  <-  $($f.Name)"
      } else {
        if (-not $fini) { $proc.Kill() }
        Deplacer $f (Join-Path $Racine "Erreurs")
        Log "ERREUR  $($p.Imprimante)  <-  $($f.Name)  (code $($proc.ExitCode))"
      }
    }
  }
  Start-Sleep -Seconds 5
}
