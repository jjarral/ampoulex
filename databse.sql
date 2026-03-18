-- ============================================================================
PRAGMA foreign_keys = ON;

-- ============================================================================
-- 1. USER MANAGEMENT
-- ============================================================================

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Default admin user (password: admin123)
INSERT OR IGNORE INTO user (username, email, password_hash, role, is_active) 
VALUES ('admin', 'admin@ampoulex.com', 'scrypt:32768:8:1$abc123$def456', 'admin', 1);

-- ============================================================================
-- 2. CORE ERP - PRODUCTS & CUSTOMERS
-- ============================================================================

CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specification TEXT,
    
    -- Ampoule Dimensions (mm)
    body_diameter REAL,
    overall_length REAL,
    sealing_point REAL,
    body_length REAL,
    stem_diameter REAL,
    wall_thickness REAL,
    
     --ricing (PKR per 1000 ampoules)
    base_price REAL NOT NULL,
    price_per_unit REAL,
    
    -- Stock & Classification
    stock INTEGER DEFAULT 0,
    color TEXT,
    product_type TEXT DEFAULT 'product',
    
    -- Material & Standards
    material_type TEXT,
    usp_type TEXT,
    shape_type TEXT,
    dimensions TEXT,
    use_case TEXT,
    
    -- Painting/White Label Service
    paint_color TEXT,
    paint_type TEXT,
    printing_method TEXT,
    
    -- Status
    is_deleted BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    business_name TEXT,
    role TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    payment_terms TEXT DEFAULT 'cash',
    is_active BOOLEAN DEFAULT 1,
    is_deleted BOOLEAN DEFAULT 0,
    credit_limit REAL DEFAULT 0,
    current_balance REAL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customer_product_price (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    agreed_price REAL NOT NULL,
    payment_terms TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (product_id) REFERENCES product(id),
    UNIQUE(customer_id, product_id)
);

CREATE TABLE IF NOT EXISTS customer_painting_price (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    price_per_unit REAL NOT NULL,
    setup_charge REAL DEFAULT 0,
    payment_terms TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- ============================================================================
-- 3. INQUIRIES & ORDERS
-- ============================================================================

CREATE TABLE IF NOT EXISTS inquiry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inquiry_number TEXT UNIQUE NOT NULL,
    customer_name TEXT NOT NULL,
    business_name TEXT,
    email TEXT,
    phone TEXT,
    product_id INTEGER,
    quantity INTEGER DEFAULT 0,
    status TEXT DEFAULT 'new',
    notes TEXT,
    is_deleted BOOLEAN DEFAULT 0,
    deleted_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS inquiry_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inquiry_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (inquiry_id) REFERENCES inquiry(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS `order` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,
    customer_id INTEGER,
    inquiry_id INTEGER,
    total_amount REAL NOT NULL,
    tax_amount REAL DEFAULT 0,
    status TEXT DEFAULT 'pending',
    payment_status TEXT DEFAULT 'unpaid',
    payment_method TEXT,
    paid_amount REAL DEFAULT 0,
    payment_date DATETIME,
    customer_name_snapshot TEXT,
    customer_business_snapshot TEXT,
    customer_phone_snapshot TEXT,
    customer_email_snapshot TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (inquiry_id) REFERENCES inquiry(id)
);

CREATE TABLE IF NOT EXISTS order_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `order`(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS order_approval (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    requested_by TEXT,
    approved_by TEXT,
    approved_at DATETIME,
    rejection_reason TEXT,
    status TEXT DEFAULT 'pending',
    approval_threshold REAL,
    FOREIGN KEY (order_id) REFERENCES `order`(id)
);

-- ============================================================================
-- 4. PAYROLL & EMPLOYEES
-- ============================================================================

CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT,
    department TEXT,
    email TEXT,
    phone TEXT,
    cnic TEXT,
    address TEXT,
    emergency_contact TEXT,
    emergency_phone TEXT,
    base_salary REAL NOT NULL,
    payment_frequency TEXT DEFAULT 'monthly',
    bank_account TEXT,
    bank_name TEXT,
    outstanding_loan REAL DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status TEXT DEFAULT 'present',
    check_in TIME,
    check_out TIME,
    hours_worked REAL,
    overtime_hours REAL,
    notes TEXT,
    is_approved BOOLEAN DEFAULT 0,
    FOREIGN KEY (employee_id) REFERENCES employee(id),
    UNIQUE(employee_id, date)
);

CREATE TABLE IF NOT EXISTS timesheet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    period_type TEXT DEFAULT 'weekly',
    regular_hours REAL,
    overtime_hours REAL,
    total_hours REAL,
    leave_days REAL,
    sick_days REAL,
    absent_days REAL,
    hourly_rate REAL,
    overtime_rate REAL,
    regular_pay REAL,
    overtime_pay REAL,
    deductions REAL DEFAULT 0,
    net_pay REAL,
    status TEXT DEFAULT 'draft',
    approved_by TEXT,
    approved_at DATETIME,
    paid_at DATETIME,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employee(id)
);

CREATE TABLE IF NOT EXISTS leave_request (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    leave_type TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_days INTEGER,
    reason TEXT,
    status TEXT DEFAULT 'pending',
    approved_by TEXT,
    approved_at DATETIME,
    rejection_reason TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employee(id)
);

CREATE TABLE IF NOT EXISTS payroll_payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    timesheet_id INTEGER,
    period_start DATE,
    period_end DATE,
    base_salary REAL,
    hourly_wages REAL,
    overtime_pay REAL,
    bonuses REAL DEFAULT 0,
    allowances REAL DEFAULT 0,
    total_earnings REAL,
    income_tax REAL,
    loan_deduction REAL,
    other_deductions REAL,
    total_deductions REAL,
    net_pay REAL,
    payment_method TEXT,
    payment_date DATE,
    bank_name TEXT,
    bank_account TEXT,
    status TEXT DEFAULT 'draft',
    processed_by TEXT,
    processed_at DATETIME,
    FOREIGN KEY (employee_id) REFERENCES employee(id),
    FOREIGN KEY (timesheet_id) REFERENCES timesheet(id)
);

-- ============================================================================
-- 5. EXPENSES & ACCOUNTING
-- ============================================================================

CREATE TABLE IF NOT EXISTS expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL,
    date DATE NOT NULL,
    status TEXT DEFAULT 'pending',
    paid_by TEXT,
    payment_method TEXT,
    reference_number TEXT,
    approved_by TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS accounting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_type TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    reference_type TEXT,
    reference_id INTEGER,
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT
);

CREATE TABLE IF NOT EXISTS tax_setting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tax_name TEXT NOT NULL,
    tax_rate REAL NOT NULL,
    is_active BOOLEAN DEFAULT 1
);

-- ============================================================================
-- 6. MANUFACTURING & PRODUCTION
-- ============================================================================

CREATE TABLE IF NOT EXISTS raw_material (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    material_type TEXT,
    specification TEXT,
    current_stock REAL DEFAULT 0,
    unit TEXT,
    reorder_level REAL DEFAULT 0,
    cost_per_unit REAL,
    supplier TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bom_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    raw_material_id INTEGER NOT NULL,
    quantity_required REAL NOT NULL,
    unit TEXT,
    waste_percentage REAL DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (raw_material_id) REFERENCES raw_material(id)
);

CREATE TABLE IF NOT EXISTS production_batch (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_number TEXT UNIQUE NOT NULL,
    product_id INTEGER NOT NULL,
    planned_quantity INTEGER NOT NULL,
    actual_quantity INTEGER,
    rejected_quantity INTEGER,
    yield_percentage REAL,
    status TEXT DEFAULT 'planned',
    start_date DATETIME,
    end_date DATETIME,
    created_by TEXT,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS material_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER NOT NULL,
    batch_id INTEGER,
    quantity_used REAL NOT NULL,
    unit TEXT,
    usage_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    used_by TEXT,
    notes TEXT,
    FOREIGN KEY (material_id) REFERENCES raw_material(id),
    FOREIGN KEY (batch_id) REFERENCES production_batch(id)
);

CREATE TABLE IF NOT EXISTS batch_raw_material (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER NOT NULL,
    material_name TEXT,
    material_type TEXT,
    quantity_used REAL,
    unit TEXT,
    cost_per_unit REAL,
    total_cost REAL,
    supplier TEXT,
    batch_code TEXT,
    FOREIGN KEY (batch_id) REFERENCES production_batch(id)
);

-- ============================================================================
-- 7. SUPPLY CHAIN
-- ============================================================================

CREATE TABLE IF NOT EXISTS supplier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_person TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    city TEXT,
    country TEXT DEFAULT 'Pakistan',
    cnic TEXT,
    ntn TEXT,
    payment_terms TEXT DEFAULT '30 days',
    credit_limit REAL DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS purchase_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    po_number TEXT UNIQUE NOT NULL,
    supplier_id INTEGER NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    expected_date DATETIME,
    received_date DATETIME,
    status TEXT DEFAULT 'draft',
    total_amount REAL DEFAULT 0,
    tax_amount REAL DEFAULT 0,
    grand_total REAL DEFAULT 0,
    payment_status TEXT DEFAULT 'unpaid',
    paid_amount REAL DEFAULT 0,
    notes TEXT,
    created_by TEXT,
    approved_by TEXT,
    approved_at DATETIME,
    FOREIGN KEY (supplier_id) REFERENCES supplier(id)
);

CREATE TABLE IF NOT EXISTS purchase_order_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    po_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity_ordered REAL NOT NULL,
    quantity_received REAL DEFAULT 0,
    unit_price REAL NOT NULL,
    subtotal REAL NOT NULL,
    tax_rate REAL DEFAULT 17,
    tax_amount REAL,
    total REAL,
    FOREIGN KEY (po_id) REFERENCES purchase_order(id),
    FOREIGN KEY (material_id) REFERENCES raw_material(id)
);

CREATE TABLE IF NOT EXISTS goods_receipt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grn_number TEXT UNIQUE NOT NULL,
    po_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    warehouse_id INTEGER,
    receipt_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    total_items INTEGER DEFAULT 0,
    accepted_items INTEGER DEFAULT 0,
    rejected_items INTEGER DEFAULT 0,
    received_by TEXT,
    FOREIGN KEY (po_id) REFERENCES purchase_order(id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(id)
);

CREATE TABLE IF NOT EXISTS goods_receipt_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gr_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity_ordered REAL,
    quantity_received REAL,
    quantity_accepted REAL,
    quantity_rejected REAL,
    rejection_reason TEXT,
    batch_number TEXT,
    expiry_date DATETIME,
    FOREIGN KEY (gr_id) REFERENCES goods_receipt(id),
    FOREIGN KEY (material_id) REFERENCES raw_material(id)
);

CREATE TABLE IF NOT EXISTS warehouse (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT UNIQUE,
    address TEXT,
    city TEXT,
    manager TEXT,
    phone TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS warehouse_stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    warehouse_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity REAL DEFAULT 0,
    available_quantity REAL DEFAULT 0,
    reserved_quantity REAL DEFAULT 0,
    FOREIGN KEY (warehouse_id) REFERENCES warehouse(id),
    FOREIGN KEY (material_id) REFERENCES raw_material(id),
    UNIQUE(warehouse_id, material_id)
);

CREATE TABLE IF NOT EXISTS stock_transfer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transfer_number TEXT UNIQUE NOT NULL,
    from_warehouse_id INTEGER NOT NULL,
    to_warehouse_id INTEGER NOT NULL,
    transfer_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    notes TEXT,
    requested_by TEXT,
    completed_at DATETIME,
    FOREIGN KEY (from_warehouse_id) REFERENCES warehouse(id),
    FOREIGN KEY (to_warehouse_id) REFERENCES warehouse(id)
);

CREATE TABLE IF NOT EXISTS stock_transfer_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transfer_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    quantity_transferred REAL DEFAULT 0,
    FOREIGN KEY (transfer_id) REFERENCES stock_transfer(id),
    FOREIGN KEY (material_id) REFERENCES raw_material(id)
);

CREATE TABLE IF NOT EXISTS material_batch (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER NOT NULL,
    batch_number TEXT,
    supplier_id INTEGER,
    quantity_received REAL,
    quantity_remaining REAL,
    expiry_date DATETIME,
    warehouse_id INTEGER,
    received_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active',
    FOREIGN KEY (material_id) REFERENCES raw_material(id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouse(id)
);

CREATE TABLE IF NOT EXISTS supplier_invoice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT NOT NULL,
    supplier_id INTEGER NOT NULL,
    po_id INTEGER,
    invoice_date DATETIME NOT NULL,
    due_date DATETIME,
    total_amount REAL NOT NULL,
    balance_amount REAL,
    status TEXT DEFAULT 'unpaid',
    paid_amount REAL DEFAULT 0,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES supplier(id),
    FOREIGN KEY (po_id) REFERENCES purchase_order(id)
);

-- ============================================================================
-- 8. INVENTORY MANAGEMENT
-- ============================================================================

CREATE TABLE IF NOT EXISTS stock_adjustment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    material_id INTEGER,
    adjustment_type TEXT NOT NULL,
    quantity REAL NOT NULL,
    reason TEXT,
    adjusted_by TEXT,
    adjusted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (material_id) REFERENCES raw_material(id)
);

CREATE TABLE IF NOT EXISTS stock_alert (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    threshold INTEGER NOT NULL,
    current_stock INTEGER NOT NULL,
    is_resolved BOOLEAN DEFAULT 0,
    resolved_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS stock_movement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER NOT NULL,
    product_id INTEGER,
    movement_type TEXT NOT NULL,
    quantity REAL NOT NULL,
    reference_type TEXT,
    reference_id INTEGER,
    movement_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    created_by TEXT,
    FOREIGN KEY (material_id) REFERENCES raw_material(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS inventory_adjustment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    adjustment_number TEXT UNIQUE NOT NULL,
    material_id INTEGER,
    product_id INTEGER,
    adjustment_type TEXT NOT NULL,
    quantity REAL NOT NULL,
    reason TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    requested_by TEXT,
    requested_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    approved_by TEXT,
    approved_date DATETIME,
    FOREIGN KEY (material_id) REFERENCES raw_material(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS stock_count (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    count_number TEXT UNIQUE NOT NULL,
    count_date DATE NOT NULL,
    warehouse_id INTEGER,
    status TEXT DEFAULT 'in_progress',
    counted_by TEXT,
    verified_by TEXT,
    notes TEXT,
    FOREIGN KEY (warehouse_id) REFERENCES warehouse(id)
);

CREATE TABLE IF NOT EXISTS stock_count_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    count_id INTEGER NOT NULL,
    material_id INTEGER,
    product_id INTEGER,
    system_quantity REAL NOT NULL,
    counted_quantity REAL NOT NULL,
    variance REAL,
    variance_reason TEXT,
    FOREIGN KEY (count_id) REFERENCES stock_count(id),
    FOREIGN KEY (material_id) REFERENCES raw_material(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- ============================================================================
-- 9. QUALITY MANAGEMENT
-- ============================================================================

CREATE TABLE IF NOT EXISTS qc_parameter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    parameter_name TEXT NOT NULL,
    min_value REAL,
    max_value REAL,
    target_value REAL,
    unit TEXT,
    test_method TEXT,
    is_mandatory BOOLEAN DEFAULT 1,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS qc_result (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER NOT NULL,
    parameter_id INTEGER NOT NULL,
    test_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    tested_value REAL,
    result TEXT NOT NULL,
    tested_by TEXT,
    remarks TEXT,
    FOREIGN KEY (batch_id) REFERENCES production_batch(id),
    FOREIGN KEY (parameter_id) REFERENCES qc_parameter(id)
);

CREATE TABLE IF NOT EXISTS customer_complaint (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_number TEXT UNIQUE NOT NULL,
    customer_id INTEGER,
    customer_name TEXT,
    order_id INTEGER,
    product_id INTEGER,
    batch_number TEXT,
    complaint_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    complaint_type TEXT,
    description TEXT NOT NULL,
    severity TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'open',
    assigned_to TEXT,
    investigation_notes TEXT,
    resolution TEXT,
    resolved_date DATETIME,
    resolved_by TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (order_id) REFERENCES `order`(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS capa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    capa_number TEXT UNIQUE NOT NULL,
    complaint_id INTEGER,
    type TEXT NOT NULL,
    root_cause TEXT,
    action_plan TEXT NOT NULL,
    assigned_to TEXT,
    due_date DATE,
    status TEXT DEFAULT 'open',
    completion_date DATETIME,
    effectiveness_check TEXT,
    closed_by TEXT,
    closed_date DATETIME,
    FOREIGN KEY (complaint_id) REFERENCES customer_complaint(id)
);

CREATE TABLE IF NOT EXISTS calibration_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_name TEXT NOT NULL,
    equipment_id TEXT,
    calibration_date DATE NOT NULL,
    next_due_date DATE NOT NULL,
    calibration_result TEXT NOT NULL,
    calibrated_by TEXT,
    certificate_number TEXT,
    remarks TEXT,
    is_active BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS quality_check (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER NOT NULL,
    check_type TEXT,
    check_result TEXT,
    checked_quantity INTEGER,
    passed_quantity INTEGER,
    failed_quantity INTEGER,
    failure_reason TEXT,
    checked_by TEXT,
    notes TEXT,
    checked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (batch_id) REFERENCES production_batch(id)
);

-- ============================================================================
-- 10. PAINTING SERVICE
-- ============================================================================

CREATE TABLE IF NOT EXISTS painting_service_price (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    price_per_unit REAL NOT NULL,
    minimum_quantity INTEGER DEFAULT 1000,
    setup_charge REAL DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS painting_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,
    customer_id INTEGER,
    customer_name TEXT,
    customer_phone TEXT,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    delivery_date DATETIME,
    status TEXT DEFAULT 'pending',
    total_amount REAL DEFAULT 0,
    paid_amount REAL DEFAULT 0,
    payment_status TEXT DEFAULT 'unpaid',
    notes TEXT,
    created_by TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(id)
);

CREATE TABLE IF NOT EXISTS painting_order_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_per_unit REAL NOT NULL,
    setup_charge REAL DEFAULT 0,
    subtotal REAL DEFAULT 0,
    color_specification TEXT,
    special_instructions TEXT,
    FOREIGN KEY (order_id) REFERENCES painting_order(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- ============================================================================
-- 11. REPORTS & SETTINGS
-- ============================================================================

CREATE TABLE IF NOT EXISTS report (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_type TEXT NOT NULL,
    module TEXT NOT NULL,
    generated_by TEXT NOT NULL,
    parameters TEXT,
    file_path TEXT,
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS company_setting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 12. FBR TAX INTEGRATION
-- ============================================================================

CREATE TABLE IF NOT EXISTS fbr_invoice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    invoice_number TEXT UNIQUE NOT NULL,
    fbr_invoice_number TEXT,
    invoice_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL NOT NULL,
    taxable_amount REAL NOT NULL,
    gst_amount REAL NOT NULL,
    withholding_tax REAL DEFAULT 0,
    status TEXT DEFAULT 'generated',
    submitted_date DATETIME,
    verified_date DATETIME,
    FOREIGN KEY (order_id) REFERENCES `order`(id)
);

CREATE TABLE IF NOT EXISTS tax_return (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    return_period TEXT NOT NULL,
    sales_tax REAL DEFAULT 0,
    input_tax REAL DEFAULT 0,
    net_tax_payable REAL DEFAULT 0,
    withholding_tax REAL DEFAULT 0,
    status TEXT DEFAULT 'draft',
    filed_date DATE,
    payment_date DATE,
    remarks TEXT
);

-- ============================================================================
-- 13. INDEXES FOR PERFORMANCE
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_product_name ON product(name);
CREATE INDEX IF NOT EXISTS idx_product_color ON product(color);
CREATE INDEX IF NOT EXISTS idx_product_type ON product(product_type);
CREATE INDEX IF NOT EXISTS idx_product_stock ON product(stock);

CREATE INDEX IF NOT EXISTS idx_order_customer ON `order`(customer_id);
CREATE INDEX IF NOT EXISTS idx_order_status ON `order`(status);
CREATE INDEX IF NOT EXISTS idx_order_created ON `order`(created_at);

CREATE INDEX IF NOT EXISTS idx_inquiry_customer ON inquiry(customer_name);
CREATE INDEX IF NOT EXISTS idx_inquiry_status ON inquiry(status);

CREATE INDEX IF NOT EXISTS idx_customer_email ON customer(email);
CREATE INDEX IF NOT EXISTS idx_customer_phone ON customer(phone);

CREATE INDEX IF NOT EXISTS idx_purchase_order_supplier ON purchase_order(supplier_id);
CREATE INDEX IF NOT EXISTS idx_purchase_order_status ON purchase_order(status);

CREATE INDEX IF NOT EXISTS idx_production_batch_product ON production_batch(product_id);
CREATE INDEX IF NOT EXISTS idx_production_batch_status ON production_batch(status);

CREATE INDEX IF NOT EXISTS idx_employee_name ON employee(name);
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date);

-- ============================================================================
-- 14. DEFAULT DATA
-- ============================================================================

-- Default tax settings
INSERT OR IGNORE INTO tax_setting (tax_name, tax_rate, is_active) VALUES ('GST', 17, 1);
INSERT OR IGNORE INTO tax_setting (tax_name, tax_rate, is_active) VALUES ('Withholding Tax', 5, 1);

-- Default company settings
INSERT OR IGNORE INTO company_setting (key, value) VALUES ('company_name', 'AmpouleX (Pvt) Ltd');
INSERT OR IGNORE INTO company_setting (key, value) VALUES ('company_address', 'Malik Arshad Farmhouse, Malik Akram Street, Darbar-e-Kareemi Stop, G.T. Road, Wah Cantt');
INSERT OR IGNORE INTO company_setting (key, value) VALUES ('company_phone', '0340-5336238');
INSERT OR IGNORE INTO company_setting (key, value) VALUES ('company_email', 'ampoulex.hr@gmail.com');
