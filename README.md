# Price List Converter

A powerful GUI application to convert supplier XLSX price lists into a unified CSV format with currency conversion and markup capabilities.

## Features

- **Simple GUI**: Easy-to-use interface with modern design
- **Multiple Formats**: Supports XLSX and CSV input files
- **Configurable**: JSON-based supplier configuration system with search
- **Auto-Detection**: Automatic column detection with smart mapping
- **Large Files**: Handles large files by splitting into smaller CSVs (80MB or 1M rows)
- **Currency Conversion**: Convert prices using exchange rates (supports both . and , decimal separators)
- **Markup Calculation**: Add markup percentages to prices
- **Config Management**: Create, edit, and search configurations with creation dates
- **Error Handling**: Clear error messages and validation

## Installation

1. Install Python 3.8 or higher
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main.py
```

### Main Interface

1. **Input File**: Select your XLSX or CSV file to convert
2. **Output Directory**: Choose where to save the converted CSV files
3. **Lead Time**: Enter the lead time value (will be placed in A1 cell)
4. **Currency Rate**: Enter exchange rate for price conversion (e.g., 3.67 or 3,67)
5. **Markup %**: Enter markup percentage to add to prices (e.g., 15 or 15,5)
6. **Conversion Options**:
   - **Auto-detect columns**: Automatically detect column types
   - **Bypass template**: Use original column names without conversion
7. **Supplier Config**: Select a pre-configured supplier mapping with search functionality

### Creating Supplier Configurations

1. Click "Create New Config" button
2. Enter a configuration name
3. Map your input file columns to the required output columns using column letters (A, B, C, etc.)
4. Click "Save Configuration"

## Output Format

The application generates CSV files with:
- **No column headers** - only data rows
- **Lead time value in A1 cell only** (not repeated in data rows)
- **Data columns start from column A** (Brand Name, Article, Quantity, MOQ, MSRP, Price)
- **UTF-8 encoding**
- **Semicolon (;) delimiter**
- **Proper CSV format** with lead time row containing semicolons for all columns

## Processing Order

The application processes data in a strict order:
1. **Mapping**: Extract data from input file using column mappings
2. **Currency Conversion**: Apply exchange rate to MSRP and Price columns (if rate > 0)
3. **Markup Calculation**: Apply markup percentage to MSRP and Price columns (if markup > 0)

## File Splitting

Large files are automatically split when they exceed:
- **80 MB** in size, OR
- **1,000,000 rows**

Split files are named: `filename_output_part_1.csv`, `filename_output_part_2.csv`, etc.

## Error Handling

- **Invalid currency rates**: Clear error messages with examples
- **Invalid markup percentages**: Clear error messages with examples
- **Decimal separators**: Both comma (,) and dot (.) are supported
- **Empty fields**: Safely ignored (no conversion applied)

## Requirements

- Python 3.8+
- pandas
- openpyxl
- tkinter (usually included with Python)