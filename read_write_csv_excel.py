import json
import csv
import os
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CheckExtractor:
    def __init__(self, input_file, output_csv_file, output_excel_file):
        self.input_file = input_file
        self.output_csv_file = output_csv_file
        self.output_excel_file = output_excel_file
        self.extracted_data = []

    # read the input file content
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

    # parse the content to json
    def parse_json(self, content):
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON: {e}")
            raise

    # extracting the checks
    def extract_checks(self, data):
        for check in data:
            check_type = check.get('check_type', 'Unknown')
            failed_checks = check['results'].get('failed_checks', [])

            if failed_checks:
                self._extract_failed_checks(check_type, failed_checks)
            else:
                self._add_passed_check(check_type)

    # extracting failed checks
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

    # passed checks
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

    # writing the extracted data to csv file
    def write_to_csv(self):
        try:
            df = pd.DataFrame(self.extracted_data)
            df['file_line_range'] = df['file_line_range'].apply(lambda x: str(x) if isinstance(x, list) else x)
            df.to_csv(self.output_csv_file, index=False)
            logging.info(f"Data successfully written to {self.output_csv_file}.")
        except Exception as e:
            logging.error(f"Error writing to CSV: {e}")
            raise

    #writing the extracted data to an Excel file
    def write_to_excel(self):
        try:
            df = pd.DataFrame(self.extracted_data)
            df['file_line_range'] = df['file_line_range'].apply(lambda x:str(x) if isinstance(x, list) else x)
            df.to_excel(self.output_excel_file, index=False, sheet_name="Checks Summary")
            logging.info(f"Data successfully written to {self.output_excel_file}.")

        except Exception as e:
            logging.error(f"Error writing to Excel: {e}")
            raise

    # read, parse, write data
    def run(self):
        try:
            logging.info(f"Reading file: {self.input_file}")
            content = self.read_file()

            logging.info("Parsing JSON content..")
            data = self.parse_json(content)

            logging.info("Extracting checks..")
            self.extract_checks(data)

            logging.info("Writing extracted data to CSV..")
            self.write_to_csv()

            logging.info("Writing extracted data to Excel..")
            self.write_to_excel()

            logging.info(f"Process completed successfully. Extracted {len(self.extracted_data)} checks.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")


if __name__ == '__main__':
    input_file = r'C:\Users\praghava\Desktop\BOA\script\chekov-viol.txt'
    output_csv_file = r'C:\Users\praghava\Desktop\BOA\script\checkov-violations-summary.csv'
    output_excel_file = r'C:\Users\praghava\Desktop\BOA\script\checkov-violations-summary.xlsx'
    extractor = CheckExtractor(input_file, output_csv_file, output_excel_file)
    extractor.run()