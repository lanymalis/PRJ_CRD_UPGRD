import pandas as pd
from datetime import datetime

class DataTransformer:
    @staticmethod
    def clean_customer_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocesses customer and transaction DataFrames:
        - Normalizes strings (emails, names)
        - Handles missing values & type casting
        - Derives features (e.g., account tenure, total spend flags)
        """
        df = df.copy()

        # 1. Clean string columns if they exist
        if "email" in df.columns:
            df["email"] = df["email"].astype(str).str.strip().str.lower()
            df["email"] = df["email"].replace(["nan", "none", ""], None)

        if "user_id" in df.columns:
            df["user_id"] = df["user_id"].astype(str).str.strip()

        # 2. Type casting & handling missing numeric values
        if "purchase_history_total" in df.columns:
            df["purchase_history_total"] = pd.to_numeric(df["purchase_history_total"], errors="coerce").fillna(0.0)

        if "is_active_member" in df.columns:
            # Handle boolean casting for various input representations (True/False, 1/0, "True")
            df["is_active_member"] = df["is_active_member"].astype(str).str.lower().isin(["true", "1", "yes"])

        # 3. Feature Engineering / Derived Metrics for Rules
        if "account_created_date" in df.columns:
            df["account_created_date"] = pd.to_datetime(df["account_created_date"], errors="coerce")
            now = pd.Timestamp(datetime.now())
            df["account_age_months"] = ((now - df["account_created_date"]).dt.days // 30).fillna(0).astype(int)
        else:
            df["account_age_months"] = 0

        # Drop duplicate records based on user identifier if present
        if "user_id" in df.columns:
            df = df.drop_duplicates(subset=["user_id"], keep="last")

        return df