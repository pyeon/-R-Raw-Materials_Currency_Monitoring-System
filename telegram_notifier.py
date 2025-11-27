"""
텔레그램 알림 발송 모듈 (요약만 전송)
"""
import requests
from datetime import datetime
from typing import List, Dict
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramNotifier:
    """텔레그램 알림 클래스"""
    
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_daily_report(self, alerts: Dict[str, List]):
        """일일 요약 리포트 전송 (상세 내용은 제외)"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # 요약 통계
        total_assets = len(alerts['level1'])
        warning_count = len(alerts['level2'])
        emergency_count = len(alerts['level3'])
        
        message = f"📊 원자재/통화 모니터링 요약\n"
        message += f"🕐 {now}\n"
        message += "─" * 30 + "\n\n"
        
        # 통계 요약
        message += f"✅ 모니터링 자산: {total_assets}개\n"
        
        if warning_count > 0:
            message += f"⚠️ 주의 알림: {warning_count}건\n"
        
        if emergency_count > 0:
            message += f"🚨 긴급 알림: {emergency_count}건\n"
        
        if warning_count == 0 and emergency_count == 0:
            message += "✨ 특이사항 없음\n"
        
        message += "\n" + "─" * 30
        message += "\n📁 상세 데이터: market_data/"
        message += "\n📄 분석 리포트: analysis_reports/"
        message += "\n📊 엑셀 파일 참조"
        
        # 조용히 전송
        self._send_message(message, silent=True)
        
        # Level 2: 주의 알림 (있는 경우만)
        if alerts['level2']:
            warning_msg = "⚠️ 주의 알림\n\n" + "\n".join(alerts['level2'][:5])  # 최대 5개만
            if len(alerts['level2']) > 5:
                warning_msg += f"\n\n... 외 {len(alerts['level2']) - 5}건"
            self._send_message(warning_msg, silent=False)
        
        # Level 3: 긴급 알림 (있는 경우만, 별도 메시지)
        if alerts['level3']:
            emergency_msg = "🚨 긴급 알림\n\n" + "\n".join(alerts['level3'][:5])  # 최대 5개만
            if len(alerts['level3']) > 5:
                emergency_msg += f"\n\n... 외 {len(alerts['level3']) - 5}건"
            self._send_message(emergency_msg, silent=False)
    
    def _send_message(self, message: str, silent: bool = False):
        """메시지 전송"""
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_notification': silent
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ 텔레그램 전송 성공 (조용히: {silent})")
            else:
                print(f"❌ 텔레그램 전송 실패: {response.text}")
                
        except Exception as e:
            print(f"❌ 텔레그램 전송 오류: {e}")
    
    def send_file(self, filepath: str, caption: str = ""):
        """파일 전송"""
        try:
            url = f"{self.base_url}/sendDocument"
            
            with open(filepath, 'rb') as file:
                files = {'document': file}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption
                }
                
                response = requests.post(url, files=files, data=data, timeout=30)
                
                if response.status_code == 200:
                    print(f"✅ 파일 전송 성공: {filepath}")
                else:
                    print(f"❌ 파일 전송 실패: {response.text}")
                    
        except Exception as e:
            print(f"❌ 파일 전송 오류: {e}")
    
    def send_error_alert(self, error_message: str):
        """오류 알림 전송"""
        message = f"🚨 시스템 오류 발생\n\n{error_message}\n\n자세한 내용은 GitHub Actions 로그를 확인하세요."
        self._send_message(message, silent=False)
