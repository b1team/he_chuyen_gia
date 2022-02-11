from typing import List, Dict, Any


def cast_value(field: str, value: str):
    _map = {
        "EPS": float,
        "LNST": float,
        "ROE": float,
        "EPS_rating": int,
        "AD_rating": str,
        "RS_rating": int,
        "SMR_rating": str,
        "PRICE": float,
        "REVENUE": float,
    }
    if not field in _map:
        return value
    return _map[field](value)


def check_condition(field_name, operator, condition_value, actual_value):
    value1 = cast_value(field=field_name, value=actual_value)
    value2 = cast_value(field=field_name, value=condition_value)

    if operator == ">":
        return value1 > value2
    elif operator == "<":
        return value1 < value2
    elif operator == "=":
        return value1 == value2
    elif operator == ">=":
        return value1 >= value2
    elif operator == "<=":
        return value1 <= value2
    else:
        return False


def expert_system(rules: List[Dict[str, Any]], data: dict):
    # conditions = [["EPS", ">", "20"], ["ROE", "<", "20"]]
    point = 0
    for rule in rules:
        passed_all_conditions = True
        for condition in rule["conditions"]:
            condition_tuple = tuple(condition)
            field_name, operator, condition_value = condition_tuple
            if field_name in data:
                actual_value = data[field_name]
                try:
                    if not check_condition(
                        field_name, operator, condition_value, actual_value
                    ):
                        passed_all_conditions = False
                        break
                except ValueError:
                    break

        if passed_all_conditions:
            point = point + float(rule["value"])
    return point
