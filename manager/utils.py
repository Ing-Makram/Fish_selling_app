# manager/utils.py (create new file)
from django.db.models import Sum, F, Count
from django.utils import timezone
from datetime import timedelta
from .models import Sale

def get_date_range(period):
    today = timezone.now().date()
    if period == 'daily':
        return today, today
    elif period == 'weekly':
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start, end
    elif period == 'monthly':
        start = today.replace(day=1)
        end = (start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        return start, end
    elif period == 'yearly':
        start = today.replace(month=1, day=1)
        end = today.replace(month=12, day=31)
        return start, end
    return None, None

def calculate_sales_summary(period=None):
    if period:
        start_date, end_date = get_date_range(period)
        sales = Sale.objects.filter(sale_date__date__range=[start_date, end_date])
    else:
        sales = Sale.objects.all()
    
    # Calculate summary statistics
    summary = sales.aggregate(
        total_sales=Count('id'),
        total_revenue=Sum('total_price'),
        total_quantity=Sum('quantity')
    )
    
    # Add period information
    summary['period'] = period
    if period:
        summary['start_date'] = start_date
        summary['end_date'] = end_date
    
    return summary

def get_best_selling_products(period=None, limit=5):
    if period:
        start_date, end_date = get_date_range(period)
        sales = Sale.objects.filter(sale_date__date__range=[start_date, end_date])
    else:
        sales = Sale.objects.all()
    
    # Aggregate best-selling products
    return sales.values(
        'product_id', 
        'product_name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('total_price'),
        sale_count=Count('id')
    ).order_by('-total_quantity')[:limit]