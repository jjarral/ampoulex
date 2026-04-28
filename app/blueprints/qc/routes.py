"""
Quality Control Blueprint Routes

Handles all QC-related HTTP requests including quality tests,
inspections, approvals, and compliance tracking.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from typing import Dict, List, Any, Optional
from datetime import datetime

qc_bp = Blueprint('qc', __name__, url_prefix='/qc')

# In-memory storage (replace with database in production)
qc_tests_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "test_name": "Dissolution Test",
        "product_type": "Tablets",
        "parameters": ["pH", "Temperature", "Time"],
        "standard": "USP <711>",
        "status": "active"
    },
    {
        "id": 2,
        "test_name": "Hardness Test",
        "product_type": "Tablets",
        "parameters": ["Force", "Thickness"],
        "standard": "In-house",
        "status": "active"
    },
    {
        "id": 3,
        "test_name": "Microbial Limit Test",
        "product_type": "All",
        "parameters": ["TAMC", "TYMC", "Pathogens"],
        "standard": "USP <61>",
        "status": "active"
    }
]

inspections_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "inspection_number": "QC-2024-001",
        "batch_number": "BATCH-2024-001",
        "product_name": "Paracetamol 500mg",
        "inspection_type": "Release",
        "status": "in_progress",
        "inspector": "Dr. Jane Smith",
        "start_date": "2024-03-15",
        "tests_completed": 2,
        "tests_total": 5,
        "created_at": "2024-03-15"
    },
    {
        "id": 2,
        "inspection_number": "QC-2024-002",
        "batch_number": "BATCH-2024-002",
        "product_name": "Ibuprofen 200mg",
        "inspection_type": "Release",
        "status": "pending",
        "inspector": "Dr. John Doe",
        "start_date": None,
        "tests_completed": 0,
        "tests_total": 5,
        "created_at": "2024-03-16"
    }
]

test_results_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "inspection_id": 1,
        "test_id": 1,
        "test_name": "Dissolution Test",
        "result": "98.5%",
        "specification": "NLT 80%",
        "status": "pass",
        "tested_by": "Lab Tech A",
        "tested_at": "2024-03-15 14:30"
    },
    {
        "id": 2,
        "inspection_id": 1,
        "test_id": 2,
        "test_name": "Hardness Test",
        "result": "8.5 kp",
        "specification": "6-10 kp",
        "status": "pass",
        "tested_by": "Lab Tech B",
        "tested_at": "2024-03-15 15:00"
    }
]


@qc_bp.route('/')
def index():
    """List all QC inspections."""
    status_filter = request.args.get('status', '')
    type_filter = request.args.get('type', '')
    
    filtered_inspections = inspections_db
    
    if status_filter:
        filtered_inspections = [i for i in filtered_inspections if i['status'] == status_filter]
    
    if type_filter:
        filtered_inspections = [i for i in filtered_inspections if i['inspection_type'] == type_filter]
    
    return render_template('qc/index.html', 
                         inspections=filtered_inspections,
                         status_filter=status_filter,
                         type_filter=type_filter)


@qc_bp.route('/new')
def new():
    """Display form to create new QC inspection."""
    return render_template('qc/new.html', tests=qc_tests_db)


@qc_bp.route('/', methods=['POST'])
def create():
    """Create a new QC inspection."""
    try:
        new_id = max([i['id'] for i in inspections_db], default=0) + 1
        today = datetime.now()
        
        new_inspection = {
            "id": new_id,
            "inspection_number": f"QC-{today.strftime('%Y')}-{new_id:03d}",
            "batch_number": request.form.get('batch_number'),
            "product_name": request.form.get('product_name'),
            "inspection_type": request.form.get('inspection_type', 'Release'),
            "status": "pending",
            "inspector": request.form.get('inspector'),
            "start_date": None,
            "tests_completed": 0,
            "tests_total": int(request.form.get('tests_total', 5)),
            "created_at": today.strftime('%Y-%m-%d')
        }
        
        inspections_db.append(new_inspection)
        flash(f'QC Inspection "{new_inspection["inspection_number"]}" created successfully!', 'success')
        return redirect(url_for('qc.index'))
    
    except Exception as e:
        flash(f'Error creating inspection: {str(e)}', 'danger')
        return render_template('qc/new.html'), 400


@qc_bp.route('/<int:inspection_id>')
def show(inspection_id: int):
    """Display QC inspection details."""
    inspection = next((i for i in inspections_db if i['id'] == inspection_id), None)
    
    if not inspection:
        flash('Inspection not found', 'danger')
        return redirect(url_for('qc.index'))
    
    inspection_results = [r for r in test_results_db if r['inspection_id'] == inspection_id]
    
    return render_template('qc/show.html', 
                         inspection=inspection,
                         results=inspection_results,
                         available_tests=qc_tests_db)


@qc_bp.route('/<int:inspection_id>/start', methods=['POST'])
def start_inspection(inspection_id: int):
    """Start a QC inspection."""
    try:
        inspection = next((i for i in inspections_db if i['id'] == inspection_id), None)
        
        if not inspection:
            flash('Inspection not found', 'danger')
            return redirect(url_for('qc.index'))
        
        inspection['status'] = 'in_progress'
        inspection['start_date'] = datetime.now().strftime('%Y-%m-%d')
        
        flash(f'Inspection "{inspection["inspection_number"]}" started!', 'success')
        return redirect(url_for('qc.show', inspection_id=inspection_id))
    
    except Exception as e:
        flash(f'Error starting inspection: {str(e)}', 'danger')
        return redirect(url_for('qc.show', inspection_id=inspection_id))


@qc_bp.route('/<int:inspection_id>/record-test', methods=['GET', 'POST'])
def record_test(inspection_id: int):
    """Record a test result for an inspection."""
    inspection = next((i for i in inspections_db if i['id'] == inspection_id), None)
    
    if not inspection:
        flash('Inspection not found', 'danger')
        return redirect(url_for('qc.index'))
    
    if request.method == 'GET':
        return render_template('qc/record_test.html', 
                             inspection=inspection,
                             tests=qc_tests_db)
    
    try:
        new_id = max([r['id'] for r in test_results_db], default=0) + 1
        
        test_result = {
            "id": new_id,
            "inspection_id": inspection_id,
            "test_id": int(request.form.get('test_id')),
            "test_name": request.form.get('test_name'),
            "result": request.form.get('result'),
            "specification": request.form.get('specification'),
            "status": request.form.get('status', 'pending'),
            "tested_by": request.form.get('tested_by'),
            "tested_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        test_results_db.append(test_result)
        
        # Update inspection progress
        inspection['tests_completed'] = len([r for r in test_results_db if r['inspection_id'] == inspection_id])
        
        flash(f'Test result recorded successfully!', 'success')
        return redirect(url_for('qc.show', inspection_id=inspection_id))
    
    except Exception as e:
        flash(f'Error recording test result: {str(e)}', 'danger')
        return render_template('qc/record_test.html', inspection=inspection), 400


@qc_bp.route('/<int:inspection_id>/approve', methods=['POST'])
def approve_inspection(inspection_id: int):
    """Approve a QC inspection."""
    try:
        inspection = next((i for i in inspections_db if i['id'] == inspection_id), None)
        
        if not inspection:
            flash('Inspection not found', 'danger')
            return redirect(url_for('qc.index'))
        
        # Check if all tests are completed and passed
        inspection_results = [r for r in test_results_db if r['inspection_id'] == inspection_id]
        failed_tests = [r for r in inspection_results if r['status'] == 'fail']
        
        if failed_tests:
            flash('Cannot approve inspection with failed tests', 'danger')
            return redirect(url_for('qc.show', inspection_id=inspection_id))
        
        if inspection['tests_completed'] < inspection['tests_total']:
            flash('Not all tests completed', 'warning')
            return redirect(url_for('qc.show', inspection_id=inspection_id))
        
        inspection['status'] = 'approved'
        
        flash(f'Inspection "{inspection["inspection_number"]}" approved!', 'success')
        return redirect(url_for('qc.show', inspection_id=inspection_id))
    
    except Exception as e:
        flash(f'Error approving inspection: {str(e)}', 'danger')
        return redirect(url_for('qc.show', inspection_id=inspection_id))


@qc_bp.route('/<int:inspection_id>/reject', methods=['POST'])
def reject_inspection(inspection_id: int):
    """Reject a QC inspection."""
    try:
        inspection = next((i for i in inspections_db if i['id'] == inspection_id), None)
        
        if not inspection:
            flash('Inspection not found', 'danger')
            return redirect(url_for('qc.index'))
        
        reason = request.form.get('reason', 'No reason provided')
        inspection['status'] = 'rejected'
        inspection['rejection_reason'] = reason
        
        flash(f'Inspection "{inspection["inspection_number"]}" rejected!', 'warning')
        return redirect(url_for('qc.show', inspection_id=inspection_id))
    
    except Exception as e:
        flash(f'Error rejecting inspection: {str(e)}', 'danger')
        return redirect(url_for('qc.show', inspection_id=inspection_id))


@qc_bp.route('/tests')
def tests():
    """List all QC tests."""
    return render_template('qc/tests.html', tests=qc_tests_db)


@qc_bp.route('/tests/new')
def new_test():
    """Display form to create new QC test."""
    return render_template('qc/new_test.html')


@qc_bp.route('/tests', methods=['POST'])
def create_test():
    """Create a new QC test."""
    try:
        new_id = max([t['id'] for t in qc_tests_db], default=0) + 1
        
        new_test = {
            "id": new_id,
            "test_name": request.form.get('test_name'),
            "product_type": request.form.get('product_type'),
            "parameters": request.form.get('parameters', '').split(','),
            "standard": request.form.get('standard'),
            "status": "active"
        }
        
        qc_tests_db.append(new_test)
        flash(f'Test "{new_test["test_name"]}" created successfully!', 'success')
        return redirect(url_for('qc.tests'))
    
    except Exception as e:
        flash(f'Error creating test: {str(e)}', 'danger')
        return render_template('qc/new_test.html'), 400


@qc_bp.route('/reports/compliance')
def compliance_report():
    """Generate QC compliance report."""
    total_inspections = len(inspections_db)
    approved = len([i for i in inspections_db if i['status'] == 'approved'])
    rejected = len([i for i in inspections_db if i['status'] == 'rejected'])
    in_progress = len([i for i in inspections_db if i['status'] == 'in_progress'])
    
    compliance_rate = (approved / total_inspections * 100) if total_inspections > 0 else 0
    
    return render_template('qc/reports/compliance.html',
                         total_inspections=total_inspections,
                         approved=approved,
                         rejected=rejected,
                         in_progress=in_progress,
                         compliance_rate=compliance_rate)


@qc_bp.route('/api/list')
def api_list():
    """API endpoint to list QC inspections."""
    return jsonify({
        'success': True,
        'data': inspections_db,
        'count': len(inspections_db)
    })


@qc_bp.route('/api/<int:inspection_id>')
def api_show(inspection_id: int):
    """API endpoint to get QC inspection details."""
    inspection = next((i for i in inspections_db if i['id'] == inspection_id), None)
    
    if not inspection:
        return jsonify({'success': False, 'error': 'Inspection not found'}), 404
    
    results = [r for r in test_results_db if r['inspection_id'] == inspection_id]
    
    return jsonify({
        'success': True,
        'data': inspection,
        'results': results
    })
