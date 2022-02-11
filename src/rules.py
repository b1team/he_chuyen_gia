from .database import insert_rule, update_rule, delete_rule, find_all_rules


def parse_rules_conditions(conditions: str) -> list:
    result = []
    data = conditions.split('\n')
    for i in data:
        result.append(i.strip().split(' '))

    return result


def parse_rules_subject(subject: str) -> str:
    data = subject.split('\n')
    result = ' & '.join(data)

    return result


def insert_new_rule(name: str, description: str, value: float,
                    conditions_str: str):
    conditions = parse_rules_conditions(conditions_str)

    rule = {
        "name": name,
        "description": description,
        "conditions": conditions,
        "value": value,
    }

    rule_new = insert_rule(rule)

    return rule_new


def update_new_rule(rule_id: str, name: str, description: str, value: float,
                    conditions_str: str):
    conditions = parse_rules_conditions(conditions_str)
    rule = {
        "name": name,
        "description": description,
        "conditions": conditions,
        "value": value
    }

    rule_update = update_rule(rule_id, rule)

    return rule_update


def rule_delete(id: str):
    deleted = delete_rule(id)

    return deleted


def expert_system(data: dict):
    rules = find_all_rules()
    pass
