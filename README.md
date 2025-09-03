# Price List Converter

A simple GUI application to convert supplier XLSX price lists into a unified CSV format.

## Features

- **Simple GUI**: Easy-to-use interface
- **Multiple Formats**: Supports XLSX and CSV input files
- **Configurable**: JSON-based supplier configuration system
- **Auto-Detection**: Automatic column detection
- **Large Files**: Handles large files by splitting into smaller CSVs

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
4. **Conversion Options**:
   - **Auto-detect columns**: Automatically detect column types
   - **Bypass template**: Use original column names without conversion
5. **Supplier Config**: Select a pre-configured supplier mapping

### Creating Supplier Configurations

1. Click "Create New Config" button
2. Enter a configuration name
3. Map your input file columns to the required output columns using column letters (A, B, C, etc.)
4. Click "Save Configuration"

## Output Format

The application generates CSV files with:
- **No column headers** - only data rows
- **Lead time value in A1 cell only** (not repeated in data rows)
- **Data columns start from column B** (Brand Name, Article, Quantity, MOQ, MSRP, Price)
- **UTF-8 encoding**
- **Semicolon (;) delimiter**

## Requirements

- Python 3.8+
- pandas
- openpyxl
- tkinter (usually included with Python)