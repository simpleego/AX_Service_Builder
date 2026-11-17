# Docker 설치 문제 진단용 (읽기 전용 - 시스템을 변경하지 않음)
# 관리자 PowerShell에서 실행: powershell -ExecutionPolicy Bypass -File E:\AX_WORK\Docker\docker-diag-admin.ps1
$out = "E:\AX_WORK\Docker\docker-diag-result.txt"
& {
  "=== Run at $(Get-Date) / Admin: $(([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))"
  "`n=== Optional features ==="
  'VirtualMachinePlatform','Microsoft-Windows-Subsystem-Linux','Microsoft-Hyper-V-All','Microsoft-Hyper-V-Hypervisor','HypervisorPlatform','Containers' | ForEach-Object {
    $f = Get-WindowsOptionalFeature -Online -FeatureName $_ -ErrorAction SilentlyContinue
    "{0,-40} {1}" -f $_, $(if ($f) { $f.State } else { 'N/A' })
  }
  "`n=== bcdedit /enum {current} ==="
  bcdedit /enum '{current}'
  "`n=== Device Guard / VBS ==="
  Get-CimInstance -Namespace root\Microsoft\Windows\DeviceGuard -ClassName Win32_DeviceGuard -ErrorAction SilentlyContinue | Format-List VirtualizationBasedSecurityStatus, SecurityServicesConfigured, SecurityServicesRunning, RequiredSecurityProperties
  "`n=== Memory integrity (HVCI) registry ==="
  Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity' -ErrorAction SilentlyContinue | Select-Object Enabled
  "`n=== DISM log (feature related, last 60) ==="
  Select-String -Path C:\Windows\Logs\DISM\dism.log -Pattern 'VirtualMachinePlatform|Hyper-V|Subsystem-Linux|Error|failed' -ErrorAction SilentlyContinue | Select-Object -Last 60 | ForEach-Object { $_.Line }
  "`n=== CBS log (rollback / failure, last 80) ==="
  Select-String -Path C:\Windows\Logs\CBS\CBS.log -Pattern 'VirtualMachinePlatform|Hypervisor|rollback|Rolling back|Failed|0x800f' -ErrorAction SilentlyContinue | Select-Object -Last 80 | ForEach-Object { $_.Line }
  "`n=== Hyper-V hypervisor operational log ==="
  Get-WinEvent -LogName 'Microsoft-Windows-Hyper-V-Hypervisor-Operational' -MaxEvents 30 -ErrorAction SilentlyContinue | Format-Table TimeCreated, Id, Message -Wrap -AutoSize | Out-String -Width 250
  "`n=== Boot drivers from AhnLab ==="
  Get-CimInstance Win32_SystemDriver | Where-Object { $_.PathName -match 'AhnLab|ahn' } | Format-Table Name, State, StartMode, PathName -AutoSize | Out-String -Width 250
} *>&1 | Out-File -FilePath $out -Encoding utf8
"결과 저장 완료: $out"
