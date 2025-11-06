#!/usr/bin/env python3
"""
Simple Inventory Management System
A business application for managing product inventory with CRUD operations.
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional


# ANSI Color codes for better UI
class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_BLUE = '\033[44m'

    @staticmethod
    def disable():
        """Disable colors (for non-color terminals)."""
        Colors.RESET = ''
        Colors.BOLD = ''
        Colors.DIM = ''
        Colors.BLACK = Colors.RED = Colors.GREEN = Colors.YELLOW = ''
        Colors.BLUE = Colors.MAGENTA = Colors.CYAN = Colors.WHITE = ''
        Colors.BG_BLACK = Colors.BG_RED = Colors.BG_GREEN = Colors.BG_BLUE = ''


# Detect if terminal supports colors
if not sys.stdout.isatty() or os.getenv('NO_COLOR'):
    Colors.disable()


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
            except Exception as e:
                print(f"{Colors.RED}✗ Error loading data: {e}{Colors.RESET}")

    def save_data(self):
        """Save inventory data to JSON file."""
        try:
            data = {
                'products': {k: v.to_dict() for k, v in self.products.items()},
                'next_id': self.next_id
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"{Colors.RED}✗ Error saving data: {e}{Colors.RESET}")

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


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')


def print_header(title: str, subtitle: str = ""):
    """Print a formatted header with optional subtitle."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}╔{'═' * 68}╗{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.BOLD}{Colors.WHITE}{title:^64}{Colors.RESET}  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    if subtitle:
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.DIM}{subtitle:^64}{Colors.RESET}  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚{'═' * 68}╝{Colors.RESET}")


def print_section(title: str):
    """Print a section divider."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}┌─ {title} {'─' * (60 - len(title))}┐{Colors.RESET}")


def print_success(message: str):
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")


def print_error(message: str):
    """Print an error message."""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")


def print_info(message: str):
    """Print an info message."""
    print(f"{Colors.CYAN}ℹ {message}{Colors.RESET}")


def print_products(products: List[Product], show_header: bool = True):
    """Print a list of products in a formatted table."""
    if not products:
        print(f"\n  {Colors.DIM}No products found.{Colors.RESET}")
        return

    if show_header:
        print(f"\n{Colors.BOLD}{'ID':<6} {'Name':<22} {'Category':<16} {'Price':<12} {'Stock':<8}{Colors.RESET}")
        print(f"{Colors.DIM}{'─' * 70}{Colors.RESET}")

    for product in products:
        # Color code stock levels
        stock_color = Colors.GREEN if product.quantity >= 10 else Colors.YELLOW if product.quantity >= 5 else Colors.RED
        qty_display = f"{stock_color}{product.quantity}{Colors.RESET}"

        print(f"{Colors.CYAN}{product.product_id:<6}{Colors.RESET} "
              f"{product.name:<22} "
              f"{Colors.DIM}{product.category:<16}{Colors.RESET} "
              f"{Colors.GREEN}${product.price:<11.2f}{Colors.RESET} "
              f"{qty_display:<8}")


def get_input(prompt: str, input_type: type = str, default=None, allow_empty: bool = False):
    """Get user input with type validation and optional default."""
    while True:
        try:
            if default is not None:
                user_input = input(f"{prompt} {Colors.DIM}[{default}]{Colors.RESET}: ").strip()
                if not user_input and allow_empty:
                    return default
            else:
                user_input = input(f"{prompt}: ").strip()

            if not user_input:
                if allow_empty:
                    return default if default is not None else None
                print_error("Input cannot be empty. Please try again.")
                continue

            if input_type == str:
                return user_input
            elif input_type == int:
                return int(user_input)
            elif input_type == float:
                return float(user_input)
            else:
                return input_type(user_input)
        except ValueError:
            print_error(f"Invalid input. Please enter a valid {input_type.__name__}.")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Operation cancelled.{Colors.RESET}")
            return None


def pause():
    """Pause and wait for user to press Enter."""
    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")


def main():
    """Main application loop."""
    clear_screen()
    inventory = InventoryManager()

    print_header("🏪 Inventory Management System", "Professional Business Inventory Solution")
    print(f"\n  {Colors.GREEN}✓{Colors.RESET} System ready  |  "
          f"{Colors.CYAN}{len(inventory.products)}{Colors.RESET} products loaded  |  "
          f"{Colors.DIM}Data file: {inventory.data_file}{Colors.RESET}")

    while True:
        print(f"\n{Colors.BOLD}{Colors.CYAN}╔{'═' * 68}╗{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.BOLD}MAIN MENU{Colors.RESET}{' ' * 56}{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}╠{'═' * 68}╣{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.GREEN}[1]{Colors.RESET} Add New Product        {Colors.GREEN}[5]{Colors.RESET} Update Price          {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.GREEN}[2]{Colors.RESET} View All Products      {Colors.GREEN}[6]{Colors.RESET} Delete Product        {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.GREEN}[3]{Colors.RESET} Search Products        {Colors.GREEN}[7]{Colors.RESET} Generate Report       {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.GREEN}[4]{Colors.RESET} Update Stock           {Colors.RED}[Q]{Colors.RESET} Quit                  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚{'═' * 68}╝{Colors.RESET}")

        choice = input(f"\n{Colors.BOLD}Select option{Colors.RESET} {Colors.DIM}(1-7, Q){Colors.RESET}: ").strip().lower()

        if choice == '1':
            # Add Product
            clear_screen()
            print_header("➕ Add New Product")
            print_info("Enter product details below")

            name = get_input(f"\n{Colors.BOLD}Product Name{Colors.RESET}")
            if name is None:
                continue

            category = get_input(f"{Colors.BOLD}Category{Colors.RESET} {Colors.DIM}(e.g., Electronics, Furniture){Colors.RESET}")
            if category is None:
                continue

            price = get_input(f"{Colors.BOLD}Price{Colors.RESET} {Colors.DIM}($){Colors.RESET}", float)
            if price is None:
                continue
            if price < 0:
                print_error("Price must be non-negative.")
                pause()
                continue

            quantity = get_input(f"{Colors.BOLD}Initial Stock{Colors.RESET}", int)
            if quantity is None:
                continue
            if quantity < 0:
                print_error("Quantity must be non-negative.")
                pause()
                continue

            product = inventory.add_product(name, category, price, quantity)
            print()
            print_success(f"Product added successfully! ID: {product.product_id}")
            print(f"\n{Colors.DIM}Product Details:{Colors.RESET}")
            print_products([product])
            pause()

        elif choice == '2':
            # View All Products
            clear_screen()
            print_header("📦 All Products")
            products = inventory.get_all_products()

            if products:
                print_products(products)
                total_value = sum(p.price * p.quantity for p in products)
                print(f"\n{Colors.BOLD}Summary:{Colors.RESET}")
                print(f"  Total Products: {Colors.CYAN}{len(products)}{Colors.RESET}")
                print(f"  Total Value: {Colors.GREEN}${total_value:,.2f}{Colors.RESET}")
            else:
                print_info("No products in inventory yet. Add some to get started!")

            pause()

        elif choice == '3':
            # Search Products
            clear_screen()
            print_header("🔍 Search Products")
            query = get_input(f"\n{Colors.BOLD}Search{Colors.RESET} {Colors.DIM}(name or category){Colors.RESET}")

            if query:
                products = inventory.search_products(query)
                if products:
                    print_success(f"Found {len(products)} product(s)")
                    print_products(products)
                else:
                    print_warning(f"No products found matching '{query}'")

            pause()

        elif choice == '4':
            # Update Quantity
            clear_screen()
            print_header("📊 Update Stock")

            product_id = get_input(f"\n{Colors.BOLD}Product ID{Colors.RESET}", int)
            if product_id is None:
                continue

            product = inventory.get_product(product_id)
            if product:
                print(f"\n{Colors.DIM}Current Product:{Colors.RESET}")
                print_products([product])

                change = get_input(f"\n{Colors.BOLD}Quantity Change{Colors.RESET} {Colors.DIM}(use +/- for add/remove){Colors.RESET}", int)
                if change is None:
                    continue

                if inventory.update_quantity(product_id, change):
                    print()
                    print_success(f"Stock updated! New quantity: {product.quantity}")
                    if product.quantity < 10:
                        print_warning(f"Low stock alert: Only {product.quantity} units remaining")
            else:
                print_error(f"Product ID {product_id} not found.")

            pause()

        elif choice == '5':
            # Update Price
            clear_screen()
            print_header("💰 Update Price")

            product_id = get_input(f"\n{Colors.BOLD}Product ID{Colors.RESET}", int)
            if product_id is None:
                continue

            product = inventory.get_product(product_id)
            if product:
                print(f"\n{Colors.DIM}Current Product:{Colors.RESET}")
                print_products([product])

                new_price = get_input(f"\n{Colors.BOLD}New Price{Colors.RESET} {Colors.DIM}(current: ${product.price:.2f}){Colors.RESET}", float)
                if new_price is None:
                    continue

                if new_price < 0:
                    print_error("Price must be non-negative.")
                else:
                    old_price = product.price
                    if inventory.update_price(product_id, new_price):
                        print()
                        change_pct = ((new_price - old_price) / old_price * 100) if old_price > 0 else 0
                        print_success(f"Price updated: ${old_price:.2f} → ${new_price:.2f} ({change_pct:+.1f}%)")
            else:
                print_error(f"Product ID {product_id} not found.")

            pause()

        elif choice == '6':
            # Delete Product
            clear_screen()
            print_header("🗑️  Delete Product")

            product_id = get_input(f"\n{Colors.BOLD}Product ID{Colors.RESET}", int)
            if product_id is None:
                continue

            product = inventory.get_product(product_id)
            if product:
                print(f"\n{Colors.DIM}Product to delete:{Colors.RESET}")
                print_products([product])

                print(f"\n{Colors.RED}{Colors.BOLD}⚠  WARNING:{Colors.RESET} {Colors.RED}This action cannot be undone!{Colors.RESET}")
                confirm = input(f"Type {Colors.BOLD}'yes'{Colors.RESET} to confirm deletion: ").strip().lower()

                if confirm == 'yes':
                    if inventory.delete_product(product_id):
                        print()
                        print_success("Product deleted successfully.")
                else:
                    print()
                    print_info("Deletion cancelled.")
            else:
                print_error(f"Product ID {product_id} not found.")

            pause()

        elif choice == '7':
            # Generate Report
            clear_screen()
            print_header("📈 Inventory Report", f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            report = inventory.generate_report()

            print_section("Overview")
            print(f"  Total Products: {Colors.CYAN}{Colors.BOLD}{report['total_products']}{Colors.RESET}")
            print(f"  Total Value: {Colors.GREEN}{Colors.BOLD}${report['total_value']:,.2f}{Colors.RESET}")

            if report['categories']:
                print_section("Categories Breakdown")
                for category, data in sorted(report['categories'].items()):
                    print(f"  {Colors.BOLD}{category}{Colors.RESET}")
                    print(f"    → {data['count']} products | ${data['total_value']:,.2f}")

            if report['low_stock']:
                print_section("⚠  Low Stock Alerts (< 10 units)")
                print_products(report['low_stock'])
            else:
                print_section("Stock Status")
                print(f"  {Colors.GREEN}✓ All products have adequate stock{Colors.RESET}")

            pause()

        elif choice in ['8', 'q', 'quit', 'exit']:
            # Exit
            clear_screen()
            print(f"\n{Colors.BOLD}{Colors.CYAN}╔{'═' * 68}╗{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.BOLD}Thank you for using Inventory Management System!{Colors.RESET}{' ' * 17}{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.DIM}All data has been saved automatically.{Colors.RESET}{' ' * 28}{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.CYAN}╚{'═' * 68}╝{Colors.RESET}\n")
            break

        else:
            print_error(f"Invalid option '{choice}'. Please select 1-7 or Q.")
            pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Program interrupted. Goodbye!{Colors.RESET}\n")
        sys.exit(0)
