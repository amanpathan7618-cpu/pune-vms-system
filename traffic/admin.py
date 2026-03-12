# FIXED: traffic/admin.py
# ONLY CHANGE: Removed filter_horizontal = ('vms_boards',) line since vms_boards is commented out in models

from django.contrib import admin
from traffic.models import VMSBoard


@admin.register(VMSBoard)
class VMSBoardAdmin(admin.ModelAdmin):
    list_display = ('board_id', 'vms_player_name', 'location', 'is_active', 'last_update')
    search_fields = ('board_id', 'vms_player_name', 'corridor_name', 'location')
    list_filter = ('is_active',)


