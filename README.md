# 📊 원자재/통화 시장 모니터링 시스템

> GitHub Actions 기반 자동화 원자재·통화 시장 분석 및 알림 시스템

## ✨ 주요 기능

### 📈 시장 데이터 수집
- **원자재**: 금, 은, 구리, 원유(WTI) 등
- **통화**: 달러/원, 달러/엔, 유로/달러 등
- Yahoo Finance API를 통한 실시간 데이터 수집

### 🔍 기술적 분석
- 이동평균선 (MA5, MA20, MA60, MA120) 계산
- 골든크로스/데드크로스 감지
- 정배열/역배열 패턴 분석
- 52주 최고/최저 경신 감지
- 자산 간 상관관계 분석

### 🔔 스마트 알림 시스템
- **Level 1**: 일일 종합 리포트 (조용히)
- **Level 2**: 주의 알림 (변동률 ±2% 이상)
- **Level 3**: 긴급 알림 (변동률 ±3% 이상, 52주 신고가/신저가)

### 📊 리포트 생성
- **엑셀**: 6개 시트 포함 상세 분석 리포트
- **마크다운**: GitHub에서 바로 확인 가능한 분석 리포트
- **JSON**: 프로그래밍 방식 데이터 접근

## 🚀 시작하기

### 1. 저장소 설정

```bash
# 저장소 클론
git clone [your-repo-url]
cd commodity_monitor

# 의존성 설치
pip install -r requirements.txt
```

### 2. GitHub Secrets 설정

Repository Settings > Secrets and variables > Actions에서 다음 추가:

- `TELEGRAM_BOT_TOKEN`: 텔레그램 봇 토큰
- `TELEGRAM_CHAT_ID`: 텔레그램 채팅 ID

### 3. 모니터링 자산 설정

`config.py`에서 모니터링할 자산 설정:

```python
ASSETS = {
    'commodities': {
        'GOLD': {
            'name': '금',
            'spot_ticker': 'GC=F',
            'enabled': True  # True/False로 쉽게 켜고 끄기
        },
        # ... 더 많은 자산
    }
}
```

## 📁 프로젝트 구조

```
commodity_monitor/
├── __init__.py              # 패키지 초기화
├── config.py                # 설정 파일 (자산, 알림 임계값 등)
├── data_collector.py        # 데이터 수집 모듈
├── data_processor.py        # 데이터 처리 및 기술 지표 계산
├── alert_manager.py         # 알림 조건 판단 및 리포트 생성
├── telegram_notifier.py     # 텔레그램 알림 발송
├── excel_reporter.py        # 엑셀 리포트 생성
├── main.py                  # 메인 실행 파일
├── requirements.txt         # 의존성 패키지
└── .github/
    └── workflows/
        └── commodity_monitor.yml  # GitHub Actions 워크플로우

생성되는 디렉토리:
market_data/                 # CSV, JSON 데이터 저장
├── GOLD_history.csv
├── SILVER_history.csv
├── collection_summary.json
└── processed_data.json

analysis_reports/            # 분석 리포트 저장
├── commodity_report_YYYYMMDD.xlsx
└── market_analysis_YYYYMMDD_HHMMSS.md
```

## ⏰ 실행 스케줄

- **자동 실행**: 매일 4회 (KST 9시, 15시, 21시, 3시)
- **수동 실행**: Actions 탭에서 언제든지 가능

## 📊 리포트 예시

### 텔레그램 알림

```
📊 원자재/통화 모니터링 요약
🕐 2024-01-15 09:00

✅ 모니터링 자산: 7개
⚠️ 주의 알림: 2건
🚨 긴급 알림: 1건

📁 상세 데이터: market_data/
📄 분석 리포트: analysis_reports/
📊 엑셀 파일 참조
```

### 엑셀 리포트 시트

1. 📊 종합요약
2. 📅 일자별상세
3. 📈 주간추이
4. 📊 월간추이
5. 🔧 기술지표
6. 🔗 상관관계

## 🎯 커스터마이징

### 알림 임계값 조정

`config.py`에서 수정:

```python
ALERT_THRESHOLDS = {
    'warning': {
        'daily_change': 2.0,  # 주의: ±2%
    },
    'emergency': {
        'daily_change': 3.0,  # 긴급: ±3%
    }
}
```

### 이동평균선 기간 변경

```python
MOVING_AVERAGES = [5, 20, 60, 120]  # 원하는 기간 추가/제거
```

## 💡 추가 가능한 자산

Yahoo Finance에서 지원하는 모든 티커 추가 가능:

- **귀금속**: 백금(PL=F), 팔라듐(PA=F)
- **에너지**: 브렌트유(BZ=F), 천연가스(NG=F)
- **농산물**: 밀(ZW=F), 옥수수(ZC=F), 대두(ZS=F)
- **암호화폐**: BTC-USD, ETH-USD

## 🔧 문제 해결

### Actions 실행 실패 시

1. Secrets 설정 확인
2. `permissions: contents: write` 확인
3. Actions 로그에서 오류 메시지 확인

### 데이터가 수집되지 않을 때

- Yahoo Finance 티커 심볼 확인
- 네트워크 연결 상태 확인
- API 제한 확인 (일시적으로 sleep 시간 증가)

## 📝 라이선스

MIT License

## 🤝 기여

Issue와 Pull Request 환영합니다!
