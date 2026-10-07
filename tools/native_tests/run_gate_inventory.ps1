param(
 [Parameter(Mandatory=$true)][string[]]$StagePaths,
 [Parameter(Mandatory=$true)][string[]]$ProbeNames,
 [int]$TimeoutSeconds=60,
 [ValidateRange(0,1000000)][int]$ParameterOffset=0,
 [ValidateRange(1,64)][int]$ParameterLimit=16,
 [string[]]$GateIds=@(),
 [int[]]$BranchOffsets=@(),
 [string[]]$RpySourceRoots=@(),
 [switch]$SourceOnly,
 [switch]$LoadedSnapshotOnly,
 [string]$HostPython
)
$ErrorActionPreference='Stop'
if($StagePaths.Count -ne $ProbeNames.Count){throw 'One existing probe name is required for each isolated stage'}
if($TimeoutSeconds -lt 1 -or $TimeoutSeconds -gt 60){throw 'Timeout must be between 1 and 60 seconds'}
if($SourceOnly -and -not $RpySourceRoots.Count){throw 'Source-only crawl requires explicit RPY source roots'}
if($BranchOffsets.Count -and -not $GateIds.Count){throw 'Branch offsets require explicit gate ids'}
if($LoadedSnapshotOnly -and $SourceOnly){throw 'Select one report mode'}
$taskRpyRoots=@($RpySourceRoots|ForEach-Object {(Resolve-Path -LiteralPath $_).Path})
$taskRepo=Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$taskHostPython=$HostPython
if(-not $taskHostPython){
 $taskBundledPython=Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
 if(Test-Path -LiteralPath $taskBundledPython){$taskHostPython=$taskBundledPython}
 else{$taskHostPython=(Get-Command python.exe -ErrorAction Stop).Source}
}
if(-not (Test-Path -LiteralPath $taskHostPython)){throw 'Host Python is required for probe syntax preflight; pass -HostPython'}
& $taskHostPython -c 'import sys;sys.path.insert(0,sys.argv[1]);from replay_guard import validate_python_blocks;validate_python_blocks(sys.argv[2])' $PSScriptRoot (Join-Path $PSScriptRoot 'perfect_save_gate_inventory.rpy')
if($LASTEXITCODE -ne 0){throw 'Native gate probe syntax preflight failed'}
$taskIsolation=[IO.Path]::GetFullPath((Join-Path $taskRepo '.codex_tmp'))+[IO.Path]::DirectorySeparatorChar
for($taskIndex=0;$taskIndex -lt $StagePaths.Count;$taskIndex++){
 $taskStage=(Resolve-Path -LiteralPath $StagePaths[$taskIndex]).Path
 if(-not ($taskStage+[IO.Path]::DirectorySeparatorChar).StartsWith($taskIsolation,[StringComparison]::OrdinalIgnoreCase)){
  throw 'Native probes must run in an isolated copy under repository .codex_tmp'
 }
 $taskName=$ProbeNames[$taskIndex]
 if([IO.Path]::GetFileName($taskName) -ne $taskName -or -not $taskName.EndsWith('.rpy')){throw 'Probe name must be a filename ending in .rpy'}
 $taskProbe=Join-Path $taskStage "game/$taskName"
 if(-not (Test-Path -LiteralPath $taskProbe)){throw 'An existing isolated probe is required; do not create a second active fixture'}
 $taskRepoMods=@(Get-ChildItem -LiteralPath (Join-Path $taskRepo 'mods/perfect_save') -Filter '*.rpy')
 $taskInstalledMods=@(Get-ChildItem -LiteralPath (Join-Path $taskStage 'game/mods/perfect_save') -Filter '*.rpy')
 if(Compare-Object ($taskRepoMods.Name|Sort-Object) ($taskInstalledMods.Name|Sort-Object)){throw 'Isolated Mod source set differs from repository'}
 foreach($taskRepoMod in $taskRepoMods){
  $taskInstalled=Join-Path $taskStage ('game/mods/perfect_save/'+$taskRepoMod.Name)
  if((Get-FileHash -LiteralPath $taskRepoMod.FullName).Hash -ne (Get-FileHash -LiteralPath $taskInstalled).Hash){throw 'Isolated Mod source differs from repository'}
 }
 foreach($taskCompiled in Get-ChildItem -LiteralPath (Join-Path $taskStage 'game/mods/perfect_save') -Filter '*.rpyc'){
  if($taskCompiled.BaseName -notin $taskRepoMods.BaseName){throw 'Orphan compiled Mod script in isolated install'}
 }
 $taskBackup=Join-Path $taskStage ('gate_probe_backup_'+[Guid]::NewGuid().ToString('N')+'.rpy')
 Copy-Item -LiteralPath $taskProbe -Destination $taskBackup
 $taskProcess=$null
 try{
  foreach($taskSource in @('gate_catalogue.py','gate_runtime.py','screen_catalogue.py','native_branch_trace.py','native_script_continuation.py','native_state_snapshot.py','rpy_gate_catalogue.py')){
   Copy-Item -LiteralPath (Join-Path $PSScriptRoot $taskSource) -Destination (Join-Path $taskStage $taskSource)
  }
  Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'replay_guard.py') -Destination (Join-Path $taskStage 'ssct_replay_guard.py')
  Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'perfect_save_gate_inventory.rpy') -Destination $taskProbe
  $taskFingerprints=@{}
  foreach($taskSource in @('gate_catalogue.py','gate_runtime.py','screen_catalogue.py','native_branch_trace.py','native_script_continuation.py','native_state_snapshot.py','rpy_gate_catalogue.py','replay_guard.py','perfect_save_gate_inventory.rpy')){
   $taskFingerprints[$taskSource]=(Get-FileHash -LiteralPath (Join-Path $PSScriptRoot $taskSource) -Algorithm SHA256).Hash.ToLowerInvariant()
  }
  foreach($taskModSource in Get-ChildItem -LiteralPath (Join-Path $taskStage 'game/mods/perfect_save') -Filter '*.rpy'){
   $taskFingerprints['installed_mod/'+$taskModSource.Name]=(Get-FileHash -LiteralPath $taskModSource.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
  }
  [IO.File]::WriteAllText((Join-Path $taskStage 'gate_probe_options.json'),
   (@{parameter_offset=$ParameterOffset;parameter_limit=$ParameterLimit;gate_ids=$GateIds;branch_offsets=$BranchOffsets;rpy_source_roots=$taskRpyRoots;source_only=[bool]$SourceOnly;loaded_snapshot_only=[bool]$LoadedSnapshotOnly;source_fingerprints=$taskFingerprints}|ConvertTo-Json -Depth 5),[Text.UTF8Encoding]::new($false))
  $taskStarted=Get-Date
  $taskProcess=Start-Process -FilePath (Join-Path $taskStage 'lib/py3-windows-x86_64/python.exe') -ArgumentList @("`"$taskStage/summertimesaga.py`"","`"$taskStage`"") -WindowStyle Hidden -PassThru -RedirectStandardError (Join-Path $taskStage 'gate_stderr.txt')
  $taskTimer=[Diagnostics.Stopwatch]::StartNew()
  while(-not $taskProcess.WaitForExit(500)){
   foreach($taskEngineError in @('errors.txt','traceback.txt')){
    $taskErrorPath=Join-Path $taskStage $taskEngineError
    if((Test-Path -LiteralPath $taskErrorPath) -and (Get-Item -LiteralPath $taskErrorPath).LastWriteTime -ge $taskStarted -and (Get-Item -LiteralPath $taskErrorPath).Length -gt 0){
     throw (Get-Content -LiteralPath $taskErrorPath -Raw)
    }
   }
   if($taskTimer.Elapsed.TotalSeconds -ge $TimeoutSeconds){throw 'Native gate probe timeout; inspect parameter_gate_checkpoints.jsonl'}
  }
  if($taskProcess.ExitCode -ne 0){throw "Native gate probe exit $($taskProcess.ExitCode)"}
  $taskFailure=Join-Path $taskStage 'gate_probe_failure.txt'
  if((Test-Path -LiteralPath $taskFailure) -and (Get-Item -LiteralPath $taskFailure).LastWriteTime -ge $taskStarted){
   throw (Get-Content -LiteralPath $taskFailure -Raw)
  }
  $taskReportName=if($SourceOnly){'rpy_gate_inventory.json'}elseif($LoadedSnapshotOnly){'loaded_generated_state.json'}else{'perfect_gate_inventory.json'}
  $taskReport=Get-Item -LiteralPath (Join-Path $taskStage $taskReportName)
  if($taskReport.LastWriteTime -lt $taskStarted){throw 'Stale native gate report'}
  if((Get-Item -LiteralPath (Join-Path $taskStage 'gate_stderr.txt')).Length -gt 0){throw 'Native stderr is nonempty'}
  if(-not $SourceOnly -and -not $LoadedSnapshotOnly){Copy-Item -LiteralPath $taskReport.FullName -Destination (Join-Path $taskStage "parameter_gates_${ParameterOffset}_${ParameterLimit}.json")}
  Write-Output "$taskStage inventory exported"
 }finally{
  if($taskProcess -and -not $taskProcess.HasExited){
   $taskOwned=Get-CimInstance Win32_Process -Filter "ProcessId=$($taskProcess.Id)"
   if($taskOwned -and $taskOwned.CommandLine.Contains($taskStage)){Stop-Process -Id $taskProcess.Id}
  }
  Copy-Item -LiteralPath $taskBackup -Destination $taskProbe
 }
}
