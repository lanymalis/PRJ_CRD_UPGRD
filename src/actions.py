def apply_discount(row_data: dict, discount_percentage: int) -> dict:
    return {
        "status": "APPROVED",
        "action_taken": "apply_discount",
        "detail": f"Applied {discount_percentage}% member discount."
    }

def restrict_access(row_data: dict, message: str) -> dict:
    return {
        "status": "RESTRICTED",
        "action_taken": "restrict_access",
        "detail": message
    }
