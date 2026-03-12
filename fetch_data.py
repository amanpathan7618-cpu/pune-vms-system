"""
FETCH_DATA.PY - CORRECTED VERSION
Uses HTTP Basic Authentication (no separate auth endpoint)
"""

import os
import requests
import json
from openpyxl import Workbook

print("\n" + "="*80)
print("FETCHING PLAYER IDs AND PAIR IDs FROM APIs")
print("="*80)

# STEP 1: Load & Validate Environment Variables
print("\nSTEP 1: Reading configuration from environment variables...")

try:
    # Vantage credentials
    vantage_username = os.getenv('VANTAGE_USERNAME')
    vantage_password = os.getenv('VANTAGE_PASSWORD')
    vantage_bearer_token = os.getenv('VANTAGE_BEARER_TOKEN')

    # VINOX credentials
    vinox_username = os.getenv('VINOX_USERNAME')
    vinox_password = os.getenv('VINOX_PASSWORD')

    # Base URLs
    vantage_base_url = os.getenv('VANTAGE_BASE_URL', 'https://vantagearguscv.iteris.com')
    vinox_base_url = os.getenv('VINOX_BASE_URL', 'http://124.66.170.66')

    # Validate required credentials
    if not all([vinox_username, vinox_password]):
        raise KeyError("Missing required environment variables for VINOX")

    if not (vantage_bearer_token or (vantage_username and vantage_password)):
        raise KeyError("Missing Vantage credentials (set VANTAGE_BEARER_TOKEN or VANTAGE_USERNAME/VANTAGE_PASSWORD)")

    # Build full URLs
    vantage_pairs_url = f"{vantage_base_url}/public-api/v1/pairs"
    vantage_locations_url = f"{vantage_base_url}/public-api/v1/locations"
    vinox_auth_url = f"{vinox_base_url}/adorvmsapi/authenticate"
    vinox_players_url = f"{vinox_base_url}/adorvmsapi/v1/players"

    print("Credentials loaded from environment")
    print(f"Vantage Base URL: {vantage_base_url}")
    print(f"VINOX Base URL: {vinox_base_url}")

except KeyError as e:
    print(f"Error: {e}")
    exit(1)

# STEP 2: Fetch Pairs from Vantage Argus (Using HTTP Basic Auth)
print("\nSTEP 2: Fetching Pair IDs from Vantage Argus...")

try:
    # Use Bearer token if provided, otherwise HTTP Basic Auth
    headers = None
    auth = None
    if vantage_bearer_token:
        token_value = vantage_bearer_token.strip()
        if token_value.lower().startswith("bearer "):
            token_value = token_value.split(" ", 1)[1].strip()
        headers = {"Authorization": f"Bearer {token_value}"}
    else:
        auth = (vantage_username, vantage_password)

    pairs_response = requests.get(
        vantage_pairs_url,
        auth=auth,
        headers=headers,
        timeout=15
    )

    if pairs_response.status_code != 200:
        raise Exception(f"Failed to fetch pairs: HTTP {pairs_response.status_code}")

    pairs_data = pairs_response.json()

    # Handle different response formats
    if isinstance(pairs_data, dict):
        pairs = pairs_data.get('data') or pairs_data.get('pairs') or []
    elif isinstance(pairs_data, list):
        pairs = pairs_data
    else:
        pairs = []

    if not pairs:
        print("No pairs fetched")
        print(f"Response type: {type(pairs_data)}")
        if isinstance(pairs_data, dict):
            print(f"Response keys: {list(pairs_data.keys())}")

    print(f"Fetched {len(pairs)} Pair IDs from Vantage Argus")

    # Show first 3 pairs as examples
    for i, pair in enumerate(pairs[:3]):
        pair_id = pair.get('id')
        pair_name = pair.get('name') or pair.get('title')
        print(f"   {i+1}. Pair ID: {pair_id} - {pair_name}")

    if len(pairs) > 3:
        print(f"   ... and {len(pairs)-3} more pairs")

except Exception as e:
    print(f"Error: {str(e)}")
    exit(1)

# STEP 3: Fetch Locations from Vantage Argus (Optional)
print("\nSTEP 3: Fetching Locations from Vantage Argus...")

try:
    headers = None
    auth = None
    if vantage_bearer_token:
        token_value = vantage_bearer_token.strip()
        if token_value.lower().startswith("bearer "):
            token_value = token_value.split(" ", 1)[1].strip()
        headers = {"Authorization": f"Bearer {token_value}"}
    else:
        auth = (vantage_username, vantage_password)

    locations_response = requests.get(
        vantage_locations_url,
        auth=auth,
        headers=headers,
        timeout=15
    )

    if locations_response.status_code == 200:
        locations_data = locations_response.json()

        if isinstance(locations_data, dict):
            locations = locations_data.get('data') or locations_data.get('locations') or []
        elif isinstance(locations_data, list):
            locations = locations_data
        else:
            locations = []

        print(f"Fetched {len(locations)} Locations from Vantage Argus")
    else:
        print(f"Locations endpoint returned {locations_response.status_code}")
        locations = []

except Exception as e:
    print(f"Error fetching locations: {str(e)}")
    locations = []

# STEP 4: Authenticate to VINOX
print("\nSTEP 4: Authenticating to VINOX...")

try:
    vinox_auth_response = requests.post(
        vinox_auth_url,
        json={
            "username": vinox_username,
            "password": vinox_password
        },
        timeout=10
    )

    if vinox_auth_response.status_code != 200:
        raise Exception(f"Authentication failed: {vinox_auth_response.status_code}")

    vinox_token = vinox_auth_response.json().get('token')

    if not vinox_token:
        raise Exception("No token in VINOX authentication response")

    print("VINOX token received")

except Exception as e:
    print(f"Error: {str(e)}")
    exit(1)

# STEP 5: Fetch Players from VINOX
print("\nSTEP 5: Fetching Player IDs from VINOX...")

try:
    players_response = requests.get(
        vinox_players_url,
        headers={"Authorization": f"Bearer {vinox_token}"},
        timeout=15
    )

    if players_response.status_code != 200:
        raise Exception(f"Failed to fetch players: HTTP {players_response.status_code}")

    players_data = players_response.json()

    # Handle different response formats
    if isinstance(players_data, dict):
        players = players_data.get('data') or players_data.get('players') or []
    elif isinstance(players_data, list):
        players = players_data
    else:
        players = []

    if not players:
        print("No players fetched")
        print(f"Response type: {type(players_data)}")

    print(f"Fetched {len(players)} Player IDs from VINOX")

    # Show first 3 players as examples
    for i, player in enumerate(players[:3]):
        player_id = player.get('playerId') or player.get('id')
        player_name = player.get('name') or player.get('playerName')
        print(f"   {i+1}. Player ID: {str(player_id)[:30]}... - {player_name}")

    if len(players) > 3:
        print(f"   ... and {len(players)-3} more players")

except Exception as e:
    print(f"Error: {str(e)}")
    exit(1)

# STEP 6: Create Player-Pair Mapping
print("\nSTEP 6: Creating Player-Pair Mapping...")

mapping_data = []

try:
    if len(pairs) == 0:
        print("No pairs available for mapping")

    for i, player in enumerate(players):
        player_id = player.get('playerId') or player.get('id')
        player_name = player.get('name') or player.get('playerName')

        # Distribute players across pairs (round-robin)
        if pairs:
            pair_index = i % len(pairs)
            pair = pairs[pair_index]
            pair_id = pair.get('id')
            corridor_name = pair.get('name') or pair.get('title')
        else:
            pair_id = 'N/A'
            corridor_name = 'N/A'

        mapping_data.append({
            'sr_no': i + 1,
            'player_name': player_name,
            'player_id': player_id,
            'pair_id': pair_id,
            'corridor_name': corridor_name
        })

    print(f"Created mapping for {len(mapping_data)} players")

except Exception as e:
    print(f"Error creating mapping: {str(e)}")
    exit(1)

# STEP 7: Generate Excel File
print("\nSTEP 7: Creating Excel File...")

try:
    wb = Workbook()
    ws = wb.active
    ws.title = "Player-Pair Mapping"

    headers = ['Sr.No', 'VMS Player Name', 'Player ID', 'Pair ID', 'Corridor Name']
    ws.append(headers)

    for item in mapping_data:
        ws.append([
            item['sr_no'],
            item['player_name'],
            item['player_id'],
            item['pair_id'],
            item['corridor_name']
        ])

    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 30
    ws.column_dimensions['C'].width = 35
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 40

    filename = 'player_pair_mapping.xlsx'
    wb.save(filename)

    print(f"Excel File Created: {filename}")

except Exception as e:
    print(f"Error creating Excel: {str(e)}")
    exit(1)

# FINAL SUMMARY
print("\n" + "="*80)
print("COMPLETE")
print("="*80)
print(f"\nSummary:")
print(f"   Pairs from Vantage Argus: {len(pairs)}")
print(f"   Locations from Vantage: {len(locations)}")
print(f"   Players from VINOX: {len(players)}")
print(f"   Mappings Created: {len(mapping_data)}")
print(f"   Excel File Created: {filename}")
print("\nExcel Columns:")
print("   - Sr.No (Serial Number)")
print("   - VMS Player Name (Location)")
print("   - Player ID (from VINOX)")
print("   - Pair ID (from Vantage Argus)")
print("   - Corridor Name (Route)")
print("\nFile saved in current directory!")
print("="*80 + "\n")
