# Ampoulex Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite with pytest fixtures
- CONTRIBUTING.md with development guidelines
- Enhanced .env.example with detailed configuration options
- Test directory structure with authentication and product tests

### Changed
- Updated README.md with accurate technology stack information
- Improved documentation for deployment options

### Fixed
- Documentation inconsistencies between README and actual tech stack

## [1.0.0] - 2024-01-01

### Added
- Complete ERP system for ampoule manufacturing
- User authentication with role-based access control
- Product management with BOM (Bill of Materials)
- Order management system
- Customer relationship management
- Supplier management
- Purchase order system
- Inventory management with warehouses
- Stock transfers between warehouses
- Production batch tracking
- Quality Control (QC) module
- Accounting module with:
  - Chart of accounts
  - Journal entries
  - General ledger
  - Trial balance
  - Payment vouchers
  - Receipt vouchers
  - Bank reconciliation
  - Audit log
  - Accounting periods
- Financial reporting:
  - Profit & Loss
  - Balance Sheet
  - Cash Flow
- HR & Payroll module:
  - Employee management
  - Attendance tracking
  - Timesheets
  - Leave requests
  - Payroll payments
- Expense tracking
- Fixed asset management
- Tax/FBR integration
- Painting service module
- Real-time updates with Socket.IO
- Dashboard with analytics
- Report generation (PDF, Excel)
- Barcode and QR code generation
- Email notifications
- Mobile-responsive UI with AdminLTE theme
- Docker support
- Database migrations with Alembic

### Technical Features
- Flask backend with SQLAlchemy ORM
- PostgreSQL database
- Jinja2 templating
- Bootstrap 5 frontend
- DataTables for data tables
- Chart.js for visualizations
- SweetAlert2 for notifications
- Select2 for dropdowns

### Security
- Password hashing with Werkzeug
- Session management
- Account lockout after failed attempts
- CSRF protection
- SQL injection prevention
- XSS protection

---

## Legend
- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security improvements
