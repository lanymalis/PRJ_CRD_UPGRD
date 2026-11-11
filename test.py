import pandas as pd
from pathlib import Path

# Ensure the directory exists
raw_dir = Path("data/raw")
raw_dir.mkdir(parents=True, exist_ok=True)

# Create mock customer data matching your rule engine expectations
mock_data = {
    "user_id": ["U1001", "U1002", "U1003", "U1004", "U1005"],
    "email": ["  Alice@Example.com ", "BOB@test.org", "charlie@domain.com", "DAVID@SAMPLE.NET", "eve@store.co"],
    "purchase_history_total": [1250.50, 450.00, 0.00, 3200.00, 85.00],
    "is_active_member": [True, True, False, True, False],
    "account_created_date": ["2022-05-10", "2023-01-15", "2024-06-01", "2021-11-20", "2025-01-05"]
}

df = pd.DataFrame(mock_data)

# Save as Excel file
file_path = raw_dir / "customers.xlsx"
df.to_excel(file_path, index=False, sheet_name="Customers")

print(f"Mock Excel file successfully created at: {file_path}")