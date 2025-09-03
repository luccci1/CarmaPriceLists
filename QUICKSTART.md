# Quick Start Guide

## Running the Application

### Option 1: Using the launcher scripts (Recommended)

**On macOS/Linux:**
```bash
./run_app.sh
```

**On Windows:**
```cmd
run_app.bat
```

### Option 2: Manual setup

1. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## First Time Setup

1. **Create a supplier configuration:**
   - Click "Create New Config" button
   - Enter a name for your supplier (e.g., "Supplier A")
   - Map your input file columns to the required output columns:
     - Lead Time → Column with delivery time info
     - Brand Name → Column with manufacturer names
     - Article → Column with part numbers
     - Quantity → Column with stock levels
     - MOQ → Column with minimum order quantities
     - MSRP → Column with list prices
     - Price → Column with sale prices
   - Click "Save Configuration"

2. **Convert your first file:**
   - Select your XLSX or CSV input file
   - Choose output directory
   - Enter lead time value (will be placed in A1 cell)
   - Select your supplier configuration
   - Click "Convert"

## Sample Data

The application includes sample data for testing:
- **Input file:** `test_data/sample_supplier_data.xlsx`
- **Test configuration:** `test_supplier` (already created)

You can use these to test the application before using your own data.

## Output Format

The application generates CSV files with:
- Fixed column order: Lead Time, Brand Name, Article, Quantity, MOQ, MSRP, Price
- UTF-8 encoding
- Semicolon (;) delimiter
- Lead time value in A1 cell

## Troubleshooting

- **Application won't start:** Make sure Python 3.8+ is installed
- **Missing columns error:** Check your supplier configuration mapping
- **Large files:** The app automatically splits files >10,000 rows
- **Permission errors:** Make sure you have write access to the output directory
