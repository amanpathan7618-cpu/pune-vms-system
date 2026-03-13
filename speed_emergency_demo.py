#!/usr/bin/env python
"""
Demo script for Speed Emergency API functionality
Shows how the APIs work with example requests/responses
"""

import os
import sys
import json

def show_api_documentation():
    """Show API documentation for speed emergency endpoints"""
    print("=" * 80)
    print("VANTAGE ARGUS + VNOX SPEED EMERGENCY API DOCUMENTATION")
    print("=" * 80)
    
    print("\n🚀 NEW API ENDPOINTS CREATED:")
    print("=" * 50)
    
    print("\n1. GET Vantage Speed Data")
    print("   URL: /api/traffic/vantage/speed/")
    print("   Method: GET")
    print("   Query Parameters:")
    print("     - pair_id (required): Vantage Argus pair ID")
    print("     - from_time (optional): Unix timestamp start")
    print("     - to_time (optional): Unix timestamp end")
    print("   Example:")
    print("   GET /api/traffic/vantage/speed/?pair_id=57445")
    print("   Response:")
    print(json.dumps({
        "success": True,
        "pair_id": "57445",
        "from_time": 1744629043,
        "to_time": 1744629643,
        "speed_data": {
            "data": [
                {"speed": 25.2, "timestamp": 1744629100},
                {"speed": 26.1, "timestamp": 1744629160}
            ]
        }
    }, indent=2))
    
    print("\n2. POST Speed Emergency Message")
    print("   URL: /api/traffic/vnox/speed-emergency/")
    print("   Method: POST")
    print("   Headers: Authorization: Token {auth_token}")
    print("   Body:")
    print(json.dumps({
        "player_ids": ["8eb4b969c5e4624ab1989b78f669c6d6"],
        "pair_id": "57445",
        "route_name": "Dandekar Bdg chwk to Navshya Maruthi",
        "duration_ms": 20000
    }, indent=2))
    print("   Response:")
    print(json.dumps({
        "success": True,
        "result": {"success_count": 1, "fail_count": 0},
        "message": "Speed emergency message sent to 1 players for route: Dandekar Bdg chwk to Navshya Maruthi"
    }, indent=2))
    
    print("\n3. POST Custom Emergency Message")
    print("   URL: /api/traffic/vnox/custom-emergency/")
    print("   Method: POST")
    print("   Headers: Authorization: Token {auth_token}")
    print("   Body:")
    print(json.dumps({
        "player_ids": ["8eb4b969c5e4624ab1989b78f669c6d6"],
        "speed_data": {"speed": "25.2", "travel_time": "3.4"},
        "route_name": "Dandekar Bdg chwk to Navshya Maruthi",
        "duration_ms": 20000
    }, indent=2))
    print("   Response:")
    print(json.dumps({
        "success": True,
        "result": {"success_count": 1, "fail_count": 0},
        "message": "Custom emergency message sent to 1 players"
    }, indent=2))

def show_emergency_message_structure():
    """Show the emergency message structure sent to VNOX"""
    print("\n" + "=" * 80)
    print("VNOX EMERGENCY MESSAGE STRUCTURE")
    print("=" * 80)
    
    emergency_payload = {
        "playerIds": ["8eb4b969c5e4624ab1989b78f669c6d6"],
        "attribute": {
            "spotsType": "IMMEDIATELY",
            "normalProgramStatus": "PAUSE",
            "duration": 20000
        },
        "page": {
            "name": "current-speed",
            "widgets": [
                {
                    "zIndex": 0,
                    "type": "ARCH_TEXT",
                    "layout": {
                        "x": "0%", "y": "0%", "width": "100%", "height": "100%"
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
                        "x": "30%", "y": "5%", "width": "100%", "height": "20%"
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
                        "x": "5%", "y": "25%", "width": "100%", "height": "20%"
                    },
                    "displayType": "STATIC",
                    "duration": 10000,
                    "lines": [{
                        "textAttributes": [{
                            "content": "Dandekar Bdg chwk to Navshya Maruthi",
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
                        "x": "30%", "y": "45%", "width": "100%", "height": "20%"
                    },
                    "displayType": "STATIC",
                    "duration": 10000,
                    "lines": [{
                        "textAttributes": [{
                            "content": "25.2 KMPH / 3.4 min",
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
                        "x": "0%", "y": "0%", "width": "100%", "height": "100%"
                    },
                    "inAnimation": {
                        "type": "NONE",
                        "duration": 20000
                    }
                }
            ]
        }
    }
    
    print("\nEmergency Message Payload sent to VNOX:")
    print(json.dumps(emergency_payload, indent=2))

def show_workflow_diagram():
    """Show the complete workflow"""
    print("\n" + "=" * 80)
    print("COMPLETE WORKFLOW DIAGRAM")
    print("=" * 80)
    
    workflow = """
    ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
    │   Client App    │    │  Django Backend  │    │  External APIs  │
    │                 │    │                  │    │                 │
    │  Dashboard/Mobile│───▶│  VNOX Service   │───▶│ Vantage Argus   │
    │                 │    │                  │    │                 │
    │                 │    │                  │    │                 │
    └─────────────────┘    └──────────────────┘    └─────────────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │  VNOX API       │
                           │                  │
                           │  Emergency       │
                           │  Message         │
                           │  Broadcast       │
                           └──────────────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │  VMS Boards      │
                           │                  │
                           │  Display Speed   │
                           │  & Travel Time   │
                           └──────────────────┘

    Steps:
    1. Client requests speed emergency message
    2. Django fetches speed data from Vantage Argus API
    3. Django formats emergency message with speed data
    4. Django sends emergency message to VNOX API
    5. VNOX broadcasts to VMS boards
    6. VMS boards display speed and travel time
    """
    
    print(workflow)

def show_usage_examples():
    """Show practical usage examples"""
    print("\n" + "=" * 80)
    print("USAGE EXAMPLES")
    print("=" * 80)
    
    print("\n📱 Mobile App Integration:")
    print("-" * 40)
    print("""
    // Fetch current speed data
    fetch('/api/traffic/vantage/speed/?pair_id=57445')
      .then(response => response.json())
      .then(data => {
        console.log('Current speed:', data.speed_data);
      });
    
    // Send emergency message
    fetch('/api/traffic/vnox/speed-emergency/', {
      method: 'POST',
      headers: {
        'Authorization': 'Token your-auth-token',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        player_ids: ['board-1', 'board-2'],
        pair_id: '57445',
        route_name: 'Main Highway'
      })
    });
    """)
    
    print("\n🖥️ Dashboard Integration:")
    print("-" * 40)
    print("""
    // Real-time speed monitoring
    const speedData = await getSpeedData('57445');
    updateDashboard(speedData);
    
    // Emergency broadcast
    const emergencyData = {
      player_ids: getSelectedBoards(),
      pair_id: getCurrentRoute(),
      route_name: getRouteName()
    };
    await sendSpeedEmergency(emergencyData);
    """)

if __name__ == "__main__":
    show_api_documentation()
    show_emergency_message_structure()
    show_workflow_diagram()
    show_usage_examples()
    
    print("\n" + "=" * 80)
    print("🎉 SPEED EMERGENCY INTEGRATION COMPLETE!")
    print("=" * 80)
    print("\n✅ Features Implemented:")
    print("  • Vantage Argus speed data fetching")
    print("  • Dynamic emergency message generation")
    print("  • VNOX API integration")
    print("  • Real-time speed & travel time display")
    print("  • RESTful API endpoints")
    print("  • Authentication & authorization")
    print("  • Error handling & logging")
    
    print("\n🔧 Ready to Use:")
    print("  • Update ITERIS_BEARER_TOKEN in .env file")
    print("  • Update VNOX credentials if needed")
    print("  • Start Django development server")
    print("  • Test with valid authentication token")
    
    print("\n📞 Next Steps:")
    print("  1. Get valid Vantage Argus bearer token")
    print("  2. Test with real VMS board player IDs")
    print("  3. Integrate with frontend dashboard")
    print("  4. Set up automated speed monitoring")
    
    print("\n🚀 Your Pune VMS System now supports dynamic speed-based emergency messages!")
