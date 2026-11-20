$pptxPath = (Resolve-Path "presentation\TapasShield_NSA6_Pitch_Deck.pptx").Path
$outDir = Join-Path (Resolve-Path "presentation").Path "slides_pptx_images"
if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
}

$ppt = New-Object -ComObject PowerPoint.Application
try {
    $pres = $ppt.Presentations.Open($pptxPath, 1, 0, 0)
    # SaveAs with 18 exports all slides as PNG images in the directory
    $pres.SaveAs($outDir, 18)
    $pres.Close()
    Write-Host "Successfully exported PPTX slides to $outDir"
} catch {
    Write-Error $_
} finally {
    $ppt.Quit()
    [System.GC]::Collect()
}
Get-ChildItem -Path $outDir

