# Polymarket Autonomous Trading Agent (Compliance-First)

이 저장소는 **Polymarket용 컴플라이언스 우선(compliance-first) 자율 트레이딩 에이전트 스캐폴드**입니다.

## 중요 고지 (반드시 읽어주세요)

- 이 소프트웨어는 교육/연구/엔지니어링 목적입니다.
- 수익을 **보장하지 않습니다**.
- 어떤 트레이딩 시스템도 고정 일수익(예: `$1,000/day`)을 안전하게 약속할 수 없습니다.
- 법률/세무/규제 준수 책임은 전적으로 사용자에게 있습니다.

---

## 이 에이전트가 하는 일

- Polymarket API에서 마켓 데이터를 가져옵니다.
- 모델 추정 확률과 시장 가격 차이(edge) 기반의 단순 시그널을 생성합니다.
- 주문 전 리스크 제한(포지션 사이징, 일간 손실 제한)을 적용합니다.
- 관할 허용 목록 + 라이브 리스크 확인 플래그로 라이브 모드를 게이트합니다.
- 기본은 Paper(시뮬레이션) 모드입니다.

---

## 프로젝트 구조

- `trading_agent/config.py` — 실행 설정 로딩(환경변수 기반)
- `trading_agent/compliance.py` — 관할/라이브 승인 체크
- `trading_agent/polymarket_client.py` — Polymarket HTTP 클라이언트
- `trading_agent/strategy.py` — 시그널 생성
- `trading_agent/risk.py` — 리스크/사이징
- `trading_agent/agent.py` — 루프 오케스트레이션
- `main.py` — CLI 진입점

---

## 실행 및 사용 방법 (STEP BY STEP, 생략 없음)

아래는 **처음 설치부터 실행까지** 한 단계도 건너뛰지 않는 순서입니다.

### 0) 사전 준비

1. Python 3.10+가 설치되어 있는지 확인합니다.
2. 터미널에서 프로젝트 폴더로 이동합니다.

```bash
cd /workspace/Polymarket_DIE
```

### 1) 가상환경 생성

```bash
python -m venv .venv
```

### 2) 가상환경 활성화

- macOS / Linux:

```bash
source .venv/bin/activate
```

- Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3) 의존성 설치

```bash
pip install -r requirements.txt
```

### 4) 환경변수 설정

최소한 관할 정보는 설정하는 것을 권장합니다.

- macOS / Linux 예시:

```bash
export AGENT_JURISDICTION=CA
export AGENT_CAPITAL_USD=10000
export AGENT_MAX_RISK_PER_TRADE=0.01
export AGENT_MAX_DAILY_DRAWDOWN=0.03
```

- Windows PowerShell 예시:

```powershell
$env:AGENT_JURISDICTION="CA"
$env:AGENT_CAPITAL_USD="10000"
$env:AGENT_MAX_RISK_PER_TRADE="0.01"
$env:AGENT_MAX_DAILY_DRAWDOWN="0.03"
```

> 참고: `AGENT_JURISDICTION`가 허용 목록(`CA, FR, DE, JP, SG, UK`) 밖이면 실행이 차단됩니다.

### 5) 테스트 먼저 실행 (권장)

```bash
python -m pytest -q
```

### 6) Paper 모드 1회 실행

```bash
python main.py --paper
```

성공 시 `{"mode": "paper", "actions": [...]}` 형태의 출력이 표시됩니다.

### 7) 출력 해석 방법

- `actions`가 빈 배열이면: 현재 조건에 맞는 시그널이 없었거나 사이징 결과가 0입니다.
- `actions`에 항목이 있으면: 현재 코드는 안전을 위해 `SIMULATED` 주문으로만 반환합니다.
- `HALTED`가 보이면: 일간 최대 손실 제한에 걸려 거래가 멈춘 상태입니다.

### 8) 라이브 모드 설명 (주의)

현재 코드는 실제 주문 라우팅이 **의도적으로 스텁 처리**되어 있습니다.
즉, `--live`를 써도 실거래 체결 로직은 구현되어 있지 않습니다.

라이브 플래그 사용 형태:

```bash
python main.py --live --ack-live-risk
```

- `--ack-live-risk` 없이 `--live`만 사용하면 실행이 차단됩니다.

### 9) 실행 중 자주 나는 문제와 해결

1. `ModuleNotFoundError`:
   - 가상환경 활성화 여부 확인
   - `pip install -r requirements.txt` 재실행

2. 관할 오류(RuntimeError with allowlist message):
   - `AGENT_JURISDICTION` 값을 허용된 코드로 설정

3. 네트워크/API 오류:
   - 인터넷 연결 확인
   - `POLYMARKET_API_BASE` 변경 여부 확인

### 10) 실행 종료

- Paper 모드는 1회 실행 후 자동 종료됩니다.
- 가상환경 비활성화:

```bash
deactivate
```

---

## 환경변수 전체 목록

- `POLYMARKET_API_BASE` (기본: `https://gamma-api.polymarket.com`)
- `POLYMARKET_PRIVATE_KEY` (실거래 구현 시 필요)
- `POLYMARKET_CHAIN_ID` (기본: `137`)
- `AGENT_CAPITAL_USD` (기본: `10000`)
- `AGENT_MAX_RISK_PER_TRADE` (기본: `0.01`)
- `AGENT_MAX_DAILY_DRAWDOWN` (기본: `0.03`)
- `AGENT_JURISDICTION` (예: `US`, `CA`)
- `AGENT_POLL_INTERVAL_SECONDS` (기본: `60`)

---

## 테스트

```bash
pytest -q
```
