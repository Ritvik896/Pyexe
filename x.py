import tkinter as tk
from tkinter import filedialog, ttk
import os
import pandas as pd
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Class for processing the input text file and extracting data
class CheckExtractor:
    def __init__(self, input_file, output_csv_file, output_excel_file):
        self.input_file = input_file
        self.output_csv_file = output_csv_file
        self.output_excel_file = output_excel_file
        self.extracted_data = []

    # Read the input file content
    def read_file(self):
        if not os.path.isfile(self.input_file):
            logging.error(f"File not found: {self.input_file}")
            raise FileNotFoundError(f"File not Found: {self.input_file}")
        with open(self.input_file, 'r') as f:
            try:
                content = f.read()
                return content
            except Exception as e:
                logging.error(f"Error reading the file: {e}")
                raise

    # Parse the content to JSON
    def parse_json(self, content):
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON: {e}")
            raise

    # Extract checks
    def extract_checks(self, data):
        for check in data:
            check_type = check.get('check_type', 'Unknown')
            failed_checks = check['results'].get('failed_checks', [])
            if failed_checks:
                self._extract_failed_checks(check_type, failed_checks)
            else:
                self._add_passed_check(check_type)

    # Extract failed checks
    def _extract_failed_checks(self, check_type, failed_checks):
        for failed_check in failed_checks:
            if failed_check['check_result']['result'] == 'FAILED':
                details = {
                    'check_type': check_type,
                    'check_id': failed_check.get('check_id', 'N/A'),
                    'check_class': failed_check.get('check_class', 'N/A'),
                    'guideline': failed_check.get('guideline', 'N/A'),
                    'resource': failed_check.get('resource', 'N/A'),
                    'file_path': failed_check.get('file_path', 'N/A'),
                    'file_abs_path': failed_check.get('file_abs_path', 'N/A'),
                    'repo_file_path': failed_check.get('repo_file_path', 'N/A'),
                    'file_line_range': failed_check.get('file_line_range', 'N/A'),
                    'status': 'FAILED'
                }
                self.extracted_data.append(details)

    # Add passed checks
    def _add_passed_check(self, check_type):
        self.extracted_data.append({
            'check_type': check_type,
            'check_id': 'N/A',
            'check_class': 'N/A',
            'guideline': 'N/A',
            'resource': 'N/A',
            'file_path': 'N/A',
            'file_abs_path': 'N/A',
            'repo_file_path': 'N/A',
            'file_line_range': 'N/A',
            'status': 'PASSED - No failed checks'
        })

    # Write the extracted data to CSV
    def write_to_csv(self):
        try:
            df = pd.DataFrame(self.extracted_data)
            df['file_line_range'] = df['file_line_range'].apply(lambda x: str(x) if isinstance(x, list) else x)
            df.to_csv(self.output_csv_file, index=False)
            logging.info(f"Data successfully written to {self.output_csv_file}.")
        except Exception as e:
            logging.error(f"Error writing to CSV: {e}")
            raise

    # Write the extracted data to Excel
    def write_to_excel(self):
        try:
            df = pd.DataFrame(self.extracted_data)
            df['file_line_range'] = df['file_line_range'].apply(lambda x: str(x) if isinstance(x, list) else x)
            # Explicitly mention openpyxl as the engine for Excel files
            df.to_excel(self.output_excel_file, index=False, sheet_name="Checks Summary", engine='openpyxl')
            logging.info(f"Data successfully written to {self.output_excel_file}.")
        except Exception as e:
            logging.error(f"Error writing to Excel: {e}")
            raise

    # Read, parse, write data
    def run(self):
        try:
            logging.info(f"Reading file: {self.input_file}")
            content = self.read_file()
            data = self.parse_json(content)
            self.extract_checks(data)
            self.write_to_csv()
            self.write_to_excel()
        except Exception as e:
            logging.error(f"Error during extraction process: {e}")
            raise

# GUI Code
def browse_files():
    file_types = file_type_var.get()

    # Modified code to support multiple file types including .txt
    if file_types == "All Files":
        file_types = [("All Files", "*.*")]
    elif file_types == "PDF Files":
        file_types = [("PDF Files", "*.pdf")]
    elif file_types == "Word Files":
        file_types = [("Word Files", "*.docx")]
    elif file_types == "Excel Files":
        file_types = [("Excel Files", "*.xlsx")]
    elif file_types == "Executable Files":
        file_types = [("Executable Files", "*.exe")]
    elif file_types == "JSON Files":
        file_types = [("JSON Files", "*.json")]
    elif file_types == "Rego Files":
        file_types = [("Rego Files", "*.rego")]
    elif file_types == "Text Files":
        file_types = [("Text Files", "*.txt")]  # Added .txt file support
    else:
        file_types = [("All Files", "*.*")]

    filename = filedialog.askopenfilename(title="Select a File", filetypes=file_types)

    if filename:
        file_label.config(text=f"Selected: {filename}", fg="black")
        global selected_file
        selected_file = filename
    else:
        file_label.config(text="No file selected", fg="red")

def submit_file():
    if 'selected_file' in globals():
        output_csv = selected_file.replace('.txt', '.csv')
        output_excel = selected_file.replace('.txt', '.xlsx')
        extractor = CheckExtractor(selected_file, output_csv, output_excel)
        try:
            extractor.run()
            file_label.config(text=f"CSV and Excel files generated for: {selected_file}", fg="green")
        except Exception as e:
            file_label.config(text=f"Error: {str(e)}", fg="red")
    else:
        file_label.config(text="Please select a file first.", fg="red")

def open_application():
    root = tk.Tk()
    root.title("File Processing Application")
    root.geometry("400x300")
    
    welcome_label = tk.Label(root, text="Welcome to File Processing Application", font=("Arial", 14))
    welcome_label.pack(pady=10)

    global file_type_var
    file_type_var = tk.StringVar(value="All Files")
    file_types = ["All Files", "Text Files", "PDF Files", "Word Files", "Excel Files", "Executable Files", "JSON Files", "Rego Files"]
    
    file_type_label = tk.Label(root, text="Select file type to view:", font=("Arial", 10))
    file_type_label.pack(pady=5)

    file_type_dropdown = ttk.Combobox(root, textvariable=file_type_var, values=file_types, state="readonly")
    file_type_dropdown.pack(pady=5)

    browse_button = tk.Button(root, text="Browse", command=browse_files, font=("Arial", 10), relief="raised", bd=2)
    browse_button.pack(pady=5)

    global file_label
    file_label = tk.Label(root, text="No file selected", font=("Arial", 10))
    file_label.pack(pady=10)

    submit_button = tk.Button(root, text="Submit", command=submit_file, font=("Arial", 10), relief="raised", bd=2)
    submit_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    open_application()
