# Inventory Management System

A simple, professional business application for managing product inventory with full CRUD operations and a beautiful, intuitive interface.

## Features

### Core Functionality
- **Add Products**: Create new product entries with name, category, price, and quantity
- **View Inventory**: Display all products in a beautifully formatted table
- **Search**: Find products by name or category
- **Update Quantity**: Adjust stock levels (add or remove items)
- **Update Price**: Modify product prices with percentage change tracking
- **Delete Products**: Remove items from inventory with confirmation
- **Generate Reports**: View statistics including total value, categories, and low-stock alerts
- **Data Persistence**: Automatic save/load using JSON file storage

### User Interface Enhancements
- **Color-Coded Display**: Visual feedback with colors (green for success, red for errors, yellow for warnings)
- **Box-Drawing Characters**: Professional-looking menus and headers with Unicode box characters
- **Smart Input Helpers**: Context-aware prompts with examples and format hints
- **Stock Level Colors**: Automatic color coding (green = good stock, yellow = low, red = critical)
- **Progress Indicators**: Real-time feedback for all operations
- **Clear Screen Management**: Clean transitions between screens for better focus
- **Keyboard Shortcuts**: Quick navigation with number keys and 'Q' to quit

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

## User Interface Preview

The application features a modern, color-coded terminal interface:

```
╔════════════════════════════════════════════════════════════════════╗
║              🏪 Inventory Management System                        ║
║              Professional Business Inventory Solution              ║
╚════════════════════════════════════════════════════════════════════╝

  ✓ System ready  |  5 products loaded  |  Data file: inventory_data.json

╔════════════════════════════════════════════════════════════════════╗
║  MAIN MENU                                                         ║
╠════════════════════════════════════════════════════════════════════╣
║  [1] Add New Product        [5] Update Price                       ║
║  [2] View All Products      [6] Delete Product                     ║
║  [3] Search Products        [7] Generate Report                    ║
║  [4] Update Stock           [Q] Quit                               ║
╚════════════════════════════════════════════════════════════════════╝

Select option (1-7, Q):
```

### Visual Features
- Stock levels are color-coded: **Green** (10+), **Yellow** (5-9), **Red** (<5)
- Success messages appear in green with checkmarks
- Warnings appear in yellow with alert symbols
- Errors appear in red with X symbols
- Box-drawing characters create professional-looking frames

## License

Free to use and modify for any purpose.
