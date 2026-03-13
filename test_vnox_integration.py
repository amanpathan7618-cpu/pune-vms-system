#!/usr/bin/env python
"""
Test script for VNOX integration
Run this script to test VNOX API connectivity and player list retrieval
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atms_backend.settings')
django.setup()

from traffic.services.vnox_service import VnoxService

def test_vnox_integration():
    """Test VNOX API integration"""
    print("=" * 60)
    print("VNOX Integration Test")
    print("=" * 60)
    
    try:
        # Initialize VNOX service
        vnox_service = VnoxService()
        
        print(f"VNOX Base URL: {vnox_service.base_url}")
        print(f"VNOX App Key: {vnox_service.app_key}")
        print()
        
        # Test connection
        print("1. Testing VNOX connection...")
        is_connected = vnox_service.test_connection()
        if is_connected:
            print("✓ VNOX connection successful")
        else:
            print("✗ VNOX connection failed")
            return False
        
        print()
        
        # Get all players
        print("2. Fetching VNOX players...")
        players = vnox_service.get_players(count=50)
        
        if players:
            print(f"✓ Found {len(players)} players")
            
            # Show first 5 players
            print("\nFirst 5 players:")
            for i, player in enumerate(players[:5]):
                status = "ONLINE" if player.get("onlineStatus") == 1 else "OFFLINE"
                print(f"  {i+1}. [{status}] {player['name']}")
                print(f"      ID: {player['playerId']}")
                print(f"      IP: {player.get('ip', 'N/A')}")
                print(f"      Last Online: {player.get('lastOnlineTime', 'N/A')}")
                print()
            
            # Get online players only
            print("3. Fetching online players only...")
            online_players = vnox_service.get_online_players()
            print(f"✓ Found {len(online_players)} online players")
            
            if online_players:
                print("\nOnline players:")
                for i, player in enumerate(online_players):
                    print(f"  {i+1}. {player['name']} (ID: {player['playerId']})")
            
            print()
            print("=" * 60)
            print("VNOX Integration Test - SUCCESS")
            print("=" * 60)
            return True
        else:
            print("✗ No players found")
            return False
            
    except Exception as e:
        print(f"✗ VNOX integration test failed: {str(e)}")
        return False

def test_api_endpoints():
    """Test VNOX API endpoints"""
    print("\n" + "=" * 60)
    print("Testing VNOX API Endpoints")
    print("=" * 60)
    
    try:
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        
        # Test connection endpoint
        print("1. Testing connection endpoint...")
        response = client.get('/api/traffic/vnox/test-connection/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Connected: {data.get('connected', False)}")
            print(f"   Message: {data.get('message', '')}")
        
        print()
        
        # Test players list endpoint
        print("2. Testing players list endpoint...")
        response = client.get('/api/traffic/vnox/players/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total Players: {data.get('total_players', 0)}")
            print(f"   Online Players: {data.get('online_players', 0)}")
            print(f"   Offline Players: {data.get('offline_players', 0)}")
        
        print()
        
        # Test online players only
        print("3. Testing online players endpoint...")
        response = client.get('/api/traffic/vnox/players/?online_only=true')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Online Players: {data.get('online_players', 0)}")
            print(f"   Online Only: {data.get('online_only', False)}")
        
        print()
        print("=" * 60)
        print("VNOX API Endpoints Test - COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ API endpoints test failed: {str(e)}")

if __name__ == "__main__":
    print("Starting VNOX Integration Tests...")
    
    # Test direct service integration
    success = test_vnox_integration()
    
    if success:
        # Test API endpoints
        test_api_endpoints()
    
    print("\nTest completed.")
