# NEW FILE: traffic/services/vnnox_service.py
# Create this new file in traffic/services/vnnox_service.py

import json
import logging
import requests
import hashlib
import time
import uuid
from django.conf import settings

logger = logging.getLogger(__name__)


class VnnoxService:
    """
    Service to send emergency messages to Vnnox VMS boards
    """
    
    def __init__(self):
        self.base_url = settings.VNNOX_BASE_URL
        self.app_key = settings.VNNOX_APP_KEY
        self.app_secret = settings.VNNOX_APP_SECRET
        self.timeout = 30
    
    def _build_headers(self):
        """Build headers with signature for Vnnox API"""
        cur_time = str(int(time.time()))
        nonce = uuid.uuid4().hex
        raw = f"{self.app_secret}{nonce}{cur_time}".encode("utf-8")
        checksum = hashlib.sha1(raw).hexdigest()
        
        return {
            "Content-Type": "application/json;charset=utf-8",
            "AppKey": self.app_key,
            "Nonce": nonce,
            "CurTime": cur_time,
            "CheckSum": checksum,
        }
    
    def send_message(self, player_ids, message_text, priority='normal', duration=300):
        """
        Send message to VMS boards via Vnnox
        
        Args:
            player_ids: List of player/board IDs
            message_text: Message to display
            priority: 'normal', 'high', or 'critical'
            duration: Display duration in seconds
        
        Returns:
            {'success': True/False, 'message_id': '...', 'response': {...}}
        """
        
        try:
            url = f"{self.base_url}/v2/player/program/normal"
            
            payload = {
                'player_ids': player_ids,
                'programs': [
                    {
                        'name': 'Emergency Message',
                        'content': message_text,
                        'duration': duration,
                    }
                ]
            }
            
            headers = self._build_headers()
            
            logger.info(f"Sending message to Vnnox: {message_text[:100]}... to {len(player_ids)} players")
            
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                logger.info(f"Message sent successfully: {data}")
                
                return {
                    'success': True,
                    'message_id': data.get('id', ''),
                    'sent_to': len(player_ids),
                    'response': data,
                }
            else:
                logger.error(f"Vnnox error: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'response': response.text,
                }
        
        except Exception as e:
            logger.exception(f"Error sending message: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
    
    def send_emergency_message(self, player_ids, message_text, duration=600):
        """
        Send EMERGENCY message (red background, critical priority)
        
        Args:
            player_ids: List of player/board IDs
            message_text: Emergency message
            duration: Display duration
        
        Returns:
            {'success': True/False, 'response': {...}}
        """
        
        try:
            url = f"{self.base_url}/v2/player/emergency-program/page"
            
            payload = {
                'player_ids': player_ids,
                'page': {
                    'content': message_text,
                    'duration': duration,
                    'background_color': 'red',
                }
            }
            
            headers = self._build_headers()
            
            logger.info(f"Sending EMERGENCY to Vnnox: {message_text[:100]}...")
            
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                logger.info(f"Emergency sent: {data}")
                
                return {
                    'success': True,
                    'message_id': data.get('id', ''),
                    'sent_to': len(player_ids),
                    'response': data,
                }
            else:
                logger.error(f"Emergency error: {response.status_code}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                }
        
        except Exception as e:
            logger.exception(f"Error sending emergency: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }


# Singleton instance
vnnox_service = VnnoxService()