import os
import urllib.request

IMAGE_DIR = "C:/Users/LENOVO/Desktop/expiry_project/presentation_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Curated, authentic, high-quality Unsplash photos
PHOTOS = {
    "slide1_supermarket.jpg": "https://images.unsplash.com/photo-1542838132-92c53300491e?w=800&q=80",  # Clean modern grocery produce
    "slide2_food_waste.jpg": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800&q=80",   # Food waste / discarded produce
    "slide3_tablet_worker.jpg": "https://images.unsplash.com/photo-1580913428706-c311e67898b3?w=800&q=80",# Supermarket worker with tablet
    "slide6_data_analytics.jpg": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80",# Laptop with data charts
    "slide7_price_tag.jpg": "https://images.unsplash.com/photo-1555529771-835f59fc5efe?w=800&q=80",     # Retail price tags / supermarket
    "slide10_fresh_produce.jpg": "https://images.unsplash.com/photo-1583258292688-d0213dc5a3a8?w=800&q=80",# Beautiful organized fresh market
    "slide11_retail_tech.jpg": "https://images.unsplash.com/photo-1553413077-190dd305871c?w=800&q=80",  # Smart warehouse & barcode scanner
}

for filename, url in PHOTOS.items():
    filepath = os.path.join(IMAGE_DIR, filename)
    if not os.path.exists(filepath) or os.path.getsize(filepath) < 1000:
        print(f"Downloading {filename}...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp, open(filepath, "wb") as f:
                f.write(resp.read())
            print(f"Saved {filename} ({os.path.getsize(filepath)} bytes)")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
    else:
        print(f"Already exists: {filename} ({os.path.getsize(filepath)} bytes)")

print("All photographs verified!")
