from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, F
from .models import Product, Sale, Command
from .serializers import ProductSerializer, SaleSerializer, CommandSerializer
from .utils import calculate_sales_summary, get_best_selling_products


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by('-sale_date')
    serializer_class = SaleSerializer

class CommandViewSet(viewsets.ModelViewSet):
    queryset = Command.objects.all().order_by('-created_at')
    serializer_class = CommandSerializer

class DashboardViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def net_worth(self, request):
        net_worth = Product.objects.aggregate(
            total_value=Sum(F('current_stock') * F('price_per_kg'))
        )['total_value'] or 0
        return Response({'net_worth': net_worth})
    
    @action(detail=False, methods=['get'])
    def sales_summary(self, request):
        period = request.query_params.get('period', 'daily')
        # Implementation would filter by date range
        return Response({'period': period, 'total_sales': 0})  # Placeholder
    
class DashboardViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def net_worth(self, request):
        net_worth = Product.objects.aggregate(
            total_value=Sum(F('current_stock') * F('price_per_kg'))
        )['total_value'] or 0
        return Response({'net_worth': net_worth})
    
    @action(detail=False, methods=['get'])
    def sales_summary(self, request):
        period = request.query_params.get('period', 'daily')
        summary = calculate_sales_summary(period)
        return Response(summary)
    
    @action(detail=False, methods=['get'])
    def best_selling(self, request):
        period = request.query_params.get('period', 'weekly')
        limit = int(request.query_params.get('limit', 5))
        best_sellers = get_best_selling_products(period, limit)
        return Response(best_sellers)
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Comprehensive dashboard overview"""
        period = request.query_params.get('period', 'daily')
        return Response({
            'net_worth': self.net_worth(request).data,
            'sales_summary': calculate_sales_summary(period),
            'best_selling': get_best_selling_products(period, 5)
        })