# ============================================================
#  2단계: Ubuntu Server VM 생성 + 무인(자동) 설치
#  실행: powershell -ExecutionPolicy Bypass -File .\02-create-vm.ps1
#  (관리자 권한 필요 없음)
# ============================================================
$ErrorActionPreference = "Stop"
. "$PSScriptRoot\config.ps1"

function VBox { & $VBoxManage @args; if ($LASTEXITCODE -ne 0) { throw "VBoxManage $($args -join ' ') 실패 (exit $LASTEXITCODE)" } }

if (-not (Test-Path $VBoxManage)) { throw "VirtualBox 가 설치되어 있지 않습니다. 01-check-host.ps1 을 먼저 실행하세요." }
if ((Get-CimInstance Win32_ComputerSystem).HypervisorPresent) {
  throw "Windows 하이퍼바이저가 켜져 있습니다. 'bcdedit /set hypervisorlaunchtype off' 후 재부팅하세요."
}

$iso = Get-ChildItem $IsoDir -Filter "ubuntu-*-live-server-amd64.iso" -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First 1
if (-not $iso) { throw "$IsoDir 에 ubuntu-*-live-server-amd64.iso 가 없습니다." }

$existing = & $VBoxManage list vms | Select-String "^`"$VmName`""
if ($existing) { throw "'$VmName' VM 이 이미 있습니다. 다시 만들려면 VirtualBox 에서 삭제(모든 파일 삭제)한 뒤 실행하세요." }

New-Item -ItemType Directory -Force $VmBaseDir, $ShareHostDir | Out-Null

Write-Host "VM 생성: $VmName  (ISO: $($iso.Name))" -ForegroundColor Cyan
VBox createvm --name $VmName --ostype Ubuntu_64 --basefolder $VmBaseDir --register

VBox modifyvm $VmName `
  --cpus $VmCpus --memory $VmMemoryMB --vram 16 `
  --graphicscontroller vmsvga --firmware bios `
  --ioapic on `
  --audio-driver none --usb-ohci off `
  --nic1 nat --clipboard-mode bidirectional

# 디스크 + 컨트롤러
$vdi = Join-Path $VmBaseDir "$VmName\$VmName.vdi"
VBox createmedium disk --filename $vdi --size $VmDiskMB --format VDI --variant Standard
VBox storagectl $VmName --name "SATA" --add sata --controller IntelAhci --portcount 2 --bootable on
VBox storageattach $VmName --storagectl "SATA" --port 0 --device 0 --type hdd --medium $vdi

# NAT 포트포워딩
foreach ($pf in $PortForwards) {
  $n, $hp, $gp = $pf.Split(",")
  VBox modifyvm $VmName --natpf1 "$n,tcp,127.0.0.1,$hp,,$gp"
}

# 공유 폴더 (Guest Additions 설치 후 /media/sf_work 로 자동 마운트)
VBox sharedfolder add $VmName --name $ShareName --hostpath $ShareHostDir --automount

# 무인 설치 (Ubuntu + Guest Additions + OpenSSH)
Write-Host "무인 설치 구성 중..." -ForegroundColor Cyan
VBox unattended install $VmName `
  --iso $iso.FullName `
  --user $VmUser --password $VmPassword --full-user-name "Docker Lab" `
  --hostname $VmHostname `
  --locale en_US --country KR --time-zone Asia/Seoul `
  --install-additions `
  --package-selection-adjustment minimal `
  --post-install-command "apt-get install -y openssh-server; systemctl enable ssh || true"

VBox startvm $VmName --type gui

Write-Host ""
Write-Host "VM 이 시작되었습니다. Ubuntu 자동 설치가 10~20분 정도 걸립니다." -ForegroundColor Green
Write-Host "로그인 화면(docker-lab login:)이 나오면 설치가 끝난 것입니다."
Write-Host "그다음 03-install-docker.ps1 을 실행하세요."
