# EDITED: traffic/views.py - ADDITIONS
# Add these to your existing views.py
# These views work with your custom EmergencyMessage and QuickMessage models

import os
import requests
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
