import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import json
import os
from pathlib import Path
import threading
import re
from difflib import SequenceMatcher

class PriceListConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Price List Converter")
        self.root.geometry("800x600")
        
        # Variables
        self.input_file_path = tk.StringVar()
        self.output_directory = tk.StringVar()
        self.lead_time = tk.StringVar(value="0")
        self.supplier_config = tk.StringVar()
        self.config_files = []
        self.bypass_template = tk.BooleanVar(value=False)
        self.auto_detect_columns = tk.BooleanVar(value=True)
        self.detected_columns = {}
        self.input_dataframe = None
        
        self.setup_ui()
        self.load_config_files()
        
    def detect_columns(self, df):
        """Automatically detect which columns match the required output columns"""
        detected = {}
        
        # Define patterns for each column type (more comprehensive)
        patterns = {
            "Lead Time": [
                r"lead\s*time", r"delivery\s*time", r"delivery", r"lead", r"time",
                r"срок\s*поставки", r"время\s*доставки", r"поставка"
            ],
            "Brand Name": [
                r"brand", r"manufacturer", r"maker", r"producer", r"company", r"mfg",
                r"бренд", r"производитель", r"марка", r"фирма"
            ],
            "Article": [
                r"article", r"part\s*number", r"part\s*no", r"sku", r"code", r"item\s*number",
                r"product\s*code", r"model", r"артикул", r"номер\s*детали", r"код", r"товар"
            ],
            "Quantity": [
                r"quantity", r"stock", r"qty", r"amount", r"count", r"available",
                r"avl\s*qty", r"in\s*stock", r"количество", r"запас", r"остаток", r"шт"
            ],
            "MOQ": [
                r"moq", r"minimum\s*order", r"min\s*order", r"min\s*qty", r"min\s*quantity",
                r"мин\s*заказ", r"минимальный\s*заказ", r"мин\s*количество"
            ],
            "MSRP": [
                r"msrp", r"list\s*price", r"retail\s*price", r"rrp", r"price\s*list",
                r"suggested\s*price", r"recommended\s*price", r"total\s*price",
                r"розничная\s*цена", r"список\s*цен", r"рекомендуемая\s*цена"
            ],
            "Price": [
                r"price", r"cost", r"sale\s*price", r"selling\s*price", r"unit\s*price",
                r"unit\s*cost", r"wholesale\s*price", r"цена", r"стоимость", r"продажная\s*цена"
            ]
        }
        
        # Get column names (convert to lowercase for matching)
        columns = [col.lower().strip() for col in df.columns]
        
        for output_col, pattern_list in patterns.items():
            best_match = None
            best_score = 0
            
            for i, col in enumerate(columns):
                for pattern in pattern_list:
                    if re.search(pattern, col, re.IGNORECASE):
                        # Calculate similarity score
                        similarity = SequenceMatcher(None, col, pattern).ratio()
                        if similarity > best_score:
                            best_score = similarity
                            best_match = df.columns[i]  # Use original column name
            
            if best_match and best_score > 0.2:  # Lower threshold for better detection
                detected[output_col] = best_match
                
        return detected
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Input file selection
        ttk.Label(main_frame, text="Input File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_file_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input_file).grid(row=0, column=2, padx=(5, 0), pady=5)
        
        # Output directory selection
        ttk.Label(main_frame, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_directory, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output_directory).grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # Lead Time input
        ttk.Label(main_frame, text="Lead Time:").grid(row=2, column=0, sticky=tk.W, pady=5)
        lead_time_frame = ttk.Frame(main_frame)
        lead_time_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5)
        
        ttk.Entry(lead_time_frame, textvariable=self.lead_time, width=20).pack(side=tk.LEFT)
        ttk.Label(lead_time_frame, text="(This value will be placed in A1 cell)").pack(side=tk.LEFT, padx=(10, 0))
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Conversion Options", padding="5")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(1, weight=1)
        
        # Auto-detect columns option
        ttk.Checkbutton(options_frame, text="Auto-detect columns", 
                       variable=self.auto_detect_columns,
                       command=self.toggle_auto_detect).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Bypass template option
        ttk.Checkbutton(options_frame, text="Bypass template (use original column names)", 
                       variable=self.bypass_template,
                       command=self.toggle_bypass_template).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # Supplier configuration selection
        ttk.Label(main_frame, text="Supplier Config:").grid(row=4, column=0, sticky=tk.W, pady=5)
        config_combo = ttk.Combobox(main_frame, textvariable=self.supplier_config, state="readonly", width=47)
        config_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5)
        config_combo['values'] = self.config_files
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Convert", command=self.start_conversion, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Create New Config", command=self.create_config_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Config", command=self.edit_config_window).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to convert")
        self.status_label.grid(row=7, column=0, columnspan=3, pady=5)
        
        # Log text area
        log_frame = ttk.LabelFrame(main_frame, text="Conversion Log", padding="5")
        log_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=15, width=80)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure main frame row weights
        main_frame.rowconfigure(8, weight=1)
        
    def toggle_auto_detect(self):
        """Toggle auto-detection and update UI accordingly"""
        if self.auto_detect_columns.get() and self.input_file_path.get():
            self.analyze_input_file()
    
    def toggle_bypass_template(self):
        """Toggle bypass template option"""
        if self.bypass_template.get():
            self.auto_detect_columns.set(True)
            if self.input_file_path.get():
                self.analyze_input_file()
    
    def analyze_input_file(self):
        """Analyze the input file and detect columns"""
        try:
            if not self.input_file_path.get():
                return
                
            input_path = Path(self.input_file_path.get())
            if input_path.suffix.lower() == '.xlsx':
                df = pd.read_excel(input_path)
            else:
                df = pd.read_csv(input_path)
                
            self.input_dataframe = df
            self.detected_columns = self.detect_columns(df)
            
            # Log detected columns
            self.log_message(f"Analyzed input file: {len(df)} rows, {len(df.columns)} columns")
            if self.detected_columns:
                self.log_message("Auto-detected columns:")
                for output_col, input_col in self.detected_columns.items():
                    self.log_message(f"  {output_col} → {input_col}")
            else:
                self.log_message("No columns could be auto-detected")
                
        except Exception as e:
            self.log_message(f"Error analyzing input file: {str(e)}")
    
    def browse_input_file(self):
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.input_file_path.set(filename)
            if self.auto_detect_columns.get():
                self.analyze_input_file()
            
    def browse_output_directory(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_directory.set(directory)
            
    def load_config_files(self):
        config_dir = Path("configs")
        if config_dir.exists():
            self.config_files = [f.stem for f in config_dir.glob("*.json")]
        else:
            self.config_files = []
            
    def create_config_window(self):
        self.config_window = tk.Toplevel(self.root)
        self.config_window.title("Create New Configuration")
        self.config_window.geometry("600x500")
        
        self.setup_config_ui()
        
    def setup_config_ui(self):
        main_frame = ttk.Frame(self.config_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuration name
        ttk.Label(main_frame, text="Configuration Name:").pack(anchor=tk.W)
        config_name_entry = ttk.Entry(main_frame, width=50)
        config_name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Column mapping
        ttk.Label(main_frame, text="Column Mapping:").pack(anchor=tk.W)
        
        mapping_frame = ttk.Frame(main_frame)
        mapping_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Required columns (without Lead Time since it's only in A1)
        required_columns = ["Brand Name", "Article", "Quantity", "MOQ", "MSRP", "Price"]
        
        self.mapping_entries = {}
        
        for i, col in enumerate(required_columns):
            row_frame = ttk.Frame(mapping_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            # Show column letter (B, C, D, E, F, G)
            column_letter = chr(66 + i)  # B=66, C=67, etc.
            ttk.Label(row_frame, text=f"{col} (Output Col {column_letter}):", width=25).pack(side=tk.LEFT)
            entry = ttk.Entry(row_frame, width=10)
            entry.pack(side=tk.LEFT, padx=(5, 0))
            ttk.Label(row_frame, text="Enter input column letter (A, B, C, etc.)", font=("TkDefaultFont", 8)).pack(side=tk.LEFT, padx=(5, 0))
            self.mapping_entries[col] = entry
            
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Save Configuration", 
                  command=lambda: self.save_config(config_name_entry.get())).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", 
                  command=self.config_window.destroy).pack(side=tk.LEFT, padx=5)
        
    def save_config(self, config_name):
        if not config_name:
            messagebox.showerror("Error", "Please enter a configuration name")
            return
            
        config = {}
        for col, entry in self.mapping_entries.items():
            value = entry.get().strip()
            if value:
                config[col] = value
                
        if len(config) < 3:  # At least 3 columns should be mapped
            messagebox.showerror("Error", "Please map at least 3 columns")
            return
            
        # Create configs directory if it doesn't exist
        config_dir = Path("configs")
        config_dir.mkdir(exist_ok=True)
        
        # Save configuration
        config_file = config_dir / f"{config_name}.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        messagebox.showinfo("Success", f"Configuration '{config_name}' saved successfully")
        self.load_config_files()
        # Update the combobox values
        config_combo = None
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Combobox):
                        config_combo = child
                        break
        if config_combo:
            config_combo['values'] = self.config_files
        self.config_window.destroy()
        
    def edit_config_window(self):
        if not self.supplier_config.get():
            messagebox.showwarning("Warning", "Please select a configuration to edit")
            return
            
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title(f"Edit Configuration: {self.supplier_config.get()}")
        self.edit_window.geometry("600x500")
        
        self.setup_edit_ui()
        
    def setup_edit_ui(self):
        # Load existing configuration
        config_file = Path("configs") / f"{self.supplier_config.get()}.json"
        with open(config_file, 'r', encoding='utf-8') as f:
            existing_config = json.load(f)
            
        main_frame = ttk.Frame(self.edit_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Column mapping
        ttk.Label(main_frame, text="Column Mapping:").pack(anchor=tk.W)
        
        mapping_frame = ttk.Frame(main_frame)
        mapping_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        required_columns = ["Brand Name", "Article", "Quantity", "MOQ", "MSRP", "Price"]
        
        self.edit_mapping_entries = {}
        
        for i, col in enumerate(required_columns):
            row_frame = ttk.Frame(mapping_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            # Show column letter (B, C, D, E, F, G)
            column_letter = chr(66 + i)  # B=66, C=67, etc.
            ttk.Label(row_frame, text=f"{col} (Output Col {column_letter}):", width=25).pack(side=tk.LEFT)
            entry = ttk.Entry(row_frame, width=10)
            entry.pack(side=tk.LEFT, padx=(5, 0))
            ttk.Label(row_frame, text="Enter input column letter (A, B, C, etc.)", font=("TkDefaultFont", 8)).pack(side=tk.LEFT, padx=(5, 0))
            entry.insert(0, existing_config.get(col, ""))
            self.edit_mapping_entries[col] = entry
            
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Update Configuration", 
                  command=lambda: self.update_config(existing_config)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", 
                  command=self.edit_window.destroy).pack(side=tk.LEFT, padx=5)
        
    def update_config(self, existing_config):
        config = {}
        for col, entry in self.edit_mapping_entries.items():
            value = entry.get().strip()
            if value:
                config[col] = value
                
        if len(config) < 3:
            messagebox.showerror("Error", "Please map at least 3 columns")
            return
            
        # Update configuration
        config_file = Path("configs") / f"{self.supplier_config.get()}.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        messagebox.showinfo("Success", f"Configuration '{self.supplier_config.get()}' updated successfully")
        self.load_config_files()
        # Update the combobox values
        config_combo = None
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Combobox):
                        config_combo = child
                        break
        if config_combo:
            config_combo['values'] = self.config_files
        self.edit_window.destroy()
        
    def start_conversion(self):
        if not self.input_file_path.get():
            messagebox.showerror("Error", "Please select an input file")
            return
            
        if not self.output_directory.get():
            messagebox.showerror("Error", "Please select an output directory")
            return
            
        # Check if we need a supplier config (only if not bypassing template)
        if not self.bypass_template.get() and not self.supplier_config.get():
            messagebox.showerror("Error", "Please select a supplier configuration or enable 'Bypass template'")
            return
            
        # Start conversion in a separate thread
        self.progress.start()
        self.status_label.config(text="Converting...")
        
        thread = threading.Thread(target=self.convert_file)
        thread.daemon = True
        thread.start()
        
    def convert_file(self):
        try:
            self.log_message("Starting conversion...")
            
            # Determine configuration source
            if self.bypass_template.get():
                # Use auto-detected columns or original column names
                if self.auto_detect_columns.get() and self.detected_columns:
                    config = self.detected_columns
                    self.log_message("Using auto-detected column mapping")
                else:
                    # Use original column names as-is
                    if self.input_dataframe is not None:
                        df = self.input_dataframe
                    else:
                        input_path = Path(self.input_file_path.get())
                        if input_path.suffix.lower() == '.xlsx':
                            df = pd.read_excel(input_path)
                        else:
                            df = pd.read_csv(input_path)
                    
                    # Create config that maps original columns to themselves
                    config = {}
                    for col in df.columns:
                        config[col] = col
                    self.log_message("Using original column names (bypassing template)")
            else:
                # Load configuration from file
                config_file = Path("configs") / f"{self.supplier_config.get()}.json"
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.log_message(f"Loaded configuration: {self.supplier_config.get()}")
            
            # Read input file if not already loaded
            if self.input_dataframe is None:
                input_path = Path(self.input_file_path.get())
                if input_path.suffix.lower() == '.xlsx':
                    # Read Excel file
                    excel_file = pd.ExcelFile(input_path)
                    if len(excel_file.sheet_names) > 1:
                        self.log_message(f"Multiple sheets found: {excel_file.sheet_names}")
                        # Process first sheet for now, can be enhanced to process all
                        df = pd.read_excel(input_path, sheet_name=0)
                    else:
                        df = pd.read_excel(input_path)
                else:
                    # Read CSV file
                    df = pd.read_csv(input_path)
            else:
                df = self.input_dataframe
                
            self.log_message(f"Input file loaded: {len(df)} rows, {len(df.columns)} columns")
            
            # Process data
            processed_data = self.process_dataframe(df, config)
            
            # Generate output
            self.generate_output(processed_data, self.input_file_path.get())
            
            self.log_message("Conversion completed successfully!")
            
            # Update UI in main thread
            self.root.after(0, self.conversion_completed)
            
        except Exception as e:
            error_msg = f"Error during conversion: {str(e)}"
            self.log_message(error_msg)
            self.root.after(0, lambda: self.conversion_error(error_msg))
            
    def process_dataframe(self, df, config):
        # Always use the fixed 7-column template structure
        output_columns = ["Lead Time", "Brand Name", "Article", "Quantity", "MOQ", "MSRP", "Price"]
        output_df = pd.DataFrame(columns=output_columns)
        
        if self.bypass_template.get():
            # Bypass template: use auto-detected columns or intelligent mapping
            if self.auto_detect_columns.get() and self.detected_columns:
                # Use auto-detected mapping
                config = self.detected_columns
                self.log_message("Using auto-detected column mapping")
            else:
                # Intelligent mapping based on column content and position
                config = {}
                columns = [col.lower().strip() for col in df.columns]
                
                for i, col in enumerate(columns):
                    column_letter = chr(65 + i)  # A, B, C, etc.
                    
                    # Smart mapping based on column name patterns
                    if any(word in col for word in ['part', 'sku', 'code', 'article', 'item', 'product']):
                        config["Article"] = column_letter
                    elif any(word in col for word in ['brand', 'manufacturer', 'maker', 'mfg', 'company']):
                        config["Brand Name"] = column_letter
                    elif any(word in col for word in ['quantity', 'stock', 'qty', 'amount', 'count', 'available']):
                        config["Quantity"] = column_letter
                    elif any(word in col for word in ['moq', 'minimum', 'min']):
                        config["MOQ"] = column_letter
                    elif any(word in col for word in ['msrp', 'list', 'retail', 'recommended', 'suggested']):
                        config["MSRP"] = column_letter
                    elif any(word in col for word in ['price', 'cost', 'unit', 'selling']):
                        config["Price"] = column_letter
                    elif any(word in col for word in ['lead', 'delivery', 'time']):
                        config["Lead Time"] = column_letter
                
                # Fallback to position-based mapping if smart mapping didn't work
                if not config:
                    for i, col in enumerate(df.columns):
                        column_letter = chr(65 + i)
                        if i == 0:  # First column - usually Article/Part Number
                            config["Article"] = column_letter
                        elif i == 1:  # Second column - usually Brand
                            config["Brand Name"] = column_letter
                        elif i == 2:  # Third column - usually Description (skip)
                            continue
                        elif i == 3:  # Fourth column - usually Quantity
                            config["Quantity"] = column_letter
                        elif i == 4:  # Fifth column - usually Price
                            config["Price"] = column_letter
                        elif i == 5:  # Sixth column - usually MSRP or another price
                            config["MSRP"] = column_letter
                
                self.log_message("Using intelligent column mapping (bypassing template)")
        
        # Map columns based on configuration (using column letters)
        for output_col in output_columns:
            if output_col in config:
                column_letter = config[output_col].upper()
                # Convert column letter to index (A=0, B=1, C=2, etc.)
                try:
                    col_index = ord(column_letter) - ord('A')
                    if 0 <= col_index < len(df.columns):
                        output_df[output_col] = df.iloc[:, col_index]
                        self.log_message(f"Mapped {output_col} → Column {column_letter} ({df.columns[col_index]})")
                    else:
                        self.log_message(f"Warning: Column '{column_letter}' is out of range (file has {len(df.columns)} columns)")
                        output_df[output_col] = ""
                except Exception as e:
                    self.log_message(f"Warning: Invalid column letter '{column_letter}': {str(e)}")
                    output_df[output_col] = ""
            else:
                self.log_message(f"Warning: No mapping found for '{output_col}'")
                output_df[output_col] = ""
                
        # Lead time is only in A1 cell, not in data rows
        # Remove the Lead Time column from data rows
        if "Lead Time" in output_df.columns:
            output_df = output_df.drop("Lead Time", axis=1)
        
        # Remove rows with all empty values
        output_df = output_df.dropna(how='all')
        
        self.log_message(f"Processed {len(output_df)} rows")
        return output_df
        
    def generate_output(self, df, input_file_path):
        output_dir = Path(self.output_directory.get())
        
        # Get lead time value for A1 cell
        lead_time_value = self.lead_time.get()
        
        # Extract input filename without extension and create output filename
        input_path = Path(input_file_path)
        input_name = input_path.stem  # filename without extension
        output_base_name = f"{input_name}_output"
        
        # Split into chunks if file is large (target ~80MB)
        chunk_size = 10000  # Adjust based on actual data size
        
        if len(df) > chunk_size:
            num_chunks = (len(df) + chunk_size - 1) // chunk_size
            self.log_message(f"Splitting into {num_chunks} files...")
            
            for i in range(num_chunks):
                start_idx = i * chunk_size
                end_idx = min((i + 1) * chunk_size, len(df))
                chunk_df = df.iloc[start_idx:end_idx]
                
                output_file = output_dir / f"{output_base_name}_part_{i+1}.csv"
                self.write_csv_with_lead_time(chunk_df, output_file, lead_time_value)
                self.log_message(f"Created: {output_file}")
        else:
            output_file = output_dir / f"{output_base_name}.csv"
            self.write_csv_with_lead_time(df, output_file, lead_time_value)
            self.log_message(f"Created: {output_file}")
    
    def write_csv_with_lead_time(self, df, output_file, lead_time_value):
        """Write CSV file with lead time in A1 cell and data starting from column B"""
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            # Write lead time in A1 cell (first line, first column only)
            if lead_time_value:
                f.write(f"{lead_time_value}\n")
            else:
                f.write("\n")  # Empty A1 cell if no lead time specified
            
            # Write data without headers, starting from column B
            # Add empty first column to shift data to column B
            df_with_empty_first_col = df.copy()
            df_with_empty_first_col.insert(0, '', '')  # Add empty column with empty name
            
            df_with_empty_first_col.to_csv(f, index=False, header=False, sep=';', encoding='utf-8')
            
    def log_message(self, message):
        timestamp = pd.Timestamp.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Update log in main thread
        self.root.after(0, lambda: self.update_log(log_entry))
        
    def update_log(self, message):
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        
    def conversion_completed(self):
        self.progress.stop()
        self.status_label.config(text="Conversion completed successfully!")
        messagebox.showinfo("Success", "Price list conversion completed successfully!")
        
    def conversion_error(self, error_msg):
        self.progress.stop()
        self.status_label.config(text="Conversion failed!")
        messagebox.showerror("Error", error_msg)

def main():
    root = tk.Tk()
    app = PriceListConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
