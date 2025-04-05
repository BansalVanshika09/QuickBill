import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pandas as pd
import os

# File paths
user_cart_file = "user_cart.xlsx"
products_file = "products_database.xlsx"

# Load or create product database
def load_database(file_name, columns):
    if os.path.exists(file_name):
        return pd.read_excel(file_name, engine="openpyxl")
    else:
        return pd.DataFrame(columns=columns)

# Load databases
products_db = load_database(products_file, ["product_id", "product_name", "stock_quantity", "price", "last_restock_date"])
user_cart = load_database(user_cart_file, ["cart_id", "product_id", "product_name", "quantity", "price", "total_cost"])

# Save function
def save_database(df, file_name):
    df.to_excel(file_name, index=False, engine="openpyxl")

# Function to scan barcode using camera
def scan_barcode(cart_id):
    global user_cart

    cap = cv2.VideoCapture(0)  # Open webcam

    while True:
        _, frame = cap.read()  # Capture frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        barcodes = decode(gray)  # Decode barcodes

        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")  # Extract barcode data
            product_id = barcode_data.strip()

            # Check if product exists in database
            product = products_db[products_db["product_id"] == product_id]
            if product.empty:
                print("❌ Product not found!")
                continue

            product_name = product.iloc[0]["product_name"]
            price = product.iloc[0]["price"]

            # Prompt for quantity
            try:
                quantity = int(input(f"Enter quantity for {product_name}: "))
                total_cost = price * quantity

                # Add to cart
                new_item = {
                    "cart_id": cart_id,
                    "product_id": product_id,
                    "product_name": product_name,
                    "quantity": quantity,
                    "price": price,
                    "total_cost": total_cost
                }

                user_cart = pd.concat([user_cart, pd.DataFrame([new_item])], ignore_index=True)
                save_database(user_cart, user_cart_file)
                print(f"✅ Added {quantity} x {product_name} to cart.")

            except ValueError:
                print("❌ Invalid quantity! Enter a number.")

            cap.release()
            cv2.destroyAllWindows()
            return  # Exit after scanning one barcode

        # Display the camera feed
        cv2.imshow("🔍 Barcode Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    scan_barcode(cart_id="101")
