##################### INSTRUCTIONS: #####################
# This script updates the header version of all the chapters ODTs
#
# 1. Define the path to the manual repository
# 2. Run this from Windows Powershell in administrator mode
#########################################################

$folderPath = "D:\Bforartists\01_Preproduction\Documents\Manual"

$sevenZip   = "C:\Program Files\7-Zip\7z.exe"

function Update-HeaderXml {
    param([string]$filePath, [string]$newHeader)

    if (Test-Path $filePath) {
        [xml]$xmlDoc = Get-Content $filePath

        # Handle <style:header>, <style:header-left>, <style:header-right>
        foreach ($tag in @("style:header","style:header-left","style:header-right")) {
            $nodes = $xmlDoc.GetElementsByTagName($tag)
            foreach ($node in $nodes) {
                $paras = $node.GetElementsByTagName("text:p")
                if ($paras.Count -gt 0) {
                    foreach ($p in $paras) {
                        $p.InnerText = $newHeader
                    }
                } else {
                    # If no <text:p>, add one
                    $p = $xmlDoc.CreateElement("text:p", $xmlDoc.DocumentElement.NamespaceURI)
                    $p.SetAttribute("text:style-name","Header")
                    $p.InnerText = $newHeader
                    $node.AppendChild($p) | Out-Null
                }
            }
        }

        # Save back with UTF-8 without BOM
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        $sw = New-Object System.IO.StreamWriter($filePath, $false, $utf8NoBom)
        $xmlDoc.Save($sw)
        $sw.Close()
    }
}

Get-ChildItem -Path $folderPath -Filter *.odt | ForEach-Object {
    $file     = $_.FullName
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file)
    $chapter  = $baseName
    # CHANGE HERE: The manual reference in the header
    $headerStr = "Bforartists 5 Reference Manual - $chapter"

    $tempDir = Join-Path $env:TEMP ("odt_edit_" + [System.Guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $tempDir | Out-Null

    try {
        # Extract ODT
        & $sevenZip x $file -o"$tempDir" -y | Out-Null

        $stylesFile  = Join-Path $tempDir "styles.xml"
        $contentFile = Join-Path $tempDir "content.xml"

        # Update headers in both files
        Update-HeaderXml $stylesFile $headerStr

        # Backup original
        $backup = $file + ".bak"
        if (-not (Test-Path $backup)) { Copy-Item $file $backup -Force }

        # Repack with 7-Zip
        Push-Location $tempDir
        $tmpZip = Join-Path $tempDir "rebuilt.zip"
        if (Test-Path $tmpZip) { Remove-Item $tmpZip -Force }
        & $sevenZip a -tzip $tmpZip * | Out-Null
        Pop-Location

        Move-Item $tmpZip $file -Force
        Write-Host "Updated header in $file → '$headerStr'"
    }
    finally {
        if (Test-Path $tempDir) { Remove-Item $tempDir -Recurse -Force }
    }
}