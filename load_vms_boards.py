"""
Script to load all 20 VMS boards into database
Each board represents a digital display location in Pune
"""

import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atms_backend.settings')
django.setup()

from traffic.models import VMSBoard

print("\n" + "="*70)
print("LOADING 20 VMS BOARDS INTO POSTGRESQL DATABASE")
print("="*70 + "\n")

# ALL 20 VMS BOARDS DATA
vms_boards_data = [
    {
        'board_id': 1,
        'vms_player_name': 'Sahjeevan chowk',
        'corridor_name': 'Karve chowk to khandoji baba',
        'pair_id': 55745,
        'location': 'Sahjeevan chowk',
        'latitude': Decimal('18.5230'),
        'longitude': Decimal('73.8567'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 2,
        'vms_player_name': 'Puram chowk',
        'corridor_name': 'Alka chowk to swargate',
        'pair_id': 55848,
        'location': 'Puram chowk',
        'latitude': Decimal('18.5156'),
        'longitude': Decimal('73.8524'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 3,
        'vms_player_name': 'Rawat Brother',
        'corridor_name': 'Rawat brother to katraj Naka',
        'pair_id': 55775,
        'location': 'Rawat Brother',
        'latitude': Decimal('18.5347'),
        'longitude': Decimal('73.8612'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 4,
        'vms_player_name': 'Chavya Nagar',
        'corridor_name': 'Katraj naka to Rawat Brothers',
        'pair_id': 55777,
        'location': 'Chavya Nagar',
        'latitude': Decimal('18.4696'),
        'longitude': Decimal('73.9035'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 5,
        'vms_player_name': 'AFMC',
        'corridor_name': 'St. mary to Sopan Baug',
        'pair_id': 27857,
        'location': 'AFMC',
        'latitude': Decimal('18.5230'),
        'longitude': Decimal('73.8567'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 6,
        'vms_player_name': 'Dhobi Ghat',
        'corridor_name': 'Swargate to Rawat Brothers',
        'pair_id': 55774,
        'location': 'Dhobi Ghat',
        'latitude': Decimal('18.5156'),
        'longitude': Decimal('73.8524'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 7,
        'vms_player_name': 'Mitramandal',
        'corridor_name': 'Swargate to navshya maruti chowk',
        'pair_id': 55974,
        'location': 'Mitramandal',
        'latitude': Decimal('18.5912'),
        'longitude': Decimal('73.8110'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 8,
        'vms_player_name': 'Mitramandal',
        'corridor_name': 'Sarasbaug to AISSMS',
        'pair_id': 56172,
        'location': 'Mitramandal',
        'latitude': Decimal('18.5912'),
        'longitude': Decimal('73.8110'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 9,
        'vms_player_name': 'Vetai Baba',
        'corridor_name': 'Hivaji housing society to Athavle chowk',
        'pair_id': 27865,
        'location': 'Vetai Baba',
        'latitude': Decimal('18.5742'),
        'longitude': Decimal('73.9170'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 10,
        'vms_player_name': 'Kalyani nagar',
        'corridor_name': 'Gunjan to khardi bypass',
        'pair_id': 57843,
        'location': 'Kalyani nagar',
        'latitude': Decimal('18.5742'),
        'longitude': Decimal('73.9170'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 11,
        'vms_player_name': 'Vimannagar',
        'corridor_name': 'Shastri chowk to khardi bypass',
        'pair_id': 27861,
        'location': 'Vimannagar',
        'latitude': Decimal('18.5742'),
        'longitude': Decimal('73.9170'),
        'display_time': '50 sec local content',
        'resolution': '1920x1080'
    },
    {
        'board_id': 12,
        'vms_player_name': 'Badami chowk',
        'corridor_name': 'SOS to Gunjan',
        'pair_id': 27860,
        'location': 'Badami chowk',
        'latitude': Decimal('18.5347'),
        'longitude': Decimal('73.8612'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 13,
        'vms_player_name': 'Lohiya jain IT park',
        'corridor_name': 'Lohiya jain IT park-1 to Anand nagar',
        'pair_id': 56174,
        'location': 'Lohiya jain IT park',
        'latitude': Decimal('18.5912'),
        'longitude': Decimal('73.8110'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 14,
        'vms_player_name': 'Maharaja chowk',
        'corridor_name': 'Lohiya jain IT park-1 to Anand nagar',
        'pair_id': 56174,
        'location': 'Maharaja chowk',
        'latitude': Decimal('18.5912'),
        'longitude': Decimal('73.8110'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 15,
        'vms_player_name': 'Balaji Nagar',
        'corridor_name': 'Pashan circle to Shivshakti',
        'pair_id': 56166,
        'location': 'Balaji Nagar',
        'latitude': Decimal('18.5230'),
        'longitude': Decimal('73.8567'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 16,
        'vms_player_name': 'Vaiduavdi chowk',
        'corridor_name': 'Ravidarsha to sopan baug',
        'pair_id': 55948,
        'location': 'Vaiduavdi chowk',
        'latitude': Decimal('18.5156'),
        'longitude': Decimal('73.8524'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 17,
        'vms_player_name': 'Chandan nagar',
        'corridor_name': 'shastri chowk to khardi bypass',
        'pair_id': 57444,
        'location': 'Chandan nagar',
        'latitude': Decimal('18.5742'),
        'longitude': Decimal('73.9170'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 18,
        'vms_player_name': 'TATA Guard room',
        'corridor_name': 'shastri chowk to khardi bypass',
        'pair_id': 57444,
        'location': 'TATA Guard room',
        'latitude': Decimal('18.5742'),
        'longitude': Decimal('73.9170'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 19,
        'vms_player_name': 'Ganesh mala',
        'corridor_name': 'Dadekar to navshya maruti',
        'pair_id': 55970,
        'location': 'Ganesh mala',
        'latitude': Decimal('18.5912'),
        'longitude': Decimal('73.8110'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
    {
        'board_id': 20,
        'vms_player_name': 'Sopan baug',
        'corridor_name': 'Sopan baug to swargate',
        'pair_id': 57445,
        'location': 'Sopan baug',
        'latitude': Decimal('18.5156'),
        'longitude': Decimal('73.8524'),
        'display_time': '10 seconds every 1 Min',
        'resolution': '1920x1080'
    },
]

# LOAD ALL BOARDS
print("📊 Loading VMS Board data...\n")

for data in vms_boards_data:
    vms_board, created = VMSBoard.objects.get_or_create(
        board_id=data['board_id'],
        defaults=data
    )
    if created:
        print(f"  ✓ Board {vms_board.board_id}: {vms_board.vms_player_name}")
    else:
        print(f"  → Board {vms_board.board_id}: Already exists")

print("\n" + "="*70)
print("✅ ALL 20 VMS BOARDS LOADED SUCCESSFULLY!")
print("="*70 + "\n")

# Show summary
total_boards = VMSBoard.objects.count()
active_boards = VMSBoard.objects.filter(is_active=True).count()

print(f"Total Boards in Database: {total_boards}")
print(f"Active Boards: {active_boards}")
print("\n")