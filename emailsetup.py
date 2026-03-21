"""
AMPOLLEX DATABASE FIX SCRIPT
Adds all missing columns to match models.py and routes.py
"""
from app import create_app, db
from sqlalchemy import inspect

def fix_database():
    app = create_app()
    
    with app.app_context():
        print("="*70)
        print("🔧 AMPOLLEX DATABASE FIX SCRIPT")
        print("="*70)
        print()
        
        # Get database inspector
        inspector = inspect(db.engine)
        
        # Define all missing columns per table
        missing_columns = {
            'product': [
                ('stock', 'INTEGER', '0'),
                ('base_price', 'NUMERIC(10,4)', '0'),
                ('price_per_unit', 'NUMERIC(10,4)', '0'),
                ('body_diameter', 'FLOAT', '0'),
                ('overall_length', 'FLOAT', '0'),
                ('sealing_point', 'FLOAT', '0'),
                ('body_length', 'FLOAT', '0'),
                ('stem_diameter', 'FLOAT', '0'),
                ('wall_thickness', 'FLOAT', '0'),
                ('material_type', 'VARCHAR(50)', 'NULL'),
                ('usp_type', 'VARCHAR(50)', 'NULL'),
                ('shape_type', 'VARCHAR(50)', 'NULL'),
                ('dimensions', 'VARCHAR(200)', 'NULL'),
                ('use_case', 'TEXT', 'NULL'),
                ('paint_color', 'VARCHAR(50)', 'NULL'),
                ('paint_type', 'VARCHAR(50)', 'NULL'),
                ('printing_method', 'VARCHAR(50)', 'NULL'),
            ],
            'user': [
                ('is_active', 'BOOLEAN', 'TRUE'),
                ('is_deleted', 'BOOLEAN', 'FALSE'),
                ('last_login', 'TIMESTAMP', 'NULL'),
                ('phone', 'VARCHAR(20)', 'NULL'),
                ('address', 'TEXT', 'NULL'),
            ],
            'customer': [
                ('business_name', 'VARCHAR(100)', 'NULL'),
                ('role', 'VARCHAR(50)', "'customer'"),
                ('is_active', 'BOOLEAN', 'TRUE'),
                ('is_deleted', 'BOOLEAN', 'FALSE'),
                ('credit_limit', 'FLOAT', '0'),
                ('current_balance', 'FLOAT', '0'),
                ('contact_person', 'VARCHAR(100)', 'NULL'),
                ('tax_number', 'VARCHAR(50)', 'NULL'),
            ],
            'employee': [
                ('cnic', 'VARCHAR(15)', 'NULL'),
                ('emergency_contact', 'VARCHAR(100)', 'NULL'),
                ('emergency_phone', 'VARCHAR(20)', 'NULL'),
                ('base_salary', 'FLOAT', '0'),
                ('payment_frequency', 'VARCHAR(20)', "'monthly'"),
                ('bank_account', 'VARCHAR(50)', 'NULL'),
                ('bank_name', 'VARCHAR(100)', 'NULL'),
                ('outstanding_loan', 'FLOAT', '0'),
                ('joined_date', 'TIMESTAMP', 'NULL'),
                ('is_active', 'BOOLEAN', 'TRUE'),
            ],
            'order': [
                ('order_number', 'VARCHAR(20)', 'NULL'),
                ('inquiry_id', 'INTEGER', 'NULL'),
                ('tax_amount', 'FLOAT', '0'),
                ('payment_method', 'VARCHAR(50)', 'NULL'),
                ('payment_date', 'TIMESTAMP', 'NULL'),
                ('paid_amount', 'FLOAT', '0'),
                ('customer_name_snapshot', 'VARCHAR(100)', 'NULL'),
                ('customer_business_snapshot', 'VARCHAR(100)', 'NULL'),
                ('customer_phone_snapshot', 'VARCHAR(20)', 'NULL'),
                ('customer_email_snapshot', 'VARCHAR(120)', 'NULL'),
                ('is_deleted', 'BOOLEAN', 'FALSE'),
                ('delivery_date', 'DATE', 'NULL'),
                ('shipping_address', 'TEXT', 'NULL'),
                ('billing_address', 'TEXT', 'NULL'),
                ('notes', 'TEXT', 'NULL'),
                ('payment_status', 'VARCHAR(20)', "'unpaid'"),
            ],
            'inquiry': [
                ('inquiry_number', 'VARCHAR(20)', 'NULL'),
                ('business_name', 'VARCHAR(100)', 'NULL'),
                ('is_deleted', 'BOOLEAN', 'FALSE'),
                ('deleted_at', 'TIMESTAMP', 'NULL'),
                ('updated_at', 'TIMESTAMP', 'NULL'),
            ],
            'production_batch': [
                ('batch_number', 'VARCHAR(50)', 'NULL'),
                ('product_id', 'INTEGER', 'NULL'),
                ('planned_quantity', 'INTEGER', '0'),
                ('actual_quantity', 'INTEGER', 'NULL'),
                ('rejected_quantity', 'INTEGER', '0'),
                ('yield_percentage', 'FLOAT', 'NULL'),
                ('status', 'VARCHAR(20)', "'planned'"),
                ('start_date', 'TIMESTAMP', 'NULL'),
                ('end_date', 'TIMESTAMP', 'NULL'),
                ('created_by', 'VARCHAR(100)', 'NULL'),
                ('notes', 'TEXT', 'NULL'),
                ('is_deleted', 'BOOLEAN', 'FALSE'),
            ],
            'raw_material': [
                ('material_type', 'VARCHAR(50)', 'NULL'),
                ('specification', 'VARCHAR(200)', 'NULL'),
                ('current_stock', 'FLOAT', '0'),
                ('unit', 'VARCHAR(20)', "'pieces'"),
                ('reorder_level', 'FLOAT', '0'),
                ('cost_per_unit', 'FLOAT', '0'),
                ('supplier', 'VARCHAR(100)', 'NULL'),
                ('is_active', 'BOOLEAN', 'TRUE'),
            ],
            'supplier': [
                ('contact_person', 'VARCHAR(100)', 'NULL'),
                ('email', 'VARCHAR(100)', 'NULL'),
                ('phone', 'VARCHAR(20)', 'NULL'),
                ('address', 'TEXT', 'NULL'),
                ('city', 'VARCHAR(50)', 'NULL'),
                ('country', 'VARCHAR(50)', "'Pakistan'"),
                ('cnic', 'VARCHAR(20)', 'NULL'),
                ('ntn', 'VARCHAR(20)', 'NULL'),
                ('payment_terms', 'VARCHAR(50)', "'30 days'"),
                ('credit_limit', 'FLOAT', '0'),
                ('current_balance', 'FLOAT', '0'),
                ('rating', 'FLOAT', '5.0'),
                ('is_active', 'BOOLEAN', 'TRUE'),
            ],
            'warehouse': [
                ('code', 'VARCHAR(20)', 'NULL'),
                ('address', 'TEXT', 'NULL'),
                ('city', 'VARCHAR(50)', 'NULL'),
                ('manager', 'VARCHAR(100)', 'NULL'),
                ('phone', 'VARCHAR(20)', 'NULL'),
                ('is_active', 'BOOLEAN', 'TRUE'),
            ],
            'warehouse_stock': [
                ('quantity', 'FLOAT', '0'),
                ('reserved_quantity', 'FLOAT', '0'),
                ('available_quantity', 'FLOAT', '0'),
                ('last_updated', 'TIMESTAMP', 'NULL'),
            ],
            'stock_alert': [
                ('product_id', 'INTEGER', 'NULL'),
                ('material_id', 'INTEGER', 'NULL'),
                ('threshold', 'INTEGER', '10000'),
                ('current_stock', 'INTEGER', '0'),
                ('is_resolved', 'BOOLEAN', 'FALSE'),
                ('resolved_at', 'TIMESTAMP', 'NULL'),
            ],
            'painting_service_price': [
                ('product_id', 'INTEGER', 'NULL'),
                ('price_per_unit', 'FLOAT', '0'),
                ('minimum_quantity', 'INTEGER', '1000'),
                ('setup_charge', 'FLOAT', '0'),
                ('is_active', 'BOOLEAN', 'TRUE'),
                ('created_at', 'TIMESTAMP', 'NULL'),
                ('updated_at', 'TIMESTAMP', 'NULL'),
            ],
            'painting_order': [
                ('order_number', 'VARCHAR(50)', 'NULL'),
                ('customer_id', 'INTEGER', 'NULL'),
                ('customer_name', 'VARCHAR(100)', 'NULL'),
                ('customer_phone', 'VARCHAR(20)', 'NULL'),
                ('order_date', 'TIMESTAMP', 'NULL'),
                ('delivery_date', 'TIMESTAMP', 'NULL'),
                ('status', 'VARCHAR(20)', "'pending'"),
                ('total_amount', 'FLOAT', '0'),
                ('paid_amount', 'FLOAT', '0'),
                ('payment_status', 'VARCHAR(20)', "'unpaid'"),
                ('notes', 'TEXT', 'NULL'),
                ('created_by', 'VARCHAR(100)', 'NULL'),
            ],
            'painting_order_item': [
                ('order_id', 'INTEGER', 'NULL'),
                ('product_id', 'INTEGER', 'NULL'),
                ('quantity', 'INTEGER', '0'),
                ('price_per_unit', 'FLOAT', '0'),
                ('setup_charge', 'FLOAT', '0'),
                ('subtotal', 'FLOAT', '0'),
                ('color_specification', 'VARCHAR(100)', 'NULL'),
                ('special_instructions', 'TEXT', 'NULL'),
            ],
            'customer_painting_price': [
                ('customer_id', 'INTEGER', 'NULL'),
                ('product_id', 'INTEGER', 'NULL'),
                ('price_per_unit', 'FLOAT', '0'),
                ('setup_charge', 'FLOAT', '0'),
                ('payment_terms', 'VARCHAR(50)', 'NULL'),
                ('is_active', 'BOOLEAN', 'TRUE'),
                ('created_at', 'TIMESTAMP', 'NULL'),
            ],
            'account': [
                ('account_code', 'VARCHAR(20)', 'NULL'),
                ('account_name', 'VARCHAR(100)', 'NULL'),
                ('account_type', 'VARCHAR(50)', 'NULL'),
                ('parent_account_id', 'INTEGER', 'NULL'),
                ('is_active', 'BOOLEAN', 'TRUE'),
                ('created_at', 'TIMESTAMP', 'NULL'),
            ],
            'journal_entry': [
                ('entry_number', 'VARCHAR(50)', 'NULL'),
                ('entry_date', 'DATE', 'NULL'),
                ('description', 'TEXT', 'NULL'),
                ('reference', 'VARCHAR(100)', 'NULL'),
                ('reference_type', 'VARCHAR(50)', 'NULL'),
                ('reference_id', 'INTEGER', 'NULL'),
                ('status', 'VARCHAR(20)', "'draft'"),
                ('created_by', 'VARCHAR(100)', 'NULL'),
                ('created_at', 'TIMESTAMP', 'NULL'),
                ('posted_by', 'VARCHAR(100)', 'NULL'),
                ('posted_at', 'TIMESTAMP', 'NULL'),
            ],
            'journal_entry_line': [
                ('entry_id', 'INTEGER', 'NULL'),
                ('account_id', 'INTEGER', 'NULL'),
                ('description', 'VARCHAR(200)', 'NULL'),
                ('debit', 'FLOAT', '0'),
                ('credit', 'FLOAT', '0'),
            ],
            'accounting_period': [
                ('period_name', 'VARCHAR(50)', 'NULL'),
                ('start_date', 'DATE', 'NULL'),
                ('end_date', 'DATE', 'NULL'),
                ('is_closed', 'BOOLEAN', 'FALSE'),
                ('closed_by', 'VARCHAR(100)', 'NULL'),
                ('closed_at', 'TIMESTAMP', 'NULL'),
                ('created_at', 'TIMESTAMP', 'NULL'),
            ],
            'bank_account': [
                ('account_name', 'VARCHAR(100)', 'NULL'),
                ('account_number', 'VARCHAR(50)', 'NULL'),
                ('bank_name', 'VARCHAR(100)', 'NULL'),
                ('account_type', 'VARCHAR(50)', "'current'"),
                ('opening_balance', 'FLOAT', '0'),
                ('current_balance', 'FLOAT', '0'),
                ('is_active', 'BOOLEAN', 'TRUE'),
                ('created_at', 'TIMESTAMP', 'NULL'),
            ],
            'payment_voucher': [
                ('voucher_number', 'VARCHAR(50)', 'NULL'),
                ('voucher_date', 'DATE', 'NULL'),
                ('payee_name', 'VARCHAR(100)', 'NULL'),
                ('payee_type', 'VARCHAR(50)', 'NULL'),
                ('payee_id', 'INTEGER', 'NULL'),
                ('payment_method', 'VARCHAR(50)', "'cash'"),
                ('bank_account_id', 'INTEGER', 'NULL'),
                ('cheque_number', 'VARCHAR(50)', 'NULL'),
                ('total_amount', 'FLOAT', '0'),
                ('description', 'TEXT', 'NULL'),
                ('status', 'VARCHAR(20)', "'draft'"),
                ('approved_by', 'VARCHAR(100)', 'NULL'),
                ('paid_by', 'VARCHAR(100)', 'NULL'),
                ('paid_at', 'TIMESTAMP', 'NULL'),
                ('created_by', 'VARCHAR(100)', 'NULL'),
                ('created_at', 'TIMESTAMP', 'NULL'),
            ],
            'payment_voucher_line': [
                ('voucher_id', 'INTEGER', 'NULL'),
                ('account_id', 'INTEGER', 'NULL'),
                ('description', 'VARCHAR(200)', 'NULL'),
                ('amount', 'FLOAT', '0'),
            ],
            'receipt_voucher': [
                ('voucher_number', 'VARCHAR(50)', 'NULL'),
                ('voucher_date', 'DATE', 'NULL'),
                ('payer_name', 'VARCHAR(100)', 'NULL'),
                ('payer_type', 'VARCHAR(50)', 'NULL'),
                ('payer_id', 'INTEGER', 'NULL'),
                ('payment_method', 'VARCHAR(50)', "'cash'"),
                ('bank_account_id', 'INTEGER', 'NULL'),
                ('cheque_number', 'VARCHAR(50)', 'NULL'),
                ('total_amount', 'FLOAT', '0'),
                ('description', 'TEXT', 'NULL'),
                ('status', 'VARCHAR(20)', "'draft'"),
                ('received_by', 'VARCHAR(100)', 'NULL'),
                ('created_by', 'VARCHAR(100)', 'NULL'),
                ('created_at', 'TIMESTAMP', 'NULL'),
            ],
            'receipt_voucher_line': [
                ('voucher_id', 'INTEGER', 'NULL'),
                ('account_id', 'INTEGER', 'NULL'),
                ('description', 'VARCHAR(200)', 'NULL'),
                ('amount', 'FLOAT', '0'),
            ],
            'audit_log': [
                ('table_name', 'VARCHAR(50)', 'NULL'),
                ('record_id', 'INTEGER', 'NULL'),
                ('action', 'VARCHAR(20)', 'NULL'),
                ('old_values', 'TEXT', 'NULL'),
                ('new_values', 'TEXT', 'NULL'),
                ('user_id', 'INTEGER', 'NULL'),
                ('username', 'VARCHAR(100)', 'NULL'),
                ('ip_address', 'VARCHAR(50)', 'NULL'),
                ('timestamp', 'TIMESTAMP', 'NULL'),
            ],
        }
        
        total_added = 0
        total_skipped = 0
        
        for table_name, columns in missing_columns.items():
            print(f"\n📋 Table: {table_name}")
            print("-" * 50)
            
            # Get existing columns for this table
            try:
                existing_columns = [col['name'] for col in inspector.get_columns(table_name)]
            except Exception as e:
                print(f"  ⚠️  Table {table_name} doesn't exist yet - skipping")
                continue
            
            for col_name, col_type, default in columns:
                if col_name not in existing_columns:
                    # Add the column
                    sql = f'ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {col_name} {col_type}'
                    if default != 'NULL':
                        sql += f' DEFAULT {default}'
                    
                    try:
                        db.session.execute(db.text(sql))
                        db.session.commit()
                        print(f"  ✅ Added: {col_name} ({col_type})")
                        total_added += 1
                    except Exception as e:
                        print(f"  ❌ Failed: {col_name} - {str(e)}")
                        db.session.rollback()
                else:
                    print(f"  ⏭️  Exists: {col_name}")
                    total_skipped += 1
        
        print()
        print("="*70)
        print("📊 SUMMARY")
        print("="*70)
        print(f"   Columns Added: {total_added}")
        print(f"   Columns Skipped (already exist): {total_skipped}")
        print()
        
        if total_added > 0:
            print("✅ Database schema updated successfully!")
            print()
            print("📍 Next Steps:")
            print("   1. Restart your Flask app: python run.py")
            print("   2. Test your site: http://127.0.0.1:5000")
            print("   3. All AttributeError errors should be fixed!")
        else:
            print("ℹ️  All columns already exist. No changes needed.")
        
        print()
        print("="*70)

if __name__ == '__main__':
    fix_database()