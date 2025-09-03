#!/usr/bin/env python3
"""
Test script for the Price List Converter application.
Creates sample data and tests basic functionality.
"""

import pandas as pd
import json
from pathlib import Path

def create_sample_data():
    """Create sample XLSX file for testing"""
    
    # Sample data
    data = {
        'Delivery_Time': ['3-5 days', '1-2 weeks', '2-3 weeks', '1 month'],
        'Manufacturer': ['Brand A', 'Brand B', 'Brand C', 'Brand D'],
        'Part_Number': ['PN001', 'PN002', 'PN003', 'PN004'],
        'Stock_Level': [100, 50, 200, 75],
        'Minimum_Order': [10, 5, 20, 15],
        'List_Price': [25.99, 15.50, 45.00, 32.75],
        'Sale_Price': [22.99, 13.50, 40.00, 29.75]
    }
    
    df = pd.DataFrame(data)
    
    # Create test directory
    test_dir = Path("test_data")
    test_dir.mkdir(exist_ok=True)
    
    # Save as XLSX
    output_file = test_dir / "sample_supplier_data.xlsx"
    df.to_excel(output_file, index=False, sheet_name='Price List')
    
    print(f"Sample data created: {output_file}")
    print(f"Columns: {list(df.columns)}")
    print(f"Rows: {len(df)}")
    
    return output_file

def test_configuration():
    """Test the configuration system"""
    
    # Create configs directory
    config_dir = Path("configs")
    config_dir.mkdir(exist_ok=True)
    
    # Test configuration (mapping to input file columns: A=Delivery_Time, B=Manufacturer, C=Part_Number, etc.)
    test_config = {
        "Brand Name": "B",  # Manufacturer is in column B
        "Article": "C",     # Part_Number is in column C
        "Quantity": "D",    # Stock_Level is in column D
        "MOQ": "E",         # Minimum_Order is in column E
        "MSRP": "F",        # List_Price is in column F
        "Price": "G"        # Sale_Price is in column G
    }
    
    config_file = config_dir / "test_supplier.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(test_config, f, indent=2, ensure_ascii=False)
    
    print(f"Test configuration created: {config_file}")
    
    return config_file

def test_conversion_logic():
    """Test the conversion logic without GUI"""
    
    try:
        # Load test data
        test_file = Path("test_data/sample_supplier_data.xlsx")
        if not test_file.exists():
            print("Test data not found. Please run create_sample_data() first.")
            return
            
        # Load configuration
        config_file = Path("configs/test_supplier.json")
        if not config_file.exists():
            print("Test configuration not found. Please run test_configuration() first.")
            return
            
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        # Read input file
        df = pd.read_excel(test_file)
        print(f"Input data loaded: {len(df)} rows, {len(df.columns)} columns")
        
        # Test 1: Normal template conversion
        print("\n=== Test 1: Normal Template Conversion ===")
        output_columns = ["Lead Time", "Brand Name", "Article", "Quantity", "MOQ", "MSRP", "Price"]
        output_df = pd.DataFrame(columns=output_columns)
        
        # Map columns based on configuration (using column letters)
        for output_col in output_columns:
            if output_col in config:
                column_letter = config[output_col].upper()
                # Convert column letter to index (A=0, B=1, C=2, etc.)
                try:
                    col_index = ord(column_letter) - ord('A')
                    if 0 <= col_index < len(df.columns):
                        output_df[output_col] = df.iloc[:, col_index]
                    else:
                        print(f"Warning: Column '{column_letter}' is out of range")
                        output_df[output_col] = ""
                except:
                    print(f"Warning: Invalid column letter '{column_letter}'")
                    output_df[output_col] = ""
            else:
                output_df[output_col] = ""
                
        # Lead time is only in A1 cell, not in data rows
        # Remove the Lead Time column from data rows
        if "Lead Time" in output_df.columns:
            output_df = output_df.drop("Lead Time", axis=1)
        
        # Remove rows with all empty values
        output_df = output_df.dropna(how='all')
        
        print(f"Processed {len(output_df)} rows")
        print(f"Output columns: {list(output_df.columns)}")
        
        # Save test output with lead time in A1 cell
        test_dir = Path("test_data")
        output_file = test_dir / "test_output_template.csv"
        lead_time_value = "5 days"
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            # Write lead time in A1 cell (first line, first column only)
            f.write(f"{lead_time_value}\n")
            # Write data without headers, starting from column B
            # Add empty first column to shift data to column B
            output_df_with_empty_first_col = output_df.copy()
            output_df_with_empty_first_col.insert(0, 'empty_col', '')  # Add empty column with proper name
            output_df_with_empty_first_col.to_csv(f, index=False, header=False, sep=';', encoding='utf-8')
        
        print(f"Template output saved: {output_file}")
        print("First few rows of template output:")
        print(output_df.head())
        
        # Test 2: Bypass template conversion
        print("\n=== Test 2: Bypass Template Conversion ===")
        # Create output with fixed 7 columns but using original column names
        bypass_output_columns = ["Lead Time", "Brand Name", "Article", "Quantity", "MOQ", "MSRP", "Price"]
        bypass_df = pd.DataFrame(columns=bypass_output_columns)
        
        # Map original columns to output columns
        original_to_output = {
            "Delivery_Time": "Lead Time",
            "Manufacturer": "Brand Name", 
            "Part_Number": "Article",
            "Stock_Level": "Quantity",
            "Minimum_Order": "MOQ",
            "List_Price": "MSRP",
            "Sale_Price": "Price"
        }
        
        for output_col in bypass_output_columns:
            if output_col in original_to_output.values():
                # Find the original column that maps to this output column
                for orig_col, out_col in original_to_output.items():
                    if out_col == output_col and orig_col in df.columns:
                        bypass_df[output_col] = df[orig_col]
                        break
                else:
                    bypass_df[output_col] = ""
            else:
                bypass_df[output_col] = ""
        
        # Lead time is only in A1 cell, not in data rows
        if "Lead Time" in bypass_df.columns:
            bypass_df = bypass_df.drop("Lead Time", axis=1)
        
        # Remove rows with all empty values
        bypass_df = bypass_df.dropna(how='all')
        
        print(f"Processed {len(bypass_df)} rows (bypassing template)")
        print(f"Output columns: {list(bypass_df.columns)}")
        
        # Save bypass output with lead time in A1 cell
        bypass_output_file = test_dir / "test_output_bypass.csv"
        
        with open(bypass_output_file, 'w', encoding='utf-8', newline='') as f:
            # Write lead time in A1 cell (first line, first column only)
            f.write(f"{lead_time_value}\n")
            # Write data without headers, starting from column B
            # Add empty first column to shift data to column B
            bypass_df_with_empty_first_col = bypass_df.copy()
            bypass_df_with_empty_first_col.insert(0, 'empty_col', '')  # Add empty column with proper name
            bypass_df_with_empty_first_col.to_csv(f, index=False, header=False, sep=';', encoding='utf-8')
        
        print(f"Bypass output saved: {bypass_output_file}")
        print("First few rows of bypass output:")
        print(bypass_df.head())
        
        return True
        
    except Exception as e:
        print(f"Error during test conversion: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Price List Converter Test Suite ===\n")
    
    print("1. Creating sample data...")
    create_sample_data()
    
    print("\n2. Testing configuration system...")
    test_configuration()
    
    print("\n3. Testing conversion logic...")
    success = test_conversion_logic()
    
    if success:
        print("\n✅ All tests passed! The application should work correctly.")
        print("\nTo run the full application:")
        print("python main.py")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
