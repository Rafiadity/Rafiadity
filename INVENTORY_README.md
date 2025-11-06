# Inventory Management System

A simple, professional business application for managing product inventory with full CRUD operations and a beautiful, intuitive interface.

## Features

### 🎯 Interactive Dashboard
- **Live Statistics**: Real-time overview of inventory value, product count, and categories
- **Visual Bar Charts**: Category breakdown with visual bars showing value distribution
- **Recent Activity Feed**: Track last 5 actions with color-coded icons
- **Stock Alerts**: Instant notifications for low-stock items
- **Quick Metrics**: See your business health at a glance

### 📦 Core Functionality
- **Add Products**: Create new product entries with category suggestions from existing data
- **View Inventory**: Display all products in a beautifully formatted, color-coded table
- **Search Products**: Find products by name or category instantly
- **Browse by Category**: Interactive category browser with product counts
- **Update Stock**: Quick stock adjustments with visual feedback
- **Update Price**: Modify prices with automatic percentage change calculation
- **Delete Products**: Safe deletion with confirmation warnings
- **Generate Reports**: Comprehensive statistics with category breakdowns
- **Data Persistence**: Automatic save/load using JSON file storage

### ⚡ Quick Actions
- **Quick Stock Update**: Fast stock adjustments with recently accessed products displayed
- **Export to CSV**: Export your entire inventory to CSV format for external use
- **Category Browser**: Browse products by category interactively
- **Recent Products**: Quick access to recently viewed/modified products

### 🎨 User Interface Excellence
- **Color-Coded Display**: Visual feedback with colors (green for success, red for errors, yellow for warnings)
- **Box-Drawing Characters**: Professional-looking menus and headers with Unicode box characters
- **Smart Input Helpers**: Context-aware prompts with examples and format hints
- **Stock Level Colors**: Automatic color coding (green = good stock ≥10, yellow = 5-9, red = <5)
- **Activity Tracking**: Every action is logged with timestamps for audit trail
- **Progress Indicators**: Real-time feedback for all operations
- **Clear Screen Management**: Clean transitions between screens for better focus
- **Intuitive Navigation**: Easy keyboard shortcuts (D=Dashboard, Q=Quick Stock, E=Export, X=Exit)

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

## Menu Options

The application features an intuitive menu system with the following options:

- **[D] Dashboard** - View live statistics, activity feed, and stock alerts
- **[1] Add Product** - Create new product entries with category suggestions
- **[2] View All** - Display complete inventory with total value
- **[3] Search** - Find products by name or category
- **[4] By Category** - Browse products organized by category
- **[5] Update Price** - Modify product prices with change tracking
- **[6] Delete Product** - Remove products with safety confirmation
- **[7] Report** - Generate comprehensive inventory reports
- **[Q] Quick Stock** - Fast stock adjustments with recent products shown
- **[E] Export** - Export inventory to CSV format
- **[X] Exit** - Quit the application

## Quick Start Guide

### First-Time Setup
1. Run the application: `python3 inventory_system.py`
2. Start with **[D] Dashboard** to see the overview (empty initially)
3. Press **[1]** to add your first products

### Daily Workflow
1. **Check Dashboard [D]**: Start your day by viewing inventory health
2. **Quick Stock Updates [Q]**: Adjust stock levels as items are sold/received
3. **Browse by Category [4]**: Find products organized by type
4. **Export Data [E]**: Backup your inventory regularly

### Example Session
```
1. Press [D] - View dashboard with live stats
2. Press [1] - Add "Laptop" in "Electronics" for $999, qty 15
3. Press [1] - Add "Mouse" in "Electronics" for $29, qty 50
4. Press [4] - Browse Electronics category (shows 2 products)
5. Press [Q] - Quick update: reduce Laptop stock by 2
6. Press [D] - Dashboard now shows activity and alerts
7. Press [E] - Export to CSV for backup
```

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

The application features a modern, fully interactive terminal interface:

### Main Menu
```
╔════════════════════════════════════════════════════════════════════╗
║              🏪 Inventory Management System                        ║
║              Professional Business Inventory Solution              ║
╚════════════════════════════════════════════════════════════════════╝

  ✓ System ready  |  5 products loaded  |  Data file: inventory_data.json

╔════════════════════════════════════════════════════════════════════╗
║  MAIN MENU                                                         ║
╠════════════════════════════════════════════════════════════════════╣
║  [D] 📊 Dashboard           [5] 💰 Update Price                    ║
║  [1] ➕ Add Product          [6] 🗑️  Delete Product                 ║
║  [2] 📦 View All            [7] 📈 Report                          ║
║  [3] 🔍 Search              [Q] ⚡ Quick Stock                      ║
║  [4] 📂 By Category         [E] 💾 Export                          ║
╠════════════════════════════════════════════════════════════════════╣
║  [X] Exit                                                          ║
╚════════════════════════════════════════════════════════════════════╝

Select option:
```

### Dashboard View
```
╔════════════════════════════════════════════════════════════════════╗
║                         📊 Dashboard                               ║
║                    Live Inventory Overview                         ║
╚════════════════════════════════════════════════════════════════════╝

┌─ Quick Stats ──────────────────────────────────────────────────────┐
  Total Products: 5
  Total Value: $12,499.50
  Categories: 3
  Low Stock Items: 2

┌─ Top Categories ───────────────────────────────────────────────────┐
  1. Electronics      ████████████████░░░░░░░░░░░░░░   $8,500.00
  2. Furniture        ██████████░░░░░░░░░░░░░░░░░░░░   $2,999.50
  3. Office Supplies  ████░░░░░░░░░░░░░░░░░░░░░░░░░░   $1,000.00

┌─ Recent Activity ──────────────────────────────────────────────────┐
  13:45:22 ➕ Added 'Wireless Keyboard' (ID: 6)
  13:44:10 📦 'Laptop' quantity: 15 → 12
  13:42:05 💰 'Office Chair' price: $299.99 → $349.99

┌─ ⚠  Stock Alerts ──────────────────────────────────────────────────┐
  • Gaming Mouse (ID: 3) - Only 4 left
  • USB Cable (ID: 8) - Only 7 left
```

### Visual Features
- **Stock Color Coding**: Green (≥10), Yellow (5-9), Red (<5)
- **Activity Icons**: ➕ Add, 📦 Stock, 💰 Price, 🗑️ Delete
- **Bar Charts**: Visual representation of category values
- **Real-time Feedback**: Instant success/error/warning messages
- **Box Characters**: Professional Unicode frames and dividers
- **Smart Hints**: Contextual help text in dimmed colors

## License

Free to use and modify for any purpose.
