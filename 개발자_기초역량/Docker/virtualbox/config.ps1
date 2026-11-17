# ============================================================
#  Docker 실습용 VirtualBox VM 설정값
#  (다른 스크립트들이 이 파일을 불러와서 사용합니다)
# ============================================================

# VM 이름 / 저장 위치 (C: 여유 공간이 적어서 E: 드라이브에 둡니다)
$VmName      = "docker-lab"
$VmBaseDir   = "E:\AX_WORK\Docker\virtualbox\vms"

# 자원 (호스트: 16 스레드 / 16GB RAM 기준)
$VmCpus      = 4
$VmMemoryMB  = 6144      # 6GB
$VmDiskMB    = 40960     # 40GB (동적 할당 - 실제 사용한 만큼만 차지)

# Ubuntu Server ISO 위치 (iso 폴더에 ubuntu-24.04.x-live-server-amd64.iso 를 넣어두세요)
$IsoDir      = "E:\AX_WORK\Docker\virtualbox\iso"

# VM 안의 계정 (강의용 테스트 계정 - 필요하면 바꾸세요)
$VmUser      = "docker"
$VmPassword  = "docker"
$VmHostname  = "docker-lab.local"

# Windows <-> VM 공유 폴더 (VM 안에서는 /media/sf_work 로 보입니다)
$ShareHostDir = "E:\AX_WORK\Docker\work"
$ShareName    = "work"

# NAT 포트포워딩: "이름,호스트포트,VM포트"
# Windows 브라우저에서 http://localhost:<호스트포트> 로 VM 안의 컨테이너에 접속합니다.
$PortForwards = @(
  "ssh,2222,22",
  "http,8080,80",
  "web3000,3000,3000",
  "web5000,5000,5000",
  "web8000,8000,8000",
  "jupyter,8888,8888"
)

# VBoxManage 경로
$VBoxManage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
