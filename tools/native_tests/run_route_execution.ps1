param(
    [Parameter(Mandatory=$true)][string]$Stage,
    [Parameter(Mandatory=$true)][string]$Probe,
    [ValidateRange(5,60)][int]$TimeoutSeconds=45
)
$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path (Join-Path $PSScriptRoot '../../.codex_tmp')).Path
$taskStage=(Resolve-Path -LiteralPath $Stage).Path
if(-not $taskStage.StartsWith($taskRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) {
    throw 'Replay may run only inside this repository isolated .codex_tmp directory'
}
if([IO.Path]::GetFileName($Probe) -ne $Probe -or -not $Probe.EndsWith('.rpy')) {throw 'Probe must be a filename'}
$taskExisting=Get-CimInstance Win32_Process | Where-Object {
    $_.Name -eq 'python.exe' -and $_.CommandLine -and $_.CommandLine.Contains($taskStage)
}
if($taskExisting) {throw 'An isolated native process already uses this stage; wait for it to exit'}
$taskConflicts=Get-ChildItem -LiteralPath (Join-Path $taskStage 'game') -Filter '*.rpy' | Where-Object {
    $_.Name -ne $Probe -and (Select-String -LiteralPath $_.FullName -Pattern 'def _ssct_replay_tick\(' -Quiet)
}
if($taskConflicts) {throw ('Duplicate native replay fixture: '+($taskConflicts.Name -join ', '))}
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'perfect_save_route_execution.rpy') -Destination (Join-Path $taskStage "game/$Probe")
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'replay_guard.py') -Destination (Join-Path $taskStage 'ssct_replay_guard.py')
& "$taskStage/lib/py3-windows-x86_64/python.exe" (Join-Path $PSScriptRoot 'replay_guard.py') (Join-Path $PSScriptRoot 'perfect_save_route_execution.rpy')
if($LASTEXITCODE -ne 0) {throw 'Replay Python syntax preflight failed; game was not launched'}
$taskStart=Get-Date
$taskProcess=Start-Process -FilePath "$taskStage/lib/py3-windows-x86_64/python.exe" -ArgumentList @("`"$taskStage/summertimesaga.py`"","`"$taskStage`"") -WindowStyle Hidden -PassThru -RedirectStandardOutput "$taskStage/replay_stdout.txt" -RedirectStandardError "$taskStage/replay_stderr.txt"
$taskTimedOut=$false
try {
    $taskTimedOut=-not $taskProcess.WaitForExit($TimeoutSeconds*1000)
} finally {
    if(-not $taskProcess.HasExited) {
        $taskOwned=Get-CimInstance Win32_Process -Filter "ProcessId=$($taskProcess.Id)"
        if($taskOwned -and $taskOwned.CommandLine.Contains($taskStage)) {
            Stop-Process -Id $taskProcess.Id
            $taskProcess.WaitForExit()
        } else {throw 'Process ownership verification failed'}
    }
}
$taskPath=Join-Path $taskStage 'native_route_execution.json'
if(-not (Test-Path -LiteralPath $taskPath) -or (Get-Item -LiteralPath $taskPath).LastWriteTime -lt $taskStart) {throw 'No fresh native replay report'}
$taskResult=Get-Content -LiteralPath $taskPath -Raw | ConvertFrom-Json
if($taskTimedOut) {
    $taskResult.status='blocked'
    $taskResult.stop=@{reason='external_wall_clock_deadline';seconds=$TimeoutSeconds;last_observation=$taskResult.stop}
    [IO.File]::WriteAllText($taskPath,($taskResult | ConvertTo-Json -Depth 100)+"`n",[Text.UTF8Encoding]::new($false))
}
$taskResult | Select-Object version,status,stop | ConvertTo-Json -Depth 10
if($taskResult.status -ne 'complete') {exit 1}
