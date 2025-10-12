import os
import shutil
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "matcher.settings")
django.setup()

from api.models import Product

DATASET_DIR = r"C:\E\productDataset"
TARGET_DIR = r"C:\E\visual-product-matcher\backend\media\products"

os.makedirs(TARGET_DIR, exist_ok=True)

for category_name in os.listdir(DATASET_DIR):
    category_path = os.path.join(DATASET_DIR, category_name)
    if os.path.isdir(category_path):
        for img_file in os.listdir(category_path):
            src_img_path = os.path.join(category_path, img_file)
            dest_img_path = os.path.join(TARGET_DIR, img_file)

            shutil.copy(src_img_path, dest_img_path)

            Product.objects.create(
                name=os.path.splitext(img_file)[0], 
                category=category_name,
                image=f"products/{img_file}" 
            )

print("DB populated")
