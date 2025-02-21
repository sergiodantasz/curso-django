def is_non_negative_number(string: str) -> bool:
    try:
        number = float(string)
    except (ValueError, TypeError):
        return False
    return number >= 0
