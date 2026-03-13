# FIXED: traffic/urls.py
# Only changed: Removed router.register for viewsets that don't exist
# Kept: All auth endpoints exactly as-is

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from traffic import views
from traffic.views_auth import LoginView, ForgotPasswordView, VerifyResetCodeView, ResetPasswordView
from traffic.views import PlayerPairMappingView, VnoxPlayerListView, VnoxPlayerDetailView, VnoxEmergencyMessageView, VnoxConnectionTestView, VantageSpeedView, VnoxSpeedEmergencyView, VnoxCustomEmergencyView

# Create router
router = DefaultRouter()

router.register(r'vms-boards', views.VMSBoardViewSet)
router.register(r'intersections', views.IntersectionViewSet)
router.register(r'signals', views.SignalViewSet)
router.register(r'routes', views.RouteViewSet)
router.register(r'traffic-data', views.TrafficDataViewSet)
router.register(r'travel-times', views.TravelTimeViewSet)

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # ==================== AUTHENTICATION ENDPOINTS ====================
    
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('auth/verify-reset-code/', VerifyResetCodeView.as_view(), name='verify-reset-code'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset-password'),

    # Player-Pair mapping endpoint
    path('player-pair-mapping/', PlayerPairMappingView.as_view(), name='player-pair-mapping'),

    # ==================== VNOX API ENDPOINTS ====================
    
    path('vnox/players/', VnoxPlayerListView.as_view(), name='vnox-players'),
    path('vnox/players/<str:player_id>/', VnoxPlayerDetailView.as_view(), name='vnox-player-detail'),
    path('vnox/emergency-message/', VnoxEmergencyMessageView.as_view(), name='vnox-emergency-message'),
    path('vnox/test-connection/', VnoxConnectionTestView.as_view(), name='vnox-test-connection'),

    # ==================== VANTAGE + VNOX INTEGRATION ENDPOINTS ====================
    
    path('vantage/speed/', VantageSpeedView.as_view(), name='vantage-speed'),
    path('vnox/speed-emergency/', VnoxSpeedEmergencyView.as_view(), name='vnox-speed-emergency'),
    path('vnox/custom-emergency/', VnoxCustomEmergencyView.as_view(), name='vnox-custom-emergency'),
]
