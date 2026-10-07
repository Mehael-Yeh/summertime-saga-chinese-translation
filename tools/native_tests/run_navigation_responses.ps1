param(
 [Parameter(Mandatory=$true)][string]$StagePath,
 [Parameter(Mandatory=$true)][string]$ProbeName,
 [int]$Tick=4,
 [ValidateRange(1,100000)][int]$Limit=1000,
 [switch]$Resume,
 [switch]$IncludeInteractions,
 [string]$RecoveryNote,
 [string]$SeedCasePath
)
$ErrorActionPreference='Stop'
$taskRepo=Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$taskIsolation=[IO.Path]::GetFullPath((Join-Path $taskRepo '.codex_tmp'))+[IO.Path]::DirectorySeparatorChar
$taskStage=(Resolve-Path -LiteralPath $StagePath).Path
if(-not ($taskStage+[IO.Path]::DirectorySeparatorChar).StartsWith($taskIsolation,[StringComparison]::OrdinalIgnoreCase)){
 throw 'Run only in an isolated official-game copy under repository .codex_tmp'
}
if([IO.Path]::GetFileName($ProbeName) -ne $ProbeName -or -not $ProbeName.EndsWith('.rpy')){throw 'ProbeName must be a .rpy filename'}
$taskProbe=Join-Path $taskStage "game/$ProbeName"
if(-not (Test-Path -LiteralPath $taskProbe)){throw 'An existing isolated probe is required'}
if($RecoveryNote -and -not $Resume){throw 'Diagnosed recovery requires Resume'}
$taskReportPath=Join-Path $taskStage 'perfect_navigation_responses.json'
if(-not $Resume -and (Test-Path -LiteralPath $taskReportPath)){
 $taskPrior=Get-Content -LiteralPath $taskReportPath -Raw | ConvertFrom-Json
 Copy-Item -LiteralPath $taskReportPath -Destination (Join-Path $taskStage ('navigation_previous_'+[Guid]::NewGuid().ToString('N')+'.json'))
}
if($Resume){
 if(-not (Test-Path -LiteralPath $taskReportPath)){throw 'No navigation frontier to resume'}
 $taskPrevious=Get-Content -LiteralPath $taskReportPath -Raw | ConvertFrom-Json
 if($taskPrevious.status -eq 'failed' -and -not $RecoveryNote){throw 'Diagnose the failure and provide RecoveryNote; do not silently skip it'}
 if($RecoveryNote){
  Copy-Item -LiteralPath $taskReportPath -Destination (Join-Path $taskStage ('navigation_failure_'+[Guid]::NewGuid().ToString('N')+'.json'))
 }
}
$taskBackup=Join-Path $taskStage ('navigation_probe_backup_'+[Guid]::NewGuid().ToString('N')+'.rpy')
Copy-Item -LiteralPath $taskProbe -Destination $taskBackup
$taskProcess=$null
try{
 $taskSeedCase=$null
 if($SeedCasePath){
  if($Resume -or -not $IncludeInteractions){throw 'A targeted seed case needs a fresh interaction scan'}
  $taskSeedPath=(Resolve-Path -LiteralPath $SeedCasePath).Path
  if(-not $taskSeedPath.StartsWith($taskIsolation,[StringComparison]::OrdinalIgnoreCase)){throw 'Seed case must be isolated test data'}
  $taskSeedCase=Get-Content -LiteralPath $taskSeedPath -Raw | ConvertFrom-Json
 }
 Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'perfect_save_navigation_responses.rpy') -Destination $taskProbe
 Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'replay_guard.py') -Destination (Join-Path $taskStage 'ssct_replay_guard.py')
 Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'native_branch_trace.py') -Destination (Join-Path $taskStage 'native_branch_trace.py')
 Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'native_wallet_protocol.py') -Destination (Join-Path $taskStage 'native_wallet_protocol.py')
 $taskDependencies=@{}
 foreach($taskDependency in @('ssct_replay_guard.py','native_branch_trace.py','native_wallet_protocol.py')){
  $taskDependencies[$taskDependency]=(Get-FileHash -LiteralPath (Join-Path $taskStage $taskDependency) -Algorithm SHA256).Hash.ToLowerInvariant()
 }
 [IO.File]::WriteAllText((Join-Path $taskStage 'navigation_probe_options.json'),
  (@{tick=$Tick;limit=$Limit;resume=[bool]$Resume;include_interactions=[bool]$IncludeInteractions;probe_sha256=(Get-FileHash -LiteralPath $taskProbe -Algorithm SHA256).Hash.ToLowerInvariant();probe_dependencies=$taskDependencies;retry_failed=[bool]$RecoveryNote;recovery_note=$RecoveryNote;seed_case=$taskSeedCase}|ConvertTo-Json -Depth 20),[Text.UTF8Encoding]::new($false))
 $taskStarted=Get-Date
 $taskProcess=Start-Process -FilePath (Join-Path $taskStage 'lib/py3-windows-x86_64/python.exe') -ArgumentList @("`"$taskStage/summertimesaga.py`"","`"$taskStage`"") -WindowStyle Hidden -PassThru -RedirectStandardError (Join-Path $taskStage 'navigation_stderr.txt')
 if(-not $taskProcess.WaitForExit(60000)){throw 'Native navigation process timeout; preserve the interrupted frontier'}
 if($taskProcess.ExitCode -ne 0){throw "Native navigation exit $($taskProcess.ExitCode)"}
 $taskReport=Get-Item -LiteralPath $taskReportPath
 if($taskReport.LastWriteTime -lt $taskStarted){throw 'Stale navigation response report'}
 if((Get-Item -LiteralPath (Join-Path $taskStage 'navigation_stderr.txt')).Length -gt 0){throw 'Native stderr is nonempty'}
 $taskResult=Get-Content -LiteralPath $taskReportPath -Raw | ConvertFrom-Json
 if($taskResult.status -notin @('navigation_scan_complete','segment_complete')){throw $taskResult.error}
 $taskScope=if($IncludeInteractions){'interactions'}else{'navigation'}
 if($SeedCasePath){$taskScope='targeted_interaction'}
 Copy-Item -LiteralPath $taskReportPath -Destination (Join-Path $taskStage "${taskScope}_tick_$Tick.json")
 Write-Output "$($taskResult.version): $($taskResult.status); $($taskResult.rows.Count) native responses, $($taskResult.seen.Count) contexts, $($taskResult.pending.Count) pending"
}finally{
 if($taskProcess -and -not $taskProcess.HasExited){
  $taskOwned=Get-CimInstance Win32_Process -Filter "ProcessId=$($taskProcess.Id)"
  if($taskOwned -and $taskOwned.CommandLine.Contains($taskStage)){Stop-Process -Id $taskProcess.Id}
 }
 Copy-Item -LiteralPath $taskBackup -Destination $taskProbe
}
