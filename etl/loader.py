import pandas as pd
from pathlib import Path
from typing import Union

class FileLoader:
    def __init__(self, output_dir: Union[str, Path]):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_to_csv(self, df: pd.DataFrame, filename: str, index: bool = False) -> Path:
        """Saves a DataFrame to a local CSV file."""
        file_path = self.output_dir / filename
        df.to_csv(file_path, index=index)
        print(f"Successfully loaded data to CSV: {file_path}")
        return file_path

    def save_to_parquet(self, df: pd.DataFrame, filename: str, index: bool = False) -> Path:
        """
        Saves a DataFrame to a local Parquet file. 
        Parquet is recommended for performance and preserving exact data types.
        """
        file_path = self.output_dir / filename
        df.to_parquet(file_path, index=index)
        print(f"Successfully loaded data to Parquet: {file_path}")
        return file_path