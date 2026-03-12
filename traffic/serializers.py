from rest_framework import serializers
from traffic.models import VMSBoard, Intersection, Signal, Route, TrafficData, TravelTime

class VMSBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VMSBoard
        fields = [
            'board_id',
            'vms_player_name',
            'corridor_name',
            'pair_id',
            'location',
            'latitude',
            'longitude',
            'display_time',
            'resolution',
            'is_active',
            'last_update'
        ]

class IntersectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intersection
        fields = '__all__'

class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class TrafficDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficData
        fields = '__all__'

class TravelTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelTime
        fields = '__all__'