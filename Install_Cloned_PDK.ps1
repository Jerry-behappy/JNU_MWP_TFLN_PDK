param([string]$KLayoutDataPath)
$ErrorActionPreference = 'Stop'
# 安装路径从克隆位置及用户配置目录推导，不覆盖已有安装。
if ([string]::IsNullOrWhiteSpace($KLayoutDataPath)) {
    if ($env:KLAYOUT_HOME) { $KLayoutDataPath = $env:KLAYOUT_HOME }
    else { $KLayoutDataPath = Join-Path ([Environment]::GetFolderPath('UserProfile')) 'KLayout' }
}
$TflnPackage = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot 'salt/JNU_MWP_TFLN_PDK')).Path
if (-not (Test-Path -LiteralPath $KLayoutDataPath)) { New-Item -ItemType Directory -Path $KLayoutDataPath | Out-Null }
$TflnData = (Resolve-Path -LiteralPath $KLayoutDataPath).Path
$TflnSalt = Join-Path $TflnData 'salt'
if (-not (Test-Path -LiteralPath $TflnSalt)) { New-Item -ItemType Directory -Path $TflnSalt | Out-Null }
$TflnDestination = Join-Path $TflnSalt 'JNU_MWP_TFLN_PDK'
if (Test-Path -LiteralPath $TflnDestination) {
    $TflnExisting = Get-Item -LiteralPath $TflnDestination -Force
    if ($TflnExisting.LinkType -eq 'Junction' -and @($TflnExisting.Target)[0] -eq $TflnPackage) {
        Write-Output "Already installed: $TflnDestination"
        exit 0
    }
    throw "Existing installation retained: $TflnDestination"
}
New-Item -ItemType Junction -Path $TflnDestination -Target $TflnPackage | Out-Null
Write-Output "Installed: $TflnDestination"
Write-Output 'Restart KLayout; select JNU_MWP_TFLN_PDK. Public libraries contain blackboxes.'
