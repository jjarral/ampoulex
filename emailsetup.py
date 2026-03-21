# emailsetup.py - Sample product creation
from app import create_app, db
from app.models import Product

app = create_app()
with app.app_context():
    # Check if sample product already exists
    if not Product.query.filter_by(name="5cc Amber Ampoule").first():
        product = Product(
            name="5cc Amber Ampoule",
            base_name="Ampoule",      # ✅ Now exists
            volume_cc=5.0,            # ✅ Now exists
            glass_type="Amber",       # ✅ Now exists
            neck_finish="Crimp",      # ✅ Now exists
            unit_price=0.15,
            is_active=True
        )
        db.session.add(product)
        db.session.commit()
        print("✅ Sample product created!")