# EDITED: traffic/views.py - ADDITIONS
# Add these to your existing views.py
# These views work with your custom EmergencyMessage and QuickMessage models

import os
import requests
import time
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from traffic.models import (
    VMSBoard,
    Intersection,
    Signal,
    Route,
    TrafficData,
    TravelTime,
)
from traffic.serializers import (
    VMSBoardSerializer,
    IntersectionSerializer,
    SignalSerializer,
    RouteSerializer,
    TrafficDataSerializer,
    TravelTimeSerializer,
)
from traffic.services.vnox_service import VnoxService

class VMSBoardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VMSBoard.objects.filter(is_active=True)
    serializer_class = VMSBoardSerializer
    permission_classes = [AllowAny]


class IntersectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Intersection.objects.filter(is_active=True)
    serializer_class = IntersectionSerializer
    permission_classes = [AllowAny]


class SignalViewSet(viewsets.ModelViewSet):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer
    permission_classes = [IsAuthenticated]


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.filter(is_active=True)
    serializer_class = RouteSerializer
    permission_classes = [AllowAny]


class TrafficDataViewSet(viewsets.ModelViewSet):
    queryset = TrafficData.objects.all()
    serializer_class = TrafficDataSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'head', 'options']


class TravelTimeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TravelTime.objects.all()
    serializer_class = TravelTimeSerializer
    permission_classes = [AllowAny]


class PlayerPairMappingView(APIView):
    """
    GET: Fetch players from VINOX and pairs from Vantage, then return a mapping list.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Vantage config
            vantage_base_url = os.getenv('VANTAGE_BASE_URL', 'https://vantagearguscv.iteris.com')
            vantage_pairs_url = f"{vantage_base_url}/public-api/v1/pairs"
            vantage_bearer_token = os.getenv('VANTAGE_BEARER_TOKEN') or os.getenv('ITERIS_BEARER_TOKEN')
            vantage_username = os.getenv('VANTAGE_USERNAME') or os.getenv('ITERIS_USERNAME')
            vantage_password = os.getenv('VANTAGE_PASSWORD') or os.getenv('ITERIS_PASSWORD')

            # VINOX config
            vinox_base_url = os.getenv('VINOX_BASE_URL', 'http://124.66.170.66')
            vinox_auth_url = f"{vinox_base_url}/adorvmsapi/authenticate"
            vinox_players_url = f"{vinox_base_url}/adorvmsapi/v1/players"
            vinox_username = os.getenv('VINOX_USERNAME') or os.getenv('VNNOX_USERNAME')
            vinox_password = os.getenv('VINOX_PASSWORD') or os.getenv('VNNOX_PASSWORD')

            if not (vantage_bearer_token or (vantage_username and vantage_password)):
                return Response({'error': 'Missing Vantage credentials'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if not (vinox_username and vinox_password):
                return Response({'error': 'Missing VINOX credentials'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Fetch pairs from Vantage
            headers = None
            auth = None
            if vantage_bearer_token:
                token_value = vantage_bearer_token.strip()
                if token_value.lower().startswith('bearer '):
                    token_value = token_value.split(' ', 1)[1].strip()
                headers = {'Authorization': f'Bearer {token_value}'}
            else:
                auth = (vantage_username, vantage_password)

            pairs_resp = requests.get(vantage_pairs_url, headers=headers, auth=auth, timeout=15)
            if pairs_resp.status_code != 200:
                return Response({'error': f'Vantage pairs fetch failed: {pairs_resp.status_code}'},
                                status=status.HTTP_502_BAD_GATEWAY)
            pairs_payload = pairs_resp.json()
            if isinstance(pairs_payload, dict):
                pairs = pairs_payload.get('data') or pairs_payload.get('pairs') or []
            elif isinstance(pairs_payload, list):
                pairs = pairs_payload
            else:
                pairs = []

            # Authenticate to VINOX
            vinox_auth_resp = requests.post(
                vinox_auth_url,
                json={'username': vinox_username, 'password': vinox_password},
                timeout=10,
            )
            if vinox_auth_resp.status_code != 200:
                return Response({'error': f'VINOX auth failed: {vinox_auth_resp.status_code}'},
                                status=status.HTTP_502_BAD_GATEWAY)
            vinox_token = vinox_auth_resp.json().get('token')
            if not vinox_token:
                return Response({'error': 'VINOX token missing in response'}, status=status.HTTP_502_BAD_GATEWAY)

            # Fetch players from VINOX
            players_resp = requests.get(
                vinox_players_url,
                headers={'Authorization': f'Bearer {vinox_token}'},
                timeout=15,
            )
            if players_resp.status_code != 200:
                return Response({'error': f'VINOX players fetch failed: {players_resp.status_code}'},
                                status=status.HTTP_502_BAD_GATEWAY)
            players_payload = players_resp.json()
            if isinstance(players_payload, dict):
                players = players_payload.get('data') or players_payload.get('players') or []
            elif isinstance(players_payload, list):
                players = players_payload
            else:
                players = []

            # Build mapping
            mapping = []
            if pairs and players:
                for i, player in enumerate(players):
                    player_id = player.get('playerId') or player.get('id') or player.get('player_id')
                    player_name = player.get('name') or player.get('playerName') or player.get('player_name')
                    if not player_id or not player_name:
                        continue
                    pair = pairs[i % len(pairs)]
                    pair_id = pair.get('id') or pair.get('pair_id')
                    corridor_name = pair.get('name') or pair.get('title')
                    mapping.append({
                        'sr_no': i + 1,
                        'vms_player_name': player_name,
                        'player_id': player_id,
                        'pair_id': pair_id,
                        'corridor_name': corridor_name,
                    })

            return Response({
                'pairs_count': len(pairs),
                'players_count': len(players),
                'mappings': mapping,
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# VNOX API Views
class VnoxPlayerListView(APIView):
    """
    GET: Fetch players from VNOX system
    """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            vnox_service = VnoxService()
            
            # Get query parameters
            count = int(request.GET.get('count', 100))
            start = int(request.GET.get('start', 0))
            name = request.GET.get('name', '')
            online_only = request.GET.get('online_only', 'false').lower() == 'true'
            
            if online_only:
                players = vnox_service.get_online_players()
            else:
                players = vnox_service.get_players(count=count, start=start, name=name)
            
            # Separate online and offline players
            online_players = [p for p in players if p.get("onlineStatus") == 1]
            offline_players = [p for p in players if p.get("onlineStatus") != 1]
            
            return Response({
                'total_players': len(players),
                'online_players': len(online_players),
                'offline_players': len(offline_players),
                'players': players,
                'online_only': online_only
            })
            
        except Exception as e:
            return Response({
                'error': f'Failed to fetch VNOX players: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VnoxPlayerDetailView(APIView):
    """
    GET: Get specific VNOX player by ID
    """
    permission_classes = [AllowAny]

    def get(self, request, player_id):
        try:
            vnox_service = VnoxService()
            player = vnox_service.get_player_by_id(player_id)
            
            if not player:
                return Response({
                    'error': f'Player with ID {player_id} not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'player': player
            })
            
        except Exception as e:
            return Response({
                'error': f'Failed to fetch VNOX player: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VnoxEmergencyMessageView(APIView):
    """
    POST: Send emergency message to VNOX players
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            vnox_service = VnoxService()
            
            # Get request data
            player_ids = request.data.get('player_ids', [])
            image_url = request.data.get('image_url', '')
            duration_ms = request.data.get('duration_ms', 30000)
            
            if not player_ids:
                return Response({
                    'error': 'player_ids is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not image_url:
                return Response({
                    'error': 'image_url is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Send emergency message
            result = vnox_service.send_emergency_message(
                player_ids=player_ids,
                image_url=image_url,
                duration_ms=duration_ms
            )
            
            return Response({
                'success': True,
                'result': result,
                'message': f'Emergency message sent to {len(player_ids)} players'
            })
            
        except Exception as e:
            return Response({
                'error': f'Failed to send emergency message: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VnoxConnectionTestView(APIView):
    """
    GET: Test connection to VNOX API
    """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            vnox_service = VnoxService()
            is_connected = vnox_service.test_connection()
            
            return Response({
                'connected': is_connected,
                'message': 'VNOX connection successful' if is_connected else 'VNOX connection failed'
            })
            
        except Exception as e:
            return Response({
                'connected': False,
                'error': f'VNOX connection test failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VantageSpeedView(APIView):
    """
    GET: Fetch speed data from Vantage Argus API
    """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            vnox_service = VnoxService()
            
            # Get query parameters
            pair_id = request.GET.get('pair_id', '')
            from_time = request.GET.get('from_time', '')
            to_time = request.GET.get('to_time', '')
            
            if not pair_id:
                return Response({
                    'error': 'pair_id is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not from_time:
                # Default to 1 hour ago
                from_time = str(int(time.time()) - 3600)
            
            if not to_time:
                # Default to current time
                to_time = str(int(time.time()))
            
            # Convert to integers
            from_time_int = int(from_time)
            to_time_int = int(to_time)
            
            # Fetch speed data
            speed_data = vnox_service.get_smoothed_speeds(
                pair_id=pair_id,
                from_time=from_time_int,
                to_time=to_time_int
            )
            
            return Response({
                'success': True,
                'pair_id': pair_id,
                'from_time': from_time_int,
                'to_time': to_time_int,
                'speed_data': speed_data
            })
            
        except Exception as e:
            return Response({
                'error': f'Failed to fetch speed data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VnoxSpeedEmergencyView(APIView):
    """
    POST: Send speed-based emergency message to VNOX players
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            vnox_service = VnoxService()
            
            # Get request data
            player_ids = request.data.get('player_ids', [])
            pair_id = request.data.get('pair_id', '')
            route_name = request.data.get('route_name', 'Dandekar Bdg chwk to Navshya Maruthi')
            duration_ms = request.data.get('duration_ms', 20000)
            
            if not player_ids:
                return Response({
                    'error': 'player_ids is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not pair_id:
                return Response({
                    'error': 'pair_id is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Send speed emergency message
            result = vnox_service.send_speed_emergency_to_players(
                player_ids=player_ids,
                pair_id=pair_id,
                route_name=route_name,
                duration_ms=duration_ms
            )
            
            return Response({
                'success': True,
                'result': result,
                'message': f'Speed emergency message sent to {len(player_ids)} players for route: {route_name}'
            })
            
        except Exception as e:
            return Response({
                'error': f'Failed to send speed emergency message: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VnoxCustomEmergencyView(APIView):
    """
    POST: Send custom emergency message with provided speed data
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            vnox_service = VnoxService()
            
            # Get request data
            player_ids = request.data.get('player_ids', [])
            speed_data = request.data.get('speed_data', {})
            route_name = request.data.get('route_name', 'Unknown Route')
            duration_ms = request.data.get('duration_ms', 20000)
            
            if not player_ids:
                return Response({
                    'error': 'player_ids is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not speed_data:
                return Response({
                    'error': 'speed_data is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Send custom emergency message
            result = vnox_service.send_custom_emergency_message(
                player_ids=player_ids,
                speed_data=speed_data,
                route_name=route_name,
                duration_ms=duration_ms
            )
            
            return Response({
                'success': True,
                'result': result,
                'message': f'Custom emergency message sent to {len(player_ids)} players'
            })
            
        except Exception as e:
            return Response({
                'error': f'Failed to send custom emergency message: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
