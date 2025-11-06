# Inventory Management System

A simple, professional business application for managing product inventory with full CRUD operations.

## Features

- **Add Products**: Create new product entries with name, category, price, and quantity
- **View Inventory**: Display all products in a formatted table
- **Search**: Find products by name or category
- **Update Quantity**: Adjust stock levels (add or remove items)
- **Update Price**: Modify product prices
- **Delete Products**: Remove items from inventory
- **Generate Reports**: View statistics including total value, categories, and low-stock alerts
- **Data Persistence**: Automatic save/load using JSON file storage

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Ensure Python 3 is installed:
   ```bash
   python3 --version
   ```

2. Make the script executable (optional):
   ```bash
   chmod +x inventory_system.py
   ```

## Usage

Run the application:
```bash
python3 inventory_system.py
```

Or if you made it executable:
```bash
./inventory_system.py
```

## Quick Start Example

1. **Add some products**:
   - Select option 1
   - Enter product details (e.g., "Laptop", "Electronics", 999.99, 15)
   - Add more products to build your inventory

2. **View all products**:
   - Select option 2 to see your complete inventory

3. **Search for products**:
   - Select option 3
   - Enter a search term (e.g., "Electronics")

4. **Generate a report**:
   - Select option 7 to see inventory statistics and low-stock alerts

## Data Storage

- Inventory data is saved to `inventory_data.json` in the current directory
- Data is automatically saved after each operation
- The file is created automatically on first use

## Business Use Cases

This application is suitable for:
- Small retail stores
- Warehouse inventory tracking
- Office supply management
- Small business stock control
- Educational purposes and prototyping

## Features in Detail

### Low Stock Alerts
Products with quantity less than 10 units are flagged in the inventory report.

### Category Reports
View total products and value grouped by category.

### Audit Trail
Each product tracks its last update timestamp.

### Input Validation
- Prevents negative prices and quantities
- Validates numeric inputs
- Confirms deletions to prevent accidents

## Example Session

```
Select an option (1-8): 1
Product Name: Wireless Mouse
Category: Electronics
Price: $29.99
Quantity: 50
✓ Product added successfully! ID: 1

Select an option (1-8): 2
ID     Name                 Category        Price      Qty
------------------------------------------------------------
1      Wireless Mouse       Electronics     $29.99     50

Total Inventory Value: $1,499.50
```

## License

Free to use and modify for any purpose.
