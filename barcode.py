import cv2
import requests
import json
from pyzbar.pyzbar import decode

# Dummy database (for testing)
ITEM_DATABASE = {
    "0123456789012": {"name": "Coca-Cola 500ml", "price": 1.50},
    "1234567890128": {"name": "Lay’s Chips", "price": 2.00},
    "4002293401102": {"name": "Nutella 750g", "price": 5.50},
}

DROIDCAM_SOURCE = 1  # Change this based on your setup (0 for laptop webcam, 1 for DroidCam)


def fetch_price_from_api(barcode):
    """Fetch price from OpenFoodFacts API (or use a real pricing API)."""
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        product = data.get("product", {})
        name = product.get("product_name", "Unknown Item")
        return {"name": name, "price": "N/A (Use a pricing API)"}
    return None


def get_item_info(barcode):
    """Check local database first, then try API if not found."""
    if barcode in ITEM_DATABASE:
        return ITEM_DATABASE[barcode]

    return fetch_price_from_api(barcode)


def scan_barcode():
    """Capture a barcode using DroidCam instead of a regular webcam."""
    cap = cv2.VideoCapture(DROIDCAM_SOURCE)  # Use DroidCam
    print("Scanning using DroidCam... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to access DroidCam. Make sure it's running!")
            break

        # Decode barcodes in the frame
        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            cap.release()
            cv2.destroyAllWindows()
            return barcode_data

        cv2.imshow("DroidCam Barcode Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None


if __name__ == "__main__":
    barcode = scan_barcode()
    if barcode:
        print(f"✅ Scanned Barcode: {barcode}")
        item_info = get_item_info(barcode)
        if item_info:
            print(f"🛒 Item: {item_info['name']}, 💰 Price: ${item_info['price']}")
        else:
            print("⚠️ Item not found in the database.")
    else:
        print("❌ No barcode detected.")