import pandas as pd
import os

# Define the file name for the Excel database
file_name = "products_database.xlsx"

# Function to initialize or load the database
def load_database():
    if os.path.exists(file_name):
        df = pd.read_excel(file_name, engine="openpyxl")
        df = df.loc[:, ~df.columns.str.contains('^Unnamed', na=False)]  # Remove "Unnamed" columns
        return df
    else:
        columns = ["product_id", "Product Name", "stock_quantity", "price", "last_restock_date"]
        return pd.DataFrame(columns=columns)  # Create new DataFrame if file doesn't exist

# Function to save the database to Excel
def save_database(df):
    print("\n📌 Data being saved to Excel:")
    print(df)  # Debugging step to confirm changes
    df.to_excel(file_name, index=False, engine="openpyxl")  # Use openpyxl to save
    print("\n✅ Database updated and saved to Excel.")

# Function to add multiple products
def input_add_product():
    global products_df
    while True:
        print("\nEnter product details (or type 'done' to finish):")
        product_id = input("Enter Product ID: ").strip()
        
        if product_id.lower() == "done":
            break  # Exit loop when user types "done"

        try:
            product_name = input("Enter product name: ").strip()
            stock_quantity = int(input("Enter Stock Quantity: "))
            price = float(input("Enter Price: "))
            last_restock_date = input("Enter Last Restock Date (YYYY-MM-DD): ").strip()

            if product_id in products_df["product_id"].values:
                print("⚠️ Product already exists! Use update_stock instead.")
                continue

            # Create a new entry
            new_product = {
                "product_id": product_id,
                "Product Name": product_name,
                "stock_quantity": stock_quantity,
                "price": price,
                "last_restock_date": last_restock_date
            }

            # Append new data
            products_df = pd.concat([products_df, pd.DataFrame([new_product])], ignore_index=True)
            save_database(products_df)

        except ValueError:
            print("❌ Invalid input! Please enter numbers for stock and price.")

# Function to update multiple products
def input_update_stock():
    global products_df
    while True:
        print("\nEnter product details to update (or type 'done' to finish):")
        product_id = input("Enter Product ID to update: ").strip()
        
        if product_id.lower() == "done":
            break  # Exit loop when user types "done"

        if product_id not in products_df["product_id"].values:
            print("⚠️ Product not found! Try again.")
            continue  # Skip to next input

        try:
            new_product_name = input("Enter New Product Name: ").strip()
            new_stock = int(input("Enter New Stock Quantity: "))
            new_price = float(input("Enter New Price: "))
            new_date = input("Enter New Restock Date (YYYY-MM-DD): ").strip()

            products_df.loc[products_df["product_id"] == product_id, ["Product Name", "stock_quantity", "price", "last_restock_date"]] = [new_product_name, new_stock, new_price, new_date]
            save_database(products_df)

        except ValueError:
            print("❌ Invalid input! Please enter numbers for stock and price.")

# Function to display all products
def view_products():
    print("\n📦 Current Product Inventory:")
    print(products_df)

# Load the existing database or create a new one
products_df = load_database()

# Main menu loop
while True:
    print("\n📊 Inventory Management System")
    print("1️⃣ Add Products (Multiple Entries)")
    print("2️⃣ Update Stock (Multiple Entries)")
    print("3️⃣ View Products")
    print("4️⃣ Exit")

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
        input_add_product()
    elif choice == "2":
        input_update_stock()
    elif choice == "3":
        view_products()
    elif choice == "4":
        print("👋 Exiting... Goodbye!")
        break
    else:
        print("❌ Invalid choice! Please enter a number between 1 and 4.")
