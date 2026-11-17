# ============================================================
#  3단계: Windows 에서 SSH 로 VM 에 접속해 Docker Engine 설치
#  실행: powershell -ExecutionPolicy Bypass -File .\03-install-docker.ps1
#  비밀번호를 물으면 config.ps1 의 $VmPassword 를 입력하세요 (2~3번 물어볼 수 있음)
# ============================================================
$ErrorActionPreference = "Stop"
. "$PSScriptRoot\config.ps1"

$sshPort = ($PortForwards | Where-Object { $_ -like "ssh,*" }).Split(",")[1]
$target  = "$VmUser@127.0.0.1"
$sshOpts = @("-p", $sshPort, "-o", "StrictHostKeyChecking=accept-new", "-o", "UserKnownHostsFile=$PSScriptRoot\known_hosts")

Write-Host "VM SSH 연결 확인 (localhost:$sshPort)..." -ForegroundColor Cyan
if (-not (Test-NetConnection 127.0.0.1 -Port $sshPort -InformationLevel Quiet -WarningAction SilentlyContinue)) {
  throw "localhost:$sshPort 에 연결할 수 없습니다. VM 설치가 끝났는지(로그인 화면) 확인하세요."
}

Write-Host "스크립트 복사..." -ForegroundColor Cyan
& scp -P $sshPort -o StrictHostKeyChecking=accept-new -o "UserKnownHostsFile=$PSScriptRoot\known_hosts" `
  "$PSScriptRoot\scripts\install-docker.sh" "$PSScriptRoot\scripts\test-docker.sh" "${target}:~/"
if ($LASTEXITCODE -ne 0) { throw "scp 실패" }

Write-Host "Docker 설치 (sudo 비밀번호를 물으면 같은 비밀번호 입력)..." -ForegroundColor Cyan
& ssh -t @sshOpts $target "sudo bash ~/install-docker.sh"
if ($LASTEXITCODE -ne 0) { throw "Docker 설치 실패" }

Write-Host "동작 확인 (새 세션 = docker 그룹 적용)..." -ForegroundColor Cyan
& ssh -t @sshOpts $target "bash ~/test-docker.sh"

Write-Host ""
Write-Host "완료! 이후 접속: ssh -p $sshPort $target" -ForegroundColor Green
Write-Host "브라우저에서 http://localhost:8080 확인"
