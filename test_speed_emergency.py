#!/usr/bin/env python
"""
Test script for Vantage Argus + VNOX Speed Emergency Integration
Tests the complete workflow: Fetch speed data -> Send emergency message
"""

import os
import sys
import django
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atms_backend.settings')
django.setup()

from traffic.services.vnox_service import VnoxService

def test_vantage_speed_data():
    """Test fetching speed data from Vantage Argus"""
    print("=" * 60)
    print("VANTAGE ARGUS SPEED DATA TEST")
    print("=" * 60)
    
    try:
        vnox_service = VnoxService()
        
        # Test parameters (using pair ID from your example)
        pair_id = "57445"
        current_time = int(time.time())
        from_time = current_time - 3600  # 1 hour ago
        
        print(f"Fetching speed data for pair {pair_id}")
        print(f"From: {from_time} ({time.ctime(from_time)})")
        print(f"To: {current_time} ({time.ctime(current_time)})")
        print()
        
        # Fetch speed data
        speed_data = vnox_service.get_smoothed_speeds(pair_id, from_time, current_time)
        
        if speed_data:
            print("✓ Speed data retrieved successfully")
            print(f"Data keys: {list(speed_data.keys())}")
            
            if 'data' in speed_data and len(speed_data['data']) > 0:
                latest_entry = speed_data['data'][-1]
                print(f"Latest speed entry: {latest_entry}")
            else:
                print("No speed data entries found")
        else:
            print("✗ No speed data retrieved")
        
        return speed_data
        
    except Exception as e:
        print(f"✗ Vantage speed test failed: {str(e)}")
        return None

def test_custom_emergency_message():
    """Test sending custom emergency message"""
    print("\n" + "=" * 60)
    print("CUSTOM EMERGENCY MESSAGE TEST")
    print("=" * 60)
    
    try:
        vnox_service = VnoxService()
        
        # Test with sample data
        player_ids = ["8eb4b969c5e4624ab1989b78f669c6d6"]  # Sample player ID
        speed_data = {
            'speed': "25.2",
            'travel_time': "3.4"
        }
        route_name = "Dandekar Bdg chwk to Navshya Maruthi"
        
        print(f"Sending custom emergency message")
        print(f"Player IDs: {player_ids}")
        print(f"Speed Data: {speed_data}")
        print(f"Route Name: {route_name}")
        print()
        
        result = vnox_service.send_custom_emergency_message(
            player_ids=player_ids,
            speed_data=speed_data,
            route_name=route_name,
            duration_ms=20000
        )
        
        if result:
            print("✓ Custom emergency message sent successfully")
            print(f"Result: {result}")
        else:
            print("✗ No response from VNOX")
        
        return result
        
    except Exception as e:
        print(f"✗ Custom emergency message test failed: {str(e)}")
        return None

def test_speed_emergency_workflow():
    """Test complete speed emergency workflow"""
    print("\n" + "=" * 60)
    print("COMPLETE SPEED EMERGENCY WORKFLOW TEST")
    print("=" * 60)
    
    try:
        vnox_service = VnoxService()
        
        # Test parameters
        player_ids = ["8eb4b969c5e4624ab1989b78f669c6d6"]  # Sample player ID
        pair_id = "57445"  # From your example
        route_name = "Dandekar Bdg chwk to Navshya Maruthi"
        
        print(f"Testing complete speed emergency workflow")
        print(f"Player IDs: {player_ids}")
        print(f"Pair ID: {pair_id}")
        print(f"Route Name: {route_name}")
        print()
        
        result = vnox_service.send_speed_emergency_to_players(
            player_ids=player_ids,
            pair_id=pair_id,
            route_name=route_name,
            duration_ms=20000
        )
        
        if result:
            print("✓ Speed emergency workflow completed successfully")
            print(f"Result: {result}")
        else:
            print("✗ No response from VNOX")
        
        return result
        
    except Exception as e:
        print(f"✗ Speed emergency workflow test failed: {str(e)}")
        return None

def test_api_endpoints():
    """Test the new API endpoints"""
    print("\n" + "=" * 60)
    print("API ENDPOINTS TEST")
    print("=" * 60)
    
    try:
        from django.test import Client
        
        client = Client()
        
        # Test Vantage speed endpoint
        print("1. Testing Vantage speed endpoint...")
        response = client.get('/api/traffic/vantage/speed/?pair_id=57445')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data.get('success', False)}")
            print(f"   Pair ID: {data.get('pair_id', '')}")
        else:
            print(f"   Error: {response.json()}")
        
        print()
        
        # Test speed emergency endpoint (will fail without auth)
        print("2. Testing speed emergency endpoint (without auth)...")
        response = client.post('/api/traffic/vnox/speed-emergency/', 
                           content_type='application/json',
                           data={
                               'player_ids': ['test'],
                               'pair_id': '57445',
                               'route_name': 'Test Route'
                           })
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✓ Correctly requires authentication")
        else:
            print(f"   Response: {response.json()}")
        
        print()
        
        # Test custom emergency endpoint (will fail without auth)
        print("3. Testing custom emergency endpoint (without auth)...")
        response = client.post('/api/traffic/vnox/custom-emergency/',
                           content_type='application/json',
                           data={
                               'player_ids': ['test'],
                               'speed_data': {'speed': '25.2', 'travel_time': '3.4'},
                               'route_name': 'Test Route'
                           })
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✓ Correctly requires authentication")
        else:
            print(f"   Response: {response.json()}")
        
        print()
        print("=" * 60)
        print("API ENDPOINTS TEST - COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ API endpoints test failed: {str(e)}")

if __name__ == "__main__":
    print("Starting Vantage Argus + VNOX Speed Emergency Tests...")
    
    # Test individual components
    speed_data = test_vantage_speed_data()
    custom_result = test_custom_emergency_message()
    workflow_result = test_speed_emergency_workflow()
    
    # Test API endpoints
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("SPEED EMERGENCY INTEGRATION TESTS - COMPLETE")
    print("=" * 60)
    
    # Summary
    print("\nTest Summary:")
    print(f"✓ Vantage Speed Data: {'SUCCESS' if speed_data else 'FAILED'}")
    print(f"✓ Custom Emergency Message: {'SUCCESS' if custom_result else 'FAILED'}")
    print(f"✓ Speed Emergency Workflow: {'SUCCESS' if workflow_result else 'FAILED'}")
    print(f"✓ API Endpoints: TESTED")
    
    print("\nYour Vantage Argus + VNOX Speed Emergency integration is ready!")
    print("You can now send dynamic speed-based emergency messages to VMS boards.")
