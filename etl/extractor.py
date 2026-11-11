import pandas as pd
from pathlib import Path
from typing import Dict, Union

class FileExtractor:
    def __init__(self, raw_data_dir: Union[str, Path]):
        
        self.raw_data_dir = Path(raw_data_dir)

    def extract_single_file(self, filename: str, sheet_name: Union[str, int] = 0) -> pd.DataFrame:
        """Extracts data from a single Excel file into a pandas DataFrame."""
        file_path = self.raw_data_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Source file not found: {file_path}")
        
        print(f"Extracting data from: {file_path}")
        return pd.read_excel(file_path, sheet_name=sheet_name)

    def extract_multiple_files(self, file_sheet_mapping: Dict[str, Union[str, int]]) -> Dict[str, pd.DataFrame]:
        """
        Extracts data from multiple Excel files based on a dictionary mapping 
        filename to sheet name/index.
        """
        extracted_data = {}
        for filename, sheet in file_sheet_mapping.items():
            df = self.extract_single_file(filename, sheet_name=sheet)
            key_name = Path(filename).stem  # Use filename without extension as dict key
            extracted_data[key_name] = df
            
        return extracted_data