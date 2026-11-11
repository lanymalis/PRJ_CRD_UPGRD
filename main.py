from pathlib import Path
import pandas as pd
from etl.extractor import FileExtractor
from etl.transformer import DataTransformer
from etl.loader import FileLoader
from src.engine import RuleEngine

def main():
    # 1. RUN ETL PIPELINE (Extract -> Transform -> Load)
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")

    print("--- Step 1: Extracting Raw Data ---")
    extractor = FileExtractor(raw_data_dir=raw_dir)
    raw_df = extractor.extract_single_file("customers.xlsx")

    print("\n--- Step 2: Transforming Data ---")
    clean_df = DataTransformer.clean_customer_data(raw_df)
    
    print("\n--- Step 3: Loading Processed Data ---")
    loader = FileLoader(output_dir=processed_dir)
    processed_file_path = loader.save_to_parquet(clean_df, filename="processed_customers.parquet")

    # 4. RUN RULE ENGINE EVALUATION ON PROCESSED DATA
    print("\n--- Step 4: Running Rule Engine Evaluation ---")
    engine = RuleEngine(rule_config_path="rules/rule_config.yaml")

    # Read processed data back as records (dictionaries)
    df_to_evaluate = pd.read_parquet(processed_file_path)
    
    for _, row in df_to_evaluate.iterrows():
        record = row.to_dict()
        user_id = record.get("user_id", "Unknown")
        
        print(f"\nEvaluating User: {user_id} (Spent: ${record.get('purchase_history_total')}, Member: {record.get('is_active_member')})")
        
        decisions = engine.evaluate_record(record)
        if not decisions:
            print(" ➔ No rules matched.")
        for decision in decisions:
            print(f" Matched [{decision['rule_id']}: {decision['rule_name']}]")
            print(f" Outcome: {decision['decision']}")

if __name__ == "__main__":
    main()