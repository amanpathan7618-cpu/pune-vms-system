import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atms_backend.settings')
sys.path.insert(0, r'C:\Users\Dell\Desktop\atms-vms-backend')
django.setup()

from traffic.models import Intersection, Signal, Route, TrafficData, TravelTime

print("=" * 60)
print("🔄 LOADING DATA INTO DATABASE")
print("=" * 60)

print("\n📍 Loading Intersections...")
intersections_data = [
    {'name': 'Pune Central Junction', 'latitude': 18.5230, 'longitude': 73.8567, 'location_description': 'Central Pune Business District', 'zone': 'Zone 1', 'is_active': True, 'signal_count': 4, 'camera_count': 2},
    {'name': 'Shaniwar Peth', 'latitude': 18.5156, 'longitude': 73.8524, 'location_description': 'Shaniwar Peth Historic Area', 'zone': 'Zone 1', 'is_active': True, 'signal_count': 3, 'camera_count': 2},
    {'name': 'Dadar', 'latitude': 18.5347, 'longitude': 73.8612, 'location_description': 'Dadar Commercial Zone', 'zone': 'Zone 2', 'is_active': True, 'signal_count': 4, 'camera_count': 2},
    {'name': 'Katraj Junction', 'latitude': 18.4654, 'longitude': 73.8234, 'location_description': 'Katraj Industrial Area', 'zone': 'Zone 2', 'is_active': True, 'signal_count': 3, 'camera_count': 1},
    {'name': 'Hinjewadi IT Park', 'latitude': 18.5910, 'longitude': 73.7345, 'location_description': 'Hinjewadi IT Park', 'zone': 'Zone 3', 'is_active': True, 'signal_count': 3, 'camera_count': 2},
    {'name': 'Viman Nagar', 'latitude': 18.5678, 'longitude': 73.9012, 'location_description': 'Viman Nagar Residential', 'zone': 'Zone 3', 'is_active': True, 'signal_count': 2, 'camera_count': 1},
    {'name': 'Lohegaon Junction', 'latitude': 18.5789, 'longitude': 73.9210, 'location_description': 'Lohegaon Airport Area', 'zone': 'Zone 4', 'is_active': True, 'signal_count': 2, 'camera_count': 1},
]

Intersection.objects.all().delete()
created_intersections = []
for data in intersections_data:
    intersection = Intersection.objects.create(**data)
    created_intersections.append(intersection)
    print(f"  ✅ Created: {data['name']}")

print(f"\n✅ Loaded {len(created_intersections)} intersections!")

print("\n🚥 Loading Signals...")
signals_data = [
    {'signal_id': 'SIGNAL_PUNE_001', 'intersection': created_intersections[0], 'current_phase': 'green', 'cycle_time': 120, 'green_time': 60, 'red_time': 50, 'yellow_time': 10, 'controlled_by': 'Central Controller', 'is_active': True, 'battery_level': 95},
    {'signal_id': 'SIGNAL_PUNE_002', 'intersection': created_intersections[0], 'current_phase': 'red', 'cycle_time': 120, 'green_time': 60, 'red_time': 50, 'yellow_time': 10, 'controlled_by': 'Central Controller', 'is_active': True, 'battery_level': 92},
    {'signal_id': 'SIGNAL_PUNE_003', 'intersection': created_intersections[0], 'current_phase': 'yellow', 'cycle_time': 120, 'green_time': 60, 'red_time': 50, 'yellow_time': 10, 'controlled_by': 'Central Controller', 'is_active': True, 'battery_level': 88},
    {'signal_id': 'SIGNAL_PUNE_004', 'intersection': created_intersections[0], 'current_phase': 'green', 'cycle_time': 120, 'green_time': 60, 'red_time': 50, 'yellow_time': 10, 'controlled_by': 'Central Controller', 'is_active': True, 'battery_level': 90},
    {'signal_id': 'SIGNAL_SHANIW_001', 'intersection': created_intersections[1], 'current_phase': 'green', 'cycle_time': 120, 'green_time': 60, 'red_time': 50, 'yellow_time': 10, 'controlled_by': 'Zone 1 Controller', 'is_active': True, 'battery_level': 94},
    {'signal_id': 'SIGNAL_SHANIW_002', 'intersection': created_intersections[1], 'current_phase': 'red', 'cycle_time': 120, 'green_time': 60, 'red_time': 50, 'yellow_time': 10, 'controlled_by': 'Zone 1 Controller', 'is_active': True, 'battery_level': 91},
    {'signal_id': 'SIGNAL_SHANIW_003', 'intersection': created_intersections[1], 'current_phase': 'yellow', 'cycle_time': 120, 'green_time': 60, 'red_time': 50, 'yellow_time': 10, 'controlled_by': 'Zone 1 Controller', 'is_active': True, 'battery_level': 87},
    {'signal_id': 'SIGNAL_DADAR_001', 'intersection': created_intersections[2], 'current_phase': 'red', 'cycle_time': 120, 'green_time': 60, 'red_time': 50, 'yellow_time': 10, 'controlled_by': 'Zone 2 Controller', 'is_active': True, 'battery_level': 93},
    {'signal_id': 'SIGNAL_DADAR_002', 'intersection': created_intersections[2], 'current_phase': 'green', 'cycle_time': 120, 'green_time': 60, 'red_time': 50, 'yellow_time': 10, 'controlled_by': 'Zone 2 Controller', 'is_active': True, 'battery_level': 89},
    {'signal_id': 'SIGNAL_DADAR_003', 'intersection': created_intersections[2], 'current_phase': 'yellow', 'cycle_time': 120, 'green_time': 60, 'red_time': 50, 'yellow_time': 10, 'controlled_by': 'Zone 2 Controller', 'is_active': True, 'battery_level': 86},
    {'signal_id': 'SIGNAL_DADAR_004', 'intersection': created_intersections[2], 'current_phase': 'red', 'cycle_time': 120, 'green_time': 60, 'red_time': 50, 'yellow_time': 10, 'controlled_by': 'Zone 2 Controller', 'is_active': True, 'battery_level': 85},
]

Signal.objects.all().delete()
created_signals = []
for data in signals_data:
    signal = Signal.objects.create(**data)
    created_signals.append(signal)
    print(f"  ✅ Created: {data['signal_id']}")

print(f"\n✅ Loaded {len(created_signals)} signals!")

print("\n🛣️ Loading Routes...")
routes_data = [
    {'start_location': 'Pune Central', 'end_location': 'Shaniwar Peth', 'distance_km': 2.96, 'description': 'Central to Shaniwar Peth route', 'is_active': True},
    {'start_location': 'Shaniwar Peth', 'end_location': 'Dadar', 'distance_km': 3.5, 'description': 'Shaniwar Peth to Dadar route', 'is_active': True},
    {'start_location': 'Dadar', 'end_location': 'Katraj', 'distance_km': 8.2, 'description': 'Dadar to Katraj route', 'is_active': True},
    {'start_location': 'Hinjewadi', 'end_location': 'Viman Nagar', 'distance_km': 12.5, 'description': 'Hinjewadi to Viman Nagar route', 'is_active': True},
    {'start_location': 'Pune Central', 'end_location': 'Hinjewadi', 'distance_km': 18.3, 'description': 'Pune Central to Hinjewadi route', 'is_active': True},
    {'start_location': 'Viman Nagar', 'end_location': 'Lohegaon', 'distance_km': 3.2, 'description': 'Viman Nagar to Lohegaon route', 'is_active': True},
    {'start_location': 'Katraj', 'end_location': 'Lohegaon', 'distance_km': 5.8, 'description': 'Katraj to Lohegaon route', 'is_active': True},
    {'start_location': 'Dadar', 'end_location': 'Hinjewadi', 'distance_km': 15.6, 'description': 'Dadar to Hinjewadi route', 'is_active': True},
    {'start_location': 'Pune Central', 'end_location': 'Viman Nagar', 'distance_km': 12.8, 'description': 'Pune Central to Viman Nagar route', 'is_active': True},
]

Route.objects.all().delete()
created_routes = []
for data in routes_data:
    route = Route.objects.create(**data)
    created_routes.append(route)
    print(f"  ✅ Created: {data['start_location']} → {data['end_location']}")

print(f"\n✅ Loaded {len(created_routes)} routes!")

print("\n🚗 Loading Traffic Data...")
TrafficData.objects.all().delete()
traffic_data_list = []
for intersection in created_intersections:
    traffic_records = [
        {'intersection': intersection, 'vehicle_count': 250, 'average_speed': 35.5, 'congestion_level': 'medium', 'source': 'camera'},
        {'intersection': intersection, 'vehicle_count': 180, 'average_speed': 40.2, 'congestion_level': 'low', 'source': 'sensor'},
    ]
    for data in traffic_records:
        traffic = TrafficData.objects.create(**data)
        traffic_data_list.append(traffic)

print(f"\n✅ Loaded {len(traffic_data_list)} traffic data records!")

print("\n⏱️ Loading Travel Times...")
TravelTime.objects.all().delete()
travel_times_list = []
for route in created_routes:
    travel_time_data = {'route': route, 'distance_km': route.distance_km, 'average_speed_kmh': 35.5, 'travel_time_minutes': int(route.distance_km / 35.5 * 60), 'congestion_level': 'medium', 'source': 'camera'}
    travel_time = TravelTime.objects.create(**travel_time_data)
    travel_times_list.append(travel_time)
    print(f"  ✅ Created travel time for: {route.start_location} → {route.end_location}")

print(f"\n✅ Loaded {len(travel_times_list)} travel time records!")

print("\n" + "=" * 60)
print("✅ DATA LOADING COMPLETE!")
print("=" * 60)
print(f"\n📊 Summary:")
print(f"  ✅ Intersections: {Intersection.objects.count()}")
print(f"  ✅ Signals: {Signal.objects.count()}")
print(f"  ✅ Routes: {Route.objects.count()}")
print(f"  ✅ Traffic Data: {TrafficData.objects.count()}")
print(f"  ✅ Travel Times: {TravelTime.objects.count()}")
print("\n🎉 All data loaded successfully!")
print("📝 Refresh your frontend to see the data!\n")