import pandas as pd
import os
from datetime import datetime

# File names for databases
user_cart_file = "user_cart.xlsx"
store_sales_file = "store_sales.xlsx"
products_file = "products_database.xlsx"  # Store inventory

# Function to load a database or create a new one
def load_database(file_name, columns):
    if os.path.exists(file_name):
        return pd.read_excel(file_name, engine="openpyxl")
    else:
        return pd.DataFrame(columns=columns)

# Load or initialize databases
user_cart = load_database(user_cart_file, ["cart_id", "product_id", "product_name", "quantity", "price", "total_cost"])
store_sales = load_database(store_sales_file, ["transaction_id", "customer_name", "items_bought", "total_amount", "date"])
products_db = load_database(products_file, ["product_id", "product_name", "stock_quantity", "price", "last_restock_date"])

# Function to save data to Excel
def save_database(df, file_name):
    df.to_excel(file_name, index=False, engine="openpyxl")

# Function to scan and add products to cart
def scan_product(cart_id):
    global user_cart
    while True:
        product_id = input("\n🔍 Scan Product ID (or type 'done' to finish): ").strip()

        if product_id.lower() == "done":
            break  # Exit scanning

        # Check if product exists
        product = products_db[products_db["product_id"] == product_id]
        if product.empty:
            print("❌ Product not found!")
            continue

        product_name = product.iloc[0]["product_name"]
        price = product.iloc[0]["price"]

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

# Function to checkout and save transaction
def checkout():
    global user_cart, store_sales

    if user_cart.empty:
        print("🛒 Cart is empty! Scan products first.")
        return

    customer_name = input("\n👤 Enter Customer Name: ").strip()
    transaction_id = f"TXN{len(store_sales) + 1:03d}"
    total_amount = user_cart["total_cost"].sum()
    items_bought = ", ".join([f"{row['product_name']} x{row['quantity']}" for _, row in user_cart.iterrows()])
    date = datetime.today().strftime("%Y-%m-%d")

    # Save transaction
    new_transaction = {
        "transaction_id": transaction_id,
        "customer_name": customer_name,
        "items_bought": items_bought,
        "total_amount": total_amount,
        "date": date
    }
    store_sales = pd.concat([store_sales, pd.DataFrame([new_transaction])], ignore_index=True)
    save_database(store_sales, store_sales_file)

    # Clear cart
    user_cart = user_cart[0:0]
    save_database(user_cart, user_cart_file)

    print(f"\n✅ Transaction saved! Customer pays: ${total_amount:.2f}")
    print("🛍️ Thank you for shopping!")

# Function to display cart
def view_cart():
    if user_cart.empty:
        print("🛒 Cart is empty.")
    else:
        print("\n🛍️ Current Cart:")
        print(user_cart)
        print(f"💰 Total: ${user_cart['total_cost'].sum():.2f}")

# Function to view store transactions
def view_sales():
    if store_sales.empty:
        print("📊 No sales recorded yet.")
    else:
        print("\n📊 Store Sales Records:")
        print(store_sales)

# Main menu loop
while True:
    print("\n📲 POS System - Barcode Scanner")
    print("1️⃣ Scan Products")
    print("2️⃣ View Cart")
    print("3️⃣ Checkout")
    print("4️⃣ View Store Sales")
    print("5️⃣ Exit")

    choice = input("Enter your choice (1-5): ").strip()

    if choice == "1":
        scan_product(cart_id="101")  # Unique cart ID for each user
    elif choice == "2":
        view_cart()
    elif choice == "3":
        checkout()
    elif choice == "4":
        view_sales()
    elif choice == "5":
        print("👋 Exiting... Goodbye!")
        break
    else:
        print("❌ Invalid choice! Enter a number between 1 and 5.")
