from django.urls import include, path
from rest_framework.routers import DefaultRouter
from manager.views import ProductViewSet, SaleViewSet, CommandViewSet, DashboardViewSet , DashboardViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'commands', CommandViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls))
]
