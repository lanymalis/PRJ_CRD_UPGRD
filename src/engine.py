import yaml
from pathlib import Path
from src import actions

class RuleEngine:
    def __init__(self, rule_config_path: str):
        with open(rule_config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.action_registry = {
            "apply_discount": actions.apply_discount,
            "restrict_access": actions.restrict_access
        }

    def evaluate_record(self, record: dict, rule_set_name: str = "tier_evaluation") -> list:
        rule_list = self.config.get("rules", {}).get(rule_set_name, [])
        triggered_decisions = []

        for rule in rule_list:
            try:
                is_matched = eval(rule["condition"], {"__builtins__": {}}, record)
                if is_matched:
                    action_fn = self.action_registry.get(rule["action"])
                    if action_fn:
                        result = action_fn(record, **rule.get("parameters", {}))
                        triggered_decisions.append({
                            "rule_id": rule["id"],
                            "rule_name": rule["name"],
                            "decision": result
                        })
            except Exception as e:
                print(f"Error evaluating rule {rule['id']}: {e}")

        return triggered_decisions
