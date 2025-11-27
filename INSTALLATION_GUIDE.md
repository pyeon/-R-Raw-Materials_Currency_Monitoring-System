# 🚀 원자재/통화 모니터링 시스템 설치 가이드

## 📦 전체 구조

```
commodity_monitor/
├── .github/workflows/
│   └── commodity_monitor.yml      # GitHub Actions 워크플로우
├── __init__.py                    # 패키지 초기화
├── config.py                      # 설정 (자산, 임계값)
├── data_collector.py              # 데이터 수집 + JSON 저장
├── data_processor.py              # 데이터 처리 + JSON 저장
├── alert_manager.py               # 알림 생성 + MD 리포트
├── telegram_notifier.py           # 텔레그램 요약 전송
├── excel_reporter.py              # 엑셀 리포트 생성
├── main.py                        # 메인 실행
├── requirements.txt               # 의존성
├── README.md                      # 프로젝트 문서
└── .gitignore                     # Git 제외 파일

생성되는 디렉토리:
├── market_data/                   # Git에 커밋됨
│   ├── GOLD_history.csv
│   ├── SILVER_history.csv
│   ├── collection_summary.json
│   └── processed_data.json
└── analysis_reports/              # Git에 커밋됨
    ├── commodity_report_YYYYMMDD.xlsx
    └── market_analysis_YYYYMMDD_HHMMSS.md
```

## 🔧 GitHub Actions 제한 해결 패턴 적용

### ✅ 적용된 개선사항

1. **API → 데이터 → 저장 → Git push**
   - Yahoo Finance API로 데이터 수집
   - JSON/CSV/Excel/MD 파일로 저장
   - Git에 자동 커밋 및 푸시

2. **Telegram 요약만 전송**
   - 상세 데이터는 GitHub 저장
   - 텔레그램은 통계 요약만
   - 파일 다운로드는 엑셀 파일 전송

3. **저장소 활용도 극대화**
   - market_data/: 원시 데이터 (CSV, JSON)
   - analysis_reports/: 분석 결과 (Excel, MD)
   - Git 히스토리로 시계열 추적 가능

## 📋 설치 단계

### 1. 저장소 생성 및 파일 업로드

```bash
# 1. GitHub에서 새 저장소 생성
# 2. commodity_monitor 폴더 전체를 저장소에 업로드

git init
git add .
git commit -m "🎉 원자재/통화 모니터링 시스템 초기 설정"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. GitHub Secrets 설정

Settings > Secrets and variables > Actions > New repository secret

필수 Secrets:
- `TELEGRAM_BOT_TOKEN`: @BotFather에서 받은 봇 토큰
- `TELEGRAM_CHAT_ID`: 본인의 Chat ID (숫자)

### 3. GitHub Actions 활성화

- Actions 탭 > "I understand my workflows, go ahead and enable them" 클릭
- 워크플로우 자동 실행 시작

## 🎯 자산 설정 (config.py)

### 활성화/비활성화

```python
ASSETS = {
    'commodities': {
        'GOLD': {
            'name': '금',
            'spot_ticker': 'GC=F',
            'enabled': True  # ← 이것만 바꾸면 됨!
        },
        'SILVER': {
            'enabled': False  # 비활성화
        }
    }
}
```

### 새 자산 추가

```python
'PLATINUM': {
    'name': '백금',
    'spot_ticker': 'PL=F',
    'unit': 'oz',
    'icon': '⚪',
    'enabled': True
}
```

## ⏰ 실행 스케줄

기본 설정 (commodity_monitor.yml):

```yaml
schedule:
  - cron: '0 0,6,12,18 * * *'  # 매일 4회
```

시간 변경 예시:
- `0 0 * * *`: 매일 1회 (KST 9시)
- `0 */6 * * *`: 매 6시간마다
- `0 0,12 * * *`: 매일 2회 (KST 9시, 21시)

## 🔔 알림 임계값 조정 (config.py)

```python
ALERT_THRESHOLDS = {
    'warning': {
        'daily_change': 2.0,   # ±2% 이상 → 주의
    },
    'emergency': {
        'daily_change': 3.0,   # ±3% 이상 → 긴급
    }
}
```

## 📊 출력물 설명

### 1. market_data/ (데이터 저장소)

- `{ASSET}_history.csv`: 최근 280일 가격 데이터
- `collection_summary.json`: 수집 성공/실패 통계
- `processed_data.json`: 계산된 지표 및 분석 결과

### 2. analysis_reports/ (리포트)

- `commodity_report_YYYYMMDD.xlsx`: 6개 시트 상세 엑셀 리포트
- `market_analysis_YYYYMMDD_HHMMSS.md`: GitHub에서 바로 보는 마크다운 리포트

### 3. 텔레그램 알림

```
📊 원자재/통화 모니터링 요약
🕐 2024-01-15 09:00
──────────────────────────────

✅ 모니터링 자산: 7개
⚠️ 주의 알림: 2건
🚨 긴급 알림: 1건

──────────────────────────────
📁 상세 데이터: market_data/
📄 분석 리포트: analysis_reports/
📊 엑셀 파일 참조
```

## 🔍 로그 확인

Actions 탭에서 실행 로그 확인:

```
📥 Step 1: 데이터 수집 중...
📊 금 데이터 수집 중...
✅ GOLD 데이터 저장: market_data/GOLD_history.csv
...

📊 Step 2: 데이터 처리 및 지표 계산 중...
✅ 처리 데이터 저장: market_data/processed_data.json

🔔 Step 3: 알림 조건 분석 중...
   - Level 1 (일반): 7개
   - Level 2 (주의): 2개
   - Level 3 (긴급): 1개

📄 Step 4: 엑셀 리포트 생성 중...
✅ 엑셀 리포트 생성: analysis_reports/commodity_report_20240115.xlsx

📱 Step 5: 텔레그램 요약 알림 발송 중...
✅ 텔레그램 전송 성공
✅ 파일 전송 성공
```

## 🛠️ 문제 해결

### Actions가 실행되지 않음

- Settings > Actions > General > Workflow permissions
- "Read and write permissions" 선택
- "Allow GitHub Actions to create and approve pull requests" 체크

### 텔레그램 알림이 안 옴

```bash
# 봇 토큰 테스트
curl "https://api.telegram.org/bot{YOUR_TOKEN}/getMe"

# Chat ID 확인
curl "https://api.telegram.org/bot{YOUR_TOKEN}/getUpdates"
```

### 데이터가 수집되지 않음

1. Yahoo Finance 티커 확인: https://finance.yahoo.com
2. Actions 로그에서 오류 메시지 확인
3. API 제한 시 `time.sleep(1)` 증가

## 🎨 커스터마이징 팁

### 1. 더 많은 자산 추가

```python
# config.py에 추가
'BTC': {
    'name': '비트코인',
    'ticker': 'BTC-USD',
    'icon': '₿',
    'enabled': True
}
```

### 2. 이동평균선 기간 변경

```python
MOVING_AVERAGES = [5, 10, 20, 60, 120, 200]  # 원하는 기간
```

### 3. 상관관계 패턴 추가

```python
CORRELATION_PATTERNS = {
    'GOLD_OIL': {
        'assets': ['GOLD', 'CRUDE_OIL'],
        'expected': 'positive',
        'threshold': 0.4,
    }
}
```

## 📚 참고 자료

- [Yahoo Finance 티커 검색](https://finance.yahoo.com)
- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## ✨ 활용 아이디어

1. **포트폴리오 모니터링**: 보유 자산만 활성화
2. **알림 조건 강화**: 임계값 낮춰서 더 민감하게
3. **시계열 분석**: Git 히스토리로 과거 데이터 추적
4. **상관관계 연구**: JSON 데이터로 Python 분석
5. **자동 매매 신호**: 크로스 신호를 매매 알림으로 활용

---

**문의사항이나 개선 제안은 Issue로 남겨주세요!** 🙏
