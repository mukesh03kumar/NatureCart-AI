import os
import shutil
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NatureCart.settings')
django.setup()

from Seller_app.models import Product, ProductImage

def copy_and_bind():
    # Source images are already in media/product_images
    media_dir = os.path.join('media', 'product_images')
    
    image_mappings = [
        {
            'product_name_contains': 'Double-Walled Stainless Steel Water Bottle',
            'image_name': 'stainless_water_bottle.png'
        },
        {
            'product_name_contains': 'Organic Bamboo Toothbrush',
            'image_name': 'bamboo_toothbrush.png'
        },
        {
            'product_name_contains': 'Reusable Shopping Canvas Bags',
            'image_name': 'canvas_shopping_bags.png'
        },
        {
            'product_name_contains': 'Dual-Compartment Kitchen Compost Bin',
            'image_name': 'kitchen_compost_bin.png'
        },
        {
            'product_name_contains': 'Seed Paper Stationery Set',
            'image_name': 'seed_paper_stationery.png'
        }
    ]

    for mapping in image_mappings:
        src_path = os.path.join(media_dir, mapping['image_name'])

        if not os.path.exists(src_path):
            print(f"Image file not found: {src_path}")
            continue

        # Fetch the matching product
        try:
            product = Product.objects.get(name__icontains=mapping['product_name_contains'])
            
            # Clean up existing images first
            product.images.all().delete()

            # Create the binding in the ProductImage table using Django File API
            from django.core.files import File
            with open(src_path, 'rb') as f:
                ProductImage.objects.create(
                    product=product,
                    image=File(f, name=mapping['image_name'])
                )
            print(f"Successfully bound and uploaded image for product: '{product.name}'")

        except Product.DoesNotExist:
            print(f"Product containing '{mapping['product_name_contains']}' not found in database.")
        except Exception as e:
            print(f"Error binding image for {mapping['product_name_contains']}: {e}")

if __name__ == '__main__':
    copy_and_bind()
