# ============================================================
#  1단계: 호스트(Windows) 점검 - 읽기 전용, 시스템을 바꾸지 않습니다
#  실행: powershell -ExecutionPolicy Bypass -File .\01-check-host.ps1
# ============================================================
. "$PSScriptRoot\config.ps1"
$ok = $true

function Pass($m) { Write-Host "[OK]   $m" -ForegroundColor Green }
function Fail($m) { Write-Host "[FAIL] $m" -ForegroundColor Red; $script:ok = $false }
function Warn($m) { Write-Host "[WARN] $m" -ForegroundColor Yellow }

Write-Host "`n=== Docker 실습 VM 호스트 점검 ===`n"

# 1) Windows 하이퍼바이저가 꺼져 있어야 VirtualBox 가 정상 속도(AMD-V)로 동작
#    이 PC 는 하이퍼바이저를 켜면 부팅이 멈추므로 반드시 꺼져 있어야 합니다.
$cs = Get-CimInstance Win32_ComputerSystem
if ($cs.HypervisorPresent) {
  Fail "Windows 하이퍼바이저가 켜져 있습니다. 관리자 PowerShell 에서 'bcdedit /set hypervisorlaunchtype off' 실행 후 재부팅하세요."
} else { Pass "Windows 하이퍼바이저 꺼짐 (VirtualBox 가 AMD-V 를 직접 사용)" }

# 2) BIOS 가상화(SVM)
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
if ($cpu.VirtualizationFirmwareEnabled) { Pass "BIOS 가상화(SVM) 켜짐 - $($cpu.Name.Trim())" }
else { Warn "BIOS 가상화 상태를 확인할 수 없거나 꺼져 있습니다. BIOS 에서 SVM Mode 를 Enabled 로 하세요." }

# 3) 자원
$ramGB = [math]::Round($cs.TotalPhysicalMemory / 1GB, 1)
Pass "RAM ${ramGB}GB / 논리 CPU $($cpu.NumberOfLogicalProcessors)개  -> VM 에 ${VmCpus}CPU / $([math]::Round($VmMemoryMB/1024,1))GB 할당 예정"
$drive = (Split-Path $VmBaseDir -Qualifier)
$free = [math]::Round((Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='$drive'").FreeSpace / 1GB, 1)
if ($free -gt ($VmDiskMB / 1024 + 10)) { Pass "$drive 여유 공간 ${free}GB" } else { Fail "$drive 여유 공간 부족 (${free}GB)" }

# 4) VirtualBox
if (Test-Path $VBoxManage) {
  Pass "VirtualBox 설치됨 - $(& $VBoxManage --version)"
} else {
  Fail "VirtualBox 가 설치되어 있지 않습니다. https://www.virtualbox.org/wiki/Downloads 에서 'Windows hosts' 설치 파일을 받아 설치하세요."
}

# 5) Ubuntu ISO
$iso = Get-ChildItem $IsoDir -Filter "ubuntu-*-live-server-amd64.iso" -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First 1
if ($iso) { Pass "Ubuntu ISO: $($iso.Name)" }
else { Fail "Ubuntu Server ISO 가 없습니다. https://ubuntu.com/download/server 에서 24.04 LTS ISO 를 받아 $IsoDir 에 넣으세요." }

# 6) OpenSSH 클라이언트 (VM 접속/Docker 설치에 사용)
if (Get-Command ssh -ErrorAction SilentlyContinue) { Pass "OpenSSH 클라이언트 있음" } else { Fail "OpenSSH 클라이언트가 없습니다 (설정 > 시스템 > 선택적 기능 > OpenSSH 클라이언트)" }

# 7) 충돌 요소
if (Test-Path "C:\Program Files\Docker\Docker\Docker Desktop.exe") {
  Warn "Docker Desktop 이 설치되어 있습니다. WSL2/Hyper-V 를 다시 켜려 할 수 있으니 제거를 권장합니다."
}
$ahn = Get-CimInstance Win32_SystemDriver | Where-Object { $_.Name -match 'ATamptNt|asc_kbc|MeDCoreD|MeDVpDrv' }
if ($ahn) { Warn "AhnLab Safe Transaction 드라이버가 실행 중입니다. VM 실행이 불안정하면 제거하세요." }

Write-Host ""
if ($ok) { Write-Host "모든 필수 항목 통과 -> 02-create-vm.ps1 을 실행하세요." -ForegroundColor Green }
else     { Write-Host "[FAIL] 항목을 해결한 뒤 다시 실행하세요." -ForegroundColor Red }
