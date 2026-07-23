import os
import shutil
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NatureCart.settings')
django.setup()

from Seller_app.models import Product, ProductImage

def copy_and_bind():
    # Define source images in artifact directory
    artifact_dir = r"C:\Users\Dell\.gemini\antigravity\brain\be452f79-330a-4fa4-9f6a-124fdac72d05"
    
    image_mappings = [
        {
            'product_name_contains': 'Double-Walled Stainless Steel Water Bottle',
            'src_file': 'stainless_water_bottle_1784741447941.png',
            'dest_name': 'stainless_water_bottle.png'
        },
        {
            'product_name_contains': 'Organic Bamboo Toothbrush',
            'src_file': 'bamboo_toothbrush_1784741461935.png',
            'dest_name': 'bamboo_toothbrush.png'
        },
        {
            'product_name_contains': 'Reusable Shopping Canvas Bags',
            'src_file': 'canvas_shopping_bags_1784741474615.png',
            'dest_name': 'canvas_shopping_bags.png'
        },
        {
            'product_name_contains': 'Dual-Compartment Kitchen Compost Bin',
            'src_file': 'kitchen_compost_bin_1784741487346.png',
            'dest_name': 'kitchen_compost_bin.png'
        },
        {
            'product_name_contains': 'Seed Paper Stationery Set',
            'src_file': 'seed_paper_stationery_1784741504691.png',
            'dest_name': 'seed_paper_stationery.png'
        }
    ]

    # Create destination directory in media root if it doesn't exist
    media_dest_dir = os.path.join('media', 'product_images')
    if not os.path.exists(media_dest_dir):
        os.makedirs(media_dest_dir)
        print(f"Created directory: {media_dest_dir}")

    for mapping in image_mappings:
        src_path = os.path.join(artifact_dir, mapping['src_file'])
        dest_path = os.path.join(media_dest_dir, mapping['dest_name'])

        if not os.path.exists(src_path):
            print(f"Source file not found: {src_path}")
            continue

        # Copy the image file to the media folder
        shutil.copy2(src_path, dest_path)
        print(f"Copied {mapping['src_file']} to {dest_path}")

        # Fetch the matching product
        try:
            product = Product.objects.get(name__icontains=mapping['product_name_contains'])
            
            # Clean up existing images first
            product.images.all().delete()

            # Create the binding in the ProductImage table
            relative_image_path = f"product_images/{mapping['dest_name']}"
            ProductImage.objects.create(
                product=product,
                image=relative_image_path
            )
            print(f"Successfully bound image to product: '{product.name}'")

        except Product.DoesNotExist:
            print(f"Product containing '{mapping['product_name_contains']}' not found in database.")
        except Exception as e:
            print(f"Error binding image for {mapping['product_name_contains']}: {e}")

if __name__ == '__main__':
    copy_and_bind()
