# Price List Converter

A GUI application for converting supplier XLSX price lists into a unified CSV format with configurable column mapping.

## Features

- **Input Support**: XLSX (Excel) and CSV files
- **Large File Handling**: Automatically splits large files (~1GB) into smaller chunks (~80MB)
- **Configurable Mapping**: JSON-based configuration for each supplier
- **Auto-Detection**: Automatically detects column types based on content patterns
- **Bypass Template**: Option to use original column names without template conversion
- **Lead Time Input**: Separate input field for lead time value (placed in A1 cell)
- **Multiple Sheet Support**: Handles Excel files with multiple sheets
- **Real-time Logging**: Conversion progress and status updates
- **Error Handling**: Gracefully handles missing columns and data issues
- **Multi-language Support**: Detects columns in English and Russian

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
5. **Supplier Config**: Select a pre-configured supplier mapping (only needed if not bypassing template)

### Creating Supplier Configurations

1. Click "Create New Config" button
2. Enter a configuration name
3. Map your input file columns to the required output columns:
   - **Lead Time**: Column containing delivery time information
   - **Brand Name**: Column containing manufacturer/brand names
   - **Article**: Column containing part numbers or article codes
   - **Quantity**: Column containing stock quantities
   - **MOQ**: Column containing minimum order quantities
   - **MSRP**: Column containing manufacturer suggested retail prices
   - **Price**: Column containing actual sale prices

4. Click "Save Configuration"

### Editing Configurations

1. Select an existing configuration from the dropdown
2. Click "Edit Config" button
3. Modify the column mappings as needed
4. Click "Update Configuration"

### Converting Files

#### Option 1: Using Template (Traditional Method)
1. Select input file and output directory
2. Enter lead time value
3. Select a supplier configuration
4. Click "Convert"

#### Option 2: Auto-Detection
1. Select input file and output directory
2. Enter lead time value
3. Enable "Auto-detect columns"
4. Click "Convert" (no supplier config needed)

#### Option 3: Bypass Template
1. Select input file and output directory
2. Enter lead time value
3. Enable "Bypass template"
4. Click "Convert" (uses original column names)

5. Monitor progress in the log area
6. Find converted CSV files in your output directory

## Output Format

The application generates CSV files with:
- **No column headers** - only data rows
- **Lead time value in A1 cell only** (not repeated in data rows)
- **Data columns start from column B** (Brand Name, Article, Quantity, MOQ, MSRP, Price)
- **UTF-8 encoding**
- **Semicolon (;) delimiter**

### Example Output:
```csv
5 days
;Brand A;PN001;100;10;25.99;22.99
;Brand B;PN002;50;5;15.50;13.50
;Brand C;PN003;200;20;45.00;40.00
;Brand D;PN004;75;15;32.75;29.75
```

**Column Structure:**
- **Column A**: Lead time value (A1 cell only), empty in data rows
- **Column B**: Brand Name
- **Column C**: Article
- **Column D**: Quantity
- **Column E**: MOQ
- **Column F**: MSRP
- **Column G**: Price

## File Splitting

For large files (>10,000 rows), the application automatically splits output into multiple files:
- `output_part_1.csv`
- `output_part_2.csv`
- etc.

## Auto-Detection

The application can automatically detect column types based on content patterns. It recognizes:

- **Lead Time**: "lead time", "delivery time", "delivery", "срок поставки", "время доставки"
- **Brand Name**: "brand", "manufacturer", "maker", "бренд", "производитель", "марка"
- **Article**: "article", "part number", "sku", "code", "артикул", "номер детали", "код"
- **Quantity**: "quantity", "stock", "qty", "количество", "запас", "остаток"
- **MOQ**: "moq", "minimum order", "мин заказ", "минимальный заказ"
- **MSRP**: "msrp", "list price", "retail price", "розничная цена", "список цен"
- **Price**: "price", "cost", "sale price", "цена", "стоимость", "продажная цена"

## Configuration Files

Supplier configurations are stored in the `configs/` directory as JSON files. Each file maps input column names to the required output format.

Example configuration:
```json
{
  "Lead Time": "Delivery_Time",
  "Brand Name": "Manufacturer",
  "Article": "Part_Number",
  "Quantity": "Stock_Level",
  "MOQ": "Minimum_Order",
  "MSRP": "List_Price",
  "Price": "Sale_Price"
}
```

## Error Handling

- Missing columns are logged as warnings
- Invalid data rows are skipped
- Conversion errors are displayed in the log
- The application continues processing even with data issues

## Requirements

- Python 3.8+
- pandas
- openpyxl
- tkinter (usually included with Python)

## Troubleshooting

- **Missing columns**: Check your supplier configuration mapping
- **Large files**: Ensure sufficient disk space for output files
- **Encoding issues**: Input files should be in a standard encoding (UTF-8 recommended)
- **Memory issues**: The application processes files in chunks to handle large datasets
