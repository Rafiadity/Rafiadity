#!/usr/bin/env python3
"""
Simple Inventory Management System
A business application for managing product inventory with CRUD operations.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Product:
    """Represents a product in the inventory."""

    def __init__(self, product_id: int, name: str, category: str,
                 price: float, quantity: int):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict:
        """Convert product to dictionary for JSON serialization."""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'quantity': self.quantity,
            'last_updated': self.last_updated
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Product':
        """Create product from dictionary."""
        product = cls(
            data['product_id'],
            data['name'],
            data['category'],
            data['price'],
            data['quantity']
        )
        product.last_updated = data.get('last_updated', product.last_updated)
        return product

    def __str__(self) -> str:
        """String representation of product."""
        return f"ID: {self.product_id} | {self.name} | {self.category} | ${self.price:.2f} | Qty: {self.quantity}"


class InventoryManager:
    """Manages the inventory system operations."""

    def __init__(self, data_file: str = "inventory_data.json"):
        self.data_file = data_file
        self.products: Dict[int, Product] = {}
        self.next_id = 1
        self.load_data()

    def load_data(self):
        """Load inventory data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.products = {
                        int(k): Product.from_dict(v)
                        for k, v in data.get('products', {}).items()
                    }
                    self.next_id = data.get('next_id', 1)
                print(f"✓ Loaded {len(self.products)} products from {self.data_file}")
            except Exception as e:
                print(f"⚠ Error loading data: {e}")
        else:
            print(f"⚠ No existing data file found. Starting fresh.")

    def save_data(self):
        """Save inventory data to JSON file."""
        try:
            data = {
                'products': {k: v.to_dict() for k, v in self.products.items()},
                'next_id': self.next_id
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Data saved successfully")
        except Exception as e:
            print(f"⚠ Error saving data: {e}")

    def add_product(self, name: str, category: str, price: float, quantity: int) -> Product:
        """Add a new product to inventory."""
        product = Product(self.next_id, name, category, price, quantity)
        self.products[self.next_id] = product
        self.next_id += 1
        self.save_data()
        return product

    def get_product(self, product_id: int) -> Optional[Product]:
        """Get a product by ID."""
        return self.products.get(product_id)

    def update_quantity(self, product_id: int, quantity_change: int) -> bool:
        """Update product quantity (positive to add, negative to remove)."""
        product = self.get_product(product_id)
        if product:
            new_quantity = product.quantity + quantity_change
            if new_quantity < 0:
                print(f"⚠ Cannot set negative quantity. Current: {product.quantity}")
                return False
            product.quantity = new_quantity
            product.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_data()
            return True
        return False

    def update_price(self, product_id: int, new_price: float) -> bool:
        """Update product price."""
        product = self.get_product(product_id)
        if product:
            product.price = new_price
            product.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_data()
            return True
        return False

    def delete_product(self, product_id: int) -> bool:
        """Delete a product from inventory."""
        if product_id in self.products:
            del self.products[product_id]
            self.save_data()
            return True
        return False

    def search_products(self, query: str) -> List[Product]:
        """Search products by name or category."""
        query = query.lower()
        return [
            p for p in self.products.values()
            if query in p.name.lower() or query in p.category.lower()
        ]

    def get_all_products(self) -> List[Product]:
        """Get all products sorted by ID."""
        return sorted(self.products.values(), key=lambda p: p.product_id)

    def generate_report(self) -> Dict:
        """Generate inventory report with statistics."""
        if not self.products:
            return {
                'total_products': 0,
                'total_value': 0.0,
                'low_stock': [],
                'categories': {}
            }

        total_value = sum(p.price * p.quantity for p in self.products.values())
        low_stock = [p for p in self.products.values() if p.quantity < 10]

        categories = {}
        for product in self.products.values():
            if product.category not in categories:
                categories[product.category] = {
                    'count': 0,
                    'total_value': 0.0
                }
            categories[product.category]['count'] += 1
            categories[product.category]['total_value'] += product.price * product.quantity

        return {
            'total_products': len(self.products),
            'total_value': total_value,
            'low_stock': low_stock,
            'categories': categories
        }


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_products(products: List[Product]):
    """Print a list of products in a formatted table."""
    if not products:
        print("  No products found.")
        return

    print(f"\n{'ID':<6} {'Name':<20} {'Category':<15} {'Price':<10} {'Qty':<6}")
    print("-" * 60)
    for product in products:
        print(f"{product.product_id:<6} {product.name:<20} {product.category:<15} ${product.price:<9.2f} {product.quantity:<6}")


def main():
    """Main application loop."""
    inventory = InventoryManager()

    print_header("Inventory Management System")
    print("Welcome! Manage your business inventory with ease.")

    while True:
        print("\n" + "-" * 60)
        print("MENU:")
        print("  1. Add Product")
        print("  2. View All Products")
        print("  3. Search Products")
        print("  4. Update Product Quantity")
        print("  5. Update Product Price")
        print("  6. Delete Product")
        print("  7. Generate Report")
        print("  8. Exit")
        print("-" * 60)

        choice = input("Select an option (1-8): ").strip()

        if choice == '1':
            # Add Product
            print_header("Add New Product")
            try:
                name = input("Product Name: ").strip()
                category = input("Category: ").strip()
                price = float(input("Price: $"))
                quantity = int(input("Quantity: "))

                if price < 0 or quantity < 0:
                    print("⚠ Price and quantity must be non-negative.")
                    continue

                product = inventory.add_product(name, category, price, quantity)
                print(f"✓ Product added successfully! ID: {product.product_id}")
            except ValueError:
                print("⚠ Invalid input. Please enter valid numbers.")

        elif choice == '2':
            # View All Products
            print_header("All Products")
            products = inventory.get_all_products()
            print_products(products)
            if products:
                total_value = sum(p.price * p.quantity for p in products)
                print(f"\nTotal Inventory Value: ${total_value:,.2f}")

        elif choice == '3':
            # Search Products
            print_header("Search Products")
            query = input("Enter search term (name or category): ").strip()
            products = inventory.search_products(query)
            print_products(products)

        elif choice == '4':
            # Update Quantity
            print_header("Update Product Quantity")
            try:
                product_id = int(input("Product ID: "))
                product = inventory.get_product(product_id)
                if product:
                    print(f"Current quantity: {product.quantity}")
                    change = int(input("Enter quantity change (+/-): "))
                    if inventory.update_quantity(product_id, change):
                        print(f"✓ Quantity updated! New quantity: {product.quantity}")
                else:
                    print("⚠ Product not found.")
            except ValueError:
                print("⚠ Invalid input. Please enter valid numbers.")

        elif choice == '5':
            # Update Price
            print_header("Update Product Price")
            try:
                product_id = int(input("Product ID: "))
                product = inventory.get_product(product_id)
                if product:
                    print(f"Current price: ${product.price:.2f}")
                    new_price = float(input("Enter new price: $"))
                    if new_price < 0:
                        print("⚠ Price must be non-negative.")
                        continue
                    if inventory.update_price(product_id, new_price):
                        print(f"✓ Price updated! New price: ${product.price:.2f}")
                else:
                    print("⚠ Product not found.")
            except ValueError:
                print("⚠ Invalid input. Please enter a valid number.")

        elif choice == '6':
            # Delete Product
            print_header("Delete Product")
            try:
                product_id = int(input("Product ID: "))
                product = inventory.get_product(product_id)
                if product:
                    print(f"Product: {product}")
                    confirm = input("Are you sure you want to delete this product? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        if inventory.delete_product(product_id):
                            print("✓ Product deleted successfully!")
                    else:
                        print("Deletion cancelled.")
                else:
                    print("⚠ Product not found.")
            except ValueError:
                print("⚠ Invalid input. Please enter a valid number.")

        elif choice == '7':
            # Generate Report
            print_header("Inventory Report")
            report = inventory.generate_report()
            print(f"\nTotal Products: {report['total_products']}")
            print(f"Total Inventory Value: ${report['total_value']:,.2f}")

            print("\n--- Categories ---")
            for category, data in report['categories'].items():
                print(f"  {category}: {data['count']} products, ${data['total_value']:,.2f}")

            if report['low_stock']:
                print("\n⚠ LOW STOCK ALERTS (< 10 units):")
                print_products(report['low_stock'])
            else:
                print("\n✓ No low stock items.")

        elif choice == '8':
            # Exit
            print("\nThank you for using Inventory Management System!")
            print("Goodbye!")
            break

        else:
            print("⚠ Invalid option. Please select 1-8.")


if __name__ == "__main__":
    main()
