import os
import django

# Set up Django environment settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NatureCart.settings')
django.setup()

from django.contrib.auth.models import User
from Customer_app.models import UserProfile, PlasticAlternative
from Seller_app.models import Product

def seed_database():
    print("Starting database seeding...")

    # 0. Create Default Admin/Superuser
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@naturecart.com'}
    )
    admin_user.set_password('admin123')
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()
    print("Ensured Superuser account exists (username: admin, password: admin123)")

    # 1. Create Default Seller
    seller_user, created = User.objects.get_or_create(
        username='seller',
        defaults={'email': 'seller@naturecart.com'}
    )
    seller_user.set_password('naturecart123')
    seller_user.first_name = 'Eco'
    seller_user.last_name = 'Merchant'
    seller_user.save()
    
    # Ensure profile exists
    UserProfile.objects.get_or_create(
        user=seller_user,
        defaults={
            'phone': '+91 99999 88888',
            'address': 'NatureCart Green Warehouse, Sector 15, Bangalore',
            'role': 'Seller'
        }
    )
    print("Ensured Seller account exists (username: seller, password: naturecart123)")

    # 2. Create Default Customer
    customer_user, created = User.objects.get_or_create(
        username='customer',
        defaults={'email': 'customer@naturecart.com'}
    )
    customer_user.set_password('naturecart123')
    customer_user.first_name = 'Jane'
    customer_user.last_name = 'EcoShopper'
    customer_user.save()
    
    # Ensure profile exists
    UserProfile.objects.get_or_create(
        user=customer_user,
        defaults={
            'phone': '+91 77777 66666',
            'address': 'Flat 402, Green Meadows Apartment, Chennai',
            'role': 'Customer',
            'preference': 'Zero-Waste'
        }
    )
    print("Ensured Customer account exists (username: customer, password: naturecart123)")

    # 3. Seed Products (the 10 requested items)
    products_data = [
        {
            'name': 'Reusable Shopping Canvas Bags (Pack of 3)',
            'category': 'Bags',
            'description': 'Sturdy, 100% organic cotton canvas bags perfect for grocery shopping. Designed to replace single-use plastic grocery bags. Washable and fully biodegradable.',
            'price': 149.00,
            'stock': 40,
            'plastic_saving_weight': 0.15,
            'co2_saving_weight': 0.35,
            'is_premium': False
        },
        {
            'name': 'Organic Bamboo Toothbrush (Set of 4)',
            'category': 'Dental',
            'description': 'Biodegradable bamboo handle with charcoal-infused soft bristles. Offers antimicrobial benefits while ensuring plastic toothbrushes stay out of landfills.',
            'price': 79.00,
            'stock': 60,
            'plastic_saving_weight': 0.08,
            'co2_saving_weight': 0.15,
            'is_premium': False
        },
        {
            'name': 'Double-Walled Stainless Steel Water Bottle (750ml)',
            'category': 'Hydration',
            'description': 'Premium food-grade 18/8 stainless steel bottle. Keeps drinks cold for 24 hours or hot for 12 hours. Sleek design, replaces hundreds of plastic bottles.',
            'price': 499.00,
            'stock': 25,
            'plastic_saving_weight': 0.50,
            'co2_saving_weight': 1.20,
            'is_premium': False
        },
        {
            'name': 'Reusable Stainless Steel Straws (Pack of 4 + Brush)',
            'category': 'Hydration',
            'description': 'Food-grade steel straws with rounded tips. Package includes a cotton cleaning brush and carry case. Fully dishwasher-safe and durable.',
            'price': 119.00,
            'stock': 50,
            'plastic_saving_weight': 0.10,
            'co2_saving_weight': 0.22,
            'is_premium': False
        },
        {
            'name': 'Dual-Compartment Kitchen Compost Bin',
            'category': 'Composting',
            'description': 'Odor-free indoor composting bin equipped with dual carbon filters. Perfect for converting vegetable scraps and coffee grounds into rich soil food.',
            'price': 849.00,
            'stock': 15,
            'plastic_saving_weight': 1.50,
            'co2_saving_weight': 4.20,
            'is_premium': False
        },
        {
            'name': 'Zero-Chemical Natural Cleaning Kit',
            'category': 'Cleaning',
            'description': 'Plant-based cleaning solutions including multi-purpose spray, dishwashing liquid, and floor cleaner. Fully biodegradable formulas, non-toxic to aquatic systems.',
            'price': 349.00,
            'stock': 30,
            'plastic_saving_weight': 0.40,
            'co2_saving_weight': 0.85,
            'is_premium': False
        },
        {
            'name': 'Eco-Friendly Bamboo Fibre Lunch Box',
            'category': 'Composting',
            'description': 'Made of natural organic bamboo fibre with a secure silicone band. Microwave and dishwasher safe, completely BPA-free and compostable.',
            'price': 299.00,
            'stock': 20,
            'plastic_saving_weight': 0.25,
            'co2_saving_weight': 0.60,
            'is_premium': False
        },
        {
            'name': 'Seed Paper Stationery Set (Notebook & 5 Pencils)',
            'category': 'Stationery',
            'description': 'Handcrafted notebook containing recycled paper embedded with wildflower seeds. The pencils contain seeds in their caps. Plant them when finished to grow plants!',
            'price': 179.00,
            'stock': 35,
            'plastic_saving_weight': 0.12,
            'co2_saving_weight': 0.40,
            'is_premium': True
        },
        {
            'name': 'Hand-Poured Soy Wax Scented Candles (Set of 2)',
            'category': 'Home',
            'description': 'Made from 100% natural soybean wax, infused with organic lavender and vanilla essential oils. Lead-free cotton wicks, burns cleanly without paraffin soot.',
            'price': 239.00,
            'stock': 30,
            'plastic_saving_weight': 0.05,
            'co2_saving_weight': 0.30,
            'is_premium': False
        },
        {
            'name': 'Home Composting Accessories & Aerator',
            'category': 'Composting',
            'description': 'Compost aerator tool and bio-activator powder. Speeds up composting rates and ensures optimal oxygen supply in your compost heaps.',
            'price': 149.00,
            'stock': 25,
            'plastic_saving_weight': 0.10,
            'co2_saving_weight': 0.28,
            'is_premium': True
        }
    ]

    seeded_products = {}
    for p_data in products_data:
        prod, created = Product.objects.get_or_create(
            name=p_data['name'],
            defaults={
                'seller': seller_user,
                'category': p_data['category'],
                'description': p_data['description'],
                'price': p_data['price'],
                'stock': p_data['stock'],
                'plastic_saving_weight': p_data['plastic_saving_weight'],
                'co2_saving_weight': p_data['co2_saving_weight'],
                'is_premium': p_data['is_premium']
            }
        )
        seeded_products[p_data['category']] = prod
        if created:
            print(f"Seeded product: {prod.name}")
        else:
            print(f"Product '{prod.name}' already exists.")

    # 4. Seed Plastic Alternatives Finder Mapping
    alternatives_data = [
        {
            'plastic': 'Plastic Shopping Bags',
            'alt_category': 'Bags',
            'co2': 0.35,
            'plastic_save': 0.15,
            'reason': 'Traditional plastic bags disintegrate into microplastics, blocking waterways and entering ecosystems. Cotton canvas bags can be washed and reused for years.'
        },
        {
            'plastic': 'Plastic Toothbrush',
            'alt_category': 'Dental',
            'co2': 0.15,
            'plastic_save': 0.08,
            'reason': 'Over 1 billion plastic toothbrushes are discarded annually. Our bamboo toothbrush handle is compostable and returns to the soil in less than 6 months.'
        },
        {
            'plastic': 'Plastic Water Bottle',
            'alt_category': 'Hydration',
            'co2': 1.20,
            'plastic_save': 0.50,
            'reason': 'Single-use bottles represent a huge percentage of municipal waste. A food-grade stainless steel bottle is durable and keeps water fresh indefinitely.'
        },
        {
            'plastic': 'Disposable Plastic Straws',
            'alt_category': 'Hydration',
            'co2': 0.22,
            'plastic_save': 0.10,
            'reason': 'Plastic straws clog marine animals airways and are too small to be recycled easily. Stainless steel straws are infinitely washable and safe.'
        },
        {
            'plastic': 'Traditional Trash Can',
            'alt_category': 'Composting',
            'co2': 4.20,
            'plastic_save': 1.50,
            'reason': 'Dumping organic waste in plastic bags causes anaerobic rotting, which releases methane. Kitchen compost bins route waste to organic composting.'
        },
        {
            'plastic': 'Chemical Detergent Bottles',
            'alt_category': 'Cleaning',
            'co2': 0.85,
            'plastic_save': 0.40,
            'reason': 'Regular detergents contain synthetic sulfates that poison water tables. Natural plant-based cleaning solutions are non-toxic and biodegradable.'
        },
        {
            'plastic': 'Plastic Lunch Box',
            'alt_category': 'Composting',
            'co2': 0.60,
            'plastic_save': 0.25,
            'reason': 'Heated plastics can leach microplastics and phthalates into hot food. Bamboo fibre boxes are chemical-free, food-safe, and biodegradable.'
        },
        {
            'plastic': 'Wood Pulp Paper Notebooks',
            'alt_category': 'Stationery',
            'co2': 0.40,
            'plastic_save': 0.12,
            'reason': 'Standard notebooks require tree logging and chemical bleaching. Seed paper notebooks are crafted from waste cotton and grow into flowers when planted.'
        },
        {
            'plastic': 'Paraffin Wax Candles',
            'alt_category': 'Home',
            'co2': 0.30,
            'plastic_save': 0.05,
            'reason': 'Paraffin is a petroleum refining byproduct that emits black soot when burned. Soy wax is clean-burning, vegetable-sourced, and carbon neutral.'
        }
    ]

    for alt in alternatives_data:
        associated_product = seeded_products.get(alt['alt_category'])
        if associated_product:
            alt_obj, created = PlasticAlternative.objects.get_or_create(
                plastic_product_name=alt['plastic'],
                defaults={
                    'alternative_product': associated_product,
                    'co2_savings': alt['co2'],
                    'plastic_savings': alt['plastic_save'],
                    'reasoning': alt['reason']
                }
            )
            if created:
                print(f"Seeded Alternative mapping: {alt_obj.plastic_product_name} -> {associated_product.name}")
            else:
                print(f"Alternative mapping for '{alt_obj.plastic_product_name}' already exists.")

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
