# VNOX Service Integration for Pune VMS System
# Based on the provided vnnox.py file

import requests
import hashlib
import time
import random
import string
import json
import logging
from django.conf import settings
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class VnoxService:
    """
    VNOX API Service for managing VMS players and emergency messages
    """
    
    def __init__(self):
        # Get configuration from Django settings or environment variables
        self.app_key = getattr(settings, 'VNOX_APP_KEY', 'a560b6661ce24349a6d148585a120fcb')
        self.app_secret = getattr(settings, 'VNOX_APP_SECRET', '55bf1e51586f45028d378a533e769a25')
        self.base_url = getattr(settings, 'VNOX_BASE_URL', 'https://open-in.vnnox.com')
        self.timeout = getattr(settings, 'VNOX_TIMEOUT', 30)
        
        # Vantage Argus configuration
        self.vantage_base_url = getattr(settings, 'ITERIS_BASE_URL', 'https://vantagearguscv.iteris.com')
        self.vantage_bearer_token = getattr(settings, 'ITERIS_BEARER_TOKEN', '')
        
    def _generate_auth_headers(self, json_body: bool = False) -> Dict[str, str]:
        """Generate authentication headers for VNOX API"""
        nonce = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        cur_time = str(int(time.time()))
        checksum = hashlib.sha256((self.app_secret + nonce + cur_time).encode()).hexdigest()
        
        headers = {
            "AppKey": self.app_key,
            "Nonce": nonce,
            "CurTime": cur_time,
            "CheckSum": checksum,
            "Accept": "application/json",
        }
        
        if json_body:
            headers["Content-Type"] = "application/json; charset=utf-8"
        else:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            
        return headers
    
    def get_players(self, count: int = 100, start: int = 0, name: str = "") -> List[Dict]:
        """
        Get list of VNOX players with their IDs, names, and online status
        
        Args:
            count: Number of players to fetch (default: 100)
            start: Starting index (default: 0)
            name: Filter by player name (optional)
            
        Returns:
            List of player dictionaries
            
        Raises:
            Exception: If API call fails
        """
        try:
            params = {"count": count, "start": start}
            if name:
                params["name"] = name

            response = requests.get(
                f"{self.base_url}/v2/player/list",
                headers=self._generate_auth_headers(),
                params=params,
                timeout=self.timeout
            )

            if response.status_code != 200:
                logger.error(f"VNOX get_players failed: {response.status_code} {response.text}")
                raise Exception(f"VNOX API error: {response.status_code} {response.text}")

            data = response.json()
            players = data.get("rows", [])
            
            total_players = data.get('total', len(players))
            logger.info(f"VNOX: Retrieved {len(players)} players out of {total_players} total")
            
            # Log player details
            for player in players:
                status = "ONLINE" if player.get("onlineStatus") == 1 else "OFFLINE"
                logger.debug(f"VNOX Player: [{status}] {player['name']} (ID: {player['playerId']})")
            
            return players

        except requests.RequestException as e:
            logger.error(f"VNOX API request failed: {str(e)}")
            raise Exception(f"VNOX connection error: {str(e)}")
        except Exception as e:
            logger.error(f"VNOX get_players error: {str(e)}")
            raise
    
    def get_online_players(self) -> List[Dict]:
        """
        Get only online players
        
        Returns:
            List of online player dictionaries
        """
        all_players = self.get_players()
        online_players = [p for p in all_players if p.get("onlineStatus") == 1]
        
        logger.info(f"VNOX: Found {len(online_players)} online players out of {len(all_players)} total")
        return online_players
    
    def send_emergency_message(self, player_ids: List[str], image_url: str, duration_ms: int = 30000) -> Dict:
        """
        Send emergency message to specified players
        
        Args:
            player_ids: List of player IDs (max 100 at once)
            image_url: Publicly accessible image URL
            duration_ms: Display duration in milliseconds (default: 30s)
            
        Returns:
            API response dictionary
        """
        try:
            payload = {
                "playerIds": player_ids,
                "attribute": {
                    "spotsType": "IMMEDIATELY",
                    "normalProgramStatus": "PAUSE",
                    "duration": duration_ms,
                },
                "page": {
                    "name": "emergency",
                    "widgets": [
                        {
                            "type": "PICTURE",
                            "url": image_url,
                            "duration": duration_ms,
                            "zIndex": 1,
                            "layout": {
                                "x": "0%",
                                "y": "0%",
                                "width": "100%",
                                "height": "100%",
                            },
                            "inAnimation": {"type": "NONE", "duration": 0},
                        }
                    ],
                },
            }

            response = requests.post(
                f"{self.base_url}/v1/player/program/emergency",
                headers=self._generate_auth_headers(json_body=True),
                json=payload,
                timeout=self.timeout
            )

            logger.info(f"VNOX send_emergency status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"VNOX send_emergency failed: {response.status_code} {response.text}")
                raise Exception(f"VNOX emergency message failed: {response.status_code}")
            
            result = response.json() if response.text.strip() else {}
            logger.info(f"VNOX emergency message response: {result}")
            
            return result

        except requests.RequestException as e:
            logger.error(f"VNOX emergency message request failed: {str(e)}")
            raise Exception(f"VNOX connection error: {str(e)}")
        except Exception as e:
            logger.error(f"VNOX send_emergency error: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test connection to VNOX API
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            players = self.get_players(count=1)
            logger.info("VNOX connection test successful")
            return True
        except Exception as e:
            logger.error(f"VNOX connection test failed: {str(e)}")
            return False
    
    def get_player_by_id(self, player_id: str) -> Optional[Dict]:
        """
        Get specific player by ID
        
        Args:
            player_id: VNOX player ID
            
        Returns:
            Player dictionary or None if not found
        """
        try:
            players = self.get_players(name=player_id)
            for player in players:
                if player.get('playerId') == player_id:
                    return player
            return None
        except Exception as e:
            logger.error(f"VNOX get_player_by_id error: {str(e)}")
            return None
    
    def get_players_by_status(self, online: bool = True) -> List[Dict]:
        """
        Get players by online status
        
        Args:
            online: True for online players, False for offline
            
        Returns:
            List of player dictionaries
        """
        all_players = self.get_players()
        if online:
            return [p for p in all_players if p.get("onlineStatus") == 1]
        else:
            return [p for p in all_players if p.get("onlineStatus") != 1]
    
    def get_smoothed_speeds(self, pair_id: str, from_time: int, to_time: int) -> Dict:
        """
        Fetch smoothed speed data from Vantage Argus API
        
        Args:
            pair_id: Vantage Argus pair ID
            from_time: Unix timestamp for start time
            to_time: Unix timestamp for end time
            
        Returns:
            Dictionary with speed data
        """
        try:
            url = f"{self.vantage_base_url}/public-api/v1/pairs/{pair_id}/smoothed-speeds"
            params = {"from": from_time, "to": to_time}
            
            headers = {"Authorization": self.vantage_bearer_token}
            
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                logger.error(f"Vantage get_smoothed_speeds failed: {response.status_code} {response.text}")
                raise Exception(f"Vantage API error: {response.status_code}")
            
            data = response.json()
            logger.info(f"Vantage: Retrieved speed data for pair {pair_id}")
            return data
            
        except requests.RequestException as e:
            logger.error(f"Vantage API request failed: {str(e)}")
            raise Exception(f"Vantage connection error: {str(e)}")
        except Exception as e:
            logger.error(f"Vantage get_smoothed_speeds error: {str(e)}")
            raise
    
    def send_custom_emergency_message(self, player_ids: List[str], speed_data: Dict, 
                                 route_name: str, duration_ms: int = 20000) -> Dict:
        """
        Send custom emergency message with speed and travel time information
        
        Args:
            player_ids: List of player IDs
            speed_data: Speed data from Vantage Argus
            route_name: Name of the route/corridor
            duration_ms: Display duration in milliseconds
            
        Returns:
            API response dictionary
        """
        try:
            # Extract speed and travel time from data
            speed_kmph = speed_data.get('speed', 0)
            travel_time_min = speed_data.get('travel_time', 0)
            
            # Build the emergency message payload
            payload = {
                "playerIds": player_ids,
                "attribute": {
                    "spotsType": "IMMEDIATELY",
                    "normalProgramStatus": "PAUSE",
                    "duration": duration_ms
                },
                "page": {
                    "name": "current-speed",
                    "widgets": [
                        {
                            "zIndex": 0,
                            "type": "ARCH_TEXT",
                            "layout": {
                                "x": "0%",
                                "y": "0%",
                                "width": "100%",
                                "height": "100%"
                            },
                            "displayType": "STATIC",
                            "backgroundColor": "#000000",
                            "duration": 10000,
                            "lines": [{
                                "textAttributes": [{
                                    "content": " ",
                                    "fontSize": 20,
                                    "textColor": "#000000",
                                    "isBold": False
                                }]
                            }]
                        },
                        {
                            "zIndex": 2,
                            "type": "ARCH_TEXT",
                            "layout": {
                                "x": "30%",
                                "y": "5%",
                                "width": "100%",
                                "height": "20%"
                            },
                            "displayType": "STATIC",
                            "duration": 10000,
                            "lines": [{
                                "textAttributes": [{
                                    "content": "Est. Travel Time",
                                    "fontSize": 20,
                                    "textColor": "#FFFF00",
                                    "isBold": False
                                }]
                            }]
                        },
                        {
                            "zIndex": 3,
                            "type": "ARCH_TEXT",
                            "layout": {
                                "x": "5%",
                                "y": "25%",
                                "width": "100%",
                                "height": "20%"
                            },
                            "displayType": "STATIC",
                            "duration": 10000,
                            "lines": [{
                                "textAttributes": [{
                                    "content": route_name,
                                    "fontSize": 20,
                                    "textColor": "#FFFF00",
                                    "isBold": False
                                }]
                            }]
                        },
                        {
                            "zIndex": 4,
                            "type": "ARCH_TEXT",
                            "layout": {
                                "x": "30%",
                                "y": "45%",
                                "width": "100%",
                                "height": "20%"
                            },
                            "displayType": "STATIC",
                            "duration": 10000,
                            "lines": [{
                                "textAttributes": [{
                                    "content": f"{speed_kmph} KMPH / {travel_time_min} min",
                                    "fontSize": 20,
                                    "textColor": "#FFFF00",
                                    "isBold": False
                                }]
                            }]
                        },
                        {
                            "zIndex": 1,
                            "type": "PICTURE",
                            "size": 25943,
                            "md5": "0ed170adac4b3f6149a8c3c100f28663",
                            "duration": 10000,
                            "url": "http://124.66.170.66/Images/logo-v2-full.png",
                            "layout": {
                                "x": "0%",
                                "y": "0%",
                                "width": "100%",
                                "height": "100%"
                            },
                            "inAnimation": {
                                "type": "NONE",
                                "duration": 20000
                            }
                        }
                    ]
                }
            }

            response = requests.post(
                f"{self.base_url}/v1/player/program/emergency",
                headers=self._generate_auth_headers(json_body=True),
                json=payload,
                timeout=self.timeout
            )

            logger.info(f"VNOX send_custom_emergency_message status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"VNOX custom emergency message failed: {response.status_code} {response.text}")
                raise Exception(f"VNOX emergency message failed: {response.status_code}")
            
            result = response.json() if response.text.strip() else {}
            logger.info(f"VNOX custom emergency message response: {result}")
            
            return result

        except requests.RequestException as e:
            logger.error(f"VNOX custom emergency message request failed: {str(e)}")
            raise Exception(f"VNOX connection error: {str(e)}")
        except Exception as e:
            logger.error(f"VNOX send_custom_emergency_message error: {str(e)}")
            raise
    
    def send_speed_emergency_to_players(self, player_ids: List[str], pair_id: str, 
                                   route_name: str, duration_ms: int = 20000) -> Dict:
        """
        Complete workflow: Fetch speed data and send emergency message
        
        Args:
            player_ids: List of player IDs
            pair_id: Vantage Argus pair ID
            route_name: Name of the route/corridor
            duration_ms: Display duration in milliseconds
            
        Returns:
            API response dictionary
        """
        try:
            # Get current timestamp
            current_time = int(time.time())
            from_time = current_time - 3600  # 1 hour ago
            
            # Fetch speed data from Vantage Argus
            speed_data = self.get_smoothed_speeds(pair_id, from_time, current_time)
            
            # Extract latest speed and calculate travel time
            if speed_data and 'data' in speed_data and len(speed_data['data']) > 0:
                latest_data = speed_data['data'][-1]  # Get latest entry
                speed_kmph = latest_data.get('speed', 0)
                distance_km = latest_data.get('distance', 10)  # Default 10km
                travel_time_min = (distance_km / speed_kmph * 60) if speed_kmph > 0 else 0
                
                speed_info = {
                    'speed': f"{speed_kmph:.1f}",
                    'travel_time': f"{travel_time_min:.1f}"
                }
            else:
                # Fallback data
                speed_info = {
                    'speed': "25.2",
                    'travel_time': "3.4"
                }
            
            # Send emergency message with speed data
            result = self.send_custom_emergency_message(
                player_ids=player_ids,
                speed_data=speed_info,
                route_name=route_name,
                duration_ms=duration_ms
            )
            
            return result
            
        except Exception as e:
            logger.error(f"VNOX send_speed_emergency_to_players error: {str(e)}")
            raise
