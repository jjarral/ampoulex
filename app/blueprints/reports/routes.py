"""
Reports Blueprint Routes

Handles all reporting-related HTTP requests including dashboard,
analytics, and various business reports.
"""

from flask import Blueprint, render_template, request, jsonify
from typing import Dict, List, Any
from datetime import datetime, timedelta

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

# Mock data for reports
dashboard_stats = {
    "total_products": 156,
    "total_orders": 1243,
    "pending_orders": 45,
    "total_customers": 89,
    "total_suppliers": 23,
    "inventory_value": 1250000,
    "monthly_revenue": 450000,
    "production_efficiency": 92.5,
    "qc_compliance_rate": 98.2
}


@reports_bp.route('/')
def index():
    """List all available reports."""
    reports_list = [
        {"name": "Sales Report", "url": "/reports/sales", "description": "Monthly and yearly sales analysis"},
        {"name": "Inventory Report", "url": "/reports/inventory", "description": "Stock levels and valuation"},
        {"name": "Production Report", "url": "/reports/production", "description": "Production efficiency and output"},
        {"name": "QC Report", "url": "/reports/qc", "description": "Quality control compliance"},
        {"name": "Financial Report", "url": "/reports/financial", "description": "Revenue and expense summary"},
        {"name": "Customer Report", "url": "/reports/customers", "description": "Customer analytics"},
        {"name": "Supplier Report", "url": "/reports/suppliers", "description": "Supplier performance metrics"}
    ]
    return render_template('reports/index.html', reports=reports_list)


@reports_bp.route('/dashboard')
def dashboard():
    """Display main dashboard with key metrics."""
    # Calculate trends (mock data)
    trends = {
        "revenue_trend": "+12.5%",
        "orders_trend": "+8.3%",
        "customers_trend": "+5.1%",
        "inventory_trend": "-2.4%"
    }
    
    # Recent activities (mock data)
    recent_activities = [
        {"type": "order", "message": "New order #ORD-2024-156 created", "time": "10 minutes ago"},
        {"type": "production", "message": "Batch BATCH-2024-001 completed", "time": "1 hour ago"},
        {"type": "qc", "message": "QC Inspection QC-2024-001 approved", "time": "2 hours ago"},
        {"type": "inventory", "message": "Low stock alert: Paracetamol 500mg", "time": "3 hours ago"},
        {"type": "customer", "message": "New customer registered: MedPharm Ltd", "time": "5 hours ago"}
    ]
    
    return render_template('reports/dashboard.html', 
                         stats=dashboard_stats,
                         trends=trends,
                         activities=recent_activities)


@reports_bp.route('/sales')
def sales_report():
    """Generate sales report."""
    period = request.args.get('period', 'monthly')
    
    # Mock sales data
    sales_data = {
        "monthly": {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "revenue": [380000, 420000, 450000, 410000, 480000, 520000],
            "orders": [95, 102, 115, 98, 125, 138]
        },
        "yearly": {
            "labels": ["2020", "2021", "2022", "2023", "2024"],
            "revenue": [3200000, 3800000, 4500000, 5100000, 5800000],
            "orders": [980, 1150, 1380, 1520, 1750]
        }
    }
    
    selected_data = sales_data.get(period, sales_data['monthly'])
    
    return render_template('reports/sales.html', 
                         period=period,
                         data=selected_data)


@reports_bp.route('/inventory')
def inventory_report():
    """Generate inventory report."""
    # Mock inventory data
    inventory_summary = {
        "total_items": 156,
        "total_value": 1250000,
        "low_stock_items": 12,
        "out_of_stock_items": 3,
        "overstocked_items": 8
    }
    
    category_breakdown = [
        {"category": "Tablets", "count": 65, "value": 520000},
        {"category": "Capsules", "count": 42, "value": 380000},
        {"category": "Injections", "count": 28, "value": 250000},
        {"category": "Syrups", "count": 21, "value": 100000}
    ]
    
    return render_template('reports/inventory.html', 
                         summary=inventory_summary,
                         categories=category_breakdown)


@reports_bp.route('/production')
def production_report():
    """Generate production report."""
    # Mock production data
    production_summary = {
        "total_orders": 48,
        "completed": 35,
        "in_progress": 10,
        "pending": 3,
        "efficiency_rate": 92.5,
        "avg_completion_time": "5.2 days"
    }
    
    monthly_output = [
        {"month": "Jan", "output": 8500, "target": 8000},
        {"month": "Feb", "output": 9200, "target": 9000},
        {"month": "Mar", "output": 8800, "target": 9000},
        {"month": "Apr", "output": 9500, "target": 9000},
        {"month": "May", "output": 10200, "target": 9500},
        {"month": "Jun", "output": 9800, "target": 9500}
    ]
    
    return render_template('reports/production.html', 
                         summary=production_summary,
                         output=monthly_output)


@reports_bp.route('/qc')
def qc_report():
    """Generate QC compliance report."""
    # Mock QC data
    qc_summary = {
        "total_inspections": 156,
        "approved": 148,
        "rejected": 5,
        "in_progress": 3,
        "compliance_rate": 96.8
    }
    
    rejection_reasons = [
        {"reason": "Failed Dissolution Test", "count": 2},
        {"reason": "Microbial Contamination", "count": 2},
        {"reason": "Weight Variation", "count": 1}
    ]
    
    return render_template('reports/qc.html', 
                         summary=qc_summary,
                         rejections=rejection_reasons)


@reports_bp.route('/financial')
def financial_report():
    """Generate financial report."""
    # Mock financial data
    financial_summary = {
        "total_revenue": 2650000,
        "total_expenses": 1890000,
        "net_profit": 760000,
        "profit_margin": 28.7,
        "accounts_receivable": 320000,
        "accounts_payable": 180000
    }
    
    expense_breakdown = [
        {"category": "Raw Materials", "amount": 850000, "percentage": 45},
        {"category": "Labor", "amount": 470000, "percentage": 25},
        {"category": "Overhead", "amount": 285000, "percentage": 15},
        {"category": "R&D", "amount": 190000, "percentage": 10},
        {"category": "Other", "amount": 95000, "percentage": 5}
    ]
    
    return render_template('reports/financial.html', 
                         summary=financial_summary,
                         expenses=expense_breakdown)


@reports_bp.route('/customers')
def customers_report():
    """Generate customer analytics report."""
    # Mock customer data
    customer_summary = {
        "total_customers": 89,
        "active_customers": 72,
        "new_this_month": 8,
        "avg_order_value": 12500,
        "top_customer": "MedPharm Ltd"
    }
    
    customer_segments = [
        {"segment": "Enterprise", "count": 15, "revenue_contribution": 45},
        {"segment": "Medium", "count": 32, "revenue_contribution": 35},
        {"segment": "Small", "count": 42, "revenue_contribution": 20}
    ]
    
    return render_template('reports/customers.html', 
                         summary=customer_summary,
                         segments=customer_segments)


@reports_bp.route('/suppliers')
def suppliers_report():
    """Generate supplier performance report."""
    # Mock supplier data
    supplier_summary = {
        "total_suppliers": 23,
        "active_suppliers": 20,
        "avg_delivery_time": "4.5 days",
        "on_time_rate": 94.2,
        "quality_score": 4.6
    }
    
    top_suppliers = [
        {"name": "Global Pharma Supplies", "orders": 45, "on_time_rate": 98, "rating": 4.8},
        {"name": "MediPack Industries", "orders": 38, "on_time_rate": 95, "rating": 4.5},
        {"name": "ChemRaw Corp", "orders": 32, "on_time_rate": 92, "rating": 4.3}
    ]
    
    return render_template('reports/suppliers.html', 
                         summary=supplier_summary,
                         top_suppliers=top_suppliers)


@reports_bp.route('/export/<report_type>')
def export_report(report_type: str):
    """Export report data."""
    # In real implementation, this would generate CSV/PDF
    return jsonify({
        'success': True,
        'message': f'Report "{report_type}" exported successfully',
        'format': 'CSV',
        'download_url': f'/downloads/{report_type}_{datetime.now().strftime("%Y%m%d")}.csv'
    })


@reports_bp.route('/api/dashboard')
def api_dashboard():
    """API endpoint for dashboard data."""
    return jsonify({
        'success': True,
        'data': dashboard_stats,
        'timestamp': datetime.now().isoformat()
    })
