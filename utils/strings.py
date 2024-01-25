def is_non_negative_number(string: str) -> bool:
    try:
        number = float(string)
    except:
        raise ValueError('The string must have the format of a number.')
    return number >= 0
