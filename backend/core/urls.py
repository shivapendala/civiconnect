from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import index_view

urlpatterns = [
    path('', index_view, name='index'),
    path('admin/', admin.site.urls),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/complaints/', include('complaints.urls')),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('complaints.urls')),
]
