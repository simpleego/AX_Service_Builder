# Docker vs Kubernetes

# **Docker vs Kubernetes — 입문 개발자를 위한 비교**

**Docker는 애플리케이션을 컨테이너로 만들고 실행하는 기술이고, Kubernetes(K8s)는 여러 서버에 분산된 컨테이너를 자동으로 배포·관리하는 플랫폼입니다.**

두 기술은 경쟁 관계가 아니라 서로 다른 역할을 수행하는 상호 보완적인 기술입니다.&#x20;

<img width="32" height="32" alt="image" src="https://github.com/user-attachments/assets/258d78fe-93ff-451c-8582-cd266bb62c5c" /> Kubernetes

## **1. 가장 쉬운 비유: 식당 하나와 프랜차이즈 본사**
<img width="500" alt="image" src="https://github.com/user-attachments/assets/4221868a-da5c-4f2c-a00b-78af43e14b76" /> | <img width="500" alt="image" src="https://github.com/user-attachments/assets/b5748fdb-062f-45e2-946b-7d7f58bf2462" />



[Isometric flat 3D vector interior of professional restourant kitchen](https://images.openai.com/static-rsc-4/Uc83sKOO_2OCEwGwLFehmjsrTw4LAiuuPrMuScKhp2JyPdWq_X3qhyjpawma3FJ1aq3ycUBlNlrV8L02enMVAwn2pHA6JjxWxBdjjnk-4xeEFiOI3gjNu_rnDcfG0CFgFFaoiOCiIsck2SG42FQeIC-E2y9sh08Ip-VuLS2LqzHfHRoW2U9c4s4iCRdnJ3at?purpose=inline)

**Docker — 식당의 주방**

음식(애플리케이션)을 정해진 조리 환경(컨테이너)에서 일관되게 만들어 제공합니다.

[Patron Mobil | Restoran POS, QR Menü ve Operasyon Yönetim Sistemi](https://images.openai.com/static-rsc-4/3MzzqcqS-LUYMRjX-ct8DCAuBSqXkO-1U9Mvu_8TVnMioCPG4v3n1Yu9WpBkSOK7CSNvLhFC831VQx1pbzIp7RAo3Q-vQ5I5r20B3zU_X9GSbLmGVDjmsO-w0mgClbeUdSH7hDWaTlFcWhdVB64Ja6gwTAFJwAiExVy6CycBolQ?purpose=inline)

**Kubernetes — 프랜차이즈 운영 본사**

여러 지점(서버)에 업무를 배분하고, 장애가 발생하면 다른 지점에서 서비스를 유지하도록 조정합니다.

예를 들어 식당이 한 개라면 주방만 관리해도 충분할 수 있습니다. 그러나 수백 개의 지점을 운영해야 한다면 지점마다 주문량, 인력, 재고를 조정하는 중앙 관리 체계가 필요합니다.

이것이 Docker와 Kubernetes를 구분하는 가장 중요한 관점입니다.

## **2. Docker, Docker Compose, Kubernetes 비교**

앞서 학습한 Docker Compose까지 포함하면 차이가 더욱 명확해집니다.

| 비교 항목  | Docker          | Docker Compose   | Kubernetes           |
| ------ | --------------- | ---------------- | -------------------- |
| 핵심 목적  | 컨테이너 생성·실행      | 여러 컨테이너 구성·관리    | 클러스터 전체 운영 자동화       |
| 관리 단위  | 컨테이너            | 서비스 묶음           | Pod, Deployment 등    |
| 서버 범위  | 주로 단일 호스트       | 주로 단일 호스트        | 단일·다중 노드             |
| 설정 방식  | 명령어, Dockerfile | YAML             | YAML, Kubernetes API |
| 장애 복구  | 재시작 정책          | 재시작 정책           | 상태 감시 및 재생성·재배치      |
| 확장성    | 수동 중심           | 서비스 복제 가능        | 자동 수평 확장 지원          |
| 로드 밸런싱 | 별도 구성           | 별도 구성            | Service 기반 트래픽 분산    |
| 학습 난이도 | 낮음              | 낮음\~중간           | 높음                   |
| 주요 사용처 | 개발·테스트·실행       | 로컬 풀스택 환경·소규모 배포 | 대규모·고가용성 서비스         |

단, Kubernetes가 반드시 여러 대의 서버를 요구하는 것은 아닙니다. 한 대의 컴퓨터에서도 학습용 클러스터를 실행할 수 있습니다.

## **3. 구조로 보는 차이**

### **Docker + Docker Compose**

한 대의 Ubuntu VM에서 MySQL, FastAPI, React를 함께 운영

**Ubuntu VM / Docker Engine**

React

Container

:5173

FastAPI

Container

:8000

MySQL

Container

:3306

Docker 네트워크

docker compose up -d

서비스를 정의된 설정대로 한꺼번에 실행

### **Kubernetes 클러스터**

여러 서버에 애플리케이션을 분산하고 원하는 실행 상태를 유지

**Control Plane**

API Server · Scheduler · Controller Manager · etcd

배포 요청 처리 / 배치 결정 / 상태 감시

클러스터 상태 관리

Worker 1

React Pod

API Pod

Worker 2

API Pod

API Pod

Worker 3

API Pod

기타 Pod

kubectl apply -f deployment.yaml

선언한 Pod 개수와 배포 상태를 지속적으로 유지

이 구조에서 Kubernetes는 Docker Engine을 필수로 요구하지 않습니다. 현재 Kubernetes는 일반적으로 `containerd`, `CRI-O` 등의 CRI 호환 컨테이너 런타임으로 컨테이너를 실행합니다. Docker로 만든 OCI 호환 이미지도 사용할 수 있습니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://azure.microsoft.com\&sz=32)

Microsoft Azure+1



## **4. Kubernetes가 Docker보다 강력한 부분**

예를 들어 FastAPI 서비스를 운영한다고 가정하겠습니다.

### **① 자동 복구(Self-healing)**

Docker에서는 컨테이너가 종료되면 재시작 정책에 따라 같은 호스트에서 다시 실행할 수 있습니다.

Kubernetes에서는 특정 Pod가 사라지거나 노드에 문제가 발생하면 컨트롤러가 원하는 실행 상태를 회복하도록 새 Pod를 생성·배치합니다.

Kubernetes 자동 복구 시뮬레이션

Pod 장애 발생

API Pod 1

정상

API Pod 2

정상

API Pod 3

정상

원하는 Pod 3개 = 현재 정상 Pod 3개

단, 자동 복구가 모든 장애에 대한 무중단 서비스를 보장하는 것은 아닙니다. 실제 가용성은 복제본 수, 준비 상태 검사, 노드 구성 등에 따라 달라집니다.

### **② 자동 확장(Auto Scaling)**

사용자가 늘어나면 Kubernetes는 설정된 기준에 따라 실행 중인 애플리케이션의 복제본 수를 조정할 수 있습니다.

**트래픽 증가에 따른 Pod 확장 예시**

30% 부하

낮음

보통

높음

# **2**

Pod 개수

기본 서비스 운영

교육용 단순화 모델입니다. 실제 HPA는 CPU 사용률 등 설정된 메트릭과 정책에 따라 복제본을 조절하며, 트래픽 수치만으로 자동 결정되지는 않습니다.

### **③ 로드 밸런싱(Load Balancing)**

Kubernetes의 Service는 여러 Pod에 들어오는 네트워크 요청을 분산할 수 있습니다.

\#chatgpt-mermaid-\_r_18j\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_18j\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_18j\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_18j\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_18j\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_18j\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_18j\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_18j\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_18j\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_18j\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_18j\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_18j\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_18j\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_18j\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_18j\_ p{margin:0;}#chatgpt-mermaid-\_r_18j\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_18j\_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_18j\_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_18j\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_18j\_ .label text,#chatgpt-mermaid-\_r_18j\_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_18j\_ .node rect,#chatgpt-mermaid-\_r_18j\_ .node circle,#chatgpt-mermaid-\_r_18j\_ .node ellipse,#chatgpt-mermaid-\_r_18j\_ .node polygon,#chatgpt-mermaid-\_r_18j\_ .node path{fill:rgb(61, 34, 20);stroke:rgb(172, 79, 35);stroke-width:1px;}#chatgpt-mermaid-\_r_18j\_ .rough-node .label text,#chatgpt-mermaid-\_r_18j\_ .node .label text,#chatgpt-mermaid-\_r_18j\_ .image-shape .label,#chatgpt-mermaid-\_r_18j\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_18j\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_18j\_ .rough-node .label,#chatgpt-mermaid-\_r_18j\_ .node .label,#chatgpt-mermaid-\_r_18j\_ .image-shape .label,#chatgpt-mermaid-\_r_18j\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_18j\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_18j\_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_18j\_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_18j\_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-\_r_18j\_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-\_r_18j\_ .edgeLabel{background-color:rgb(14, 14, 14);text-align:center;}#chatgpt-mermaid-\_r_18j\_ .edgeLabel p{background-color:rgb(14, 14, 14);}#chatgpt-mermaid-\_r_18j\_ .edgeLabel rect{opacity:0.5;background-color:rgb(14, 14, 14);fill:rgb(14, 14, 14);}#chatgpt-mermaid-\_r_18j\_ .labelBkg{background-color:rgba(14, 14, 14, 0.5);}#chatgpt-mermaid-\_r_18j\_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-\_r_18j\_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_18j\_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_18j\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_18j\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_18j\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_18j\_ .icon-shape,#chatgpt-mermaid-\_r_18j\_ .image-shape{background-color:rgb(14, 14, 14);text-align:center;}#chatgpt-mermaid-\_r_18j\_ .icon-shape p,#chatgpt-mermaid-\_r_18j\_ .image-shape p{background-color:rgb(14, 14, 14);padding:2px;}#chatgpt-mermaid-\_r_18j\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_18j\_ .image-shape .label rect{opacity:0.5;background-color:rgb(14, 14, 14);fill:rgb(14, 14, 14);}#chatgpt-mermaid-\_r_18j\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_18j\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_18j\_ .node .neo-node{stroke:rgb(172, 79, 35);}#chatgpt-mermaid-\_r_18j\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_18j\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_18j\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_18j\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_18j\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_18j\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_18j\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_18j\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_18j\_ [data-look="neo"].node .neo-line path{stroke:rgb(172, 79, 35);filter:none;}#chatgpt-mermaid-\_r_18j\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_18j\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_18j\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_18j\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_18j\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_18j\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_18j\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_18j\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(255, 183, 144);}#chatgpt-mermaid-\_r_18j\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(255, 183, 144);}#chatgpt-mermaid-\_r_18j\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_18j\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_18j\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(40, 17, 5);stroke:rgb(92, 56, 31);stroke-width:1px;}#chatgpt-mermaid-\_r_18j\_ .node rect,#chatgpt-mermaid-\_r_18j\_ .node circle,#chatgpt-mermaid-\_r_18j\_ .node ellipse,#chatgpt-mermaid-\_r_18j\_ .node polygon,#chatgpt-mermaid-\_r_18j\_ .node path{fill:rgb(74, 34, 6);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_18j\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_18j\_ .mermaid-decision .label-container{fill:rgb(40, 17, 5);stroke:rgb(92, 56, 31);stroke-dasharray:2,2;}#chatgpt-mermaid-\_r_18j\_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_18j\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_18j\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}사용자 요청Kubernetes ServiceFastAPI Pod 1FastAPI Pod 2FastAPI Pod 3

이 외에도 Kubernetes는 롤링 업데이트, 서비스 디스커버리, 스토리지 오케스트레이션 등의 기능을 제공합니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://kubernetes.io\&sz=32)

Kubernetes+1



## **5. 같은 FastAPI 서비스를 배포한다면?**

### **Docker Compose 방식**

```
services:
  backend:
    image: my-fastapi:1.0
    ports:
      - "8000:8000"
```

```
docker compose up -d
```

### **Kubernetes 방식**

Kubernetes는 일반적으로 Deployment와 Service를 별도로 정의합니다.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
        - name: backend
          image: my-fastapi:1.0
          ports:
            - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  selector:
    app: fastapi
  ports:
    - port: 8000
      targetPort: 8000
```

```
kubectl apply -f fastapi.yaml
```

위 예제에서는 Kubernetes가 FastAPI Pod 3개를 유지하도록 설정합니다. Service는 클러스터 내부에서 이 Pod들에 접근하는 통로를 제공합니다. 외부 인터넷에 공개하려면 별도의 노출 방식이 필요합니다.

## **6. 현재 MySQL 실습에서는 무엇을 선택해야 할까?**

현재처럼 Windows, VirtualBox, Ubuntu VM을 이용해 MySQL 8.4 DB 서버를 구성하고, Python 클라이언트로 접속하는 실습에서는 **Docker Compose가 더 적합합니다.**

| 개발 환경                   | 권장 기술          | 이유                 |
| ----------------------- | -------------- | ------------------ |
| MySQL DB 실습             | Docker Compose | 설정과 데이터 관리가 간단     |
| React + FastAPI + MySQL | Docker Compose | 여러 서비스를 한 번에 실행    |
| 팀 프로젝트 서버 1대            | Docker Compose | 구성과 유지보수가 상대적으로 쉬움 |
| 여러 서버에 분산된 API          | Kubernetes 검토  | 배포·복구·확장 자동화       |
| 대규모 서비스와 높은 가용성 요구      | Kubernetes     | 클러스터 기반 운영 기능      |

특히 MySQL과 같은 데이터베이스는 Kubernetes에 배포한다고 해서 데이터 복제, 장애 복구, 백업이 자동으로 완성되지는 않습니다. StatefulSet, 영구 볼륨, 데이터베이스 복제·백업 전략 등을 별도로 설계해야 합니다.

## **7. 입문 개발자를 위한 학습 순서**

1. **Docker 기본**

   이미지, 컨테이너, Dockerfile, 포트 매핑, 볼륨, 네트워크
2. **Docker Compose**

   YAML, services, environment, ports, volumes, healthcheck
3. **풀스택 컨테이너화**

   React + FastAPI + MySQL을 Compose로 통합 실행
4. **Kubernetes 기본**

   Cluster, Node, Pod, Deployment, Service
5. **Kubernetes 운영**

   ReplicaSet, HPA, Ingress/Gateway, ConfigMap, Secret, PVC, StatefulSet

## **최종 정리**

- **Docker:** 애플리케이션을 컨테이너로 만들어 실행한다.
- **Docker Compose:** 여러 컨테이너를 하나의 설정 파일로 실행·관리한다.
- **Kubernetes:** 컨테이너 기반 애플리케이션을 클러스터 전체에서 자동 배포·확장·복구한다.

현재 진행 중인 풀스택 교육에서는 **Docker와 Docker Compose를 충분히 실습한 다음 Kubernetes의 기본 개념으로 확장하는 순서**가 적합합니다. Kubernetes는 Docker의 상위 버전이 아니라, 컨테이너 운영의 복잡성을 해결하기 위한 별도의 플랫폼이라는 점을 학생들에게 강조하면 좋습니다.

<img width="848" height="1036" alt="image" src="https://github.com/user-attachments/assets/684524f3-ac7a-4760-816f-a81abedd1dde" />
