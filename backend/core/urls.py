from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/complaints/", include("complaints.urls")),
    path("api/v1/sla/", include("sla_engine.urls")),
    path("api/v1/gis/", include("gis.urls")),
    path("api/v1/ai/", include("ai_routing.urls")),
    path("api/v1/notifications/", include("notifications.urls")),
    path("api/v1/workforce/", include("workforce.urls")),
    path("api/v1/iot/", include("iot.urls")),
    path("api/v1/gamification/", include("gamification.urls")),
    path("api/v1/analytics/", include("analytics.urls")),
]
