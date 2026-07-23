import os
import shutil

def copy_images():
    artifact_dir = r"C:\Users\Dell\.gemini\antigravity\brain\be452f79-330a-4fa4-9f6a-124fdac72d05"
    media_dest_dir = os.path.join('media', 'about_images')

    if not os.path.exists(media_dest_dir):
        os.makedirs(media_dest_dir)
        print(f"Created directory: {media_dest_dir}")

    mappings = [
        ('soy_candles_1784741912098.png', 'soy_candles.png'),
        ('secure_payment_1784741929311.png', 'secure_payment.png'),
        ('eco_products_group_1784741944494.png', 'eco_products_group.png')
    ]

    for src_name, dest_name in mappings:
        src_path = os.path.join(artifact_dir, src_name)
        dest_path = os.path.join(media_dest_dir, dest_name)

        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Copied {src_name} to {dest_path}")
        else:
            print(f"Source file not found: {src_path}")

if __name__ == '__main__':
    copy_images()
